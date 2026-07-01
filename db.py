import sqlite3
import json

DB_FILE = "scans.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            score INTEGER,
            risk TEXT,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


def save_scan(url, score, risk, data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute(
        "INSERT INTO scans (url, score, risk, data) VALUES (?, ?, ?, ?)",
        (url, score, risk, json.dumps(data))
    )

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
SELECT url, score, risk, timestamp
FROM (
    SELECT url, score, risk, timestamp
    FROM scans
    ORDER BY timestamp DESC
    LIMIT 10
)
ORDER BY timestamp ASC
""")
    rows = c.fetchall()

    conn.close()
    return rows