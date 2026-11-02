# MedPod — Non-invasive Diagnostic Triage Station

An open research prototype: a station where a person lies down or sits, safe non-invasive
sensors measure their body, and an AI combines the readings to flag what looks wrong
and how urgently they should see a doctor.

> Research prototype only. Not a medical device. Not for diagnosing real patients.

## Folders
| Folder | Contents |
|---|---|
| `docs/` | The study record: vision, requirements, decisions, knowledge, limitations |
| `cad/macros/` | SolidWorks VBA macros that generate the parts and assemblies |
| `cad/parts/` | Exported STEP files and drawings |
| `simulation/` | Simulation setups and results (FEA, thermal, motion) |
| `electronics/` | KiCad schematics and PCBs, LTspice circuits |
| `firmware/` | Microcontroller code that reads the sensors |
| `software/` | Signal processing and AI models |

## The study record (`docs/`)
| File | Purpose |
|---|---|
| `00-vision.md` | The problem, the goal, what's in and out of scope |
| `01-requirements.md` | What the pod must do, with numbers and where they came from |
| `decision-log.md` | Every design choice: options, what we picked, why |
| `knowledge-log.md` | Sources used (books, standards, papers, datasets, tools) and lessons learned |
| `limitations.md` | What we couldn't solve, what's unverified, open problems |

Every work session adds entries to these files. At the end of the project they become the
final report: what we built, how, from what sources, and what's still unsolved.
