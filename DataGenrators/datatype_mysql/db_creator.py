import mysql.connector
import csv 

class MySQLDatabaseCreator:
    def __init__(self, host, user, password, database_name):
        self.host = host
        self.user = user
        self.password = password
        self.database_name = database_name

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()


    def execute_and_print_query(self, query):
        self.connect()
        self.cursor.execute(f"USE {self.database_name}")

        try:
            self.cursor.execute(query)
            # If the query is a SELECT statement, fetch and print the data
            if query.strip().upper().startswith("SELECT"):
                rows = self.cursor.fetchall()
                # Print column names
                column_names = [i[0] for i in self.cursor.description]
                print(", ".join(column_names))
                print("-" * 50)
                # Print each row of data
                for row in rows:
                    print(", ".join(map(str, row)))
            else:
                # If it's not a SELECT statement, just commit (for INSERT, UPDATE, DELETE)
                self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.disconnect()

    def create_database(self):
        self.connect()

        # Create the database
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
        
        # Use the database
        self.cursor.execute(f"USE {self.database_name}")

        self.disconnect()

    def execute_schema(self, schema):
        self.connect()
        self.cursor.execute(f"USE {self.database_name}")
        
        # Split the schema by semicolons and execute each statement
        # (this assumes each statement in the schema is separated by a semicolon)
        commands = schema.split(";")
        for command in commands:
            if command.strip():  # ensure the command is not empty
                self.cursor.execute(command)

        self.connection.commit()
        self.disconnect()

    def fetch_and_print_table_data(self, table_name):
        self.connect()
        self.cursor.execute(f"USE {self.database_name}")
        
        # Fetch data from the specified table
        self.cursor.execute(f"SELECT * FROM {table_name}")
        rows = self.cursor.fetchall()
        
        # Print column names
        column_names = [i[0] for i in self.cursor.description]
        print(", ".join(column_names))
        print("-" * 50)
        
        # Print each row of data
        for row in rows:
            print(", ".join(map(str, row)))
        
        self.disconnect()

    def delete_all_data_from_table(self, table_name):
        """Delete all data from the specified table."""
        self.connect()
        self.cursor.execute(f"USE {self.database_name}")
        
        # Delete all records from the specified table
        self.cursor.execute(f"DELETE FROM {table_name}")
        
        self.connection.commit()
        self.disconnect()

    def inject_data_from_csv(self, table_name, csv_file_name):
        self.connect()
        self.cursor.execute(f"USE {self.database_name}")

        # Read data from CSV file
        with open(csv_file_name, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            headers = next(csvreader)  # Skip header row

            for row in csvreader:
                # Build the query string for this row
                placeholders = ', '.join(['%s'] * len(row))
                query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"
                print(query)  # Print the query to debug
                
                try:
                    # Execute the query for this row
                    self.cursor.execute(query, tuple(row))
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    print(f"Row: {row}")

        self.connection.commit()
        self.disconnect()

    # def inject_data_from_csv(self, table_name, csv_file_name):
    #     self.connect()
    #     self.cursor.execute(f"USE {self.database_name}")

    #     # Read data from CSV file
    #     with open(csv_file_name, newline='', encoding='utf-8') as csvfile:
    #         csvreader = csv.reader(csvfile)
    #         headers = next(csvreader)  # Skip header row
    #         data = list(csvreader)  # Read remaining data

    #     # Create a SQL query string with the appropriate number of placeholders
    #     placeholders = ', '.join(['%s'] * len(headers))
    #     query = f"INSERT INTO {table_name} VALUES ({placeholders})"

    #     # Execute the query with the data
    #     self.cursor.executemany(query, data)
    #     self.connection.commit()

    #     self.disconnect()

if __name__ == "__main__":
    db_creator = MySQLDatabaseCreator(host="localhost", user="root", password="root", database_name="Travel_01")
    query="""DROP TABLE IF EXISTS package_reviews;
"""
    db_creator.execute_and_print_query(query)
    # db_creator.delete_all_data_from_table('users')
    # db_creator.inject_data_from_csv('users', 'users.csv')
    # db_creator.fetch_and_print_table_data('user_packages')
    

# if __name__ == "__main__":
#     db_creator = MySQLDatabaseCreator(host="localhost", user="root", password="root", database_name="Travel_01")

#     # The provided schema
#     schema = """CREATE TABLE users (
#     user_id INT AUTO_INCREMENT PRIMARY KEY, 
#     username VARCHAR(50) UNIQUE NOT NULL, 
#     password_hash VARCHAR(255) NOT NULL, 
#     email VARCHAR(100) UNIQUE NOT NULL, 
#     first_name VARCHAR(50), 
#     last_name VARCHAR(50), 
#     phone VARCHAR(15), 
#     date_of_birth DATE, 
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
#     updated_at DATETIME
# );

# CREATE TABLE flights (
#     flight_id INT AUTO_INCREMENT PRIMARY KEY, 
#     airline_name VARCHAR(100), 
#     source VARCHAR(100), 
#     destination VARCHAR(100), 
#     departure_time DATETIME, 
#     arrival_time DATETIME
# );

# CREATE TABLE hotels (
#     hotel_id INT AUTO_INCREMENT PRIMARY KEY, 
#     hotel_name VARCHAR(255), 
#     address TEXT, 
#     city VARCHAR(50), 
#     country VARCHAR(50), 
#     rating DECIMAL(2,1)
# );

# CREATE TABLE room_types (
#     room_type_id INT AUTO_INCREMENT PRIMARY KEY, 
#     hotel_id INT, 
#     type_name ENUM('Single', 'Double', 'Suite', 'Deluxe'), 
#     amenities TEXT, 
#     price DECIMAL(15,2), 
#     available_rooms INT, 
#     FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
# );

# CREATE TABLE flight_bookings (
#     booking_id INT AUTO_INCREMENT PRIMARY KEY, 
#     user_id INT, 
#     flight_id INT, 
#     booking_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
#     price DECIMAL(15,2), 
#     FOREIGN KEY (user_id) REFERENCES users(user_id), 
#     FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
# );

# CREATE TABLE hotel_bookings (
#     booking_id INT AUTO_INCREMENT PRIMARY KEY, 
#     user_id INT, 
#     room_type_id INT, 
#     check_in_date DATETIME, 
#     check_out_date DATETIME, 
#     price DECIMAL(15,2), 
#     FOREIGN KEY (user_id) REFERENCES users(user_id), 
#     FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id)
# );

# CREATE TABLE travel_packages (
#     package_id INT AUTO_INCREMENT PRIMARY KEY, 
#     package_name VARCHAR(255), 
#     description TEXT, 
#     start_date DATETIME, 
#     end_date DATETIME, 
#     price DECIMAL(15,2)
# );

# CREATE TABLE user_packages (
#     user_package_id INT AUTO_INCREMENT PRIMARY KEY, 
#     user_id INT, 
#     package_id INT, 
#     booking_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
#     FOREIGN KEY (user_id) REFERENCES users(user_id), 
#     FOREIGN KEY (package_id) REFERENCES travel_packages(package_id)
# );

# CREATE TABLE package_reviews (
#     review_id INT AUTO_INCREMENT PRIMARY KEY, 
#     package_id INT, 
#     user_id INT, 
#     rating DECIMAL(2,1), 
#     comment TEXT, 
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
#     FOREIGN KEY (package_id) REFERENCES travel_packages(package_id), 
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# );

# CREATE TABLE payments (
#     payment_id INT AUTO_INCREMENT PRIMARY KEY, 
#     user_id INT, 
#     amount DECIMAL(15,2), 
#     payment_method ENUM('Credit Card', 'Debit Card', 'PayPal', 'Others'), 
#     payment_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# );

# -- room_types.hotel_id can be joined with hotels.hotel_id
# -- flight_bookings.user_id can be joined with users.user_id
# -- flight_bookings.flight_id can be joined with flights.flight_id
# -- hotel_bookings.user_id can be joined with users.user_id
# -- hotel_bookings.room_type_id can be joined with room_types.room_type_id
# -- user_packages.user_id can be joined with users.user_id
# -- user_packages.package_id can be joined with travel_packages.package_id
# -- package_reviews.package_id can be joined with travel_packages.package_id
# -- package_reviews.user_id can be joined with users.user_id
# -- payments.user_id can be joined with users.user_id
# """  # Copy the provided schema here

#     db_creator.create_database()
#     db_creator.execute_schema(schema)
