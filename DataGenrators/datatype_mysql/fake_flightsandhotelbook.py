import mysql.connector
from faker import Faker
import random
from datetime import timedelta
from datetime import datetime
# Connect to the database
conn = mysql.connector.connect(
host="localhost", user="root", password="root", database="Travel_01"
)
cursor = conn.cursor()

# Initialize Faker
fake = Faker()

def create_fake_user(cursor):
    while True:  # This loop will keep running until a unique username is found
        username = fake.user_name()
        
        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if not cursor.fetchone():  # If fetchone() returns None, the username does not exist
            break  # Exit the loop
    password_hash = fake.sha256()
    email = fake.email()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.phone_number().replace('-', '').replace('(', '').replace(')', '').replace(' ', '')[:15]  
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=100).strftime('%Y-%m-%d')
    created_at = fake.past_datetime(start_date="-10y").strftime('%Y-%m-%d %H:%M:%S')
    # Parse the created_at string to a datetime object
    created_at_datetime = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
    # Now pass the datetime object to past_datetime
    updated_at = fake.past_datetime(start_date=created_at_datetime).strftime('%Y-%m-%d %H:%M:%S')


    user_insert_query = """
        INSERT INTO users (
            username,
            password_hash,
            email,
            first_name,
            last_name,
            phone,
            date_of_birth,
            created_at,
            updated_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(user_insert_query, (username, password_hash, email, first_name, last_name, phone, date_of_birth, created_at, updated_at))
    
    # Get the user_id of the newly inserted user
    cursor.execute("SELECT LAST_INSERT_ID()")
    user_id = cursor.fetchone()[0]
    return user_id


def create_bookings_for_hotel(hotel, room_types, flights):
    # Determine random number of users to create
    num_users = random.randint(5, 17)
    for _ in range(num_users):
        user_id = create_fake_user(cursor)
        
        # Create hotel booking
        room_type = random.choice(room_types)
        check_in_date = fake.date_this_decade()
        check_out_date = (fake.date_this_decade() + timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d %H:%M:%S')
        hotel_booking_query = """
            INSERT INTO hotel_bookings (user_id, room_type_id, check_in_date, check_out_date, price)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(hotel_booking_query, (user_id, room_type[0], check_in_date, check_out_date, room_type[4]))
        
        # Create flight booking
        flight = random.choice(flights)
        flight_booking_query = """
            INSERT INTO flight_bookings (user_id, flight_id, booking_date, price)
            VALUES (%s, %s, %s, %s)
        """
        flight_price = round(random.uniform(100.0, 500.0), 2)  # Generate a random flight price between 100 and 500
        cursor.execute(flight_booking_query, (user_id, flight[0], check_in_date, flight_price))  # Use the random flight price # Assuming flight price is in column 5

# Fetch hotel data
cursor.execute("SELECT * FROM hotels")
hotels = cursor.fetchall()

for hotel in hotels:
    # Fetch room types for the hotel
    cursor.execute("SELECT * FROM room_types WHERE hotel_id = %s", (hotel[0],))
    room_types = cursor.fetchall()
    
    # Fetch flights for the hotel's city
    print(f"Hotel city: {hotel[3]}")
    city = hotel[3].strip()  # Remove any leading or trailing whitespaces from the city name
    query = f"SELECT * FROM flights WHERE UPPER(destination) = UPPER(%s)"  # Case-insensitive comparison
    cursor.execute(query, (city,))  # Pass the trimmed and upper-cased city name as a parameter
    flights = cursor.fetchall()
    print(flights)  
    if flights:
        create_bookings_for_hotel(hotel, room_types, flights)

# Commit the transactions
conn.commit()

# Close the connection
cursor.close()
conn.close()
