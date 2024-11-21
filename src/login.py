import tkinter as tk
from tkinter import messagebox
import csv
import os
from src.feed import open_feed
from . import signin  # Importa signin.py


# Function to read users from the CSV file
def read_users():
    users = {}
    file_path = os.path.join(os.getcwd(), 'assets', 'data', 'users.csv')  # Absolute path

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                user_id, username, password = row  # Adjusted for updated columns
                users[username] = {"user_id": user_id, "password": password}
    except FileNotFoundError:
        messagebox.showerror("Error", "The users file was not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
    return users


# Function to validate login
def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    users = read_users()

    if username in users and users[username]["password"] == password:
        user_id = users[username]["user_id"]  # Get the user_id of the logged-in user
        messagebox.showinfo("Login Successful", "Welcome to the system!")
        open_feed(user_id,username)  # Pass user_id to open_feed() when the login is successful
        root.destroy()  # Close the login window
    else:
        messagebox.showerror("Login Error", "Invalid username or password.")


# Function to open the sign-up window
def open_signin():
    signin.open_signin_window()  # Llama a la función en signin.py

# Create the login window using Tkinter
root = tk.Tk()
root.title("Login")

# Login interface elements
label_username = tk.Label(root, text="Username:")
label_username.grid(row=0, column=0, padx=10, pady=10)

entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)

label_password = tk.Label(root, text="Password:")
label_password.grid(row=1, column=0, padx=10, pady=10)

entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(root, text="Login", command=validate_login)
login_button.grid(row=2, columnspan=2, pady=10)

# Add a sign-up button
signup_button = tk.Button(root, text="Sign Up", command=open_signin)
signup_button.grid(row=3, columnspan=2, pady=10)

# Keep the login window open
root.mainloop()
