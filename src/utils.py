from pathlib import Path 
import datetime as dt
import hashlib


ROOT_DIR = Path(__file__).parent.parent
UI_DIR = ROOT_DIR / "ui" / "v3" / "asche_yiu_screens 2" /  "ui"
UI_V1_DIR = ROOT_DIR / "v1"

DATABASE_DIR = ROOT_DIR / "police.db"
TIME_FORMAT = "%d/%m/%Y %H:%M"

DOT = "\u00b7"

ACCEPTED = "Accepted"
REJECTED = "Rejected"
PENDING = "Pending"

CHIEF = "Chief"

def get_pass_hash(password:str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def toi_to_str(toi:dt.datetime|str) -> str:
    if type(toi) == str:
        return toi

    return toi.strftime(TIME_FORMAT) # type: ignore

def format_caseid(caseid: int|str) -> str:
    if type(caseid) == str:
        return caseid 

    return f"{caseid:04d}"

if __name__ == "__main__":
    print(UI_DIR)