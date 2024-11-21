# __init__.py

import sys

if sys.version_info < (3, 6):
    raise RuntimeError("Este paquete requiere Python 3.6 o superior")
