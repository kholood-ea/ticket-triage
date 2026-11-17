import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    text       TEXT NOT NULL,
    channel    TEXT NOT NULL,
    metadata   TEXT,
    category   TEXT,
    priority   TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
)
"""


@contextmanager
def connect(db_path: str):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path: str) -> None:
    with connect(db_path) as conn:
        conn.execute(SCHEMA)


def insert_ticket(db_path, text, channel, metadata=None, category=None, priority=None) -> int:
    with connect(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO tickets (text, channel, metadata, category, priority) VALUES (?, ?, ?, ?, ?)",
            (text, channel, json.dumps(metadata, ensure_ascii=False) if metadata else None, category, priority),
        )
        return cur.lastrowid


def get_ticket(db_path: str, ticket_id: int) -> dict | None:
    with connect(db_path) as conn:
        row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    if row is None:
        return None
    d = dict(row)
    d["metadata"] = json.loads(d["metadata"]) if d["metadata"] else None
    return d


def counts_by_category(db_path: str) -> list[dict]:
    # SQL practice: GROUP BY + COALESCE for tickets not yet classified.
    sql = """
        SELECT COALESCE(category, 'unclassified') AS category, COUNT(*) AS n
        FROM tickets
        GROUP BY 1
        ORDER BY n DESC, category ASC
    """
    with connect(db_path) as conn:
        return [dict(r) for r in conn.execute(sql).fetchall()]
