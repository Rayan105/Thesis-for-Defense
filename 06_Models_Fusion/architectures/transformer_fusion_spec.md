# Architectural Specification — `CVD-MM-Transformer` (`MC0015` / `STEP-023`)

| Field | Value |
|---|---|
| Document | `06_Models_Fusion/architectures/transformer_fusion_spec.md` |
| Version | v1.0.0 (`UD14` Approved Architecture Blueprint) |
| Framework (`UD13`) | **PyTorch (`torch >= 2.1`)** |
| Consumed Release | `REL0001` (`rel0001_{train,val,test}.jsonl` — exact shapes verified compatible) |
| Parameter Regime | **Compact EPV-Governed (`< 250K` core fusion + backbone params)** |
| Governing Section | OS §6.2–§6.3, §12.1 (`UD14`, `UD26`); Blueprint `STEP-023` |

---

## 1. Exact Input Tensor Contracts Consumed From `REL0001`

Because `REL0001` enforces **Zero Cross-Cohort Stitching (`DEC0004` / `DEC0006`)** and **Unit Isolation (`DS0003 mg/dL` vs `DS0004 ordinal 1–3`)**, the architecture accepts heterogeneous cohort batches seamlessly through **modality-type tokenizers + `ModalityMask_CELS` key-padding masking**:

1. **Modality Presence Mask (`ModalityMask_CELS`):** Shape `(B, 4)` boolean/int tensor `[has_C, has_E, has_L, has_S]`.
   - `DS0001 PTB-XL`: `[1, 1, 0, 0]`
   - `DS0002 CARDIO-ML-ED`: `[1, 1, 1, 0]` (`329` paired PNGs) or `[1, 0, 1, 0]` (`226` `MISSING_ECG`)
   - `DS0003 CAIR-CVD-2025`: `[1, 0, 1, 1]`
   - `DS0004 sulianova`: `[1, 0, 1, 1]`
2. **Tabular Modality Decomposed Input (`TabularFeatures`):**
   Each cohort block (`DS0001: 11d`, `DS0002: 15d`, `DS0003: 31d`, `DS0004: 25d` — already standardized with Train-only `RobustScaler` + `_isnan` MNAR indicators) maps its semantic column slices cleanly into **three modality-specific latent tokens (`(B, d_model)` each, `d_model = 64`)**:
   - **Clinical Adapter ($\phi_C^{(ds)}$):** Maps demographic & vital features + `_isnan` flags (`age, sex, height, weight, bmi, sbp, dbp, pr`) -> `z_C ∈ R^(B × 64)`.
   - **Laboratory Adapter ($\phi_L^{(ds)}$):** Separate linear+LayerNorm+GELU heads for continuous ED labs (`DS0002`: `creatinine, wbc` + `_isnan`), continuous BD fasting labs (`DS0003`: `tc, hdl, ldl, fbs` + `_isnan`), and screening ordinal tiers (`DS0004`: `chol_tier, gluc_tier`), outputting `z_L ∈ R^(B × 64)` (`zeros` + masked when `has_L == 0`).
   - **Lifestyle Adapter ($\phi_S^{(ds)}$):** Maps `smoking, family_history, activity_level` (`DS0003`) and `smoking, alcohol, activity` (`DS0004`) -> `z_S ∈ R^(B × 64)` (`zeros` + masked when `has_S == 0`).
3. **Dual-Track ECG Encoders ($\phi_E$ -> `z_E ∈ R^(B × 64)`):**
   - **Digital 12-Lead WFDB Track (`DS0001 PTB-XL`, `(B, 12, 5000)` @ `500 Hz` or `(B, 12, 1000)` @ `100 Hz`):**
     Compact `ResNet-1D` stem (`Conv1d(12 -> 32, k=15, stride=2)` -> `3` residual squeeze-excite temporal blocks `[32 -> 48 -> 64]` with adaptive global average + max pooling -> linear projection to `(B, 64)`). Total params: **`~78,000`**.
   - **Paper 12-Row PNG Scan Track (`DS0002 CARDIO-ML-ED`, `(B, 1, 256, 768)` cleaned red-grid inverted ink):**
     Compact `4`-stage depthwise/standard `Conv2d` backbone (`[1 -> 16 -> 32 -> 48 -> 64]` with BatchNorm + GELU + AdaptiveAvgMaxPool -> projection to `(B, 64)`). Total params: **`~62,000`**.
     *Note:* Optional `STEP-024/028` ablation tests initializing `2D` conv features or cross-transfer representations on `PTB-XL` rendered 12-lead synthetic images if beneficial (`never pretraining on DS0002 Val/Test`).

---

## 2. Cross-Modal Transformer Fusion Block (`d_model = 64`)

1. **Sequence Assembly (`5` Tokens Per Encounter):**
   Concatenate a learnable **`[CLS]`** token `(B, 1, 64)` + the four modality tokens **`[z_C, z_E, z_L, z_S]`** `(B, 4, 64)` -> `H_0 ∈ R^(B × 5 × 64)`, adding learnable **Modality-Type Positional Embeddings** `E_type ∈ R^(1 × 5 × 64)`.
2. **Zero-Artifact Missing-Modality Key-Padding Mask (`OS §4.5 #1`):**
   Construct `key_padding_mask ∈ {False, True}^(B × 5)`:
   - Column `0` (`[CLS]`): always `False` (unmasked).
   - Columns `1..4`: `~ModalityMask_CELS.bool()` (`True` = ignored by softmax attention!).
   - Thus **`z_E`, `z_L`, or `z_S` when absent contributes ZERO key/value leakage** to cross-attention — eliminating dummy zero-filling bias cleanly!
   - **Training Modality Dropout (`p_drop = 0.15` on non-clinical `[E, L, S]` when `>1` modality present):** Forces `[CLS]` + remaining modalities to calibrate robustly for inference-time missing-modality stress tests (`Block F`).
3. **Transformer Encoder Stack:**
   - `num_layers = 2`, `nhead = 4`, `d_model = 64`, `dim_feedforward = 128`, `dropout = 0.25`, `norm_first = True` (Pre-LN `TransformerEncoderLayer` for stable gradient flow across small & large cohorts).
   - Transformer core params: **`~68,000`**.
4. **Calibrated Risk Prediction Head:**
   - Extracts `h_cls = H_L[:, 0, :]` -> `LayerNorm(64) -> Dropout(0.30) -> Linear(64, 1)` logit `z_hat`.
   - Trained with cohort-stratified weighted **`BCEWithLogitsLoss(pos_weight=pos_weight_train)`** (and post-hoc Platt/Temperature calibration on `Validation` ONLY at `STEP-032`).

---

## 3. Parameter Budget vs EPV Audit (`UD26` Safeguard)

| Component / Scope | Trainable Params | Train Events ($E_{\text{train}}$) | EPV / Regularization Assessment |
|---|---|---|---|
| **Tabular Adapters + Fusion Core (`C, L, S` + `2L` Transformer)** | `~85K` total (`shared core ~68K + ~4K per cohort adapter`) | `34,216` combined Train events (`23,749` `DS0004`, `9,747` `DS0001`, `487` `DS0003`) | **Healthy:** Combined tabular/fusion core ratio `> 0.4` events/param (`<<` overparameterized) & heavily regularized (`Dropout 0.25–0.30`, `WeightDecay 1e-2`). |
| **`DS0001 PTB-XL` WFDB `ResNet-1D` Branch** | `~78K` | `9,747` Train positive events (`16,929` rows) | Compact `1D-ResNet` avoids memorizing `5000`-step waveforms. |
| **`DS0002 CARDIO-ML-ED` `2D-CNN` + Per-Cohort Tuning** | `~62K` (CNN) + `~68K` (Fusion, shared/frozen option) | `233` Train events (`390` Train rows; `231` PNG) | **Critical `UD26` Rule:** When fine-tuning solely inside low-$N$ `DS0002`, freeze or share backbone + heavy dropout (`0.35`) + `5`-fold Train CV (`CVFoldInTrain 0..4`) instead of training multi-million ViT/ResNet50 weights! |
| **Rejected Heavy Backbones (`MC0016`)** | `25M–90M+` (`ViT-B/16`, `ResNet50`, `ECG-FM`) | `233` (`DS0002`) | **REJECTED** due to severe overfitting & unverified private checkpoint provenance. |

---

## 4. Pretrained Weight Provenance & `REL0001` Schema Compatibility
- **Baseline & Proposed Models (`MC0001–MC0015`):** All architectures train cleanly **from deterministic seeded initialization** directly on `REL0001` (`zero unverified weights`). If `UD26` self-supervised `PTB-XL` pretraining is tested as a sensitivity run (`Block E`), it trains **exclusively on `REL0001` `DS0001 Train`** (`StratFold 1–8`), never touching external unvetted weights or `Val/Test`.
- **Schema Feedback Check to `G08`:** Every tensor dimension (`11, 15, 31, 25` tabular; `(12, 5000)` / `(12, 1000)` WFDB; `(1, 256, 768)` cleaned PNG; `4D` `ModalityMask_CELS`) matches **`REL0001` identically** — **zero changes to `PP0001` or `REL0001` required**.
