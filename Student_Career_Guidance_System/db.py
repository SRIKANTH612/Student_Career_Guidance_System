import sqlite3

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, user_id INTEGER, name TEXT, career TEXT, readiness INTEGER, missing_skills TEXT)")
    c.execute("INSERT OR IGNORE INTO users VALUES (1,'user','user123')")
    conn.commit()
    conn.close()
