import tkinter as tk
from tkinter import messagebox
import csv
import os

# Function to get the next available user ID
def get_next_id():
    file_path = os.path.join(os.getcwd(), 'assets', 'data', 'users.csv')
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            max_id = 0
            for row in reader:
                user_id = int(row[0])  # Assumes ID is in the first column
                max_id = max(max_id, user_id)
            return max_id + 1  # Next available ID
    except FileNotFoundError:
        return 1  # If the file doesn't exist, start with ID 1

# Function to save a new user
def save_user(username, password):
    user_id = get_next_id()
    file_path = os.path.join(os.getcwd(), 'assets', 'data', 'users.csv')

    try:
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, username, password])
            messagebox.showinfo("Sign Up Successful", "You have been successfully registered!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the user: {e}")

# Function to validate sign-up and save the user
def validate_signup():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        save_user(username, password)
        signup_window.destroy()  # Close the sign-up window after successful registration
    else:
        messagebox.showerror("Sign Up Error", "Please enter both username and password.")

# Function to open the sign-up window
def open_signin_window():
    global signup_window, entry_username, entry_password
    signup_window = tk.Tk()
    signup_window.title("Sign Up")

    label_username = tk.Label(signup_window, text="Username:")
    label_username.grid(row=0, column=0, padx=10, pady=10)

    entry_username = tk.Entry(signup_window)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    label_password = tk.Label(signup_window, text="Password:")
    label_password.grid(row=1, column=0, padx=10, pady=10)

    entry_password = tk.Entry(signup_window, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    signup_button = tk.Button(signup_window, text="Sign Up", command=validate_signup)
    signup_button.grid(row=2, columnspan=2, pady=10)

    signup_window.mainloop()
