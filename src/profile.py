import tkinter as tk
from tkinter import messagebox
import pandas as pd
from stack import Stack
import os
import sys
import subprocess  # To open friends.py as a new process


def load_user_data(user_id):
    try:
        file_path = os.path.join(os.getcwd(), 'assets', 'data', 'users.csv')  # Absolute path
        users = pd.read_csv(file_path)
        user = users.loc[users['id'] == user_id]
        if user.empty:
            return None
        return {
            "username": user.iloc[0]['username'],
            "description": user.iloc[0]['description']
        }
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load user data: {e}")
        return None


def load_user_posts(user_id):
    try:
        file_path = os.path.join(os.getcwd(), 'assets', 'data', 'posts.csv')  # Absolute path
        posts = pd.read_csv(file_path)
        user_posts = posts[posts['author_id'] == user_id]
        stack = Stack()
        for _, post in user_posts.iterrows():
            stack.push({
                "post_id": post['post_id'],
                "post_text": post['post_text'],
                "date": post['date']
            })
        return stack
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load user posts: {e}")
        return Stack()


def open_friends_window(user_id):
    """Opens the friends.py window with the user_id."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    friends_script = os.path.join(script_dir, "friends.py")
    try:
        # Execute friends.py with the user_id as an argument
        subprocess.Popen(["python", friends_script, str(user_id)])  
    except FileNotFoundError:
        messagebox.showerror("Error", "friends.py file not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open friends.py: {e}")


def profile_interface(root, user_id):
    user_data = load_user_data(user_id)

    if not user_data:
        messagebox.showwarning("Warning", "User not available")
        return

    # Main Frame
    profile_frame = tk.Frame(root, bg="white")
    profile_frame.pack(fill=tk.BOTH, expand=True)

    # User Info
    user_info_frame = tk.Frame(profile_frame, bg="lightblue", pady=10)
    user_info_frame.pack(fill=tk.X)

    username_label = tk.Label(user_info_frame, text=f"Username: {user_data['username']}", font=("Arial", 16), bg="lightblue")
    username_label.pack(anchor="w", padx=10)

    description_label = tk.Label(user_info_frame, text=f"Description: {user_data['description']}", font=("Arial", 12), bg="lightblue")
    description_label.pack(anchor="w", padx=10)

    # Button to open friends window
    friends_button = tk.Button(
        user_info_frame,
        text="Check Friends",
        font=("Arial", 12),
        bg="lightgreen",
        command=lambda: open_friends_window(user_id)  # Open friends.py with user_id
    )
    friends_button.pack(pady=10)

    # Posts Section
    posts_frame = tk.Frame(profile_frame, bg="white")
    posts_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    posts_label = tk.Label(posts_frame, text="User Posts", font=("Arial", 14), bg="white")
    posts_label.pack(anchor="w", padx=10, pady=5)

    posts_stack = load_user_posts(user_id)

    while not posts_stack.is_empty():
        post = posts_stack.pop()
        post_frame = tk.Frame(posts_frame, bg="lightgray", pady=5, padx=5, relief=tk.RIDGE, borderwidth=2)
        post_frame.pack(fill=tk.X, pady=5, padx=10)

        post_text = tk.Label(post_frame, text=f"{post['post_text']} (Date: {post['date']})", font=("Arial", 12), bg="lightgray")
        post_text.pack(anchor="w")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: User ID not provided.")
        sys.exit(1)
    
    try:
        user_id = int(sys.argv[1])  # Convert user_id to an integer
    except ValueError:
        print("Error: User ID must be an integer.")
        sys.exit(1)

    root = tk.Tk()
    root.title("User Profile")
    root.geometry("400x600")

    # Pass the dynamic user_id
    profile_interface(root, user_id)

    root.mainloop()

