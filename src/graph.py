import csv
from collections import defaultdict
import os

class Graph:
    def __init__(self):
        # Initialize an adjacency list to represent the graph
        self.adjacency_list = defaultdict(set)

    def add_edge(self, user_id, friend_id):
        """Add a friendship (edge) between two users."""
        self.adjacency_list[user_id].add(friend_id)
        self.adjacency_list[friend_id].add(user_id)

    def remove_edge(self, user_id, friend_id):
        """Remove a friendship (edge) between two users."""
        if friend_id in self.adjacency_list[user_id]:
            self.adjacency_list[user_id].remove(friend_id)
        if user_id in self.adjacency_list[friend_id]:
            self.adjacency_list[friend_id].remove(user_id)

    def get_friends(self, user_id):
        """Return a list of friends for a given user."""
        return list(self.adjacency_list[user_id])

    def are_friends(self, user_id, friend_id):
        """Check if two users are friends."""
        return friend_id in self.adjacency_list[user_id]

    def load_from_csv(self, file_path):
        """Load relationships from a CSV file."""
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user_id = int(row['user_id'])
                    friend_id = int(row['friend_id'])
                    self.add_edge(user_id, friend_id)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except Exception as e:
            print(f"An error occurred while loading the CSV: {e}")

    def __str__(self):
        """Return a string representation of the graph."""
        result = "Graph adjacency list:\n"
        for user_id, friends in self.adjacency_list.items():
            result += f"{user_id}: {sorted(friends)}\n"
        return result
