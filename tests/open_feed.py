import importlib.util
import os

# Ruta al archivo feed.py
file_path = os.path.abspath("../src/feed.py")  # Ruta relativa a src/feed.py

# Verificar si el archivo existe
if not os.path.exists(file_path):
    raise FileNotFoundError(f"El archivo no se encontró en la ruta: {file_path}")

# Cargar dinámicamente el módulo
spec = importlib.util.spec_from_file_location("feed", file_path)
feed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(feed)

# Llamar a funciones del módulo
feed.open_feed()  # Usa funciones o variables del archivo feed.py
