from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
OUT = BASE / "data" / "processed" / "manufacturing_master.csv"

def build_master():
    prod = pd.read_csv(RAW / "production_jobs.csv", parse_dates=["date"])
    inv = pd.read_csv(RAW / "inventory.csv", parse_dates=["date"])
    quality = pd.read_csv(RAW / "quality_metrics.csv", parse_dates=["date"])
    daily = prod.groupby("date").agg(
        planned_units=("planned_units", "sum"),
        units_produced=("units_produced", "sum"),
        good_units=("good_units", "sum"),
        scrap_units=("scrap_units", "sum"),
        downtime_minutes=("downtime_minutes", "sum")
    ).reset_index()
    inv_daily = inv.groupby("date").agg(total_inventory_variance=("variance", "sum")).reset_index()
    master = daily.merge(inv_daily, on="date", how="left").merge(quality, on="date", how="left")
    master["throughput"] = master["units_produced"]
    master["yield_calc"] = (master["good_units"] / master["units_produced"] * 100).round(2)
    master["waste_percent"] = (master["scrap_units"] / master["units_produced"] * 100).round(2)
    master["availability"] = ((1440 - master["downtime_minutes"]) / 1440).clip(0, 1)
    master["performance"] = (master["units_produced"] / master["planned_units"]).clip(0, 1)
    master["quality"] = (master["good_units"] / master["units_produced"]).clip(0, 1)
    master["oee"] = (master["availability"] * master["performance"] * master["quality"] * 100).round(2)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    master.to_csv(OUT, index=False)
    print(f"Saved master data to {OUT}")
    return master

if __name__ == "__main__":
    build_master()
