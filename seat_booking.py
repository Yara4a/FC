# Apache Airlines - Seat Booking System
# This program allows users to check, book, free seats, and view the booking layout.
# F = Free, R = Reserved, S = Storage

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
    print("\nBooking Status")  # Print a header for clarity
    print("Legend: F = Free, R = Reserved, S = Storage")  # Explain seat status codes
    for row in range(1, 81):  # Loop through each row
        row_status = []  # List to hold seat status strings for this row
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:  # Loop through seat columns
            seat = f"{row}{col}"  # Build the seat label
            if seat in seats:
                row_status.append(f"{seat}:{seats[seat]}")  # Append seat status (e.g. 12B:F)
        print(" ".join(row_status))  # Print the full row status

# Function to check if a specific seat is available
def check_availability(seats):
    seat = input("Enter the seat (e.g., 10A): ").upper()  # Get and format seat input
    if seat in seats:  # Check if the seat exists
        if seats[seat] == 'F':  # Free seat
            print(f"{seat} is available")
        elif seats[seat] == 'R':  # Already reserved
            print(f"{seat} is already booked")
        elif seats[seat] == 'S':  # Storage seat
            print(f"{seat} is a storage area and cannot be booked")
    else:
        print("Seat does not exist. Please check your input.")  # Invalid seat entered

# Function to book a seat
def book_seat(seats):
    seat = input("Enter the seat to book: ").upper()  # Get and format seat input
    if seat in seats:  # Check if the seat exists
        if seats[seat] == 'F':  # If seat is free, book it
            seats[seat] = 'R'  # Change status to Reserved
            print(f"{seat} has been booked")
        elif seats[seat] == 'R':  # Already reserved
            print(f"{seat} is already booked")
        else:
            print(f"{seat} cannot be booked")  # Storage or invalid
    else:
        print("Seat does not exist")  # Invalid input

# Function to free up a reserved seat
def free_seat(seats):
    seat = input("Enter the seat to free: ").upper()  # Get and format seat input
    if seat in seats:  # Check if the seat exists
        if seats[seat] == 'R':  # If it's reserved
            seats[seat] = 'F'  # Mark it as free again
            print(f"{seat} is now available")
        else:
            print(f"{seat} is not currently booked")  # Seat is already free or storage
    else:
        print("Seat does not exist")  # Invalid input

# Function to display all currently booked seats
def show_booked_seats(seats):
    print("\nBooked Seats")  # Header
    # Filter out only seats marked as 'R' (reserved)
    booked = [seat for seat, status in seats.items() if status == 'R']
    if booked:  # If there are any booked seats
        print(" ".join(booked))  # Show all booked seat labels
    else:
        print("No seats are currently booked")  # If none, tell the user

# Main function to run the system
def main():
    seats = create_seats()  # Initialize all seats
    while True:  # Keep showing menu until user exits
        # Display the main menu
        print("\n--- Apache Airlines Booking Menu ---")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit programme")
        print("6. Show all booked seats")  # New feature added for Q5

        choice = input("Choose an option (1–6): ")  # Get user choice

        # Match user choice with actions
        if choice == '1':
            check_availability(seats)
        elif choice == '2':
            book_seat(seats)
        elif choice == '3':
            free_seat(seats)
        elif choice == '4':
            show_booking_status(seats)
        elif choice == '5':
            print("Exiting programme. Goodbye.")  # Exit message
            break  # Exit the loop and end program
        elif choice == '6':
            show_booked_seats(seats)  # Call the new function
        else:
            print("Invalid option. Please try again.")  # If user enters something not in menu

# Run the system
main()
