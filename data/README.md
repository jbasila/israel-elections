# Data

See the [root README](../README.md) §2 for what each file is and where it came from.

- `raw/`: official CEC and CBS data as downloaded by `scripts/fetch_data.py` (gzipped CSV, unmodified).
- `knesset26_turnout_by_sector.csv`: election-night **press** estimates, kept for comparison. The measured figures are in `sector_turnout.csv`.
- Results are not certified until 2026-11-04. Rerun the pipeline after that date.
