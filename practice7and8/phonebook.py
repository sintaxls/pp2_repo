import psycopg2
from pathlib import Path
from config import DB_HOST, DB_USER, DB_NAME, DB_PASSWORD
from connect import connect
csv_path = Path(__file__).resolve().parent / "contacts.csv"

def create_phonebook_table():
    try:
        conn = connect()
        cursor = conn.cursor()
        
        create_table = """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(20) NOT NULL UNIQUE
        );
        """
        
        cursor.execute(create_table)
        
        with open(csv_path, 'r') as f:
            next(f)
            cursor.copy_from(
                f,
                'phonebook',
                columns=('first_name', 'last_name', 'phone_number'),
                sep=',')
        cursor.execute(create_table)
        conn.commit()
        print("Phonebook created")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)

def print_tb():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM phonebook")
    rows = cursor.fetchall()
    cursor.description

    header = [desc[0] for desc in cursor.description]
    print(f"{header[0]:<5} {header[1]:<15} {header[2]:<15} {header[3]:<20}")
    print("-" * 60)

    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<20}")

    cursor.close()
    conn.close()


def update_contact():
    print("What update? enter 1 - first name \nenter 2 - last name \nenter 3 - phone number \n")
    what = int(input())
    phone_id = int(input("ID: "))

    if what == 1:
        new_first_name = input("New first name: ")
        
        conn = connect()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE phonebook SET first_name = %s WHERE id = %s", (new_first_name, phone_id))
        conn.commit()
        print("Updated successfully")
        
        cursor.close()
        conn.close()

    elif what == 2:
        new_last_name = input("New last name: ")
        
        conn = connect()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE phonebook SET last_name = %s WHERE id = %s", (new_last_name, phone_id))
        conn.commit()
        print("Updated successfully")
        
        cursor.close()
        conn.close()

    elif what == 3:
        new_number = input("New phone number: ")
        
        conn = connect()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE phonebook SET phone_number = %s WHERE id = %s", (new_number, phone_id))
        conn.commit()
        print("Updated successfully")
        
        cursor.close()
        conn.close()
    else:
        print("Invalid option")
        cursor.close()
        conn.close()
        return

def search_querry():
    what = input("Search what: 1 - first name, 2 - last name, 3 - phone prefix\n")
    search_term = input("Enter search term: ")

    conn = connect()
    cursor = conn.cursor()

    if what == "1":
        cursor.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{search_term}%",))
    elif what == "2":
        cursor.execute("SELECT * FROM phonebook WHERE last_name ILIKE %s", (f"%{search_term}%",))
    elif what == "3":
        cursor.execute("SELECT * FROM phonebook WHERE phone_number LIKE %s", (f"{search_term}%",))
    else:
        print("Invalid option")
        cursor.close()
        conn.close()
        return

    rows = cursor.fetchall()
    if rows:
        header = [desc[0] for desc in cursor.description]
        print(f"{header[0]:<5} {header[1]:<15} {header[2]:<15} {header[3]:<20}")
        print("-" * 60)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<20}")
    else:
        print("No results found")

    cursor.close()
    conn.close()

def delete_contact():
    phone_id = int(input("ID: "))

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM phonebook WHERE id = %s", (phone_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Contact deleted successfully")
    else:
        print("Contact not found")

    cursor.close()
    conn.close()

def add_contact():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone_number = input("Phone number: ")
    
    try:
        conn = connect()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
            (first_name, last_name, phone_number)
        )
        conn.commit()
        print("Added successfully")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

def find_using_function():
    search_item = input("Search item:")
    
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM public.search_records(%s)", (search_item,))

    rows = cursor.fetchall()
    if rows:
        header = [desc[0] for desc in cursor.description]
        print(f"{header[0]:<5} {header[1]:<15} {header[2]:<15} {header[3]:<20}")
        print("-" * 60)
        for row in rows:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<20}")
    else:
        print("No results found")


def insert_using_function():
    first_n = input("first name: ")
    last_n = input("last name: ")
    phone = input("phone: ")
    
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("CALL public.insert_user(%s, %s, %s)", 
                       (first_n, last_n, phone))
        conn.commit()
        print("Success")
    except Exception as e:
        print(f"err: {e}")
    finally:
        cursor.close()
        conn.close()




#######################################################################



if __name__ == "__main__":
    create_phonebook_table()
    print_tb()
    print()

    while True:
        whatchoose = int(input("1 - update contact, 2 - search querry\n3 - add contact, 4 - delete contact\n\n5 - find using functions\n6 - insert using procedure\n"))
        if whatchoose == 1:
            update_contact()
            print()
            print()
        elif whatchoose == 2:
            search_querry()
            print()
            print()
            input("Press any button ")
        elif whatchoose == 3:
            add_contact()
            print()
            print()
        elif whatchoose == 4:
            delete_contact()
            print()
            print()
        elif whatchoose == 5:
            find_using_function()
            print()
            print()
            input("Press any button ")
        elif whatchoose == 6:
            insert_using_function()
            print()
            print()
        print_tb()

