# Test Menu v0.1: Draft

**Status:** Draft, for owner review. Built 2026-11-02 from official WHO sources. Cost and accuracy
columns are not filled in yet (see "Gaps").
**Data:** `data/test_menu.csv` (machine-readable), `data/README.md` (sources, licence).
**Checked by:** `tests/test_test_menu_data.py` (T-001…T-007 in `docs/verification-log.md`).
**Picture:** `docs/img/test_menu.png`

![Test menu](img/test_menu.png)

## What changed since the plan (important)
1. **WHO's current list is EDL 5, not EDL 4.** The electronic EDL now says "Fifth WHO model list of
   essential in vitro diagnostics (EDL 5)", © WHO 2025. EDL 5 replaces EDL 4's "Tier I / Tier II"
   with **Setting: Non-laboratory / Laboratory** plus a "tiered testing service" (community/outreach,
   primary health care centre without laboratory, district hospital, …). I fetched both:
   - EDL 4 Tier I: 39 rows from WHO TRS 1053 (`data/who_edl4_tier1.csv`).
   - EDL 5 (all 234 rows, 39 Non-laboratory): `data/who_edl5.csv`.
   The menu uses **EDL 5 Non-laboratory**, because it is the newer list. Proposed as D-007, needs owner OK.
2. **Moving from EDL 4 Tier I to EDL 5** (from the row-by-row cross-check):
   - Moved to Laboratory: ABO/Rh slide agglutination, ESR, HBeAg (specimen also changed to serum/plasma),
     HIV qualitative and quantitative NAT, influenza NAT, hCG latex agglutination.
   - Not found in EDL 5: urine bilirubin dipstick, influenza A/B antigen RDT, TB skin tests (TST/TBST).
   - New in EDL 5 Non-laboratory: microhaematocrit, G6PD (POC test and RDT), Kato-Katz, lead,
     total cholesterol, creatinine, HCV self-test, cholera dipstick.
3. **GHE 2021 DALYs could not be fetched.** www.who.int, cdn.who.int and the GHO API are blocked from
   the cloud (proxy 403; web-fetch "ENOTFOUND"). What I could get: the **2021 top-10 causes of death by
   World Bank income group** from *World health statistics 2024*, Fig. 1.9 (on iris.who.int), which uses
   GHE 2021. So the ranking below uses **deaths, not DALYs**. The order may change once DALYs are added.

## Burden: top 10 causes of death, 2021 (WHO GHE 2021 via WHS 2024 Fig. 1.9)
| Rank | Low-income | Lower-middle-income |
|---|---|---|
| 1 | Lower respiratory infections | COVID-19 |
| 2 | Stroke | Ischaemic heart disease |
| 3 | Ischaemic heart disease | Stroke |
| 4 | Malaria | Chronic obstructive pulmonary disease |
| 5 | Preterm birth complications | Lower respiratory infections |
| 6 | COVID-19 | Tuberculosis |
| 7 | Diarrhoeal diseases | Diarrhoeal diseases |
| 8 | Tuberculosis | Diabetes mellitus |
| 9 | Birth asphyxia and birth trauma | Cirrhosis of the liver |
| 10 | HIV/AIDS | Preterm birth complications |

## Pod methods
- **Pod sensor:** no consumable (BP, ECG, SpO2, temperature, weight, camera, microphone).
- **Cartridge reader:** a WHO-listed lateral-flow RDT or dipstick, read by the pod's camera under
  controlled light. Accuracy of camera reading is **unverified** and needs its own test per cartridge.
- **Handheld analyser:** EDL "point-of-care test" formats that need an instrument (glucose, HbA1c,
  Hb, cholesterol, creatinine, CD4, G6PD, lead). We would integrate an existing meter, not build one.
- **Refer:** test exists only in the Laboratory setting, or the EDL purpose says it must not be used
  for individual diagnosis.

## The menu
Priority **A** = top-10 cause of death in LIC or LMIC *and* an EDL 5 Non-laboratory test.
**B** = EDL 5 Non-laboratory test, burden rank pending (not in the top 10 deaths; DALYs not fetched).
**C** = top-10 cause with no IVD: pod sensor or referral. Draft until a WHO guideline is sourced.
EDL ids link to `https://edl.who-healthtechnologies.org/recommendations/<id>`.

| Pri | Condition | GHE 2021 rank (LIC / LMIC) | EDL 5 ids | Pod method | Notes |
|---|---|---|---|---|---|
| A | Malaria | 4 / – | 34, 114, 115 | cartridge reader | Plasmodium RDT. G6PD informs primaquine/tafenoquine (EDL purpose). Pod refers, never prescribes. |
| A | HIV infection | 10 / – | 24, 25, 26, 29, 30 | cartridge reader | Antibody RDTs. CD4 (29) needs an instrument; CrAg (30) is only for advanced HIV disease. |
| A | Tuberculosis | 8 / 6 | 32 | cartridge reader (limited) | Urine LAM only for people living with HIV (EDL purpose). All other EDL 5 TB tests are Laboratory: refer. Cough-sound AI is Draft research. |
| A | COVID-19 | 6 / 1 | 16 | cartridge reader | Antigen RDT, upper respiratory swab. |
| A | Diabetes mellitus | – / 8 | 4, 19, 17, 5 | handheld analyser | Capillary glucose, HbA1c; urine glucose only if blood glucose is unavailable; ketones. |
| A | Cardiovascular risk (IHD, stroke) | 3, 2 / 2, 3 | 227 | handheld analyser | Total cholesterol: "to assess risk of cardiovascular disease". |
| A | Chronic hepatitis B and C | cirrhosis – / 9 | 20, 22, 233 | cartridge reader | HBsAg RDT, anti-HCV RDT and self-test. **Draft:** the share of cirrhosis caused by HBV/HCV in LIC/LMIC is not sourced yet. |
| A | Diarrhoeal disease (cholera) | 7 / 7 | 14, 15 | refer | EDL: cholera RDTs "cannot be used to confirm individual cholera cases". Outbreak surveillance flag only. |
| C | Hypertension | (IHD, stroke) | – | pod sensor | BP isn't an IVD, so it isn't in the EDL. **Draft:** thresholds must come from the WHO hypertension guideline (fetch from IRIS). |
| C | Lower respiratory infections | 1 / 5 | – | pod sensor → refer | No EDL 5 non-lab IVD (CRP is Laboratory). SpO2, temperature, breathing rate. **Draft:** danger-sign thresholds need a WHO source. |
| C | COPD | – / 4 | – | refer | No IVD. Spirometry isn't in pod v0.1. Possible future module. |
| – | Preterm birth, birth asphyxia | 5, 9 / 10 | – | out of scope | Newborn conditions; the capsule is built for adults (D-006). |
| B | Anaemia | – | 8 (97) | handheld analyser | Hb POC (8). Microhaematocrit (97): equipment needs not yet checked. |
| B | Syphilis | – | 37, 38 | cartridge reader | Treponemal RDT; dual HIV/syphilis RDT. |
| B | Kidney disease, UTI | – | 3, 6, 228 | cartridge reader + analyser | Urine albumin and urinalysis dipsticks; creatinine POC. |
| B | Pregnancy | – | 10, 11 | cartridge reader | Urine beta-hCG. |
| B | Sickle cell disease | – | 36 | cartridge reader | Haemoglobin A/S/C RDT. |
| B | Hepatitis E | – | 23 | cartridge reader | anti-HEV IgM RDT. |
| B | Group A strep pharyngitis | – | 35 | cartridge reader | Throat swab: who takes it in an unattended pod is an open question. |
| B | Blood group ABO/Rh | – | 1 | cartridge reader | Reading an agglutination card by camera is unverified. |
| B | Lead exposure | – | 226 | handheld analyser | |
| B | Chagas, visceral leishmaniasis | – | 13, 39 | cartridge reader | Only where these diseases occur. |
| B | Soil-transmitted helminths, schistosomiasis | – | 174 | refer | Kato-Katz is stool microscopy, so the pod can't do it. |

## What this means for the pod (proposal, for discussion)
- One **cartridge reader** is the main method for 13 of the 23 rows. It is the single most useful piece of hardware
  after the vitals sensors. Most of those tests use **capillary whole blood**, so the finger-prick
  station in the plan is confirmed as needed.
- A small set of **handheld analysers** (glucose/HbA1c, Hb, cholesterol, creatinine) covers the
  noncommunicable-disease side. These are instrument tests in the EDL, not RDTs.
- A suggested first cartridge set, all priority A and all capillary blood RDTs: **malaria, HIV,
  HBsAg, anti-HCV**, plus syphilis (B, but it shares the dual HIV/syphilis RDT). For the NCD side:
  **glucose/HbA1c and cholesterol**, plus the BP cuff. This is a proposal, not a decision.

## Gaps (also in `docs/limitations.md`)
1. **GHE 2021 DALYs** by income group: blocked (www.who.int). Need the owner to allow `www.who.int`
   and `cdn.who.int`, or to download the GHE 2021 DALY spreadsheet on the PC and add it to `data/`.
2. **Cost per test:** not sourced. Next sources: Global Fund Pooled Procurement price list, UNICEF
   Supply Catalogue, WHO prequalification lists. None tried yet.
3. **Accuracy per test:** each e-EDL page has a "Summary of Evidence Evaluation". These aren't extracted yet.
4. **Camera reading of RDTs:** no evidence collected yet. Needs a literature search and our own bench test.
5. **Referral thresholds** (BP, SpO2, glucose, Hb): must come from the relevant WHO guidelines on IRIS.
6. EDL is a *model* list. Each country has its own national EDL and guidelines, so a deployment must
   follow its national list.
