"""Render the MedPod capsule to docs/img/. Run: python3 cad/render_capsule.py"""
import math
import os
import sys

import numpy as np
import pyvista as pv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import medpod_capsule as m  # noqa: E402

OUT = f"{ROOT}/docs/img"
GLOW = {"led_strip", "scanner_glow", "led_bar_+60", "led_bar_-60"}
SHELL = {"tub", "canopy_caps", "pedestal", "scanner_ring", "seam_band", "blood_analyzer_port"}
METAL = {"gas_struts", "rails", "hinges", "lid_handle", "load_cells", "ecg_hand_electrodes", "ecg_back_electrodes",
         "console_stand", "ring_carriages"}
_cache = {}


def to_mesh(shape, key):
    if key not in _cache:
        verts, tris = shape.tessellate(0.4, 0.15)
        pts = np.array([[v.x, v.y, v.z] for v in verts])
        faces = np.hstack([np.full((len(tris), 1), 3), np.array(tris)]).ravel()
        _cache[key] = pv.PolyData(pts, faces).compute_normals(split_vertices=True, feature_angle=35)
    return _cache[key]


def plotter(title, subtitle):
    pl = pv.Plotter(off_screen=True, window_size=(1920, 1200), lighting="none")
    pl.set_background("#0b1220", top="#24344f")
    pl.add_light(pv.Light(position=(2500, -3500, 4000), focal_point=(0, 0, 800), intensity=0.9))
    pl.add_light(pv.Light(position=(-3000, 2500, 3000), focal_point=(0, 0, 800), intensity=0.45))
    pl.add_light(pv.Light(position=(0, -1500, -800), focal_point=(0, 0, 800), intensity=0.25))
    pl.add_light(pv.Light(light_type="headlight", intensity=0.25))
    floor = pv.Disc(center=(0, 0, -1), inner=0, outer=3200, c_res=120)
    pl.add_mesh(floor, color="#141c2b", ambient=0.3, specular=0.3)
    pl.add_text(title, position=(30, 1140), font_size=17, color="white")
    pl.add_text(subtitle, position=(30, 1105), font_size=10, color="#9fb3c8")
    pl.add_text("MedPod research prototype - not a medical device. Sensor envelopes provisional.",
                position=(30, 20), font_size=9, color="#6f8296")
    return pl


def add_parts(pl, parts, tag, clip=None, hide=()):
    for name, (shape, colour, opacity) in parts.items():
        if name in hide:
            continue
        mesh = to_mesh(shape, f"{tag}:{name}")
        if clip and name in clip:
            mesh = mesh.clip(normal=(0, 1, 0), origin=(0, 0, 0), invert=False)  # keep y >= 0
            if mesh.n_points == 0:
                continue
        kw = dict(color=colour, opacity=opacity, smooth_shading=True)
        if name in GLOW:
            kw.update(ambient=1.0, diffuse=0.0, specular=0.0)
        elif name in METAL:
            kw.update(pbr=True, metallic=0.85, roughness=0.3)
        elif name in SHELL:
            kw.update(ambient=0.32, diffuse=0.75, specular=0.6, specular_power=40)
        elif name == "canopy_glass":
            kw.update(specular=1.0, specular_power=80, ambient=0.15)
        else:
            kw.update(pbr=True, metallic=0.05, roughness=0.35)
        pl.add_mesh(mesh, **kw)


def shoot(pl, name, cam):
    pl.camera_position = cam
    pl.enable_anti_aliasing("ssaa")
    pl.screenshot(f"{OUT}/{name}.png")
    pl.close()
    print("wrote", name)


def sensor_cones(pl, x0):
    """Field-of-view cones. Half-angles are ASSUMED (typical class values) - verify from datasheets."""
    fov = {"rgbd_camera": (0, 36, "#7cffb2"), "thermal_camera": (30, 28, "#ff7a59"),
           "mmwave_radar": (-30, 45, "#c38bff")}
    for name, (theta, half, colour) in fov.items():
        (px, py, pz), a = m.sensor_pose(x0, theta)
        ar = math.radians(a)
        d = np.array([0.0, math.sin(ar), -math.cos(ar)])  # sensor facing direction (-z rotated by a)
        h = 520.0
        apex = np.array([px, py, pz]) + d * 40
        cone = pv.Cone(center=apex + d * h / 2, direction=-d, height=h,
                       radius=h * math.tan(math.radians(half)), resolution=80, capping=False)
        pl.add_mesh(cone, color=colour, opacity=0.22, ambient=0.6)
        pl.add_mesh(cone.extract_feature_edges(), color=colour, opacity=0.6, line_width=2)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    closed = m.build(ring_x=350, lid_open=False, patient=True)
    opened = m.build(ring_x=350, lid_open=True, patient=True)
    empty = m.build(ring_x=-450, lid_open=True, patient=False)

    pl = plotter("MedPod capsule - closed, scan in progress",
                 "Scanner ring at chest: RGB-D camera, thermal camera, 60 GHz radar, lights, microphones")
    add_parts(pl, closed, "closed")
    shoot(pl, "capsule_01_hero", [(2600, -3300, 2300), (0, 0, 750), (0, 0, 1)])

    pl = plotter("MedPod capsule - lid open (gas-strut hinge, 70 deg)",
                 "Patient on contoured bed: hand rests with ECG electrodes, SpO2 clip, BP cuff, blood-analyser port")
    add_parts(pl, opened, "open")
    shoot(pl, "capsule_02_open", [(-3300, -3700, 3000), (0, 250, 1000), (0, 0, 1)])

    pl = plotter("MedPod capsule - cutaway",
                 "Pedestal: battery, isolated medical PSU, compute unit, fans | bed on 4 load cells | ring on rails")
    add_parts(pl, closed, "closed", hide={"console_stand", "console_tablet"},
              clip={"tub", "seam_band", "led_strip", "pedestal", "plinth", "canopy_glass", "canopy_caps",
                    "deck", "rails", "scanner_ring", "scanner_glow", "ring_carriages",
                    "casters", "lid_handle", "estop_base", "estop_button"})
    shoot(pl, "capsule_03_cutaway", [(500, -3600, 1300), (0, 0, 650), (0, 0, 1)])

    pl = plotter("MedPod capsule - sensor coverage (assumed fields of view)",
                 "Green: RGB-D camera | Orange: thermal camera | Purple: mmWave radar. Lid hidden for clarity.")
    add_parts(pl, closed, "closed", hide={"canopy_glass", "canopy_caps", "patient_display", "lid_handle",
                                          "console_stand", "console_tablet"})
    sensor_cones(pl, 350)
    shoot(pl, "capsule_04_sensors", [(2200, -2300, 2500), (300, 0, 950), (0, 0, 1)])

    pl = plotter("MedPod capsule - empty interior",
                 "ECG back electrodes in cushion, hand-rest electrodes, finger-prick analyser port, "
                 "ultrasound arm (future module) parked at feet")
    add_parts(pl, empty, "empty", hide={"console_stand", "console_tablet"})
    shoot(pl, "capsule_05_interior", [(-2300, -3000, 3400), (-100, 250, 950), (0, 0, 1)])
