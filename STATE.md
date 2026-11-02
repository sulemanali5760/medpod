# STATE

**Milestone:** v0.1 — non-invasive triage station
**Updated:** 2026-11-02

## Phases
| # | Phase | Status |
|---|---|---|
| 0 | Project setup, rules, verified toolchain | ✅ Done |
| 1 | Capsule design + geometry verification | ✅ Done (structure/thermal next) |
| 2 | Sensor arm and mounts | ⏳ |
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

## Open questions for the owner
- SolidWorks Student: which year?
- Allow vendor/doc domains in the environment's network settings (help.solidworks.com, datasheet sites)?
