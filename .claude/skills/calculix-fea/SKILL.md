---
name: calculix-fea
description: Run structural or thermal finite-element analysis with CalculiX (ccx) and gmsh in this project. Use when checking stress, deflection, safety factor, heat flow or temperature of any MedPod part, or when writing/debugging a CalculiX .inp deck.
---

# CalculiX FEA (MedPod)

Source of truth: the official CalculiX CrunchiX User's Manual by Guido Dhondt.
Keyword pages are saved in `references/ccx-2.11-keywords.txt`. Grep it before you use a keyword.
That manual is version 2.11 (Debian `calculix-ccx-doc`) while the solver is 2.21. The keywords
used here are verified on 2.21 by tests B-001 and B-002. For any keyword not covered by a
passing test, check https://www.dhondt.de (ccx_2.21.pdf) when reachable, or add a benchmark test.

## Pipeline (code: `software/medpod/fea/ccx.py`)
1. Geometry: CadQuery → STEP, or a box for benchmarks.
2. Mesh: `mesh_step_or_box(size, step_file=...)` makes gmsh 2nd-order tets and maps them to C3D10.
   gmsh's last two mid-edge nodes are swapped relative to CalculiX C3D10. The mapping is
   `_GMSH_TO_CCX_TET10`. Never change it without rerunning B-001.
3. Deck: `write_inp(...)`. Model definition (*NODE, *ELEMENT, *NSET, *MATERIAL, *SOLID SECTION),
   then step lines.
4. Run: `run_ccx(path)`. It raises if ccx prints *ERROR.
5. Read: `parse_dat(dat)` → `{(quantity, NSET): {node: values}}` from *NODE PRINT.
   Quantity names in the .dat: `displacements` (U), `forces` (RF), `heat generation` (RFL).

## Facts from the manual
- *BOUNDARY DOFs for structures: 1,2,3 = translations x,y,z; 4–6 = rotations (beam/shell nodes only); 11 = temperature.
- *CLOAD: a force on the same node and direction within one step is **added**.
- *SOLID SECTION needs ELSET and MATERIAL. For 3D elements there is no thickness line.
- *ELASTIC TYPE=ISO line: E, ν, (temperature).
- C3D10: a good general-purpose element that works with automatic tet meshers. C3D20R is better per DOF.
  The manual warns: "Do not take element choice lightheartedly!"

## Rules
- Units: N, mm, MPa, W, K. Then E is in MPa, k in W/(mm·K), h in W/(mm²·K).
- Always check equilibrium: the sum of RF must equal the applied load.
- Every new analysis type (contact, buckling, frequency, convection) needs its own closed-form
  benchmark in `tests/test_fea_benchmarks.py` before it's used on a real part.
- Mesh convergence: when a result decides a design, rerun with half the element size.
  It must change by less than 5%.
- Point loads on tets give singular local stresses. Judge stress away from load points, or spread the load over an area.
