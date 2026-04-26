try:
    import psycopg2
except ImportError:
    psycopg2 = None

from config import DB_CONFIG

last_error = ""


def get_connection():
    global last_error

    if psycopg2 is None:
        last_error = "psycopg2 is not installed"
        return None

    try:
        return psycopg2.connect(**DB_CONFIG)

    except Exception as error:
        last_error = str(error)
        return None


def init_db():
    # Creates tables from the TSIS schema if database connection works.
    conn = get_connection()

    if conn is None:
        return False

    try:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)

        conn.commit()
        cur.close()
        conn.close()

        return True

    except Exception as error:
        global last_error
        last_error = str(error)

        try:
            conn.rollback()
            conn.close()
        except Exception:
            pass

        return False


def get_or_create_player(username):
    conn = get_connection()

    if conn is None:
        return None

    try:
        cur = conn.cursor()

        cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
        row = cur.fetchone()

        if row:
            player_id = row[0]

        else:
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id;",
                (username,)
            )
            player_id = cur.fetchone()[0]
            conn.commit()

        cur.close()
        conn.close()

        return player_id

    except Exception as error:
        global last_error
        last_error = str(error)

        try:
            conn.rollback()
            conn.close()
        except Exception:
            pass

        return None


def save_game_session(username, score, level_reached):
    # Result is saved automatically after game over.
    player_id = get_or_create_player(username)

    if player_id is None:
        return False

    conn = get_connection()

    if conn is None:
        return False

    try:
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s);
            """,
            (player_id, int(score), int(level_reached))
        )

        conn.commit()
        cur.close()
        conn.close()

        return True

    except Exception as error:
        global last_error
        last_error = str(error)

        try:
            conn.rollback()
            conn.close()
        except Exception:
            pass

        return False


def get_top_scores(limit=10):
    conn = get_connection()

    if conn is None:
        return []

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
            LIMIT %s;
            """,
            (limit,)
        )

        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = []

        for username, score, level, played_at in rows:
            if played_at is None:
                date_text = ""
            else:
                date_text = played_at.strftime("%Y-%m-%d %H:%M")

            result.append({
                "username": username,
                "score": score,
                "level": level,
                "date": date_text
            })

        return result

    except Exception as error:
        global last_error
        last_error = str(error)

        try:
            conn.close()
        except Exception:
            pass

        return []


def get_personal_best(username):
    conn = get_connection()

    if conn is None or username.strip() == "":
        return 0

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT COALESCE(MAX(gs.score), 0)
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            WHERE p.username = %s;
            """,
            (username,)
        )

        best = cur.fetchone()[0]
        cur.close()
        conn.close()

        return int(best)

    except Exception as error:
        global last_error
        last_error = str(error)

        try:
            conn.close()
        except Exception:
            pass

        return 0


def get_last_error():
    return last_error
