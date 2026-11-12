from src.utils import DATABASE_DIR
import sqlite3

def CreateCase(time, codename, filepath, ID, majorver):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Cases (TimeofIncident,CodeName,Status)Values (?)(?)('Ongoing')", (time, codename,))
    cursor.execute("INSERT INTO CasesFiles (Majorver, Caseid, Filepath) Values (?) WHERE CaseID = ?", (majorver, filepath, ID,))
    conn.commit()
    conn.close()

def acceptMinorVer(ID, minorver):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()


    cursor.execute("INSERT INTO CasesFiles (Majorver, Caseid, Filepath) Values (SELECT Majorver, Caseid, Filepath FROM CasesFiles WHERE CaseID = ? AND Minorver = ?)", (ID, minorver,))
    cursor.execute("DELETE FROM CasesFiles WHERE CaseID = ? AND Minorver = ?", (ID, minorver,))
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