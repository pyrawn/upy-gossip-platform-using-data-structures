class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_user(self, user_id, username):
        if user_id not in self.adjacency_list:
            self.adjacency_list[user_id] = {"username": username, "friends": []}
        else:
            print(f"User {user_id} already exists.")

    def add_friendship(self, user_id1, user_id2):
        if user_id1 in self.adjacency_list and user_id2 in self.adjacency_list:
            if user_id2 not in self.adjacency_list[user_id1]["friends"]:
                self.adjacency_list[user_id1]["friends"].append(user_id2)
                self.adjacency_list[user_id2]["friends"].append(user_id1)
            else:
                print(f"Users {user_id1} and {user_id2} are already friends.")
        else:
            print("One or both users do not exist.")

    def list_friends(self, user_id):
        if user_id in self.adjacency_list:
            friends_ids = self.adjacency_list[user_id]["friends"]
            friends = [
                self.adjacency_list[friend_id]["username"] for friend_id in friends_ids
            ]
            return friends
        else:
            print(f"User {user_id} does not exist.")
            return []

    def are_friends(self, user_id1, user_id2):
        if user_id1 in self.adjacency_list and user_id2 in self.adjacency_list:
            return user_id2 in self.adjacency_list[user_id1]["friends"]
        return False

    def display_graph(self):
        for user_id, details in self.adjacency_list.items():
            print(
                f"User {user_id} ({details['username']}): Friends -> {details['friends']}"
            )


# Crear un grafo
social_graph = Graph()

# Agregar usuarios
social_graph.add_user(1, "user1")
social_graph.add_user(2, "user2")
social_graph.add_user(3, "user3")
social_graph.add_user(4, "pyrawn")
social_graph.add_user(5, "this")

# Crear relaciones
social_graph.add_friendship(1, 2)
social_graph.add_friendship(1, 3)
social_graph.add_friendship(4, 5)

# Mostrar el grafo
social_graph.display_graph()

# Listar amigos de un usuario
print("Amigos de user1:", social_graph.list_friends(1))

# Verificar si dos usuarios son amigos
print("¿user1 y user2 son amigos?", social_graph.are_friends(1, 2))
