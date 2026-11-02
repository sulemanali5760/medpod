"""Design checks for the capsule geometry (exact OpenCascade solids, not meshes).
G-001..G-006 in docs/verification-log.md."""
import sys
from pathlib import Path

import cadquery as cq
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cad"))
import medpod_capsule as m  # noqa: E402

V = cq.Vector


def overlap(a, b):
    """Volume (mm^3) shared by two shapes; 0 when they don't touch."""
    return a.intersect(b).Volume()


@pytest.fixture(scope="module")
def model():
    tub, glass, caps, band, led = m.shell_parts()
    skin, gown, cuff = m.mannequin()
    display, handle = m.lid_fittings()
    return dict(tub=tub, canopy=cq.Compound.makeCompound([glass, caps]), band=band,
                patient=cq.Compound.makeCompound([skin, gown, cuff]), display=display)


def test_G000_overlap_check_detects_a_real_collision(model):
    """Control: the checker must report a collision when one exists (shift the patient up 300 mm)."""
    lifted = model["patient"].translate(V(0, 0, 300))
    assert overlap(lifted, model["canopy"]) > 1000.0
    assert lifted.distance(model["canopy"]) < 1e-6  # float noise, not exactly 0


def test_G001_patient_fits_inside_closed_capsule(model):
    """No part of a 1755 mm patient touches the shell, and there is >= 150 mm of air
    between the patient and the lid (comfort / claustrophobia margin, our assumption)."""
    assert overlap(model["patient"], model["canopy"]) == 0.0
    assert overlap(model["patient"], model["tub"]) == 0.0
    assert model["patient"].distance(model["canopy"]) >= 150.0


@pytest.mark.parametrize("x0", [-800, -500, -200, 100, 350, 600, 800])
def test_G002_scanner_ring_clears_patient_over_full_travel(model, x0):
    """The moving ring and its sensors keep >= 50 mm from the patient at every position
    (pinch/contact margin for a moving part, our assumption)."""
    ring, glow, carriages, sensors = m.scanner(x0)
    moving = cq.Compound.makeCompound([ring] + [s for s, _ in sensors.values()])
    assert overlap(moving, model["patient"]) == 0.0
    assert moving.distance(model["patient"]) >= 50.0


@pytest.mark.parametrize("x0", m.RING_TRAVEL)
def test_G003_scanner_ring_stays_inside_shell(model, x0):
    ring, *_ = m.scanner(x0)
    assert overlap(ring, model["canopy"]) == 0.0
    assert overlap(ring, model["tub"]) == 0.0
    assert overlap(ring, model["display"]) == 0.0


def test_G004_lid_display_inside_lid(model):
    assert overlap(model["display"], model["canopy"]) == 0.0


def test_G005_open_lid_clears_tub_and_floor(model):
    lid = m.rotate_lid(model["canopy"])
    assert overlap(lid, model["tub"]) == 0.0
    assert overlap(lid, model["band"]) == 0.0
    assert lid.BoundingBox().zmin > 800.0


def test_G006_patient_can_get_in_with_lid_open(model):
    """With the lid open, the space above the bed on the entry side (-y) is clear up to
    2000 mm, so nothing blocks a person climbing in."""
    lid = m.rotate_lid(model["canopy"])
    entry = m.box((0, -300, 1450), (2000, 600, 1100))
    assert overlap(lid, entry) == 0.0
