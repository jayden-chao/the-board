import sqlite3 as sl

def init_db():
    conn = sl.connect("chat.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (session_id) REFERENCES sessions(id)
    );
    """)

    conn.commit()
    conn.close()


def get_db():
    return sl.connect("chat.db", check_same_thread=False)


def create_sessions(session_id, created_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sessions (id, created_at) VALUES (?, ?)",
        (session_id, created_at)
    )

    conn.commit()
    conn.close()


def session_exists(session_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT 1 FROM sessions WHERE id = ?",
        (session_id,)
    )

    exists = cur.fetchone() is not None
    conn.close()
    return exists


def delete_session(session_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM messages WHERE session_id = ?", (session_id,))
    cur.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

    conn.commit()
    conn.close()