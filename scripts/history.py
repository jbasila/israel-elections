"""Build data/history.csv: turnout per sector and Arab-list strength for every election 2013-2026."""
import csv
import os

DATA = os.path.join(os.path.dirname(__file__), "..", "data")

with open(os.path.join(DATA, "sector_turnout.csv")) as f:
    turnout = list(csv.DictReader(f))
with open(os.path.join(DATA, "arab_list_seats.csv")) as f:
    seats = {r["knesset"]: r for r in csv.DictReader(f)}

rows = []
for k in sorted({r["knesset"] for r in turnout}, key=int):
    sec = {r["sector"]: r for r in turnout if r["knesset"] == k}
    registered = sum(int(r["registered"]) for r in sec.values())
    voters = sum(int(r["voters"]) for r in sec.values())
    valid = sum(int(r["valid"]) for r in sec.values())
    arab_list_votes = sum(int(r["valid"]) * float(r["arab_lists_share_pct"] or 0) / 100 for r in sec.values())
    rows.append({
        "knesset": k,
        "date": seats[k]["date"],
        "national_turnout_pct": round(100 * voters / registered, 2),
        "arab_turnout_pct": sec["Arab"]["turnout_pct"],
        "druze_turnout_pct": sec["Druze"]["turnout_pct"],
        "haredi_turnout_pct": sec["Haredi"]["turnout_pct"],
        "jewish_other_turnout_pct": sec["Jewish (other)"]["turnout_pct"],
        "arab_share_of_electorate_pct": round(100 * int(sec["Arab"]["registered"]) / registered, 2),
        "arab_vote_to_arab_lists_pct": sec["Arab"]["arab_lists_share_pct"],
        "arab_lists_national_share_pct": round(100 * arab_list_votes / valid, 2),
        "arab_list_seats": seats[k]["arab_list_seats"],
    })

with open(os.path.join(DATA, "history.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(r)
