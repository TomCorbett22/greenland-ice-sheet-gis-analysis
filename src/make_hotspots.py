from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

# Optional: fall back to netCDF4 to discover nested groups
try:
    from netCDF4 import Dataset as NC
except Exception:
    NC = None

BASE = Path(__file__).resolve().parents[1]
NC_PATH = BASE / "data" / "raw" / "icesat" / "greenland_elev_change.nc"
OUT = BASE / "figures" / "elevation_hotspots.png"

CAND_DIM_NAMES = {"x", "y", "lon", "lat", "xc", "yc", "nx", "ny", "xgrid", "ygrid"}
CAND_VAR_HINTS = ("dh", "dhdt", "elev", "height", "dz", "rate", "change")

def find_group_and_var(nc_path: Path):
    """
    Return (group_path, var_name) inside the NetCDF that looks like a 2D dh/dt
    grid. Works even when variables are in nested groups.
    """
    # First try root with xarray
    try:
        ds = xr.open_dataset(nc_path)
        if len(ds.data_vars):
            for v in ds.data_vars:
                name = v.lower()
                if any(k in name for k in CAND_VAR_HINTS):
                    return ("", v)
            # fallback to first var if present
            v = list(ds.data_vars)[0]
            return ("", v)
    except Exception:
        pass

    # Otherwise, scan groups with netCDF4
    if NC is None:
        raise RuntimeError("netCDF4 not installed and dataset has no root variables.")

    best = None  # (score, group_path, var_name, shape)
    def walk(grp, path=""):
        nonlocal best
        # score variables
        for vname, var in grp.variables.items():
            dims = tuple(d.lower() for d in var.dimensions)
            rank = len(var.shape)
            # prefer 2D (or 3D with a trivial band dimension)
            if rank >= 2:
                has_space_dims = any(d in CAND_DIM_NAMES for d in dims)
                name_score = 1000 if any(h in vname.lower() for h in CAND_VAR_HINTS) else 0
                area = int(np.prod(var.shape[-2:])) if rank >= 2 else 0
                score = name_score + (500 if has_space_dims else 0) + area
                cand = (score, path, vname, var.shape)
                if (best is None) or (cand[0] > best[0]):
                    best = cand
        # recurse
        for gname, sub in grp.groups.items():
            walk(sub, f"{path}/{gname}" if path else gname)

    root = NC(nc_path.as_posix(), "r")
    walk(root)
    root.close()

    if best is None:
        raise RuntimeError("Could not find a suitable variable in any group.")
    _, group_path, var_name, _ = best
    return (group_path, var_name)

def main():
    # Find the best group/var
    group, var = find_group_and_var(NC_PATH)

    # Open with xarray at the chosen group (engine h5netcdf is robust for HDF5)
    if group:
        ds = xr.open_dataset(NC_PATH, engine="h5netcdf", group=group)
    else:
        try:
            ds = xr.open_dataset(NC_PATH)
        except Exception:
            ds = xr.open_dataset(NC_PATH, engine="h5netcdf")

    da = ds[var].squeeze(drop=True)

    # Compute hotspots = top/bottom deciles
    q_lo = float(da.quantile(0.10))
    q_hi = float(da.quantile(0.90))
    mask = xr.where((da <= q_lo) | (da >= q_hi), 1, 0)

    # Plot & save
    plt.figure(figsize=(7,5))
    mask.plot()
    title = f"Hotspots (top/bottom deciles)\nGroup: {group or '/'}  Var: {var}"
    plt.title(title)
    plt.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, dpi=220)
    plt.close()
    print("Wrote:", OUT)

if __name__ == "__main__":
    main()
