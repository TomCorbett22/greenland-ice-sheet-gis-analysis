from pathlib import Path
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw" / "icesat"
FIG = BASE / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# Open your ATL15 file (you already copied/renamed it)
nc = RAW / "greenland_elev_change.nc"
ds = xr.open_dataset(nc)

# Try to find a sensible dh/dt variable name
candidates = ["dhdt", "elevation_change", "dz", "rate"]
for name in ds.data_vars:
    if name.lower() in candidates:
        var = name
        break
else:
    var = list(ds.data_vars)[0]  # fallback: first data variable

da = ds[var].squeeze(drop=True)

# Compute hotspots = top/bottom deciles
q_lo = float(da.quantile(0.10))
q_hi = float(da.quantile(0.90))
mask = xr.where((da <= q_lo) | (da >= q_hi), 1, 0)

# Plot & save
plt.figure(figsize=(7,5))
mask.plot()
plt.title("Hotspots (top/bottom deciles)")
plt.tight_layout()
out = FIG / "elevation_hotspots.png"
plt.savefig(out, dpi=220)
plt.close()
print("Wrote:", out)
