# data/: official source data (Phase 2 test menu)

| File | What | Source | How obtained | Fetched |
|---|---|---|---|---|
| `who_edl5.csv` | All 234 recommendations of the electronic EDL (39 Non-laboratory, 195 Laboratory) | WHO e-EDL, https://edl.who-healthtechnologies.org (site states: "Fifth WHO model list of essential in vitro diagnostics (EDL 5)", © WHO 2025) | One `curl` per id listed on the home page (ids 1–234), parsed by `tools/who_edl.py` | 2026-11-02 |
| `who_edl4_tier1.csv` | EDL 4 Tier I (Section I.a and I.b: community settings and health facilities without laboratories), 39 rows | WHO TRS 1053 (2023), ISBN 9789240081093, https://iris.who.int/handle/10665/373322, pp. 127–146. PDF sha256 `6ca9bc6e…9089923` | Hand transcription from `pdftotext -layout` output; `edl5_ids` maps each row to the e-EDL | 2026-11-02 |
| `who_ghe2021_top10_deaths.csv` | Top 10 causes of death in 2021, low-income and lower-middle-income (World Bank groups) | WHO World health statistics 2024, Figure 1.9, p. 14, https://iris.who.int/handle/10665/376869 (its source is WHO Global Health Estimates 2021). PDF sha256 `f7b08734…1d3c3555` | Read from the figure's 2021 column; text extraction and the rendered page agree | 2026-11-02 |
| `test_menu.csv` | Our menu: condition × EDL 5 id × pod method. **Draft** | Derived from the three files above | Hand-built; checked by `tests/test_test_menu_data.py` | 2026-11-02 |

Fields are copied verbatim (tags stripped, whitespace collapsed). One typo comes from the source:
EDL 5 id 13 says "withotu".

`who_edl5.csv` keeps only the first EDL-edition reference found in each SAGE IVD recommendation
(`sage_section`), so many rows leave it empty. Use `setting` and `tiered_testing_service` instead.

## Refetch
```bash
curl -sSL https://edl.who-healthtechnologies.org/ -o home.html
grep -oE 'recommendations/[0-9]+"' home.html | grep -oE '[0-9]+' | sort -un > ids.txt
mkdir -p recs && for i in $(cat ids.txt); do curl -sSL https://edl.who-healthtechnologies.org/recommendations/$i -o recs/$i.html; sleep 0.3; done
python3 -I tools/who_edl.py recs data/who_edl5.csv
```
Keep downloads outside the repo. If the list changed, `tests/test_test_menu_data.py` fails until
the counts and mappings are reviewed.

## Licence
Both WHO EDL editions and WHS 2024 are released under **CC BY-NC-SA 3.0 IGO**. You may copy and adapt them
for non-commercial use, with attribution, and the copy keeps the same licence. Required attribution
for the e-EDL: "© World Health Organization, Fifth WHO model list of essential in vitro diagnostics (EDL 5),
World Health Organization, 2025. Some rights reserved. CC BY-NC-SA 3.0 IGO."
WHO does not endorse MedPod. If MedPod ever becomes commercial, these files need a licence review.
