# Verification Log

Every test, what it proves, how it was checked, and its latest result.
Run all: `python3 -m pytest` from the repo root.

| ID | Test | Proves | Independent check | Tolerance | Result (2026-11-02) |
|---|---|---|---|---|---|
| F-001 | `test_calc_beams::test_cantilever_point_tip` | P L³/3EI | Numerical integration of E I y'' = M | 1e-6 | ✅ |
| F-002 | `test_calc_beams::test_cantilever_udl_tip` | w L⁴/8EI | same | 1e-6 | ✅ |
| F-003 | `test_calc_beams::test_simply_supported_point_mid` | P L³/48EI | same | 1e-6 | ✅ |
| F-004 | `test_calc_beams::test_simply_supported_udl_mid` | 5 w L⁴/384EI | same | 1e-6 | ✅ |
| F-005 | `test_calc_beams::test_second_moments` | I of rectangle / rectangular tube | Numerical ∫y² dA | 1e-3 | ✅ |
| B-001 | `test_fea_benchmarks::test_cantilever...` | CalculiX + gmsh tet10 pipeline (mesh, node order, loads, BCs, output parsing) give correct static results | Beam theory | 3% | ✅ FEA 7.426 mm vs 7.440 mm (−0.19%); reactions sum 1000.0 N |
| B-002 | `test_fea_benchmarks::test_plane_wall...` | CalculiX steady heat transfer pipeline | Fourier's law | 0.5% | ✅ 300.000 W vs 300 W |
| G-000 | `test_capsule_geometry::test_G000...` | The collision checker itself works (control test) | Patient lifted 300 mm must collide | > 1000 mm³ | ✅ 453,574 mm³ detected |
| G-001 | `test_G001_patient_fits...` | 1755 mm patient fits inside closed capsule | Exact OpenCascade solid intersection + min distance | 0 overlap, ≥ 150 mm to lid | ✅ 236 mm clearance |
| G-002 | `test_G002_scanner_ring_clears...` (7 positions) | Moving ring + sensors never touch the patient | same | 0 overlap, ≥ 50 mm | ✅ min 140 mm (at x = −800) |
| G-003 | `test_G003_scanner_ring_stays_inside_shell` | Ring at both travel ends doesn't hit shell or display | same | 0 overlap | ✅ |
| G-004 | `test_G004_lid_display_inside_lid` | Display fits inside the lid | same | 0 overlap | ✅ |
| G-005 | `test_G005_open_lid_clears...` | Open lid (70°) doesn't hit tub/trim, stays above floor | same | 0 overlap | ✅ 17 mm gap to trim |
| G-006 | `test_G006_patient_can_get_in...` | Entry side is clear with lid open | same | 0 overlap | ✅ |

## Lessons
- gmsh and CalculiX number the mid-edge nodes of 10-node tets differently (last two swapped).
  B-001 would fail or give nonsense if the mapping in `fea/ccx.py` were wrong.
- Always check equilibrium (reaction forces = applied load) as well as the answer.
- 2026-11-02: Always add a control test that proves a checker can FAIL. The first version of the
  collision helper returned 0 on any error, which could have hidden real collisions. It was removed,
  and G-000 now proves a known collision is detected.
- 2026-11-02: Distances from OpenCascade are floats (5e-15, not 0). Compare with a tolerance.
- 2026-11-02 (design): the cutaway shows ~340 mm of empty space under the bed inside the tub.
  The electronics could move up there to make the pedestal smaller. Open item.

## Phase 2: test menu data (`tests/test_test_menu_data.py`)
| ID | Test | What it proves | Independent check | Pass criterion | Result |
|---|---|---|---|---|---|
| T-001 | `test_edl5_scrape_complete` | e-EDL scrape is complete | Home page id list (1–234) | 234 rows, all with test/setting/assay/specimen; 39 Non-laboratory | ✅ |
| T-002 | `test_edl4_tier1_transcription_shape` | EDL 4 Tier I transcription has every row | TRS 1053 tables | 39 rows, 11 in I.a | ✅ |
| T-003 | `test_edl4_row_agrees_with_edl5` (39 cases) | Each hand-transcribed EDL 4 row matches the scraped EDL 5 row it points to | Second official source, second method (scrape vs. hand transcription) | Same test name word and specimen family, or the difference is declared in `edl5_note` | ✅ after 2 notes added (see below) |
| T-004 | `test_ghe_top10_well_formed` | GHE table has ranks 1–10, no duplicates | Rendered WHS 2024 p. 14 read visually = text extraction | ranks 1..10 per group | ✅ |
| T-005 | `test_menu_references_exist` | Every menu row points to real data; rows with no EDL test are marked Draft/Out of scope | Data files | all ids Non-laboratory, all causes in GHE table | ✅ |
| T-006 | `test_every_ghe_cause_addressed` | No top-10 cause is silently dropped | GHE table | menu covers all 13 distinct causes | ✅ |
| T-007 | `test_parser_reads_minimal_page` | Parser extracts fields and leaves missing ones empty | Hand-written page | exact field values | ✅ |

### Lessons
- 2026-11-02: T-003 failed on first run for two rows. Both were real changes between editions, not
  transcription errors: EDL 5 lists HBeAg with serum/plasma (EDL 4: capillary/venous whole blood) and
  renamed "Sickle cell testing" to "Haemoglobin A, S and C detection". Notes were added to the data, and
  the test now accepts a mismatch only when the note declares it and names the EDL 5 value.

## Phase 2b: cost per test (`tests/test_test_costs.py`)
| ID | Test | What it proves | Independent check | Pass criterion | Result |
|---|---|---|---|---|---|
| T-008 | `test_every_number_is_in_its_quote` (17 rows) | Every stored price matches the source wording | Verbatim quote extracted by script from the source text | each low/high/point value appears in the quote | ✅ |
| T-009 | `test_ranges_are_ordered` | low ≤ point ≤ high | — | ordered | ✅ |
| T-010 | `test_missing_price_is_never_zero` | An unsourced price (BP device, C-12) can't silently count as $0 | — | `ValueError` | ✅ |
| T-011 | `test_d008_set_has_a_cost_row` | Every D-008 test has a price row | D-008 list | 7 EDL ids priced | ✅ |
| T-012 | `test_panel_totals_match_hand_sum` | Panel calculator adds correctly | Hand sum written in the test | 1e-9 | ✅ 16.733–22.988 USD |

### Lessons
- 2026-11-02: One page reference was wrong (D-01: Table 6 is on PDF p.27, not 26). A per-page `pdftotext` search caught it.
  Check page numbers by script, not by eye.
