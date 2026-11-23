from tkinter import *
from tkinter import ttk, messagebox
import random
from datetime import datetime


root = Tk()
root.title("Railway Reservation System")
root.geometry("850x900")
root.configure(bg="#eaf2f8")


trains = [
    [12301, "Rajdhani Express", "Delhi", "Kolkata", 1500, 50],
    [12302, "Howrah Express", "Kolkata", "Delhi", 1200, 40],
    [12023, "Shatabdi Express", "Delhi", "Chandigarh", 800, 30],
    [12024, "Jan Shatabdi", "Chandigarh", "Delhi", 600, 35],
    [12801, "Purushottam Express", "Delhi", "Puri", 1000, 25],
    [12802, "Odisha Express", "Puri", "Delhi", 1100, 20],
    [12951, "Mumbai Rajdhani", "Delhi", "Mumbai", 1800, 30],
    [12952, "Mumbai Express", "Mumbai", "Delhi", 1600, 25]
]


bookings = []

cities = ["Delhi", "Kolkata", "Chandigarh", "Puri", "Mumbai"]




def get_train(train_number):
    for train in trains:
        if train[0] == int(train_number):
            return train
    return None


def generate_pnr():
    while True:
        pnr = str(random.randint(1000000000, 9999999999))

        if not any(booking[0] == pnr for booking in bookings):
            return pnr


def get_seat_type(seat_number):
  
    if seat_number % 3 == 1:
        return "Window"
    elif seat_number % 3 == 2:
        return "Middle"
    else:
        return "Aisle"


def get_available_seats(train_number, preference):
    train = get_train(train_number)

    if train is None:
        return []

    occupied = []

    for booking in bookings:
        if booking[3] == train[0]:
            occupied.append(booking[6])

    available = []

    for seat in range(1, train[5] + 1):
        if seat not in occupied:
            if preference == "Any" or get_seat_type(seat) == preference:
                available.append(str(seat))

    return available


def refresh_seats(event=None):
    train_number = train_var.get()
    preference = preference_var.get()

    if train_number == "":
        seat_box["values"] = []
        seat_var.set("")
        return

    available = get_available_seats(train_number, preference)

    seat_box["values"] = available

    if available:
        seat_var.set(available[0])
    else:
        seat_var.set("")

    update_fare()


def update_fare(event=None):
    train_number = train_var.get()

    if train_number == "":
        fare_label.config(text="Fare: ₹0")
        return

    train = get_train(train_number)

    if train:
        fare_label.config(text="Fare: ₹" + str(train[4]))




def search():
    source = source_var.get()
    destination = destination_var.get()

    if source == "" or destination == "":
        messagebox.showwarning("Warning", "Please select source and destination.")
        return

    if source == destination:
        messagebox.showwarning("Warning", "Source and destination cannot be the same.")
        return

    result = ""

    for train in trains:
        if train[2] == source and train[3] == destination:
            available = len(get_available_seats(train[0], "Any"))

            if available > 0:
                result += (
                    f"Train: {train[1]}\n"
                    f"Number: {train[0]}\n"
                    f"Fare: ₹{train[4]}\n"
                    f"Available Seats: {available}\n"
                    "-----------------------------\n"
                )

    if result == "":
        result = "No trains available for this route."

    train_display.delete("1.0", END)
    train_display.insert(END, result)



def available_trains():
    window = Toplevel(root)
    window.title("Available Trains")
    window.geometry("750x400")
    window.configure(bg="#eaf2f8")

    Label(
        window,
        text="AVAILABLE TRAINS",
        font=("Arial", 18, "bold"),
        bg="#eaf2f8"
    ).pack(pady=15)

    columns = ("Number", "Name", "Source", "Destination", "Fare", "Seats")

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=12
    )

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=110)

    table.pack(fill=BOTH, expand=True, padx=15, pady=10)

    for train in trains:
        available = len(get_available_seats(train[0], "Any"))

        if available > 0:
            table.insert(
                "",
                END,
                values=(
                    train[0],
                    train[1],
                    train[2],
                    train[3],
                    "₹" + str(train[4]),
                    available
                )
            )

    def select_train(event):
        selected = table.focus()

        if selected:
            values = table.item(selected, "values")

            train_var.set(str(values[0]))
            source_var.set(values[2])
            destination_var.set(values[3])

            refresh_seats()
            window.destroy()

    table.bind("<Double-1>", select_train)

    Label(
        window,
        text="Double-click a train to select it.",
        bg="#eaf2f8",
        font=("Arial", 10)
    ).pack(pady=5)




def book():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    source = source_var.get()
    destination = destination_var.get()
    date = date_entry.get().strip()
    train_number = train_var.get()
    preference = preference_var.get()
    seat = seat_var.get()
    payment = payment_var.get()

    

    if name == "" or age == "" or date == "":
        messagebox.showwarning("Warning", "Please fill all passenger details.")
        return

    if not age.isdigit() or int(age) <= 0 or int(age) > 120:
        messagebox.showwarning("Invalid Age", "Enter a valid age.")
        return

    if source == "" or destination == "" or train_number == "":
        messagebox.showwarning("Warning", "Please select your route and train.")
        return

    if source == destination:
        messagebox.showwarning("Warning", "Source and destination cannot be the same.")
        return

    try:
        journey_date = datetime.strptime(date, "%d-%m-%Y").date()

        if journey_date < datetime.today().date():
            messagebox.showwarning("Invalid Date", "Journey date cannot be in the past.")
            return

    except ValueError:
        messagebox.showwarning(
            "Invalid Date",
            "Enter date in DD-MM-YYYY format."
        )
        return

    train = get_train(train_number)

    if train is None:
        messagebox.showwarning("Invalid Train", "Please select a valid train.")
        return

    if train[2] != source or train[3] != destination:
        messagebox.showwarning(
            "Invalid Route",
            "The selected train does not match your route."
        )
        return

    if preference == "" or seat == "" or payment == "":
        messagebox.showwarning(
            "Missing Selection",
            "Please select seat preference, seat number and payment method."
        )
        return

    available_seats = get_available_seats(train_number, preference)

    if seat not in available_seats:
        messagebox.showwarning(
            "Seat Unavailable",
            "This seat is no longer available. Please select another seat."
        )
        refresh_seats()
        return

    fare = train[4]

 

    confirm = messagebox.askyesno(
        "Payment Confirmation",
        f"Passenger: {name}\n"
        f"Train: {train[1]}\n"
        f"Seat: {seat} ({preference})\n"
        f"Payment Method: {payment}\n"
        f"Total Amount: ₹{fare}\n\n"
        "Proceed with payment?"
    )

    if not confirm:
        return

    

    messagebox.showinfo(
        "Payment Successful",
        f"Payment of ₹{fare} completed successfully!\n"
        f"Method: {payment}"
    )

    

    pnr = generate_pnr()

    booking = [
        pnr,
        name,
        int(age),
        train[0],
        date,
        fare,
        int(seat),
        preference,
        payment
    ]

    bookings.append(booking)

   

    messagebox.showinfo(
        "Ticket Confirmed",
        f"YOUR TICKET IS BOOKED!\n\n"
        f"PNR Number: {pnr}\n"
        f"Passenger: {name}\n"
        f"Age: {age}\n"
        f"Train: {train[1]}\n"
        f"Train Number: {train[0]}\n"
        f"Route: {source} to {destination}\n"
        f"Journey Date: {date}\n"
        f"Seat Number: {seat}\n"
        f"Seat Preference: {preference}\n"
        f"Fare: ₹{fare}\n"
        f"Payment: {payment}\n"
        f"Status: CONFIRMED"
    )

    refresh_seats()
    search()




def cancel():
    pnr = pnr_entry.get().strip()

    if not pnr.isdigit() or len(pnr) != 10:
        messagebox.showwarning(
            "Invalid PNR",
            "Enter a valid 10-digit PNR number."
        )
        return

    for booking in bookings:
        if booking[0] == pnr:
            bookings.remove(booking)

            messagebox.showinfo(
                "Cancelled",
                f"Ticket with PNR {pnr} has been cancelled.\n"
                "The seat is now available again."
            )

            refresh_seats()
            search()
            return

    messagebox.showerror("Not Found", "No booking found with this PNR.")




def view_bookings():
    window = Toplevel(root)
    window.title("All Bookings")
    window.geometry("1050x450")

    Label(
        window,
        text="BOOKING DETAILS",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    columns = (
        "PNR", "Name", "Age", "Train", "Date",
        "Fare", "Seat", "Preference", "Payment"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=105)

    table.pack(fill=BOTH, expand=True, padx=10, pady=10)

    for booking in bookings:
        table.insert(
            "",
            END,
            values=(
                booking[0],
                booking[1],
                booking[2],
                booking[3],
                booking[4],
                "₹" + str(booking[5]),
                booking[6],
                booking[7],
                booking[8]
            )
        )

    if not bookings:
        Label(window, text="No bookings available.").pack(pady=10)




def clear():
    name_entry.delete(0, END)
    age_entry.delete(0, END)
    date_entry.delete(0, END)
    pnr_entry.delete(0, END)

    source_var.set("")
    destination_var.set("")
    train_var.set("")
    preference_var.set("Any")
    seat_var.set("")
    payment_var.set("")

    seat_box["values"] = []
    fare_label.config(text="Fare: ₹0")

    train_display.delete("1.0", END)

Label(
    root,
    text="RAILWAY RESERVATION SYSTEM",
    font=("Arial", 23, "bold"),
    bg="#eaf2f8",
    fg="#17365d"
).pack(pady=15)

form = Frame(root, bg="#eaf2f8")
form.pack(pady=5)

label_font = ("Arial", 11, "bold")
entry_font = ("Arial", 11)


def make_label(text, row):
    Label(
        form,
        text=text,
        font=label_font,
        bg="#eaf2f8"
    ).grid(row=row, column=0, padx=15, pady=8, sticky="w")




make_label("Passenger Name:", 0)
name_entry = Entry(form, font=entry_font, width=30)
name_entry.grid(row=0, column=1, pady=8)

make_label("Passenger Age:", 1)
age_entry = Entry(form, font=entry_font, width=30)
age_entry.grid(row=1, column=1, pady=8)



make_label("Source:", 2)
source_var = StringVar()
source_box = ttk.Combobox(
    form,
    textvariable=source_var,
    values=cities,
    state="readonly",
    width=28
)
source_box.grid(row=2, column=1, pady=8)

make_label("Destination:", 3)
destination_var = StringVar()
destination_box = ttk.Combobox(
    form,
    textvariable=destination_var,
    values=cities,
    state="readonly",
    width=28
)
destination_box.grid(row=3, column=1, pady=8)



make_label("Journey Date (DD-MM-YYYY):", 4)
date_entry = Entry(form, font=entry_font, width=30)
date_entry.grid(row=4, column=1, pady=8)



make_label("Train Number:", 5)
train_var = StringVar()
train_box = ttk.Combobox(
    form,
    textvariable=train_var,
    values=[str(train[0]) for train in trains],
    state="readonly",
    width=28
)
train_box.grid(row=5, column=1, pady=8)

train_box.bind("<<ComboboxSelected>>", refresh_seats)



make_label("Seat Preference:", 6)
preference_var = StringVar(value="Any")
preference_box = ttk.Combobox(
    form,
    textvariable=preference_var,
    values=["Any", "Window", "Middle", "Aisle"],
    state="readonly",
    width=28
)
preference_box.grid(row=6, column=1, pady=8)
preference_box.bind("<<ComboboxSelected>>", refresh_seats)



make_label("Select Seat Number:", 7)
seat_var = StringVar()
seat_box = ttk.Combobox(
    form,
    textvariable=seat_var,
    state="readonly",
    width=28
)
seat_box.grid(row=7, column=1, pady=8)



make_label("Payment Method:", 8)
payment_var = StringVar()
payment_box = ttk.Combobox(
    form,
    textvariable=payment_var,
    values=["UPI (Simulation)", "Debit/Credit Card (Simulation)", "Cash (Simulation)"],
    state="readonly",
    width=28
)
payment_box.grid(row=8, column=1, pady=8)



fare_label = Label(
    form,
    text="Fare: ₹0",
    font=("Arial", 14, "bold"),
    bg="#eaf2f8",
    fg="#087e3d"
)
fare_label.grid(row=9, column=1, pady=10)



make_label("PNR for Cancellation:", 10)
pnr_entry = Entry(form, font=entry_font, width=30)
pnr_entry.grid(row=10, column=1, pady=8)




button_frame = Frame(root, bg="#eaf2f8")
button_frame.pack(pady=12)

Button(
    button_frame,
    text="Search Train",
    command=search,
    width=17,
    bg="#2874a6",
    fg="white"
).grid(row=0, column=0, padx=5, pady=5)

Button(
    button_frame,
    text="Available Trains",
    command=available_trains,
    width=17,
    bg="#2874a6",
    fg="white"
).grid(row=0, column=1, padx=5, pady=5)

Button(
    button_frame,
    text="Pay & Book Ticket",
    command=book,
    width=17,
    bg="#239b56",
    fg="white"
).grid(row=1, column=0, padx=5, pady=5)

Button(
    button_frame,
    text="Cancel Ticket",
    command=cancel,
    width=17,
    bg="#c0392b",
    fg="white"
).grid(row=1, column=1, padx=5, pady=5)

Button(
    button_frame,
    text="View Bookings",
    command=view_bookings,
    width=17,
    bg="#7d3c98",
    fg="white"
).grid(row=2, column=0, padx=5, pady=5)

Button(
    button_frame,
    text="Clear All",
    command=clear,
    width=17,
    bg="#566573",
    fg="white"
).grid(row=2, column=1, padx=5, pady=5)



Label(
    root,
    text="TRAIN SEARCH RESULTS",
    font=("Arial", 13, "bold"),
    bg="#eaf2f8"
).pack(pady=5)

train_display = Text(
    root,
    height=8,
    width=85,
    font=("Arial", 10)
)
train_display.pack(pady=5)



root.mainloop()
