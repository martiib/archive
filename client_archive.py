# -- ARCHIVE MANAGER -- 

# This project implements a simple Archive Manager.
# The user can insert new clients and visualize all the clients stored in the manager.
# Right before exiting, the program saves the archive into a .txt file.

# ---- Class Definitions ----
# 1. Class that allows the user to enter the data of a new customer
# 1.1 I need to define what a client is ("Client" class)
# A client is identified by: name, surname, tax code, address
class Client:
    def __init__(self, name, surname, tax_code, address):
        self.name = name
        self.surname = surname
        self.tax_code = tax_code
        self.address = address

    def __str__(self):
        return f"Name:{self.name}\nSurname:{self.surname}\nTax Code:{self.tax_code}\nAddress:{self.address}\n\n"

    def __repr__(self):
        return f"Name:{self.name}\nSurname:{self.surname}\nTax Code:{self.tax_code}\nAddress:{self.address}\n\n"


# 2. Entity that creates my customer archive
class Archive:
    def __init__(self, name):
        self.client_list = []

    def add_client(self, name = None, surname = None, tax_code = None, address = None):
        if name == None:
            name = input("Enter the client's name: ")
        if surname == None:
            surname = input("Enter the client's surname: ")
        if tax_code == None:
            tax_code = input("Enter the client's tax_code: ")
        if address == None:
            address = input("Enter the client's address: ")
        self.client_list.append(Client(name, surname, tax_code, address))

    def view_archive(self):
        for i, client in enumerate(self.client_list):
            print(f"Client number {i + 1}:\n{client}")

    def save_archive(self, path_to_file):
        with open(path_to_file, "a") as file:
            for client in self.client_list:
                file.write(str(client))


# ---- Function Definitions ----
def load_archive(archive, path_to_file):
    with open(path_to_file, "r") as file:
        line_number = 0
        for line in file:
            line = line.strip().split(":")[1]

            if line_number == 0:
                name = line
            elif line_number == 1:
                surname = line
            elif line_number == 2:
                tax_code = line
            elif line_number == 3:
                address = line
            
            line_number += 1

            if line_number == 4:
                line_number = 0
                archive.add_client(name, surname, tax_code, address)    
            

def run(archive_path):
    choice = -1
    client_archive = Archive(archive_path)
    load_archive(client_archive, archive_path)
    while choice != 2:
        try:
            choice = int(input("\nWhat do you want to do? \nEnter a new client : button 0" + \
                        "\nView the archive : button 1" + \
                        "\nQuit : button 2\n"))
        except ValueError:
            print("Invalid choice!\nThe only valid choices are:" + \
                  "\nadd client : button 0" + \
                  "\nview the archive : button 1" + \
                  "\nquit : button 2")            
      
        if choice == 0:
            client_archive.add_client()
            print("\nClient added successfully! !\n")
        elif choice == 1:
            print("\nThe archive contains:")
            client_archive.view_archive()
        elif choice != 2:
            print("Invalid choice!\nThe only valid choices are:" + \
                  "\nadd client : button 0" + \
                  "\nview the archive : button 1" + \
                  "\nquit : button 2")

    # 3. At the end of my program, I have to save my customer archive in a text file
    client_archive.save_archive(archive_path)
    print("\nProgram completed successfully!")


# ---- Main Code ----
path_to_archive = "myArchive.txt"
run(path_to_archive)