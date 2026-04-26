import psycopg2
from config import config


def get_connection():
    # Small helper so phonebook.py does not repeat connection code everywhere.
    params = config()
    conn = psycopg2.connect(**params)
    return conn


def test_connection():
    # I use this only to quickly check if PostgreSQL connection works.
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print("Connected to PostgreSQL:")
        print(version[0])
        cur.close()
        conn.close()

    except Exception as error:
        print("Connection error:", error)


if __name__ == "__main__":
    test_connection()
