'''

List: 
Tuplas -> (id,username, passworddescription)

Metodos:
    - Ordenar alfabeticamente
    - Ordenar en alfabeto inverso
    - Aleatorio

'''
import csv
import random

def read_csv(file_path):
    """Reads user data from a CSV file and returns a list of tuples."""
    users = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            users.append((int(row[0]), row[1], row[2]))  
    return users

def sort_alphabetically(data):
    """Sorts the list of tuples alphabetically by username."""
    return sorted(data, key=lambda x: x[1])

def sort_reverse_alphabetically(data):
    """Sorts the list of tuples in reverse alphabetical order by username."""
    return sorted(data, key=lambda x: x[1], reverse=True)

def shuffle_randomly(data):
    """Shuffles the list of tuples randomly."""
    data_copy = data[:] 
    random.shuffle(data_copy)
    return data_copy

def write_csv(file_path, data):
    """Writes the modified data back to a CSV file."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'username', 'password']) 
        writer.writerows(data)

if __name__ == "__main__":
    input_file = "assets/data/users.csv"  
    output_file = "assets/data/sorted_users.csv"  

    users = read_csv(input_file)
    print("Original data:", users)

    sorted_users = sort_alphabetically(users)
    print("Alphabetically sorted:", sorted_users)

    reverse_sorted_users = sort_reverse_alphabetically(users)
    print("Reverse alphabetically sorted:", reverse_sorted_users)

    shuffled_users = shuffle_randomly(users)
    print("Shuffled data:", shuffled_users)

    write_csv(output_file, sorted_users)
    print(f"Sorted data written to {output_file}")
