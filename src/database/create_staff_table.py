from src.utils import DATABASE_DIR
import sqlite3

def create_staff_table():

  conn = sqlite3.connect(DATABASE_DIR)
  cursor = conn.cursor()

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS Staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Title TEXT NOT NULL,
            PasswordHash TEXT NOT NULL,
            RegistrationStatus TEXT NOT NULL
        )
    """)
  conn.commit()
  conn.close()