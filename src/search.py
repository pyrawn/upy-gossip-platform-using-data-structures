import tkinter as tk
from tkinter import messagebox
import os
import csv


def send_friend_request(sender_id, receiver_id):
    """Send a friend request by appending it to the requests.csv file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requests_file = os.path.join(script_dir, "../assets/data/requests.csv")

    try:
        # Ensure IDs are integers
        sender_id, receiver_id = int(sender_id), int(receiver_id)

        # Append the friend request to the file
        with open(requests_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([sender_id, receiver_id])

        messagebox.showinfo("Success", f"Friend request sent to user {receiver_id}.")
    except ValueError:
        messagebox.showerror("Error", f"Invalid sender_id or receiver_id: {sender_id}, {receiver_id}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send friend request: {e}")


def search_users(user_id):
    """Search for users and allow sending friend requests."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    users_file = os.path.join(script_dir, "../assets/data/users.csv")

    # Load users from the file
    users = []
    try:
        with open(users_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(row)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load users: {e}")
        return

    # Create search window
    search_window = tk.Tk()
    search_window.title("Search Users")
    search_window.geometry("400x600")

    # Add a search box and button
    search_label = tk.Label(search_window, text="Search Users", font=("Arial", 16))
    search_label.pack(pady=10)

    search_entry = tk.Entry(search_window, font=("Arial", 12))
    search_entry.pack(pady=5)

    def perform_search():
        query = search_entry.get().lower()
        results_frame = tk.Frame(search_window)
        results_frame.pack(fill="both", expand=True, pady=10)

        for widget in results_frame.winfo_children():
            widget.destroy()

        # Filter users by query
        for user in users:
            if query in user["username"].lower():
                result_label = tk.Label(results_frame, text=user["username"], font=("Arial", 14))
                result_label.pack(anchor="w", padx=10, pady=2)

                send_button = tk.Button(
                    results_frame,
                    text="Send Request",
                    font=("Arial", 12),
                    bg="lightblue",
                    command=lambda receiver_id=user["id"]: send_friend_request(user_id, receiver_id),
                )
                send_button.pack(anchor="e", padx=10, pady=2)

    search_button = tk.Button(search_window, text="Search", font=("Arial", 12), command=perform_search)
    search_button.pack(pady=5)

    search_window.mainloop()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Error: User ID not provided.")
        sys.exit(1)

    user_id = int(sys.argv[1])
    search_users(user_id)
