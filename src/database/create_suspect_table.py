from src.utils import DATABASE_DIR
import sqlite3

def create_suspect_table():

    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Suspect (
            suspect_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            alias TEXT,
            date_of_birth DATE,
            Apprehended TEXT,
            Guilty BOOLEAN,
            Photo
        );
    """)