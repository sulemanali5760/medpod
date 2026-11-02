# STATE

**Milestone:** v0.1 — non-invasive triage station
**Updated:** 2026-11-02

## Phases
| # | Phase | Status |
|---|---|---|
| 0 | Project setup, rules, verified toolchain | ✅ Done |
| 1 | Patient platform: concept, frame design, FEA vs 180 kg × SF 2 | 🔄 Next |
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

## Phase 1 plan (to agree with owner)
1. Decide platform type: flat bed vs reclined chair (decision D-004).
2. Get official 40×40 T-slot profile data (I, mass, alloy) from a supplier datasheet.
3. Model frame in CadQuery → render → owner reviews.
4. FEA: 180 kg distributed + 2× safety factor; also point load (person sitting on edge).
5. Tests: stress < yield / 2, deflection < limit (to decide), tip-over stability.
6. Export STEP + SolidWorks macro; owner re-checks in SolidWorks Simulation.

## Open questions for the owner
- Bed (lie down) or reclined chair for v0.1?
- SolidWorks Student version year (e.g. 2025)?
