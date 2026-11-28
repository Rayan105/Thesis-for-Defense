# Spurious-Shortcut & MNAR Confounder Audit (`XAI0001` / `STEP-040`)

| Model & Cohort | Max Additivity RelErr | Top-3 Attributed Features | MNAR `_isnan` Flag in Top-3? | Outcome |
|---|---:|---|---|---|
| `MC0004_XGB_DS0001` | `8.3e-07` | `age_years(0.7540); weight_kg_isnan(0.3951); sex__F(0.2297)` | YES (**SHORTCUT_FLAG**) | SHORTCUT_DETECTED |
| `MC0004_XGB_DS0002` | `6.2e-07` | `dbp_mmhg(0.4793); sbp_mmhg(0.3940); age_years(0.3030)` | No | **CLEAN** |
| `MC0004_XGB_DS0003` | `8.1e-07` | `age_years(0.4907); smoking_status(0.4725); activity_level__Low(0.4608)` | No | **CLEAN** |
| `MC0004_XGB_DS0004` | `6.9e-07` | `sbp_mmhg(0.6991); age_years(0.3076); cholesterol_tier(0.2673)` | No | **CLEAN** |
| `MC0015_CVDMM_DS0001` | `0.032514` | `age_years(0.2089); sex__M(0.0800); sex__F(0.0641)` | No | **CLEAN** |
| `MC0015_CVDMM_DS0002` | `0.032514` | `pr_bpm(1.3725); age_years(0.6672); sbp_mmhg(0.5465)` | No | **CLEAN** |
| `MC0015_CVDMM_DS0003` | `0.032514` | `activity_level__Low(0.8456); family_history_cvd(0.6677); smoking_status(0.5768)` | No | **CLEAN** |
| `MC0015_CVDMM_DS0004` | `0.032514` | `sbp_mmhg(1.0333); age_years(0.4205); weight_kg(0.2088)` | No | **CLEAN** |

## Key Comparative Shortcut Finding
- **Baseline XGBoost (`MC0004` on `DS0001`):** **`SHORTCUT_DETECTED`** — `weight_kg_isnan` (`MeanAbsSHAP = 0.3951`) ranked **`#2` overall** above biological sex and weight (`0.0650`), confirming that unimodal tabular trees exploit PTB-XL's clinic anthropometry-recording pattern.
- **Proposed Champion `CVD-MM-Transformer` (`MC0015`):** **`CLEAN` across 4/4 cohorts (`0/4` MNAR flags in Top-3)** — driven consistently by clinical pathophysiology (`age_years`, `sbp_mmhg`, `pr_bpm`, `weight_kg`, `activity_level__Low`, `family_history_cvd`, `smoking_status`) alongside 12-lead ECG waveform representations (`78.50%` ECG share on `DS0001`, `28.49%` on `DS0002`), plus distributed `10`-window temporal and `4x8` spatial ECG attributions (`ecg_temporal_spatial_map.csv`) without isolated border/noise spikes.
