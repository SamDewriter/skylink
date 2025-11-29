from __future__ import annotations

from typing import Dict
import pandas as pd
from .config import RAW_USAGE_CSV, ROAMING_EXCEL, SESSIONS_JSON


def read_usage_csv() -> pd.DataFrame:
    try:
        df = pd.read_csv(RAW_USAGE_CSV)
        return df
    except FileNotFoundError:
        print(f"[extract] WARNING: CSV file not found")
        return pd.DataFrame()
    

def read_sessions_json() -> pd.DataFrame:
    try:
        df = pd.read_json(SESSIONS_JSON, lines=True)
        return df
    except FileNotFoundError:
        print(f"[extract] WARNING: JSON file not found")
        return pd.DataFrame()
    


def read_roaming_excel() -> pd.DataFrame:
    try:
        df = pd.read_excel(ROAMING_EXCEL, engine='openpyxl')
        return df
    except FileNotFoundError:
        print(f"[extract] WARNING: EXCEL file not found")
        return pd.DataFrame()
    

def extract_all() -> Dict[str, pd.DataFrame]:
    usage_df = read_usage_csv()
    sessions_df = read_sessions_json()
    roaming_df = read_roaming_excel()

    return {
        "usage": usage_df,
        "sessions": sessions_df,
        "roaming": roaming_df
    }