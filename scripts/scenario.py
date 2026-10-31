"""Counterfactual seat allocation for the 26th Knesset under different sector turnouts.

Every vote cast in a sector (for any list) is scaled by target / measured turnout; other sectors and
double-envelope votes are unchanged. Measured turnouts come from data/sector_turnout.csv.

Usage: python3 scripts/scenario.py [--arab PCT] [--haredi PCT] [--druze PCT] [--jewish PCT]
"""
import argparse
import csv
import os
from collections import defaultdict

from seats import allocate

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
KNESSET = "26"
FLAGS = {"arab": "Arab", "haredi": "Haredi", "druze": "Druze", "jewish": "Jewish (other)"}


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


LETTERS = {r["letter"]: r["party"] for r in read_csv("knesset26_letters.csv")}
AGREEMENTS = [(r["party_a"], r["party_b"]) for r in read_csv("knesset26_surplus_agreements.csv")]
BLOCS = {r["party"]: r["bloc"] for r in read_csv("knesset26_blocs.csv")}
MEASURED = {r["sector"]: float(r["turnout_pct"]) for r in read_csv("sector_turnout.csv")
            if r["knesset"] == KNESSET and r["turnout_pct"]}
SECTOR_VOTES = defaultdict(dict)
for r in read_csv("sector_votes.csv"):
    if r["knesset"] == KNESSET:
        SECTOR_VOTES[r["sector"]][LETTERS[r["letter"]]] = int(r["votes"])
PARTIES = [r["party"] for r in read_csv("knesset26_results.csv")]


def scenario(turnouts=None):
    """turnouts: {sector: pct}. Returns (votes per party, seats per party)."""
    turnouts = turnouts or {}
    votes = dict.fromkeys(PARTIES, 0)
    for sector, party_votes in SECTOR_VOTES.items():
        factor = turnouts[sector] / MEASURED[sector] if sector in turnouts else 1
        for p, v in party_votes.items():
            votes[p] += v * factor
    votes = {p: round(v) for p, v in votes.items()}
    return votes, allocate(votes, AGREEMENTS)


def bloc_seats(seats):
    totals = dict.fromkeys(BLOCS.values(), 0)
    for p, b in BLOCS.items():
        totals[b] += seats[p]
    return totals


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    for flag, sector in FLAGS.items():
        ap.add_argument(f"--{flag}", type=float, help=f"{sector} turnout %% (measured {MEASURED[sector]})")
    args = ap.parse_args()
    turnouts = {FLAGS[f]: v for f, v in vars(args).items() if v is not None}

    base_votes, actual = scenario()
    votes, seats = scenario(turnouts)
    total = sum(votes.values())
    print("Turnout: " + ", ".join(f"{s} {MEASURED[s]}% -> {t}%" for s, t in turnouts.items()) if turnouts else "Baseline")
    print(f"Valid votes {sum(base_votes.values()):,} -> {total:,}; threshold {0.0325 * total:,.0f}")
    print(f"{'party':30} {'votes':>10} {'actual':>7} {'scen':>5} {'diff':>5}")
    for p in PARTIES:
        if actual[p] or seats[p]:
            print(f"{p:30} {votes[p]:>10,} {actual[p]:>7} {seats[p]:>5} {seats[p] - actual[p]:>+5}")
    print()
    print(f"{'bloc':30} {'actual':>7} {'scen':>5} {'diff':>5}")
    a, s = bloc_seats(actual), bloc_seats(seats)
    for b in a:
        print(f"{b:30} {a[b]:>7} {s[b]:>5} {s[b] - a[b]:>+5}")
