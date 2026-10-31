"""Download official ballot-box results (Knesset 19-26) and the CBS locality file into data/raw/.

Sources:
  - Knesset 19-25: Central Elections Committee via data.gov.il datastore (dataset "votes-knesset")
  - Knesset 26:    Central Elections Committee, media26.bechirot.gov.il/files/expb.csv
  - Localities:    CBS "bycode2023" via data.gov.il datastore (dataset "localities-in-israel")
"""
import csv
import gzip
import io
import json
import os
import urllib.request

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
UA = {"User-Agent": "Mozilla/5.0"}

DATASTORE = {
    "k19_ballots": "432d3185-545a-41d9-8c72-d10ee515919c",
    "k20_ballots": "c3db5581-f48d-45fc-b221-e7635e940c41",
    "k21_ballots": "f79f9ba5-fe12-4b90-96cc-916f1b7c1c34",
    "k22_ballots": "22f3a195-3a79-436c-be23-cb606bc7b398",
    "k23_ballots": "3b9e911a-2e90-4587-b209-84171664056b",
    "k24_ballots": "419be3b0-fd30-455a-afc0-034ec36be990",
    "k25_ballots": "cc223336-07bc-485d-b160-62df92967c0a",
    "cbs_localities_2023": "d47a54ff-87f0-44b3-b33a-f284c0c38e5a",
}
DIRECT = {
    "k26_ballots": "https://media26.bechirot.gov.il/files/expb.csv",
}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()


def datastore(resource_id):
    rows, fields, offset = [], None, 0
    while True:
        url = f"https://data.gov.il/api/3/action/datastore_search?resource_id={resource_id}&limit=10000&offset={offset}"
        result = json.loads(get(url))["result"]
        fields = fields or [f["id"] for f in result["fields"] if f["id"] != "_id"]
        rows += result["records"]
        offset += len(result["records"])
        if not result["records"] or offset >= result["total"]:
            return fields, rows


def write(name, fields, rows):
    path = os.path.join(RAW, f"{name}.csv.gz")
    with gzip.open(path, "wt", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    for name, rid in DATASTORE.items():
        write(name, *datastore(rid))
    for name, url in DIRECT.items():
        reader = csv.DictReader(io.StringIO(get(url).decode("utf-8-sig")))
        rows = list(reader)
        write(name, [f for f in reader.fieldnames if f], rows)
