from src.utils import DATABASE_DIR
import sqlite3

def create_arrested_table():

    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Arrested (
            arrested_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Ethnicity VARCHAR,
            Height Float,
            Weight Float,
            Front_Profile BLOB,
            Side_Profile BLOB,
            arrest_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        );
    """)