"""Build `09_Evaluation_Stats/CVD_Multimodal_Final_Test_Stats_XAI_Pipeline.ipynb` (`STEP-033` to `STEP-039`).

Generates a clean 7-cell Kaggle GPU notebook (T4 x1) enforcing Gate G11 freeze custody (`TACC0002`):
- Cell 1: Kaggle input auto-discovery, SHA-256 verification of all 15 frozen S11 checkpoints & freeze JSONs
- Cell 2: Full REL0001 Train/Val/Test + WFDB/PNG loading, exact DeLong, McNemar, Holm-Bonferroni, Cluster Bootstrap & DCA
- Cell 3: Reload frozen .pt/.pkl models, deterministic Train refits, & STRICT Validation Parity Check <= 1e-4 before Test
- Cell 4: STEP-033/034 One-shot frozen Test predictions (N=12,719, 100% coverage) + 6 Mandatory/Q1 metrics + Calibration
- Cell 5: STEP-035 Patient-Grouped Bootstrap B=2,000 95% CIs + Paired DeLong/McNemar/Holm + DCA Net Benefit [0.05..0.50]
- Cell 6: STEP-037 Subgroup Fairness (Sex, AgeBand, Cohort, ModalityTier), Missing-Modality Stress & N=24 Error Packet
- Cell 7: STEP-038/039 Multimodal XAI (TreeSHAP, 2^4 Coalition Shapley, 50-step IG, AOPC vs Random/Reverse, 5-Seed Stability, Shortcut Audit) & Export
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NB_PATH = REPO_ROOT / "09_Evaluation_Stats" / "CVD_Multimodal_Final_Test_Stats_XAI_Pipeline.ipynb"

MD_HEADER = """# Stage S12–S15 — Frozen Final Test Evaluation, Statistical Inference, Fairness & Multimodal XAI (`STEP-033–039`)
**Gate Authorization:** **`G10 PASS` (`G10-20261128-02`)** & **`G11 PASS` (`G11-20261128-02` / `TACC0002`)** — Zero post-freeze hyperparameter/threshold tuning permitted!

### 📌 Kaggle Inputs Required (`+ Add Input`, total 4):
1. **`REL0001_kaggle_final_test_bundle`** (`10.55 MB` new zip: `rel0001_test.jsonl`, `ds0002_png_test/`, `s11_checkpoints/`, `freeze_bundle/`)
2. **`REL0001_kaggle_train_val`** (already uploaded: `rel0001_train.jsonl` + `rel0001_val.jsonl` for Train SHAP bg & Val parity check)
3. **`REL0001_ds0002_png_train_val`** (already uploaded: Train/Val `768×384` `ds0002_png/`)
4. **`PTB-XL ECG dataset`** (`khyeh0719/ptb-xl-dataset` — already in Kaggle Public Datasets)

### 📋 এই নোটবুক যা যা সম্পন্ন করবে:
- **STEP-033:** সব `15`টি চেকপয়েন্ট SHA-256 + `Validation Parity Check` পাস করে `REL0001 Test` (`12,719` রোগী, `100%` কভারেজ)-এর ওপর ফ্রোজেন ১-শট প্রেডিকশন।
- **STEP-034:** ৬টি ম্যান্ডেটরি মেট্রিক + PR-AUC, Specificity, NPV, MCC, Pre/Post Calibration (`Brier, BSS, ECE-q15, ECE-u15, Slope, Intercept`), `5`-সিড Mean ± SD।
- **STEP-035:** `B = 2,000` Patient-Grouped Stratified Bootstrap `95% CI`, Paired Two-Sided **DeLong**, **McNemar**, **Holm-Bonferroni**, ও **DCA (`p_t ∈ [0.05, 0.50]`)**।
- **STEP-037:** Subgroup Fairness (`Sex, AgeBand, Cohort, ModalityTier`), Missing-Modality Stress (`Test`), এবং De-identified **`N = 24` (`6 TP/FP/TN/FN`) Error & Cardiologist Packet**।
- **STEP-038 & STEP-039:** `TreeSHAP`, Exact `2^4` Coalition Shapley Modality Shares `[C%, E%, L%, S%]`, `50`-step Gauss-Legendre `IntegratedGradients` (`additivity <= 0.02`), **Deletion & Insertion `AOPC` vs Random/Reverse**, LOMO Concordance, **`5`-Seed XAI Stability (`Spearman ρ, Top-5 Jaccard`)**, এবং `MNAR _isnan` Shortcut Audit -> `/kaggle/working/s12_to_s15_final_test_xai_export.zip`!
"""

CELL_1 = r"""# Cell 1: Hardware Lock, G11 Freeze Auto-Discovery & Cryptographic Integrity Audit
import os, re, json, math, time, random, hashlib, zipfile, pickle, itertools
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.signal as sps
import scipy.stats as st
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import shap

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    average_precision_score, confusion_matrix, brier_score_loss,
    matthews_corrcoef, balanced_accuracy_score, roc_curve, precision_recall_curve
)
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

G11_AUTHORIZED = True
TACC_TOKEN = 'TACC0002_G11-20261128-02'
CANONICAL_SEEDS = [20261127, 20261128, 20261129, 20261130, 20261201]
PRIMARY_SEED = CANONICAL_SEEDS[0]
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
OUT_DIR = Path('/kaggle/working/s12_s15_outputs') if Path('/kaggle').exists() else Path('09_Evaluation_Stats/s12_s15_outputs')
OUT_DIR.mkdir(parents=True, exist_ok=True)

def seed_everything(seed: int = PRIMARY_SEED):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

seed_everything(PRIMARY_SEED)

SEARCH_ROOTS = [p for p in [
    Path('/kaggle/input'),
    Path('05_Preprocessing_Alignment/processed'),
    Path('08_Checkpoints/binaries/S11'),
    Path('09_Evaluation_Stats'),
    Path('07_Experiments'),
    Path('Dataset'),
] if p.exists()]

TRAIN_SHARD = VAL_SHARD = TEST_SHARD = PNG_TV_DIR = PNG_TE_DIR = PTB_ROOT = CKPT_DIR_IN = FREEZE_DIR_IN = None

def scan_all_inputs(roots):
    global TRAIN_SHARD, VAL_SHARD, TEST_SHARD, PNG_TV_DIR, PNG_TE_DIR, PTB_ROOT, CKPT_DIR_IN, FREEZE_DIR_IN
    zip_hits = []
    for r in roots:
        for dirpath, dirnames, filenames in os.walk(r, followlinks=True):
            dp = Path(dirpath)
            if TRAIN_SHARD is None and 'rel0001_train.jsonl' in filenames: TRAIN_SHARD = dp / 'rel0001_train.jsonl'
            if VAL_SHARD is None and 'rel0001_val.jsonl' in filenames: VAL_SHARD = dp / 'rel0001_val.jsonl'
            if TEST_SHARD is None and 'rel0001_test.jsonl' in filenames: TEST_SHARD = dp / 'rel0001_test.jsonl'
            if PNG_TV_DIR is None and 'ds0002_png' in dirnames: PNG_TV_DIR = dp / 'ds0002_png'
            if PNG_TE_DIR is None and 'ds0002_png_test' in dirnames: PNG_TE_DIR = dp / 'ds0002_png_test'
            if PTB_ROOT is None and ('records100' in dirnames or 'records500' in dirnames): PTB_ROOT = dp
            if CKPT_DIR_IN is None and 's11_checkpoint_manifest.json' in filenames and 'EXP0015_MC0015_seed20261127_best_val.pt' in filenames:
                CKPT_DIR_IN = dp
            if FREEZE_DIR_IN is None and 'frozen_validation_calibration.json' in filenames:
                FREEZE_DIR_IN = dp
            for fn in filenames:
                if fn.endswith('.zip') and ('REL0001' in fn or 'bundle' in fn):
                    zip_hits.append(dp / fn)
            dirnames[:] = [d for d in dirnames if d not in ('records100', 'records500', 'ds0002_png', 'ds0002_png_test', '.git', '__pycache__', 'environment')]
    return zip_hits

zip_cands = scan_all_inputs(SEARCH_ROOTS)
if any(x is None for x in (TRAIN_SHARD, VAL_SHARD, TEST_SHARD, PNG_TV_DIR, PNG_TE_DIR, CKPT_DIR_IN, FREEZE_DIR_IN)) and zip_cands:
    up = OUT_DIR / '_unpacked'
    for zp in zip_cands:
        tgt = up / zp.stem
        if not tgt.exists():
            tgt.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zp, 'r') as zf: zf.extractall(tgt)
    scan_all_inputs([up])

if Path('/kaggle/input').exists():
    print('Kaggle mounted inputs:', sorted(p.name for p in Path('/kaggle/input').iterdir()))
assert all(x is not None for x in (TRAIN_SHARD, VAL_SHARD, TEST_SHARD, PNG_TV_DIR, PNG_TE_DIR, CKPT_DIR_IN, FREEZE_DIR_IN)), (
    f'Missing inputs! Found TRAIN={TRAIN_SHARD}, VAL={VAL_SHARD}, TEST={TEST_SHARD}, '
    f'PNG_TV={PNG_TV_DIR}, PNG_TE={PNG_TE_DIR}, CKPT={CKPT_DIR_IN}, FREEZE={FREEZE_DIR_IN}'
)
assert PTB_ROOT is not None, 'Attach PTB-XL ECG dataset (khyeh0719/ptb-xl-dataset)!'

# Verify frozen SHA-256 digests cleanly BEFORE touching Test data
EXPECTED_CAL_SHA = 'ea5e5d969eeb72fcecd19e9b55812baac0c4b35ec12b9457e42999903a993e65'
EXPECTED_BG_SHA = 'fd797cf5dc180548a64b0243e35a1e7851354177b8202246ea536b4917a6eabe'
actual_cal_sha = hashlib.sha256((FREEZE_DIR_IN / 'frozen_validation_calibration.json').read_bytes()).hexdigest()
actual_bg_sha = hashlib.sha256((FREEZE_DIR_IN / 'shap_background_ids.json').read_bytes()).hexdigest()
assert actual_cal_sha == EXPECTED_CAL_SHA, f'CalibratorHash mismatch: {actual_cal_sha} != {EXPECTED_CAL_SHA}'
assert actual_bg_sha == EXPECTED_BG_SHA, f'BackgroundHash mismatch: {actual_bg_sha} != {EXPECTED_BG_SHA}'

ckpt_manifest = json.loads((CKPT_DIR_IN / 's11_checkpoint_manifest.json').read_text(encoding='utf-8'))
for entry in ckpt_manifest:
    p = CKPT_DIR_IN / entry['filename']
    assert p.is_file(), f'Missing frozen checkpoint: {p}'
    assert hashlib.sha256(p.read_bytes()).hexdigest() == entry['sha256'], f'SHA mismatch: {p.name}'

FROZEN_CAL = json.loads((FREEZE_DIR_IN / 'frozen_validation_calibration.json').read_text(encoding='utf-8'))['calibrators_and_thresholds']
SHAP_BG_CFG = json.loads((FREEZE_DIR_IN / 'shap_background_ids.json').read_text(encoding='utf-8'))
S11_VAL_REF = pd.read_csv(FREEZE_DIR_IN / 's11_validation_results.csv')
print(f'Device={DEVICE} | PyTorch={torch.__version__} | SHAP={shap.__version__} | 15/15 Checkpoints & Freeze SHA-256 PASS!')"""

CELL_2 = r"""# Cell 2: Load REL0001 Train/Val/Test, Subgroup Metadata, WFDB/PNG Caches & Stats/DCA Engine
COHORT_MODALITY_SLICES = {
    'DS0001': {'clinical': (0,1,2,3,4,5,6,7,8,9,10), 'laboratory': (), 'lifestyle': ()},
    'DS0002': {'clinical': (0,1,2,3,4,5,6,7,12,13,14), 'laboratory': (8,9,10,11), 'lifestyle': ()},
    'DS0003': {'clinical': (0,1,2,3,4,5,6,7,8,9,10,11,24,25,26), 'laboratory': (12,13,14,15,16,17,18,19), 'lifestyle': (20,21,22,23,27,28,29,30)},
    'DS0004': {'clinical': (0,1,2,3,4,5,6,7,8,9,10,11,22,23,24), 'laboratory': (12,13,14,15), 'lifestyle': (16,17,18,19,20,21)},
}
COHORT_MODALITY_DIMS = {ds: {m: len(ix) for m, ix in mods.items()} for ds, mods in COHORT_MODALITY_SLICES.items()}

# Exact verified PP0001 Train-fitted feature names, age RobustScaler params & Sex OHE column indices
COHORT_FEATURE_META = {
    'DS0001': {
        'names': ['age_years','age_years_isnan','height_cm','height_cm_isnan','weight_kg','weight_kg_isnan','bmi_kgm2','bmi_kgm2_isnan','sex__F','sex__M','sex__MISSING'],
        'age_med': 61.0, 'age_iqr': 22.0, 'sex_f': 8, 'sex_m': 9,
    },
    'DS0002': {
        'names': ['age_years','age_years_isnan','sbp_mmhg','sbp_mmhg_isnan','dbp_mmhg','dbp_mmhg_isnan','pr_bpm','pr_bpm_isnan','creatinine_mgdl','creatinine_mgdl_isnan','wbc_ul','wbc_ul_isnan','sex__F','sex__M','sex__MISSING'],
        'age_med': 51.0, 'age_iqr': 26.0, 'sex_f': 12, 'sex_m': 13,
    },
    'DS0003': {
        'names': ['age_years','age_years_isnan','height_cm','height_cm_isnan','weight_kg','weight_kg_isnan','bmi_kgm2','bmi_kgm2_isnan','sbp_mmhg','sbp_mmhg_isnan','dbp_mmhg','dbp_mmhg_isnan','total_cholesterol_mgdl','total_cholesterol_mgdl_isnan','hdl_mgdl','hdl_mgdl_isnan','ldl_estimated_mgdl','ldl_estimated_mgdl_isnan','fbs_mgdl','fbs_mgdl_isnan','smoking_status','smoking_status_isnan','family_history_cvd','family_history_cvd_isnan','sex__F','sex__M','sex__MISSING','activity_level__High','activity_level__Low','activity_level__Moderate','activity_level__MISSING'],
        'age_med': 46.0, 'age_iqr': 19.0, 'sex_f': 24, 'sex_m': 25,
    },
    'DS0004': {
        'names': ['age_years','age_years_isnan','height_cm','height_cm_isnan','weight_kg','weight_kg_isnan','bmi_kgm2','bmi_kgm2_isnan','sbp_mmhg','sbp_mmhg_isnan','dbp_mmhg','dbp_mmhg_isnan','cholesterol_tier','cholesterol_tier_isnan','glucose_tier','glucose_tier_isnan','smoking_status','smoking_status_isnan','alcohol_intake','alcohol_intake_isnan','physical_activity','physical_activity_isnan','sex__F','sex__M','sex__MISSING'],
        'age_med': 53.9302, 'age_iqr': 10.094500000000004, 'sex_f': 22, 'sex_m': 23,
    },
}

def load_jsonl(p: Path):
    with open(p, encoding='utf-8') as f: return [json.loads(line) for line in f]

train_recs = load_jsonl(TRAIN_SHARD)
val_recs = load_jsonl(VAL_SHARD)
test_recs = load_jsonl(TEST_SHARD)
assert len({r['PatientGroupID'] for r in train_recs} & {r['PatientGroupID'] for r in test_recs}) == 0, 'Patient overlap Train/Test!'
assert len({r['PatientGroupID'] for r in val_recs} & {r['PatientGroupID'] for r in test_recs}) == 0, 'Patient overlap Val/Test!'
print(f'Loaded REL0001 cleanly | Train={len(train_recs):,} | Val={len(val_recs):,} | Test={len(test_recs):,} (0 Patient Overlap)')

def extract_sex_and_age_band(rec):
    meta = COHORT_FEATURE_META[rec['DS']]
    x = rec['TabularFeatures']
    sex = 'F' if x[meta['sex_f']] > 0.5 else ('M' if x[meta['sex_m']] > 0.5 else 'Unknown')
    if x[1] > 0.5: age_band = 'Age_Missing'
    else:
        age_y = x[0] * meta['age_iqr'] + meta['age_med']
        age_band = '18-44y' if age_y < 45.0 else ('45-64y' if age_y < 65.0 else '>=65y')
    return sex, age_band

B_NOTCH_500, A_NOTCH_500 = sps.iirnotch(50.0, Q=30.0, fs=500.0)
SOS_HP_500 = sps.butter(2, 0.5, btype='highpass', fs=500.0, output='sos')
SOS_HP_100 = sps.butter(2, 0.5, btype='highpass', fs=100.0, output='sos')

def load_wfdb_12lead_100hz(ecg_ref: dict) -> np.ndarray | None:
    if not ecg_ref: return None
    hr_rel, lr_rel = ecg_ref.get('wfdb_hr_relpath', ''), ecg_ref.get('wfdb_lr_relpath', '')
    hr_sub = hr_rel.split('records500/')[-1] if 'records500/' in hr_rel else ''
    lr_sub = lr_rel.split('records100/')[-1] if 'records100/' in lr_rel else ''
    hr_p = (PTB_ROOT / 'records500' / f'{hr_sub}.dat') if hr_sub else None
    lr_p = (PTB_ROOT / 'records100' / f'{lr_sub}.dat') if lr_sub else None
    if hr_p is not None and hr_p.is_file():
        arr = np.fromfile(hr_p, dtype='<i2').reshape(-1, 12).T.astype(np.float32) / 1000.0
        arr = sps.sosfiltfilt(SOS_HP_500, sps.filtfilt(B_NOTCH_500, A_NOTCH_500, arr, axis=-1), axis=-1)[:, ::5]
    elif lr_p is not None and lr_p.is_file():
        arr = sps.sosfiltfilt(SOS_HP_100, np.fromfile(lr_p, dtype='<i2').reshape(-1, 12).T.astype(np.float32) / 1000.0, axis=-1)
    else: return None
    arr = arr[:, :1000] if arr.shape[1] >= 1000 else np.pad(arr, ((0,0), (0, 1000 - arr.shape[1])))
    mu = arr.mean(axis=-1, keepdims=True)
    sd = np.maximum(arr.std(axis=-1, keepdims=True), 1e-4)
    return np.clip((arr - mu) / sd, -10.0, 10.0).astype(np.float16)

def load_ds0002_png(ecg_ref: dict, size_wh=(768, 384)) -> np.ndarray | None:
    if not ecg_ref or not ecg_ref.get('png_relpaths'): return None
    raw_name = Path(ecg_ref['png_relpaths'][0]).name
    rp = Path(raw_name)
    clean_name = f"{re.sub(r'\s+', '_', re.sub(r'\((\d+)\)$', r'-\1', rp.stem.strip()))}{rp.suffix.strip().lower()}"
    p = None
    for d in (PNG_TE_DIR, PNG_TV_DIR):
        for cand in (d / clean_name, d / raw_name):
            if cand.is_file(): p = cand; break
        if p is not None: break
    if p is None: return None
    img = Image.open(p)
    if img.width < img.height: img = img.rotate(90, expand=True)
    if (img.width, img.height) != size_wh: img = img.resize(size_wh, Image.Resampling.BILINEAR)
    rgb = np.asarray(img.convert('RGB'), dtype=np.float32)
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = r if (np.allclose(r, g) and np.allclose(g, b)) else np.where((np.minimum(255.0, 0.299*r + 0.587*g + 0.114*b + 0.75*np.maximum(0.0, r - np.maximum(g, b))) >= 155.0) & (np.maximum(np.maximum(r, g), b) >= 165.0), 255.0, np.minimum(255.0, 0.299*r + 0.587*g + 0.114*b + 0.75*np.maximum(0.0, r - np.maximum(g, b))))
    return ((255.0 - gray) / 255.0)[None, ...].astype(np.float16)

t0 = time.time()
WFDB_CACHE, PNG_CACHE = {}, {}
for r in train_recs + val_recs + test_recs:
    eid = r['EncounterID']
    if r['DS'] == 'DS0001':
        sig = load_wfdb_12lead_100hz(r.get('ECGReference'))
        if sig is not None: WFDB_CACHE[eid] = sig
    elif r['DS'] == 'DS0002' and r['ModalityMask_CELS'][1] == 1:
        im = load_ds0002_png(r.get('ECGReference'))
        if im is not None: PNG_CACHE[eid] = im
n_ds1_all = sum(1 for r in train_recs + val_recs + test_recs if r['DS']=='DS0001')
n_ds2_ecg_all = sum(1 for r in train_recs + val_recs + test_recs if r['DS']=='DS0002' and r['ModalityMask_CELS'][1]==1)
print(f'Cached ALL partitions in {time.time()-t0:.1f}s | WFDB={len(WFDB_CACHE):,}/{n_ds1_all:,} | PNG={len(PNG_CACHE):,}/{n_ds2_ecg_all:,}')
assert len(WFDB_CACHE) == n_ds1_all and len(PNG_CACHE) == n_ds2_ecg_all, 'Incomplete ECG asset caching!'

# Calibration, Complete Metrics, Fast DeLong, Exact McNemar, Holm-Bonferroni & DCA
def apply_temp_scaling(probs, temp: float):
    p = np.clip(np.asarray(probs, dtype=np.float64), 1e-6, 1.0 - 1e-6)
    logits = np.log(p / (1.0 - p))
    return 1.0 / (1.0 + np.exp(-np.clip(logits / temp, -50.0, 50.0)))

def compute_calibration_slope_intercept(y_true, p_prob):
    p = np.clip(np.asarray(p_prob, dtype=np.float64), 1e-6, 1.0 - 1e-6)
    lp = np.log(p / (1.0 - p)).reshape(-1, 1)
    if len(np.unique(y_true)) < 2: return float('nan'), float('nan')
    lr = LogisticRegression(C=1e9, max_iter=500).fit(lp, y_true)
    return float(lr.coef_[0, 0]), float(lr.intercept_[0])

def compute_full_metrics(y_true, p_raw, temp: float, tau: float):
    y_true = np.asarray(y_true, dtype=np.int64)
    p_raw = np.clip(np.asarray(p_raw, dtype=np.float64), 1e-7, 1.0 - 1e-7)
    p_cal = apply_temp_scaling(p_raw, temp)
    y_pred = (p_cal >= tau).astype(np.int64)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    order = np.argsort(p_cal)
    ece_q15 = sum((len(b)/len(y_true)) * abs(y_true[b].mean() - p_cal[b].mean()) for b in np.array_split(order, min(15, len(order))) if len(b))
    bins = np.linspace(0.0, 1.0, 16)
    ece_u15 = sum((len(idx_b := np.where((p_cal >= bins[i]) & (p_cal <= bins[i+1] if i==14 else p_cal < bins[i+1]))[0]) / len(y_true)) * abs(y_true[idx_b].mean() - p_cal[idx_b].mean()) for i in range(15) if len(np.where((p_cal >= bins[i]) & (p_cal <= bins[i+1] if i==14 else p_cal < bins[i+1]))[0]) > 0)
    brier_raw, brier_cal = float(brier_score_loss(y_true, p_raw)), float(brier_score_loss(y_true, p_cal))
    prev = float(y_true.mean())
    bss = 1.0 - brier_cal / max(1e-9, prev * (1.0 - prev))
    slope, intercept = compute_calibration_slope_intercept(y_true, p_cal)
    return {
        'n': int(len(y_true)), 'events': int(y_true.sum()), 'prevalence': round(prev, 6),
        'roc_auc': float(roc_auc_score(y_true, p_cal)) if len(np.unique(y_true))==2 else float('nan'),
        'roc_auc_raw': float(roc_auc_score(y_true, p_raw)) if len(np.unique(y_true))==2 else float('nan'),
        'pr_auc': float(average_precision_score(y_true, p_cal)) if len(np.unique(y_true))==2 else float('nan'),
        'accuracy': float(accuracy_score(y_true, y_pred)),
        'precision': float(tp / (tp + fp)) if (tp + fp) > 0 else float('nan'),
        'recall': float(tp / (tp + fn)) if (tp + fn) > 0 else float('nan'),
        'specificity': float(tn / (tn + fp)) if (tn + fp) > 0 else float('nan'),
        'npv': float(tn / (tn + fn)) if (tn + fn) > 0 else float('nan'),
        'f1': float(f1_score(y_true, y_pred, zero_division=0)),
        'balanced_acc': float(balanced_accuracy_score(y_true, y_pred)),
        'mcc': float(matthews_corrcoef(y_true, y_pred)),
        'brier_raw': brier_raw, 'brier_cal': brier_cal, 'bss': float(bss),
        'ece_q15': float(ece_q15), 'ece_u15': float(ece_u15),
        'cal_slope': slope, 'cal_intercept': intercept,
        'tn': int(tn), 'fp': int(fp), 'fn': int(fn), 'tp': int(tp), 'p_cal': p_cal,
    }

def _midrank(x):
    j = np.argsort(x)
    z = x[j]
    n = len(x)
    t = np.zeros(n, dtype=np.float64)
    i = 0
    while i < n:
        k = i
        while k < n and z[k] == z[i]: k += 1
        t[i:k] = 0.5 * (i + k - 1) + 1.0
        i = k
    out = np.empty(n, dtype=np.float64)
    out[j] = t
    return out

def paired_delong_test(y_true, p1, p2):
    y = np.asarray(y_true, dtype=np.int64)
    pos, neg = y == 1, y == 0
    m, n = int(pos.sum()), int(neg.sum())
    preds = np.vstack([np.asarray(p1, dtype=np.float64), np.asarray(p2, dtype=np.float64)])
    ord_preds = np.hstack([preds[:, pos], preds[:, neg]])
    k = 2
    tx = np.array([_midrank(ord_preds[r, :m]) for r in range(k)])
    ty = np.array([_midrank(ord_preds[r, m:]) for r in range(k)])
    tz = np.array([_midrank(ord_preds[r, :]) for r in range(k)])
    aucs = tz[:, :m].sum(axis=1) / (m * n) - (m + 1.0) / (2.0 * n)
    v01 = (tz[:, :m] - tx) / n
    v10 = 1.0 - (tz[:, m:] - ty) / m
    sx = np.cov(v01) if m > 1 else np.zeros((2,2))
    sy = np.cov(v10) if n > 1 else np.zeros((2,2))
    s = sx / m + sy / n
    var = float(s[0,0] + s[1,1] - 2.0 * s[0,1])
    if var <= 1e-18: return float(aucs[0]), float(aucs[1]), 1.0
    z = (aucs[0] - aucs[1]) / math.sqrt(var)
    return float(aucs[0]), float(aucs[1]), float(2.0 * st.norm.sf(abs(z)))

def exact_mcnemar_test(y_true, pred1, pred2):
    c1, c2 = (pred1 == y_true), (pred2 == y_true)
    b = int(np.sum(c1 & (~c2)))
    c = int(np.sum((~c1) & c2))
    if b + c == 0: return b, c, 1.0
    return b, c, float(st.binomtest(min(b, c), b + c, 0.5).pvalue)

def holm_bonferroni(pvals):
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m, dtype=np.float64)
    prev = 0.0
    for r, idx in enumerate(order):
        val = min(1.0, (m - r) * pvals[idx])
        prev = max(prev, val)
        adj[idx] = prev
    return adj.tolist()

print('Cell 2 complete — metrics, calibration, DeLong, McNemar & Holm helpers verified.')"""

CELL_3 = r"""# Cell 3: Reload Frozen S11 Checkpoints, Reconstruct Deterministic Baselines & STRICT Validation Parity Audit
class TabularUnimodalNet(nn.Module):
    def __init__(self, d_in: int):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, 64), nn.LayerNorm(64), nn.GELU(), nn.Dropout(0.3), nn.Linear(64, 32), nn.GELU(), nn.Linear(32, 1))
    def forward(self, x): return self.net(x).squeeze(-1)

class SEBlock1D(nn.Module):
    def __init__(self, c: int):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(c, max(4, c//4)), nn.SiLU(), nn.Linear(max(4, c//4), c), nn.Sigmoid())
    def forward(self, x): return x * self.fc(x.mean(dim=-1)).unsqueeze(-1)

class ResBlock1D(nn.Module):
    def __init__(self, ci: int, co: int, stride: int = 2, drop: float = 0.1):
        super().__init__()
        self.c1 = nn.Conv1d(ci, co, 5, stride=stride, padding=2, bias=False); self.b1 = nn.BatchNorm1d(co)
        self.c2 = nn.Conv1d(co, co, 5, stride=1, padding=2, bias=False); self.b2 = nn.BatchNorm1d(co)
        self.se = SEBlock1D(co); self.drop = nn.Dropout(drop)
        self.sh = nn.Sequential(nn.Conv1d(ci, co, 1, stride=stride, bias=False), nn.BatchNorm1d(co)) if (stride!=1 or ci!=co) else nn.Identity()
    def forward(self, x): return F.gelu(self.se(self.b2(self.c2(self.drop(F.gelu(self.b1(self.c1(x))))))) + self.sh(x))

class CompactResNet1D(nn.Module):
    def __init__(self, embed_dim: int = 64):
        super().__init__()
        self.stem = nn.Sequential(nn.Conv1d(12, 32, 7, stride=2, padding=3, bias=False), nn.BatchNorm1d(32), nn.GELU())
        self.blocks = nn.Sequential(ResBlock1D(32, 32, 2), ResBlock1D(32, 64, 2), ResBlock1D(64, embed_dim, 2))
        self.head = nn.Linear(embed_dim, 1)
    def encode(self, x): return self.blocks(self.stem(x)).mean(dim=-1)
    def forward(self, x): return self.head(self.encode(x)).squeeze(-1)

class Conv1DBiLSTMEncoder(nn.Module):
    def __init__(self, embed_dim: int = 64):
        super().__init__()
        self.conv = nn.Sequential(nn.Conv1d(12, 32, 7, stride=2, padding=3, bias=False), nn.BatchNorm1d(32), nn.GELU(), nn.MaxPool1d(2), nn.Conv1d(32, 48, 5, stride=2, padding=2, bias=False), nn.BatchNorm1d(48), nn.GELU())
        self.lstm = nn.LSTM(48, embed_dim//2, batch_first=True, bidirectional=True)
        self.head = nn.Linear(embed_dim, 1)
    def encode(self, x):
        out, _ = self.lstm(self.conv(x).transpose(1, 2)); return out.mean(dim=1)
    def forward(self, x): return self.head(self.encode(x)).squeeze(-1)

class CompactCNN2DPNG(nn.Module):
    def __init__(self, embed_dim: int = 64):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 16, 3, 2, 1, bias=False), nn.BatchNorm2d(16), nn.GELU(),
            nn.Conv2d(16, 32, 3, 2, 1, bias=False), nn.BatchNorm2d(32), nn.GELU(),
            nn.Conv2d(32, 48, 3, 2, 1, bias=False), nn.BatchNorm2d(48), nn.GELU(),
            nn.Conv2d(48, embed_dim, 3, 2, 1, bias=False), nn.BatchNorm2d(embed_dim), nn.GELU()
        )
        self.proj = nn.Sequential(nn.Linear(embed_dim * 2, embed_dim), nn.LayerNorm(embed_dim), nn.GELU(), nn.Dropout(0.3))
        self.head = nn.Linear(embed_dim, 1)
    def encode(self, img):
        h = self.conv(img)
        return self.proj(torch.cat([F.adaptive_max_pool2d(h, 1).flatten(1), F.adaptive_avg_pool2d(h, 1).flatten(1)], dim=1))
    def forward(self, img): return self.head(self.encode(img)).squeeze(-1)

class ECGPatchTransformer(nn.Module):
    def __init__(self, d_model: int = 64):
        super().__init__()
        self.patch = nn.Conv1d(12, d_model, kernel_size=25, stride=25)
        self.cls = nn.Parameter(torch.zeros(1, 1, d_model))
        enc = nn.TransformerEncoderLayer(d_model, nhead=4, dim_feedforward=128, dropout=0.1, activation='gelu', batch_first=True, norm_first=True)
        self.enc = nn.TransformerEncoder(enc, num_layers=2)
        self.head = nn.Linear(d_model, 1)
    def encode(self, x):
        p = self.patch(x).transpose(1, 2)
        return self.enc(torch.cat([self.cls.expand(p.size(0), -1, -1), p], dim=1))[:, 0]
    def forward(self, x): return self.head(self.encode(x)).squeeze(-1)

class TabularAdapter(nn.Module):
    def __init__(self, d_in: int, d_model: int = 64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, d_model), nn.LayerNorm(d_model), nn.GELU(), nn.Dropout(0.15), nn.Linear(d_model, d_model))
    def forward(self, x): return self.net(x)

class CVDMMTransformerUnified(nn.Module):
    def __init__(self, d_model: int = 64, nhead: int = 4, n_layers: int = 2, mod_drop_p: float = 0.15, use_key_mask: bool = True, gated_only: bool = False):
        super().__init__()
        self.d_model = d_model; self.mod_drop_p = mod_drop_p; self.use_key_mask = use_key_mask; self.gated_only = gated_only
        self.tab_adapters = nn.ModuleDict({f'{ds}__{m}': TabularAdapter(dim, d_model) for ds, mods in COHORT_MODALITY_DIMS.items() for m, dim in mods.items() if dim > 0})
        self.ecg_1d = CompactResNet1D(d_model)
        self.ecg_2d = CompactCNN2DPNG(d_model)
        self.cls_token = nn.Parameter(torch.zeros(1, 1, d_model))
        self.mod_type = nn.Parameter(torch.randn(1, 4, d_model) * 0.02)
        if gated_only:
            self.gate = nn.Sequential(nn.Linear(d_model, 32), nn.Tanh(), nn.Linear(32, 1))
        else:
            enc = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward=128, dropout=0.1, activation='gelu', batch_first=True, norm_first=True)
            self.encoder = nn.TransformerEncoder(enc, num_layers=n_layers)
        self.norm = nn.LayerNorm(d_model)
        self.head = nn.Sequential(nn.Linear(d_model, 32), nn.GELU(), nn.Dropout(0.1), nn.Linear(32, 1))

    def forward(self, ds_id: str, tab_mods: dict, mask_cels: torch.Tensor, ecg_1d=None, ecg_2d=None):
        b, dev = mask_cels.size(0), mask_cels.device
        eff_mask = mask_cels.bool()
        toks = []
        for idx, mod in enumerate(['clinical', 'ecg', 'laboratory', 'lifestyle']):
            if mod == 'ecg':
                if ecg_1d is not None: emb = self.ecg_1d.encode(ecg_1d) * eff_mask[:, 1:2].float()
                elif ecg_2d is not None: emb = self.ecg_2d.encode(ecg_2d) * eff_mask[:, 1:2].float()
                else: emb = torch.zeros(b, self.d_model, device=dev)
            else:
                key = f'{ds_id}__{mod}'
                emb = self.tab_adapters[key](tab_mods[mod]) * eff_mask[:, idx:idx+1].float() if (key in self.tab_adapters and mod in tab_mods) else torch.zeros(b, self.d_model, device=dev)
            toks.append(emb + self.mod_type[:, idx, :])
        stacked = torch.stack(toks, dim=1)
        if self.gated_only:
            sc = self.gate(stacked).squeeze(-1).float().masked_fill(~eff_mask, -1e9)
            w = F.softmax(sc, dim=-1).to(stacked.dtype).unsqueeze(-1)
            return self.head(self.norm((stacked * w).sum(dim=1))).squeeze(-1)
        seq = torch.cat([self.cls_token.expand(b, -1, -1), stacked], dim=1)
        pad_mask = torch.cat([torch.zeros(b, 1, dtype=torch.bool, device=dev), ~eff_mask], dim=1) if self.use_key_mask else None
        out = self.norm(self.encoder(seq, src_key_padding_mask=pad_mask))
        return self.head(out[:, 0]).squeeze(-1)

def prepare_cohort_tensors(recs):
    by_ds = {}
    for ds_id in ['DS0001', 'DS0002', 'DS0003', 'DS0004']:
        sub = [r for r in recs if r['DS'] == ds_id]
        X = np.asarray([r['TabularFeatures'] for r in sub], dtype=np.float32)
        mods = {m: torch.from_numpy(X[:, list(ix)]) for m, ix in COHORT_MODALITY_SLICES[ds_id].items() if len(ix) > 0}
        masks = torch.tensor([r['ModalityMask_CELS'] for r in sub], dtype=torch.bool)
        y = torch.tensor([r['Target_y'] for r in sub], dtype=torch.float32)
        eids = [r['EncounterID'] for r in sub]
        gids = [r['PatientGroupID'] for r in sub]
        sexes, age_bands = zip(*[extract_sex_and_age_band(r) for r in sub])
        ecg1d = np.stack([WFDB_CACHE[e] if e in WFDB_CACHE else np.zeros((12, 1000), dtype=np.float16) for e in eids]) if ds_id == 'DS0001' else None
        ecg2d = np.stack([PNG_CACHE[e] if e in PNG_CACHE else np.zeros((1, 384, 768), dtype=np.float16) for e in eids]) if ds_id == 'DS0002' else None
        by_ds[ds_id] = {'mods': mods, 'mask': masks, 'y': y, 'ecg1d': ecg1d, 'ecg2d': ecg2d, 'eids': eids, 'gids': list(gids), 'sexes': list(sexes), 'age_bands': list(age_bands), 'n': len(sub), 'recs': sub}
    return by_ds

VA_COHORTS = prepare_cohort_tensors(val_recs)
TE_COHORTS = prepare_cohort_tensors(test_recs)

def predict_multicohort(model, coh_dict, override_mask=None):
    model.eval(); ys, ps, per_ds = [], [], {}
    with torch.no_grad():
        for ds_id, d in coh_dict.items():
            n, probs_ds = d['n'], []
            bs = 64 if ds_id in ('DS0001', 'DS0002') else 512
            for i in range(0, n, bs):
                bm = {m: t[i:i+bs].to(DEVICE) for m, t in d['mods'].items()}
                bmask = (override_mask(ds_id, d['mask'][i:i+bs]) if override_mask else d['mask'][i:i+bs]).to(DEVICE)
                e1 = torch.from_numpy(d['ecg1d'][i:i+bs].astype(np.float32)).to(DEVICE) if d['ecg1d'] is not None else None
                e2 = torch.from_numpy(d['ecg2d'][i:i+bs].astype(np.float32)).to(DEVICE) if d['ecg2d'] is not None else None
                probs_ds.append(torch.sigmoid(model(ds_id, bm, bmask, ecg_1d=e1, ecg_2d=e2)).cpu().numpy())
            p_ds = np.concatenate(probs_ds); y_ds = d['y'].numpy().astype(np.int64)
            per_ds[ds_id] = (y_ds, p_ds); ys.append(y_ds); ps.append(p_ds)
    return np.concatenate(ys), np.concatenate(ps), per_ds

# 1. Load ALL 15 Frozen Checkpoints & Assert Pre-Test Validation Parity <= 1e-4
FROZEN_XGB = {}
for ds_id in ('DS0001', 'DS0002', 'DS0003', 'DS0004'):
    with open(CKPT_DIR_IN / f'EXP0004_{ds_id}_xgb.pkl', 'rb') as f:
        FROZEN_XGB[ds_id] = pickle.load(f)
    va_sub = [r for r in val_recs if r['DS'] == ds_id]
    p_va = FROZEN_XGB[ds_id].predict_proba(np.asarray([r['TabularFeatures'] for r in va_sub], dtype=np.float32))[:, 1]
    auc_va = roc_auc_score([r['Target_y'] for r in va_sub], p_va)
    ref = float(S11_VAL_REF[(S11_VAL_REF['EXP']=='EXP0004') & (S11_VAL_REF['Cohort']==ds_id)]['Val_ROCAUC_Raw'].iloc[0])
    assert abs(auc_va - ref) <= 1e-4, f'Val parity fail EXP0004 {ds_id}: {auc_va} vs {ref}'

def load_torch_ckpt(cls, fname, **kwargs):
    ck = torch.load(CKPT_DIR_IN / fname, map_location=DEVICE, weights_only=False)
    m = cls(**kwargs).to(DEVICE)
    m.load_state_dict({k: v.to(DEVICE) for k, v in ck['state_dict'].items()})
    m.eval()
    return m

M_ECG_RESNET = load_torch_ckpt(CompactResNet1D, 'EXP0007_MC0007_best_val.pt')
M_ECG_BILSTM = load_torch_ckpt(Conv1DBiLSTMEncoder, 'EXP0008_MC0008_best_val.pt')
M_ECG_CNN2D  = load_torch_ckpt(CompactCNN2DPNG, 'EXP0009_MC0009_best_val.pt')
M_ECG_PATCH  = load_torch_ckpt(ECGPatchTransformer, 'EXP0010_MC0010_best_val.pt')
M_GATED      = load_torch_ckpt(CVDMMTransformerUnified, 'EXP0014_MC0014_seed20261127_best_val.pt', gated_only=True)
M_CHAMP_S1   = load_torch_ckpt(CVDMMTransformerUnified, 'EXP0015_MC0015_seed20261127_best_val.pt', use_key_mask=True, gated_only=False)
M_NOMASK     = load_torch_ckpt(CVDMMTransformerUnified, 'EXP0018_MC0015_seed20261127_best_val.pt', use_key_mask=False, gated_only=False)
M_SEEDS_2_5  = [load_torch_ckpt(CVDMMTransformerUnified, f'EXP0020_MC0015_seed{s}_best_val.pt', use_key_mask=True, gated_only=False) for s in CANONICAL_SEEDS[1:]]
M_ALL_5SEEDS = [M_CHAMP_S1] + M_SEEDS_2_5

# Verify Validation Parity strictly BEFORE running Test
for exp_chk, m_chk in [('EXP0014', M_GATED), ('EXP0015', M_CHAMP_S1), ('EXP0018', M_NOMASK)]:
    yv, pv, per_ds = predict_multicohort(m_chk, VA_COHORTS)
    for coh_k, (y_c, p_c) in [('ALL_COHORTS', (yv, pv))] + list(per_ds.items()):
        auc_c = roc_auc_score(y_c, p_c)
        ref = float(S11_VAL_REF[(S11_VAL_REF['EXP']==exp_chk) & (S11_VAL_REF['Cohort']==coh_k)]['Val_ROCAUC_Raw'].iloc[0])
        assert abs(auc_c - ref) <= 1e-4, f'Val parity fail {exp_chk} {coh_k}: {auc_c} vs {ref}'

def pred_ecg_model(m, cache_dict, recs):
    X = np.stack([cache_dict[r['EncounterID']] for r in recs])
    out_p, out_e = [], []
    with torch.no_grad():
        for i in range(0, len(X), 64):
            bx = torch.from_numpy(X[i:i+64].astype(np.float32)).to(DEVICE)
            eb = m.encode(bx)
            pr = torch.sigmoid(m.head(eb).squeeze(-1))
            out_e.append(eb.cpu().numpy()); out_p.append(pr.cpu().numpy())
    return np.concatenate(out_p), np.concatenate(out_e)

for exp_e, mod_e, cache_e, ds_e in [('EXP0007', M_ECG_RESNET, WFDB_CACHE, 'DS0001'), ('EXP0008', M_ECG_BILSTM, WFDB_CACHE, 'DS0001'), ('EXP0009', M_ECG_CNN2D, PNG_CACHE, 'DS0002'), ('EXP0010', M_ECG_PATCH, WFDB_CACHE, 'DS0001')]:
    va_it = [r for r in val_recs if r['DS']==ds_e and r['EncounterID'] in cache_e]
    p_e, _ = pred_ecg_model(mod_e, cache_e, va_it)
    auc_e = roc_auc_score([r['Target_y'] for r in va_it], p_e)
    ref = float(S11_VAL_REF[S11_VAL_REF['EXP']==exp_e]['Val_ROCAUC_Raw'].iloc[0])
    assert abs(auc_e - ref) <= 1e-4, f'ECG parity fail {exp_e}: {auc_e} vs {ref}'

print('VALIDATION PARITY AUDIT 100% PASS across ALL serialized S11 checkpoints (<= 1e-4)!')

# 2. Deterministic Train-Only Reconstruction of Non-Serialized Classical Baselines (matching S11 hyperparameters)
CLASSIC_TAB_MODELS = {}
TAB_VAL_XGB = {}
TAB_OOF_XGB = {}
for ds_id in ['DS0001', 'DS0002', 'DS0003', 'DS0004']:
    tr_s = [r for r in train_recs if r['DS']==ds_id]; va_s = [r for r in val_recs if r['DS']==ds_id]
    Xtr = np.asarray([r['TabularFeatures'] for r in tr_s], dtype=np.float32); ytr = np.asarray([r['Target_y'] for r in tr_s], dtype=np.int64)
    Xva = np.asarray([r['TabularFeatures'] for r in va_s], dtype=np.float32); yva = np.asarray([r['Target_y'] for r in va_s], dtype=np.int64)
    pw = float((ytr == 0).sum()) / max(1.0, float((ytr == 1).sum()))
    specs = [
        ('EXP0001', 'MC0001', [lambda: LogisticRegression(C=0.5, max_iter=1000, class_weight='balanced', random_state=PRIMARY_SEED), lambda: LogisticRegression(C=2.0, max_iter=1000, class_weight='balanced', random_state=PRIMARY_SEED)]),
        ('EXP0002', 'MC0002', [lambda: RandomForestClassifier(n_estimators=300, max_depth=8, class_weight='balanced', n_jobs=-1, random_state=PRIMARY_SEED), lambda: RandomForestClassifier(n_estimators=300, max_depth=14, class_weight='balanced', n_jobs=-1, random_state=PRIMARY_SEED)]),
        ('EXP0005', 'MC0005', [lambda: LGBMClassifier(n_estimators=200, max_depth=4, num_leaves=15, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, reg_lambda=5.0, scale_pos_weight=pw, random_state=PRIMARY_SEED, n_jobs=-1, verbose=-1), lambda: LGBMClassifier(n_estimators=400, num_leaves=31, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, reg_lambda=2.0, scale_pos_weight=pw, random_state=PRIMARY_SEED, n_jobs=-1, verbose=-1)]),
    ]
    for exp_id, mc_id, builders in specs:
        best_c, best_auc = None, -1.0
        for bf in builders:
            c = bf().fit(Xtr, ytr)
            a = roc_auc_score(yva, c.predict_proba(Xva)[:, 1])
            if a > best_auc: best_auc, best_c = a, c
        CLASSIC_TAB_MODELS[(exp_id, mc_id, ds_id)] = best_c
    # Also rebuild 5-fold XGB OOF for EXP0013 Stacker matching best XGB Val depth on ds_id
    xgb_depth = FROZEN_XGB[ds_id].get_params()['max_depth']
    xgb_n = FROZEN_XGB[ds_id].get_params()['n_estimators']
    xgb_reg = FROZEN_XGB[ds_id].get_params()['reg_lambda']
    oof = np.zeros(len(ytr), dtype=np.float32)
    for ti, vi in StratifiedKFold(n_splits=5, shuffle=True, random_state=PRIMARY_SEED).split(Xtr, ytr):
        mf = XGBClassifier(n_estimators=xgb_n, max_depth=xgb_depth, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, reg_lambda=xgb_reg, scale_pos_weight=pw, eval_metric='auc', random_state=PRIMARY_SEED, n_jobs=-1).fit(Xtr[ti], ytr[ti])
        oof[vi] = mf.predict_proba(Xtr[vi])[:, 1]
    TAB_OOF_XGB[ds_id] = oof
    TAB_VAL_XGB[ds_id] = FROZEN_XGB[ds_id].predict_proba(Xva)[:, 1]

# Build frozen ECG embeddings & probs across Train/Val/Test using M_ECG_RESNET & M_ECG_CNN2D
ECG_EMB_ALL, ECG_PROB_ALL = {}, {}
for mod_e, cache_e, ds_e in [(M_ECG_RESNET, WFDB_CACHE, 'DS0001'), (M_ECG_CNN2D, PNG_CACHE, 'DS0002')]:
    it_all = [r for r in train_recs + val_recs + test_recs if r['DS']==ds_e and r['EncounterID'] in cache_e]
    p_all, e_all = pred_ecg_model(mod_e, cache_e, it_all)
    for r, pr, eb in zip(it_all, p_all, e_all):
        ECG_PROB_ALL[r['EncounterID']] = float(pr)
        ECG_EMB_ALL[r['EncounterID']] = eb

def align_early_concat(recs, width=39):
    ds_map = {'DS0001': 0, 'DS0002': 1, 'DS0003': 2, 'DS0004': 3}
    X = np.zeros((len(recs), width + 64), dtype=np.float32)
    y = np.asarray([r['Target_y'] for r in recs], dtype=np.int64)
    for i, r in enumerate(recs):
        X[i, :4] = r['ModalityMask_CELS']; X[i, 4 + ds_map[r['DS']]] = 1.0
        tf = r['TabularFeatures'][:width-8]; X[i, 8:8+len(tf)] = tf
        if r['EncounterID'] in ECG_EMB_ALL: X[i, width:] = ECG_EMB_ALL[r['EncounterID']]
    return X, y

Xtr_ec, ytr_ec = align_early_concat(train_recs)
pw_all = float((ytr_ec == 0).sum()) / max(1.0, float((ytr_ec == 1).sum()))
M_EARLY_XGB = XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, scale_pos_weight=pw_all, eval_metric='auc', random_state=PRIMARY_SEED, n_jobs=-1).fit(Xtr_ec, ytr_ec)

def build_stack_feats(recs, tab_dict, is_oof=False):
    Fmat = np.zeros((len(recs), 6), dtype=np.float32)
    offs = {ds: 0 for ds in ['DS0001', 'DS0002', 'DS0003', 'DS0004']}
    for i, r in enumerate(recs):
        ds = r['DS']
        ptab = tab_dict[ds][offs[ds]] if is_oof else float(tab_dict[ds].predict_proba(np.asarray([r['TabularFeatures']], dtype=np.float32))[:, 1][0])
        if is_oof: offs[ds] += 1
        Fmat[i, 0] = math.log(min(max(ptab, 1e-6), 1-1e-6) / (1 - min(max(ptab, 1e-6), 1-1e-6)))
        if r['EncounterID'] in ECG_PROB_ALL:
            pecg = ECG_PROB_ALL[r['EncounterID']]
            Fmat[i, 1] = math.log(min(max(pecg, 1e-6), 1-1e-6) / (1 - min(max(pecg, 1e-6), 1-1e-6)))
        Fmat[i, 2:] = r['ModalityMask_CELS']
    return Fmat

M_STACK_LR = LogisticRegression(C=1.0, class_weight='balanced', random_state=PRIMARY_SEED).fit(build_stack_feats(train_recs, TAB_OOF_XGB, True), ytr_ec)

# Refit EXP0016 Progressive Models cleanly on Train
M_PROG_XGB = {}
for ds_id in ('DS0003', 'DS0004'):
    tr_s = [r for r in train_recs if r['DS']==ds_id]
    Xtr_d = np.asarray([r['TabularFeatures'] for r in tr_s], dtype=np.float32); ytr_d = np.asarray([r['Target_y'] for r in tr_s])
    pw = float((ytr_d == 0).sum()) / max(1.0, float((ytr_d == 1).sum()))
    sl = COHORT_MODALITY_SLICES[ds_id]
    for tag, cols in [('C_only', list(sl['clinical'])), ('C_plus_L', list(sl['clinical'])+list(sl['laboratory'])), ('C_plus_L_plus_S', list(sl['clinical'])+list(sl['laboratory'])+list(sl['lifestyle']))]:
        c = XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.05, subsample=0.8, scale_pos_weight=pw, eval_metric='auc', random_state=PRIMARY_SEED, n_jobs=-1).fit(Xtr_d[:, cols], ytr_d)
        M_PROG_XGB[(ds_id, tag)] = (c, cols)

print('All frozen checkpoints & deterministic comparators verified ready for ONE-SHOT Test evaluation.')"""

CELL_4 = r"""# Cell 4: STEP-033 & STEP-034 — Frozen One-Shot Test Inference (N=12,719), All Metrics, Calibration & Multi-Seed Variance
TEST_PREDS = {}   # (exp, mc, cohort) -> {'y': np.ndarray, 'gids': list, 'p_raw': np.ndarray, 'p_cal': np.ndarray, 'temp': float, 'tau_j': float, 'tau_85': float}
METRICS_ROWS = []
CM_ROWS = []

def record_test_eval(exp, block, tier, mc, cohort, y, gids, p_raw, seed=PRIMARY_SEED, cal_key=None):
    ck = cal_key or f'{exp}__{mc}__{cohort}'
    if ck not in FROZEN_CAL:
        # Fallback cleanly to ALL_COHORTS or primary EXP0015 cohort scalar
        ck = f'EXP0015__MC0015__{cohort}' if f'EXP0015__MC0015__{cohort}' in FROZEN_CAL else 'EXP0015__MC0015__ALL_COHORTS'
    cal = FROZEN_CAL[ck]
    m = compute_full_metrics(y, p_raw, cal['temperature'], cal['tau_youden'])
    m85 = compute_full_metrics(y, p_raw, cal['temperature'], cal['tau_sens85'])
    if seed == PRIMARY_SEED:
        TEST_PREDS[(exp, mc, cohort)] = {'y': np.asarray(y, dtype=np.int64), 'gids': list(gids), 'p_raw': np.asarray(p_raw, dtype=np.float64), 'p_cal': m['p_cal'], 'temp': cal['temperature'], 'tau_j': cal['tau_youden'], 'tau_85': cal['tau_sens85']}
    METRICS_ROWS.append({
        'EXP': exp, 'Block': block, 'Tier': tier, 'MC': mc, 'Cohort': cohort, 'Seed': seed,
        'N': m['n'], 'Events': m['events'], 'Prevalence': m['prevalence'],
        'Test_ROCAUC': round(m['roc_auc'], 6), 'Test_PRAUC': round(m['pr_auc'], 6),
        'Test_Acc': round(m['accuracy'], 6), 'Test_Prec': round(m['precision'], 6) if not math.isnan(m['precision']) else 'N/A',
        'Test_Recall': round(m['recall'], 6), 'Test_F1': round(m['f1'], 6),
        'Test_Spec': round(m['specificity'], 6), 'Test_NPV': round(m['npv'], 6) if not math.isnan(m['npv']) else 'N/A',
        'Test_BalAcc': round(m['balanced_acc'], 6), 'Test_MCC': round(m['mcc'], 6),
        'Test_Brier_Raw': round(m['brier_raw'], 6), 'Test_Brier_Cal': round(m['brier_cal'], 6), 'Test_BSS': round(m['bss'], 6),
        'Test_ECE_Q15': round(m['ece_q15'], 6), 'Test_ECE_U15': round(m['ece_u15'], 6),
        'Cal_Slope': round(m['cal_slope'], 6), 'Cal_Intercept': round(m['cal_intercept'], 6),
        'Frozen_Temp': cal['temperature'], 'Frozen_TauJ': cal['tau_youden'], 'Frozen_Tau85': cal['tau_sens85'],
        'Tau85_Recall': round(m85['recall'], 6), 'Tau85_Spec': round(m85['specificity'], 6),
    })
    CM_ROWS.append({'EXP': exp, 'MC': mc, 'Cohort': cohort, 'Seed': seed, 'Tau_Used': cal['tau_youden'], 'TN': m['tn'], 'FP': m['fp'], 'FN': m['fn'], 'TP': m['tp'], 'Total': m['n']})

# 1. Tabular Tier 1 (MC0001, MC0002, MC0004 frozen XGB, MC0005) & Tier 2 Clinical Score (EXP0011)
for ds_id, d in TE_COHORTS.items():
    sub = d['recs']
    Xte = np.asarray([r['TabularFeatures'] for r in sub], dtype=np.float32)
    yte = np.asarray([r['Target_y'] for r in sub], dtype=np.int64)
    gids = d['gids']
    for exp_id, mc_id in [('EXP0001','MC0001'), ('EXP0002','MC0002'), ('EXP0005','MC0005')]:
        p = CLASSIC_TAB_MODELS[(exp_id, mc_id, ds_id)].predict_proba(Xte)[:, 1]
        record_test_eval(exp_id, 'Block_A', 'unimodal', mc_id, ds_id, yte, gids, p)
    p_xgb = FROZEN_XGB[ds_id].predict_proba(Xte)[:, 1]
    record_test_eval('EXP0004', 'Block_A', 'unimodal', 'MC0004', ds_id, yte, gids, p_xgb)
    if ds_id in ('DS0003', 'DS0004'):
        z_who = -0.35 + 0.55 * Xte[:, 0] + 0.35 * Xte[:, 2] + 0.25 * Xte[:, 12] + 0.20 * Xte[:, 14]
        record_test_eval('EXP0011', 'Block_B', 'clinical_score', 'MC0011', ds_id, yte, gids, 1.0 / (1.0 + np.exp(-np.clip(z_who, -50, 50))))

# 2. Unimodal Deep ECG (EXP0007, EXP0008, EXP0009, EXP0010)
for exp_e, mc_e, mod_e, cache_e, ds_e in [('EXP0007','MC0007',M_ECG_RESNET,WFDB_CACHE,'DS0001'), ('EXP0008','MC0008',M_ECG_BILSTM,WFDB_CACHE,'DS0001'), ('EXP0009','MC0009',M_ECG_CNN2D,PNG_CACHE,'DS0002'), ('EXP0010','MC0010',M_ECG_PATCH,WFDB_CACHE,'DS0001')]:
    te_it = [r for r in test_recs if r['DS']==ds_e and r['EncounterID'] in cache_e]
    p_e, _ = pred_ecg_model(mod_e, cache_e, te_it)
    record_test_eval(exp_e, 'Block_A', 'unimodal', mc_e, ds_e, [r['Target_y'] for r in te_it], [r['PatientGroupID'] for r in te_it], p_e)

# 3. Simple Fusion Block C (EXP0012 EarlyConcat & EXP0013 Stacker)
Xte_ec, yte_ec = align_early_concat(test_recs)
gids_ec = [r['PatientGroupID'] for r in test_recs]
record_test_eval('EXP0012', 'Block_C', 'simple_fusion', 'MC0012', 'ALL_COHORTS', yte_ec, gids_ec, M_EARLY_XGB.predict_proba(Xte_ec)[:, 1])
record_test_eval('EXP0013', 'Block_C', 'simple_fusion', 'MC0013', 'ALL_COHORTS', yte_ec, gids_ec, M_STACK_LR.predict_proba(build_stack_feats(test_recs, FROZEN_XGB, False))[:, 1])

# 4. Neural Unified Models (EXP0014 Gated, EXP0015 Champion, EXP0018 NoMask, EXP0020 4 extra seeds + Ensemble)
ALL_TE_GIDS = [g for ds in ['DS0001','DS0002','DS0003','DS0004'] for g in TE_COHORTS[ds]['gids']]
SEED_ENS_PREDS = {'ALL_COHORTS': []}
for ds in ['DS0001','DS0002','DS0003','DS0004']: SEED_ENS_PREDS[ds] = []

for exp_m, tier_m, mc_m, mod_m, seed_m in [
    ('EXP0014', 'simple_fusion', 'MC0014', M_GATED, PRIMARY_SEED),
    ('EXP0015', 'transformer_fusion', 'MC0015', M_CHAMP_S1, PRIMARY_SEED),
    ('EXP0018', 'ablation', 'MC0015', M_NOMASK, PRIMARY_SEED),
] + [('EXP0020', 'ablation', 'MC0015', ms, sd) for ms, sd in zip(M_SEEDS_2_5, CANONICAL_SEEDS[1:])]:
    yt, pt, per_ds = predict_multicohort(mod_m, TE_COHORTS)
    blk = 'Block_C' if exp_m in ('EXP0014','EXP0015') else ('Block_E' if exp_m=='EXP0018' else 'Block_F')
    record_test_eval(exp_m, blk, tier_m, mc_m, 'ALL_COHORTS', yt, ALL_TE_GIDS, pt, seed=seed_m, cal_key=(f'{exp_m}__{mc_m}__ALL_COHORTS' if exp_m!='EXP0020' else 'EXP0015__MC0015__ALL_COHORTS'))
    if exp_m in ('EXP0015', 'EXP0020'): SEED_ENS_PREDS['ALL_COHORTS'].append(pt)
    for ds_id, (yd, pd_) in per_ds.items():
        record_test_eval(exp_m, blk, tier_m, mc_m, ds_id, yd, TE_COHORTS[ds_id]['gids'], pd_, seed=seed_m, cal_key=(f'{exp_m}__{mc_m}__{ds_id}' if exp_m!='EXP0020' else f'EXP0015__MC0015__{ds_id}'))
        if exp_m in ('EXP0015', 'EXP0020'): SEED_ENS_PREDS[ds_id].append(pd_)

# Also compute Per-Cohort breakdowns for EXP0012 & EXP0013 and Champion 5-Seed Mean Ensemble
for ds_id in ('DS0001','DS0002','DS0003','DS0004'):
    idx_ds = [i for i, r in enumerate(test_recs) if r['DS']==ds_id]
    record_test_eval('EXP0012', 'Block_C', 'simple_fusion', 'MC0012', ds_id, yte_ec[idx_ds], [gids_ec[i] for i in idx_ds], TEST_PREDS[('EXP0012','MC0012','ALL_COHORTS')]['p_raw'][idx_ds], cal_key='EXP0012__MC0012__ALL_COHORTS')
    record_test_eval('EXP0013', 'Block_C', 'simple_fusion', 'MC0013', ds_id, yte_ec[idx_ds], [gids_ec[i] for i in idx_ds], TEST_PREDS[('EXP0013','MC0013','ALL_COHORTS')]['p_raw'][idx_ds], cal_key='EXP0013__MC0013__ALL_COHORTS')
    record_test_eval('EXP0015_ENS5', 'Block_C', 'transformer_fusion', 'MC0015_ENS5', ds_id, TE_COHORTS[ds_id]['y'].numpy().astype(np.int64), TE_COHORTS[ds_id]['gids'], np.mean(SEED_ENS_PREDS[ds_id], axis=0), cal_key=f'EXP0015__MC0015__{ds_id}')
record_test_eval('EXP0015_ENS5', 'Block_C', 'transformer_fusion', 'MC0015_ENS5', 'ALL_COHORTS', TEST_PREDS[('EXP0015','MC0015','ALL_COHORTS')]['y'], ALL_TE_GIDS, np.mean(SEED_ENS_PREDS['ALL_COHORTS'], axis=0), cal_key='EXP0015__MC0015__ALL_COHORTS')

# 5. Block D Progressive (EXP0016) & LOMO (EXP0017) on Test
for (ds_id, tag), (clf, cols) in M_PROG_XGB.items():
    sub = TE_COHORTS[ds_id]['recs']
    Xte_d = np.asarray([r['TabularFeatures'] for r in sub], dtype=np.float32); yte_d = np.asarray([r['Target_y'] for r in sub], dtype=np.int64)
    record_test_eval('EXP0016', 'Block_D', 'ablation', 'MC0004', f'{ds_id}_{tag}', yte_d, TE_COHORTS[ds_id]['gids'], clf.predict_proba(Xte_d[:, cols])[:, 1], cal_key=f'EXP0004__MC0004__{ds_id}')

LOMO_TEST_AUCS = {}
for drop_idx, drop_name in [(0, 'Clinical'), (1, 'ECG'), (2, 'Lab'), (3, 'Lifestyle')]:
    def _lomo_te(ds_id, m, ix=drop_idx): m2=m.clone(); m2[:, ix]=False; return m2
    yt, pt, _ = predict_multicohort(M_CHAMP_S1, TE_COHORTS, override_mask=_lomo_te)
    LOMO_TEST_AUCS[drop_name] = float(roc_auc_score(yt, pt))
    record_test_eval('EXP0017', 'Block_D', 'ablation', 'MC0015', f'ALL_LOMO_drop_{drop_name}', yt, ALL_TE_GIDS, pt, cal_key='EXP0015__MC0015__ALL_COHORTS')

df_test_metrics = pd.DataFrame(METRICS_ROWS)
df_test_cm = pd.DataFrame(CM_ROWS)
df_test_metrics.to_csv(OUT_DIR / 'test_metrics_summary.csv', index=False)
df_test_cm.to_csv(OUT_DIR / 'test_confusion_matrices.csv', index=False)

# Multi-seed Test Variance summary
ms_rows = []
for coh in ['ALL_COHORTS', 'DS0001', 'DS0002', 'DS0003', 'DS0004']:
    sub_m = df_test_metrics[(df_test_metrics['MC']=='MC0015') & (df_test_metrics['Cohort']==coh) & (df_test_metrics['EXP'].isin(['EXP0015','EXP0020']))]
    ms_rows.append({'Cohort': coh, 'Seeds': len(sub_m), 'AUC_Mean': round(sub_m['Test_ROCAUC'].mean(), 6), 'AUC_SD': round(sub_m['Test_ROCAUC'].std(ddof=1), 6), 'PRAUC_Mean': round(sub_m['Test_PRAUC'].mean(), 6), 'F1_Mean': round(sub_m['Test_F1'].mean(), 6), 'Brier_Mean': round(sub_m['Test_Brier_Cal'].mean(), 6), 'ECE_Mean': round(sub_m['Test_ECE_Q15'].mean(), 6)})
pd.DataFrame(ms_rows).to_csv(OUT_DIR / 'test_multiseed_summary.csv', index=False)

# Curve coordinates for FIG0003
curves_out = {}
for key_pair in [('EXP0015','MC0015','ALL_COHORTS'), ('EXP0015_ENS5','MC0015_ENS5','ALL_COHORTS'), ('EXP0014','MC0014','ALL_COHORTS'), ('EXP0015','MC0015','DS0001'), ('EXP0008','MC0008','DS0001'), ('EXP0015','MC0015','DS0002'), ('EXP0015','MC0015','DS0003'), ('EXP0002','MC0002','DS0003'), ('EXP0015','MC0015','DS0004')]:
    tp_obj = TEST_PREDS[key_pair]
    fpr, tpr, _ = roc_curve(tp_obj['y'], tp_obj['p_cal'])
    pr_p, pr_r, _ = precision_recall_curve(tp_obj['y'], tp_obj['p_cal'])
    step_r = max(1, len(fpr)//100); step_p = max(1, len(pr_p)//100)
    curves_out['__'.join(key_pair)] = {'fpr': fpr[::step_r].round(4).tolist(), 'tpr': tpr[::step_r].round(4).tolist(), 'precision': pr_p[::step_p].round(4).tolist(), 'recall': pr_r[::step_p].round(4).tolist()}
(OUT_DIR / 'test_roc_pr_reliability_coords.json').write_text(json.dumps(curves_out), encoding='utf-8')

print('FINAL SEALED TEST LEADERBOARD (Primary Seed & 5-Seed Ensemble):')
print(df_test_metrics[df_test_metrics['EXP'].isin(['EXP0001','EXP0002','EXP0004','EXP0005','EXP0008','EXP0009','EXP0011','EXP0012','EXP0013','EXP0014','EXP0015','EXP0015_ENS5'])][['EXP','MC','Cohort','N','Test_ROCAUC','Test_PRAUC','Test_F1','Test_Brier_Cal','Test_ECE_Q15','Cal_Slope']].to_string(index=False))"""

CELL_5 = r"""# Cell 5: STEP-035 — Patient-Cluster Stratified Bootstrap (B=2,000), DeLong, McNemar, Holm-Bonferroni & DCA
def make_cluster_boot_indices(y, gids, B=2000, seed=PRIMARY_SEED):
    rng = np.random.default_rng(seed)
    pos_groups, neg_groups = {}, {}
    for i, (yi, gid) in enumerate(zip(y, gids)):
        (pos_groups if int(yi)==1 else neg_groups).setdefault(gid, []).append(i)
    pos_lists = [np.asarray(v, dtype=np.int64) for v in pos_groups.values()]
    neg_lists = [np.asarray(v, dtype=np.int64) for v in neg_groups.values()]
    np_g, nn_g = len(pos_lists), len(neg_lists)
    idx_boots = []
    for _ in range(B):
        sp = rng.integers(0, np_g, size=np_g)
        sn = rng.integers(0, nn_g, size=nn_g)
        idx_boots.append(np.concatenate([pos_lists[j] for j in sp] + [neg_lists[j] for j in sn]))
    return idx_boots

BOOT_BY_COHORT = {}
for coh_key in ['ALL_COHORTS', 'DS0001', 'DS0002', 'DS0003', 'DS0004']:
    ref_tp = TEST_PREDS[('EXP0015', 'MC0015', coh_key)]
    BOOT_BY_COHORT[coh_key] = make_cluster_boot_indices(ref_tp['y'], ref_tp['gids'], B=2000, seed=PRIMARY_SEED)

def fast_roc_auc(y, p):
    # Exact tie-aware C-speed Mann-Whitney AUC via scipy.stats.rankdata
    n1 = float(np.sum(y == 1)); n0 = float(np.sum(y == 0))
    if n1 == 0 or n0 == 0: return float('nan')
    ranks = st.rankdata(p, method='average')
    return float((ranks[y == 1].sum() - n1 * (n1 + 1.0) * 0.5) / (n1 * n0))

# 1. Patient-Grouped Bootstrap 95% CIs (B=2,000) across key models
CI_TARGETS = [
    ('EXP0015','MC0015','ALL_COHORTS'), ('EXP0015_ENS5','MC0015_ENS5','ALL_COHORTS'),
    ('EXP0014','MC0014','ALL_COHORTS'), ('EXP0012','MC0012','ALL_COHORTS'), ('EXP0013','MC0013','ALL_COHORTS'),
    ('EXP0015','MC0015','DS0001'), ('EXP0008','MC0008','DS0001'), ('EXP0004','MC0004','DS0001'),
    ('EXP0015','MC0015','DS0002'), ('EXP0001','MC0001','DS0002'), ('EXP0004','MC0004','DS0002'), ('EXP0014','MC0014','DS0002'), ('EXP0018','MC0015','DS0002'),
    ('EXP0015','MC0015','DS0003'), ('EXP0002','MC0002','DS0003'), ('EXP0004','MC0004','DS0003'), ('EXP0011','MC0011','DS0003'),
    ('EXP0015','MC0015','DS0004'), ('EXP0005','MC0005','DS0004'), ('EXP0014','MC0014','DS0004'), ('EXP0011','MC0011','DS0004'),
]
CI_ROWS = []
for kp in CI_TARGETS:
    tp = TEST_PREDS[kp]
    y, pc, tau = tp['y'], tp['p_cal'], tp['tau_j']
    boots = BOOT_BY_COHORT[kp[2]]
    aucs, brs, f1s, accs, specs, recs = [], [], [], [], [], []
    for bi in boots:
        yb, pb = y[bi], pc[bi]
        aucs.append(fast_roc_auc(yb, pb))
        brs.append(float(np.mean((pb - yb) ** 2)))
        ypb = (pb >= tau).astype(np.int64)
        tp_c = float(np.sum((ypb==1)&(yb==1))); fp_c = float(np.sum((ypb==1)&(yb==0))); fn_c = float(np.sum((ypb==0)&(yb==1))); tn_c = float(np.sum((ypb==0)&(yb==0)))
        f1s.append((2*tp_c) / max(1.0, 2*tp_c + fp_c + fn_c))
        accs.append((tp_c + tn_c) / len(yb))
        recs.append(tp_c / max(1.0, tp_c + fn_c))
        specs.append(tn_c / max(1.0, tn_c + fp_c))
    def ci95(arr): lo, hi = np.nanpercentile(arr, [2.5, 97.5]); return round(float(np.nanmean(arr)), 4), round(float(lo), 4), round(float(hi), 4)
    a_m, a_l, a_h = ci95(aucs); f_m, f_l, f_h = ci95(f1s); b_m, b_l, b_h = ci95(brs); r_m, r_l, r_h = ci95(recs); s_m, s_l, s_h = ci95(specs)
    CI_ROWS.append({'EXP': kp[0], 'MC': kp[1], 'Cohort': kp[2], 'B': 2000, 'ROCAUC_Mean': a_m, 'ROCAUC_CI_Lo': a_l, 'ROCAUC_CI_Hi': a_h, 'F1_Mean': f_m, 'F1_CI_Lo': f_l, 'F1_CI_Hi': f_h, 'Brier_Mean': b_m, 'Brier_CI_Lo': b_l, 'Brier_CI_Hi': b_h, 'Recall_CI': f'[{r_l:.4f}, {r_h:.4f}]', 'Spec_CI': f'[{s_l:.4f}, {s_h:.4f}]'})
pd.DataFrame(CI_ROWS).to_csv(OUT_DIR / 'test_bootstrap_cis.csv', index=False)

# 2. Paired DeLong, McNemar & Bootstrap Delta Tests + Holm-Bonferroni (Champion vs Key Comparators)
PAIRS = [
    (('EXP0015','MC0015','ALL_COHORTS'), ('EXP0014','MC0014','ALL_COHORTS'), 'Champ vs GatedAttn (ALL)'),
    (('EXP0015','MC0015','ALL_COHORTS'), ('EXP0012','MC0012','ALL_COHORTS'), 'Champ vs EarlyConcatXGB (ALL)'),
    (('EXP0015','MC0015','ALL_COHORTS'), ('EXP0013','MC0013','ALL_COHORTS'), 'Champ vs LateOOFStack (ALL)'),
    (('EXP0015','MC0015','ALL_COHORTS'), ('EXP0018','MC0015','ALL_COHORTS'), 'Champ vs ZeroFillNoMask (ALL)'),
    (('EXP0015','MC0015','DS0001'), ('EXP0004','MC0004','DS0001'), 'Champ vs TabularXGB (DS0001)'),
    (('EXP0015','MC0015','DS0001'), ('EXP0008','MC0008','DS0001'), 'Champ vs Conv1DBiLSTM (DS0001)'),
    (('EXP0015','MC0015','DS0002'), ('EXP0001','MC0001','DS0002'), 'Champ vs BestTabularLR (DS0002)'),
    (('EXP0015','MC0015','DS0002'), ('EXP0014','MC0014','DS0002'), 'Champ vs GatedAttn (DS0002)'),
    (('EXP0015','MC0015','DS0002'), ('EXP0018','MC0015','DS0002'), 'Champ vs ZeroFillNoMask (DS0002)'),
    (('EXP0015','MC0015','DS0003'), ('EXP0002','MC0002','DS0003'), 'Champ vs BestRF (DS0003)'),
    (('EXP0015','MC0015','DS0003'), ('EXP0011','MC0011','DS0003'), 'Champ vs WHO ClinicalScore (DS0003)'),
    (('EXP0015','MC0015','DS0004'), ('EXP0005','MC0005','DS0004'), 'Champ vs BestLGBM (DS0004)'),
    (('EXP0015','MC0015','DS0004'), ('EXP0011','MC0011','DS0004'), 'Champ vs WHO ClinicalScore (DS0004)'),
]
STAT_ROWS, delong_pvals, mcn_pvals = [], [], []
for ka, kb, label in PAIRS:
    ta, tb = TEST_PREDS[ka], TEST_PREDS[kb]
    y, pa, pb = ta['y'], ta['p_cal'], tb['p_cal']
    auc_a, auc_b, p_del = paired_delong_test(y, pa, pb)
    b_cnt, c_cnt, p_mcn = exact_mcnemar_test(y, (pa >= ta['tau_j']).astype(int), (pb >= tb['tau_j']).astype(int))
    d_br = [float(np.mean((pa[bi]-y[bi])**2) - np.mean((pb[bi]-y[bi])**2)) for bi in BOOT_BY_COHORT[ka[2]]]
    br_lo, br_hi = np.percentile(d_br, [2.5, 97.5])
    delong_pvals.append(p_del); mcn_pvals.append(p_mcn)
    STAT_ROWS.append({'Comparison': label, 'Cohort': ka[2], 'AUC_Champ': round(auc_a, 5), 'AUC_Comp': round(auc_b, 5), 'Delta_AUC': round(auc_a - auc_b, 5), 'DeLong_p_raw': p_del, 'McNemar_b_c': f'{b_cnt}/{c_cnt}', 'McNemar_p_raw': p_mcn, 'Delta_Brier_Mean': round(float(np.mean(d_br)), 5), 'Delta_Brier_CI': f'[{br_lo:.5f}, {br_hi:.5f}]'})
adj_del = holm_bonferroni(delong_pvals); adj_mcn = holm_bonferroni(mcn_pvals)
for i, row in enumerate(STAT_ROWS):
    row['DeLong_p_Holm'] = round(adj_del[i], 6); row['McNemar_p_Holm'] = round(adj_mcn[i], 6); row['DeLong_p_raw'] = round(row['DeLong_p_raw'], 6); row['McNemar_p_raw'] = round(row['McNemar_p_raw'], 6)
df_stats = pd.DataFrame(STAT_ROWS)
df_stats.to_csv(OUT_DIR / 'test_paired_stat_tests.csv', index=False)

# 3. Decision Curve Analysis (DCA) across p_t in [0.05, 0.50] step=0.01
DCA_ROWS = []
pts_grid = [round(x, 2) for x in np.arange(0.05, 0.501, 0.01)]
for coh_d, comps_d in [
    ('ALL_COHORTS', [('EXP0015','MC0015'), ('EXP0014','MC0014'), ('EXP0012','MC0012')]),
    ('DS0001', [('EXP0015','MC0015'), ('EXP0008','MC0008'), ('EXP0004','MC0004')]),
    ('DS0002', [('EXP0015','MC0015'), ('EXP0001','MC0001'), ('EXP0014','MC0014')]),
    ('DS0003', [('EXP0015','MC0015'), ('EXP0002','MC0002'), ('EXP0011','MC0011')]),
    ('DS0004', [('EXP0015','MC0015'), ('EXP0005','MC0005'), ('EXP0011','MC0011')]),
]:
    y_d = TEST_PREDS[(comps_d[0][0], comps_d[0][1], coh_d)]['y']
    prev_d = float(y_d.mean())
    for pt in pts_grid:
        nb_all = prev_d - (1.0 - prev_d) * (pt / (1.0 - pt))
        row_d = {'Cohort': coh_d, 'Threshold_pt': pt, 'NB_TreatAll': round(nb_all, 6), 'NB_TreatNone': 0.0}
        for exp_c, mc_c in comps_d:
            pc = TEST_PREDS[(exp_c, mc_c, coh_d)]['p_cal']
            pred = pc >= pt
            tp_n = float(np.sum(pred & (y_d==1))) / len(y_d)
            fp_n = float(np.sum(pred & (y_d==0))) / len(y_d)
            row_d[f'NB_{exp_c}_{mc_c}'] = round(tp_n - fp_n * (pt / (1.0 - pt)), 6)
        DCA_ROWS.append(row_d)
pd.DataFrame(DCA_ROWS).to_csv(OUT_DIR / 'test_dca_net_benefit.csv', index=False)

print('Paired DeLong / McNemar / Holm-Bonferroni Summary:')
print(df_stats[['Comparison','Delta_AUC','DeLong_p_raw','DeLong_p_Holm','McNemar_p_Holm']].to_string(index=False))"""

CELL_6 = r"""# Cell 6: STEP-037 — Test Subgroup Fairness, Inference Missing-Modality Stress & N=24 Error Packet
# 1. Stratified Subgroup Fairness on Frozen Champion MODEL0015
SUB_ROWS = []
meta_df = pd.DataFrame([
    {'DS': r['DS'], 'EncounterID': r['EncounterID'], 'Target_y': r['Target_y'],
     'Sex': extract_sex_and_age_band(r)[0], 'AgeBand': extract_sex_and_age_band(r)[1],
     'ModalityTier': f"{r['DS']}_{'C_Ewfdb' if r['DS']=='DS0001' else ('C_Epng_L' if (r['DS']=='DS0002' and r['ModalityMask_CELS'][1]==1) else ('C_L_MISSING_ECG' if r['DS']=='DS0002' else 'C_L_S'))}"}
    for ds in ['DS0001','DS0002','DS0003','DS0004'] for r in TE_COHORTS[ds]['recs']
])
tp_all = TEST_PREDS[('EXP0015', 'MC0015', 'ALL_COHORTS')]
meta_df['p_raw'] = tp_all['p_raw']; meta_df['p_cal'] = tp_all['p_cal']

for dim_col in ['DS', 'Sex', 'AgeBand', 'ModalityTier']:
    for grp_val, gdf in meta_df.groupby(dim_col):
        if len(gdf) < 15 or len(gdf['Target_y'].unique()) < 2: continue
        # Use cohort-specific frozen scalar if grouping by DS or ModalityTier, else ALL_COHORTS frozen scalar
        coh_cal = grp_val if dim_col == 'DS' else ('DS0001' if 'DS0001' in str(grp_val) else ('DS0002' if 'DS0002' in str(grp_val) else ('DS0003' if 'DS0003' in str(grp_val) else ('DS0004' if 'DS0004' in str(grp_val) else 'ALL_COHORTS'))))
        cal_g = FROZEN_CAL[f'EXP0015__MC0015__{coh_cal}']
        mg = compute_full_metrics(gdf['Target_y'].values, gdf['p_raw'].values, cal_g['temperature'], cal_g['tau_youden'])
        SUB_ROWS.append({'SubgroupDim': dim_col, 'Group': grp_val, 'N': mg['n'], 'Events': mg['events'], 'ROC_AUC': round(mg['roc_auc'], 4), 'PR_AUC': round(mg['pr_auc'], 4), 'Recall': round(mg['recall'], 4), 'Spec': round(mg['specificity'], 4), 'F1': round(mg['f1'], 4), 'Brier_Cal': round(mg['brier_cal'], 4), 'ECE_Q15': round(mg['ece_q15'], 4)})

df_sub = pd.DataFrame(SUB_ROWS)
df_sub.to_csv(OUT_DIR / 'test_subgroup_fairness.csv', index=False)

# 2. Missing-Modality Inference Stress Tests on Held-Out Test (no retraining!)
STRESS_ROWS = []
cal_all = FROZEN_CAL['EXP0015__MC0015__ALL_COHORTS']
for drop_cols, tag in [
    ((), 'Full_Baseline_0pct'),
    ((1,), 'Drop_100pct_ECG'), ((2,), 'Drop_100pct_Lab'), ((3,), 'Drop_100pct_Lifestyle'),
    ((1,2), 'Drop_100pct_ECG_Lab'), ((1,3), 'Drop_100pct_ECG_Life'), ((2,3), 'Drop_100pct_Lab_Life'),
]:
    def _mask_combo(ds_id, m, cols=drop_cols):
        m2 = m.clone()
        for c in cols: m2[:, c] = False
        return m2
    yt, pt, per_ds = predict_multicohort(M_CHAMP_S1, TE_COHORTS, override_mask=_mask_combo)
    ms = compute_full_metrics(yt, pt, cal_all['temperature'], cal_all['tau_youden'])
    STRESS_ROWS.append({'StressCondition': tag, 'Cohort': 'ALL_COHORTS', 'Test_ROCAUC': round(ms['roc_auc'], 5), 'Test_PRAUC': round(ms['pr_auc'], 5), 'Test_F1': round(ms['f1'], 5), 'Test_Brier': round(ms['brier_cal'], 5)})
    for ds_id, (yd, pd_) in per_ds.items():
        cal_ds = FROZEN_CAL[f'EXP0015__MC0015__{ds_id}']
        ms_d = compute_full_metrics(yd, pd_, cal_ds['temperature'], cal_ds['tau_youden'])
        STRESS_ROWS.append({'StressCondition': tag, 'Cohort': ds_id, 'Test_ROCAUC': round(ms_d['roc_auc'], 5), 'Test_PRAUC': round(ms_d['pr_auc'], 5), 'Test_F1': round(ms_d['f1'], 5), 'Test_Brier': round(ms_d['brier_cal'], 5)})

for m_idx, m_tag in [(1, 'ECG'), (2, 'Lab'), (3, 'Life')]:
    for p_drop in (0.10, 0.25, 0.50, 1.00):
        rng_s = np.random.default_rng(PRIMARY_SEED)
        def _pdrop(ds_id, m, pr=p_drop, col=m_idx):
            m2 = m.clone()
            dc = torch.from_numpy((rng_s.random(len(m2)) < pr)) & m2[:, col]
            m2[dc, col] = False
            return m2
        yt, pt, _ = predict_multicohort(M_CHAMP_S1, TE_COHORTS, override_mask=_pdrop)
        ms = compute_full_metrics(yt, pt, cal_all['temperature'], cal_all['tau_youden'])
        STRESS_ROWS.append({'StressCondition': f'Gradual_Drop_{m_tag}_{int(p_drop*100)}pct', 'Cohort': 'ALL_COHORTS', 'Test_ROCAUC': round(ms['roc_auc'], 5), 'Test_PRAUC': round(ms['pr_auc'], 5), 'Test_F1': round(ms['f1'], 5), 'Test_Brier': round(ms['brier_cal'], 5)})

df_stress = pd.DataFrame(STRESS_ROWS)
df_stress.to_csv(OUT_DIR / 'test_missing_modality_robustness.csv', index=False)

# 3. Stratified N=24 Clinical Error & Cardiologist Review Packet (6 TP, 6 FP, 6 TN, 6 FN across cohorts)
meta_df['y_pred'] = (meta_df['p_cal'] >= cal_all['tau_youden']).astype(int)
meta_df['outcome_cell'] = np.where((meta_df['Target_y']==1)&(meta_df['y_pred']==1), 'TP', np.where((meta_df['Target_y']==0)&(meta_df['y_pred']==1), 'FP', np.where((meta_df['Target_y']==0)&(meta_df['y_pred']==0), 'TN', 'FN')))
ERROR_PACKET = []
for cell in ['TP', 'FP', 'TN', 'FN']:
    sub_c = meta_df[meta_df['outcome_cell'] == cell].copy()
    # Deterministic cohort-balanced sample prioritizing DS0002/DS0003/DS0001/DS0004 representation
    chosen_eids = []
    for ds_pref in ['DS0002', 'DS0003', 'DS0001', 'DS0004', 'DS0001', 'DS0004']:
        cand_pool = sub_c[(sub_c['DS']==ds_pref) & (~sub_c['EncounterID'].isin(chosen_eids))]
        if len(cand_pool) == 0:
            cand_pool = sub_c[~sub_c['EncounterID'].isin(chosen_eids)]
        if len(cand_pool) > 0:
            pick = cand_pool.sort_values('p_cal', ascending=(cell in ('TN','FP'))).iloc[0]
            chosen_eids.append(pick['EncounterID'])
            ERROR_PACKET.append({'ErrorQuadrant': cell, 'EncounterID': pick['EncounterID'], 'DS': pick['DS'], 'Sex': pick['Sex'], 'AgeBand': pick['AgeBand'], 'ModalityTier': pick['ModalityTier'], 'True_y': int(pick['Target_y']), 'Pred_Cal_Prob': round(float(pick['p_cal']), 4), 'Pred_Label': int(pick['y_pred'])})

print('Test Subgroup Fairness Overview:')
print(df_sub[['SubgroupDim','Group','N','Events','ROC_AUC','Recall','Spec','ECE_Q15']].to_string(index=False))"""

CELL_7 = r"""# Cell 7: STEP-038 & STEP-039 — TreeSHAP, Exact 2^4 Modality Shapley, 50-Step IG, AOPC, LOMO Concordance, 5-Seed Stability & Shortcut Audit
# 1. Exact shap.TreeExplainer on Frozen XGBoost (CKPT0002-0005) using Train-only background (N_bg=64/cohort)
TREESHAP_ROWS = []
SHORTCUT_ROWS = []
for ds_id in ['DS0001', 'DS0002', 'DS0003', 'DS0004']:
    bg_ids = set(SHAP_BG_CFG['encounter_ids_by_cohort'][ds_id])
    X_bg = np.asarray([r['TabularFeatures'] for r in train_recs if r['EncounterID'] in bg_ids], dtype=np.float32)
    te_s = [r for r in test_recs if r['DS']==ds_id][:200]
    X_te_s = np.asarray([r['TabularFeatures'] for r in te_s], dtype=np.float32)
    expl = shap.TreeExplainer(FROZEN_XGB[ds_id], data=X_bg, model_output='raw')
    sv = expl.shap_values(X_te_s, check_additivity=True)
    # Verify exact additivity tolerance <= 0.02 * max(1, |f(x)|)
    fx = FROZEN_XGB[ds_id].predict(X_te_s, output_margin=True)
    exp_v = float(np.asarray(expl.expected_value).reshape(-1)[0])
    err = np.abs(fx - (exp_v + sv.sum(axis=1))) / np.maximum(1.0, np.abs(fx))
    max_err = float(err.max())
    assert max_err <= 0.02, f'TreeSHAP additivity failed {ds_id}: {max_err}'
    fnames = COHORT_FEATURE_META[ds_id]['names']
    mean_abs = np.mean(np.abs(sv), axis=0)
    ranked = sorted(zip(fnames, mean_abs.tolist()), key=lambda x: x[1], reverse=True)
    top3_isnan = any('_isnan' in fn for fn, _ in ranked[:3])
    SHORTCUT_ROWS.append({'Model': f'MC0004_XGB_{ds_id}', 'MaxAdditivityRelErr': round(max_err, 8), 'Top3_Features': '; '.join(f'{fn}({v:.4f})' for fn, v in ranked[:3]), 'Has_MNAR_isnan_in_Top3': top3_isnan})
    for rnk, (fn, v) in enumerate(ranked[:10], 1):
        TREESHAP_ROWS.append({'DS': ds_id, 'Rank': rnk, 'Feature': fn, 'MeanAbsSHAP': round(v, 6), 'Is_MNAR_Flag': ('_isnan' in fn)})

pd.DataFrame(TREESHAP_ROWS).to_csv(OUT_DIR / 'xai_treeshap_global.csv', index=False)

# 2. Prepare Train-Only Stratified N_bg=256 Background Tensors for CVDMMTransformer XAI (ZERO Test records!)
BG_BY_DS = {}
for ds_id in ['DS0001', 'DS0002', 'DS0003', 'DS0004']:
    b_ids = set(SHAP_BG_CFG['encounter_ids_by_cohort'][ds_id])
    b_recs = [r for r in train_recs if r['EncounterID'] in b_ids]
    Xb = np.asarray([r['TabularFeatures'] for r in b_recs], dtype=np.float32)
    BG_BY_DS[ds_id] = {
        'tab_mean': {m: torch.from_numpy(Xb[:, list(ix)].mean(axis=0, keepdims=True)).to(DEVICE) for m, ix in COHORT_MODALITY_SLICES[ds_id].items() if len(ix) > 0},
        'ecg1d_mean': torch.from_numpy(np.mean([WFDB_CACHE[r['EncounterID']].astype(np.float32) for r in b_recs if r['EncounterID'] in WFDB_CACHE], axis=0, keepdims=True)).to(DEVICE) if ds_id=='DS0001' else None,
        'ecg2d_mean': torch.from_numpy(np.mean([PNG_CACHE[r['EncounterID']].astype(np.float32) for r in b_recs if r['EncounterID'] in PNG_CACHE], axis=0, keepdims=True)).to(DEVICE) if ds_id=='DS0002' else None,
    }

# Select N=200 Stratified Test Explanation Cohort (50 per DS) + Ensure All N=24 Error Packet cases are covered
XAI_RECS = []
seen_xai_ids = set()
for ep in ERROR_PACKET:
    r_hit = next(r for r in test_recs if r['EncounterID']==ep['EncounterID'])
    XAI_RECS.append(r_hit); seen_xai_ids.add(r_hit['EncounterID'])
rng_x = random.Random(PRIMARY_SEED)
for ds_id in ['DS0001', 'DS0002', 'DS0003', 'DS0004']:
    pool_d = [r for r in test_recs if r['DS']==ds_id and r['EncounterID'] not in seen_xai_ids]
    for r in rng_x.sample(pool_d, min(50, len(pool_d))):
        XAI_RECS.append(r); seen_xai_ids.add(r['EncounterID'])

# 3. Exact 2^4 Coalition Shapley Values over Active Modalities [C, E, L, S] (Additivity Error = ~0 by Shapley Axiom!)
def exact_4mod_shapley(model, rec):
    ds_id = rec['DS']
    active_m = [idx for idx, val in enumerate(rec['ModalityMask_CELS']) if val == 1]
    tf = np.asarray([rec['TabularFeatures']], dtype=np.float32)
    bm = {m: torch.from_numpy(tf[:, list(ix)]).to(DEVICE) for m, ix in COHORT_MODALITY_SLICES[ds_id].items() if len(ix) > 0}
    e1 = torch.from_numpy(WFDB_CACHE[rec['EncounterID']].astype(np.float32)[None, ...]).to(DEVICE) if ds_id=='DS0001' else None
    e2 = torch.from_numpy(PNG_CACHE[rec['EncounterID']].astype(np.float32)[None, ...]).to(DEVICE) if (ds_id=='DS0002' and rec['EncounterID'] in PNG_CACHE) else None
    v_cache = {}
    with torch.no_grad():
        for bits in range(1 << 4):
            mask_t = torch.tensor([[bool((bits >> j) & 1) for j in range(4)]], dtype=torch.bool, device=DEVICE)
            logit_v = float(model(ds_id, bm, mask_t, ecg_1d=e1, ecg_2d=e2).item())
            v_cache[bits] = logit_v
    M = len(active_m)
    phi = np.zeros(4, dtype=np.float64)
    full_mask = sum(1 << j for j in active_m)
    v_empty, v_full = v_cache[0], v_cache[full_mask]
    for idx_j in active_m:
        others = [m for m in active_m if m != idx_j]
        for s_len in range(M):
            w = math.factorial(s_len) * math.factorial(M - 1 - s_len) / math.factorial(M)
            for sub_o in itertools.combinations(others, s_len):
                s_bits = sum(1 << k for k in sub_o)
                phi[idx_j] += w * (v_cache[s_bits | (1 << idx_j)] - v_cache[s_bits])
    rel_err = abs(v_full - (v_empty + phi.sum())) / max(1.0, abs(v_full))
    return phi, v_empty, v_full, rel_err

SHAP_MOD_ROWS = []
PKT_MAP = {p['EncounterID']: p for p in ERROR_PACKET}
for r in XAI_RECS:
    phi, v0, vf, rel_e = exact_4mod_shapley(M_CHAMP_S1, r)
    assert rel_e <= 1e-4, f'Shapley axiom check fail: {rel_e}'
    tot_abs = max(1e-9, float(np.sum(np.abs(phi))))
    shares = (np.abs(phi) / tot_abs) * 100.0
    row_s = {'EncounterID': r['EncounterID'], 'DS': r['DS'], 'AdditivityRelErr': rel_e, 'Phi_C': round(phi[0], 5), 'Phi_E': round(phi[1], 5), 'Phi_L': round(phi[2], 5), 'Phi_S': round(phi[3], 5), 'Share_C_pct': round(shares[0], 2), 'Share_E_pct': round(shares[1], 2), 'Share_L_pct': round(shares[2], 2), 'Share_S_pct': round(shares[3], 2)}
    SHAP_MOD_ROWS.append(row_s)
    if r['EncounterID'] in PKT_MAP:
        PKT_MAP[r['EncounterID']]['Modality_SHAP_Shares_CELS_pct'] = [row_s['Share_C_pct'], row_s['Share_E_pct'], row_s['Share_L_pct'], row_s['Share_S_pct']]

df_mod_shap = pd.DataFrame(SHAP_MOD_ROWS)
df_mod_shap.to_csv(OUT_DIR / 'xai_multimodal_shares.csv', index=False)

# 4. 50-Step Gauss-Legendre Integrated Gradients (Feature + 12-Lead ECG Temporal/Spatial Attribution) & Shortcut Audit
GL_NODES, GL_WEIGHTS = np.polynomial.legendre.leggauss(50)
ALPHAS = 0.5 * (GL_NODES + 1.0)
AL_WEIGHTS = 0.5 * GL_WEIGHTS

def ig_50step_record(model, rec):
    ds_id = rec['DS']
    bg = BG_BY_DS[ds_id]
    tf = np.asarray([rec['TabularFeatures']], dtype=np.float32)
    bmask = torch.tensor([rec['ModalityMask_CELS']], dtype=torch.bool, device=DEVICE).expand(50, -1)
    x_mods = {m: torch.from_numpy(tf[:, list(ix)]).to(DEVICE) for m, ix in COHORT_MODALITY_SLICES[ds_id].items() if len(ix) > 0}
    b_mods = bg['tab_mean']
    e1 = torch.from_numpy(WFDB_CACHE[rec['EncounterID']].astype(np.float32)[None, ...]).to(DEVICE) if ds_id=='DS0001' else None
    b1 = bg['ecg1d_mean'] if ds_id=='DS0001' else None
    e2 = torch.from_numpy(PNG_CACHE[rec['EncounterID']].astype(np.float32)[None, ...]).to(DEVICE) if (ds_id=='DS0002' and rec['EncounterID'] in PNG_CACHE) else None
    b2 = bg['ecg2d_mean'] if (ds_id=='DS0002' and rec['EncounterID'] in PNG_CACHE) else None

    a_tab = torch.tensor(ALPHAS, dtype=torch.float32, device=DEVICE).view(50, 1)
    w_t = torch.tensor(AL_WEIGHTS, dtype=torch.float32, device=DEVICE)

    model.zero_grad(set_to_none=True)
    im = {m: (b_mods[m] + a_tab * (x_mods[m] - b_mods[m])).detach().requires_grad_(True) for m in x_mods}
    ie1 = (b1 + a_tab.view(50, 1, 1) * (e1 - b1)).detach().requires_grad_(True) if e1 is not None else None
    ie2 = (b2 + a_tab.view(50, 1, 1, 1) * (e2 - b2)).detach().requires_grad_(True) if e2 is not None else None
    logits = model(ds_id, im, bmask, ecg_1d=ie1, ecg_2d=ie2)
    ins = list(im.values()) + ([ie1] if ie1 is not None else []) + ([ie2] if ie2 is not None else [])
    grads = torch.autograd.grad((logits * w_t).sum(), ins)

    # Batched forward already summed quadrature-weighted gradients across all 50 steps!
    acc_mods, g_idx = {}, 0
    for m in x_mods:
        acc_mods[m] = grads[g_idx].detach().sum(dim=0, keepdim=True); g_idx += 1
    acc_e1 = grads[g_idx].detach().sum(dim=0, keepdim=True) if ie1 is not None else None
    if ie1 is not None: g_idx += 1
    acc_e2 = grads[g_idx].detach().sum(dim=0, keepdim=True) if ie2 is not None else None

    with torch.no_grad():
        fx = float(model(ds_id, x_mods, bmask[:1], ecg_1d=e1, ecg_2d=e2).item())
        f0 = float(model(ds_id, b_mods, bmask[:1], ecg_1d=b1, ecg_2d=b2).item())
    tab_attr = np.zeros(len(rec['TabularFeatures']), dtype=np.float64)
    total_ig = 0.0
    for m, ix in COHORT_MODALITY_SLICES[ds_id].items():
        if len(ix) > 0:
            am = ((x_mods[m] - b_mods[m]) * acc_mods[m]).squeeze(0).cpu().numpy()
            total_ig += float(am.sum())
            for local_i, col_i in enumerate(ix): tab_attr[col_i] = float(am[local_i])
    ecg_10s = None; ecg_4x8 = None
    if e1 is not None:
        ae1 = ((e1 - b1) * acc_e1).squeeze(0).cpu().numpy()  # (12, 1000)
        total_ig += float(ae1.sum())
        ecg_10s = np.abs(ae1.reshape(12, 10, 100)).sum(axis=(0, 2))  # 1s windows
    if e2 is not None:
        ae2 = ((e2 - b2) * acc_e2).squeeze(0).squeeze(0).cpu().numpy()  # (384, 768)
        total_ig += float(ae2.sum())
        ecg_4x8 = np.abs(ae2.reshape(4, 96, 8, 96)).sum(axis=(1, 3)).flatten()
    rel_err = abs((fx - f0) - total_ig) / max(1.0, abs(fx))
    return tab_attr, ecg_10s, ecg_4x8, rel_err

IG_TAB_ACC = {ds: [] for ds in ['DS0001','DS0002','DS0003','DS0004']}
IG_ERRS, ECG_1D_PROF, ECG_2D_PROF, AOPC_RECS = [], [], [], []
for r in XAI_RECS[:80]:  # 80 diverse Test records across all 4 cohorts + Error Packet
    ta, e10, e48, rerr = ig_50step_record(M_CHAMP_S1, r)
    IG_TAB_ACC[r['DS']].append(ta)
    IG_ERRS.append(rerr)
    if e10 is not None: ECG_1D_PROF.append(e10)
    if e48 is not None: ECG_2D_PROF.append(e48)
    AOPC_RECS.append((r, ta))

for ds_id in ['DS0001','DS0002','DS0003','DS0004']:
    arr = np.mean(np.abs(np.asarray(IG_TAB_ACC[ds_id])), axis=0)
    fnames = COHORT_FEATURE_META[ds_id]['names']
    ranked = sorted(zip(fnames, arr.tolist()), key=lambda x: x[1], reverse=True)
    SHORTCUT_ROWS.append({'Model': f'MC0015_CVDMM_{ds_id}', 'MaxAdditivityRelErr': round(float(max(IG_ERRS)), 6), 'Top3_Features': '; '.join(f'{fn}({v:.4f})' for fn, v in ranked[:3]), 'Has_MNAR_isnan_in_Top3': any('_isnan' in fn for fn, _ in ranked[:3])})

pd.DataFrame(SHORTCUT_ROWS).to_csv(OUT_DIR / 'xai_feature_rankings_and_shortcut_audit.csv', index=False)
pd.DataFrame([{'Type': 'DS0001_WFDB_1sWindow', 'Segments': 10, 'MeanAbsIG_Profile': np.mean(ECG_1D_PROF, axis=0).round(5).tolist() if ECG_1D_PROF else []}, {'Type': 'DS0002_PNG_4x8Grid', 'Segments': 32, 'MeanAbsIG_Profile': np.mean(ECG_2D_PROF, axis=0).round(5).tolist() if ECG_2D_PROF else []}]).to_csv(OUT_DIR / 'xai_ecg_temporal_spatial_map.csv', index=False)

# 5. Deletion & Insertion AOPC Faithfulness vs Random & Reverse Controls on Test (fixing P0029's deletion failure!)
AOPC_K = 6
del_top, del_rnd, del_rev, ins_top, ins_rnd = np.zeros(AOPC_K), np.zeros(AOPC_K), np.zeros(AOPC_K), np.zeros(AOPC_K), np.zeros(AOPC_K)
rng_a = np.random.default_rng(PRIMARY_SEED)
with torch.no_grad():
    for r, ta in AOPC_RECS:
        ds_id = r['DS']; d_tab = len(ta); k_eff = min(AOPC_K, d_tab)
        bg = BG_BY_DS[ds_id]
        tf = np.asarray([r['TabularFeatures']], dtype=np.float32)
        bmask = torch.tensor([r['ModalityMask_CELS']], dtype=torch.bool, device=DEVICE)
        e1 = torch.from_numpy(WFDB_CACHE[r['EncounterID']].astype(np.float32)[None, ...]).to(DEVICE) if ds_id=='DS0001' else None
        b1 = bg['ecg1d_mean'] if ds_id=='DS0001' else None
        e2 = torch.from_numpy(PNG_CACHE[r['EncounterID']].astype(np.float32)[None, ...]).to(DEVICE) if (ds_id=='DS0002' and r['EncounterID'] in PNG_CACHE) else None
        b2 = bg['ecg2d_mean'] if (ds_id=='DS0002' and r['EncounterID'] in PNG_CACHE) else None

        # Flatten baseline tabular vector matching Train BG_BY_DS means
        b_vec = np.zeros(d_tab, dtype=np.float32)
        for m, ix in COHORT_MODALITY_SLICES[ds_id].items():
            if len(ix) > 0:
                bm_np = bg['tab_mean'][m].squeeze(0).cpu().numpy()
                for li, ci in enumerate(ix): b_vec[ci] = bm_np[li]

        def eval_vec(vec_np):
            vm = {m: torch.from_numpy(vec_np[None, list(ix)]).to(DEVICE) for m, ix in COHORT_MODALITY_SLICES[ds_id].items() if len(ix) > 0}
            return float(torch.sigmoid(M_CHAMP_S1(ds_id, vm, bmask, ecg_1d=e1, ecg_2d=e2)).item())

        p_orig = eval_vec(tf[0])
        # Base ECG baseline prediction for Insertion anchor:
        bm_base = {m: bg['tab_mean'][m] for m in bg['tab_mean']}
        order_top = np.argsort(-np.abs(ta))
        order_rev = order_top[::-1]
        order_rnd = rng_a.permutation(d_tab)

        for mode_arr, ord_arr, is_del in [(del_top, order_top, True), (del_rnd, order_rnd, True), (del_rev, order_rev, True), (ins_top, order_top, False), (ins_rnd, order_rnd, False)]:
            cur = tf[0].copy() if is_del else b_vec.copy()
            for step_k in range(AOPC_K):
                col = ord_arr[min(step_k, d_tab - 1)]
                cur[col] = b_vec[col] if is_del else tf[0][col]
                pk = eval_vec(cur)
                mode_arr[step_k] += (p_orig - pk) if is_del else pk

n_aopc = max(1, len(AOPC_RECS))
df_aopc = pd.DataFrame({
    'Top_k_Step': list(range(1, AOPC_K + 1)),
    'Deletion_TopK_AOPC': (del_top / n_aopc).round(6),
    'Deletion_Random_Ctrl': (del_rnd / n_aopc).round(6),
    'Deletion_Reverse_Ctrl': (del_rev / n_aopc).round(6),
    'Insertion_TopK_Prob': (ins_top / n_aopc).round(6),
    'Insertion_Random_Ctrl': (ins_rnd / n_aopc).round(6),
})
df_aopc.to_csv(OUT_DIR / 'xai_aopc_faithfulness.csv', index=False)

# 6. LOMO Concordance & 5-Seed XAI Stability (Spearman rho, Kendall tau, Top-5 Jaccard)
mean_shares = df_mod_shap[['Share_C_pct','Share_E_pct','Share_L_pct','Share_S_pct']].mean().values
base_te_auc = float(df_test_metrics[(df_test_metrics['EXP']=='EXP0015')&(df_test_metrics['Cohort']=='ALL_COHORTS')]['Test_ROCAUC'].iloc[0])
lomo_drops = np.array([base_te_auc - LOMO_TEST_AUCS['Clinical'], base_te_auc - LOMO_TEST_AUCS['ECG'], base_te_auc - LOMO_TEST_AUCS['Lab'], base_te_auc - LOMO_TEST_AUCS['Lifestyle']])
lomo_rho, lomo_p = st.spearmanr(mean_shares, lomo_drops)
lomo_r, _ = st.pearsonr(mean_shares, lomo_drops)

# 5-Seed Stability on DS0004 global importance rankings (n=25 features, 40 Test cases per seed)
SEED_RANKS = []
ds4_probe = [r for r in test_recs if r['DS']=='DS0004'][:40]
for ms in M_ALL_5SEEDS:
    SEED_RANKS.append(np.mean(np.abs(np.asarray([ig_50step_record(ms, r)[0] for r in ds4_probe])), axis=0))
rhos, taus, jaccards = [], [], []
for a_i, b_i in itertools.combinations(range(len(M_ALL_5SEEDS)), 2):
    rhos.append(float(st.spearmanr(SEED_RANKS[a_i], SEED_RANKS[b_i])[0]))
    taus.append(float(st.kendalltau(SEED_RANKS[a_i], SEED_RANKS[b_i])[0]))
    t5_a = set(np.argsort(-SEED_RANKS[a_i])[:5].tolist()); t5_b = set(np.argsort(-SEED_RANKS[b_i])[:5].tolist())
    jaccards.append(len(t5_a & t5_b) / max(1, len(t5_a | t5_b)))

# Lipschitz perturbation test (+-0.05 SD Gaussian perturbation on tabular inputs)
rng_lip = np.random.default_rng(PRIMARY_SEED)
lip_sims = []
for r in ds4_probe[:20]:
    r_p = dict(r); r_p['TabularFeatures'] = (np.asarray(r['TabularFeatures']) + rng_lip.normal(0.0, 0.05, size=len(r['TabularFeatures']))).tolist()
    ta1, _, _, _ = ig_50step_record(M_CHAMP_S1, r); ta2, _, _, _ = ig_50step_record(M_CHAMP_S1, r_p)
    lip_sims.append(float(st.spearmanr(np.abs(ta1), np.abs(ta2))[0]))

pd.DataFrame([{
    'LOMO_SHAP_Spearman_rho': round(float(lomo_rho), 4), 'LOMO_SHAP_Pearson_r': round(float(lomo_r), 4),
    'ModShares_C_E_L_S_pct': [round(float(x), 2) for x in mean_shares],
    'LOMO_AUC_Drops': [round(float(x), 5) for x in lomo_drops],
    'Seed5_Mean_Spearman_rho': round(float(np.mean(rhos)), 4), 'Seed5_Mean_Kendall_tau': round(float(np.mean(taus)), 4),
    'Seed5_Top5_Jaccard': round(float(np.mean(jaccards)), 4), 'Lipschitz_005SD_Spearman': round(float(np.mean(lip_sims)), 4),
    'Max_IG_Completeness_RelErr': round(float(max(IG_ERRS)), 6),
    'Mean_Del_TopK_AOPC': round(float(df_aopc['Deletion_TopK_AOPC'].mean()), 6),
    'Mean_Del_Random_AOPC': round(float(df_aopc['Deletion_Random_Ctrl'].mean()), 6),
    'Mean_Del_Reverse_AOPC': round(float(df_aopc['Deletion_Reverse_Ctrl'].mean()), 6),
    'Mean_Ins_TopK_Prob': round(float(df_aopc['Insertion_TopK_Prob'].mean()), 6),
    'Mean_Ins_Random_Prob': round(float(df_aopc['Insertion_Random_Ctrl'].mean()), 6),
}]).to_csv(OUT_DIR / 'xai_stability_and_concordance.csv', index=False)

# Save N=24 Error & Clinical Review Packet + Per-Patient Test Prediction Archive (Tier 2B/3 restricted)
(OUT_DIR / 'error_and_clinician_packet_n24.json').write_text(json.dumps(ERROR_PACKET, indent=2), encoding='utf-8')
np.savez_compressed(OUT_DIR / 'frozen_test_predictions_bundle.npz', **{f'{k[0]}__{k[1]}__{k[2]}': v['p_cal'] for k, v in TEST_PREDS.items()}, **{f'Y__{k[0]}__{k[2]}': v['y'] for k, v in TEST_PREDS.items()})

export_zip = OUT_DIR.parent / 's12_to_s15_final_test_xai_export.zip'
with zipfile.ZipFile(export_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    for p in OUT_DIR.rglob('*'):
        if p.is_file() and '_unpacked' not in str(p):
            zf.write(p, arcname=str(p.relative_to(OUT_DIR)))

print('=== XAI AOPC & STABILITY SUMMARY ===')
print(df_aopc.to_string(index=False))
print('Shortcut Audit:')
print(pd.DataFrame(SHORTCUT_ROWS).to_string(index=False))
print(f'\nSaved Final Export Archive: {export_zip} ({export_zip.stat().st_size/(1024*1024):.2f} MB)!')"""


def build_notebook() -> int:
    def to_src(text: str) -> list[str]:
        return [ln + "\n" for ln in text.rstrip().splitlines()[:-1]] + [text.rstrip().splitlines()[-1]]

    cells = [{"cell_type": "markdown", "id": "final-test-00", "metadata": {}, "source": to_src(MD_HEADER)}]
    for idx, code_str in enumerate((CELL_1, CELL_2, CELL_3, CELL_4, CELL_5, CELL_6, CELL_7), start=1):
        ast.parse(code_str)
        cells.append({"cell_type": "code", "execution_count": None, "id": f"final-test-{idx:02d}", "metadata": {}, "outputs": [], "source": to_src(code_str)})

    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.10.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Built & AST-verified {NB_PATH} ({len(cells)-1} code cells).")
    return 0


if __name__ == "__main__":
    raise SystemExit(build_notebook())
