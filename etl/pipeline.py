
from .extract import extract_all
from .transform import transform_all
import datetime as dt


def run_pipeline() -> None:
    start = dt.datetime.utcnow()

    #1. Extract
    dfs_raw = extract_all()
    for name, df in dfs_raw.items():
        print(f" - {name}: {len(df)} rows")

    #2. Transform
    dfs_tx = transform_all(dfs_raw)
    daily_usage = dfs_tx["daily_usage"]

    print("Daily Usage: ", daily_usage)
    print(f"[pipeline] Transformed daily_usage rows: {len(daily_usage)}")

    end = dt.datetime.utcnow()
    duration = (end - start).total_seconds()    
    print(f"[pipeline] Finished ETL at {end.isoformat()}Z (duration: {duration:.1f}s)")


    #3. Load

    