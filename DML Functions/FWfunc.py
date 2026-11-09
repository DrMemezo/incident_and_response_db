from src.utils import DATABASE_DIR
import sqlite3
import questionary

def submitTempCase():
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    time = questionary.text("").ask()
    codename = questionary.text("").ask()

    cursor.execute("INSERT INTO Cases (TimeofIncident,CodeName,Status)Values (?)(?)('Pending')", (time, codename,))
    conn.commit()
    conn.close()


def submitMinorVer():
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    ID = questionary.text("").ask()
    filepath = questionary.text("").ask()
    minorver = questionary.text("").ask()

    cursor.execute("INSERT INTO CasesFiles (Minorver, Filepath) Values (?) WHERE CaseID = ?", (minorver, filepath, ID,))
    conn.commit()

def createSuspect():
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    Codename = questionary.text("").ask()
    photofilepath = questionary.text("").ask()

    cursor.execute("INSERT INTO Suspects (CodeName, Photo, Guility, Apprehended) Values (?,?,FALSE,'At Large')", (Codename, photofilepath,))
    conn.commit()
    conn.close()

def LinkSuspectCase():
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    CaseID = questionary.text("").ask()
    SuspectID = questionary.text("").ask()

    cursor.execute("INSERT INTO CasesSuspects (CaseID, SuspectID) Values (?,?)", (CaseID, SuspectID,))
    conn.commit()
    conn.close()