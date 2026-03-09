# database.py
import sqlite3

def create_database():
    try:
        # Connect to a local SQLite database (creates it if it doesn't exist)
        conn = sqlite3.connect("arogyamitra.db")
        cursor = conn.cursor()

        # Create a table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """)

        conn.commit()
        print("SQLite database and 'users' table are set up successfully!")
    except sqlite3.Error as e:
        print(f"An error occurred with the database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()