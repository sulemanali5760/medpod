"""Steady-state heat transfer formulas (Fourier conduction, Newton cooling).

Units: W, mm, K. Conductivity k in W/(mm K), film coefficient h in W/(mm^2 K).
(1 W/(m K) = 1e-3 W/(mm K); 1 W/(m^2 K) = 1e-6 W/(mm^2 K).)
Cross-checked in tests/ against CalculiX heat-transfer FEA.
"""


def conduction_wall(k, A, dT, L):
    """Heat flow through a plane wall: Q = k A dT / L (Fourier's law, 1-D steady)."""
    return k * A * dT / L


def R_conduction(L, k, A):
    """Thermal resistance of a plane wall: L / (k A)  [K/W]."""
    return L / (k * A)


def R_convection(h, A):
    """Thermal resistance of a convective surface: 1 / (h A)  [K/W]."""
    return 1.0 / (h * A)


def heat_flow_series(dT, *resistances):
    """Heat flow through resistances in series: Q = dT / sum(R)."""
    return dT / sum(resistances)
