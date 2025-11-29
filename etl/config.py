from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_USAGE_CSV = RAW_DIR / "raw_usage_2025_01.csv"
SESSIONS_JSON = RAW_DIR / "sessions.json"
ROAMING_EXCEL = RAW_DIR / "partner_roaming.xlsx"