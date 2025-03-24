import random  # Needed to generate random references
import string  # Needed to use letters and digits

# Apache Airlines - Seat Booking System
# This program allows users to check, book, free seats, and view the booking layout.
# F = Free, R = Reserved, S = Storage

# Set to store all booking references and ensure uniqueness
existing_references = set()

# Function to generate a unique 8-character alphanumeric booking reference
def generate_booking_reference():
    while True:
        # Create a random string of 8 characters using uppercase letters and digits
        reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # Check if this reference has already been used
        if reference not in existing_references:
            existing_references.add(reference)  # Save it to avoid duplicates
            return reference  # Return the unique reference

# Function to create the full seating layout of the plane
def create_seats():
    seats = {}  # Dictionary to hold seat names and their status
    for row in range(1, 81):  # Loop through all rows from 1 to 80
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:  # Loop through all seat columns
            seat = f"{row}{col}"  # Combine row and column to form seat label (e.g. 12B)
            # Seats in rows 77-80 and columns D–F are storage, cannot be booked
            if row >= 77 and col in ['D', 'E', 'F']:
                seats[seat] = 'S'  # Mark these seats as storage
            else:
                seats[seat] = 'F'  # All other seats start as free
    return seats  # Return the completed seat dictionary

# Function to display the current status of all seats
def show_booking_status(seats):
    print("\nBooking Status")
    print("Legend: F = Free, R = Reserved, S = Storage")
    for row in range(1, 81):
        row_status = []
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:
            seat = f"{row}{col}"
            if seat in seats:
                row_status.append(f"{seat}:{seats[seat]}")
        print(" ".join(row_status))

# Function to check if a specific seat is available
def check_availability(seats):
    seat = input("Enter the seat (e.g., 10A): ").upper()
    if seat in seats:
        if seats[seat] == 'F':
            print(f"{seat} is available")
        elif seats[seat] == 'R':
            print(f"{seat} is already booked")
        elif seats[seat] == 'S':
            print(f"{seat} is a storage area and cannot be booked")
    else:
        print("Seat does not exist. Please check your input.")

# Function to book a seat
def book_seat(seats):
    seat = input("Enter the seat to book: ").upper()
    if seat in seats:
        if seats[seat] == 'F':
            # Generate and show a unique booking reference
            reference = generate_booking_reference()
            seats[seat] = 'R'  # For now, we keep 'R' to indicate reserved (Part B Q2 will store ref)
            print(f"{seat} has been booked. Booking reference: {reference}")
        elif seats[seat] == 'R':
            print(f"{seat} is already booked")
        else:
            print(f"{seat} cannot be booked")
    else:
        print("Seat does not exist")

# Function to free up a reserved seat
def free_seat(seats):
    seat = input("Enter the seat to free: ").upper()
    if seat in seats:
        if seats[seat] == 'R':
            seats[seat] = 'F'  # Mark it as free again
            print(f"{seat} is now available")
        else:
            print(f"{seat} is not currently booked")
    else:
        print("Seat does not exist")

# Function to display all currently booked seats
def show_booked_seats(seats):
    print("\nBooked Seats")
    booked = [seat for seat, status in seats.items() if status == 'R']
    if booked:
        print(" ".join(booked))
    else:
        print("No seats are currently booked")

# Main function to run the system
def main():
    seats = create_seats()  # Initialize all seats
    while True:
        print("\n--- Apache Airlines Booking Menu ---")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit programme")
        print("6. Show all booked seats")

        choice = input("Choose an option (1–6): ")

        if choice == '1':
            check_availability(seats)
        elif choice == '2':
            book_seat(seats)
        elif choice == '3':
            free_seat(seats)
        elif choice == '4':
            show_booking_status(seats)
        elif choice == '5':
            print("Exiting programme. Goodbye.")
            break
        elif choice == '6':
            show_booked_seats(seats)
        else:
            print("Invalid option. Please try again.")

# Run the system
main()
