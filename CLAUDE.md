# MedPod — rules for every Claude session

Read `STATE.md` first: it says where the project is and what's next. Then `docs/`.

## 1. Truth and sources (owner's rule #1)
- Never state a number, formula, API call or keyword from memory alone. Get it from an
  **official source** (vendor docs, standard, manual, datasheet) or **prove it by test**.
- Record every source used in `docs/knowledge-log.md` (what, where, version, used for).
- Anything not yet verified is marked **Draft** / **Unverified** and listed in `docs/limitations.md`.
- If an official source can't be reached, say so plainly. Don't fill the gap with a guess.

## 2. Test everything (owner's rule #2)
- Each tool, formula and design must pass a test before it is used for the next step.
- Formulas: check against an independent method (numerical integration, FEA, or a
  published worked example), never against themselves.
- FEA tools: must reproduce closed-form benchmarks (`tests/test_fea_benchmarks.py`)
  before being used on a real part.
- Designs: each part gets a test with its requirement as the pass criterion
  (e.g. safety factor ≥ 2 under 180 kg).
- Every new discovery becomes a regression test. Never delete a test to make things pass;
  if a test was wrong, fix it and log why in `docs/verification-log.md`.
- Run `python3 -m pytest` before every commit. Report failures honestly.

## 3. Work loop (from GSD Core, open-gsd/gsd-core)
Each unit of work is a **phase**: Discuss → Plan → Execute → Verify → Ship.
- **Discuss:** agree decisions with the owner; record in `docs/decision-log.md`.
- **Plan:** write the plan and its acceptance criteria in `STATE.md` before building.
- **Execute:** small commits, one completed task each.
- **Verify:** tests pass and the result matches the requirement, not just "it ran".
- **Ship:** commit, push, update `STATE.md`, show the owner a rendered picture of the result.
- State lives in files, not in chat. A new session must be able to continue from the repo alone.
- When in doubt, make the phase smaller.

## 4. Coding (from andrej-karpathy-skills and Ponytail)
- State assumptions; if a request is ambiguous, ask. Push back when a simpler way exists.
- Smallest complete change: no speculative features, abstractions or options.
- Reuse what exists (project code, standard library, installed deps) before adding anything.
- Touch only what the task needs; match existing style.
- Turn tasks into verifiable goals: "write the test, then make it pass".
- Never cut: input validation, safety checks, calibration, error handling that prevents data loss.
- Mark known shortcuts in code: `shortcut: <limit>, <when to upgrade>`.

## 5. Project conventions
- Units: **N, mm, MPa, W, K, s** everywhere (match SolidWorks MMGS and CalculiX decks).
- CAD: parametric in code. CadQuery (cloud) → STEP → SolidWorks (owner's PC).
  SolidWorks macros live in `cad/macros/`; the owner runs them, or a local Claude session
  drives SolidWorks through its API.
- Simulation: CalculiX (cloud) for checks; SolidWorks Simulation / ANSYS Student on the
  owner's PC for final verification. Results must agree within stated tolerances.
- Medical safety: patient-connected electronics battery-powered or isolated (IEC 60601-1).
- This is a research prototype, never presented as a medical device.

## 6. Environment
- Cloud sessions: run `bash tools/setup_cloud.sh` first (tools are not persistent).
- Skills for this project: `.claude/skills/` (calculix-fea, engineering-calcs, solidworks-api,
  karpathy-guidelines, anatomy).
