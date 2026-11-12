from pathlib import Path
import shutil
from src.utils import DATABASE_DIR
import sqlite3

REPO_ROOT = Path(__file__).resolve().parent
TEMP_DIR = REPO_ROOT / "data" / "temp"

def submitTempCase(time, codename):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Cases (TimeofIncident,CodeName,Status)Values (?)(?)('Pending')", (time, codename,))
    conn.commit()
    conn.close()



def submitMinorVer(ID, filepath):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    #check if it already exists
    cursor.execute("SELECT ID FROM CaseFiles WHERE CaseID = (?)", (ID,))
    result = cursor.fetchone()

    #get the filepath 
    source_path = Path(filepath)
    
    if result == None:
        cursor.execute("INSERT INTO CasesFiles (CaseID, Minorver, Filepath) Values (?, 0.1 ,?)", (ID, filepath,))
        minorver = 0.1
        #create a new filename with the minor version and copy the file to the temp directory


        new_filename = f"case_{ID}_v{minorver}{source_path.suffix}"
        shutil.copy2(source_path, TEMP_DIR / new_filename)
    else:
        cursor.execute("SELECT Minorver FROM CasesFiles WHERE CaseID = (?)", (ID,))
        minorver = cursor.fetchone()[0]
        minorver = round(minorver + 0.1, 1)
        cursor.execute("UPDATE CasesFiles SET Minorver = ?, Filepath = ? WHERE CaseID = ?", (minorver, filepath, ID,))


        #create a new filename with the minor version and copy the file to the temp directory
        new_filename = f"case_{ID}_v{minorver}{source_path.suffix}"
        shutil.copy2(source_path, TEMP_DIR / new_filename)
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