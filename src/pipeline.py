from pathlib import Path
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
PROC = BASE / "data" / "processed"
FIG = BASE / "figures"
PROC.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

def make_demo_data():
    dates = pd.date_range("2002-01-01", "2024-12-31", freq="MS")
    n = len(dates)
    trend = np.linspace(0, -3500, n)
    season = 80 * np.sin(2*np.pi*np.arange(n)/12)
    noise = np.random.normal(0, 40, n)
    mass = trend + season + noise
    df = pd.DataFrame({"date": dates, "mass_anomaly_gt": mass})
    df.to_csv(PROC / "mass_anomaly.csv", index=False)

    ny, nx = 220, 220
    y, x = np.mgrid[-1:1:complex(0,ny), -1:1:complex(0,nx)]
    base = -2.5*(1 - (x**2 + y**2))
    hotspot1 = -1.2 * np.exp(-((x-0.7)**2 + (y+0.5)**2)/0.02)
    hotspot2 = -0.9 * np.exp(-((x+0.6)**2 + (y-0.6)**2)/0.03)
    dhdt = base + hotspot1 + hotspot2 + 0.15*np.random.normal(size=(ny,nx))
    np.save(PROC / "elevation_change.npy", dhdt)

def make_figures():
    import pandas as pd, numpy as np
    df = pd.read_csv(PROC / "mass_anomaly.csv", parse_dates=["date"]).sort_values("date")
    annual = df.groupby(df["date"].dt.year)["mass_anomaly_gt"].mean()
    plt.figure(figsize=(8,4))
    plt.plot(df["date"], df["mass_anomaly_gt"], label="Monthly")
    plt.plot(pd.to_datetime(annual.index, format="%Y"), annual.values, label="Annual mean")
    plt.title("Greenland Mass Anomaly (Synthetic)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG / "mass_balance_timeseries.png", dpi=220)
    plt.close()

    arr = np.load(PROC / "elevation_change.npy")
    plt.figure(figsize=(5,4))
    plt.imshow(arr, origin="lower")
    plt.title("Synthetic Elevation Change (dh/dt)")
    plt.tight_layout()
    plt.savefig(FIG / "elevation_change_map.png", dpi=200)
    plt.close()

if __name__ == "__main__":
    make_demo_data()
    make_figures()
    print("Wrote figures to:", FIG)
