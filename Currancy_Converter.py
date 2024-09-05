from tkinter import mainloop, Tk, Label, Entry, Button, END, Text
import json
from urllib.request import urlopen
import urllib.error
from datetime import datetime
import os

# --------------------------------------------------------------------------- #

# class to store conversion data
class Conversion:
    # class constructor
    def __init__(self,currancy1,currancy2,amount):
        self.currancy1 = currancy1
        self.currancy2 = currancy2
        self.rate = rate
        self.amount = 0.0
        self.result = 0.0

    # method that returns instance data as a formatted string
    def __str__(self):
        return f"""Conversion from {self.currancy1} to {self.currancy2}
Amount: {self.amount}
Rate: {"%.5f" % float(self.rate)}
Result: {"%.2f" % float(self.result)}
Date: {datetime.utcnow().date()}"""

# --------------------------------------------------------------------------- #

# function that fetches conversion data from API
def get_exchange_data(conversion):
    error_message = None
    try:
        # gets exchane data for currancy 1
        url = "http://www.floatrates.com/daily/" + conversion.currancy1 + ".json"
        with urlopen(url) as response:
            source = response.read()

        # parses JOSN data into a python dictonary
        data = json.loads(source)
        # gets the rate of exchange and calculates the resulting amount
        conversion.rate = data[conversion.currancy2]["rate"]
        conversion.result = (conversion.amount * float(conversion.rate))
    except urllib.error.URLError:
        error_message = "Could not connect to intenet, please try again later."
    except:
        error_message = "One or both of your currancy codes are invalid"
    return error_message


def save_data(conversion):
    # gets the path to logs file
    path = os.path.dirname(os.path.abspath(__file__)) + "\\conversion_logs.txt"
    # reads the data from the text file
    with open(path, "r") as f:
        f_data = f.read()
    # appends the new conversion data
    f_data +=f"""\n{str(conversion)}\n"""
    # writes the updated data to the text file
    with open(path, "w") as f:
        f.write(f_data)


def output(message):
    # creates output window to display message
    output_field = Text(window, width=30,height=6)
    output_field.grid(row=5,column=0)
    output_field.insert(END,message)


def display_message():
    # gets the data from inputs
    C1 = C1_input.get().lower()
    C2 = C2_input.get().lower()
    try:
        amount = float(amount_input.get())
    except:
        output("Please input a valid amount (No text or symbols).")
        return

    # checks if amount input is valid
    if conversion.amount <= 0:
        output("Invalid amount")
        return
        
    # creates instance of Conversion class using user inputs
    conversion = Conversion(C1,C2,amount)
    # gets the exchange rate data and catches any errors
    error = get_exchange_data(conversion)

    # outputs conversion data or any errors
    if error:
        output(error)
    else:
        output(conversion)
        save_data(conversion)
    
# --------------------------------------------------------------------------- #

# creates window and sets its attributes
window = Tk()
window.title("Currancy Converter")
window.geometry("300x260")
window.configure(background='#b1dbe6')

# Heading label
Label(window, text="Currancy Converter", font="Times 20 bold", bg="#b1dbe6").grid(row=0, column=0)
Label(window, text="From:", font="Broadway 15", bg="#b1dbe6").grid(row=1, column=0)

# input field for currancy 1
C1_input = Entry(window, width=4)
C1_input.grid(row=1, column=1)

Label(window, text="To:", font="Broadway 15", bg="#b1dbe6").grid(row=2, column=0)

# input field for currancy 2
C2_input = Entry(window, width=4)
C2_input.grid(row=2, column=1)

Label(window, text="Amount:", font="Broadway 15", bg="#b1dbe6").grid(row=3, column=0)

# input field for amount
amount_input = Entry(window, width=7)
amount_input.grid(row=3, column=1)

# button to start convert
Button(window, text="Calculate", command=display_message, bg="black", fg="white").grid(row=4, column=0)

# keeps window up
window.mainloop()
