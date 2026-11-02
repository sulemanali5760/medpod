#!/usr/bin/env bash
# Reinstall the MedPod cloud toolchain (Ubuntu). Cloud containers are not persistent.
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq calculix-ccx ngspice xvfb libgl1 libxrender1 libglu1-mesa libosmesa6 libegl1
pip install --break-system-packages -q cadquery gmsh numpy scipy matplotlib pytest meshio pyvista trimesh pint
ccx -v | head -2
python3 -m pytest -q
