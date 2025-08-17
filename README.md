# Greenland Ice Sheet – GIS & Time‑Series Demo
Turning satellite data into maps & insights: Greenland mass balance (time-series) and elevation-change hotspots with Python, xarray & Geo tools.
![Elevation change](figures/elevation_change_map.png)
![Hotspots](figures/elevation_hotspots.png)
Turning satellite data into maps & insights: Greenland mass balance (time-series) with trend & 95% CI, plus elevation-change hotspots (if ICESat data provided).

![Mass balance](figures/mass_balance_timeseries.png)
![STL trend](figures/mass_balance_trend_stl.png)

![Build](https://github.com/TomCorbett22/greenland-ice-sheet-gis-analysis/actions/workflows/build.yml/badge.svg)

Quickstart:

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/pipeline.py
```
