---
name: engineering-calcs
description: Hand calculations for MedPod (beam deflection and stress, buckling, second moment of area, conduction, convection, thermal resistance). Use before any FEA to predict the answer, and when sizing frames, mounts or cooling.
---

# Engineering calculations (MedPod)

Code: `software/medpod/calc/` (`beams.py`, `thermal.py`). Tests: `tests/test_calc_*.py`.

## Rule: a formula is usable only after a passing independent test
Each function has a test that checks it with a **different method**: numerical integration,
FEA, or a published worked example with its citation. The status of each formula is in
`docs/verification-log.md`.

To add a formula:
1. Write the function with a docstring giving the formula, units and validity limits.
2. Cite its source in `docs/knowledge-log.md` (textbook and edition, standard, or derivation).
3. Write the independent test, run it, and log the result.

## Verified so far
| Formula | Function | Test |
|---|---|---|
| Cantilever tip, point load: PL³/3EI | `cantilever_point_tip` | F-001, B-001 |
| Cantilever tip, UDL: wL⁴/8EI | `cantilever_udl_tip` | F-002 |
| Simply supported mid, point: PL³/48EI | `simply_supported_point_mid` | F-003 |
| Simply supported mid, UDL: 5wL⁴/384EI | `simply_supported_udl_mid` | F-004 |
| I of rectangle / rectangular tube | `I_rect`, `I_rect_tube` | F-005 |
| Plane wall conduction Q = kAΔT/L | `conduction_wall` | B-002 |

Not yet verified (do not use for decisions): `euler_buckling_load`, `bending_stress`,
`R_convection`, `heat_flow_series`.

## Limits to remember
- Euler-Bernoulli assumes slender beams (L/h ≳ 10), small deflection and linear elastic material.
- Material properties (E, yield, k) must come from a supplier datasheet or standard. Never from memory.
- Design rule M3: yield safety factor ≥ 2.0 under the 180 kg safe working load.
