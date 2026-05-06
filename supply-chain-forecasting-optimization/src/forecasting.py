from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

DATA = Path(__file__).resolve().parents[1] / "data" / "processed" / "supply_chain_clean.csv"
REPORT = Path(__file__).resolve().parents[1] / "reports" / "forecast_results.csv"

def train_forecast(material="Pulp_A"):
    df = pd.read_csv(DATA, parse_dates=["date"])
    df = df[df["material"] == material].sort_values("date")
    features = ["production_volume", "ending_inventory", "waste_percent", "month", "week", "day_of_week"]
    target = "material_demand"
    split = int(len(df) * 0.8)
    train, test = df.iloc[:split], df.iloc[split:]
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(train[features], train[target])
    pred = model.predict(test[features])
    out = test[["date", "material", target]].copy()
    out["forecast"] = pred.round(2)
    out["absolute_error"] = (out[target] - out["forecast"]).abs().round(2)
    rmse = np.sqrt(mean_squared_error(out[target], out["forecast"]))
    mae = mean_absolute_error(out[target], out["forecast"])
    print(f"Material: {material} | MAE: {mae:.2f} | RMSE: {rmse:.2f}")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(REPORT, index=False)
    return out

if __name__ == "__main__":
    train_forecast()
