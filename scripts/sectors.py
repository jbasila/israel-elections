"""Classify every ballot box into a sector and aggregate registered voters, turnout and votes per sector.

Sectors:
  Druze           ballot boxes in Druze-majority localities (DRUZE_LOCALITIES)
  Arab            boxes in localities the CBS classifies as non-Jewish (religion code 2) or Bedouin tribes (3),
                  plus boxes elsewhere (mixed cities) where Arab-led lists won >= ARAB_BOX_SHARE of valid votes
  Haredi          boxes in Jewish/mixed localities where Haredi lists won >= HAREDI_BOX_SHARE of valid votes
  Jewish (other)  all remaining boxes
  Double envelope soldiers, diplomats, hospital/prison voters etc.; counted centrally and not tied to a box

Usage: python3 scripts/sectors.py [knesset ...]   -> writes data/sector_turnout.csv and data/sector_votes.csv
"""
import csv
import gzip
import os
import sys
from collections import defaultdict

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
RAW = os.path.join(DATA, "raw")

ARAB_BOX_SHARE = 0.5
HAREDI_BOX_SHARE = 0.75

ELECTIONS = {
    # knesset: (date, Arab-led list letters, Haredi list letters)
    19: ("2013-01-22", ("עם", "ו", "ד"), ("ג", "שס")),
    20: ("2015-03-17", ("ודעם",), ("ג", "שס")),
    21: ("2019-04-09", ("ום", "דעם"), ("ג", "שס")),
    22: ("2019-09-17", ("ודעם",), ("ג", "שס")),
    23: ("2020-03-02", ("ודעם",), ("ג", "שס")),
    24: ("2021-03-23", ("ודעם", "עם"), ("ג", "שס")),
    25: ("2022-11-01", ("עם", "ום", "ד"), ("ג", "שס")),
    26: ("2026-10-27", ("ודם", "עם"), ("ג", "שס", "זך")),
}

# CBS locality codes of Druze-majority localities (Galilee, Carmel, Golan).
DRUZE_LOCALITIES = {480, 481, 485, 494, 496, 502, 525, 534, 536, 546, 1295, 1296, 4001, 4201, 4203, 4502}
DOUBLE_ENVELOPE = {875, 9999, 99999}
META = {"סמל ועדה", "ברזל", "שם ישוב", "סמל ישוב", "קלפי", "מספר קלפי", "ריכוז", "שופט",
        "בזב", "מצביעים", "פסולים", "כשרים", "חיצוניות", "קלפי אחרת"}
SECTORS = ("Arab", "Druze", "Haredi", "Jewish (other)", "Double envelope")


def num(x):
    return int(float(x)) if x not in (None, "") else 0


def cbs_religion():
    with gzip.open(os.path.join(RAW, "cbs_localities_2023.csv.gz"), "rt", encoding="utf-8") as f:
        return {int(r["סמל יישוב"]): r["דת יישוב"] for r in csv.DictReader(f)}


def ballots(knesset):
    with gzip.open(os.path.join(RAW, f"k{knesset}_ballots.csv.gz"), "rt", encoding="utf-8") as f:
        yield from csv.DictReader(f)


def classify(row, letters, religion, arab_lists, haredi_lists):
    code = num(row["סמל ישוב"])
    if code in DOUBLE_ENVELOPE:
        return "Double envelope"
    if code in DRUZE_LOCALITIES:
        return "Druze"
    if religion.get(code) in ("2", "3"):
        return "Arab"
    valid = num(row["כשרים"])
    if valid:
        if sum(num(row[l]) for l in arab_lists if l in letters) / valid >= ARAB_BOX_SHARE:
            return "Arab"
        if sum(num(row[l]) for l in haredi_lists if l in letters) / valid >= HAREDI_BOX_SHARE:
            return "Haredi"
    return "Jewish (other)"


def aggregate(knesset, religion=None):
    """Return ({sector: {registered, voters, valid}}, {sector: {letter: votes}})."""
    religion = religion or cbs_religion()
    _, arab_lists, haredi_lists = ELECTIONS[knesset]
    totals = {s: defaultdict(int) for s in SECTORS}
    votes = {s: defaultdict(int) for s in SECTORS}
    for row in ballots(knesset):
        letters = [c for c in row if c and c.strip() not in META]
        sector = classify(row, letters, religion, arab_lists, haredi_lists)
        totals[sector]["registered"] += num(row["בזב"])
        totals[sector]["voters"] += num(row["מצביעים"])
        totals[sector]["valid"] += num(row["כשרים"])
        for l in letters:
            votes[sector][l.strip()] += num(row[l])
    return totals, votes


if __name__ == "__main__":
    knessets = [int(k) for k in sys.argv[1:]] or list(ELECTIONS)
    religion = cbs_religion()
    turnout_rows, vote_rows = [], []
    for k in knessets:
        date, arab_lists, _ = ELECTIONS[k]
        totals, votes = aggregate(k, religion)
        registered = sum(t["registered"] for t in totals.values())
        voters = sum(t["voters"] for t in totals.values())
        print(f"K{k} {date}: registered {registered:,}, turnout {voters / registered:.2%}")
        for s in SECTORS:
            t = totals[s]
            arab_votes = sum(votes[s][l] for l in arab_lists)
            turnout_rows.append({
                "knesset": k, "date": date, "sector": s,
                "registered": t["registered"], "voters": t["voters"], "valid": t["valid"],
                "turnout_pct": round(100 * t["voters"] / t["registered"], 2) if t["registered"] else "",
                "arab_lists_share_pct": round(100 * arab_votes / t["valid"], 2) if t["valid"] else "",
            })
            print(f"   {s:16} reg {t['registered']:>9,}  voters {t['voters']:>9,}  "
                  f"turnout {turnout_rows[-1]['turnout_pct']!s:>6}%  Arab-list share {turnout_rows[-1]['arab_lists_share_pct']}%")
            for l, v in sorted(votes[s].items(), key=lambda x: -x[1]):
                if v:
                    vote_rows.append({"knesset": k, "sector": s, "letter": l, "votes": v})
    if not sys.argv[1:]:
        for name, rows in (("sector_turnout.csv", turnout_rows), ("sector_votes.csv", vote_rows)):
            with open(os.path.join(DATA, name), "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=rows[0].keys())
                w.writeheader()
                w.writerows(rows)
