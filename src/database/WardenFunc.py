from src.utils import DATABASE_DIR
import sqlite3

def makeArrestCase():
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    SuspectID = questionary.text("").ask()
    Name = questionary.text("").ask()
    Ethnicity = questionary.text("").ask()
    Height = questionary.text("").ask()
    Weight = questionary.text("").ask()
    FrontProfile = questionary.text("").ask()
    SideProfile = questionary.text("").ask()
    TimeofArrest = questionary.text("").ask()
    caseID = questionary.text("").ask()

    cursor.execute("INSERT INTO Arrested Values (ID, Name, Ethinicity, Height, Weight, FrontProfile, SideProfile, TimeofArrest) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (SuspectID, Name, Ethnicity, Height, Weight, FrontProfile, SideProfile, TimeofArrest))
    cursor.execute("ALTER TABLE Arrested SET Arrested = TRUE WHERE ID = ?", (SuspectID,))
    cursor.execute("INSERT INTO ArrestFromCase Values (CaseID, SuspectID) VALUES (?, ?)", (caseID, SuspectID))
    conn.commit()
    conn.close()

def LinktoCase(suspectID, caseID):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO ArrestFromCase Values (CaseID, SuspectID) VALUES (?, ?)", (caseID, suspectID))
    conn.commit()
    conn.close()