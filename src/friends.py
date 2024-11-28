import tkinter as tk
import sys
import os
from index_list import Index_List  # Asegúrate de que Index_List esté en el mismo directorio o en el PYTHONPATH

def open_friends_window(user_id):
    """Display a list of friends for the given user ID."""
    # Initialize Index_List with the paths to the datasets
    script_dir = os.path.dirname(os.path.abspath(__file__))
    users_file = os.path.join(script_dir, "../assets/data/users.csv")
    relations_file = os.path.join(script_dir, "../assets/data/relations.csv")
    index_list = Index_List(users_file, relations_file)

    # Get the list of friends
    friends = index_list.get_user_friends(user_id)

    # Create the friends window
    friends_window = tk.Tk()
    friends_window.title("Friends List")
    friends_window.geometry("400x600")

    # Add title
    title_label = tk.Label(friends_window, text=f"Friends of User {user_id}", font=("Arial", 16))
    title_label.pack(pady=20)

    # If no friends are found
    if not friends:
        no_friends_label = tk.Label(friends_window, text="No friends found.", font=("Arial", 12))
        no_friends_label.pack(pady=20)
        return

    # Display each friend's information
    for friend in friends:
        friend_frame = tk.Frame(friends_window, bg="lightgray", pady=5, padx=5, relief=tk.RIDGE, borderwidth=2)
        friend_frame.pack(fill="x", padx=10, pady=5)

        friend_label = tk.Label(friend_frame, text=f"Username: {friend['username']}", font=("Arial", 14), bg="lightgray")
        friend_label.pack(anchor="w", padx=10)

        description_label = tk.Label(friend_frame, text=f"Description: {friend['description']}", font=("Arial", 12), bg="lightgray")
        description_label.pack(anchor="w", padx=10)

    # Button to close the window
    close_button = tk.Button(friends_window, text="Close", font=("Arial", 12), command=friends_window.destroy)
    close_button.pack(pady=10)

    friends_window.mainloop()

if __name__ == "__main__":
    # Ensure a user_id is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Error: User ID not provided.")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])  # Convert user_id to integer
    except ValueError:
        print("Error: User ID must be an integer.")
        sys.exit(1)

    open_friends_window(user_id)
