# Requirements (v0.1)

Status key: **Draft** = our assumption, not yet checked against the source. **Verified** = checked.

## Mechanical
| ID | Requirement | Value | Source / reasoning | Status |
|---|---|---|---|---|
| M1 | Fit patient length | Up to ~195 cm tall | Covers about the 99th percentile of adult men; check against ANSUR II anthropometric data | Draft |
| M2 | Patient weight capacity | 180 kg safe working load | Hospital-bed range; check against IEC 60601-2-52 | Draft |
| M3 | Structural safety factor | ≥ 2.0 on yield, under the M2 load | Common engineering practice for people-carrying structures; confirm in FEA | Draft |
| M4 | Platform height | Fixed ~650 mm for v0.1 (adjustable 500–700 mm later) | Easy to sit on and slide onto; to decide | Draft |
| M5 | Frame material | Aluminium extrusion (T-slot) | Light, modular, easy to change; see decision D-001 | Draft |
| M6 | Sensor mounts | Adjustable arms for camera, thermal camera, microphone above the chest/face | — | Draft |

## Safety and regulatory (reference only — v0.1 is a research prototype)
| ID | Standard | What it covers |
|---|---|---|
| S1 | IEC 60601-1 | General safety of medical electrical equipment (electrical isolation, leakage current, mechanical hazards) |
| S2 | IEC 60601-2-52 | Medical beds (loads, stability, entrapment gaps) |
| S3 | ISO 14971 | Risk management for medical devices |
| S4 | IEC 62304 | Medical device software lifecycle |
| S5 | ISO 13485 | Quality management for medical device makers |

v0.1 design rule: **anything touching the patient (ECG electrodes, SpO2 clip) is battery
powered or isolated from mains.** No direct connection to a mains-powered laptop through
patient electrodes.
