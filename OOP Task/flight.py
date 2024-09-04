class Airport:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Airline:
    def __init__(self, name):
        self.name = name


class Flight:
    def __init__(self, flight_id, airline, departure, arrival, price, time):
        self.flight_id = flight_id
        self.airline = airline
        self.departure = departure
        self.arrival = arrival
        self.price = price
        self.time = time

    def __str__(self):
        return (f"Flight {self.flight_id} by {self.airline.name} from {self.departure} "
                f"to {self.arrival} at {self.time} - ${self.price}")


class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class Booking:
    def __init__(self, customer, flight, meal_option=None, services=None):
        self.customer = customer
        self.flight = flight
        self.meal_option = meal_option
        self.services = services if services else []

    def __str__(self):
        services_str = ', '.join(self.services) if self.services else 'None'
        return (f"Booking for {self.customer.name} ({self.customer.email}):\n"
                f"{self.flight}\nMeal: {self.meal_option if self.meal_option else 'None'}\n"
                f"Services: {services_str}")


class FlightBookingSystem:
    def __init__(self):
        self.flights = []
        self.meal_options = {
            "1": "Meal1",
            "2": "Meal2",
            "3": "Meal3",
            "4": "Meal4"
        }
        self.services = {
            "1": "Extra Baggage - $50",
            "2": "Priority Boarding - $30",
            "3": "In-Flight WiFi - $20",
            "4": "Travel Insurance - $100"
        }

    def add_flight(self, flight):
        self.flights.append(flight)

    def search_flights(self, departure, arrival, criteria=None):
        # Normalize case and strip whitespace
        departure = departure.strip().lower()
        arrival = arrival.strip().lower()
        flights = [f for f in self.flights if
                   f.departure.strip().lower() == departure and f.arrival.strip().lower() == arrival]
        if criteria:
            flights.sort(key=criteria)
        return flights

    def book_flight(self, customer, flight, meal_option=None, services=None):
        return Booking(customer, flight, meal_option, services)


def main():
    system = FlightBookingSystem()

    # Initialize airports
    hba = Airport("Borg AlArab")
    lxr = Airport("Luxor")
    cai = Airport("Cairo")
    ssh = Airport("Sharm El Sheikh")

    # Initialize airlines
    egyptair = Airline("EgyptAir")
    nileair = Airline("Nile Air")
    flyegypt = Airline("FlyEgypt")

    # Initialize available flights with different airlines
    flight1 = Flight(101, egyptair, hba.name, cai.name, 500, "10:00 AM")
    flight2 = Flight(102, nileair, cai.name, lxr.name, 600, "12:00 PM")
    flight3 = Flight(103, nileair, cai.name, lxr.name, 450, "02:00 PM")
    flight4 = Flight(104, flyegypt, hba.name, ssh.name, 400, "03:00 PM")
    flight5 = Flight(105, egyptair, ssh.name, cai.name, 550, "05:00 PM")

    # Add flights to the system
    system.add_flight(flight1)
    system.add_flight(flight2)
    system.add_flight(flight3)
    system.add_flight(flight4)
    system.add_flight(flight5)


    print("Welcome!!")

    # Enter customer information
    customer_name = input("Enter your name: ")
    customer_email = input("Enter your email: ")
    customer = Customer(customer_name, customer_email)

    # Print all available flights
    print("\nAvailable Flights:")
    for i, flight in enumerate(system.flights):
        print(f"{i + 1}. {flight}")

    # Search for flights
    departure = input("\nEnter departure airport: ").strip().lower()
    arrival = input("Enter arrival airport: ").strip().lower()
    criteria = input("Sort by (price/time): ")

    flights = system.search_flights(departure, arrival,
                                    lambda f: f.price if criteria == "price" else f.time)
    if flights:
        print("\nFiltered Available Flights:")
        for i, flight in enumerate(flights):
            print(f"{i + 1}. {flight}")
        flight_choice = int(input("Select a flight (number): ")) - 1
        flight = flights[flight_choice]

        # Choose meal option
        print("\nAvailable Meal Options:")
        for key, meal in system.meal_options.items():
            print(f"{key}. {meal}")
        meal_choice = input("Select a meal option (number): ")
        meal_option = system.meal_options.get(meal_choice, None)

        # Choose additional services
        print("\nAvailable Additional Services:")
        for key, service in system.services.items():
            print(f"{key}. {service}")
        service_choices = input("Select additional services (comma-separated numbers, or leave blank): ").split(", ")
        services = [system.services.get(choice.strip(), None) for choice in service_choices if choice.strip()]

        # Book the flight
        booking = system.book_flight(customer, flight, meal_option, services)
        print(f"\nBooking successful:\n{booking}")
    else:
        print("No flights available for the selected route.")

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # For handling images
import itertools  # For animation

# Function to handle flight booking
def book_flight():
    result_label.config(text="Booking in progress...")
    root.update_idletasks()  # Update the GUI before starting the booking process

    customer_name = name_entry.get()
    customer_email = email_entry.get()
    customer = Customer(customer_name, customer_email)
    
    selected_flight_index = flight_var.get()
    selected_flight = system.flights[selected_flight_index]

    meal_option = meal_var.get()
    selected_services = [service for idx, service in enumerate(system.services.values()) if service_vars[idx].get()]
    
    booking = system.book_flight(customer, selected_flight, meal_option, selected_services)
    result_label.config(text=f"Booking successful:\n{booking}")

# Initialize the system and flights
system = FlightBookingSystem()
hba = Airport("Borg AlArab")
cai = Airport("Cairo")
lxr = Airport("Luxor")
ssh = Airport("Sharm El Sheikh")

egyptair = Airline("EgyptAir")
system.add_flight(Flight(101, egyptair, hba.name, cai.name, 500, "10:00 AM"))
system.add_flight(Flight(102, egyptair, cai.name, lxr.name, 600, "12:00 PM"))
system.add_flight(Flight(103, egyptair, cai.name, lxr.name, 450, "02:00 PM"))
system.add_flight(Flight(104, egyptair, hba.name, ssh.name, 400, "03:00 PM"))
system.add_flight(Flight(105, egyptair, ssh.name, cai.name, 550, "05:00 PM"))

# Initialize the main window
root = tk.Tk()
root.title("Flight Booking System")

# Add a banner image
banner_img = Image.open(r"OOP Task\flight-logo-115498980752zdckzquoo-4171084381.png")  #
banner_photo = ImageTk.PhotoImage(banner_img)
banner_label = tk.Label(root, image=banner_photo)
banner_label.grid(row=0, column=0, columnspan=2)

# Name and Email Inputs
tk.Label(root, text="Name").grid(row=1, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="Email").grid(row=2, column=0)
email_entry = tk.Entry(root)
email_entry.grid(row=2, column=1)

# Flight Selection
tk.Label(root, text="Select Flight").grid(row=3, column=0)
flight_var = tk.IntVar()
flight_var.set(0)
flight_options = [str(flight) for flight in system.flights]
flight_dropdown = ttk.Combobox(root, textvariable=flight_var, values=flight_options)
flight_dropdown.grid(row=3, column=1)

# Meal Option Selection
tk.Label(root, text="Select Meal Option").grid(row=4, column=0)
meal_var = tk.StringVar()
meal_var.set("None")
meal_options = list(system.meal_options.values())
meal_dropdown = ttk.Combobox(root, textvariable=meal_var, values=meal_options)
meal_dropdown.grid(row=4, column=1)

# Additional Services
tk.Label(root, text="Additional Services").grid(row=5, column=0)
service_vars = [tk.BooleanVar() for _ in system.services]
for idx, (service, description) in enumerate(system.services.items()):
    tk.Checkbutton(root, text=description, variable=service_vars[idx]).grid(row=6+idx, column=0, columnspan=2)

# Book Button
tk.Button(root, text="Book Flight", command=book_flight).grid(row=10, column=0, columnspan=2)

# Result Label
result_label = tk.Label(root, text="")
result_label.grid(row=12, column=0, columnspan=2)

# Start the GUI loop
root.mainloop()
