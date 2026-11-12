from src.utils import DATABASE_DIR
import hashlib
import sqlite3
import questionary

from src.database.definition.create_staff_table import create_staff_table

def add_chief():
  conn = sqlite3.connect(DATABASE_DIR)
  cursor = conn.cursor()

  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Staff';")
  table_exists = cursor.fetchone()

  if not table_exists:
    conn.close()
    raise ValueError("The staff table has not been created yet.")  

  print("=== Add Police Chief ===")

  name = questionary.text("Enter the Chief's name:").ask()

  if not name:
    print("[Error] Name cannot be empty.")
    conn.close()
    return

  cursor.execute("SELECT * FROM Staff WHERE Name=?", 
                 (name,)) # To make sure no one else has the same name
  name_already_there = cursor.fetchone()

  if name_already_there is not None:
    print("[Error] Choose a different name.")
    conn.close()
    return


  password = questionary.password("Enter the Chief's password:").ask()

  # Validate that inputs are not empty
  if not password:
    print("[Error] Password cannot be empty.")
    conn.close()
    return



  password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

  title = "Chief"
  registration_status = "Accepted"

  cursor.execute(
      """
        INSERT INTO Staff (Name, Title, PasswordHash, RegistrationStatus)
        VALUES (?, ?, ?, ?)
    """,
      (name, title, password_hash, registration_status),
  )

  conn.commit()

  chief_id = cursor.lastrowid
  print(
      f"\n[Success] Chief '{name}' added successfully! Assigned Staff"
      f" ID: {chief_id}"
  )

  conn.close()



# !!!!! DEPRECATED !!!!
def adding_chief():
  """ DEPRECATED. Dont use """
  conn = sqlite3.connect(DATABASE_DIR)
  cursor = conn.cursor()

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS Staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Title TEXT NOT NULL,
            PasswordHash TEXT NOT NULL,
            RegistrationStatus TEXT NOT NULL
        )
    """)
  conn.commit()

  print("=== Add Police Chief ===")

  name = questionary.text("Enter the Chief's name:").ask()
  password = questionary.password("Enter the Chief's password:").ask()

  # Validate that inputs are not empty
  if not name or not password:
    print("[Error] Name and password cannot be empty.")
    conn.close()
    return

  password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

  title = "Chief"
  registration_status = "Accepted"

  cursor.execute(
      """
        INSERT INTO Staff (Name, Title, PasswordHash, RegistrationStatus)
        VALUES (?, ?, ?, ?)
    """,
      (name, title, password_hash, registration_status),
  )

  conn.commit()

  chief_id = cursor.lastrowid
  print(
      f"\n[Success] Chief '{name}' added successfully! Assigned Staff"
      f" ID: {chief_id}"
  )

  conn.close()


if __name__ == "__main__":
    create_staff_table()
    add_chief()