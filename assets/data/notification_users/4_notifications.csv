import tkinter as tk
import csv
import os
from src.stack import Stack  # Ensure the Stack module is available

def load_notifications(user_id):
    """Load notifications for the user from the corresponding CSV file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    notifications_file = os.path.join(script_dir, f"../assets/data/notification_users/{user_id}_notifications.csv")

    notifications_stack = Stack()  # Stack to store notifications

    if os.path.exists(notifications_file):
        try:
            with open(notifications_file, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    notifications_stack.push(row)  # Push notifications into the stack (LIFO)
        except Exception as e:
            print(f"Error reading notifications file: {e}")
    else:
        # If the notifications file doesn't exist, create an empty one
        create_empty_notifications_file(user_id)

    return notifications_stack

def create_empty_notifications_file(user_id):
    """Create an empty notifications file for a new user."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    notifications_file = os.path.join(script_dir, f"../assets/data/notification_users/{user_id}_notifications.csv")

    try:
        with open(notifications_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ['id_notification', 'message', 'user_id', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()  # Write headers
            print(f"Created empty notifications file: {notifications_file}")
    except Exception as e:
        print(f"Error creating notifications file: {e}")

def open_notifications(user_id):
    """Open the user's notifications window."""
    notifications_stack = load_notifications(user_id)

    # Create the notifications window
    notifications_window = tk.Tk()
    notifications_window.title("Notifications")

    # Window title
    label_notifications = tk.Label(notifications_window, text="Your Notifications", font=("Arial", 16))
    label_notifications.pack(pady=20)

    # Frame to display the notifications
    notifications_frame = tk.Frame(notifications_window)
    notifications_frame.pack(fill="both", expand=True)

    # Display notifications from the stack
    while not notifications_stack.is_empty():
        notification = notifications_stack.pop()
        notification_id = notification["id_notification"]
        message = notification["message"]
        date = notification["date"]

        # Create a frame for each notification
        notification_frame = tk.Frame(notifications_frame, borderwidth=1, relief="solid", padx=10, pady=10)
        notification_frame.pack(fill="x", padx=10, pady=5)

        # Show message and date of the notification
        message_label = tk.Label(notification_frame, text=f"Message: {message}", font=("Arial", 12))
        message_label.pack(pady=5)

        date_label = tk.Label(notification_frame, text=f"Date: {date}", font=("Arial", 12))
        date_label.pack(pady=5)

        # Button to remove notification from the stack
        remove_button = tk.Button(notification_frame, text="Remove", command=lambda notif_id=notification_id: remove_notification(user_id, notif_id))
        remove_button.pack(pady=5)

    # Button to close notifications
    close_button = tk.Button(notifications_window, text="Close", command=notifications_window.quit)
    close_button.pack(pady=10)

    notifications_window.mainloop()

def remove_notification(user_id, notif_id):
    """Remove a notification from the stack and update the CSV file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    notifications_file = os.path.join(script_dir, f"../assets/data/notification_users/{user_id}_notifications.csv")

    notifications_stack = load_notifications(user_id)  # Load the current notifications
    updated_notifications = []

    # Keep the notifications that are not the one being removed
    while not notifications_stack.is_empty():
        notification = notifications_stack.pop()
        if notification["id_notification"] != notif_id:
            updated_notifications.append(notification)  # Keep the notification that isn't removed

    # Write the updated notifications back to the CSV file
    try:
        with open(notifications_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ['id_notification', 'message', 'user_id', 'date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()  # Write the header
            for notification in updated_notifications:
                writer.writerow(notification)  # Write the remaining notifications

        print(f"Notification {notif_id} removed successfully.")
    except Exception as e:
        print(f"Error removing notification: {e}")
