import sqlite3
from src.utils import DATABASE_DIR, get_pass_hash, PENDING, ACCEPTED, REJECTED

from typing import Optional



def check_for_same_name(name:str):
    """Checks if there is a staff member with the same name already"""
    with sqlite3.connect(DATABASE_DIR) as conn:
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT * FROM Staff WHERE Name=? 
        """, (name,))

    return cursor.fetchone() is None

def submit_request(name:str, title:str, passw:str):
    """Submits a request for the staff"""
    with sqlite3.connect(DATABASE_DIR) as conn:
        cursor = conn.cursor()
        cursor.execute(
      """
        INSERT INTO Staff (Name, Title, PasswordHash, RegistrationStatus)
        VALUES (?, ?, ?, ?)
    """,
      (name, title, get_pass_hash(passw), PENDING),
    )

    conn.commit()
    conn.close()

def check_registration_denied(name, passw):
    with sqlite3.connect(DATABASE_DIR) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT RegistrationStatus FROM Staff WHERE Name = (?) AND PasswordHash = ?", (name, get_pass_hash(passw))
                       )
        result = cursor.fetchone()
        conn.close()

    if not result:
        return("You have been denied!")    

def delete_denied_registration(name, passw):
    with sqlite3.connect(DATABASE_DIR) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT RegistrationStatus FROM Staff WHERE Name = (?) AND PasswordHash = ?", (name, get_pass_hash(passw))
                           )
            result = cursor.fetchone()

            if result and result[0] == REJECTED:
                cursor.execute("DELETE FROM Staff WHERE Name = (?) AND PasswordHash = ?", (name, get_pass_hash(passw)))
                conn.commit()

def is_accepted(name:str, passw:str) -> bool:
    with sqlite3.connect(DATABASE_DIR) as conn:
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT RegistrationStatus FROM Staff WHERE Name = ? AND PasswordHash = ?
        """, (name,get_pass_hash(passw)))

        result = cursor.fetchone()
        if not result:
            return False

        return result[0] == ACCEPTED

def get_staff_info(name:str, passw:str) -> Optional[ tuple[str, str, str] ]:
    if not is_accepted(name, passw):
        return

    with sqlite3.connect(DATABASE_DIR) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT id, Name, Title FROM Staff WHERE Name=? AND PasswordHash=?""",
            (name, get_pass_hash(passw))
        )

        x = cursor.fetchone()

    return x