from pathlib import Path 


ROOT_DIR = Path(__file__).parent.parent
UI_DIR = ROOT_DIR / "ui" / "v3" / "asche_yiu_screens 2" /  "ui"
UI_V1_DIR = ROOT_DIR / "v1"

DATABASE_DIR = ROOT_DIR / "police.db"


if __name__ == "__main__":
    print(UI_DIR)