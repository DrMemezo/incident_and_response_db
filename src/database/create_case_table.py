from src.utils import DATABASE_DIR
import sqlite3

def create_case_table():

    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cases (
        case_id INTEGER PRIMARY KEY AUTOINCREMENT,
        code VARCHAR UNIQUE NOT NULL,
        status TEXT DEFAULT 'Open',
        time_of_incident TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    )
    """)