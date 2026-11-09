from src.utils import DATABASE_DIR
import sqlite3

# getters (to add, to reject) are temp, in real implementation get this from whichever column the chief clicks on using signals. idk how to do it any other way yet

def accept_requestChief(to_add):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("ALTER TABLE Staff SET registration_status = 'Accepted' WHERE registration_status = 'Pending' AND ID = ?)", (to_add,))
    conn.commit()
    conn.close()

def reject_requestChief(to_reject):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("UPDATE Staff SET registration_status = 'Rejected' WHERE registration_status = 'Pending' AND ID = ?", (to_reject,))
    conn.commit()
    conn.close()

def delete_staffChief(to_delete):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()


    cursor.execute("DELETE FROM Staff WHERE ID = ?", (to_delete,))
    conn.commit()
    conn.close()

def closeCaseChief(to_close):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("UPDATE Cases SET Status = 'Closed' WHERE id = (?)", (to_close,))
    conn.commit()
    conn.close()

