# STATE

**Milestone:** v0.1 — non-invasive triage station
**Updated:** 2026-11-02

## Phases
| # | Phase | Status |
|---|---|---|
| 0 | Project setup, rules, verified toolchain | ✅ Done |
| 1 | Capsule design + geometry verification | ✅ Done (structure/thermal next) |
| 2 | Test menu (owner direction 2026-11-02; was "sensor arm and mounts") | 🔄 Draft v0.1 |
| 3 | Sensor electronics (ECG, SpO2, BP, cameras, mic) | ⏳ |
| 4 | Firmware + data capture | ⏳ |
| 5 | AI triage brain | ⏳ |
| 6 | Integration, tests against reference devices | ⏳ |

## Phase 0 result
- Tools installed in cloud: CalculiX 2.21, gmsh 4.15 (Python), ngspice 42, CadQuery 2.8, PyVista.
- Benchmarks passed: cantilever B-001 (−0.19% vs theory), conduction B-002 (≈0%).
- Official docs gathered: CalculiX manual (Debian calculix-ccx-doc), gmsh manual,
  CadQuery docs (GitHub), PyMAPDL docs (GitHub).
- Blocked: help.solidworks.com unreachable from cloud. SolidWorks API skill to be built from
  the official `apihelp.chm` installed with SolidWorks on the owner's PC.

## Phase 1 — Capsule design (owner chose: final version, fully enclosed)
Done:
- Full parametric capsule model, STEP export for SolidWorks, 5 renders.
- Geometry tests G-000…G-006 pass (fit, clearances, ring travel, lid opening).

Next, in order:
1. Ventilation and heat: a person gives off heat and CO2 inside a closed lid. Size the fans/vents
   (verify the formulas first). **Safety-critical.**
2. FEA: deck + load cells + pedestal under 180 kg (SF 2), patient sitting on the rim, lid hinge.
3. Lid: mass, gas-strut force, manual inside release, power-loss behaviour.
4. Replace provisional component envelopes with datasheet values (needs vendor sites, or the owner's PC).
5. SolidWorks: import STEP, build native features via macros (needs official API docs).

## Phase 2 — Test menu (CURRENT, owner direction 2026-11-02)
General-purpose affordable screening for common LMIC conditions; venom later.
Plan: `docs/03-test-menu-plan.md`. Result: **`docs/04-test-menu.md` (Draft v0.1)**, picture `docs/img/test_menu.png`.
Capsule structure/thermal work is paused, not dropped.

Done (2026-11-02):
- WHO e-EDL scraped in full (234 tests; 39 Non-laboratory) → `data/who_edl5.csv` (parser `tools/who_edl.py`).
  The site now hosts **EDL 5**, not EDL 4.
- EDL 4 Tier I (39 rows) transcribed from WHO TRS 1053 → `data/who_edl4_tier1.csv`, cross-checked row by row against EDL 5.
- GHE 2021 top-10 causes of death, LIC and LMIC (WHS 2024 Fig. 1.9) → `data/who_ghe2021_top10_deaths.csv`.
- Menu joined → `data/test_menu.csv`; tests T-001…T-007 pass (`tests/test_test_menu_data.py`).

Next, in order:
1. Owner: approve D-007 (use EDL 5) and the proposed first cartridge set.
2. GHE 2021 **DALYs** by income group (needs www.who.int / cdn.who.int allowed, or the owner downloads the xlsx).
3. Cost per test: Global Fund / UNICEF supply catalogue price lists.
4. Accuracy per test: extract e-EDL "Summary of Evidence Evaluation" for the chosen cartridges.
5. Referral thresholds from WHO guidelines on IRIS (hypertension, diabetes, anaemia, pulse oximetry).
6. Evidence on camera-read RDTs, then a bench test plan for the cartridge reader.

## Open questions for the owner
- SolidWorks Student: which year?
- Allow vendor/doc domains in the environment's network settings (help.solidworks.com, datasheet sites)?
- Allow www.who.int and cdn.who.int (GHE 2021 DALY spreadsheets)?
- D-007: build the menu on EDL 5 (WHO's current list) rather than EDL 4? First cartridge set?
