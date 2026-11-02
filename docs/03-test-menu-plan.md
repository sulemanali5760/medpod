# Test Menu Plan — general-purpose, affordable screening pod

**Owner direction (2026-11-02):** keep MedPod general-purpose. Target the most common conditions
in low- and middle-income countries (LMICs), at a price people there can afford, so they can get a
yearly check-up and know what they're facing. Venom testing stays as a later module.

## Why this matters (sourced)
- The Lancet Commission on Diagnostics (Oct 2021) found 47% of the world's population have
  little or no access to diagnostics. Only ~19% of people in low and lower-middle income countries
  can get the simplest tests, other than HIV and malaria. Its tracer conditions are diabetes,
  hypertension, HIV and TB, plus hepatitis B and syphilis in pregnancy.
  [PMC8494468](https://pmc.ncbi.nlm.nih.gov/articles/PMC8494468/), [PMC8654090](https://pmc.ncbi.nlm.nih.gov/articles/PMC8654090)
- In the WHO African Region, 6 of the top 10 causes of death in 2019 were communicable diseases.
  It's the only region where HIV/AIDS and malaria are still in the top 10.
  [WHO visual summary](https://www.who.int/data/stories/leading-causes-of-death-and-disability-2000-2019-a-visual-summary)

## Method: build the menu from official lists, not guesses
1. **WHO Model List of Essential In Vitro Diagnostics (EDL 4, 2023)**, Tier I: the tests WHO says
   belong in community settings and facilities with no laboratory. Source: WHO Technical Report
   Series 1053 (iris.who.int) and the electronic EDL (edl.who-healthtechnologies.org).
   EDL 3 had 142 unique tests. **Not yet fetched: WHO sites are still blocked in this session.**
2. **Burden ranking:** WHO Global Health Estimates 2000–2021 (deaths/DALYs by country and income
   group) and IHME GBD, to rank conditions by burden in LMICs.
3. **Non-lab measurements the pod already has:** blood pressure, ECG, SpO2, temperature, weight/BMI,
   breathing, vision/eye photos (to research), cough sounds (TB screening research, to verify).
4. For each condition record: test type (pod sensor / rapid cartridge / reader + AI / not feasible),
   specimen, approximate cost per test (from supplier or WHO/Global Fund price lists), evidence
   for accuracy, and the official guideline the result maps to.

## Pod architecture this implies
- **Sensors (no consumables):** vitals, ECG, SpO2, temperature, weight, camera, microphone.
- **Cartridge reader:** one camera-based reader with controlled lighting and AI that reads WHO-listed
  rapid tests (e.g. malaria, HIV, syphilis, hepatitis B/C, pregnancy, haemoglobin, glucose, urine
  dipstick). Each new test is a new cartridge, not new hardware.
- **Finger-prick sampling** at the hand rest feeds the cartridges.

## Safety and ethics rules (non-negotiable)
- Results lead to a **clinician, pharmacist or telemedicine referral** following WHO and national
  guidelines. The pod does not prescribe. Self-treating from a screen result risks wrong treatment
  and antibiotic resistance.
- Every result shows its uncertainty and "see a health worker" thresholds.
- Data privacy: results belong to the patient. Offline-first.

## Next actions (need WHO sites reachable)
1. Fetch EDL 4 Tier I in full → `data/who_edl4_tier1.csv` (verbatim, with source and version).
2. Fetch GHE 2021 cause-specific DALYs for low and lower-middle income groups → rank.
3. Join them → `docs/04-test-menu.md`: ranked conditions × test method × cost × evidence.
