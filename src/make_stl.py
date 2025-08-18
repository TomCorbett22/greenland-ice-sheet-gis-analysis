from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL

BASE = Path(__file__).resolve().parents[1]
proc = BASE / "data" / "processed" / "mass_anomaly.csv"
out = BASE / "figures" / "mass_balance_trend_stl.png"

df = pd.read_csv(proc, parse_dates=["date"])
s = df.set_index("date")["mass_anomaly_gt"].asfreq("MS").interpolate()

res = STL(s, period=12, robust=True).fit()

plt.figure(figsize=(8,3))
plt.plot(res.trend.index, res.trend.values)
plt.title("STL trend (monthly)")
plt.tight_layout()
plt.savefig(out, dpi=220)
print("Wrote:", out)
