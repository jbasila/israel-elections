"""Inject model data into site/explorer.template.html.

Writes docs/explorer.html (page body, as published to claude.ai artifacts) and docs/index.html
(a full HTML document for GitHub Pages).
"""
import csv
import json
import os

from scenario import AGREEMENTS, BLOCS, MEASURED, PARTIES, SECTOR_VOTES

ROOT = os.path.join(os.path.dirname(__file__), "..")


def read_csv(name):
    with open(os.path.join(ROOT, "data", name)) as f:
        return list(csv.DictReader(f))


registered = {r["sector"]: int(r["registered"]) for r in read_csv("sector_turnout.csv") if r["knesset"] == "26"}
seats = {r["knesset"]: r for r in read_csv("arab_list_seats.csv")}
history = [{
    "knesset": r["knesset"], "date": r["date"],
    "arab": float(r["arab_turnout_pct"]), "haredi": float(r["haredi_turnout_pct"]),
    "jewish": float(r["jewish_other_turnout_pct"]), "seats": int(r["arab_list_seats"]),
    "lists": seats[r["knesset"]]["lists"],
} for r in read_csv("history.csv")]

data = {
    "parties": PARTIES,
    "sectorVotes": SECTOR_VOTES,
    "measured": MEASURED,
    "registered": registered,
    "agreements": AGREEMENTS,
    "blocs": BLOCS,
    "history": history,
}

with open(os.path.join(ROOT, "site", "explorer.template.html")) as f:
    page = f.read().replace("__DATA__", json.dumps(data, ensure_ascii=False))
os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
with open(os.path.join(ROOT, "docs", "explorer.html"), "w") as f:
    f.write(page)
with open(os.path.join(ROOT, "docs", "index.html"), "w") as f:
    f.write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            "</head>\n<body>\n" + page + "\n</body>\n</html>\n")
print("wrote docs/explorer.html and docs/index.html")
