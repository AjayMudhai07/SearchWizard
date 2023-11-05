import csv
import random
from datetime import datetime, timedelta

# List of sample Indian cities
cities = ["Delhi", "Mumbai", "Bengaluru", "Kolkata", "Chennai", "Hyderabad"]
# Domestic tourist destinations
domestic_destinations = ["Goa", "Jaipur", "Agra", "Shimla", "Kochi", "Udaipur"]
# International tourist destinations
international_destinations = ["Paris", "New York", "London", "Dubai", "Singapore", "Sydney"]

# Combined destinations list
all_destinations = domestic_destinations + international_destinations

# Airlines for variety
airlines = ["Air India", "IndiGo", "SpiceJet", "Vistara", "GoAir"]

# Generating 40 random flight data
with open("flights.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["flight_id", "airline_name", "source", "destination", "departure_time", "arrival_time"])

    for i in range(1, 101): # since flight_id starts from 1
        source = random.choice(cities)
        # ensuring the destination is different from source
        destination = random.choice([d for d in all_destinations if d != source])

        # Creating random departure and arrival times
        current_date = datetime.now().date()
        departure_time = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        
        # Assuming flight duration is between 1 to 5 hours for domestic destinations and 6 to 15 for international destinations
        if destination in domestic_destinations:
            arrival_time = departure_time + timedelta(hours=random.randint(1, 5))
        else:  # International destination
            arrival_time = departure_time + timedelta(hours=random.randint(6, 15))

        writer.writerow([i, random.choice(airlines), source, destination, departure_time, arrival_time])
