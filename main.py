# Importing necessary libraries
from tkinter import *
from tkinter import messagebox, END
import pyperclip
import random
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    # Define the characters used to generate the password
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Randomly select the number of characters for each category
    nr_letters = random.randint(8, 12)  # Choose a random number of letters (8 to 12)
    nr_symbols = random.randint(2, 5)  # Choose a random number of symbols (2 to 5)
    nr_numbers = random.randint(2, 5)  # Choose a random number of numbers (2 to 5)

    # Create random selections from each category
    password_letters = [random.choice(letters) for i in range(nr_letters)]
    password_symbols = [random.choice(symbols) for j in range(nr_symbols)]
    password_number = [random.choice(numbers) for k in range(nr_numbers)]

    # Combine all selected characters into one list and shuffle them for randomness
    password_list = password_number + password_symbols + password_letters
    random.shuffle(password_list)

    # Convert the list of characters into a string and insert it into the password entry field
    password = "".join(password_list)
    password_entry.insert(END, password)

    # Copy the generated password to the clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    # Get the website, username, and password from the user input
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Create a new dictionary with the entered information
    new_data = {
        website.upper(): {
            "email:": username,
            "password:": password,
        }
    }

    # Check if any fields are left empty and show an error message
    if len(website) == 0 or len(username) == 0:
        messagebox.showerror(title="Oops", message="You forgot to fill in something!")
    else:
        # Try to open the existing passwords.json file and load its content
        try:
            with open("passwords.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            # If the file doesn't exist, create a new one and store the new data
            with open("passwords.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            # If the file exists, update it with the new data
            data.update(new_data)
            with open("passwords.json", "w") as f:
                json.dump(data, f, indent=4)

        # Clear the input fields after saving
        website_entry.delete(0, END)
        password_entry.delete(0, END)


# -------------------------- SEARCH FILE ------------------------------ #
def search():
    # Get the website name from the user input
    query = website_entry.get().upper()

    try:
        # Try to open and load the passwords.json file
        with open("passwords.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, show an error message
        messagebox.showinfo(title="Oops", text="No Data File Found.")
    else:
        # If the website is found in the stored data, show its details
        if query in data:
            email = data[query]["email:"]
            password = data[query]["password:"]
            messagebox.showinfo(title=query, message=f"E-mail: {email}\nPassword: {password}")
            pyperclip.copy(password)  # Copy the password to the clipboard
        else:
            # If no details are found for the website, show a message
            messagebox.showinfo(title="Oops", message=f"No details for {query} exists.")


# ---------------------------- UI SETUP ------------------------------- #
# Initialize the window
window = Tk()
window.title("Password Generator")  # Set the window title
window.config(padx=100, pady=50, bg="white")  # Set padding and background color

# Create a canvas to display the logo image
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock_img = PhotoImage(file="logo.png")  # Load the logo image
canvas.create_image(100, 100, image=lock_img)  # Add the image to the canvas
canvas.grid(row=0, column=1)

# Label for the website entry field
website_label = Label(text="Website:", bg="white", font=("Arial", 12), pady=5, padx=5)
website_label.grid(row=1, column=0)

# Entry field for the website
website_entry = Entry(width=27)
website_entry.grid(row=1, column=1)
website_entry.focus()  # Set focus to this field by default

# Label for the username/email entry field
username_label = Label(text="E-mail/Username:", bg="white", font=("Arial", 12), pady=5, padx=5)
username_label.grid(row=2, column=0)

# Entry field for the username/email, with a default value
username_entry = Entry(width=45)
username_entry.insert(END, "michael.michaels3000@yahoo.com")
username_entry.grid(row=2, column=1, columnspan=2)

# Label for the password entry field
password_label = Label(text="Password:", bg="white", font=("Arial", 12), pady=5, padx=5)
password_label.grid(row=3, column=0)

# Entry field for the password
password_entry = Entry(width=27)
password_entry.grid(row=3, column=1)

# Button to generate a random password
generate_button = Button(text="Generate Password", font=("Arial", 8), command=generate)
generate_button.grid(row=3, column=2)

# Button to save the entered password data
add_button = Button(text="Add", width=37, pady=5, padx=5, command=save_data)
add_button.grid(row=4, column=1, columnspan=2)

# Button to search for stored passwords
search_button = Button(text="Search", font=("Arial", 8), width=16, command=search)
search_button.grid(row=1, column=2)

# Start the Tkinter main loop to keep the app running
window.mainloop()
