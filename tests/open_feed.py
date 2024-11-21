import os
import importlib.util

# Cambiar el directorio base al nivel del proyecto
project_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(project_base)

# Ruta al archivo feed.py relativa al proyecto
file_path = os.path.join(project_base, "src", "feed.py")

if not os.path.exists(file_path):
    raise FileNotFoundError(f"El archivo no se encontró en la ruta: {file_path}")

# Cargar el módulo dinámicamente
spec = importlib.util.spec_from_file_location("feed", file_path)
feed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(feed)

# Llamar a funciones del módulo
feed.open_feed()
