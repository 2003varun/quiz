import sqlite3

conn = sqlite3.connect("quiz.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS scores (
    username TEXT,
    score INTEGER
)
""")

conn.commit()
conn.close()

print("Database created successfully")
