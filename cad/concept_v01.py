"""MedPod v0.1 concept: bed frame of 40x40 T-slot (simplified as square bars), padded platform,
sensor arch over the chest. Dimensions are DRAFT (see docs/01-requirements.md M1-M6).
Run: python3 cad/concept_v01.py  -> cad/parts/concept_v01.step + docs/img/concept_v01.png
"""
import os

import cadquery as cq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = 40.0                      # T-slot profile size (mm)
L, W, H = 2000.0, 700.0, 650.0  # bed length, width, top-of-platform height (M1, M4)
BOARD, PAD = 18.0, 60.0         # platform board and pad thickness
RAIL_TOP = H - PAD - BOARD      # top face of frame rails
ARCH_X, ARCH_H = 1450.0, 1350.0  # arch position (chest) and top height


def bar(p0, p1):
    """Square P x P bar between two points that differ along one axis."""
    (x0, y0, z0), (x1, y1, z1) = p0, p1
    dx, dy, dz = abs(x1 - x0) or P, abs(y1 - y0) or P, abs(z1 - z0) or P
    c = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    return cq.Workplane().box(dx, dy, dz).translate(c)


def frame():
    h = P / 2
    legs = [bar((x, y, 0), (x, y, RAIL_TOP)) for x in (h, L - h) for y in (h, W - h)]
    legs += [bar((L / 2, y, 0), (L / 2, y, RAIL_TOP - P)) for y in (h, W - h)]  # mid legs
    z = RAIL_TOP - h
    rails = [bar((0, y, z), (L, y, z)) for y in (h, W - h)]
    rails += [bar((x, P, z), (x, W - P, z)) for x in (h, 500, 1000, 1500, L - h)]
    rails += [bar((P, y, 150), (L - P, y, 150)) for y in (h, W - h)]  # lower stretchers
    parts = legs + rails
    out = parts[0]
    for p in parts[1:]:
        out = out.union(p)
    return out


def arch():
    h, top = P / 2, ARCH_H
    ups = [bar((ARCH_X, y, RAIL_TOP), (ARCH_X, y, top)) for y in (-h, W + h)]
    beam = bar((ARCH_X, -P, top - h), (ARCH_X, W + P, top - h))
    out = ups[0].union(ups[1]).union(beam)
    return out


def sensors():
    z = ARCH_H - P
    cam = cq.Workplane().box(60, 90, 50).translate((ARCH_X, W / 2 - 80, z - 25))
    thermal = cq.Workplane().box(60, 70, 60).translate((ARCH_X, W / 2 + 80, z - 30))
    lens = (cq.Workplane("XY").circle(15).extrude(15)
            .translate((ARCH_X, W / 2 - 80, z - 65)))
    lens2 = (cq.Workplane("XY").circle(18).extrude(15)
             .translate((ARCH_X, W / 2 + 80, z - 75)))
    mic = cq.Workplane().box(30, 30, 20).translate((ARCH_X, W / 2, z - 10))
    return cam.union(lens), thermal.union(lens2), mic


def platform():
    board = cq.Workplane().box(L, W, BOARD).translate((L / 2, W / 2, RAIL_TOP + BOARD / 2))
    pad = (cq.Workplane().box(L - 20, W - 20, PAD).edges("|X or |Y").fillet(20)
           .translate((L / 2, W / 2, RAIL_TOP + BOARD + PAD / 2)))
    pillow = (cq.Workplane().box(300, 450, 80).edges().fillet(30)
              .translate((L - 220, W / 2, H + 35)))
    return board, pad, pillow


def enclosure():
    return cq.Workplane().box(400, 300, 150).translate((700, W / 2, RAIL_TOP - P - 75))


def build():
    board, pad, pillow = platform()
    cam, thermal, mic = sensors()
    return {
        "frame": (frame(), "#b8c0c8"),
        "arch": (arch(), "#9aa4ae"),
        "board": (board, "#c9a26b"),
        "pad": (pad, "#3f7fbf"),
        "pillow": (pillow, "#7fb2e5"),
        "camera": (cam, "#222222"),
        "thermal_camera": (thermal, "#c0392b"),
        "microphone": (mic, "#555555"),
        "electronics_box": (enclosure(), "#2e8b57"),
    }


if __name__ == "__main__":
    import pyvista as pv

    parts = build()
    asm = cq.Assembly(name="medpod_concept_v01")
    for name, (shape, color) in parts.items():
        asm.add(shape, name=name, color=cq.Color(color))
    os.makedirs(f"{ROOT}/cad/parts", exist_ok=True)
    asm.save(f"{ROOT}/cad/parts/concept_v01.step")

    os.makedirs(f"{ROOT}/docs/img", exist_ok=True)
    tmp = "/tmp/claude-0/stl"
    os.makedirs(tmp, exist_ok=True)
    for view, cam_pos, fname in [
        ("iso", [(L * 1.9, -W * 3.2, 2300), (L / 2, W / 2, 500), (0, 0, 1)], "concept_v01.png"),
        ("head", [(L * 2.4, W * 1.6, 1300), (L / 2, W / 2, 600), (0, 0, 1)], "concept_v01_head.png"),
    ]:
        pl = pv.Plotter(off_screen=True, window_size=(1600, 1000))
        pl.set_background("white")
        for name, (shape, color) in parts.items():
            f = f"{tmp}/{name}.stl"
            cq.exporters.export(shape, f, tolerance=0.5, angularTolerance=0.2)
            pl.add_mesh(pv.read(f), color=color, smooth_shading=False, specular=0.2)
        floor = pv.Plane(center=(L / 2, W / 2, 0), i_size=L * 1.6, j_size=W * 3.5)
        pl.add_mesh(floor, color="#eeeeee")
        pl.add_text(f"MedPod v0.1 concept (draft)  -  {L:.0f} x {W:.0f} mm bed, "
                    f"{H:.0f} mm high, sensor arch at chest", font_size=11, color="black")
        pl.camera_position = cam_pos
        pl.enable_eye_dome_lighting() if view == "none" else None
        pl.screenshot(f"{ROOT}/docs/img/{fname}")
        pl.close()
    print("saved STEP and images")
