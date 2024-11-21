import importlib.util
import os

# Ruta al archivo feed.py
file_path = os.path.abspath("../src/feed.py")

try:
    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo no se encontró en la ruta: {file_path}")

    # Cargar dinámicamente el módulo feed.py
    spec = importlib.util.spec_from_file_location("feed", file_path)
    feed = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(feed)

    # Llamar a la función open_feed()
    feed.open_feed()
except FileNotFoundError as e:
    print(f"Error: {e}")
except AttributeError:
    print("Error: La función 'open_feed' no existe en el módulo.")
except Exception as e:
    print(f"Error inesperado: {e}")
