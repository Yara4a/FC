import random
import string
import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('bookings.db')
cursor = conn.cursor()

# Create table for customer bookings
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        reference TEXT PRIMARY KEY,
        passport TEXT,
        first_name TEXT,
        last_name TEXT,
        seat TEXT
    )
''')
conn.commit()

existing_references = set()

# Generate unique 8-character booking reference
def generate_booking_reference():
    while True:
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if ref not in existing_references:
            existing_references.add(ref)
            return ref

# Create the seating layout
def create_seats():
    seats = {}
    for row in range(1, 81):
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:
            seat = f"{row}{col}"
            if row >= 77 and col in ['D', 'E', 'F']:
                seats[seat] = 'S'
            else:
                seats[seat] = 'F'
    return seats

# Show all seats
def show_booking_status(seats):
    print("\nBooking Status:")
    for row in range(1, 81):
        row_data = []
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:
            seat = f"{row}{col}"
            if seat in seats:
                row_data.append(f"{seat}:{seats[seat]}")
        print(" ".join(row_data))

# Check availability
def check_availability(seats):
    seat = input("Enter the seat (e.g., 10A): ").upper()
    if seat in seats:
        status = seats[seat]
        if status == 'F':
            print(f"{seat} is available.")
        elif status == 'S':
            print(f"{seat} is a storage area.")
        else:
            print(f"{seat} is booked with reference {status}")
    else:
        print("Seat does not exist.")

# Book a seat and store customer details
def book_seat(seats):
    seat = input("Enter seat to book: ").upper()
    if seat in seats and seats[seat] == 'F':
        passport = input("Enter passport number: ")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        reference = generate_booking_reference()

        seats[seat] = reference

        # Save to database
        cursor.execute('''
            INSERT INTO bookings (reference, passport, first_name, last_name, seat)
            VALUES (?, ?, ?, ?, ?)
        ''', (reference, passport, first_name, last_name, seat))
        conn.commit()

        print(f"{seat} booked successfully. Reference: {reference}")
    elif seat in seats and seats[seat] != 'F':
        print(f"{seat} is already booked or unavailable.")
    else:
        print("Invalid seat.")

# Free a booked seat and remove customer from DB
def free_seat(seats):
    seat = input("Enter seat to free: ").upper()
    if seat in seats and seats[seat] not in ['F', 'S']:
        reference = seats[seat]
        seats[seat] = 'F'

        # Delete from database
        cursor.execute('DELETE FROM bookings WHERE reference = ?', (reference,))
        conn.commit()

        print(f"{seat} is now free. Booking {reference} removed.")
    else:
        print("Seat not booked or invalid.")

# Main menu
def main():
    seats = create_seats()
    while True:
        print("\n--- Apache Airlines Booking Menu ---")
        print("1. Check availability")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            check_availability(seats)
        elif choice == '2':
            book_seat(seats)
        elif choice == '3':
            free_seat(seats)
        elif choice == '4':
            show_booking_status(seats)
        elif choice == '5':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option.")

main()
