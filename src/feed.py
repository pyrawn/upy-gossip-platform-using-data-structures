import tkinter as tk
import csv
import os
import subprocess  # To execute external Python scripts
try:
    from src.stack import Stack  # When running from the project root
except ModuleNotFoundError:
    from .stack import Stack  # When running from within the `src` folder

from src import notifications  # Adjust the path according to your project structure


def load_users():
    """Loads users from users.csv and returns them as a dictionary."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    users_file = os.path.join(script_dir, "../assets/data/users.csv")

    users = {}
    try:
        with open(users_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["id"]] = row["username"]  # Maps ID to username
    except FileNotFoundError:
        print("Error: users.csv file not found.")
    return users


def open_profile(user_id):
    """Opens profile.py with the given user_id as a parameter."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    profile_script = os.path.join(script_dir, "profile.py")  # Path to profile.py

    try:
        subprocess.Popen(["python", profile_script, str(user_id)])  # Run profile.py with user_id
    except FileNotFoundError:
        print("Error: profile.py file not found.")
    except Exception as e:
        print(f"An error occurred while opening profile.py: {e}")


def open_search(user_id):
    """Opens search.py with the given user_id as a parameter."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    search_script = os.path.join(script_dir, "search.py")  # Path to search.py

    try:
        subprocess.Popen(["python", search_script, str(user_id)])  # Run search.py with user_id
    except FileNotFoundError:
        print("Error: search.py file not found.")
    except Exception as e:
        print(f"An error occurred while opening search.py: {e}")


def open_friend_requests(user_id):
    """Opens friendreq.py with the given user_id as a parameter."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    friendreq_script = os.path.join(script_dir, "friendreq.py")  # Path to friendreq.py

    try:
        subprocess.Popen(["python", friendreq_script, str(user_id)])  # Run friendreq.py with user_id
    except FileNotFoundError:
        print("Error: friendreq.py file not found.")
    except Exception as e:
        print(f"An error occurred while opening friendreq.py: {e}")


def open_feed(user_id, user_name):
    # Create the feed window
    feed_window = tk.Tk()
    feed_window.title("Feed")

    # Title in the feed window
    label_feed = tk.Label(feed_window, text=f"Welcome to your Feed, {user_name}", font=("Arial", 16))
    label_feed.pack(pady=20)

    # Frame for navigation buttons
    nav_frame = tk.Frame(feed_window)
    nav_frame.pack(fill="x", pady=10)

    # Navigation buttons
    notifications_button = tk.Button(nav_frame, text="Notifications", width=15, command=lambda: open_notifications(user_id))
    notifications_button.pack(side="left", padx=5)

    profile_button = tk.Button(nav_frame, text="Profile", width=15, command=lambda: open_profile(user_id))
    profile_button.pack(side="left", padx=5)

    friend_requests_button = tk.Button(
        nav_frame,
        text="Friend Requests",
        width=20,
        command=lambda: open_friend_requests(user_id)  # Open friendreq.py
    )
    friend_requests_button.pack(side="left", padx=5)

    search_button = tk.Button(nav_frame, text="Search Users", width=15, command=lambda: open_search(user_id))
    search_button.pack(side="left", padx=5)

    # Frame for the feed content
    feed_frame = tk.Frame(feed_window)
    feed_frame.pack(fill="both", expand=True)

    # Load users and posts
    users = load_users()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    posts_file = os.path.join(script_dir, "../assets/data/posts.csv")

    posts_stack = Stack()
    try:
        with open(posts_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                posts_stack.push(row)
    except FileNotFoundError:
        tk.Label(feed_window, text="No posts found.", font=("Arial", 12)).pack(pady=10)
        feed_window.mainloop()
        return

    # Display posts from the stack
    while not posts_stack.is_empty():
        post = posts_stack.pop()
        author_id = post["author_id"]
        author_name = users.get(author_id, "Unknown User")  # Find the author's name
        header = author_name
        date = post["date"]
        message = post["post_text"]

        # Create a frame for each post
        post_frame = tk.Frame(feed_frame, borderwidth=1, relief="solid", padx=10, pady=10)
        post_frame.pack(fill="x", padx=10, pady=5)

        # Header with author (left) and date (right)
        header_frame = tk.Frame(post_frame)
        header_frame.pack(fill="x")

        author_label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"), anchor="w")
        author_label.pack(side="left", expand=True)

        date_label = tk.Label(header_frame, text=date, font=("Arial", 12), anchor="e")
        date_label.pack(side="right", expand=True)

        # Message centered
        message_label = tk.Label(post_frame, text=message, font=("Arial", 12), wraplength=500, justify="center")
        message_label.pack(pady=5)

    # Button to logout (optional)
    logout_button = tk.Button(feed_window, text="Logout", command=feed_window.quit)
    logout_button.pack(pady=10)

    # Keep the feed window open until the user closes it
    feed_window.mainloop()


# Function to open notifications
def open_notifications(user_id):
    notifications.open_notifications(user_id)  # Call the open_notifications function in notifications.py
