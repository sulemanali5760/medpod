# Limitations and Open Problems

## Known limitations of v0.1
- Not a medical device; no clinical validation or regulatory approval.
- Triage only — it flags abnormal readings, it does not diagnose diseases.
- No internal imaging (no X-ray, CT, MRI, ultrasound) and no blood tests yet.
- Camera-based heart rate (rPPG) is less accurate with motion, poor light and darker skin
  tones unless specifically handled — must be tested across skin tones.
- Thermal cameras measure skin temperature, not core body temperature.

## Unsolved problems in the field (that this project touches)
- No objective biomarker for pain.
- Combining many signals into one reliable conclusion (multimodal fusion) is still research.
- Getting AI models to reliably say "I don't know".

## Unverified in this project
- All sensor/electronics envelopes and fields of view (docs/02-components.md): placeholders.
- Mannequin proportions: common anthropometric fractions, not yet checked against ANSUR II.
- Clearance margins (150 mm to lid, 50 mm to moving ring) are our own assumptions, not from a standard.
- Structural strength of pedestal/deck/hinge: no FEA yet.
- Lid gas-strut force, lid mass and hand force to open: not calculated.
- Heat and CO2 build-up inside a closed capsule with a person in it: not calculated. This is a safety issue.

## Known design issues
- 1136 mm wide: won't fit through a standard doorway.
- Enclosed capsule: claustrophobia risk. Clear canopy, lights and an inside display help but don't solve it.
- Lid must open from inside and on power loss (manual release). Not designed yet.

## Unverified in Phase 2 (test menu, `docs/04-test-menu.md`)
- Burden ranking uses 2021 **deaths** (WHS 2024 Fig. 1.9), not DALYs. GHE 2021 DALY tables are blocked (www.who.int).
- Cost per test: not sourced.
- Accuracy per test: not extracted (e-EDL "Summary of Evidence Evaluation" exists per test).
- Reading RDTs and agglutination cards with the pod camera: no evidence yet.
- Referral thresholds for BP, SpO2, glucose, Hb: no WHO guideline fetched yet.
- Link between HBV/HCV and cirrhosis burden in LIC/LMIC: not sourced.
- EDL 4 Tier I is a hand transcription of a PDF. It is cross-checked against the e-EDL but not against a second transcription.
