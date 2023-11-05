import csv
import random

# Define room types and amenities
room_types = ['Single', 'Double', 'Suite', 'Deluxe']
amenities = [
    'Free WiFi,TV,Air Conditioning',
    'Free WiFi,TV,Air Conditioning,Minibar',
    'Free WiFi,TV,Air Conditioning,Minibar,Living Room',
    'Free WiFi,TV,Air Conditioning,Minibar,Living Room,Sea View'
]

def generate_room_data(hotel_id):
    """Generate room type data for a given hotel."""
    data = []
    for i, room_type in enumerate(room_types):
        price = random.randint(50, 200) + i * 50  # Random price between 50 and 200, plus a premium for higher room types
        available_rooms = random.randint(5, 20)  # Random number of available rooms between 5 and 20
        data.append([hotel_id, room_type, amenities[i], f'{price}.00', available_rooms])
    return data

def main():
    # Read hotel data from CSV
    with open('hotels.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
        hotel_data = list(csvreader)

    # Generate room type data
    room_data = []
    room_type_id = 1  # Start with 1 and increment for each new room type
    for hotel in hotel_data:
        hotel_id = hotel[0]
        for room in generate_room_data(hotel_id):
            room_data.append([room_type_id] + room)  # Prepend room_type_id to each row
            room_type_id += 1  # Increment room_type_id for the next room type

    # Write room type data to CSV
    with open('room_types.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['room_type_id', 'hotel_id', 'type_name', 'amenities', 'price', 'available_rooms'])  # Write header row
        csvwriter.writerows(room_data)  # Write data rows

if __name__ == "__main__":
    main()
