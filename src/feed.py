import tkinter as tk
from tkinter import ttk
import csv
import os
import subprocess  # To execute external Python scripts
try:
    from src.stack import Stack  # When running from the project root
except ModuleNotFoundError:
    from .stack import Stack  # When running from within the `src` folder

from src import notifications  # Adjust the path according to your project structure
from .tree import CommentTree  # Importamos la clase del árbol de comentarios


def load_users():
    """Loads users from users.csv and returns them as a dictionary."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    users_file = os.path.join(script_dir, "../assets/data/users.csv")

    users = {}
    try:
        with open(users_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[int(row["id"])] = row["username"]  # Maps ID to username
    except FileNotFoundError:
        print("Error: users.csv file not found.")
    return users


def load_posts_and_comments():
    """Cargar publicaciones y comentarios en un CommentTree."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    posts_file = os.path.join(script_dir, "../assets/data/posts.csv")

    comment_tree = CommentTree()
    try:
        with open(posts_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                post_id = int(row["post_id"])
                post_text = row["post_text"]
                author_id = int(row["author_id"])
                parent_id = int(row["parent_id"]) if "parent_id" in row and row["parent_id"] else None
                comment_tree.add_node(post_id, {"text": post_text, "author_id": author_id}, parent_id)
    except FileNotFoundError:
        print("No posts file found.")
    return comment_tree


def add_post(author_id, text, parent_id=None):
    """Agregar un nuevo post o comentario al archivo posts.csv."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    posts_file = os.path.join(script_dir, "../assets/data/posts.csv")

    try:
        with open(posts_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            last_post_id = max([int(row["post_id"]) for row in reader], default=0)
    except FileNotFoundError:
        last_post_id = 0

    new_post = {
        "post_id": last_post_id + 1,
        "post_text": text,
        "author_id": author_id,
        "parent_id": parent_id or "",
        "date": "2024-11-26"  # Reemplaza con la fecha actual si es necesario
    }

    try:
        with open(posts_file, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["post_id", "post_text", "author_id", "parent_id", "date"])
            if last_post_id == 0:  # Si el archivo estaba vacío, escribir encabezados
                writer.writeheader()
            writer.writerow(new_post)
    except Exception as e:
        print(f"Error adding post: {e}")


def display_posts(canvas, frame, comment_tree, users, user_id):
    """Muestra publicaciones y comentarios en el feed."""
    for node in comment_tree.get_root_nodes():
        display_post(canvas, frame, node, users, user_id)


def display_post(canvas, frame, node, users, user_id, depth=0):
    """Muestra un post o comentario, con sangría para respuestas."""
    author_name = users.get(node.data["author_id"], "Unknown User")
    text = node.data["text"]

    post_frame = tk.Frame(frame, borderwidth=1, relief="solid", padx=10, pady=10, bg="lightgray")
    post_frame.pack(fill="x", padx=10 + depth * 20, pady=5)

    author_label = tk.Label(post_frame, text=f"{author_name}:", font=("Arial", 12, "bold"))
    author_label.pack(anchor="w")

    text_label = tk.Label(post_frame, text=text, font=("Arial", 12), wraplength=500, justify="left")
    text_label.pack(anchor="w")

    comment_button = tk.Button(post_frame, text="Comment", font=("Arial", 10), command=lambda: open_comment_window(user_id, node.id))
    comment_button.pack(anchor="e")

    for child in node.children:
        display_post(canvas, frame, child, users, user_id, depth + 1)


def open_comment_window(user_id, parent_id):
    """Abrir una ventana para comentar un post."""
    comment_window = tk.Tk()
    comment_window.title("Add Comment")

    label = tk.Label(comment_window, text="Write your comment:", font=("Arial", 12))
    label.pack(pady=10)

    text_area = tk.Text(comment_window, height=5, width=40)
    text_area.pack(pady=10)

    submit_button = tk.Button(
        comment_window,
        text="Submit",
        command=lambda: submit_comment(user_id, text_area.get("1.0", tk.END).strip(), parent_id, comment_window)
    )
    submit_button.pack(pady=10)

    comment_window.mainloop()


def submit_comment(user_id, text, parent_id, comment_window):
    """Guardar un comentario y recargar el feed."""
    if text:
        add_post(user_id, text, parent_id)
        comment_window.destroy()
        open_feed(user_id, load_users()[int(user_id)])

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

def open_profile(user_id):
    """Abre el perfil del usuario."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    profile_script = os.path.join(script_dir, "profile.py")

    try:
        subprocess.Popen(["python", profile_script, str(user_id)])  # Ejecutar profile.py con el user_id
    except FileNotFoundError:
        print("Error: profile.py file not found.")
    except Exception as e:
        print(f"An error occurred while opening profile.py: {e}")


def open_feed(user_id, user_name):
    """Abre el feed principal."""
    feed_window = tk.Tk()
    feed_window.title("Feed")

    label_feed = tk.Label(feed_window, text=f"Welcome to your Feed, {user_name}", font=("Arial", 16))
    label_feed.pack(pady=20)

    nav_frame = tk.Frame(feed_window)
    nav_frame.pack(fill="x", pady=10)

    notifications_button = tk.Button(nav_frame, text="Notifications", width=15, command=lambda: open_notifications(user_id))
    notifications_button.pack(side="left", padx=5)

    profile_button = tk.Button(nav_frame, text="Profile", width=15, command=lambda: open_profile(user_id))
    profile_button.pack(side="left", padx=5)

    friend_requests_button = tk.Button(
        nav_frame,
        text="Friend Requests",
        width=20,
        command=lambda: open_friend_requests(user_id)
    )
    friend_requests_button.pack(side="left", padx=5)

    search_button = tk.Button(nav_frame, text="Search Users", width=15, command=lambda: open_search(user_id))
    search_button.pack(side="left", padx=5)

    canvas = tk.Canvas(feed_window)
    scroll_y = tk.Scrollbar(feed_window, orient="vertical", command=canvas.yview)
    feed_frame = tk.Frame(canvas)

    feed_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=feed_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    users = load_users()
    comment_tree = load_posts_and_comments()

    display_posts(canvas, feed_frame, comment_tree, users, user_id)

    new_post_button = tk.Button(
        feed_window,
        text="Add New Post",
        font=("Arial", 12),
        command=lambda: open_comment_window(user_id, None)
    )
    new_post_button.pack(pady=10)

    logout_button = tk.Button(feed_window, text="Logout", command=feed_window.quit)
    logout_button.pack(pady=10)

    feed_window.mainloop()


def open_notifications(user_id):
    notifications.open_notifications(user_id)

