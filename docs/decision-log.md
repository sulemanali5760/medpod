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
