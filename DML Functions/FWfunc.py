from src.utils import DATABASE_DIR
import sqlite3

def submitTempCase(time, codename):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Cases (TimeofIncident,CodeName,Status)Values (?)(?)('Pending')", (time, codename,))
    conn.commit()
    conn.close()



def submitMinorVer(ID, filepath, minorver):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO CasesFiles (Minorver, Filepath) Values (?) WHERE CaseID = ?", (minorver, filepath, ID,))
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