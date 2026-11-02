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
