from src.utils import DATABASE_DIR
import sqlite3

def makeArrestCase(SuspectID, Name, Ethnicity, Height, Weight, FrontProfile, SideProfile, TimeofArrest,caseID):
    conn = sqlite3.connect(DATABASE_DIR)
    cursor = conn.cursor()

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