"""Sweep Arab turnout (20-90%) x Haredi turnout (60-95%) and write seats per list and bloc to data/scenario_grid.csv."""
import csv
import os

from scenario import BLOCS, DATA, bloc_seats, scenario

rows = []
for haredi in range(60, 96):
    for arab in range(20, 91):
        votes, seats = scenario({"Arab": arab, "Haredi": haredi})
        blocs = bloc_seats(seats)
        rows.append({
            "arab_turnout_pct": arab,
            "haredi_turnout_pct": haredi,
            "valid_votes": sum(votes.values()),
            **{p: seats[p] for p in BLOCS},
            **blocs,
        })

with open(os.path.join(DATA, "scenario_grid.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows")
