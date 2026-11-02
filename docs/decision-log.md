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

## D-005 — Concept layout v0.1 — SUPERSEDED by D-006
- **Date:** 2026-11-02
- Flat bed 2000 × 700 mm, top at 650 mm, 40×40 T-slot frame with 6 legs, sensor arch over the
  chest (x = 1450 mm) carrying an RGB camera, a thermal camera and a microphone, electronics box under the platform.
- Picture: docs/img/concept_v01.png. STEP: cad/parts/concept_v01.step.

## D-006 — Final form: fully enclosed capsule (owner decision)
- **Date:** 2026-11-02
- **Decision (owner):** one final design, no interim versions; fully enclosed capsule.
- **Layout:** capsule shell 2620 × 1120 × 960 mm (split at the axis, z = 900 mm). Upper half is a lid
  with a clear polycarbonate centre and white end caps, hinged on one side (70°, gas struts).
  Inside: contoured bed on 4 load cells, scanner ring on rails (travel ±800 mm) carrying
  camera / thermal / radar / lights / mics, hand rests with ECG electrodes, SpO2 clip, BP cuff,
  blood-analyser port, ultrasound arm (future). Pedestal holds battery, isolated PSU, compute, fans.
- **Why a moving ring:** one set of sensors covers the whole body at a fixed short distance, instead of
  many fixed sensors. That's the same idea as CT/MRI gantries.
- **Verified:** geometry tests G-000…G-006 pass. **Not yet verified:** structure (FEA), lid strut
  forces, ventilation/heat, component sizes (provisional).
- Model: `cad/medpod_capsule.py` → `cad/parts/medpod_capsule.step`. Renders: `docs/img/capsule_*.png`.

## D-007 — Test menu built on WHO EDL 5 Non-laboratory list (APPROVED by owner 2026-11-02)
- **Date:** 2026-11-02
- **Proposal:** the plan said "EDL 4 Tier I", but WHO's e-EDL now hosts EDL 5 (© WHO 2025), which replaces
  tiers with Non-laboratory / Laboratory settings. Build the menu on EDL 5 Non-laboratory (39 tests) and
  keep EDL 4 Tier I on file for traceability (`data/who_edl4_tier1.csv`).
- **Why:** it is WHO's current list. Changes between the two are listed in `docs/04-test-menu.md`.
- **Open:** first cartridge set (proposal: malaria, HIV, HBsAg, anti-HCV, syphilis; glucose/HbA1c, cholesterol, BP).

## D-008 — First cartridge set (owner approved 2026-11-02)
- **Rapid tests (cartridge reader, capillary blood):** malaria (EDL 5 id 34), HIV (25, or 38 dual HIV/syphilis),
  HBsAg (20), anti-HCV (22), syphilis (37 / 38).
- **NCD side:** glucose (4) / HbA1c (19) and total cholesterol (227) on handheld analysers, plus the BP cuff (pod sensor).
- **Why:** each is a top-10 cause of death in LIC/LMIC (GHE 2021) or shares a test with one, and is on WHO EDL 5
  Non-laboratory. See `docs/04-test-menu.md`.
- **Next:** cost per test for this set (Phase 2b).
