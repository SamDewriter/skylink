
from __future__ import annotations

import pandas as pd
from typing import Dict

def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_", regex=False)
    print("Standardize Type", type(df))
    return df


def _parse_timestamp(df: pd.DataFrame, column: str = "timestamp") -> pd.DataFrame:
    """Convert a timestamp column to timezone-aware pandas datetime (UTC)."""
    print(type(df))
    if column not in list(df.columns):
        return df

    df = df.copy()
    df[column] = pd.to_datetime(df[column], errors="coerce", utc=True)
    return df

def _clean_usage(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    print(type(df))
    df = _standardize_columns(df)
    df = _parse_timestamp(df)
    
    if "avg_throughput" in df.columns:
        median_tp = df['avg_throughput'].median()
        df["avg_throughput"] = df["avg_throughput"].fillna(median_tp)

    if "app_category" in df.columns:
        df['app_category'] = df['app_category'].fillna('unknown')

    if "duration_ms" in df.columns:
        df = df[df['duration_ms'] >= 0]

    if "session_id" in df.columns:
        df = df.drop_duplicates(subset=["session_id"], keep='first')


    if {"download_mb", "upload_mb"}.issubset(df.columns):
        df['total_usage_mb'] = df['download_mb'].fillna(0) + df['upload_mb'].fillna(0)

    return df


def _aggregate_daily(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty or "msisdn" not in df.columns or "timestamp" not in df.columns:
        return pd.DataFrame()

    df["date"] = df["timestamp"].dt.date
    # 1. Define the base aggregations
    aggregations = {
        "total_usage_mb": ("total_usage_mb", "sum"),
        "sessions": ("session_id", "nunique"),
        "avg_throughput": ("avg_throughput", "mean"),
    }

    # 2. Conditionally add the latency/count aggregation
    if "latency_ms" in df.columns:
        aggregations["avg_latency_ms"] = ("latency_ms", "mean")
    else:
        # If latency is missing, use count of timestamps instead for the same output column name
        aggregations["avg_latency_ms"] = ("timestamp", "count")

    # 3. Apply the constructed dictionary to .agg()
    agg = (
        df.groupby(["msisdn", "date"])
        .agg(**aggregations) # Use the dynamically created dictionary
        .reset_index()
    )
    
    return agg

def transform_all(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    usage = dfs.get("usage", pd.DataFrame())
    print(type(usage))

    clean_usage = _clean_usage(usage)
    daily_usage = _aggregate_daily(clean_usage)

    return {
        "clean_usage": clean_usage,
        "daily_usage": daily_usage
    }


    
    