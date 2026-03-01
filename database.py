import sqlite3

conn = sqlite3.connect("health.db", check_same_thread=False)
cursor = conn.cursor()

# USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# STEPS
cursor.execute("""
CREATE TABLE IF NOT EXISTS steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    step_count INTEGER
)
""")

conn.commit()

def create_user(username, password):
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

def check_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchone()

def add_steps(username, date, steps):
    cursor.execute("INSERT INTO steps (username, date, step_count) VALUES (?, ?, ?)",
                   (username, date, steps))
    conn.commit()

def get_steps(username):
    cursor.execute("SELECT date, step_count FROM steps WHERE username=?", (username,))
    return cursor.fetchall()