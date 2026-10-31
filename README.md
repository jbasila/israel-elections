# The Arab Minority as a Pivotal Electorate: Turnout Counterfactuals for the 26th Knesset Election (2026)

## Abstract

In the 27 October 2026 election to the 26th Knesset, turnout among Arab citizens of Israel reached about 80%. That is roughly 27 percentage points above 2022 and, for the first time, above the national rate (77.97%). Arab-led lists won a record 19 of 120 seats. This study asks how much of the post-election balance of power depends on that turnout. We hold all other votes fixed, vary Arab-party votes in proportion to Arab turnout, and reapply Israel's seat-allocation rules: the 3.25% threshold, the Bader-Ofer (D'Hondt) method, and surplus-vote agreements. We find that Arab turnout is the deciding factor for a governing majority. Above about 31%, neither the Extreme Right bloc nor the Change Coalition can reach 61 seats without the Arab parties. Below that level, the Extreme Right bloc gains a majority. The relationship is driven mainly by the electoral threshold and is strongly non-linear.

## 1. Research question

Two questions guide the study:

- How sensitive is the Knesset's bloc composition to Arab voter turnout?
- At what turnout levels does the balance of power change?

## 2. Data

All data is in [`data/`](data/). Fetched 2026-10-31.

| File | Contents |
|---|---|
| `knesset26_results.csv` | Votes and seats for all 36 competing lists |
| `knesset26_summary.csv` | Registered voters (7,331,981), valid votes (5,690,685), invalid votes (25,988), turnout, threshold |
| `knesset26_surplus_agreements.csv` | The five surplus-vote agreements in force |
| `knesset26_blocs.csv` | Assignment of each seat-winning list to a bloc |
| `knesset26_turnout_by_sector.csv` | Reported turnout by sector and locality |
| `scenario_sweep.csv` | Model output: seats per list and bloc for Arab turnout from 20% to 80% in 0.5-point steps |

**Bloc definitions.** The labels follow common Israeli political usage:

| Bloc | Lists | Actual seats |
|---|---|---|
| Extreme Right | Likud, Otzma Yehudit, Religious Zionism–Zehut, Shas, United Torah Judaism | 53 |
| Change Coalition | Yashar, Together, The Democrats, Yisrael Beiteinu | 48 |
| Arab Parties | Joint List, Ra'am | 19 |

## 3. Method

1. **Seat allocation** (`scripts/seats.py`). Lists below 3.25% of valid votes are excluded. Each pair of lists with a surplus agreement is treated as one unit, seats are allocated among units by D'Hondt, and each pair's seats are then split between its two lists by D'Hondt.
2. **Validation.** Applied to the actual 2026 votes, the model reproduces the official allocation exactly, list by list, for all 120 seats. Without surplus agreements it misallocates one seat (Ra'am 7 instead of 8, Shas 7 instead of 6), which confirms that the agreements must be modelled.
3. **Counterfactual** (`scripts/arab_turnout_scenario.py`). Joint List and Ra'am votes are multiplied by *T* / 80, where *T* is the hypothetical Arab turnout. All other lists keep their actual vote counts. Total valid votes, and therefore the threshold, are recomputed.
4. **Sweep** (`scripts/turnout_sweep.py`). Steps 1–3 are repeated for *T* from 20% to 80%.

## 4. Results

### 4.1 Selected scenarios

| Arab turnout | Extreme Right | Change Coalition | Arab Parties | Change + Arab | Majority |
|---|---|---|---|---|---|
| **80% (observed)** | 53 | 48 | 19 | 67 | None without Arab parties |
| 53.2% (2022 level) | 56 | 51 | 13 | 64 | None without Arab parties |
| 40% | 60 | 54 | 6 | 60 | Tied 60–60 |
| 30% | **61** | 55 | 4 | 59 | Extreme Right |
| 25% | **63** | 57 | 0 | 57 | Extreme Right |

### 4.2 Breakpoints

| Arab turnout | Event |
|---|---|
| < 27% | Joint List falls below the threshold; no Arab representation |
| < 31% | The Extreme Right bloc reaches 61 or more seats |
| 31% – 40.5% | 60–60 deadlock |
| < 41% | Ra'am falls below the threshold |
| ≥ 79.5% | The observed outcome (53 / 48 / 19) |

### 4.3 Findings

1. **The Arab electorate is decisive.** At every turnout above about 31%, the Arab parties hold seats that neither bloc can do without: the Change Coalition can reach 61 only with them, and the Extreme Right is held to 60 or fewer.
2. **The Change Coalition cannot form a majority by itself.** Its maximum in any scenario is 57 seats, reached when the Arab parties are wiped out entirely.
3. **The threshold makes the effect non-linear.** Between 80% and 41% turnout, the Extreme Right gains one seat for roughly every 7–8 points of lost Arab turnout (53 → 58). When Ra'am drops below the threshold at 41%, two seats move to the Extreme Right at once (58 → 60), as its votes no longer count toward any seat.
4. **Small margins decide the outcome.** At 26.6% turnout (half the 2022 rate), the Joint List misses the threshold by 482 votes. Arab representation then falls from 4 seats to 0, and the Extreme Right goes from 61 to 63.
5. **The 2026 rise in turnout cost the Extreme Right three seats** compared with a repeat of 2022 turnout (56 → 53). This alone did not decide the election, since 56 is also short of a majority.

## 5. Limitations

- **Party vote is used as a proxy for sector vote.** The model treats all Joint List and Ra'am votes as Arab votes, and all Arab votes as going to them. In practice, a share of Arab voters (historically around 10–15%) choose Jewish-led lists, and a small number of Jewish voters choose Arab-led lists. Both effects are ignored.
- **Uniform scaling.** The model assumes that lower turnout reduces both Arab parties by the same proportion. In reality, turnout differs by region and community (for example, Negev Bedouin versus the Triangle and the Galilee), and the two parties draw on these communities differently.
- **No behavioural response.** All other parties' votes are held fixed. In reality, mobilisation in one sector tends to produce counter-mobilisation in another.
- **The turnout baseline is an estimate.** The 80% Arab turnout figure comes from press reports, and no official sector breakdown has been published. Published estimates range from 75% to 80%. Using a 75% baseline would shift every breakpoint upward.
- **The results are not yet certified.** The Central Elections Committee certifies the results on 4 November 2026, and the data should be refreshed then.
- **Bloc membership is a modelling choice.** Bloc assignments reflect common usage, not formal coalition commitments. They can be changed in `data/knesset26_blocs.csv`.

## 6. Reproducing

```sh
python3 scripts/seats.py data/knesset26_results.csv      # seat allocation without surplus agreements
python3 scripts/arab_turnout_scenario.py 53.2            # single scenario
python3 scripts/turnout_sweep.py                         # regenerate data/scenario_sweep.csv
```

Requires Python 3 with the standard library only.

## 7. Sources

**Results**
- Central Elections Committee, via [Wikipedia: 2026 Israeli legislative election](https://en.wikipedia.org/wiki/2026_Israeli_legislative_election)

**Surplus-vote agreements**
- [JPost: Hadash-Ta'al and Ra'am](https://www.jpost.com/israel-election-2026/article-908431)
- [JPost: Bennett-Liberman and Eisenkot-Golan](https://www.jpost.com/israel-election-2026/article-908296)
- [JPost: Shas and UTJ](https://www.jpost.com/israel-election-2026/article-911320)
- [JPost: Likud and RZP](https://www.jpost.com/israel-election-2026/article-910758)
- [Times of Israel](https://www.timesofisrael.com/main-opposition-factions-ink-surplus-vote-deals-in-bid-to-maximize-knesset-representation/)

**2026 turnout**
- [JPost](https://www.jpost.com/israel-election-2026/article-913061)
- [JNS](https://www.jns.org/analysis/decoding-israels-vote-electorate-divided-netanyahu-resilient-arabs-rising)
- [Washington Times](https://www.washingtontimes.com/news/2026/oct/30/netanyahus-party-calls-record-arab-turnout-islamization-israel/)
- [Mideast Journal](https://www.mideastjournal.org/post/israel-election-results-2026-netanyahu-coalition)
- [Ynet](https://www.ynetnews.com/article/bknat9r3ge)

**2022 Arab turnout (53.2%)**
- [Reichman University, IPS](https://www.runi.ac.il/en/research-institutes/government/ips/activities/newsletter/milshtein24-11-22e)
- [INSS](https://www.inss.org.il/publication/elections-2022-arab-society/)
