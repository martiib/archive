import sqlite3
import pandas as pd

class Client:
    """
    Represents a client with personal and contact information.

    Attributes:
        name (str): The first name of the client.
        surname (str): The last name of the client.
        tax_code (str): The tax code of the client.
        address (str): The address of the client.
    """
    def __init__(self, name: str, surname: str, tax_code: str, address: str):
        """
        Initializes a new Client object.

        Args:
            name (str): The first name of the client.
            surname (str): The last name of the client.
            tax_code (str): The tax code of the client.
            address (str): The address of the client.
        """
        self.name = name
        self.surname = surname
        self.tax_code = tax_code
        self.address = address


class Archive:
    """
    Manages a database of clients, providing functionalities to add, view, update, and delete client records.

    Attributes:
        db_path (str): The path to the SQLite database file.
        conn (sqlite3.Connection): The database connection object.
        cursor (sqlite3.Cursor): The database cursor object.
    """
    def __init__(self, db_path: str = "customers.db"):
        """
        Initializes the Archive, connects to the SQLite database, and ensures the clients table exists.

        Args:
            db_path (str, optional): The path to the SQLite database file. Defaults to "customers.db".
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Creates the 'clients' table in the database if it does not already exist.
        The table includes columns for id, name, surname, tax_code, and address.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                tax_code TEXT,
                address TEXT
            )
        ''')
        self.conn.commit()

    # Create
    def add_client(self, name: str | None = None, surname: str | None = None, 
                   tax_code: str | None = None, address: str | None = None):
        """
        Adds a new client record to the database.

        If any argument is not provided, the user will be prompted to enter the information.

        Args:
            name (str, optional): The first name of the client. Defaults to None.
            surname (str, optional): The last name of the client. Defaults to None.
            tax_code (str, optional): The tax code of the client. Defaults to None.
            address (str, optional): The address of the client. Defaults to None.
        """
        if name is None:
            name = input("Name: ")
        if surname is None:
            surname = input("Surname: ")
        if tax_code is None:
            tax_code = input("Tax code: ")
        if address is None:
            address = input("Address: ")
        self.cursor.execute(
            "INSERT INTO clients (name, surname, tax_code, address) VALUES (?, ?, ?, ?)",
            (name, surname, tax_code, address)
        )
        self.conn.commit()
        print("Client added!")

    # Read
    def view_archive(self):
        """
        Retrieves and displays all client records from the database.

        If the archive is empty, a corresponding message is printed. Otherwise, a pandas DataFrame
        is used to display the clients in a formatted string, along with the total count.

        Returns:
            pd.DataFrame: A DataFrame containing all client records.
        """
        df = pd.read_sql("SELECT * FROM clients", self.conn)
        if df.empty:
            print("Archive is empty.")
        else:
            print(df.to_string(index = False))
            print(f"\nTotal clients: {len(df)}")
        return df

    # Update
    def update_client(self, client_id: int):
        """
        Updates an existing client record identified by `client_id`.

        The user will be prompted to enter new values for name, surname, tax code, and address.
        If an input is left blank, the current value for that field will be retained.

        Args:
            client_id (int): The ID of the client to update.
        """
        df = self.view_archive()
        if client_id not in df['id'].values:
            print("Client not found.")
            return
        name = input("New name (leave blank to keep current): ")
        surname = input("New surname: ")
        tax_code = input("New tax code: ")
        address = input("New address: ")
        self.cursor.execute(
            "UPDATE clients SET name=?, surname=?, tax_code=?, address=? WHERE id=?",
            (name or df.loc[df.id == client_id, 'name'].values[0],
             surname or df.loc[df.id == client_id, 'surname'].values[0],
             tax_code or df.loc[df.id == client_id, 'tax_code'].values[0],
             address or df.loc[df.id == client_id, 'address'].values[0],
             client_id)
        )
        self.conn.commit()
        print("Client updated!")

    # Delete
    def delete_client(self, client_id: int):
        """
        Deletes a client record from the database.

        Args:
            client_id (int): The ID of the client to delete.
        """
        self.cursor.execute("DELETE FROM clients WHERE id=?", (client_id,))
        self.conn.commit()
        print("Client deleted!")

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()


def run():
    """
    Runs the main interactive menu for managing the client archive.

    This function allows users to add, view, update, and delete client records
    through a command-line interface until the user chooses to quit.
    """
    archive = Archive()
    choice = -1
    while choice != 5:
        print("\n--- Menu ---")
        print("1: Add client")
        print("2: View archive")
        print("3: Update client")
        print("4: Delete client")
        print("5: Quit")
        try:
            choice = int(input("Choice: "))
        except ValueError:
            continue

        if choice == 1:
            archive.add_client()
        elif choice == 2:
            archive.view_archive()
        elif choice == 3:
            try:
                cid = int(input("Enter client ID to update: "))
                archive.update_client(cid)
            except ValueError:
                print("Invalid ID")
        elif choice == 4:
            try:
                cid = int(input("Enter client ID to delete: "))
                archive.delete_client(cid)
            except ValueError:
                print("Invalid ID")
        elif choice == 5:
            print("\nClient Archive closed. Goodbye!")
        else:
            print("Invalid choice")
    archive.close()

if __name__ == "__main__":
    run()