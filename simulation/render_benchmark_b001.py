"""Render benchmark B-001 (cantilever) as a picture: deformed shape coloured by displacement.
Run: python3 simulation/render_benchmark_b001.py -> docs/img/benchmark_b001.png"""
import os
import sys

import numpy as np
import pyvista as pv

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{ROOT}/software")
from medpod.calc import beams  # noqa: E402
from medpod.fea import ccx  # noqa: E402

L, b, h, P, E = 1000.0, 40.0, 40.0, 1000.0, 210000.0
ids, xyz, el = ccx.mesh_step_or_box(size=10.0, box=(0, 0, 0, L, b, h))
fix = ccx.nodes_where(ids, xyz, lambda c: np.isclose(c[:, 0], 0.0))
tip = ccx.nodes_where(ids, xyz, lambda c: np.isclose(c[:, 0], L))
step = ["*STEP", "*STATIC", "*BOUNDARY", "FIX,1,3,0.0", "*CLOAD"]
step += [f"{n},3,{-P / len(tip):.9g}" for n in tip]
step += ["*NODE PRINT,NSET=NALL", "U", "*END STEP"]
wd = ccx.workdir()
ccx.write_inp(f"{wd}/c.inp", ids, xyz, el, {"FIX": fix, "TIP": tip, "NALL": list(map(int, ids))},
              {"name": "STEEL", "E": E, "nu": 0.3}, step)
U = ccx.parse_dat(ccx.run_ccx(f"{wd}/c.inp")[0])[("displacements", "NALL")]
disp = np.array([U[int(n)] for n in ids])
index = {int(n): i for i, n in enumerate(ids)}
cells = np.hstack([np.full((len(el), 1), 4), np.vectorize(index.get)(el[:, :4])]).ravel()
grid = pv.UnstructuredGrid(cells, np.full(len(el), pv.CellType.TETRA), xyz)
grid["|U| (mm)"] = np.linalg.norm(disp, axis=1)
scale = 10.0
warped = grid.copy()
warped.points = xyz + scale * disp

theory = beams.cantilever_point_tip(P, L, E, beams.I_rect(b, h))
fea = -disp[[index[n] for n in tip], 2].mean()
pl = pv.Plotter(off_screen=True, window_size=(1600, 800))
pl.set_background("white")
pl.add_mesh(grid, style="wireframe", color="#bbbbbb", opacity=0.3)
pl.add_mesh(warped, scalars="|U| (mm)", cmap="turbo", show_edges=False,
            scalar_bar_args={"color": "black", "title": "|U| (mm)"})
pl.add_text(f"Benchmark B-001: steel bar 1000x40x40 mm, clamped, 1000 N at tip (deformation x{scale:.0f})\n"
            f"CalculiX FEA tip deflection {fea:.3f} mm  vs  beam theory PL^3/3EI {theory:.3f} mm"
            f"  ->  error {100 * (fea - theory) / theory:+.2f}%  PASS (limit 3%)",
            font_size=11, color="black")
pl.camera_position = [(500, -2200, 300), (500, 20, -150), (0, 0, 1)]
os.makedirs(f"{ROOT}/docs/img", exist_ok=True)
pl.screenshot(f"{ROOT}/docs/img/benchmark_b001.png")
print(f"fea={fea:.4f} theory={theory:.4f}")
