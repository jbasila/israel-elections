# The Arab Minority as a Pivotal Electorate: Turnout and Power in the 26th Knesset (2026)

**[Interactive explorer](https://jbasila.github.io/israel-elections/)**: move each sector's turnout and watch the 120 seats reallocate.

## Abstract

In the 27 October 2026 election to the 26th Knesset, Arab citizens of Israel voted at **78.4%**. That was a 25-point jump from 2022, the highest rate in at least eight elections, and above the national rate of 77.97%. Arab-led lists won a record 19 of 120 seats. Using official results for each ballot box, we measure turnout in every sector for all eight Knesset elections between 2013 and 2026. We then feed that measured electorate into a seat model that reproduces the official allocation exactly, and use it to ask a counterfactual question: how much of today's Knesset depends on who turned out?

Arab turnout is the decisive variable. Above about 31% Arab turnout, neither the Extreme Right bloc nor the Change Coalition can reach 61 seats without the Arab parties. Below that level, the Extreme Right gains a majority. Haredi turnout, by contrast, has almost no leverage. Raising it from 74% to 90% moves the Extreme Right only from 53 to 55 seats, because that electorate is small and already highly mobilized.

## 1. Research questions

1. What was the actual turnout in each sector, and how does 2026 compare with 2013–2022?
2. How sensitive is the Knesset's bloc composition to Arab turnout?
3. Could higher Haredi mobilization have offset the Arab surge?

## 2. Data

All official data is downloaded by `scripts/fetch_data.py` into [`data/raw/`](data/raw/).

| Source | Content |
|---|---|
| Central Elections Committee (CEC), Knesset 19–25, via [data.gov.il](https://data.gov.il/dataset/votes-knesset) | Results for each ballot box, 2013–2022 |
| CEC, Knesset 26 (`media26.bechirot.gov.il/files/expb.csv`) | Results for each ballot box, 2026 (12,926 boxes) |
| Central Bureau of Statistics (CBS), via [data.gov.il](https://data.gov.il/dataset/localities-in-israel) | Locality file (2023), with each locality's religion classification |
| Press (JPost, Times of Israel) | 2026 surplus-vote agreements |

The 2026 ballot-box file sums exactly to the national totals: 5,690,685 valid votes, with every list's total matching.

### Derived files ([`data/`](data/))

| File | Contents |
|---|---|
| `knesset26_results.csv` | Votes and seats for each list, 2026 |
| `knesset26_letters.csv` | Ballot letter → list name, 2026 |
| `knesset26_surplus_agreements.csv` | The five surplus-vote agreements |
| `knesset26_blocs.csv` | Bloc assignment of each seat-winning list |
| `sector_turnout.csv` | Registered voters, voters, valid votes, turnout and Arab-list share per sector, 2013–2026 |
| `sector_votes.csv` | Votes per ballot letter per sector, 2013–2026 |
| `history.csv` | One row per election: turnout by sector, Arab-list vote share and seats |
| `arab_list_seats.csv` | Seats won by Arab-led lists per election |
| `scenario_grid.csv` | Model output: seats per list and bloc for every Arab turnout (20–90%) × Haredi turnout (60–95%) |

## 3. Method

### 3.1 Sector classification (`scripts/sectors.py`)

Every ballot box is assigned to one sector:

| Sector | Rule |
|---|---|
| Druze | Box in one of 16 Druze-majority localities (CBS codes listed in the script) |
| Arab | Box in a locality the CBS classifies as non-Jewish (religion code 2) or a Bedouin tribe (code 3); **or**, in Jewish or mixed localities, a box where Arab-led lists won ≥ 50% of valid votes (this captures Arab neighbourhoods of Haifa, Jaffa, Lod, Ramla and Acre) |
| Haredi | Box in a Jewish or mixed locality where Haredi lists (UTJ, Shas, and in 2026 Haredi Public) won ≥ 75% of valid votes |
| Jewish (other) | All remaining boxes |
| Double envelope | Soldiers, diplomats, and hospital and prison voters, counted centrally and not tied to any box |

Sector turnout is voters ÷ registered voters at the sector's ballot boxes.

**Validation.** Our measured Arab turnout is within about one point of every published figure:

| Election | 2013 | 2015 | 2019a | 2019b | 2020 | 2021 | 2022 |
|---|---|---|---|---|---|---|---|
| Published | 56.5 | 63.5 | 49.2 | 59.2 | 64.8 | 44.6 | 53.2 |
| **Measured** | 55.9 | 63.5 | 48.2 | 58.8 | 64.5 | 43.9 | 52.9 |

**Haredi robustness.** The 75% cutoff defines a conservative core: 432k registered voters, capturing 45% of Haredi-list votes (many Shas voters are not Haredi). Measured Haredi turnout is stable at 74.0–74.3% for any cutoff from 50% to 90%.

### 3.2 Seat allocation (`scripts/seats.py`)

Lists below 3.25% of valid votes are excluded. Lists with a surplus agreement are paired; seats are allocated among units by D'Hondt and then split within each pair by D'Hondt. Applied to the actual votes, the model reproduces the official 2026 allocation exactly, list by list. Without the surplus agreements it misallocates one seat.

### 3.3 Counterfactual (`scripts/scenario.py`)

For a target turnout *T* in sector *S*, **every vote cast in S, for any list**, is multiplied by *T* ÷ measured turnout. Other sectors and double-envelope votes are unchanged, and the threshold is recomputed. This captures Arab votes for Jewish-led lists and the reverse. `scripts/turnout_sweep.py` runs the full Arab × Haredi grid. The interactive explorer reimplements the same model in JavaScript and matches the Python output on all 28,116 list × scenario cells.

## 4. Results

### 4.1 Turnout by sector, 2013–2026

| Election | National | Arab | Druze | Haredi (core) | Jewish (other)\* | Arab-led lists' seats |
|---|---|---|---|---|---|---|
| 2013 | 67.8 | 55.9 | 55.4 | 77.6 | 64.5 | 11 |
| 2015 | 72.3 | 63.5 | 55.7 | 78.8 | 68.8 | 13 |
| 2019a | 68.5 | 48.2 | 55.8 | 74.8 | 66.8 | 10 |
| 2019b | 69.9 | 58.8 | 53.1 | 75.7 | 66.0 | 13 |
| 2020 | 71.5 | 64.5 | 55.4 | 74.8 | 66.3 | 15 |
| 2021 | 67.4 | 43.9 | 45.7 | 70.9 | 63.4 | 10 |
| 2022 | 70.6 | 52.9 | 48.8 | 73.9 | 65.2 | 10 |
| **2026** | **78.0** | **78.4** | **62.0** | **74.3** | **70.6** | **19** |

\* The "Jewish (other)" figure counts only voters at home ballot stations, so it is understated: almost all of the 450k double-envelope voters in 2026 are Jewish, and including them would put this sector's turnout near 78%.

- **2026 broke the historical range.** Arab turnout had swung between 44% and 65% for a decade. In 2026 it rose 14 points above the previous peak and, for the first time on record, exceeded the national rate.
- **Arab voters also consolidated behind Arab-led lists:** 93.2% of the Arab-sector vote went to them, up from 83% in 2013 and 78% in April 2019.
- **The threshold, not only turnout, sets Arab representation.** In 2022, Arab-led lists won 10.7% of the national vote but only 10 seats, because Balad's 2.9% fell below the threshold and elected no one.
- **Haredi turnout is high and flat.** It has stayed between 71% and 79% in every election, with no 2026 surge.

### 4.2 Counterfactual: Arab turnout (Haredi held at the measured 74.3%)

| Arab turnout | Extreme Right | Change Coalition | Arab Parties | Outcome |
|---|---|---|---|---|
| ≥ 78% (observed 78.4%) | 53 | 48 | 19 | Change + Arab = 67 |
| 52.9% (2022 level) | 56 | 50 | 14 | No bloc reaches 61 alone |
| 43.9% (2021 low) | 56 | 52 | 12 | No bloc reaches 61 alone |
| 31 – 36% | 60 | 54 | 6 | **60–60 deadlock** (Ra'am below threshold) |
| 24.5 – 30.5% | **61** | 54 | 5 | Extreme Right majority |
| 20% | **62** | 54 | 4 | Extreme Right majority |

### 4.3 Counterfactual: Haredi turnout (Arab held at the measured 78.4%)

| Haredi turnout | Extreme Right | Change Coalition | Arab Parties |
|---|---|---|---|
| 74.3% (observed) | 53 | 48 | 19 |
| 80% | 54 | 48 | 18 |
| 90% | 55 | 47 | 18 |
| 90%, with Arab turnout at the 2022 level | 56 | 50 | 14 |

The result holds with a broader Haredi definition (a 50% cutoff, covering 578k registered voters): 90% Haredi turnout still gives the Extreme Right only 55 seats.

### 4.4 Findings

1. **Arab turnout decides the majority.** At every Arab turnout above about 31%, the Arab parties hold seats that neither bloc can do without: the Change Coalition can reach 61 only with them, and the Extreme Right is held to 60 or fewer.
2. **The Change Coalition cannot win alone.** Its maximum in any scenario is 54 seats.
3. **The 2026 surge was worth 3 seats to each side of the 61 line.** Compared with 2022 turnout, it moved the Extreme Right from 56 to 53 and the Arab parties from 14 to 19. Even without the surge, though, the Extreme Right would have fallen short.
4. **Ra'am's threshold sets the critical point.** Below 36.5% Arab turnout Ra'am drops out, its votes elect no one, and the Extreme Right jumps from 58 to 60. The Joint List stays above the threshold even at 20%, because it also draws votes in mixed cities and from double envelopes.
5. **Haredi under-mobilization did not cost the Extreme Right the election.** At 74%, Haredi turnout is near its ceiling, and its electorate is about 40% the size of the Arab one. No realistic Haredi surge offsets an Arab surge.

## 5. Limitations

- **Ecological inference.** Sectors are defined by ballot boxes and localities, not by individuals. Jewish voters in Arab localities and Arab voters in Jewish-majority boxes are assigned to the wrong sector.
- **The Haredi core is conservative.** Haredi voters in mixed neighbourhoods (for example in Jerusalem or Beit Shemesh) fall into "Jewish (other)." The sensitivity check in §3.1 bounds this effect.
- **Uniform scaling.** A turnout change scales a sector's party mix proportionally. In practice, marginal voters may differ from habitual ones.
- **No behavioural response.** Each scenario holds the other sectors fixed. In reality, mobilisation in one sector tends to produce counter-mobilisation in another.
- **The results are not yet certified.** The CEC certifies the results on 4 November 2026; rerun `scripts/fetch_data.py` afterwards.
- **Some inputs are curated by hand.** The surplus agreements come from press reports. Arab-list seats before 2026 are recorded from published results. The bloc labels follow common usage and can be changed in `data/knesset26_blocs.csv`.

## 6. Reproducing

```sh
python3 scripts/fetch_data.py         # download raw CEC and CBS data into data/raw/
python3 scripts/sectors.py            # classify ballot boxes -> sector_turnout.csv, sector_votes.csv
python3 scripts/history.py            # -> history.csv
python3 scripts/scenario.py --arab 52.93 --haredi 90   # a single counterfactual
python3 scripts/turnout_sweep.py      # -> scenario_grid.csv
python3 scripts/build_explorer.py     # -> docs/index.html (interactive explorer)
```

Requires Python 3 with the standard library only.

## 7. Sources

- Central Elections Committee: results for each ballot box ([data.gov.il](https://data.gov.il/dataset/votes-knesset), [media26.bechirot.gov.il](https://media26.bechirot.gov.il/files/expb.csv))
- Central Bureau of Statistics: locality file ([data.gov.il](https://data.gov.il/dataset/localities-in-israel))
- [Wikipedia: 2026 Israeli legislative election](https://en.wikipedia.org/wiki/2026_Israeli_legislative_election)
- Surplus agreements: [JPost: Hadash-Ta'al and Ra'am](https://www.jpost.com/israel-election-2026/article-908431) · [JPost: Bennett-Liberman and Eisenkot-Golan](https://www.jpost.com/israel-election-2026/article-908296) · [JPost: Shas and UTJ](https://www.jpost.com/israel-election-2026/article-911320) · [JPost: Likud and RZP](https://www.jpost.com/israel-election-2026/article-910758) · [Times of Israel](https://www.timesofisrael.com/main-opposition-factions-ink-surplus-vote-deals-in-bid-to-maximize-knesset-representation/)
- Published Arab turnout for validation: [Reichman University, IPS](https://www.runi.ac.il/en/research-institutes/government/ips/activities/newsletter/milshtein24-11-22e) · [INSS](https://www.inss.org.il/publication/elections-2022-arab-society/) · [IDI](https://en.idi.org.il/articles/47986)
