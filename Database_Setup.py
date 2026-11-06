import hashlib
import sqlite3
import questionary


def adding_chief():
  conn = sqlite3.connect("police.db")
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
  adding_chief()