from src.utils import DATABASE_DIR
import sqlite3

def create_CaseFiles_table():

    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CaseFiles (
            case_id INTEGER NOT NULL,
            MajorVersion INTEGER,
            MinorVersion INTEGER,
            FilePath TEXT,
            FOREIGN KEY (case_id) REFERENCES Cases(case_id)
        );
    """)