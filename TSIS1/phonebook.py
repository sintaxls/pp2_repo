import psycopg2
from pathlib import Path
from config import DB_HOST, DB_USER, DB_NAME, DB_PASSWORD
from connect import connect
import json
import csv
csv_path = Path(__file__).resolve().parent / "contacts.csv"
json_path = Path(__file__).resolve().parent / "contacts.json"

def create_phonebook_table():
    try:
        conn = connect()
        cursor = conn.cursor()
        
        create_table = """
        CREATE TABLE IF NOT EXISTS groups (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );

        INSERT INTO groups (name)
        VALUES ('Family'), ('Work'), ('Friend'), ('Other')
        ON CONFLICT (name) DO NOTHING;

        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            phone_number VARCHAR(20) UNIQUE,
            email VARCHAR(100),
            birthday DATE,
            group_id INTEGER REFERENCES groups(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS phones (
            id SERIAL PRIMARY KEY,
            contact_id INTEGER REFERENCES phonebook(id) ON DELETE CASCADE,
            phone VARCHAR(20) NOT NULL,
            type VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
        );
        """
        
        cursor.execute(create_table)
        
        # with open(csv_path, 'r') as f:
        #     next(f)
        #     cursor.copy_from(
        #         f,
        #         'phonebook',
        #         columns=('first_name', 'last_name', 'phone_number'),
        #         sep=',')
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

    cursor.execute("""
        SELECT
            p.id,
            p.first_name,
            p.last_name,
            p.email,
            p.birthday,
            g.name AS group_name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        ORDER BY p.id
    """)
    rows = cursor.fetchall()
    cursor.description

    header = [desc[0] for desc in cursor.description]
    print(f"{'ID':<5} {'First':<15} {'Last':<15} {'Email':<25} {'Birthday':<12} {'Group':<10}")
    print("-" * 90)

    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {str(row[3]):<25} {str(row[4]):<12} {str(row[5]):<10}")

    cursor.close()
    conn.close()

def print_contacts(rows): # helper
    if rows:
        print(f"{'ID':<5} {'First':<15} {'Last':<15} {'Phone':<20} {'Email':<25} {'Birthday':<12} {'Group':<10}")
        print("-" * 105)

        for row in rows:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {str(row[3]):<20} {str(row[4]):<25} {str(row[5]):<12} {str(row[6]):<10}")
    else:
        print("No results found")


def show_contact_phones():
    contact_id = int(input("id: "))

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT phone, type
        FROM phones
        WHERE contact_id = %s
        ORDER BY id
        """,
        (contact_id,)
    )

    rows = cursor.fetchall()

    if rows:
        print(f"{'Phone':<20} {'Type':<10}")
        print("-" * 30)
        for row in rows:
            print(f"{row[0]:<20} {row[1]:<10}")
    else:
        print("No phones")

    cursor.close()
    conn.close()


def add_additional_phone_by_id():
    contact_id = int(input("Contact id: "))
    phone = input("Additional phone number: ")
    phone_type = get_phone_type(input("Phone type (home/work/mobile): "))

    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM phonebook WHERE id = %s", (contact_id,))
        if cursor.fetchone() is None:
            print("Contact not found")
            return

        cursor.execute(
            """
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
            """,
            (contact_id, phone, phone_type)
        )
        conn.commit()
        print("Additional phone added successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
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

def search_by_email():
    email = input("Search email: ")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.first_name,
            p.last_name,
            p.phone_number,
            p.email,
            p.birthday,
            g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        WHERE p.email ILIKE %s
        ORDER BY p.id
    """, (f"%{email}%",))

    rows = cursor.fetchall()
    print_contacts(rows)

    cursor.close()
    conn.close()


def filter_by_group():
    group_name = input("Group name (Family, Work, Friend, Other): ")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.first_name,
            p.last_name,
            p.phone_number,
            p.email,
            p.birthday,
            g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        WHERE g.name ILIKE %s
        ORDER BY p.id
    """, (group_name,))

    rows = cursor.fetchall()
    print_contacts(rows)

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


def get_group_id(cursor, group_name):
    if group_name == "" or group_name is None:
        group_name = "Other"

    cursor.execute(
        """
        INSERT INTO groups (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        """,
        (group_name,)
    )

    cursor.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
    return cursor.fetchone()[0]


def get_phone_type(phone_type):
    if phone_type in ("home", "work", "mobile"):
        return phone_type
    return "mobile"


def insert_imported_contact(cursor, contact, overwrite):
    first_name = contact.get("first_name", "")
    last_name = contact.get("last_name", "")
    phone_number = contact.get("phone_number", "")
    email = contact.get("email", "")
    birthday = contact.get("birthday", "")
    group_name = contact.get("group", "Other")
    phones = contact.get("phones", [])

    if not phones and phone_number:
        phones = [{"phone": phone_number, "type": contact.get("phone_type", "mobile")}]

    group_id = get_group_id(cursor, group_name)

    cursor.execute(
        """
        SELECT id
        FROM phonebook
        WHERE first_name = %s AND last_name = %s
        """,
        (first_name, last_name)
    )
    existing = cursor.fetchone()

    if existing and not overwrite:
        return "skipped"

    if existing and overwrite:
        contact_id = existing[0]
        cursor.execute(
            """
            UPDATE phonebook
            SET phone_number = %s,
                email = %s,
                birthday = %s,
                group_id = %s
            WHERE id = %s
            """,
            (phone_number, email, birthday or None, group_id, contact_id)
        )
        cursor.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
    else:
        cursor.execute(
            """
            INSERT INTO phonebook (first_name, last_name, phone_number, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (first_name, last_name, phone_number, email, birthday or None, group_id)
        )
        contact_id = cursor.fetchone()[0]

    for phone in phones:
        cursor.execute(
            """
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
            """,
            (contact_id, phone.get("phone", ""), get_phone_type(phone.get("type", "mobile")))
        )

    if existing:
        return "overwritten"
    return "inserted"


def add_contact():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone_number = input("Phone number: ")
    email = input("Email: ")
    birthday = input("Birthday YYYY-MM-DD: ")
    group_id = int(input("Group id: 1-Family, 2-Work, 3-Friend, 4-Other: "))
    phone_type = input("Phone type (home/work/mobile): ")

    try:
        conn = connect()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO phonebook (first_name, last_name, phone_number, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (first_name, last_name, phone_number, email, birthday, group_id)
        )
        # we return id because it is used also for phones table

        contact_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO phones (contact_id, phone, type)
            VALUES (%s, %s, %s)
            """,
            (contact_id, phone_number, phone_type)
        )

        conn.commit()
        print("Added successfully")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


def sort_contacts():
    print("Sort by: 1 - name, 2 - birthday, 3 - date added")
    what = input()

    if what == "1":
        order_by = "p.first_name, p.last_name"
    elif what == "2":
        order_by = "p.birthday"
    elif what == "3":
        order_by = "p.created_at"
    else:
        print("Invalid option")
        return

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            p.id,
            p.first_name,
            p.last_name,
            p.phone_number,
            p.email,
            p.birthday,
            g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        ORDER BY {order_by}
    """)

    rows = cursor.fetchall()
    print_contacts(rows)

    cursor.close()
    conn.close()


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


def insert_many_users_using_procedures():
    n = int(input("How many: "))
    arr = []
    for i in range(n):
        arr.append({"first_name":input('first_name: '), 
                  "last_name":input('last_name: '),
                  "phone_number":input('phone_number: '),})
        print()
    print(arr)
    
    # print(f'''SELECT public.insert_many_users_fn(
    #     '{str(arr)}'::jsonb
    # );''')
    try:
        conn = connect()
        cursor = conn.cursor()

        payload = json.dumps(arr)

        cursor.execute("CALL public.insert_many_users(%s::jsonb, %s::jsonb);",
            (payload, "[]"))
        conn.commit()

        invalid_rows = cursor.fetchone()[0]
        
        print("Invalid rows:", invalid_rows)
    except Exception as e:
        conn.rollback()
        print(f"error: {e}")
    finally:
        cursor.close()
        conn.close()


def show_paginated_contacts():
    lim = int(input("Limit: "))
    offst = int(input("Offset: "))

    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM public.phonebook_paginate(%s, %s)",
            (lim, offst)
        )
        rows = cursor.fetchall()

        if rows:
            header = [desc[0] for desc in cursor.description]
            print(f"{header[0]:<5} {header[1]:<15} {header[2]:<15} {header[3]:<20}")
            print("-" * 60)
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<20}")
            input("Press any button ")
        else:
            print("No rows found")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def paginate_with_navigation():
    lim = int(input("Limit: "))
    offst = 0

    while True:
        try:
            conn = connect()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM public.phonebook_paginate(%s, %s)",
                (lim, offst)
            )

            rows = cursor.fetchall()

            if rows:
                header = [desc[0] for desc in cursor.description]
                print(f"{header[0]:<5} {header[1]:<15} {header[2]:<15} {header[3]:<20}")
                print("-" * 60)

                for row in rows:
                    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<20}")
            else:
                print("No rows found")

            command = input("next / prev / quit: ")

            if command == "next":
                offst += lim
            elif command == "prev":
                offst -= lim
                if offst < 0:
                    offst = 0
            elif command == "quit":
                break
            else:
                print("Invalid command")

        except Exception as e:
            print(f"Error: {e}")
            break
        finally:
            cursor.close()
            conn.close()


def delete_by_id_or_phone():

    what = input("1 - id, 2 - phone\n")

    try:
        conn = connect()
        cursor = conn.cursor()

        if what == "1":
            phone_id = int(input("ID: "))
            cursor.execute(
                "CALL public.delete_by_id_or_phone(%s, %s)",
                (phone_id, None)
            )
        elif what == "2":
            phone = input("phone: ")
            cursor.execute(
                "CALL public.delete_by_id_or_phone(%s, %s)",
                (None, phone)
            )
        else:
            print("Invalid option")
            return

        conn.commit()
        print("Deleted successfully")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# JSON
def export_to_json():
    file_name = input("JSON name: ")
    if file_name == "":
        file_name = json_path

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.first_name,
            p.last_name,
            p.phone_number,
            p.email,
            p.birthday,
            g.name
        FROM phonebook p
        LEFT JOIN groups g ON p.group_id = g.id
        ORDER BY p.id
    """)
    rows = cursor.fetchall()

    contacts = []
    for row in rows:
        cursor.execute(
            """
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s
            ORDER BY id
            """,
            (row[0],)
        )
        phones = []
        for phone in cursor.fetchall():
            phones.append({"phone": phone[0], "type": phone[1]})

        contacts.append({
            "first_name": row[1],
            "last_name": row[2],
            "phone_number": row[3],
            "email": row[4],
            "birthday": str(row[5]) if row[5] else "",
            "group": row[6],
            "phones": phones
        })

    with open(file_name, "w") as f:
        json.dump(contacts, f, indent=4)

    print("export success")

    cursor.close()
    conn.close()


def import_from_json():
    file_name = input("JSON name: ")
    if file_name == "":
        file_name = json_path

    with open(file_name, "r") as f:
        contacts = json.load(f)

    if isinstance(contacts, dict):
        contacts = contacts.get("contacts", [])

    inserted = 0
    skipped = 0
    overwritten = 0

    conn = connect()
    cursor = conn.cursor()

    try:
        for contact in contacts:
            cursor.execute(
                """
                SELECT id
                FROM phonebook
                WHERE first_name = %s AND last_name = %s
                """,
                (contact.get("first_name", ""), contact.get("last_name", ""))
            )
            existing = cursor.fetchone()
            overwrite = False

            if existing:
                answer = input(f"{contact.get('first_name')} {contact.get('last_name')} exists. skip or overwrite: ")
                if answer == "overwrite":
                    overwrite = True
                else:
                    skipped += 1
                    continue

            result = insert_imported_contact(cursor, contact, overwrite)
            if result == "inserted":
                inserted += 1
            elif result == "overwritten":
                overwritten += 1
            else:
                skipped += 1

        conn.commit()
        print(f"inserted: {inserted}, overwritten: {overwritten}, skipped: {skipped}")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def import_from_csv():
    file_name = input("CSV file name: ")
    if file_name == "":
        file_name = csv_path

    inserted = 0
    skipped = 0

    conn = connect()
    cursor = conn.cursor()

    try:
        with open(file_name, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                contact = {
                    "first_name": row.get("first_name") or row.get("name") or "",
                    "last_name": row.get("last_name") or row.get("surname") or "",
                    "phone_number": row.get("phone_number") or row.get("phone") or "",
                    "email": row.get("email") or "",
                    "birthday": row.get("birthday") or "",
                    "group": row.get("group") or "Other",
                    "phone_type": row.get("phone_type") or row.get("type") or "mobile"
                }

                result = insert_imported_contact(cursor, contact, False)
                if result == "inserted":
                    inserted += 1
                else:
                    skipped += 1

        conn.commit()
        print(f"inserted: {inserted}, skipped: {skipped}")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
#######################################################################



if __name__ == "__main__":
    create_phonebook_table()
    print_tb()
    print()

    while True:
        whatchoose = int(input("1 - update contact, 2 - search querry\n3 - add contact, 4 - delete contact\n\n5 - find using functions\n6 - insert using procedure\n7 - insert many users using procedures\n8 - paginate\n9 - delete by id or phone using procedure\n10 - show contact phones\n11 - filter by group\n12 - search by email\n13 - sort contacts\n14 - paginate navigation\n15 - export to json\n16 - import from json\n17 - import from csv\n18 - add additional phone by id\n\n"))
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
        elif whatchoose == 7:
            insert_many_users_using_procedures()
            print()
            print()
        elif whatchoose == 8:
            show_paginated_contacts()
            print()
            print()
        elif whatchoose == 9:
            delete_by_id_or_phone()
            print()
            print()
        elif whatchoose == 10:
            show_contact_phones()
            print()
            print()
        elif whatchoose == 11:
            filter_by_group()
            print()
            print()
            input("Press any button ")
        elif whatchoose == 12:
            search_by_email()
            print()
            print()
            input("Press any button ")
        elif whatchoose == 13:
            sort_contacts()
            print()
            print()
            input("Press any button ")
        elif whatchoose == 14:
            paginate_with_navigation()
            print()
            print()
        elif whatchoose == 15:
            export_to_json()
            print()
            print()
        elif whatchoose == 16:
            import_from_json()
            print()
            print()
        elif whatchoose == 17:
            import_from_csv()
            print()
            print()
        elif whatchoose == 18:
            add_additional_phone_by_id()
            print()
            print()
        print_tb()
