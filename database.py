import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    premium INTEGER DEFAULT 0,
    score INTEGER DEFAULT 0
)
""")

conn.commit()

def add_user(user_id, name):
    cur.execute("INSERT OR IGNORE INTO users(user_id,name) VALUES(?,?)", (user_id,name))
    conn.commit()

def add_score(user_id):
    cur.execute("UPDATE users SET score = score + 1 WHERE user_id=?", (user_id,))
    conn.commit()

def get_score(user_id):
    cur.execute("SELECT score FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    return row[0] if row else 0
