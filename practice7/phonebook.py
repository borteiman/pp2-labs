import csv
import psycopg2
from config import load_config


def insert_contact(username, phone):
    """ Insert one contact into the phonebook """
    sql = """INSERT INTO phonebook(username, phone)
             VALUES(%s, %s)
             RETURNING id;"""
    contact_id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username, phone))
                row = cur.fetchone()
                if row:
                    contact_id = row[0]
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return contact_id


def insert_many_contacts(contact_list):
    """ Insert multiple contacts into the phonebook """
    sql = """INSERT INTO phonebook(username, phone)
             VALUES(%s, %s)
             ON CONFLICT (phone) DO NOTHING"""
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.executemany(sql, contact_list)
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def import_from_csv(filename):
    """ Import contacts from CSV file """
    contact_list = []

    try:
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contact_list.append((row['username'], row['phone']))
        insert_many_contacts(contact_list)
        print("CSV import completed.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as error:
        print(error)


def get_all_contacts():
    """ Query all contacts """
    sql = "SELECT id, username, phone FROM phonebook ORDER BY id"
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []


def search_by_username(username):
    """ Query contacts by exact username """
    sql = "SELECT id, username, phone FROM phonebook WHERE username ILIKE %s ORDER BY id"
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username,))
                rows = cur.fetchall()
                return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []


def search_by_phone_prefix(prefix):
    """ Query contacts by phone prefix """
    sql = "SELECT id, username, phone FROM phonebook WHERE phone LIKE %s ORDER BY id"
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (prefix + '%',))
                rows = cur.fetchall()
                return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []


def update_username_by_phone(phone, new_username):
    """ Update username by phone """
    updated_row_count = 0
    sql = """UPDATE phonebook
             SET username = %s
             WHERE phone = %s"""
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_username, phone))
                updated_row_count = cur.rowcount
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return updated_row_count


def update_phone_by_username(username, new_phone):
    """ Update phone by username """
    updated_row_count = 0
    sql = """UPDATE phonebook
             SET phone = %s
             WHERE username = %s"""
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (new_phone, username))
                updated_row_count = cur.rowcount
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return updated_row_count


def delete_by_username(username):
    """ Delete contact by username """
    rows_deleted = 0
    sql = "DELETE FROM phonebook WHERE username = %s"
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username,))
                rows_deleted = cur.rowcount
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return rows_deleted


def delete_by_phone(phone):
    """ Delete contact by phone """
    rows_deleted = 0
    sql = "DELETE FROM phonebook WHERE phone = %s"
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (phone,))
                rows_deleted = cur.rowcount
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return rows_deleted


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print(f"id={row[0]}, username={row[1]}, phone={row[2]}")


def menu():
    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Import contacts from CSV")
        print("2. Insert contact from console")
        print("3. Show all contacts")
        print("4. Search by username")
        print("5. Search by phone prefix")
        print("6. Update username by phone")
        print("7. Update phone by username")
        print("8. Delete by username")
        print("9. Delete by phone")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            filename = input("Enter CSV filename: ")
            import_from_csv(filename)

        elif choice == '2':
            username = input("Enter username: ")
            phone = input("Enter phone: ")
            contact_id = insert_contact(username, phone)
            print("Inserted contact id:", contact_id)

        elif choice == '3':
            rows = get_all_contacts()
            print_contacts(rows)

        elif choice == '4':
            username = input("Enter username: ")
            rows = search_by_username(username)
            print_contacts(rows)

        elif choice == '5':
            prefix = input("Enter phone prefix: ")
            rows = search_by_phone_prefix(prefix)
            print_contacts(rows)

        elif choice == '6':
            phone = input("Enter current phone: ")
            new_username = input("Enter new username: ")
            updated = update_username_by_phone(phone, new_username)
            print("Updated rows:", updated)

        elif choice == '7':
            username = input("Enter current username: ")
            new_phone = input("Enter new phone: ")
            updated = update_phone_by_username(username, new_phone)
            print("Updated rows:", updated)

        elif choice == '8':
            username = input("Enter username to delete: ")
            deleted = delete_by_username(username)
            print("Deleted rows:", deleted)

        elif choice == '9':
            phone = input("Enter phone to delete: ")
            deleted = delete_by_phone(phone)
            print("Deleted rows:", deleted)

        elif choice == '0':
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    menu()