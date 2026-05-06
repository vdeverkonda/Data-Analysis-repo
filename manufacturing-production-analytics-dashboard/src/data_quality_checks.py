from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"

def run_checks():
    files = ["production_jobs.csv", "downtime_logs.csv", "inventory.csv", "quality_metrics.csv"]
    results = []
    for file in files:
        df = pd.read_csv(RAW / file)
        results.append({
            "file": file,
            "rows": len(df),
            "duplicate_rows": int(df.duplicated().sum()),
            "missing_values": int(df.isna().sum().sum())
        })
    out = pd.DataFrame(results)
    print(out.to_string(index=False))
    return out

if __name__ == "__main__":
    run_checks()
