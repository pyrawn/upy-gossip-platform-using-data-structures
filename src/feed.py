import tkinter as tk
import csv
import os
try:
    from src.stack import Stack  # Cuando se ejecuta desde la raíz del proyecto
except ModuleNotFoundError:
    from .stack import Stack  # Cuando se ejecuta dentro de la carpeta `src`

def load_users():
    """Carga los usuarios desde users.csv y los devuelve como un diccionario."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    users_file = os.path.join(script_dir, "../assets/data/users.csv")

    users = {}
    try:
        with open(users_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["id"]] = row["username"]  # Relaciona ID con nombre de usuario
    except FileNotFoundError:
        print("Error: No se encontró el archivo users.csv.")
    return users

def open_feed(user_id,user_name):
    # Crear la ventana del feed
    feed_window = tk.Tk()
    feed_window.title("Feed")

    # Título en la ventana del feed
    label_feed = tk.Label(feed_window, text=f"Bienvenido a tu Feed {user_name}", font=("Arial", 16))
    label_feed.pack(pady=20)

    # Frame para los botones de navegación
    nav_frame = tk.Frame(feed_window)
    nav_frame.pack(fill="x", pady=10)

    # Botones de navegación
    notifications_button = tk.Button(nav_frame, text="Notificaciones", width=15)
    notifications_button.pack(side="left", padx=5)

    profile_button = tk.Button(nav_frame, text="Perfil", width=15)
    profile_button.pack(side="left", padx=5)

    friend_requests_button = tk.Button(nav_frame, text="Solicitudes de Amistad", width=20)
    friend_requests_button.pack(side="left", padx=5)

    # Frame para contener el feed
    feed_frame = tk.Frame(feed_window)
    feed_frame.pack(fill="both", expand=True)

    # Cargar usuarios y posts
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
        tk.Label(feed_window, text="No se encontraron publicaciones.", font=("Arial", 12)).pack(pady=10)
        feed_window.mainloop()
        return

    # Mostrar los posts desde la pila
    while not posts_stack.is_empty():
        post = posts_stack.pop()
        author_id = post["author_id"]
        author_name = users.get(author_id, "Usuario desconocido")  # Buscar el nombre del autor
        header = author_name
        date = post["date"]
        message = post["post_text"]

        # Crear un frame para cada post
        post_frame = tk.Frame(feed_frame, borderwidth=1, relief="solid", padx=10, pady=10)
        post_frame.pack(fill="x", padx=10, pady=5)

        # Header con autor (izquierda) y fecha (derecha)
        header_frame = tk.Frame(post_frame)
        header_frame.pack(fill="x")

        author_label = tk.Label(header_frame, text=header, font=("Arial", 14, "bold"), anchor="w")
        author_label.pack(side="left", expand=True)

        date_label = tk.Label(header_frame, text=date, font=("Arial", 12), anchor="e")
        date_label.pack(side="right", expand=True)

        # Mensaje centrado
        message_label = tk.Label(post_frame, text=message, font=("Arial", 12), wraplength=500, justify="center")
        message_label.pack(pady=5)

    # Botón para cerrar sesión (opcional)
    logout_button = tk.Button(feed_window, text="Cerrar sesión", command=feed_window.quit)
    logout_button.pack(pady=10)

    # Asegúrate de que el feed_window siga abierto hasta que el usuario cierre la ventana
    feed_window.mainloop()
