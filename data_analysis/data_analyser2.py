import os
import logging
import sqlite3
import mysql.connector
import sys
from datetime import datetime

from data_analysis.src.irame_da.llmtools import openaiapi as openai, tools
from data_analysis.src.irame_da.agents.react import make_react_agent
from data_analysis.src.irame_da.agents.helpers import check_question,question_generator,question_generator2
from data_analysis.src.irame_da.db.sqlite_utils import get_db_creation_sql
from data_analysis.src.irame_da.db.mysql_utils import get_db_creation_mysql
from data_analysis.vectordb import VectorStore
from dotenv import find_dotenv, load_dotenv
from data_analysis.data_visualisation import DataVisualiser
from pathlib import Path
import csv
import re
import io
import base64
import json





env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


class DataAnalyser:
    def __init__(self, db_type="sqlite",socketio=None):
        self.db_type = db_type
        self.socketio = socketio
        self.DV=DataVisualiser()
        self.vdb=VectorStore()

        # Set the OpenAI API key from environment variable
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Logging setup
        logging.basicConfig(
            stream=sys.stdout,
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %H:%M:%S'
        )
        logging.getLogger('agent').setLevel(logging.DEBUG)
        self.log = logging.getLogger('agent')
        
        self.MAX_LLM_CALLS_PER_INTERACTION = 10


    def log_to_file(self, filename, user_query, messages):
        """Logs the user query and messages to a text file."""
        with open(filename, 'a') as file:
            file.write(f"User Query: {user_query}\n")
            for idx, message in enumerate(messages, 1):
                file.write(f"Message {idx}: {message}\n")
            file.write("\n")  # Separate different user queries with a newline


    def show_answer(self, answer):
        if self.socketio:
            self.socketio.emit('show_answer', {'answer': answer})

    def show_suggestions(self, suggestions):
        if self.socketio:
            self.socketio.emit('show_suggestions', {'suggestions': suggestions})

    def show_graph(self, base64_image):
        print("Emitting graph...")
        if self.socketio:
            self.socketio.emit('show_graph', {'image': base64_image})

    def show_insight(self, insights):
        # Check if insights is a string and try to load it as JSON
        if isinstance(insights, str):
            try:
                insights = json.loads(insights)
            except json.JSONDecodeError:
                print("Failed to decode insights JSON string.")
                return

        # Now, check if the loaded/passed insights is a dictionary with an 'insights' key
        if isinstance(insights, dict) and 'insights' in insights:
            if self.socketio:
                formatted_insights = []
                for insight in insights['insights']:
                    formatted_insight = f"<strong>{insight['insight_title']}</strong> : {insight['insight_description']}"
                    formatted_insights.append(formatted_insight)
                self.socketio.emit('show_insight', {'insights': formatted_insights})
        else:
            print("Insights is not in the expected format.")


    def store_last_query_data(self,query_data):
        """Sends the last user query data to the frontend."""
        if self.socketio:
            self.socketio.emit('store_last_query_data', {'lastQueryData': query_data})


    
    def connect_to_database(self):
        """Establishes a connection to the database."""
        if self.db_type == "sqlite":
            return sqlite3.connect('data/synthbank.db')
        elif self.db_type == "mysql":
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="sqluser",
                    passwd="password",
                    database="travelDB",
                    autocommit=True  # Automatically commit changes
                )
                return connection
            except mysql.connector.Error as err:
                print(f"Database connection failed: {err}")
                sys.exit(1) 


    def execute_sql_query(self, sql_query):
        """Executes the provided SQL query and returns the result."""
        db_connection = self.connect_to_database()
        cursor = db_connection.cursor()
        
        try:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            return None
        finally:
            cursor.close()
            db_connection.close()



    def generate_suggestions(self,user_query,schema_description,model,function_descriptions):
        queries=[user_query]
        history_suggestions=self.vdb.query_vdb(user_query,n=10,collection_name="travel_sample2_suggestions")
        history_queries=self.vdb.query_vdb(user_query,n=10,collection_name="travel_sample2")
        history_suggestions.update(history_queries)

        
        for hsuggestion in history_suggestions:
            self.show_suggestions(hsuggestion)
            queries.append(hsuggestion)
        
        suggestions_count=len(history_suggestions)

        if(suggestions_count<8):
            qcount=str(8-suggestions_count)
            questions = question_generator(
                queries,
                qcount,
                schema_description,
                model,
                function_descriptions
            )
            questions_list = questions.split('\n')
            print(questions_list)
        
        # Record each generated question to a CSV
            valid_questions = []
            for question in questions_list:
                response = check_question(
                    question,
                    schema_description,
                    model,
                    function_descriptions
                )
                if "This is a reasonable question" in response:
                    valid_questions.append(question)
                    # Send the valid question to frontend
                    question=re.sub(r'^(Question\s*)?(\d+[\.:) ]*)?', '', question).strip()
                    self.show_suggestions(question)
                    self.vdb.add_suggestion(question,collection_name="travel_sample2_suggestions")
                    print(valid_questions)
                    # Record the valid question to CSV
                    self.record_to_csv('generated_questions.csv', [question])

            
            return valid_questions
    
    def generate_answer(self,user_query,system_message,function_descriptions,model):

        # Build the functions that the agent can use
        db_connection = self.connect_to_database()
        
        if self.db_type == "sqlite":
            query_database, _ = tools.make_sqlite_query_tool(db_connection)
        elif self.db_type == "mysql":
            query_database, _ = tools.make_mysql_query_tool(db_connection)
        else:
            raise ValueError("Unsupported database type")

        functions = {
            'query_database': query_database

        }
        
        agent = make_react_agent(
            system_message,
            model,
            function_descriptions,
            functions,
            self.MAX_LLM_CALLS_PER_INTERACTION,
            simple_formatting=False
        )
        
        chat_history = []
        for message in agent(user_query):
            chat_history.append(str(message))
            if message.role == 'assistant' and 'Final Answer:' in message.content:
                response = message.content.split('Final Answer:')[1].strip()
                db_connection.close()
                self.record_to_csv('questions_and_responses.csv', [user_query, response])
                self.log_to_file('chat_log.txt', user_query, chat_history)
                return response,chat_history
        
        db_connection.close()
        return "Could not determine an answer.",_

    def record_to_csv(self, filename, data):
        """Writes data to a CSV file."""
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)


    
    


    def get_dashboard_names_for_datasource(self, data_source_name):
        try:
            with open("dashboards.json", "r") as file:
                data = json.load(file)
                if data_source_name in data:
                    return list(data[data_source_name]['dashboards'].keys())
                else:
                    return []
        except FileNotFoundError:
            print("dashboards.json not found!")
            return []
        except json.JSONDecodeError:
            print("Error decoding dashboards.json!")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def process_query(self, user_query, schema_description):
        function_descriptions = [
            {
                'name': 'query_database',
                'description': 'Query the database.',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'query': {
                            'type': 'string',
                            'description': 'A query to run against the database.'
                        },
                    },
                    'required': ['query']
                }
            }
        ]

        # Setup
        openai.set_api_key(os.getenv('OPENAI_API_KEY'))
        model = openai.start_chat('gpt-4-0613')
        db_connection = self.connect_to_database()
        if not db_connection:
            return "Failed to connect to the database."
        
        if self.db_type == "sqlite":
            schema_description += get_db_creation_sql(db_connection)
        elif self.db_type == "mysql":
            schema_description += get_db_creation_mysql(db_connection)
        db_connection.close()

        system_message = (
            "You are an assistant for a database..."
            # ... (rest of the system message)
        )

        system_message += schema_description
        vdb_result = self.vdb.query_vdb(user_query, 1,collection_name="travel_sample2")
        if vdb_result:
            print(vdb_result)
            first_key = list(vdb_result.keys())[0]  # Get the key from the vdb_result
            data_description = vdb_result[first_key]['data_description']
            plot_params = eval(vdb_result[first_key]['plot_params'])  # Convert string representation back to dictionary
            sql_query = vdb_result[first_key]['sql']
            data= self.execute_sql_query(sql_query)
            if data:
                print("SQL query result:", data)
                base64_image = self.DV.generate_plot(
                    dict(data),
                    plot_params.get('plot_title'),
                    plot_params.get('axis_names'),
                    plot_params.get('graph_type')
                )
                if base64_image:
                    print("Generated graph successfully!")
                    self.show_graph(base64_image)
                    dashboard_names = self.get_dashboard_names_for_datasource('Travel - 1')
                    query_data = {
                    'Data Source Name': 'Travel - 1',  # You can adjust this if you have different data sources
                    'class': 'mysql',  # Adjust this as needed
                    'dashboards': dashboard_names,  
                    'graph_description': data_description,  # A simple description
                    'sql_query': sql_query,
                    'plot_params': plot_params
                    }
                    self.store_last_query_data(query_data)
                    response=self.DV.get_answer_and_insight_function_params(data,data_description,user_query)
                    self.show_answer(response.get('answer'))
                    self.show_insight(response)
                else:
                    print("Failed to generate graph.")
            
            
        else:
        # Check the reasonableness of the user's question
            response = check_question(
            user_query,
            schema_description,
            model,
            function_descriptions
            )
            suggestions=[]
            if "This is a reasonable question" not in response:
                self.show_answer(response)
            answer,react_log=self.generate_answer(user_query,system_message,function_descriptions,model)
            self.show_answer(answer)
            response=self.DV.generate_sql_for_datavisualisation(user_query,react_log,schema_description)
            sql_query=response.get('SQL_QUERY')
            data_description=response.get('Data_Description')
            data= self.execute_sql_query(sql_query)
            if data:
                print("SQL query result:", data)

                plot_params=self.DV.get_plot_function_params(data,data_description)
                base64_image = self.DV.generate_plot(
                    plot_params.get('data'),
                    plot_params.get('plot_title'),
                    plot_params.get('axis_names'),
                    plot_params.get('graph_type')
                )
                if base64_image:
                    print("Generated graph successfully!")
                    self.show_graph(base64_image)
                    dashboard_names = self.get_dashboard_names_for_datasource('Travel - 1')
                    plot_params.pop('data')
                    query_data = {
                    'Data Source Name': 'Travel - 1',  # You can adjust this if you have different data sources
                    'class': 'mysql',  # Adjust this as needed
                    'dashboards': dashboard_names,  
                    'graph_description': data_description,  # A simple description
                    'sql_query': sql_query,
                    'plot_params': plot_params
                    }
                    self.store_last_query_data(query_data)
                   
                else:
                    print("Failed to generate graph.")
                
                insights=self.DV.get_insight_function_params(data, data_description, user_query)
                self.vdb.add_question(user_query,sql_query,str(plot_params),data_description,collection_name="travel_sample2")
                self.show_insight(insights)

                
            else:
                print("Failed to execute SQL query.")
            
            
        suggestions=self.generate_suggestions(user_query,schema_description,model,function_descriptions)
        
            
            
        

            

    # Example usage:
    # chatbot = GenericDatabaseChatbot(db_type="mysql")
    # schema_description = (
    #     "Each user can book one or more flights and hotels. Flights have different classes, and hotels offer various room types..."
    #     # ... (rest of the schema description)
    # )

    # while True:
    #     query = input("Query : ")
    #     da = DataAnalyser(db_type="mysql")
    #     schema_description = (
    #     "Each user can book one or more flights and hotels. Flights have different classes, and hotels offer various room types...") 
    #     response = da.main(query,schema_description)  
    #     print(response)