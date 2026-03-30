import psycopg2
from config import load_config


def print_contacts(rows):
    if not rows:
        print("No contacts found.")
        return

    for row in rows:
        print(f"id={row[0]}, username={row[1]}, surname={row[2]}, phone={row[3]}")


def search_contacts(pattern):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
                rows = cur.fetchall()
                return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []


def get_contacts_paginated(limit_value, offset_value):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit_value, offset_value))
                rows = cur.fetchall()
                return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []


def upsert_contact(username, surname, phone):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s, %s)", (username, surname, phone))
                conn.commit()
                print("Upsert completed.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def bulk_insert_contacts(usernames, surnames, phones):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL bulk_insert_contacts(%s, %s, %s)",
                    (usernames, surnames, phones)
                )
                conn.commit()
                print("Bulk insert completed.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def delete_contact_by_username(username):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s, %s)", (username, None))
                conn.commit()
                print("Delete by username completed.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def delete_contact_by_phone(phone):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s, %s)", (None, phone))
                conn.commit()
                print("Delete by phone completed.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def manual_bulk_input():
    usernames = []
    surnames = []
    phones = []

    count = int(input("How many contacts do you want to insert? "))

    for i in range(count):
        print(f"\nContact {i + 1}")
        username = input("Enter username: ")
        surname = input("Enter surname: ")
        phone = input("Enter phone: ")

        usernames.append(username)
        surnames.append(surname)
        phones.append(phone)

    bulk_insert_contacts(usernames, surnames, phones)


def menu():
    while True:
        print("\n--- PRACTICE 8 PHONEBOOK MENU ---")
        print("1. Search contacts by pattern")
        print("2. Upsert contact")
        print("3. Bulk insert contacts")
        print("4. Get contacts with pagination")
        print("5. Delete contact by username")
        print("6. Delete contact by phone")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            pattern = input("Enter search pattern: ")
            rows = search_contacts(pattern)
            print_contacts(rows)

        elif choice == '2':
            username = input("Enter username: ")
            surname = input("Enter surname: ")
            phone = input("Enter phone: ")
            upsert_contact(username, surname, phone)

        elif choice == '3':
            manual_bulk_input()

        elif choice == '4':
            limit_value = int(input("Enter LIMIT: "))
            offset_value = int(input("Enter OFFSET: "))
            rows = get_contacts_paginated(limit_value, offset_value)
            print_contacts(rows)

        elif choice == '5':
            username = input("Enter username to delete: ")
            delete_contact_by_username(username)

        elif choice == '6':
            phone = input("Enter phone to delete: ")
            delete_contact_by_phone(phone)

        elif choice == '0':
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    menu()