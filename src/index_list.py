'''

List: 
Tuplas -> (id,username, passworddescription)

Metodos:
    - Ordenar alfabeticamente
    - Ordenar en alfabeto inverso
    - Aleatorio

'''
<<<<<<< HEAD
=======
class Index_List:
    def _init_(self, users_file, relations_file):
        self.users_file = users_file
        self.relations_file = relations_file
        self.users = []  # List to hold user data
        self.relations = []  # List to hold relations
        self.load_users()
        self.load_relations()

    def load_users(self):
        """Load users from the users CSV file."""
        try:
            with open(self.users_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.users = [
                    {"id": int(row["id"]), "username": row["username"], "description": row["description"]}
                    for row in reader
                ]
        except FileNotFoundError:
            print(f"Error: File {self.users_file} not found.")
        except Exception as e:
            print(f"Error loading users: {e}")

    def load_relations(self):
        """Load relations from the relations CSV file."""
        try:
            with open(self.relations_file, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.relations = [{"user_id": int(row["user_id"]), "friend_id": int(row["friend_id"])} for row in reader]
        except FileNotFoundError:
            print(f"Error: File {self.relations_file} not found.")
        except Exception as e:
            print(f"Error loading relations: {e}")

    def get_all_users(self):
        """Return all user data."""
        return self.users

    def get_sorted_users(self):
        """Return users sorted alphabetically by username."""
        return sorted(self.users, key=lambda user: user["username"])

    def get_random_users(self):
        """Return users in a random order."""
        shuffled_users = self.users[:]
        random.shuffle(shuffled_users)
        return shuffled_users

    def get_user_friends(self, user_id):
        """Return a list of friends for the given user ID."""
        friend_ids = [relation["friend_id"] for relation in self.relations if relation["user_id"] == user_id]
        return [user for user in self.users if user["id"] in friend_ids]

    def filter_users_by_friends(self, user_id):
        """Filter all user data to include only friends of the given user ID."""
        friends = self.get_user_friends(user_id)
        return sorted(friends, key=lambda user: user["username"])  # Alphabetical order of friends
>>>>>>> 6605a440e737ee44261c529814b6b1608e113c66
