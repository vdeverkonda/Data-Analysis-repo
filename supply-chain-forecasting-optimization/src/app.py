import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Supply Chain Forecasting Dashboard", layout="wide")
st.title("Supply Chain Forecasting & Operations Optimization")
DATA = Path(__file__).resolve().parents[1] / "data" / "processed" / "supply_chain_clean.csv"
df = pd.read_csv(DATA, parse_dates=["date"])
material = st.sidebar.selectbox("Material", sorted(df["material"].unique()))
view = df[df["material"] == material]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Demand", f"{view['material_demand'].sum():,.0f}")
col2.metric("Avg Production", f"{view['production_volume'].mean():,.1f}")
col3.metric("Avg Waste %", f"{view['waste_percent'].mean():.2f}%")
col4.metric("Avg Inventory DOH", f"{view['inventory_doh'].mean():.1f}")
st.line_chart(view.set_index("date")[["material_demand", "production_volume", "ending_inventory"]])
st.dataframe(view.tail(30), use_container_width=True)
