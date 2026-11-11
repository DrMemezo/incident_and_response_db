from src.utils import DATABASE_DIR
import sqlite3

def create_ArrestFromCase_table():

    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ArrestFromCase (
            arrested_id INTEGER NOT NULL,
            case_id INTEGER NOT NULL,
            PRIMARY KEY (arrested_id, case_id),
            FOREIGN KEY (arrested_id) REFERENCES Arrested(arrested_id),
            FOREIGN KEY (case_id) REFERENCES Cases(case_id)
        );
    """)