import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
PROC = BASE / "data" / "processed"
FIG = BASE / "figures"

st.set_page_config(page_title="Greenland Ice Sheet Demo", layout="wide")
st.title("Greenland Ice Sheet – GIS & Time‑Series Demo")

csv_path = PROC / "mass_anomaly.csv"
npy_path = PROC / "elevation_change.npy"

if csv_path.exists():
    df = pd.read_csv(csv_path, parse_dates=["date"]).sort_values("date")
else:
    # generate quick demo if missing
    dates = pd.date_range("2002-01-01", "2024-12-31", freq="MS")
    n = len(dates)
    trend = np.linspace(0, -3500, n)
    season = 80 * np.sin(2*np.pi*np.arange(n)/12)
    noise = np.random.normal(0, 40, n)
    mass = trend + season + noise
    df = pd.DataFrame({"date": dates, "mass_anomaly_gt": mass})

st.subheader("Mass Balance Time Series (Synthetic)")
fig = plt.figure(figsize=(8,3))
plt.plot(df["date"], df["mass_anomaly_gt"], label="Monthly")
annual = df.groupby(df["date"].dt.year)["mass_anomaly_gt"].mean()
plt.plot(pd.to_datetime(annual.index, format="%Y"), annual.values, label="Annual mean")
plt.legend()
plt.tight_layout()
st.pyplot(fig)

if npy_path.exists():
    arr = np.load(npy_path)
    st.subheader("Elevation Change Map (Synthetic)")
    st.image(str(FIG / "elevation_change_map.png"), caption="Synthetic dh/dt map (not georeferenced)")
else:
    st.info("Run: python src/pipeline.py to generate demo data & figures.")
