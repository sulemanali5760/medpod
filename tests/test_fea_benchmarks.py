"""Toolchain benchmarks: CalculiX FEA must reproduce known closed-form answers
before we trust it on MedPod parts. Each benchmark records its tolerance and why."""
import shutil

import numpy as np
import pytest

from medpod.calc import beams, thermal
from medpod.fea import ccx

pytestmark = pytest.mark.skipif(shutil.which("ccx") is None, reason="CalculiX not installed")


def test_cantilever_tip_deflection_matches_beam_theory():
    """B-001: 1000 x 40 x 40 mm solid bar, clamped at x=0, 1000 N down at the tip.
    Tolerance 3%: C3D10 tets plus a fully clamped face and shear deformation
    (L/h = 25) make the FEA differ slightly from Euler-Bernoulli theory."""
    L, b, h, P, E, nu = 1000.0, 40.0, 40.0, 1000.0, 210000.0, 0.3
    ids, xyz, el = ccx.mesh_step_or_box(size=10.0, box=(0, 0, 0, L, b, h))
    fix = ccx.nodes_where(ids, xyz, lambda c: np.isclose(c[:, 0], 0.0))
    tip = ccx.nodes_where(ids, xyz, lambda c: np.isclose(c[:, 0], L))
    step = ["*STEP", "*STATIC", "*BOUNDARY", "FIX,1,3,0.0", "*CLOAD"]
    step += [f"{n},3,{-P / len(tip):.9g}" for n in tip]
    step += ["*NODE PRINT,NSET=TIP", "U", "*NODE PRINT,NSET=FIX", "RF", "*END STEP"]
    wd = ccx.workdir()
    ccx.write_inp(f"{wd}/cant.inp", ids, xyz, el, {"FIX": fix, "TIP": tip},
                  {"name": "STEEL", "E": E, "nu": nu}, step)
    res = ccx.parse_dat(ccx.run_ccx(f"{wd}/cant.inp")[0])
    u = np.array(list(res[("displacements", "TIP")].values()))
    rf = np.array(list(res[("forces", "FIX")].values()))
    assert rf[:, 2].sum() == pytest.approx(P, rel=1e-6)  # equilibrium check
    expected = beams.cantilever_point_tip(P, L, E, beams.I_rect(b, h))
    assert -u[:, 2].mean() == pytest.approx(expected, rel=0.03)


def test_plane_wall_conduction_matches_fourier():
    """B-002: 100 x 50 x 50 mm block, 80 C on x=0, 20 C on x=100, k = 0.2 W/(mm K)
    (200 W/m K, aluminium-like). Linear field -> FEA should be exact to 0.5%."""
    L, A, k, T1, T2 = 100.0, 50.0 * 50.0, 0.2, 80.0, 20.0
    ids, xyz, el = ccx.mesh_step_or_box(size=10.0, box=(0, 0, 0, L, 50, 50))
    hot = ccx.nodes_where(ids, xyz, lambda c: np.isclose(c[:, 0], 0.0))
    cold = ccx.nodes_where(ids, xyz, lambda c: np.isclose(c[:, 0], L))
    step = ["*STEP", "*HEAT TRANSFER,STEADY STATE", "*BOUNDARY",
            f"HOT,11,11,{T1}", f"COLD,11,11,{T2}",
            "*NODE PRINT,NSET=HOT", "RFL", "*END STEP"]
    wd = ccx.workdir()
    ccx.write_inp(f"{wd}/wall.inp", ids, xyz, el, {"HOT": hot, "COLD": cold},
                  {"name": "AL", "k": k}, step)
    res = ccx.parse_dat(ccx.run_ccx(f"{wd}/wall.inp")[0])
    q = sum(v[0] for v in res[("heat generation", "HOT")].values())
    assert q == pytest.approx(thermal.conduction_wall(k, A, T1 - T2, L), rel=0.005)
