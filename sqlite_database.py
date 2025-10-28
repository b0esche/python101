import sqlite3

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER
)
''')

# Insert data
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 25))
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 30))

# Query data
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
print("Users in database:")
for row in rows:
    print(row)

# Update data
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (26, "Alice"))

# Delete data
cursor.execute("DELETE FROM users WHERE name = ?", ("Bob",))

# Commit changes and close
conn.commit()
conn.close()

print("Database operations completed.")