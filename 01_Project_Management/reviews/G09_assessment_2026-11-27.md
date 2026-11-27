# G09 Assessment — Architecture Lock, Runtime Readiness & Smoke/Recovery Audit (`STEP-027`)

| Field | Value |
|---|---|
| TemplateID | T22 (gate_audit.md) |
| template_version | v1.0.0 |
| AssessmentID | `G09-20261127-01` |
| GateID | `G09` |
| DocumentOrEntityScope | `environment/model/`, `DEC0009–0012`, `07_Experiments/experiment_plan.md`, `09_Evaluation_Stats/protocol.md`, `10_Explainability_XAI/xai_protocol.md`, `src/cvd_mm/`, `tests/`, `EXP0000_SMOKE`, `CKPT0001` |
| EntityVersions | `environment/model` v1.0.0; `REL0001` v1.0.0; `T32` v1.0.0; `EXP0000_SMOKE` v1.0.0; `CKPT0001` v1.0.0 |
| Outcome | **`NOT ASSESSED`** *(Technical criteria **`C1–C4` 100% PASS** verified across `32/32` unit tests, real `REL0001` local CPU drill, Kaggle GPU `cuda` smoke execution, `CKPT0001` SHA-256 parity retrieval, and `0` Test reads; formal **`PASS`** awaits Supervisor confirmation of **`DEC0009–DEC0012`** (`UD13–UD21, UD24`) & **`G09`**)* |
| Assessor | Rayan Ahmed (`232-15-847`), Mohammad Nafis Sadiq (`232-15-895`) |
| Human Approver | Md. Mizanur Rahman (`Supervisor`) + Method/Evaluation Reviewer |
| Assessment Date | `2026-11-27` *(Pending Supervisor Sign-Off)* |
| Governing References | OS §6, §11, §14.1, §14.2 (`G09`); Blueprint `STEP-023`–`STEP-027` |
| PHI Sensitivity | Tier 1 (Public / Git-safe audit; Tier 3 `.pt` weights excluded via `.gitignore`) |

---

## 1. Mandatory Criteria Audit Matrix (`STEP-027` / `OS §14.2 G09`)

| Criterion # | Mandatory Criterion | Evidence Path & Verified Measurements | Technical Status | Action / Notes |
|---|---|---|---|---|
| **C1** | **Runtime, Architecture & Protocol Lock:** `environment/model/` pinned, `MC0001–MC0017` defined, `Blocks A–F` + Calibration/Stats + XAI protocols SHA-256 frozen. | [requirements.txt](file:///e:/FYDP/environment/model/requirements.txt) (`7b0553ce...`), [candidates.csv](file:///e:/FYDP/06_Models_Fusion/candidates.csv), [preregistration_hashes.json](file:///e:/FYDP/07_Experiments/preregistration_hashes.json) | **PASS** | `32/32` unit tests (`-W error`) + `validate_repo.py` clean. |
| **C2** | **End-to-End Classical & 4-Modality Transformer Smoke Runs (`Train`/`Val` Only):** Finite loss/gradients across `DS0001–04`, zero `NaN` on missing masks, WFDB DSP check, zero Test reads. | [smoke_kaggle_g09_report.json](file:///e:/FYDP/07_Experiments/EXP0000_SMOKE/smoke_kaggle_g09_report.json), [smoke_local_report.json](file:///e:/FYDP/07_Experiments/EXP0000_SMOKE/smoke_local_report.json), [test_access_log.csv](file:///e:/FYDP/03_Datasets_Cohort/splits/test_access_log.csv) | **PASS** | Kaggle CUDA (`XGB AUROC=0.768026`, `CVDMMTransformer=129,169 params`, `missing_masks_zero_nan=true`); Local WFDB `12x5000` verified; `test_partition_accessed=false`. |
| **C3** | **Checkpoint Interruption, Tier 3 SHA-256 Backup & State Restoration:** Interrupt mid-run, retrieve Tier 3 backup, verify SHA-256, resume training cleanly. | [checkpoint_policy.md](file:///e:/FYDP/08_Checkpoints/checkpoint_policy.md), [CKPT0001.md](file:///e:/FYDP/08_Checkpoints/manifests/CKPT0001.md), [checkpoint_registry.csv](file:///e:/FYDP/08_Checkpoints/checkpoint_registry.csv) | **PASS** | Kaggle `CKPT0001` (`1,691,308 B`, SHA-256 `18824d5e3c858bc52591a1ccf75a9af4998dda00bf64cfa2934e749603240b82`) restored & resumed Epochs `3–4` with finite losses; Local drill proved bitwise `max_weight_diff=0.0`. |
| **C4** | **Diagnostic Calibration & XAI Faithfulness Hook Verification:** Validation-only calibrator + Train-only SHAP additivity `<= 0.02` + AOPC vs controls. | [smoke_kaggle_g09_report.json](file:///e:/FYDP/07_Experiments/EXP0000_SMOKE/smoke_kaggle_g09_report.json), [smoke_local_report.json](file:///e:/FYDP/07_Experiments/EXP0000_SMOKE/smoke_local_report.json) | **PASS** | Kaggle `TreeSHAP` err=`7.15e-07`, `KernelSHAP` err=`2.98e-08`; Local AOPC `del_top=0.101628 > rand=0.030764 > rev=0.000202`, `shortcut_free=true`. |
| **C5** | **Human / Supervisor Ratification (`UD13–UD21, UD24`):** Supervisor & Method Reviewer confirm framework lock, compact Transformer budget, prospective Q1 plan & smoke recovery. | [DEC0009.md](../decision_log/DEC0009.md) – [DEC0012.md](../decision_log/DEC0012.md) | **AWAITING SUPERVISOR SIGN-OFF** | Team/Supervisor confirmation promotes `G09` to **`PASS`** and unlocks **`Stage S11` (`STEP-028+`)**. |

---

## 2. Determination & Unblocking Path
- **Overall Outcome:** **`NOT ASSESSED`** *(Empirical technical readiness **`100% PASS`** across local CPU and Kaggle `cuda` GPU; confirm Supervisor ratification of **`DEC0009–DEC0012`** & **`G09`** to launch controlled `Blocks A–F` experiments in **`Stage S11`**).*
