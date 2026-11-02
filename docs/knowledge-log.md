# Knowledge Log

## Sources used
| Source | Type | Used for |
|---|---|---|
| IEC 60601-1, 60601-2-52 | Standard | Safety and bed requirements (S1, S2) |
| ISO 14971, IEC 62304, ISO 13485 | Standard | Risk, software and quality processes (reference) |
| ANSUR II (US Army anthropometric survey, 2012) | Dataset | Body sizes for platform dimensions (M1) |
| SolidWorks API Help | Documentation | Writing CAD macros. **Not yet loaded**: help.solidworks.com is blocked from the cloud; load from local apihelp.chm |
| CalculiX CrunchiX User's Manual 2.11 (G. Dhondt), Debian pkg calculix-ccx-doc | Official manual | FEA keywords; saved in .claude/skills/calculix-fea/references |
| gmsh 4.12 reference manual, Debian pkg gmsh-doc | Official manual | Meshing |
| CadQuery docs (github.com/CadQuery/cadquery, doc/) | Official docs | Parametric CAD |
| PyMAPDL docs (github.com/ansys/pymapdl, doc/) | Official docs | Driving ANSYS Student from Python (owner's PC) |
| open-gsd/gsd-core (docs/explanation) | Method | Phase loop and file-based state, adopted in CLAUDE.md §3 |
| forrestchang/andrej-karpathy-skills | Method | Coding rules, CLAUDE.md §4 |
| DietrichGebert/ponytail | Method | Smallest-complete-change rules, CLAUDE.md §4 |
| wheresryan22/anatomy | Tool | Explanatory isometric figures for the final report |
| WHO e-EDL, edl.who-healthtechnologies.org ("Fifth WHO model list of essential IVDs (EDL 5)", © WHO 2025), fetched 2026-11-02 | Official list | All 234 recommendations → `data/who_edl5.csv`; test menu (Phase 2) |
| WHO TRS 1053 (2023), 4th SAGE IVD report incl. EDL 4, iris.who.int/handle/10665/373322, pp. 127–146 | Official list | EDL 4 Tier I transcription → `data/who_edl4_tier1.csv` |
| WHO Global hepatitis report 2024 (iris.who.int/handle/10665/376461), PDF pp. 72, 75 | Official report | HBsAg and anti-HCV RDT prices → `data/test_costs.csv` |
| WHO Availability, price and affordability of health technologies for the management of diabetes (2025), Tables 4–6, 11 | Official report | Glucose strip, lancet, meter, HbA1c analyser prices; lowest day's wages |
| Malar J 2022;21:12 (PMC8752184) | Peer-reviewed | Malaria RDT price (Global Fund purchases 2009–2018) |
| Health Policy Open 2026;10:100172 (PMC13199886) | Peer-reviewed | HIV RDT and dual HIV/syphilis RDT prices |
| Glob Health Epidemiol Genom 2019;4:e7 (PMC6749552) | Peer-reviewed | HbA1c and cholesterol POC cost per test (Haiti) |
| WHO World health statistics 2024, Fig. 1.9 (source: WHO GHE 2021), iris.who.int/handle/10665/376869 | Official statistics | 2021 top-10 causes of death, LIC and LMIC → `data/who_ghe2021_top10_deaths.csv` |

## Tools
| Tool | Used for |
|---|---|
| SolidWorks + SolidWorks Simulation | Mechanical design and stress analysis |
| KiCad, LTspice | Electronics design and circuit simulation |
| Arduino IDE / PlatformIO | Sensor firmware |
| Python, PyTorch | Signal processing and AI |

## Lessons learned
- 2026-11-02: gmsh and CalculiX order the mid-edge nodes of 10-node tets differently. A wrong mapping is silent until you benchmark against a known answer.
- 2026-11-02: Debian strips /usr/share/doc on install in this container. Unpack doc packages with dpkg-deb -x.
- 2026-11-02: Headless 3D rendering needs libosmesa6 (pyvista/VTK).
- 2026-11-02: iris.who.int and edl.who-healthtechnologies.org are reachable from the cloud; www.who.int,
  cdn.who.int, apps.who.int and the GHO API (ghoapi.azureedge.net) are not (proxy 403). IRIS has a
  DSpace REST API: `/server/api/discover/search/objects?query=…` and `/server/api/core/items/<uuid>?embed=bundles/bitstreams`.
- 2026-11-02: The e-EDL moved from EDL 4 "tiers" to EDL 5 "settings" (Non-laboratory / Laboratory). Check the
  edition a source is on before quoting it.
- 2026-11-02: `ccx -v` exits with code 201, which stopped `tools/setup_cloud.sh` (set -o pipefail) before
  pytest ran. Fixed with `|| true`.
- 2026-11-02: Official price-list hosts are blocked from the cloud: theglobalfund.org, supply.unicef.org,
  clintonhealthaccess.org, finddx.org, msfaccess.org, stoptb.org (proxy 403; web-fetch DNS failure).
  pmc.ncbi.nlm.nih.gov is reachable, but NCBI E-utilities are not. PMC shows a reCAPTCHA after a burst of
  requests; wait and retry.
- 2026-11-02: Quote extraction: `pdftotext` (raw) loses table rows that `pdftotext -layout` keeps. Check each quote against both.
