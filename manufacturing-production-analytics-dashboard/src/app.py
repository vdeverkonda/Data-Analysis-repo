import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Manufacturing Production Analytics", layout="wide")
st.title("Manufacturing & Production Analytics Dashboard")
BASE = Path(__file__).resolve().parents[1]
master = pd.read_csv(BASE / "data" / "processed" / "manufacturing_master.csv", parse_dates=["date"])
downtime = pd.read_csv(BASE / "data" / "raw" / "downtime_logs.csv")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Throughput", f"{master['throughput'].sum():,.0f}")
col2.metric("Avg OEE", f"{master['oee'].mean():.2f}%")
col3.metric("Avg Yield", f"{master['yield_calc'].mean():.2f}%")
col4.metric("Avg Waste", f"{master['waste_percent'].mean():.2f}%")
st.subheader("Daily Production KPIs")
st.line_chart(master.set_index("date")[["throughput", "downtime_minutes", "oee"]])
st.subheader("Downtime Pareto")
pareto = downtime.groupby("downtime_reason")["minutes"].sum().sort_values(ascending=False)
st.bar_chart(pareto)
st.subheader("Recent Records")
st.dataframe(master.tail(30), use_container_width=True)
