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

## Lessons
- gmsh and CalculiX number the mid-edge nodes of 10-node tets differently (last two swapped).
  B-001 would fail or give nonsense if the mapping in `fea/ccx.py` were wrong.
- Always check equilibrium (reaction forces = applied load) as well as the answer.
