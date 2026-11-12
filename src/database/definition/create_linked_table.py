from src.utils import DATABASE_DIR
import sqlite3

def create_linked_table():

    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Linked (
            case_id INTEGER NOT NULL,
            suspect_id INTEGER NOT NULL,
            PRIMARY KEY (case_id, suspect_id),
            FOREIGN KEY (case_id) REFERENCES Cases(case_id),
            FOREIGN KEY (suspect_id) REFERENCES Suspect(suspect_id)
        );
    """)