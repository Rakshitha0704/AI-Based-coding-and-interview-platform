import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Create users table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Create quiz_scores table
c.execute("""
CREATE TABLE IF NOT EXISTS quiz_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    module_id TEXT,
    score INTEGER
)
""")

conn.commit()

# Insert initial users if they don't exist
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "1234"))
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("sunshine", "pass"))

conn.commit()
conn.close()
print("Database initialized successfully.")
