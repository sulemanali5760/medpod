"""Closed-form beam formulas (Euler-Bernoulli, small deflection, linear elastic).

Units: consistent set, we use N, mm, MPa (N/mm^2) throughout the project.
Every formula here is cross-checked in tests/ against an independent method
(numerical integration and/or CalculiX FEA) - see tests/test_calc_beams.py.
"""


def I_rect(b, h):
    """Second moment of area of a solid rectangle about its horizontal centroidal axis."""
    return b * h**3 / 12.0


def I_rect_tube(b, h, t):
    """Second moment of area of a rectangular tube, outer b x h, uniform wall t."""
    return (b * h**3 - (b - 2 * t) * (h - 2 * t) ** 3) / 12.0


def cantilever_point_tip(P, L, E, I):
    """Tip deflection of a cantilever with a point load P at the free end: P L^3 / (3 E I)."""
    return P * L**3 / (3.0 * E * I)


def cantilever_udl_tip(w, L, E, I):
    """Tip deflection of a cantilever under uniform load w (force/length): w L^4 / (8 E I)."""
    return w * L**4 / (8.0 * E * I)


def simply_supported_point_mid(P, L, E, I):
    """Midspan deflection, simply supported, central point load: P L^3 / (48 E I)."""
    return P * L**3 / (48.0 * E * I)


def simply_supported_udl_mid(w, L, E, I):
    """Midspan deflection, simply supported, uniform load: 5 w L^4 / (384 E I)."""
    return 5.0 * w * L**4 / (384.0 * E * I)


def bending_stress(M, c, I):
    """Max bending stress sigma = M c / I (c = distance from neutral axis to extreme fibre)."""
    return M * c / I


def euler_buckling_load(E, I, L, K=1.0):
    """Euler critical load P_cr = pi^2 E I / (K L)^2. K: 1.0 pinned-pinned, 0.5 fixed-fixed,
    0.699 fixed-pinned, 2.0 fixed-free. Valid for slender columns only (check slenderness)."""
    from math import pi
    return pi**2 * E * I / (K * L) ** 2
