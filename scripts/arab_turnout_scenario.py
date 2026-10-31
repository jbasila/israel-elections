"""Counterfactual: seat allocation if Arab turnout had been X% instead of the observed ~80%.

Arab-party votes are scaled by X / 80; all other lists' votes are held fixed.
Usage: python3 scripts/arab_turnout_scenario.py [turnout_pct]   (default 53.2, the 2022 level)
"""
import csv
import os
import sys

from seats import allocate, load

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
ARAB_PARTIES = ("Joint List", "Ra'am")
ACTUAL_TURNOUT = 80.0


def read_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


VOTES = load(os.path.join(DATA, "knesset26_results.csv"))
AGREEMENTS = [(r["party_a"], r["party_b"]) for r in read_csv("knesset26_surplus_agreements.csv")]
BLOCS = {r["party"]: r["bloc"] for r in read_csv("knesset26_blocs.csv")}


def scenario(turnout):
    votes = dict(VOTES)
    for p in ARAB_PARTIES:
        votes[p] = round(VOTES[p] * turnout / ACTUAL_TURNOUT)
    return votes, allocate(votes, AGREEMENTS)


def bloc_seats(seats):
    totals = dict.fromkeys(BLOCS.values(), 0)
    for p, b in BLOCS.items():
        totals[b] += seats[p]
    return totals


if __name__ == "__main__":
    turnout = float(sys.argv[1]) if len(sys.argv) > 1 else 53.2
    _, actual = scenario(ACTUAL_TURNOUT)
    votes, seats = scenario(turnout)
    total = sum(votes.values())
    print(f"Arab turnout {ACTUAL_TURNOUT}% -> {turnout}%; valid votes {sum(VOTES.values()):,} -> {total:,}; threshold {0.0325 * total:,.0f}")
    print(f"{'party':30} {'votes':>10} {'actual':>7} {'scen':>5} {'diff':>5}")
    for p in votes:
        if actual[p] or seats[p]:
            print(f"{p:30} {votes[p]:>10,} {actual[p]:>7} {seats[p]:>5} {seats[p] - actual[p]:>+5}")
    print()
    print(f"{'bloc':30} {'actual':>7} {'scen':>5} {'diff':>5}")
    a, s = bloc_seats(actual), bloc_seats(seats)
    for b in a:
        print(f"{b:30} {a[b]:>7} {s[b]:>5} {s[b] - a[b]:>+5}")
