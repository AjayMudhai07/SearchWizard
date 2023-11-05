import mysql.connector
import random
from faker import Faker

# Assume you have these set up according to your database configuration
db = mysql.connector.connect(
host="localhost", user="root", password="root", database="Travel_01"
)
cursor = db.cursor()

fake = Faker()

def create_fake_user():
    while True:
        username = fake.user_name()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if not cursor.fetchone():
            break

    while True:
        email = fake.email()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if not cursor.fetchone():
            break

    password_hash = fake.sha256()
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = fake.phone_number()[:15]
    date_of_birth = fake.date_of_birth(minimum_age=18).strftime('%Y-%m-%d')

    cursor.execute("""
        INSERT INTO users (username, password_hash, email, first_name, last_name, phone, date_of_birth)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (username, password_hash, email, first_name, last_name, phone, date_of_birth))

    db.commit()
    return cursor.lastrowid

def create_fake_package_booking(user_id, package_id):
    booking_date = fake.date_this_decade().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        INSERT INTO user_packages (user_id, package_id, booking_date)
        VALUES (%s, %s, %s)
    """, (user_id, package_id, booking_date))

    db.commit()

def book_packages_for_users():
    cursor.execute("SELECT package_id FROM travel_packages")
    packages = cursor.fetchall()

    for package in packages:
        package_id = package[0]
        num_users = random.randint(4, 20)  # Random number of users between 4 and 20

        for _ in range(num_users):
            user_id = create_fake_user()
            create_fake_package_booking(user_id, package_id)

# Call the function to start the booking process
book_packages_for_users()

# Close the database connection
cursor.close()
db.close()
