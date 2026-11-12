from src.utils import DATABASE_DIR


if __name__ == "__main__":
    DATABASE_DIR.unlink(missing_ok=True) 