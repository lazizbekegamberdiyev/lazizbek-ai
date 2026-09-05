import sqlite3

DB_NAME = "memory.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_message(role, content):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content)
    )

    conn.commit()
    conn.close()


def load_messages():
    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        "SELECT role, content FROM messages ORDER BY id"
    ).fetchall()

    conn.close()

    return rows


def save_memory(memory):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "INSERT INTO memories (memory) VALUES (?)",
        (memory,)
    )

    conn.commit()
    conn.close()


def load_memories():
    conn = sqlite3.connect(DB_NAME)

    rows = conn.execute(
        "SELECT memory FROM memories ORDER BY id"
    ).fetchall()

    conn.close()

    return [row[0] for row in rows]


def get_memory_count():
    conn = sqlite3.connect(DB_NAME)

    count = conn.execute(
        "SELECT COUNT(*) FROM memories"
    ).fetchone()[0]

    conn.close()

    return count
