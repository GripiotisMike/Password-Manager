from tkinter import *
from tkinter import messagebox, END
import pyperclip
import random
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 12)
    nr_symbols = random.randint(2, 5)
    nr_numbers = random.randint(2, 5)

    password_letters = [random.choice(letters) for i in range(nr_letters)]
    password_symbols = [random.choice(symbols) for j in range(nr_symbols)]
    password_number = [random.choice(numbers) for k in range(nr_numbers)]
    password_list = password_number + password_symbols + password_letters
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website.upper(): {
            "email:": username,
            "password:": password,
        }
    }
    if len(website) == 0 or len(username) == 0:
        messagebox.showerror(title="Oops", message="You forgot to fill in something!")
    else:
        try:
            with open("passwords.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open("passwords.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            data.update(new_data)
            with open("passwords.json", "w") as f:
                json.dump(data, f, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

    # -------------------------- SEARCH FILE ------------------------------ #


def search():
    query = website_entry.get().upper()
    try:
        with open("passwords.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", text="No Data File Found.")
    else:
        if query in data:
            email = data[query]["email:"]
            password = data[query]["password:"]
            messagebox.showinfo(title=query, message=f"E-mail: {email}\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="Oops", message=f"No details for {query} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config(padx=100, pady=50, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", bg="white", font=("Arial", 12), pady=5, padx=5)
website_label.grid(row=1, column=0)

website_entry = Entry(width=27)
website_entry.grid(row=1, column=1)
website_entry.focus()

username_label = Label(text="E-mail/Username:", bg="white", font=("Arial", 12), pady=5, padx=5)
username_label.grid(row=2, column=0)

username_entry = Entry(width=45)
username_entry.insert(END, "michael.michaels3000@yahoo.com")
username_entry.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password:", bg="white", font=("Arial", 12), pady=5, padx=5)
password_label.grid(row=3, column=0)

password_entry = Entry(width=27)
password_entry.grid(row=3, column=1)

generate_button = Button(text="Generate Password", font=("Arial", 8), command=generate)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=37, pady=5, padx=5, command=save_data)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", font=("Arial", 8), width=16, command=search)
search_button.grid(row=1, column=2)

window.mainloop()
