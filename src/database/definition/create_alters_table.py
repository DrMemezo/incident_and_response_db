from src.utils import DATABASE_DIR
import sqlite3

def create_alters_table():

    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alters (
            staff_id INTEGER NOT NULL,
            case_id INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
            FOREIGN KEY (case_id) REFERENCES Cases(case_id)
        );
    """)