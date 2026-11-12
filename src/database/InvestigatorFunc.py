from pathlib import Path
import shutil
from src.utils import DATABASE_DIR
import sqlite3


REPO_ROOT = Path(__file__).resolve().parent
APPROVED_DIR = (
    REPO_ROOT / "data")  

def CreateCase(time, codename, filepath, ID, majorver):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Cases (TimeofIncident,CodeName,Status)Values (?)(?)('Ongoing')", (time, codename,))
    cursor.execute("INSERT INTO CasesFiles (Majorver, Caseid, Filepath) Values (?) WHERE CaseID = ?", (majorver, filepath, ID,))
    conn.commit()
    conn.close()

#unfinished, need to finish this
def acceptMinorVer(ID, filepath):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    #need to implement the code for getting the data from the minor version temp directory
    cursor.execute(
      "SELECT Filepath FROM CasesFiles WHERE CaseID = ? AND Minorver IS NOT"
      " NULL ORDER BY Minorver DESC LIMIT 1",
      (ID,),
  )
    temp_row = cursor.fetchone()

    if temp_row is None:
        print(f"No pending minor version found for Case {ID}.")
        conn.close()
        return

    temp_filepath = temp_row[0]

    # Move the file from the temp directory to the approved directory
    shutil.move(temp_filepath, APPROVED_DIR / Path(temp_filepath).name)

    #get last majorversion of this case
    cursor.execute("SELECT Majorver FROM CasesFiles WHERE CaseID = (?) ORDER BY Majorver DESC LIMIT 1", (ID,))
    majorver = int(cursor.fetchone()[0])
    majorver = float(round((majorver + 1), 1))

    cursor.execute("INSERT INTO CasesFiles (Majorver, Caseid, Filepath) Values (?, ?, ?)", (majorver, ID, filepath,))
    conn.commit()
    conn.close()

def createSuspect(Codename, photofilepath):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Suspects (CodeName, Photo, Guility, Apprehended) Values (?,?,FALSE,'At Large')", (Codename, photofilepath,))
    conn.commit()
    conn.close()

def LinkSuspectCase(CaseID, SuspectID):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO CasesSuspects (CaseID, SuspectID) Values (?,?)", (CaseID, SuspectID,))
    conn.commit()
    conn.close()

def updateGuiltiness(SuspectID, GuiltyStatus):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    if GuiltyStatus == "Guilty":
        cursor.execute("UPDATE Suspects SET Guility = FALSE WHERE ID = ?", ( SuspectID,))
        conn.commit()
        conn.close()
    elif GuiltyStatus == "Not Guilty":
        cursor.execute("UPDATE Suspects SET Guility = TRUE WHERE ID = ?", ( SuspectID,))
        conn.commit()
        conn.close()
    else:
        cursor.execute("UPDATE Suspects SET Guility = NULL WHERE ID = ?", ( SuspectID,))