---
name: solidworks-api
description: Write or run SolidWorks API macros (VBA .swp/.bas, or Python/C# over COM) to build MedPod parts and assemblies. Use for any SolidWorks automation task.
---

# SolidWorks API (MedPod)

## Status: official reference NOT yet loaded
The cloud session cannot reach help.solidworks.com. Until the official reference is in
`references/`, do not write API calls from memory. If you must, mark each call
**Unverified** and have the owner run it on a test part first.

## How to load the official reference (on the owner's Windows PC)
SolidWorks installs its API help locally. A local Claude session should:
1. Find the help files under the SolidWorks install folder, usually
   `C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\api\`. Look for `apihelp.chm` and the
   `swconst` help. Confirm the exact names on the PC.
2. Decompile the CHM to HTML (`hh.exe -decompile <outdir> apihelp.chm`, built into Windows).
3. Extract the pages for the interfaces we use (ISldWorks, IModelDoc2, IModelDocExtension,
   ISketchManager, IFeatureManager, IPartDoc, IAssemblyDoc, IComponent2, IMate2,
   swconst enums) into `references/` as text. Record the SolidWorks version.

## Workflow
- Geometry is designed in CadQuery (`cad/`) and exported to STEP, which is the source of truth
  for shape. SolidWorks macros are for native features, drawings, materials and Simulation studies.
- SolidWorks API internal units are **metres and radians**, even when the document uses mm.
  Verify this against the official help once it's loaded.
- Every macro gets a check: after it runs, compare mass and bounding box with the CadQuery
  model (`cad/` test). They must agree within 0.5%.
