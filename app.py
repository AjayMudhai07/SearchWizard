from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from data_analysis.data_analyser2 import DataAnalyser
import time
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

last_processed_query = None
last_processed_time = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    global last_processed_query, last_processed_time

    print("Received request for /get_answer")  # Added logging
    query = request.json.get('query')

    current_time = time.time()
    if query == last_processed_query and (current_time - last_processed_time) < 2:  # 2 seconds threshold
        print("Duplicate request detected. Ignoring.")
        return jsonify({"status": "ignored"})

    last_processed_query = query
    last_processed_time = current_time

    da.process_query(query, schema_description)
    print("Processed query in /get_answer")  # Added logging
    return jsonify({"status": "success"})


@app.route('/get_left_nav_items')
def get_left_nav_items():
    # Load the data from dashboards.json
    with open("dashboards.json", "r") as file:
        data = json.load(file)

    items = []
    for name, details in data.items():
        # Extract details for each item
        class_name = details.get("class")
        dropdown_options = list(details.get("dashboards", {}).keys())

        item = {
            "class": class_name,
            "name": name,
            "dropdown": dropdown_options
        }
        items.append(item)

    return jsonify(items)


# @app.route('/get_left_nav_items')
# def get_left_nav_items():
#     items = [
#         {"class": "icon-db1", "name": "Travel -1", "dropdown": ["Option 1", "Option 2", "Option 3"]},
#         {"class": "icon-db2", "name": "Travel -2", "dropdown": ["Option A", "Option B", "Option C"]},
#         {"class": "db3", "name": "Finance - 1", "dropdown": ["Option X", "Option Y", "Option Z"]},
#         {"class": "db4", "name": "Finance - 2", "dropdown": ["Option M", "Option N", "Option O"]},
#     ]
#     return jsonify(items)

@app.route('/page/<string:option_name>')
def serve_option_page(option_name):
    return render_template('dashboards.html', option_name=option_name)


@app.route('/update_dashboard', methods=['POST'])
def update_dashboard():
    # Load the current data from dashboards.json
    with open("dashboards.json", "r") as file:
        data = json.load(file)

    # Extract the provided parameters from the request
    data_source_name = request.json.get('Data Source Name')
    class_name = request.json.get('class')
    dashboard_name = request.json.get('dashboard name')
    graph_description = request.json.get('graph_description')
    sql_query = request.json.get('sql_query')
    plot_params = request.json.get('plot_params')

    # Check if the data source name exists
    if data_source_name not in data:
        data[data_source_name] = {
            "class": class_name,
            "dashboards": {}
        }

    # Check if the dashboard name exists within the data source
    if dashboard_name not in data[data_source_name]['dashboards']:
        data[data_source_name]['dashboards'][dashboard_name] = {}

    # Update or add the graph description
    data[data_source_name]['dashboards'][dashboard_name][graph_description] = {
        "sql_query": sql_query,
        "plot_params": plot_params
    }

    # Save the updated data back to dashboards.json
    with open("dashboards.json", "w") as file:
        json.dump(data, file, indent=4)

    return jsonify({"status": "success"})



if __name__ == '__main__':
    da = DataAnalyser(db_type="mysql", socketio=socketio)
    schema_description = (
    "Each user can book one or more flights and hotels. Flights have different classes, and hotels offer various room types..."
    )
    socketio.run(app, debug=True)
