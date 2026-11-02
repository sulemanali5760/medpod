# Components (capsule design)

**Status key:** *Provisional* = the envelope (size, field of view) is a placeholder chosen to be
typical of the product class. It has **not** been checked against a datasheet, because vendor sites
are blocked from the cloud session. Each one must be replaced by datasheet values before ordering
parts or making final decisions.

| # | Component | Purpose | Product class (to pick a model) | Envelope used in model | Status |
|---|---|---|---|---|---|
| C01 | RGB-D camera (ring top) | Face and body video: heart rate (rPPG), breathing, facial expression, 3D body shape | Stereo depth camera module | 40 × 100 × 30 mm, 3 lenses; FOV cone half-angle 36° | Provisional |
| C02 | Thermal camera (ring +30°) | Skin temperature map, fever, inflammation | Radiometric LWIR thermal core | 60 × 60 × 45 mm; FOV half-angle 28° | Provisional |
| C03 | mmWave radar (ring −30°) | Contactless breathing and heart motion | 60 GHz FMCW radar sensor | 80 × 70 × 18 mm; FOV half-angle 45° | Provisional |
| C04 | LED light bars ×2 | Even lighting for camera vital signs | High-CRI LED strip | 100 × 30 × 12 mm | Provisional |
| C05 | Microphones ×2 | Cough and breathing sounds, voice | MEMS microphone | 25 × 25 × 15 mm | Provisional |
| C06 | Scanner ring + rails + carriages | Carries C01–C05 head to toe (travel ±800 mm) | Linear guide + belt or ball-screw drive | Ring 1074 × 914 mm outer, 130 wide, 70 deep | Design |
| C07 | ECG hand electrodes ×2 | Lead-I ECG from both palms | Dry stainless/Ag-AgCl plates + isolated ECG front-end | 110 × 70 × 3 mm | Provisional |
| C08 | ECG back electrodes ×4 | Additional leads through the back | Dry electrodes in cushion | Ø60 mm | Provisional; dry-electrode signal quality is an open research question |
| C09 | SpO2 finger clip | Blood oxygen, pulse | Medical pulse-oximetry module | 60 × 40 × 40 mm | Provisional |
| C10 | Automatic BP cuff | Blood pressure | Oscillometric NIBP module | Ø132 mm × ~150 mm sleeve | Provisional |
| C11 | Finger-prick analyser port | Future: glucose, haemoglobin etc. | Point-of-care cartridge analyser | 90 × 70 × 60 mm | Future module |
| C12 | Robotic ultrasound arm | Future: guided ultrasound | Compact 6-axis arm + probe | Parked at foot end | Future module |
| C13 | Load cells ×4 | Body weight, movement | Shear-beam load cells | Ø44 × 25 mm | Provisional |
| C14 | Patient display (inside lid) | Instructions and calming content | Small LCD | 220 × 150 × 12 mm | Provisional |
| C15 | Operator console | Start scan, view results | Tablet on floor stand | 330 × 230 mm | Provisional |
| C16 | Compute unit | Runs the AI triage | Edge AI computer | 220 × 160 × 70 mm | Provisional |
| C17 | Isolated medical PSU | Mains → low voltage with patient isolation | IEC 60601-1 rated supply | 260 × 130 × 90 mm | Provisional |
| C18 | Battery pack | Runs sensors off-mains during scan | Li-ion pack with BMS | 380 × 170 × 110 mm | Provisional |
| C19 | Cooling fans ×2 + vents | Electronics cooling; fresh air through cap slots for the patient | Axial fans | Ø110 mm | Provisional, airflow not yet calculated |
| C20 | Lid: polycarbonate canopy + end caps, hinge, 2 gas struts | Enclosure, opens 70° | Thermoformed PC, gas springs | 8 mm wall | Design; strut force not yet calculated |
| C21 | Emergency stop | Stops ring motion, releases lid | Mushroom-head E-stop | Ø80 base | Provisional |

## Overall size
- Capsule 2620 × 1120 mm (plus trim), top at 1380 mm; pedestal 1800 × 720 mm on 4 castors.
- Patient space: fits a 1755 mm adult with 236 mm clearance to the lid (test G-001).
- **Issue:** 1136 mm wide (over the trim) won't pass a standard ~900 mm doorway. It needs a
  wide door or must come apart (lid off). Logged in limitations.
