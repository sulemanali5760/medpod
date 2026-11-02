# Decision Log

Each entry: what we had to decide, the options, what we picked, and why.

---

## D-001 — CAD tool: SolidWorks
- **Date:** 2026-11-02
- **Options:** Blender, FreeCAD, Fusion 360, SolidWorks
- **Picked:** SolidWorks (owner already has a license)
- **Why:** real dimensions, assemblies, built-in FEA (SolidWorks Simulation), industry
  standard for medical device design. Blender is for visuals, not engineering.
- **How we use it:** Claude writes VBA macros against the SolidWorks API; the owner runs
  them and reports results or errors. Repeatable and version-controlled.

## D-002 — v0.1 is a non-invasive triage station, not a diagnostic pod
- **Date:** 2026-11-02
- **Picked:** Only safe, existing, non-radiation sensors. Output = triage + urgency, not diagnosis.
- **Why:** buildable with consumer-priced parts, no radiation safety work, no blood handling,
  far lower regulatory burden. Proves the core idea: many sensors + one AI brain.

## D-003 — Frame material: aluminium T-slot extrusion (proposed)
- **Date:** 2026-11-02
- **Options:** welded steel tube, aluminium T-slot extrusion, wood
- **Proposed:** 40×40 mm aluminium T-slot extrusion (e.g. 6063-T5 / 6105-T5 alloys)
- **Why:** bolt-together, no welding, easy to rework while the design changes,
  widely sold. To be confirmed by FEA against requirement M2/M3.

## D-004 — Toolchain split: cloud (open source) + owner's PC (SolidWorks, ANSYS)
- **Date:** 2026-11-02
- **Why:** SolidWorks and ANSYS are Windows-only and licensed to the owner, so they can't run in a
  Linux cloud container. The cloud does CadQuery CAD, CalculiX FEA, code and AI. The PC does
  SolidWorks modelling and drawings, plus SolidWorks Simulation / ANSYS as an independent second check.
  Two different solvers agreeing is stronger evidence than one.

## D-005 — Concept layout v0.1 (draft, needs owner review)
- **Date:** 2026-11-02
- Flat bed 2000 × 700 mm, top at 650 mm, 40×40 T-slot frame with 6 legs, sensor arch over the
  chest (x = 1450 mm) carrying an RGB camera, a thermal camera and a microphone, electronics box under the platform.
- Picture: docs/img/concept_v01.png. STEP: cad/parts/concept_v01.step.
