"""Knesset seat allocation: 3.25% threshold, then Bader-Ofer (D'Hondt), optionally with surplus agreements."""
import csv
import sys

SEATS = 120
THRESHOLD = 0.0325


def dhondt(votes, seats):
    alloc = {p: 0 for p in votes}
    for _ in range(seats):
        p = max(votes, key=lambda p: votes[p] / (alloc[p] + 1))
        alloc[p] += 1
    return alloc


def allocate(votes, agreements=()):
    total = sum(votes.values())
    passed = {p: v for p, v in votes.items() if v >= THRESHOLD * total}
    # Pair lists under surplus agreements (only if both passed), allocate pairs as blocs.
    blocs, members = {}, {}
    paired = set()
    for a, b in agreements:
        if a in passed and b in passed:
            blocs[(a, b)] = passed[a] + passed[b]
            members[(a, b)] = (a, b)
            paired |= {a, b}
    for p, v in passed.items():
        if p not in paired:
            blocs[(p,)] = v
            members[(p,)] = (p,)
    bloc_seats = dhondt(blocs, SEATS)
    result = {p: 0 for p in votes}
    for bloc, n in bloc_seats.items():
        result.update(dhondt({p: passed[p] for p in members[bloc]}, n))
    return result


def load(path):
    with open(path) as f:
        return {r["party"]: int(r["votes"]) for r in csv.DictReader(f)}


if __name__ == "__main__":
    votes = load(sys.argv[1])
    for p, s in allocate(votes).items():
        if s:
            print(f"{p:30} {s}")
