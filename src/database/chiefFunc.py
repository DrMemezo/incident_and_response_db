from src.utils import DATABASE_DIR
import sqlite3

# getters (to add, to reject) are temp, in real implementation get this from whichever column the chief clicks on using signals. idk how to do it any other way yet
# TODO: Remove everything related to questionary
# TODO: 

def accept_requestChief():
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    to_add = questionary.text("").ask()

    cursor.execute("ALTER TABLE Staff SET registration_status = 'Accepted' WHERE registration_status = 'Pending' AND name = ?)", (to_add,))
    conn.commit()
    conn.close()

def reject_requestChief():
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    to_reject = questionary.text("").ask()

    cursor.execute("UPDATE Staff SET registration_status = 'Rejected' WHERE registration_status = 'Pending' AND name = ?", (to_reject,))
    conn.commit()
    conn.close()

def delete_staffChief():
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    to_delete = questionary.text("").ask()

    cursor.execute("DELETE FROM Staff WHERE name = ?", (to_delete,))
    conn.commit()
    conn.close()

def closeCaseChief():
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    to_close = questionary.text("").ask()

    cursor.execute("UPDATE Cases SET Status = 'Closed' WHERE id = (?)", (to_close,))
    conn.commit()
    conn.close()

