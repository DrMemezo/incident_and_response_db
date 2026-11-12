from src.utils import DATABASE_DIR, get_pass_hash, PENDING, ACCEPTED, REJECTED
import sqlite3

def get_pending_reg_requests():
    """ Returns a list of Name, Title tuples NO TIMES YET"""
    with sqlite3.connect(DATABASE_DIR) as conn:
        cursor = conn.cursor()

        # TODO: Get registration times as well
        cursor.execute(""" 
            SELECT Name, Title WHERE RegistrationStatus = ?
        """, (PENDING,))

        if (x := cursor.fetchall()):
            return x 
        else:
            return []


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

