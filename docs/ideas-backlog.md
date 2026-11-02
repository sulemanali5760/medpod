# Ideas Backlog

Ideas parked for later, so they aren't lost. Each one gets its own research pass before any work.

## Active direction — rapid test platform inside MedPod (owner, 2026-11-02)
- Goal: MedPod runs 100–200 rapid tests, not "every test in the world".
- Architecture idea: **one reader, many cartridges.** A camera-based reader with AI reads lateral-flow
  and colour-change test cartridges. Each new test is a new cartridge, not new hardware.
  The same reader can go in the capsule and in a portable field kit.
- First target test: **snake venom detection** for trekkers and remote areas.

### Snake venom — what the research says (2026-11-02 web search, to verify in primary sources)
- Snakebite is classed as a neglected tropical disease. Estimates are 1.8–2.7 million envenomings and
  81,000–138,000 deaths a year (systematic review, secondary source; WHO figure to confirm).
- Lateral-flow venom tests are active research but mostly prototypes. A 2021 review said only the
  Australian Snake Venom Detection Kit was commercial at the time.
- Main problem: antibodies are species-specific. A test made for one snake species can fail on others
  (Bangladesh study of the Taiwan Cobra Rapid Test).
- Bedside fallback in use today: the **20-minute whole blood clotting test (20WBCT)**, recommended
  in WHO snakebite guidelines. It detects venom-induced coagulopathy, not the species.
  It's cheap but has a high false-negative rate in some studies (60% accuracy in one Pakistani study),
  and it's sensitive to technique (glass tube, no detergent).
- Opportunity for MedPod: a reader + AI that standardises reading of 20WBCT and venom strips,
  plus region-specific species panels.
- Safety rule: the device must never delay evacuation or antivenom. First-aid advice only from
  official guidelines (WHO / national), never generated.

Sources: PMC8530336, PMC10831076, bioRxiv 10.1101/2022.09.26.509137, PMC8405032,
PLoS NTD 10.1371/journal.pntd.0009657, MIT Solve 102286, PAFMJ 3684.

## Parked ideas
| Idea | Notes |
|---|---|
| Field deploy kit / portable pod | Backpack or case version of the test reader for trekking and remote clinics |
| Private-jet escape pod | Prior art to study: whole-aircraft ballistic parachutes on small planes, crew escape capsules on some military jets. Needs aviation certification. Separate project. |
| Dedicated AI chip | Very high cost and specialist field. Start by using existing edge-AI chips; revisit later. |
