from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "processed" / "manufacturing_master.csv"
RAW = BASE / "data" / "raw"
REPORT = BASE / "reports" / "manufacturing_kpi_report.xlsx"

def create_report():
    master = pd.read_csv(DATA, parse_dates=["date"])
    downtime = pd.read_csv(RAW / "downtime_logs.csv")
    inventory = pd.read_csv(RAW / "inventory.csv")
    downtime_pareto = downtime.groupby("downtime_reason")["minutes"].sum().sort_values(ascending=False).reset_index()
    inventory_summary = inventory.groupby("material").agg(
        avg_variance=("variance", "mean"),
        total_abs_variance=("variance", lambda x: x.abs().sum())
    ).round(2).reset_index()
    daily_kpis = master[["date", "throughput", "downtime_minutes", "yield_calc", "waste_percent", "oee", "total_inventory_variance"]]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(REPORT) as writer:
        daily_kpis.to_excel(writer, sheet_name="Daily KPIs", index=False)
        downtime_pareto.to_excel(writer, sheet_name="Downtime Pareto", index=False)
        inventory_summary.to_excel(writer, sheet_name="Inventory Variance", index=False)
    print(f"Saved report to {REPORT}")

if __name__ == "__main__":
    create_report()
