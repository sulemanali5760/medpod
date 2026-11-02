"""Minimal CalculiX (ccx) pipeline: gmsh tet10 mesh -> .inp deck -> run ccx -> parse .dat.

Keyword syntax follows the official CalculiX CrunchiX User's Manual
(*NODE, *ELEMENT TYPE=C3D10, *NSET, *MATERIAL, *ELASTIC, *CONDUCTIVITY, *SOLID SECTION,
*STEP, *STATIC, *HEAT TRANSFER, *BOUNDARY, *CLOAD, *NODE PRINT).
Units: N, mm, MPa, W, K.
"""
import os
import re
import subprocess
import tempfile

import gmsh
import numpy as np

# gmsh 10-node tet edge order (0-1,1-2,2-0,3-0,3-2,3-1) vs CalculiX C3D10
# (1-2,2-3,3-1,1-4,2-4,3-4): the last two mid-edge nodes are swapped.
_GMSH_TO_CCX_TET10 = [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]


def mesh_step_or_box(size, step_file=None, box=None):
    """Mesh a STEP file or an axis-aligned box (x0,y0,z0,dx,dy,dz) with 2nd-order tets.
    Returns (node_ids, coords[N,3], elems[M,10] as CalculiX-ordered node ids)."""
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    try:
        if step_file:
            gmsh.model.occ.importShapes(step_file)
        else:
            gmsh.model.occ.addBox(*box)
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeMax", size)
        gmsh.option.setNumber("Mesh.ElementOrder", 2)
        gmsh.option.setNumber("Mesh.SecondOrderLinear", 1)  # keep mid-nodes on straight edges
        gmsh.model.mesh.generate(3)
        tags, xyz, _ = gmsh.model.mesh.getNodes()
        coords = xyz.reshape(-1, 3)
        etypes, _, enodes = gmsh.model.mesh.getElements(3)
        k = list(etypes).index(11)  # 11 = 10-node tetrahedron
        elems = enodes[k].reshape(-1, 10)[:, _GMSH_TO_CCX_TET10].astype(int)
        return tags.astype(int), coords, elems
    finally:
        gmsh.finalize()


def write_inp(path, node_ids, coords, elems, nsets, material, step_lines):
    """material: dict(name, E, nu) and/or k (conductivity). step_lines: list of deck lines."""
    with open(path, "w") as f:
        f.write("*NODE\n")
        for n, (x, y, z) in zip(node_ids, coords):
            f.write(f"{n},{x:.9g},{y:.9g},{z:.9g}\n")
        f.write("*ELEMENT,TYPE=C3D10,ELSET=EALL\n")
        for i, e in enumerate(elems, 1):
            f.write(f"{i}," + ",".join(map(str, e)) + "\n")
        for name, ids in nsets.items():
            f.write(f"*NSET,NSET={name}\n")
            for j in range(0, len(ids), 12):
                f.write(",".join(map(str, ids[j:j + 12])) + ",\n")
        f.write(f"*MATERIAL,NAME={material['name']}\n")
        if "E" in material:
            f.write(f"*ELASTIC\n{material['E']},{material['nu']}\n")
        if "k" in material:
            f.write(f"*CONDUCTIVITY\n{material['k']}\n")
        f.write(f"*SOLID SECTION,ELSET=EALL,MATERIAL={material['name']}\n")
        f.write("\n".join(step_lines) + "\n")


def run_ccx(inp_path):
    """Run ccx on a deck (path without needing the .inp suffix). Raises on failure."""
    wd, base = os.path.split(os.path.abspath(inp_path))
    job = base[:-4] if base.endswith(".inp") else base
    r = subprocess.run(["ccx", "-i", job], cwd=wd, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0 or "*ERROR" in r.stdout:
        raise RuntimeError(f"ccx failed:\n{r.stdout[-3000:]}\n{r.stderr[-2000:]}")
    return os.path.join(wd, job + ".dat"), r.stdout


def parse_dat(dat_path):
    """Parse *NODE PRINT blocks of a .dat file -> {(quantity, set): {node: np.array}}."""
    out, key = {}, None
    hdr = re.compile(r"^\s*(\S.*?)\s+(?:\(.*?\)\s+)?for set\s+(\S+)\s+and time", re.I)
    for line in open(dat_path):
        m = hdr.match(line)
        if m:
            key = (m.group(1).strip().lower(), m.group(2).upper())
            out[key] = {}
            continue
        parts = line.split()
        if key and parts and re.fullmatch(r"\d+", parts[0]):
            out[key][int(parts[0])] = np.array([float(v) for v in parts[1:]])
        elif key and line.strip() and not parts[0].lstrip("-").replace(".", "").isdigit():
            key = None
    return out


def nodes_where(node_ids, coords, mask):
    return [int(n) for n in node_ids[mask(coords)]]


def workdir(prefix="ccx_"):
    return tempfile.mkdtemp(prefix=prefix)
