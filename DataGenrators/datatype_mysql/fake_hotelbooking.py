import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Establish database connection
conn = mysql.connector.connect(
    host="localhost", user="root", password="root", database="Travel_01"
)

cursor = conn.cursor()

# Initialize Faker
fake = Faker()

def generate_unique_email():
    while True:
        email = fake.unique.email()
        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        if not cursor.fetchone():
            return email 

# Fetch all hotels
cursor.execute("SELECT * FROM hotels")
hotels = cursor.fetchall()

for hotel in hotels:
    hotel_id = hotel[0]
    # Fetch room types for the current hotel
    cursor.execute(f"SELECT * FROM room_types WHERE hotel_id = {hotel_id}")
    room_types = cursor.fetchall()
    
    if not room_types:
        continue  # Skip to next hotel if no room types found
    
    # Generate random number of fake users and bookings for the current hotel
    num_users = random.randint(5, 17)
    for _ in range(num_users):
        # Create fake user data
        username = fake.unique.user_name()
        password_hash = fake.sha256()
        email =  generate_unique_email() 
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.phone_number()[:15]
        date_of_birth = fake.date_of_birth(minimum_age=18).strftime('%Y-%m-%d')
        
        user_data = (username, password_hash, email, first_name, last_name, phone, date_of_birth)
        cursor.execute("""
            INSERT INTO users (username, password_hash, email, first_name, last_name, phone, date_of_birth)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, user_data)
        conn.commit()
        
        user_id = cursor.lastrowid  # Get the ID of the newly inserted user
        
        # Randomly select a room type for booking
        room_type = random.choice(room_types)
        room_type_id = room_type[0]
        price = room_type[5]  # Assuming price is in the 6th column of the room_types table
        
        # Generate fake booking data
        check_in_date = fake.date_this_year().strftime('%Y-%m-%d %H:%M:%S')
        check_out_date = (datetime.strptime(check_in_date, '%Y-%m-%d %H:%M:%S') + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d %H:%M:%S')
        
        booking_data = (user_id, room_type_id, check_in_date, check_out_date, price)
        cursor.execute("""
            INSERT INTO hotel_bookings (user_id, room_type_id, check_in_date, check_out_date, price)
            VALUES (%s, %s, %s, %s, %s)
        """, booking_data)
        conn.commit()

# Close the database connection
cursor.close()
conn.close()
