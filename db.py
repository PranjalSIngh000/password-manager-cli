import sqlite3
from crypto import encrypt, decrypt

DB_PATH = "vault.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            encrypted_password BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(site: str, username: str, password: str, key: bytes):
    encrypted = encrypt(password, key)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entries (site, username, encrypted_password) VALUES (?, ?, ?)",
        (site, username, encrypted)
    )
    conn.commit()
    conn.close()

def get_entry(site: str, key: bytes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, encrypted_password FROM entries WHERE site = ?", (site,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return None
    username, encrypted_password = row
    return username, decrypt(encrypted_password, key)

def get_all_entries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT site, username, created_at FROM entries")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_entry(site: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries WHERE site = ?", (site,))
    conn.commit()
    conn.close()