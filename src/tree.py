class TreeNode:
    def __init__(self, id, data, parent_id=None):
        self.id = id  # ID del nodo
        self.data = data  # Contenido del nodo
        self.parent_id = parent_id  # ID del nodo padre (None para posts principales)
        self.children = []  # Lista de respuestas o hijos

    def add_child(self, child_node):
        self.children.append(child_node)

class CommentTree:
    def __init__(self):
        self.nodes = {}  # Diccionario para almacenar nodos por ID

    def add_node(self, id, data, parent_id=None):
        new_node = TreeNode(id, data, parent_id)
        self.nodes[id] = new_node
        if parent_id is not None and parent_id in self.nodes:
            self.nodes[parent_id].add_child(new_node)

    def get_root_nodes(self):
        """Obtiene los nodos raíz (posts principales)."""
        return [node for node in self.nodes.values() if node.parent_id is None]
