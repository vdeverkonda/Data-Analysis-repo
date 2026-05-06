from pathlib import Path
import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "supply_chain_daily.csv"
OUT = Path(__file__).resolve().parents[1] / "data" / "processed" / "supply_chain_clean.csv"

def clean_data():
    df = pd.read_csv(RAW, parse_dates=["date"])
    df = df.drop_duplicates()
    numeric_cols = ["material_demand", "production_volume", "ending_inventory", "waste_percent"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df["month"] = df["date"].dt.month
    df["week"] = df["date"].dt.isocalendar().week.astype(int)
    df["day_of_week"] = df["date"].dt.dayofweek
    df["inventory_doh"] = df["ending_inventory"] / (df["material_demand"] / 30)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Saved clean data to {OUT}")
    return df

if __name__ == "__main__":
    clean_data()
