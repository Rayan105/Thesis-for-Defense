# Cardiologist Explanation Plausibility Summary (`XAI0001` / `STEP-040`)

- **Packet Location (Restricted Tier 2B):** `04_Outcome_Schema_QA/adjudications/clinician_review_n24_s15.json` (`24` stratified de-identified Test encounters: `6 TP, 6 FP, 6 TN, 6 FN` spanning `DS0001–DS0004`).
- **Observed Multimodal Case Plausibility Examples:** Acute `DS0001` positives allocate `89.5%–93.8%` attribution to 12-lead WFDB ECG waveforms; ED `DS0002` scanned-ECG true positive balances `44.4%` Clinical + `45.3%` ECG + `10.4%` Lab; Bangladeshi `DS0003` cases reflect `Lifestyle` (`40.8%–51.6%`) + `Clinical` (`33.3%–57.2%`) + `Lab` (`7.3%–25.9%`).
- **Review Status:** **`PENDING_EXT_CARDIOLOGIST_SIGN_OFF`** — External cardiologist must score pathophysiology concordance (`1–3`), multimodal clarity (`1–3`), and any implausible drivers across all `24` packets prior to ratifying Gate `G14`.
- **Permitted Claim Boundary (`OS §8.3`):** Explanations strictly describe frozen model attribution behavior (`faithfulness, stability, shortcut-freedom`); biological causality and unmeasured *'improved clinician trust/speed'* claims remain strictly prohibited.
