import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('viewLabsDB.db')
cursor = conn.cursor()

# Drop tables if they exist
tables_to_drop = ['lab', 'user', 'computer', 'announcement', 'booking']
for table in tables_to_drop:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Commit changes and close the connection
conn.commit()
conn.close()

print("Dropped existing tables.")
