# Import required libraries
import random       # Used to generate random references
import string       # Used for letters and digits in references
import sqlite3      # Used to connect and interact with SQLite database

# Define a class to represent one booking
class Booking:
    def __init__(self, reference, passport, first_name, last_name, seat):
        self.reference = reference        # Unique booking reference
        self.passport = passport          # Customer's passport number
        self.first_name = first_name      # Customer's first name
        self.last_name = last_name        # Customer's last name
        self.seat = seat                  # Seat number booked

# Define the main booking system class
class BookingSystem:
    def __init__(self):
        self.seats = self.create_seats()              # Initialise seat layout
        self.existing_references = set()              # Set to keep track of used references
        self.conn = sqlite3.connect('bookings.db')    # Connect to the SQLite database
        self.cursor = self.conn.cursor()              # Create a cursor to run SQL commands
        self.setup_database()                         # Create bookings table if it doesn't exist

    # Create the bookings table in the database
    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                reference TEXT PRIMARY KEY,
                passport TEXT,
                first_name TEXT,
                last_name TEXT,
                seat TEXT
            )
        ''')  # SQL command to create table with 5 fields
        self.conn.commit()  # Save the changes to the database

    # Generate all 480 seats and assign default statuses
    def create_seats(self):
        seats = {}  # Dictionary to hold seat info
        for row in range(1, 81):  # Loop through rows 1 to 80
            for col in ['A', 'B', 'C', 'D', 'E', 'F']:  # Loop through seat columns
                seat = f"{row}{col}"  # Create seat label (e.g. 12A)
                if row >= 77 and col in ['D', 'E', 'F']:
                    seats[seat] = 'S'  # Mark as storage
                else:
                    seats[seat] = 'F'  # Mark as free
        return seats  # Return the completed layout

    # Generate a unique 8-character alphanumeric booking reference
    def generate_booking_reference(self):
        while True:
            ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # Create random string
            if ref not in self.existing_references:  # Check if unique
                self.existing_references.add(ref)  # Save the reference
                return ref  # Return the unique reference

    # Check if a seat is available
    def check_availability(self):
        seat = input("Enter the seat (e.g., 10A): ").upper()  # Ask for seat input
        if seat in self.seats:  # Check if seat exists
            status = self.seats[seat]  # Get current seat status
            if status == 'F':
                print(f"{seat} is available.")
            elif status == 'S':
                print(f"{seat} is a storage area.")
            else:
                print(f"{seat} is booked with reference {status}")
        else:
            print("Seat does not exist.")

    # Book a seat and store customer data in the database
    def book_seat(self):
        seat = input("Enter seat to book: ").upper()  # Ask user for seat
        if seat in self.seats and self.seats[seat] == 'F':  # Check if seat is available
            passport = input("Enter passport number: ")       # Get passport input
            first_name = input("Enter first name: ")          # Get first name
            last_name = input("Enter last name: ")            # Get last name
            reference = self.generate_booking_reference()     # Create unique booking reference

            self.seats[seat] = reference  # Assign reference to seat

            # Create booking object and insert into database
            booking = Booking(reference, passport, first_name, last_name, seat)
            self.cursor.execute('''
                INSERT INTO bookings (reference, passport, first_name, last_name, seat)
                VALUES (?, ?, ?, ?, ?)
            ''', (booking.reference, booking.passport, booking.first_name, booking.last_name, booking.seat))
            self.conn.commit()  # Save to database

            print(f"{seat} booked successfully. Reference: {reference}")
        elif seat in self.seats and self.seats[seat] != 'F':
            print(f"{seat} is already booked or unavailable.")
        else:
            print("Invalid seat.")

    # Cancel a booking and remove customer data from database
    def free_seat(self):
        seat = input("Enter seat to free: ").upper()  # Ask user for seat to free
        if seat in self.seats and self.seats[seat] not in ['F', 'S']:  # Ensure seat is booked
            reference = self.seats[seat]  # Get reference tied to seat
            self.seats[seat] = 'F'  # Reset seat to free

            # Delete booking from database using the reference
            self.cursor.execute('DELETE FROM bookings WHERE reference = ?', (reference,))
            self.conn.commit()  # Save the change

            print(f"{seat} is now free. Booking {reference} removed.")
        else:
            print("Seat not booked or invalid.")

    # Display the current layout of all seats
    def show_booking_status(self):
        print("\nBooking Status:")
        for row in range(1, 81):  # Loop through all rows
            row_data = []  # List to hold status of one row
            for col in ['A', 'B', 'C', 'D', 'E', 'F']:  # Loop through all columns
                seat = f"{row}{col}"  # Create seat label
                if seat in self.seats:
                    row_data.append(f"{seat}:{self.seats[seat]}")  # Append status
            print(" ".join(row_data))  # Print row

    # Main menu loop
    def run(self):
        while True:
            print("\n--- Apache Airlines Booking Menu ---")
            print("1. Check availability")
            print("2. Book a seat")
            print("3. Free a seat")
            print("4. Show booking status")
            print("5. Exit")

            choice = input("Choose an option: ")  # Get user input

            if choice == '1':
                self.check_availability()
            elif choice == '2':
                self.book_seat()
            elif choice == '3':
                self.free_seat()
            elif choice == '4':
                self.show_booking_status()
            elif choice == '5':
                print("Exiting. Goodbye!")
                break  # Exit the menu
            else:
                print("Invalid option.")

# Create and run the booking system
system = BookingSystem()
system.run()
