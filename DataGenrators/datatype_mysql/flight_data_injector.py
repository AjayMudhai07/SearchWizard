import mysql.connector
import csv

# Database configuration
config = {
    "user": "root",
    "password": "root",
    "host": "localhost",
    "database": "Travel_01"
}

# Connect to the database
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Inserting data from flights.csv to the flights table
with open("flights.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        cursor.execute("INSERT INTO flights (flight_id, airline_name, source, destination, departure_time, arrival_time) VALUES (%s, %s, %s, %s, %s, %s)", row)

conn.commit()
cursor.close()
conn.close()
