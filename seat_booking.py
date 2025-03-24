# Apache Airlines - Seat Booking System
# This system lets users check, book, and free seats.
# F = Free, R = Reserved, S = Storage

# Creates all the seats in the plane and sets their default status
def create_seats():
    seats = {}  # Dictionary to store each seat and its current status
    for row in range(1, 81):  # Rows go from 1 to 80
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:  # Seats in each row
            seat = f"{row}{col}"  # Combine row and column to get the seat label
            # From row 77 onward, seats D-F are used for storage
            if row >= 77 and col in ['D', 'E', 'F']:
                seats[seat] = 'S'  # Mark as Storage (cannot be booked)
            else:
                seats[seat] = 'F'  # All other seats are initially Free
    return seats  # Return the full seat layout

# Display the current status of every seat
def show_booking_status(seats):
    print("\nBooking Status")
    print("Legend: F = Free, R = Reserved, S = Storage")
    for row in range(1, 81):
        row_status = []  # List to build the seat statuses for this row
        for col in ['A', 'B', 'C', 'D', 'E', 'F']:
            seat = f"{row}{col}"
            if seat in seats:
                row_status.append(f"{seat}:{seats[seat]}")  # Append seat status to row list
        print(" ".join(row_status))  # Print the status of the row in one line

# Check if a single seat is free, reserved, or storage
def check_availability(seats):
    seat = input("Enter the seat (e.g., 10A): ").upper()  # Normalize input
    if seat in seats:
        if seats[seat] == 'F':
            print(f"{seat} is available")
        elif seats[seat] == 'R':
            print(f"{seat} is already booked")
        elif seats[seat] == 'S':
            print(f"{seat} is a storage area and cannot be booked")
    else:
        print("Seat does not exist. Please check your input.")

# Attempt to reserve a seat if it's available
def book_seat(seats):
    seat = input("Enter the seat to book: ").upper()
    if seat in seats:
        if seats[seat] == 'F':
            seats[seat] = 'R'  # Change status from Free to Reserved
            print(f"{seat} has been booked")
        elif seats[seat] == 'R':
            print(f"{seat} is already booked")
        else:
            print(f"{seat} cannot be booked")
    else:
        print("Seat does not exist")

# Free up a reserved seat
def free_seat(seats):
    seat = input("Enter the seat to free: ").upper()
    if seat in seats:
        if seats[seat] == 'R':
            seats[seat] = 'F'  # Mark it as Free again
            print(f"{seat} is now available")
        else:
            print(f"{seat} is not currently booked")
    else:
        print("Seat does not exist")

# Main menu that controls the flow of the system
def main():
    seats = create_seats()  # Initialize all seats
    while True:
        # Print the menu options for the user
        print("\n--- Apache Airlines Booking Menu ---")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit programme")
        choice = input("Choose an option (1–5): ")  # Get user choice

        # Handle user selection
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
            break  # Exit the loop and end the programme
        else:
            print("Invalid option. Please try again.")

# Start the booking system
main()