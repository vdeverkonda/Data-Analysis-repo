from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data" / "processed" / "supply_chain_clean.csv"
OUT = Path(__file__).resolve().parents[1] / "reports" / "supply_chain_kpis.xlsx"

def build_kpis():
    df = pd.read_csv(DATA, parse_dates=["date"])
    summary = df.groupby("material").agg(
        total_demand=("material_demand", "sum"),
        avg_production=("production_volume", "mean"),
        avg_inventory=("ending_inventory", "mean"),
        avg_waste=("waste_percent", "mean"),
        avg_inventory_doh=("inventory_doh", "mean")
    ).round(2).reset_index()
    weekly = df.groupby(["week", "material"]).agg(
        weekly_demand=("material_demand", "sum"),
        weekly_production=("production_volume", "sum"),
        avg_waste=("waste_percent", "mean")
    ).round(2).reset_index()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(OUT) as writer:
        summary.to_excel(writer, sheet_name="Material Summary", index=False)
        weekly.to_excel(writer, sheet_name="Weekly KPIs", index=False)
    print(f"Saved KPI workbook to {OUT}")

if __name__ == "__main__":
    build_kpis()
