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


def delete_post(post_id, user_id, root):
    """Delete a post by its ID."""
    file_path = os.path.join(os.getcwd(), 'assets', 'data', 'posts.csv')
    try:
        posts = pd.read_csv(file_path)
        posts = posts[posts['post_id'] != post_id]  # Remove the post with the given ID
        posts.to_csv(file_path, index=False)  # Save the updated posts
        messagebox.showinfo("Success", "Post deleted successfully!")
        root.destroy()  # Close the current window
        profile_interface(tk.Tk(), user_id)  # Reload the profile interface
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete post: {e}")


def update_description(user_id, new_description, root):
    """Update the user's description."""
    file_path = os.path.join(os.getcwd(), 'assets', 'data', 'users.csv')
    try:
        users = pd.read_csv(file_path)
        users.loc[users['id'] == user_id, 'description'] = new_description
        users.to_csv(file_path, index=False)  # Save the updated users
        messagebox.showinfo("Success", "Description updated successfully!")
        root.destroy()  # Close the current window
        profile_interface(tk.Tk(), user_id)  # Reload the profile interface
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update description: {e}")


def open_friends_window(user_id):
    """Opens the friends.py window with the user_id."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    friends_script = os.path.join(script_dir, "friends.py")
    try:
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

    # Button to update description
    update_desc_button = tk.Button(
        user_info_frame,
        text="Update Description",
        font=("Arial", 12),
        bg="lightblue",
        command=lambda: open_update_description_window(user_id, root)
    )
    update_desc_button.pack(pady=5)

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

        delete_button = tk.Button(
            post_frame,
            text="Delete Post",
            font=("Arial", 10),
            bg="red",
            command=lambda post_id=post['post_id']: delete_post(post_id, user_id, root)
        )
        delete_button.pack(anchor="e", pady=5)


def open_update_description_window(user_id, root):
    """Open a window to update the user's description."""
    update_window = tk.Tk()
    update_window.title("Update Description")

    label = tk.Label(update_window, text="Enter new description:", font=("Arial", 12))
    label.pack(pady=10)

    text_area = tk.Text(update_window, height=5, width=40)
    text_area.pack(pady=10)

    submit_button = tk.Button(
        update_window,
        text="Submit",
        command=lambda: update_description(user_id, text_area.get("1.0", tk.END).strip(), root)
    )
    submit_button.pack(pady=10)

    update_window.mainloop()


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
