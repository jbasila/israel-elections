"""Sweep Arab turnout from 20% to 80% and write per-party and per-bloc seats to data/scenario_sweep.csv."""
import csv
import os

from arab_turnout_scenario import BLOCS, DATA, bloc_seats, scenario

TURNOUTS = [t / 2 for t in range(40, 161)] + [26.6, 53.2]

rows = []
for t in sorted(set(TURNOUTS)):
    votes, seats = scenario(t)
    blocs = bloc_seats(seats)
    rows.append({
        "arab_turnout_pct": t,
        "valid_votes": sum(votes.values()),
        **{p: seats[p] for p in BLOCS},
        **blocs,
        "Change + Arab": blocs["Change Coalition"] + blocs["Arab Parties"],
    })

with open(os.path.join(DATA, "scenario_sweep.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"wrote {len(rows)} rows")
