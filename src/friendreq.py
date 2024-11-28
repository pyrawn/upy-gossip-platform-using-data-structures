import tkinter as tk
from tkinter import messagebox
from queue import Queue
import os
import csv
from datetime import datetime


def load_requests(user_id):
    """Load friend requests for the current user."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requests_file = os.path.join(script_dir, "../assets/data/requests.csv")
    requests_queue = Queue()

    if not os.path.exists(requests_file):
        return requests_queue

    try:
        with open(requests_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if int(row[1]) == user_id:  # Requests addressed to the current user
                    requests_queue.enqueue(row)
    except Exception as e:
        print(f"Error loading requests: {e}")
    return requests_queue


def save_requests(requests_queue):
    """Save the updated requests queue back to the file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    requests_file = os.path.join(script_dir, "../assets/data/requests.csv")

    try:
        with open(requests_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            while not requests_queue.is_empty():
                writer.writerow(requests_queue.dequeue())
    except Exception as e:
        print(f"Error saving requests: {e}")


def add_relation(sender_id, receiver_id):
    """Add a friendship relation to relations.csv."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    relations_file = os.path.join(script_dir, "../assets/data/relations.csv")

    try:
        # Load existing relations to avoid duplicates
        existing_relations = set()
        if os.path.exists(relations_file):
            with open(relations_file, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    # Convert row values to integers to avoid issues
                    try:
                        existing_relations.add(tuple(map(int, row)))
                    except ValueError:
                        print(f"Skipping invalid row: {row}")

        with open(relations_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Add the relationship in both directions if not already present
            if (sender_id, receiver_id) not in existing_relations:
                writer.writerow([sender_id, receiver_id])
            if (receiver_id, sender_id) not in existing_relations:
                writer.writerow([receiver_id, sender_id])
    except Exception as e:
        print(f"Error adding relation: {e}")



def add_notification(receiver_id, message):
    """Add a notification to the corresponding user's notification file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    notifications_file = os.path.join(script_dir, f"../assets/data/notification_users/{receiver_id}_notifications.csv")

    try:
        # Ensure the file exists
        if not os.path.exists(notifications_file):
            with open(notifications_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["id_notification", "message", "user_id", "date"])
                writer.writeheader()

        # Write the notification
        with open(notifications_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id_notification", "message", "user_id", "date"])
            notification_id = datetime.now().strftime("%Y%m%d%H%M%S")
            writer.writerow({
                "id_notification": notification_id,
                "message": message,
                "user_id": receiver_id,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    except Exception as e:
        print(f"Error adding notification: {e}")


def friend_requests_interface(user_id):
    """Interface to handle friend requests."""
    requests_queue = load_requests(user_id)

    requests_window = tk.Tk()
    requests_window.title("Friend Requests")
    requests_window.geometry("400x600")

    # Title
    title_label = tk.Label(requests_window, text="Friend Requests", font=("Arial", 16))
    title_label.pack(pady=10)

    def accept_request(request):
        # Remove request from the queue and save changes
        sender_id = int(request[0])  # Get sender ID from the request
        requests_queue.dequeue()
        save_requests(requests_queue)
        add_relation(sender_id, user_id)  # Add to relations.csv
        add_notification(sender_id, f"You are now friends with User {user_id}.")
        add_notification(user_id, f"You have added User {sender_id} as a friend.")
        messagebox.showinfo("Accepted", f"Friend request from User {sender_id} accepted.")
        requests_window.destroy()
        friend_requests_interface(user_id)

    def reject_request():
        # Simply dequeue the request
        requests_queue.dequeue()
        save_requests(requests_queue)
        messagebox.showinfo("Rejected", "Friend request rejected.")
        requests_window.destroy()
        friend_requests_interface(user_id)

    # Display requests
    if requests_queue.is_empty():
        no_requests_label = tk.Label(requests_window, text="No friend requests.", font=("Arial", 12))
        no_requests_label.pack(pady=20)
    else:
        request = requests_queue.front()
        sender_id = request[0]

        request_label = tk.Label(requests_window, text=f"Friend request from User {sender_id}", font=("Arial", 14))
        request_label.pack(pady=10)

        accept_button = tk.Button(requests_window, text="Accept", font=("Arial", 12), bg="lightgreen",
                                  command=lambda: accept_request(request))
        accept_button.pack(pady=5)

        reject_button = tk.Button(requests_window, text="Reject", font=("Arial", 12), bg="lightcoral",
                                  command=reject_request)
        reject_button.pack(pady=5)

    requests_window.mainloop()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Error: User ID not provided.")
        sys.exit(1)

    user_id = int(sys.argv[1])
    friend_requests_interface(user_id)
