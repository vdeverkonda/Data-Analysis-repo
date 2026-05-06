# Manufacturing & Production Analytics Dashboard

A production analytics project designed for Production Data Analyst, Manufacturing Analyst, Operations Analyst, and BI Analyst roles.

## Business Problem
Manufacturing teams need accurate daily production, inventory, downtime, and quality reporting. Manual reports can create delays and data accuracy issues.

## What This Project Does
- Builds a manufacturing master dataset from production, inventory, quality, and downtime tables
- Calculates plant KPIs such as throughput, yield, waste, downtime, inventory variance, and OEE
- Performs data quality checks for duplicates and missing values
- Creates Excel reports for operations leadership
- Provides an interactive Streamlit dashboard

## KPIs Included
- Throughput
- Downtime minutes
- Yield percentage
- Waste percentage
- Inventory variance
- OEE
- Downtime Pareto

## How to Run
```bash
pip install -r requirements.txt
python src/etl.py
python src/data_quality_checks.py
python src/kpi_dashboard_data.py
streamlit run src/app.py
```
