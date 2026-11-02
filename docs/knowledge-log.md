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
