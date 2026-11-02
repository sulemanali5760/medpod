"""MedPod capsule - full parametric model (CadQuery / OpenCascade).

Coordinates: x = along the body (head at +x), y = width, z = up. Units: mm. Floor at z = 0.
All component envelopes marked PROVISIONAL in docs/02-components.md until checked
against manufacturer datasheets.
"""
import math

import cadquery as cq
from OCP.BRepBuilderAPI import BRepBuilderAPI_GTransform
from OCP.gp import gp_GTrsf, gp_Mat

V = cq.Vector

# ---------------- main parameters ----------------
RY, RZ = 560.0, 480.0    # capsule outer half-width (y) and half-height (z)
LC = 1500.0              # length of the straight (cylindrical) section
T = 8.0                  # shell wall thickness
ZC = 900.0               # capsule axis height = lid split line
BED_TOP = 860.0          # cushion top surface
LID_OPEN_DEG = 70.0      # lid opening angle
HINGE = (0.0, RY + 20.0, ZC + 16.0)  # hinge axis point (axis parallel to x), offset outward
RING_RY, RING_RZ, RING_W, RING_D = 537.0, 457.0, 130.0, 70.0  # scanner ring outer radii, width, depth
RING_TRAVEL = (-800.0, 800.0)          # scanner ring travel along x
PATIENT_H = 1755.0                     # mannequin stature (approx. 50th percentile adult male)


# ---------------- geometry helpers ----------------
def gscale(shape, sx, sy, sz):
    g = gp_GTrsf()
    g.SetVectorialPart(gp_Mat(sx, 0, 0, 0, sy, 0, 0, 0, sz))
    return cq.Shape.cast(BRepBuilderAPI_GTransform(shape.wrapped, g, True).Shape())


def box(c, d):
    return cq.Solid.makeBox(d[0], d[1], d[2], V(c[0] - d[0] / 2, c[1] - d[1] / 2, c[2] - d[2] / 2))


def rbox(c, d, r):
    """Box with all edges filleted."""
    return cq.Workplane().box(*d).edges().fillet(r).val().translate(V(*c))


def rod(p0, p1, r):
    d = V(*p1) - V(*p0)
    return cq.Solid.makeCylinder(r, d.Length, V(*p0), d.normalized())


def capsule_rod(p0, p1, r):
    s = rod(p0, p1, r)
    for p in (p0, p1):
        s = s.fuse(cq.Solid.makeSphere(r, V(*p), angleDegrees1=-90, angleDegrees2=90))
    return s


def ellipsoid(c, a, b, cc):
    s = cq.Solid.makeSphere(a, angleDegrees1=-90, angleDegrees2=90)
    return gscale(s, 1.0, b / a, cc / a).translate(V(*c))


def pill(ry, rz, lc=LC, zc=ZC):
    """Capsule solid: cylinder along x with hemispherical ends, then squashed to height rz."""
    s = cq.Solid.makeCylinder(ry, lc, V(-lc / 2, 0, 0), V(1, 0, 0))
    for x in (-lc / 2, lc / 2):
        s = s.fuse(cq.Solid.makeSphere(ry, V(x, 0, 0), angleDegrees1=-90, angleDegrees2=90))
    return gscale(s.clean(), 1.0, 1.0, rz / ry).translate(V(0, 0, zc))


def ring_yz(x0, ry_o, rz_o, ry_i, rz_i, width, z_cut):
    """Elliptical ring in the YZ plane centred on the capsule axis, cut below z_cut."""
    r = (cq.Workplane("YZ", origin=(x0 - width / 2, 0, ZC))
         .ellipse(ry_o, rz_o).ellipse(ry_i, rz_i).extrude(width).val())
    return r.cut(box((x0, 0, z_cut - 1000), (width + 10, 3000, 2000)))


def compound(shapes):
    return cq.Compound.makeCompound(list(shapes))


def rotate_lid(shape, deg=LID_OPEN_DEG):
    p = V(*HINGE)
    return shape.rotate(p, p + V(1, 0, 0), -deg)


# ---------------- shell, lid, pedestal ----------------
def shell_parts():
    outer, inner = pill(RY, RZ), pill(RY - T, RZ - T)
    shell = outer.cut(inner)
    below = box((0, 0, ZC - 1500), (4000, 3000, 3000))
    tub = shell.intersect(below)
    canopy = shell.cut(below)
    mid = box((0, 0, ZC + 1500), (LC, 3000, 3000))
    glass = canopy.intersect(mid)
    caps = canopy.cut(mid)
    # ventilation slots in both end caps (fresh-air in at the feet, out at the head)
    for xs in (-1, 1):
        for i in range(6):
            caps = caps.cut(box((xs * 1090, -75 + i * 30, ZC + 380), (140, 12, 260)))
    band = pill(RY + 8, RZ + 8).cut(pill(RY - 4, RZ - 4)).intersect(
        box((0, 0, ZC - 1), (4000, 3000, 26)))
    led = pill(RY + 10, RZ + 10).cut(pill(RY, RZ)).intersect(box((0, 0, ZC - 1), (4000, 3000, 6)))
    return tub, glass, caps, band, led


def pedestal_parts():
    body = (cq.Workplane("XY").slot2D(1800, 720).extrude(620).val()
            .translate(V(0, 0, 110)).cut(pill(RY + 8, RZ + 8)))
    for side in (-1, 1):
        for i in range(25):
            body = body.cut(box((-480 + i * 40, side * 360, 360), (14, 30, 140)))
    plinth = cq.Workplane("XY").slot2D(1640, 600).extrude(35).val().translate(V(0, 0, 75))
    casters = []
    for x in (-720, 720):
        for y in (-210, 210):
            casters.append(rod((x, y - 16, 37), (x, y + 16, 37), 37))
            casters.append(box((x, y, 62), (30, 44, 30)))
    electronics = {
        "compute_unit": box((-250, 0, 330), (220, 160, 70)),
        "isolated_psu": box((230, 0, 330), (260, 130, 90)),
        "battery_pack": box((0, 0, 190), (380, 170, 110)),
        "cooling_fans": compound([rod((s * 520, 300, 360), (s * 520, 340, 360), 55) for s in (-1, 1)]),
    }
    return body, plinth, compound(casters), electronics


# ---------------- bed, rails, docks ----------------
def bed_parts():
    inner = pill(RY - T, RZ - T)
    deck = inner.intersect(box((0, 0, 770), (4000, 3000, 20)))
    cushion = rbox((0, 0, 820), (2000, 600, 80), 30)
    headrest = rbox((830, 0, BED_TOP + 25), (260, 380, 50), 20).cut(
        ellipsoid((830, 0, BED_TOP + 50 + 65), 150, 110, 90))
    load_cells = compound([rod((x, y, 735), (x, y, 760), 22) for x in (-800, 800) for y in (-200, 200)])
    rails = compound([box((0, s * 501, 830), (1700, 24, 100)) for s in (-1, 1)])
    hand_rests = compound([rbox((-75, s * 300, BED_TOP + 17.5), (370, 110, 35), 15) for s in (-1, 1)])
    ecg_hand = compound([box((-60, s * 300, BED_TOP + 36.5), (110, 70, 3)) for s in (-1, 1)])
    ecg_back = compound([rod((x, y, BED_TOP - 2.5), (x, y, BED_TOP + 0.5), 30)
                         for x in (600, 250) for y in (-90, 90)])
    spo2 = rbox((-175, -270, 917), (60, 40, 40), 10)
    analyzer = rbox((-80, 395, 900), (90, 70, 60), 8).cut(box((-80, 395, 930), (50, 6, 20)))
    return {
        "deck": deck, "cushion": cushion, "headrest": headrest, "load_cells": load_cells,
        "rails": rails, "hand_rests": hand_rests, "ecg_hand_electrodes": ecg_hand,
        "ecg_back_electrodes": ecg_back, "spo2_finger_clip": spo2, "blood_analyzer_port": analyzer,
    }


# ---------------- scanner ring and sensors ----------------
SENSORS = [  # (angle from top deg, name, (dx, dy, dz), lenses [(ly, r)], colour)
    (0, "rgbd_camera", (40, 100, 30), [(-35, 8), (0, 6), (35, 8)], "#1b1b1b"),
    (30, "thermal_camera", (60, 60, 45), [(0, 16)], "#5a1a14"),
    (-30, "mmwave_radar", (80, 70, 18), [], "#e8e8e8"),
    (60, "led_bar", (100, 30, 12), [], "#fff6d5"),
    (-60, "led_bar", (100, 30, 12), [], "#fff6d5"),
    (82, "microphone", (25, 25, 15), [], "#333333"),
    (-82, "microphone", (25, 25, 15), [], "#333333"),
]


def sensor_pose(x0, theta_deg):
    ry_i, rz_i = RING_RY - RING_D, RING_RZ - RING_D
    t = math.radians(theta_deg)
    y, z = ry_i * math.sin(t), ZC + rz_i * math.cos(t)
    a = math.degrees(math.atan2(-y, z - ZC))
    return (x0, y, z), a


def scanner(x0):
    ry_i, rz_i = RING_RY - RING_D, RING_RZ - RING_D
    ring = ring_yz(x0, RING_RY, RING_RZ, ry_i, rz_i, RING_W, ZC - 20)
    glow = compound([ring_yz(x0 + s * 53, ry_i + 3, rz_i + 3, ry_i - 4, rz_i - 4, 8, ZC - 20)
                     for s in (-1, 1)])
    carriages = compound([box((x0, s * 501, 885), (160, 50, 30)) for s in (-1, 1)])
    sensors = {}
    for theta, name, (dx, dy, dz), lenses, colour in SENSORS:
        body = box((0, 0, -dz / 2), (dx, dy, dz))
        parts = [body] + [cq.Solid.makeCylinder(r, 5, V(0, ly, -dz), V(0, 0, -1)) for ly, r in lenses]
        m = compound(parts)
        (px, py, pz), a = sensor_pose(x0, theta)
        m = m.rotate(V(0, 0, 0), V(1, 0, 0), a).translate(V(px, py, pz))
        key = f"{name}_{theta:+d}" if name in ("led_bar", "microphone") else name
        sensors[key] = (m, colour)
    return ring, glow, carriages, sensors


# ---------------- lid-mounted parts, exterior ----------------
def lid_fittings():
    display = (box((0, 0, 0), (12, 220, 150)).rotate(V(0, 0, 0), V(0, 1, 0), -49)
               .translate(V(1010, 0, 1230)))
    handle = compound([rod((-250, -580, 960), (250, -580, 960), 12)] +
                      [rod((x, -548, 960), (x, -582, 960), 9) for x in (-220, 220)])
    return display, handle


def gas_struts(lid_open):
    """Two gas struts on the hinge side. Lid end follows the lid rotation."""
    out = []
    for x in (-900, 900):
        a = V(x, RY - 40, ZC - 60)
        b = rotate_lid(cq.Vertex.makeVertex(x, RY - 140, ZC + 260), LID_OPEN_DEG if lid_open else 0).Center()
        mid = a + (b - a) * 0.55
        out += [rod(a.toTuple(), mid.toTuple(), 14), rod(mid.toTuple(), b.toTuple(), 7)]
    return compound(out)


def exterior_parts():
    hinges = compound([rod((x - 60, HINGE[1], HINGE[2]), (x + 60, HINGE[1], HINGE[2]), 16)
                       for x in (-550, 550)] +
                      [box((x, RY + 8, ZC + 4), (110, 26, 30)) for x in (-550, 550)])
    estop = compound([rod((-700, -562, 860), (-700, -578, 860), 40)])
    estop_btn = rod((-700, -578, 860), (-700, -605, 860), 28)
    console = compound([
        rod((1700, -350, 0), (1700, -350, 25), 230),
        rod((1700, -350, 25), (1700, -350, 1150), 25),
        rod((1700, -350, 1150), (1640, -350, 1200), 18),
    ])
    tablet = (box((0, 0, 0), (15, 330, 230)).rotate(V(0, 0, 0), V(0, 1, 0), -25)
              .translate(V(1625, -350, 1260)))
    return hinges, estop, estop_btn, console, tablet


def ultrasound_arm():
    """Future module: compact robotic ultrasound arm parked at the foot end."""
    pts = [(-1100, 0, 780), (-1100, 0, 840), (-1100, 0, 1000), (-1010, 0, 1110), (-1040, 0, 1170)]
    radii = [60, 40, 32, 22]
    return compound([capsule_rod(pts[i], pts[i + 1], radii[i]) for i in range(4)] +
                    [rod((-1040, 0, 1170), (-1060, 0, 1215), 18)])


# ---------------- mannequin ----------------
def mannequin():
    """Supine adult, stature PATIENT_H. Segment positions use common anthropometric
    proportions of stature (APPROXIMATE - to be checked against ANSUR II data)."""
    H, top = PATIENT_H, 930.0
    x = lambda frac_from_floor: top - (1 - frac_from_floor) * H  # noqa: E731
    sh, elb, wr, hip, kn, ank = x(0.818), x(0.630), x(0.485), x(0.530), x(0.285), x(0.039)
    skin, gown = [], []
    skin.append(ellipsoid((top - 114, 0, 1000), 114, 78, 100))                 # head
    skin.append(rod((top - 228, 0, 960), (sh, 0, 960), 55))                    # neck
    gown.append(ellipsoid(((sh + hip) / 2 + 40, 0, 975), (sh - hip) / 2 + 20, 175, 112))  # chest
    gown.append(ellipsoid((hip + 25, 0, 955), 125, 170, 95))                   # pelvis
    for s in (-1, 1):
        gown.append(capsule_rod((sh, s * 205, 950), (elb, s * 250, 925), 48))  # upper arm
        skin.append(capsule_rod((elb, s * 250, 925), (wr, s * 268, 915), 40))  # forearm
        skin.append(ellipsoid((wr - 95, s * 270, 917), 95, 45, 22))            # hand
        gown.append(capsule_rod((hip, s * 95, 950), (kn, s * 95, 935), 78))    # thigh
        skin.append(capsule_rod((kn, s * 95, 935), (ank, s * 90, 920), 55))    # shin
        skin.append(ellipsoid((ank - 25, s * 90, 975), 50, 42, 85))            # foot
    cuff = rod((sh + 0.3 * (elb - sh), -219, 942), (sh + 0.75 * (elb - sh), -239, 932), 66).cut(
        rod((sh + 0.25 * (elb - sh), -217, 943), (sh + 0.8 * (elb - sh), -241, 931), 50))
    return compound(skin), compound(gown), cuff


# ---------------- assembly ----------------
def build(ring_x=350.0, lid_open=False, patient=True):
    """Returns {name: (shape, colour, opacity)}."""
    tub, glass, caps, band, led = shell_parts()
    body, plinth, casters, electronics = pedestal_parts()
    display, handle = lid_fittings()
    hinges, estop, estop_btn, console, tablet = exterior_parts()
    ring, glow, carriages, sensors = scanner(ring_x)
    lid = {"canopy_glass": (glass, "#9fd8ff", 0.22), "canopy_caps": (caps, "#f4f6f8", 1.0),
           "patient_display": (display, "#0d1b2a", 1.0), "lid_handle": (handle, "#8a939c", 1.0)}
    if lid_open:
        lid = {k: (rotate_lid(s), c, o) for k, (s, c, o) in lid.items()}
    parts = {
        "tub": (tub, "#f4f6f8", 1.0), "seam_band": (band, "#c9d1d9", 1.0), "led_strip": (led, "#38e8ff", 1.0),
        "pedestal": (body, "#e9edf1", 1.0), "plinth": (plinth, "#2a2f36", 1.0), "casters": (casters, "#1c1f24", 1.0),
        "hinges": (hinges, "#8a939c", 1.0), "estop_base": (estop, "#f2c500", 1.0), "estop_button": (estop_btn, "#d0021b", 1.0),
        "console_stand": (console, "#c9d1d9", 1.0), "console_tablet": (tablet, "#0d1b2a", 1.0),
        "scanner_ring": (ring, "#f7f9fb", 1.0), "scanner_glow": (glow, "#38e8ff", 1.0),
        "ring_carriages": (carriages, "#5c6670", 1.0), "ultrasound_arm": (ultrasound_arm(), "#ff8c1a", 1.0),
        "gas_struts": (gas_struts(lid_open), "#2f3439", 1.0),
    }
    colours = {"deck": "#9aa4ae", "cushion": "#2b4c7e", "headrest": "#35609e", "load_cells": "#c0c0c0",
               "rails": "#6b7580", "hand_rests": "#35609e", "ecg_hand_electrodes": "#d4af37",
               "ecg_back_electrodes": "#d4af37", "spo2_finger_clip": "#6c7a89", "blood_analyzer_port": "#e9edf1"}
    for k, s in bed_parts().items():
        parts[k] = (s, colours[k], 1.0)
    for k, s in electronics.items():
        parts[k] = (s, {"compute_unit": "#3a7d44", "isolated_psu": "#555b61",
                        "battery_pack": "#b8860b", "cooling_fans": "#2f3439"}[k], 1.0)
    for k, (s, c) in sensors.items():
        parts[k] = (s, c, 1.0)
    parts.update(lid)
    if patient:
        skin, gown, cuff = mannequin()
        parts["patient_skin"] = (skin, "#d9a383", 1.0)
        parts["patient_gown"] = (gown, "#a9c6de", 1.0)
        parts["bp_cuff"] = (cuff, "#30343a", 1.0)
    return parts


if __name__ == "__main__":
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    asm = cq.Assembly(name="medpod_capsule")
    for name, (shape, colour, _) in build(patient=False).items():
        asm.add(shape, name=name, color=cq.Color(colour))
    os.makedirs(f"{root}/cad/parts", exist_ok=True)
    asm.export(f"{root}/cad/parts/medpod_capsule.step")
    print("exported cad/parts/medpod_capsule.step")
