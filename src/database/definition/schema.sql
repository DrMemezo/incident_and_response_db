CREATE TABLE Staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Title TEXT NOT NULL,
            PasswordHash TEXT NOT NULL,
            RegistrationStatus TEXT NOT NULL
        );
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE Cases (
        case_id INTEGER PRIMARY KEY AUTOINCREMENT,
        code VARCHAR UNIQUE NOT NULL,
        status TEXT DEFAULT 'Open',
        time_of_incident TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
CREATE TABLE Suspect (
            suspect_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            alias TEXT,
            date_of_birth DATE,
            Apprehended TEXT,
            Guilty BOOLEAN,
            Photo
        );
CREATE TABLE Arrested (
            arrested_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Ethnicity VARCHAR,
            Height Float,
            Weight Float,
            Front_Profile BLOB,
            Side_Profile BLOB,
            arrest_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
CREATE TABLE Alters (
            staff_id INTEGER NOT NULL,
            case_id INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (staff_id) REFERENCES Staff(staff_id),
            FOREIGN KEY (case_id) REFERENCES Cases(case_id)
        );
CREATE TABLE Linked (
            case_id INTEGER NOT NULL,
            suspect_id INTEGER NOT NULL,
            PRIMARY KEY (case_id, suspect_id),
            FOREIGN KEY (case_id) REFERENCES Cases(case_id),
            FOREIGN KEY (suspect_id) REFERENCES Suspect(suspect_id)
        );
CREATE TABLE ArrestFromCase (
            arrested_id INTEGER NOT NULL,
            case_id INTEGER NOT NULL,
            PRIMARY KEY (arrested_id, case_id),
            FOREIGN KEY (arrested_id) REFERENCES Arrested(arrested_id),
            FOREIGN KEY (case_id) REFERENCES Cases(case_id)
        );
