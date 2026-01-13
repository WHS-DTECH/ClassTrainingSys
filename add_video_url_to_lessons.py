import sqlite3

# Update this path if your database is elsewhere
DB_PATH = 'app.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE lessons ADD COLUMN video_url TEXT;")
    print("Successfully added video_url column to lessons table.")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("Column video_url already exists.")
    else:
        print(f"Error: {e}")
finally:
    conn.commit()
    conn.close()
