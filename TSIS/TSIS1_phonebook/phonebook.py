import csv
import json
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor

from connect import get_connection


VALID_PHONE_TYPES = ["home", "work", "mobile"]


def run_sql_file(filename):
    # I run schema.sql and procedures.sql from Python, so setup is easier.
    path = Path(filename)

    if not path.exists():
        print(f"{filename} not found")
        return

    conn = get_connection()

    try:
        cur = conn.cursor()
        sql = path.read_text(encoding="utf-8")
        cur.execute(sql)
        conn.commit()
        cur.close()
        print(f"{filename} executed successfully")

    except Exception as error:
        conn.rollback()
        print(f"Error while running {filename}:", error)

    finally:
        conn.close()


def setup_database():
    # Run this once from menu or at the first start.
    # It creates tables and stored procedures/functions.
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")


def get_group_id(cur, group_name):
    # Creates group if it does not exist and returns its id.
    if group_name.strip() == "":
        group_name = "Other"

    cur.execute(
        """
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
        """,
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
    return cur.fetchone()[0]


def get_contact_id(cur, name):
    cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
    row = cur.fetchone()

    if row:
        return row[0]

    return None


def normalize_phone_type(phone_type):
    phone_type = phone_type.strip().lower()

    if phone_type not in VALID_PHONE_TYPES:
        phone_type = "mobile"

    return phone_type


def print_rows(rows):
    if not rows:
        print("No contacts found.")
        return

    print("-" * 110)
    print(f"{'ID':<4} {'Name':<18} {'Email':<25} {'Birthday':<12} {'Group':<12} Phones")
    print("-" * 110)

    for row in rows:
        print(
            f"{row['contact_id']:<4} "
            f"{row['contact_name']:<18} "
            f"{str(row['email'] or ''):<25} "
            f"{str(row['birthday'] or ''):<12} "
            f"{row['group_name']:<12} "
            f"{row['phones'] or ''}"
        )

    print("-" * 110)


def fetch_all_contacts(sort_by="name"):
    # Sort by safe predefined columns only, not direct user SQL.
    order_map = {
        "name": "c.name",
        "birthday": "c.birthday NULLS LAST",
        "date": "c.created_at",
    }

    order_by = order_map.get(sort_by, "c.name")

    conn = get_connection()

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            f"""
            SELECT
                c.id AS contact_id,
                c.name AS contact_name,
                c.email,
                c.birthday,
                COALESCE(g.name, 'Other') AS group_name,
                COALESCE(
                    STRING_AGG(ph.type || ': ' || ph.phone, ', ' ORDER BY ph.id),
                    ''
                ) AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones ph ON ph.contact_id = c.id
            GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
            ORDER BY {order_by};
            """
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    finally:
        conn.close()


def show_all_contacts():
    rows = fetch_all_contacts("name")
    print_rows(rows)


def add_contact_console():
    print("\nAdd new contact")
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    birthday = input("Birthday YYYY-MM-DD, empty if none: ").strip()
    group_name = input("Group Family/Work/Friend/Other: ").strip() or "Other"
    phone = input("Phone: ").strip()
    phone_type = normalize_phone_type(input("Phone type home/work/mobile: "))

    if not name:
        print("Name cannot be empty.")
        return

    birthday_value = birthday if birthday else None
    email_value = email if email else None

    conn = get_connection()

    try:
        cur = conn.cursor()
        group_id = get_group_id(cur, group_name)

        cur.execute(
            """
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """,
            (name, email_value, birthday_value, group_id)
        )

        contact_id = cur.fetchone()[0]

        if phone:
            cur.execute(
                """
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s);
                """,
                (contact_id, phone, phone_type)
            )

        conn.commit()
        cur.close()
        print("Contact added.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


def add_phone_console():
    print("\nAdd phone to existing contact")
    name = input("Contact name: ").strip()
    phone = input("New phone: ").strip()
    phone_type = normalize_phone_type(input("Type home/work/mobile: "))

    conn = get_connection()

    try:
        cur = conn.cursor()
        cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, phone_type))
        conn.commit()
        cur.close()
        print("Phone added.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


def move_to_group_console():
    print("\nMove contact to group")
    name = input("Contact name: ").strip()
    group_name = input("New group name: ").strip()

    conn = get_connection()

    try:
        cur = conn.cursor()
        cur.execute("CALL move_to_group(%s, %s);", (name, group_name))
        conn.commit()
        cur.close()
        print("Contact moved.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


def search_contacts_console():
    query = input("\nSearch query: ").strip()

    conn = get_connection()

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM search_contacts(%s);", (query,))
        rows = cur.fetchall()
        cur.close()
        print_rows(rows)

    finally:
        conn.close()


def search_by_email_console():
    query = input("\nEmail contains: ").strip()

    conn = get_connection()

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            SELECT *
            FROM search_contacts(%s)
            WHERE email ILIKE %s;
            """,
            (query, f"%{query}%")
        )
        rows = cur.fetchall()
        cur.close()
        print_rows(rows)

    finally:
        conn.close()


def filter_by_group_console():
    group_name = input("\nGroup name: ").strip()

    conn = get_connection()

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            SELECT
                c.id AS contact_id,
                c.name AS contact_name,
                c.email,
                c.birthday,
                COALESCE(g.name, 'Other') AS group_name,
                COALESCE(
                    STRING_AGG(ph.type || ': ' || ph.phone, ', ' ORDER BY ph.id),
                    ''
                ) AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones ph ON ph.contact_id = c.id
            WHERE g.name ILIKE %s
            GROUP BY c.id, c.name, c.email, c.birthday, g.name
            ORDER BY c.name;
            """,
            (group_name,)
        )
        rows = cur.fetchall()
        cur.close()
        print_rows(rows)

    finally:
        conn.close()


def sort_contacts_console():
    print("\nSort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ").strip()

    if choice == "2":
        sort_by = "birthday"

    elif choice == "3":
        sort_by = "date"

    else:
        sort_by = "name"

    rows = fetch_all_contacts(sort_by)
    print_rows(rows)


def paginated_navigation():
    print("\nPaginated contacts")
    page_size_text = input("Page size, default 5: ").strip()
    page_size = int(page_size_text) if page_size_text.isdigit() else 5

    print("Sort by: name / birthday / created_at")
    sort_by = input("Sort: ").strip()

    if sort_by not in ["name", "birthday", "created_at"]:
        sort_by = "name"

    page = 0

    while True:
        offset = page * page_size

        conn = get_connection()

        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(
                "SELECT * FROM get_contacts_page(%s, %s, %s);",
                (page_size, offset, sort_by)
            )
            rows = cur.fetchall()
            cur.close()

        finally:
            conn.close()

        print(f"\nPage {page + 1}")
        print_rows(rows)

        command = input("n-next, p-prev, q-quit: ").strip().lower()

        if command == "n":
            page += 1

        elif command == "p":
            if page > 0:
                page -= 1

        elif command == "q":
            break


def export_to_json(filename="exported_contacts.json"):
    contacts = get_contacts_nested()

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4, ensure_ascii=False, default=str)

    print(f"Exported to {filename}")


def get_contacts_nested():
    conn = get_connection()

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            """
            SELECT
                c.id,
                c.name,
                c.email,
                c.birthday,
                COALESCE(g.name, 'Other') AS group_name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.name;
            """
        )

        contacts = cur.fetchall()

        for contact in contacts:
            cur.execute(
                """
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s
                ORDER BY id;
                """,
                (contact["id"],)
            )
            contact["phones"] = cur.fetchall()
            contact["group"] = contact.pop("group_name")
            contact.pop("id")

        cur.close()
        return contacts

    finally:
        conn.close()


def import_from_json(filename="sample_contacts.json"):
    path = Path(input("JSON filename, empty for sample_contacts.json: ").strip() or filename)

    if not path.exists():
        print("File not found.")
        return

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    conn = get_connection()

    try:
        cur = conn.cursor()

        for item in data:
            name = item.get("name", "").strip()

            if not name:
                continue

            existing_id = get_contact_id(cur, name)

            if existing_id:
                print(f"Duplicate contact: {name}")
                action = input("skip or overwrite? ").strip().lower()

                if action != "overwrite":
                    print("Skipped.")
                    continue

                contact_id = overwrite_contact(cur, existing_id, item)

            else:
                contact_id = insert_contact_from_dict(cur, item)

            insert_phones_from_list(cur, contact_id, item.get("phones", []))

        conn.commit()
        cur.close()
        print("JSON import finished.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


def insert_contact_from_dict(cur, item):
    group_id = get_group_id(cur, item.get("group", "Other"))
    birthday = item.get("birthday") or None
    email = item.get("email") or None

    cur.execute(
        """
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (item["name"], email, birthday, group_id)
    )

    return cur.fetchone()[0]


def overwrite_contact(cur, contact_id, item):
    group_id = get_group_id(cur, item.get("group", "Other"))
    birthday = item.get("birthday") or None
    email = item.get("email") or None

    cur.execute(
        """
        UPDATE contacts
        SET email = %s,
            birthday = %s,
            group_id = %s
        WHERE id = %s;
        """,
        (email, birthday, group_id, contact_id)
    )

    cur.execute("DELETE FROM phones WHERE contact_id = %s;", (contact_id,))

    return contact_id


def insert_phones_from_list(cur, contact_id, phones):
    for item in phones:
        phone = item.get("phone", "").strip()
        phone_type = normalize_phone_type(item.get("type", "mobile"))

        if phone:
            cur.execute(
                """
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
                ON CONFLICT (contact_id, phone) DO UPDATE
                SET type = EXCLUDED.type;
                """,
                (contact_id, phone, phone_type)
            )


def import_from_csv(filename="sample_contacts.csv"):
    path = Path(input("CSV filename, empty for sample_contacts.csv: ").strip() or filename)

    if not path.exists():
        print("File not found.")
        return

    conn = get_connection()

    try:
        cur = conn.cursor()

        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row.get("name", "").strip()

                if not name:
                    continue

                group_id = get_group_id(cur, row.get("group", "Other").strip() or "Other")
                email = row.get("email", "").strip() or None
                birthday = row.get("birthday", "").strip() or None

                cur.execute(
                    """
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (name) DO UPDATE
                    SET email = EXCLUDED.email,
                        birthday = EXCLUDED.birthday,
                        group_id = EXCLUDED.group_id
                    RETURNING id;
                    """,
                    (name, email, birthday, group_id)
                )

                contact_id = cur.fetchone()[0]

                phone = row.get("phone", "").strip()
                phone_type = normalize_phone_type(row.get("type", "mobile"))

                if phone:
                    cur.execute(
                        """
                        INSERT INTO phones(contact_id, phone, type)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (contact_id, phone) DO UPDATE
                        SET type = EXCLUDED.type;
                        """,
                        (contact_id, phone, phone_type)
                    )

        conn.commit()
        cur.close()
        print("CSV import finished.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


def delete_contact_console():
    value = input("\nDelete by name or phone: ").strip()

    conn = get_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM contacts c
            WHERE c.name = %s
               OR EXISTS (
                    SELECT 1
                    FROM phones p
                    WHERE p.contact_id = c.id
                      AND p.phone = %s
               );
            """,
            (value, value)
        )

        conn.commit()
        deleted = cur.rowcount
        cur.close()

        print(f"Deleted contacts: {deleted}")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


def update_contact_console():
    name = input("\nContact name to update: ").strip()
    new_email = input("New email, empty to skip: ").strip()
    new_birthday = input("New birthday YYYY-MM-DD, empty to skip: ").strip()

    if not new_email and not new_birthday:
        print("Nothing to update.")
        return

    conn = get_connection()

    try:
        cur = conn.cursor()

        if new_email:
            cur.execute("UPDATE contacts SET email = %s WHERE name = %s;", (new_email, name))

        if new_birthday:
            cur.execute("UPDATE contacts SET birthday = %s WHERE name = %s;", (new_birthday, name))

        conn.commit()
        cur.close()
        print("Contact updated.")

    except Exception as error:
        conn.rollback()
        print("Error:", error)

    finally:
        conn.close()


def show_menu():
    print("""
PhoneBook TSIS 1
1. Setup database schema and procedures
2. Show all contacts
3. Add contact
4. Add phone to contact
5. Move contact to group
6. Search contacts
7. Search by email
8. Filter by group
9. Sort contacts
10. Paginated navigation
11. Import from CSV
12. Export to JSON
13. Import from JSON
14. Update contact email/birthday
15. Delete contact
0. Exit
""")


def main():
    while True:
        show_menu()
        choice = input("Choose: ").strip()

        if choice == "1": setup_database()
        elif choice == "2": show_all_contacts()
        elif choice == "3": add_contact_console()
        elif choice == "4": add_phone_console()
        elif choice == "5": move_to_group_console()
        elif choice == "6": search_contacts_console()
        elif choice == "7": search_by_email_console()
        elif choice == "8": filter_by_group_console()
        elif choice == "9": sort_contacts_console()
        elif choice == "10": paginated_navigation()
        elif choice == "11": import_from_csv()
        elif choice == "12": export_to_json()
        elif choice == "13": import_from_json()
        elif choice == "14": update_contact_console()
        elif choice == "15": delete_contact_console()
        elif choice == "0":
            print("Bye.")
            break
        else:
            print("Wrong option.")


if __name__ == "__main__":
    main()
