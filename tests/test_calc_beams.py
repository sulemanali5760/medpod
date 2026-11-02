"""Verify the closed-form beam formulas with an independent method:
numerically integrate the Euler-Bernoulli equation E I y'' = M(x) and compare.
If a formula (or its coefficient) is wrong, these tests fail."""
import numpy as np
import pytest
from scipy.integrate import cumulative_trapezoid

from medpod.calc import beams

E, I, L = 70000.0, 2.0e5, 1000.0  # MPa, mm^4, mm  (arbitrary test values)
x = np.linspace(0.0, L, 200001)


def integrate_cantilever(M):
    """Clamped at x=0: y(0)=0, y'(0)=0. Returns tip deflection."""
    slope = cumulative_trapezoid(M / (E * I), x, initial=0.0)
    return cumulative_trapezoid(slope, x, initial=0.0)[-1]


def integrate_simply_supported_mid(M):
    """y(0)=y(L)=0. Integrate twice, then remove the linear part to satisfy y(L)=0."""
    slope = cumulative_trapezoid(M / (E * I), x, initial=0.0)
    y = cumulative_trapezoid(slope, x, initial=0.0)
    y -= y[-1] * x / L
    return np.interp(L / 2, x, y)


def test_cantilever_point_tip():
    P = 1000.0
    numeric = integrate_cantilever(P * (L - x))  # sagging-positive moment
    assert beams.cantilever_point_tip(P, L, E, I) == pytest.approx(numeric, rel=1e-6)


def test_cantilever_udl_tip():
    w = 2.0
    numeric = integrate_cantilever(w * (L - x) ** 2 / 2)
    assert beams.cantilever_udl_tip(w, L, E, I) == pytest.approx(numeric, rel=1e-6)


def test_simply_supported_point_mid():
    P = 1000.0
    M = np.where(x <= L / 2, P * x / 2, P * (L - x) / 2)
    numeric = -integrate_simply_supported_mid(M)
    assert beams.simply_supported_point_mid(P, L, E, I) == pytest.approx(numeric, rel=1e-6)


def test_simply_supported_udl_mid():
    w = 2.0
    numeric = -integrate_simply_supported_mid(w * x * (L - x) / 2)
    assert beams.simply_supported_udl_mid(w, L, E, I) == pytest.approx(numeric, rel=1e-6)


def test_second_moments():
    # Independent: numerically integrate y^2 dA over the section.
    b, h, t = 40.0, 60.0, 3.0
    y = np.linspace(-h / 2, h / 2, 600001)
    width = np.where(np.abs(y) > h / 2 - t, b, 2 * t)
    assert beams.I_rect(b, h) == pytest.approx(np.trapezoid(b * y**2, y), rel=1e-6)
    assert beams.I_rect_tube(b, h, t) == pytest.approx(np.trapezoid(width * y**2, y), rel=1e-3)
