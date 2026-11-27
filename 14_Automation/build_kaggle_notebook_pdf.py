"""
Generate a crisp, multi-page Bangla + English Printable PDF Guide for running the
CVD Multimodal Preprocessing & Post-Preprocessing Kaggle Workflow (`PP0001` / `SPLIT0001`).

Reads live cells from:
  05_Preprocessing_Alignment/notebooks/CVD_Multimodal_Kaggle_Preprocessing_Pipeline.ipynb
and verified hashes/metrics from:
  05_Preprocessing_Alignment/fitted_states/PP0001/pp0001_execution_summary.json

Renders styled UTF-8 HTML -> PDF via headless Chrome/Edge (`--print-to-pdf`).
Note: Generated `.pdf` stays gitignored per `.gitignore` (`*.pdf`).
"""

from __future__ import annotations

import html
import json
import os
import shutil
import subprocess

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
NB_PATH = os.path.join(
    REPO_ROOT, "05_Preprocessing_Alignment", "notebooks", "CVD_Multimodal_Kaggle_Preprocessing_Pipeline.ipynb"
)
SUMMARY_PATH = os.path.join(
    REPO_ROOT, "05_Preprocessing_Alignment", "fitted_states", "PP0001", "pp0001_execution_summary.json"
)
OUT_DIR = os.path.join(REPO_ROOT, "05_Preprocessing_Alignment", "notebooks")
HTML_TEMP = os.path.join(REPO_ROOT, "05_Preprocessing_Alignment", "processed", "kaggle_guide_render.html")
PDF_OUT = os.path.join(OUT_DIR, "CVD_Multimodal_Kaggle_Notebook_Guide_PP0001.pdf")

CELL_NOTES_BN = {
    1: (
        "<strong>সেল ১ — Kaggle এনভায়রনমেন্ট সেটআপ ও অটো ডেটাসেট ডিসকভারি:</strong> "
        "এই সেলটি নিজেই শনাক্ত করে কোড Kaggle (<code>/kaggle/input</code>) নাকি লোকাল পিসিতে চলছে। "
        "আউটপুট ফাইল সেভ হবে <code>/kaggle/working/preprocessed_outputs</code> ফোল্ডারে। "
        "Kaggle-এ <code>Add Input</code> দিয়ে চারটি ডেটাসেট অ্যাড করলেই পাথ স্বয়ংক্রিয়ভাবে খুঁজে নেবে।"
    ),
    2: (
        "<strong>সেল ২ — Stage A (রোগী-স্বাধীন) হেল্পার ফাংশন ও প্রোটেকশন গার্ড:</strong> "
        "১) <code>PROHIBITED_LEAK_COLS</code> দিয়ে <code>Troponine - I (Q)</code>, <code>CVD Risk Score</code> এবং টার্গেট লিকেজ কলাম ব্লক করা হয়। "
        "২) <code>Datasheet1 (Edited).csv</code>-কে OpenXML ZIP/XML (<code>Sheet 1</code>) দিয়ে নির্ভুলভাবে পড়া হয়। "
        "৩) ডিজিটাল 12-lead ECG-র জন্য <code>0.5 Hz</code> জিরো-ফেজ Butterworth হাই-পাস (ST-T সেগমেন্ট রক্ষায়) ও <code>50 Hz</code> Notch (<code>fs &gt; 120 Hz</code> গার্ড সহ) এবং "
        "৪) পেপার স্ক্যান PNG-র জন্য <code>90°</code> CCW রোটেশন + লাল গ্রিড রিমুভাল + <code>(256×768)</code> লেটারবক্সিং ডিফাইন করা আছে।"
    ),
    3: (
        "<strong>সেল ৩ — Stage A কোহর্ট ক্লিনিং ও কোয়ারেন্টাইন (কোনো স্ট্যাটিস্টিকস ফিট ছাড়াই):</strong> "
        "প্রতিটি কোহর্ট আলাদা আলাদা ক্লিন করা হয়: <code>PTB-XL</code> থেকে ফ্ল্যাটলাইন <code>ecg_id=12722</code> ও &lt;১৮ বছর বাদ; "
        "<code>CARDIO-ML-ED</code> থেকে ৮টি uncropped <code>.jpg</code> ও ২টি টাইপো বাদ; "
        "<code>CAIR-CVD-2025</code> থেকে <code>SBP &lt;= DBP</code> এবং নেগেটিভ LDL বাদ (সঠিক missingness NaN রেখে); "
        "<code>sulianova</code> থেকে ডুপ্লিকেট কনফ্লিক্ট ও অসম্ভব BP বাদ দিয়ে <code>age / 365.25</code> রূপান্তর করা হয়।"
    ),
    4: (
        "<strong>সেল ৪ — STEP-020 (রোগী-ভিত্তিক স্প্লিট ও জিরো-লিকেজ প্রুফ):</strong> "
        "ইম্পিউটার বা স্কেলার ফিট করার <strong>আগেই</strong> <code>PatientGroupID</code> অনুযায়ী Train / Val / Test ভাগ করা হয়। "
        "<code>PTB-XL</code>-এ অফিশিয়াল <code>strat_fold 1–8 / 9 / 10</code> এবং বাকিগুলোতে <code>StratifiedGroupKFold</code> ব্যবহার করে নিশ্চিত করা হয় "
        "যে একই রোগীর একাধিক ভিজিট কখনোই Train ও Test-এ ভাগ হবে না (<code>PATIENT LEAK</code> অ্যাসার্শন)।"
    ),
    5: (
        "<strong>সেল ৫ — Stage B (শুধুমাত্র Train ডেটায় ফিটকৃত ইমপিউটেশন, স্কেলিং ও এক্সপোর্ট):</strong> "
        "<code>Train</code> সেটের ওপর <code>IterativeImputer (MICE, max_iter=15)</code>, <code>RobustScaler (median/IQR)</code>, এবং <code>OneHotEncoder</code> ফিট করে "
        "<code>FitStateHash</code> তৈরি করা হয়। ইমপিউটেশনের আগে প্রতিটি মিসিং ভ্যালুর জন্য বাইনারি <code>_isnan</code> (MNAR) মাস্ক সংরক্ষণ করা হয়। "
        "প্রি-স্প্লিট SMOTE না চালিয়ে <code>train_pos_weight</code> বের করে <code>*_tabular_splits.npz</code> ও <code>*_train_fitted_pipe.joblib</code> সেভ করা হয়।"
    ),
    6: (
        "<strong>সেল ৬ — ECG ভিজ্যুয়াল ও মরফোলজি যাচাই (Gate G08 রিভিউ প্লট):</strong> "
        "<code>PTB-XL 500 Hz</code>-এর কাঁচা বনাম ফিল্টারকৃত Lead II ওয়েভফর্ম (ST-T সংরক্ষণ সহ পিয়ারসন <code>r</code>) এবং "
        "<code>CARDIO-ML-ED</code> পেপার স্ক্যানের লাল গ্রিড রিমুভ করার আগের ও পরের ছবি পাশাপাশি প্লট করে দেখায়।"
    ),
    7: (
        "<strong>সেল ৭ — ৪-ডাইমেনশনাল মডালিটি প্রেজেন্স মাস্ক (<code>[has_C, has_E, has_L, has_S]</code>) সামারি:</strong> "
        "মাল্টিমোডাল ট্রান্সফর্মার ক্রস-অ্যাটেনশনের জন্য প্রতিটি কোহর্টের অনুপস্থিত মডালিটি মাস্ক প্রিন্ট করে নিশ্চিত করে যে সম্পূর্ণ প্রি-প্রসেসিং মডেলিংয়ের জন্য প্রস্তুত।"
    ),
}

STAGE_S10_STARTER_CODE = '''# ==============================================================================
# Cell 8 (Stage S10 Starter) — Preprocessed Outputs লোড করে Kaggle GPU-তে মডেল রান
# ==============================================================================
import glob, json, numpy as np, torch, torch.nn as nn
from pathlib import Path

WORK_DIR = Path("/kaggle/working/preprocessed_outputs")
COHORT_MASKS = {
    "DS0001_ptbxl":      [1, 1, 0, 0],
    "DS0002_cardiomled": [1, 1, 1, 0],  # C+L_[MISSING_ECG]-এর ক্ষেত্রে [1, 0, 1, 0]
    "DS0003_cair":       [1, 0, 1, 1],
    "DS0004_sulianova":  [1, 0, 1, 1],
}

# ১) প্রতিটি কোহর্টের প্রি-প্রসেসড Tabular টেন্সর ও Train pos_weight লোড করা
for npz_path in sorted(WORK_DIR.glob("*_tabular_splits.npz")):
    ds_name = npz_path.stem.replace("_tabular_splits", "")
    data = np.load(npz_path)
    X_tr, y_tr = data["X_train"], data["y_train"]
    X_va, y_va = data["X_val"],   data["y_val"]
    # লক্ষ রাখুন: y_test / X_test ফাইনাল Gate G12 পর্যন্ত আনসিল করা হবে না!
    n_pos = int((y_tr == 1).sum())
    n_neg = int((y_tr == 0).sum())
    pos_w = torch.tensor([n_neg / max(1, n_pos)], dtype=torch.float32)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_w)
    print(f"[{ds_name}] Train={X_tr.shape}, Val={X_va.shape}, pos_weight={pos_w.item():.4f}, Mask={COHORT_MASKS[ds_name]}")

# ২) Kaggle Output সেভ বা Export করার আগে ম্যান্ডেটরি লিকেজ চেক:
#    - কোনো Train/Val পারফরম্যান্স টিউনিংয়ে Test অ্যারে রিড করবেন না।
#    - Kaggle Notebook-টি অবশ্যই PRIVATE রাখুন এবং /kaggle/working/* GitHub-এ push করবেন না!
'''


def find_browser() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("chrome") or "",
        shutil.which("msedge") or "",
    ]
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    raise FileNotFoundError("Chrome or Microsoft Edge executable not found for PDF rendering.")


def build_html() -> str:
    nb = json.load(open(NB_PATH, encoding="utf-8"))
    summary = json.load(open(SUMMARY_PATH, encoding="utf-8"))

    ecg_aud = summary["ecg_and_png_audit"]
    cohorts = summary["cohorts"]
    parent = summary["parent_hashes"]

    cohort_rows_html = []
    labels = {
        "DS0001": ("PTB-XL", "Digital 12-Lead WFDB + Clinical", "[1, 1, 0, 0]"),
        "DS0002": ("CARDIO-ML-ED", "PNG Paper ECG + ED Vitals/Labs", "[1, 1, 1, 0] / [1, 0, 1, 0]"),
        "DS0003": ("CAIR-CVD-2025", "BD Clinical + Lipids/FBS + Lifestyle", "[1, 0, 1, 1]"),
        "DS0004": ("Kaggle sulianova", "Clinical + Ordinal Lab + Lifestyle", "[1, 0, 1, 1]"),
    }
    for ds_id in ("DS0001", "DS0002", "DS0003", "DS0004"):
        c = cohorts[ds_id]
        name, mods, mask = labels[ds_id]
        sh = c["part_shapes"]
        cohort_rows_html.append(
            f"<tr>"
            f"<td><strong>{ds_id}</strong> ({name})</td>"
            f"<td>{mods}<br><code>{mask}</code></td>"
            f"<td>{sh['train'][0]:,} / {sh['val'][0]:,} / {sh['test'][0]:,}</td>"
            f"<td><strong>{c['n_features']}</strong></td>"
            f"<td>{c['mask_flagged_cells']:,}</td>"
            f"<td>{c['train_pos_weight']}</td>"
            f"<td><code>{c['fit_state_hash'][:12]}...</code></td>"
            f"</tr>"
        )

    code_cells_html = []
    code_idx = 0
    for cell in nb["cells"]:
        src = "".join(cell["source"]).strip()
        if cell["cell_type"] == "code":
            code_idx += 1
            note_bn = CELL_NOTES_BN.get(code_idx, "")
            code_cells_html.append(f"""
            <div class="cell-block">
              <div class="cell-banner">
                <span class="badge">Code Cell {code_idx}</span>
                <div class="bn-note">{note_bn}</div>
              </div>
              <pre><code>{html.escape(src)}</code></pre>
            </div>
            """)

    return f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="utf-8">
<title>CVD Multimodal Kaggle Notebook Guide (PP0001 / STEP-021)</title>
<style>
  @page {{
    size: A4;
    margin: 15mm 13mm 16mm 13mm;
  }}
  body {{
    font-family: "Nirmala UI", "Segoe UI", Arial, sans-serif;
    color: #1a202c;
    font-size: 9.8pt;
    line-height: 1.52;
    margin: 0;
  }}
  .header-card {{
    background: linear-gradient(135deg, #0f2942 0%, #1b4965 100%);
    color: #ffffff;
    padding: 18px 20px;
    border-radius: 8px;
    margin-bottom: 16px;
  }}
  .header-card h1 {{
    margin: 0 0 6px 0;
    font-size: 16pt;
    line-height: 1.25;
  }}
  .header-card .sub {{
    font-size: 9.2pt;
    color: #dbeafe;
  }}
  .meta-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 14px;
    font-size: 8.8pt;
  }}
  h2 {{
    color: #0f2942;
    border-bottom: 2px solid #2563eb;
    padding-bottom: 4px;
    margin-top: 16px;
    margin-bottom: 8px;
    font-size: 12.2pt;
    page-break-after: avoid;
  }}
  h3 {{
    color: #1e3a8a;
    margin-top: 12px;
    margin-bottom: 5px;
    font-size: 10.5pt;
    page-break-after: avoid;
  }}
  .callout {{
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    padding: 9px 12px;
    border-radius: 4px;
    margin: 10px 0;
    break-inside: avoid;
  }}
  .callout-warn {{
    background: #fef2f2;
    border-left: 4px solid #dc2626;
    padding: 9px 12px;
    border-radius: 4px;
    margin: 10px 0;
    break-inside: avoid;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 14px 0;
    font-size: 8.5pt;
    break-inside: avoid;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 5px 7px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background: #e2e8f0;
    color: #0f172a;
    font-weight: 700;
  }}
  code {{
    font-family: "Consolas", "Courier New", monospace;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 8.4pt;
    color: #0f172a;
  }}
  .cell-block {{
    margin: 12px 0;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    overflow: hidden;
  }}
  .cell-banner {{
    background: #f1f5f9;
    padding: 8px 11px;
    border-bottom: 1px solid #cbd5e1;
    break-inside: avoid;
    page-break-after: avoid;
  }}
  .badge {{
    display: inline-block;
    background: #1d4ed8;
    color: #ffffff;
    font-size: 8pt;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    margin-bottom: 4px;
  }}
  .bn-note {{
    font-size: 9pt;
    color: #1e293b;
  }}
  pre {{
    margin: 0;
    padding: 10px 12px;
    background: #0f172a;
    color: #f8fafc;
    overflow-x: hidden;
    white-space: pre-wrap;
    word-break: break-word;
    font-size: 7.7pt;
    line-height: 1.38;
  }}
  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    font-size: 7.7pt;
  }}
  .flow-box {{
    background: #f8fafc;
    border: 1px dashed #64748b;
    padding: 10px;
    border-radius: 6px;
    font-family: "Consolas", monospace;
    font-size: 8.3pt;
    white-space: pre-wrap;
    break-inside: avoid;
  }}
  .page-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<div class="header-card">
  <h1>CVD Multimodal Risk Prediction — Kaggle প্রি-প্রসেসিং ও এক্সিকিউশন নোটবুক গাইড</h1>
  <div class="sub">
    <strong>প্রজেক্ট:</strong> An Explainable Multimodal Framework for Early Cardiovascular Disease Risk Prediction (DIU CSE499)<br>
    <strong>গবেষক:</strong> Rayan Ahmed (232-15-847) &amp; Mohammad Nafis Sadiq (232-15-895) | <strong>তত্ত্বাবধায়ক:</strong> Md. Mizanur Rahman<br>
    <strong>লকড রিলিজ:</strong> <code>STEP-021 / PP0001</code> &amp; <code>SPLIT0001</code> | <strong>Master FitStateHash:</strong> <code>{summary['master_fit_state_hash'][:24]}...</code>
  </div>
</div>

<div class="meta-grid">
  <div><strong>সোর্স নোটবুক (.ipynb):</strong><br><code>05_Preprocessing_Alignment/notebooks/CVD_Multimodal_Kaggle_Preprocessing_Pipeline.ipynb</code></div>
  <div><strong>মোট ভেরিফায়েড রেকর্ড:</strong><br><code>91,781</code> এনকাউন্টার (<code>89,005</code> ইউনিক রোগী | <code>66,338</code> Train / <code>12,724</code> Val / <code>12,719</code> Test)</div>
  <div><strong>SPLIT0001 Manifest SHA-256:</strong><br><code>{parent['SPLIT0001'][:28]}...</code></div>
  <div><strong>লিঙ্কেজ ও প্রাইভেসি গার্ড:</strong><br>Zero Patient Overlap | <code>Tier A</code> (No Troponin/RiskScore) | No Pre-Split SMOTE</div>
</div>

<h2>১. Kaggle-এ রান করার ধাপসমূহ (Step-by-Step Setup Checklist)</h2>
<ol>
  <li><strong>নোটবুক ইমপোর্ট করুন:</strong> আপনার প্রজেক্টের <code>05_Preprocessing_Alignment/notebooks/CVD_Multimodal_Kaggle_Preprocessing_Pipeline.ipynb</code> ফাইলটি Kaggle-এ নতুন নোটবুক খুলে <code>File &rarr; Import Notebook</code> দিয়ে আপলোড করুন।</li>
  <li><strong>অ্যাক্সিলারেটর ও প্রাইভেসি সেটিংস:</strong> ডানদিকের প্যানেল থেকে <strong>Sharing: Private</strong> সেট করুন (কখনোই পাবলিক করবেন না)। <strong>Accelerator: GPU T4 x2 / P100</strong> নির্বাচন করুন এবং <strong>Persistence: Variables and Files</strong> চালু রাখুন (এই প্রি-প্রসেসিং রান করতে <em>Internet OFF</em> রাখলেও চলবে)।</li>
  <li><strong>৪টি ডেটাসেট যুক্ত করুন (<code>+ Add Input</code>):</strong> Kaggle Private Dataset হিসেবে নিচের ফাইলগুলো অ্যাড করুন:
    <ul>
      <li><code>DS0001 PTB-XL</code> (যার ভেতর <code>ptbxl_database.csv</code>, <code>scp_statements.csv</code>, <code>records100/</code>, <code>records500/</code> আছে)</li>
      <li><code>DS0002 CARDIO-ML-ED</code> (যার ভেতর <code>Datasheet1 (Edited).csv</code>, <code>ECG Labels.csv</code>, ও <code>ECGS/</code> ফোল্ডার আছে)</li>
      <li><code>DS0003 CAIR-CVD-2025</code> (<code>CVD Dataset.csv</code>) এবং <code>DS0004 Kaggle sulianova</code> (<code>cardio_train.csv</code>)</li>
    </ul>
  </li>
  <li><strong>অটো-পাথ ডিসকভারি:</strong> সেল ১ রান করলেই <code>/kaggle/input</code>-এর ভেতর ফাইলগুলো নিজে খুঁজে নেবে এবং সব প্রি-প্রসেসড আউটপুট <code>/kaggle/working/preprocessed_outputs/</code>-এ সেভ হবে।</li>
</ol>

<div class="callout-warn">
  <strong>জরুরি নিরাপত্তা নিয়ম (PHI ও GitHub সুরক্ষা):</strong> Kaggle থেকে তৈরি কোনো <code>.npz</code>, <code>.joblib</code>, <code>.csv</code>, বা এই <code>.pdf</code> ফাইল কখনোই GitHub-এ push করবেন না (<code>.gitignore</code> ইতিমধ্যেই এগুলো ব্লক করে রেখেছে)।
</div>

<h2>২. ডাটা-লিকেজ প্রতিরোধী Two-Stage আর্কিটেকচার</h2>
<div class="flow-box">ADJ0001..ADJ0004 (91,781 Eligible Adult Records — Tier 2B Frozen)
   │
   ▼ [STAGE A — Record-Local Deterministic Ops (স্প্লিটের আগে, রোগী-স্বাধীন)]
   │  • age_days / 365.25, BMI গণনা, SBP&lt;=DBP / LDL&lt;0 / ecg_id=12722 / 8টি JPG কোয়ারেন্টাইন
   │  • Tier-A গার্ড (Troponin-I, CVD Risk Score, Diagnosis আউটকাম কলাম ব্লকড)
   │  • WFDB 12-Lead ECG: 0.5 Hz Zero-Phase Butterworth High-Pass + 50 Hz Notch (fs &gt; 120 Hz)
   │  • CARDIO-ML-ED PNG: 90° CCW রোটেশন + লাল গ্রিড রিমুভাল (100%) + 256×768 লেটারবক্সিং
   │
   ▼ [STEP-020 — SPLIT0001 Patient-Grouped Split Barrier (0 Overlap)]
   │  • PTB-XL: Official strat_fold (1–8 Train / 9 Val / 10 Test)
   │  • বাকি কোহর্ট: Connected PatientGroupID Stratified 70% / 15% / 15% (+ 5-Fold Train CV)
   │
   ▼ [STAGE B — Train-Only Fitted Ops (PP0001, Val/Test পরিসংখ্যান সম্পূর্ণ অদৃশ্য)]
   │  • ইম্পিউটেশনের আগেই MNAR {{col}}_isnan মাস্ক তৈরি (যেমন ED Creatinine/WBC অনুপস্থিতি)
   │  • Train-only IterativeImputer (Kaggle MICE) / Median + RobustScaler (IQR) + OneHotEncoder
   │  • প্রি-স্প্লিট SMOTE ছাড়াই Train pos_weight হিসাব ও 4D [has_C, has_E, has_L, has_S] মাস্ক এক্সপোর্ট</div>

<h2>৩. লোকাল <code>PP0001</code> ভেরিফাইড বেঞ্চমার্ক রেফারেন্স (Kaggle রেজাল্ট মেলানোর জন্য)</h2>
<table>
  <thead>
    <tr>
      <th>কোহর্ট</th>
      <th>মডালিটি ও 4D মাস্ক</th>
      <th>Train / Val / Test</th>
      <th>ফিচার ডাইমেনশন</th>
      <th>MNAR মাস্ক সেল</th>
      <th>Train pos_weight</th>
      <th>FitStateHash</th>
    </tr>
  </thead>
  <tbody>
    {"".join(cohort_rows_html)}
  </tbody>
</table>

<div class="callout">
  <strong>ECG সিগন্যাল ও PNG গ্রিড অডিট রেজাল্ট (<code>STEP-021</code> Train স্যাম্পল):</strong><br>
  • <strong>WFDB (N=25 Train):</strong> <code>500 Hz</code> গড় কোরিলেশন <code>r = {ecg_aud['wfdb_hr_mean_corr']}</code>, <code>100 Hz</code> (50 Hz Nyquist সেফ-বাইপাস) <code>r = {ecg_aud['wfdb_lr_mean_corr']}</code>, QRS লোকালাইজড ফেজ-ল্যাগ <code>0 ms</code> (<code>{ecg_aud['wfdb_zero_lag_count']}/{ecg_aud['wfdb_sample_n']}</code>), DC ড্রিফট কমেছে <code>{ecg_aud['wfdb_dc_before_mv']} &rarr; {ecg_aud['wfdb_dc_after_mv']} mV</code>.<br>
  • <strong>CARDIO-ML-ED PNG (N=10 Train):</strong> পোর্ট্রেট রোটেশন শনাক্ত <code>{ecg_aud['png_portrait_count']}/{ecg_aud['png_sample_n']}</code>, লাল গ্রিড সাপ্রেশন <strong><code>{ecg_aud['png_mean_red_suppressed_pct']}%</code></strong>, এবং ডার্ক ECG কালি সংরক্ষণ <strong><code>{ecg_aud['png_mean_ink_preserved_pct']}%</code></strong>।
</div>

<div class="page-break"></div>
<h2>৪. সম্পূর্ণ Kaggle নোটবুক কোড ও বাংলায় বিস্তারিত ব্যাখ্যা (Cells 1–7)</h2>
{"".join(code_cells_html)}

<div class="page-break"></div>
<h2>৫. প্রি-প্রসেসিং শেষ হওয়ার পর Kaggle GPU-তে পরবর্তী ব্যবহার (<code>Stage S10</code> লোডার)</h2>
<p>Cell 1 থেকে Cell 7 রান শেষ হলে <code>/kaggle/working/preprocessed_outputs/</code> ফোল্ডারে সব ডেটাসেটের <code>*_tabular_splits.npz</code> ও <code>*_train_fitted_pipe.joblib</code> তৈরি হয়ে যাবে। নিচের কোডটি দিয়ে আপনি সরাসরি Stage S10 (PyTorch/XGBoost ট্রেনিং) শুরু করতে পারবেন:</p>
<div class="cell-block">
  <div class="cell-banner">
    <span class="badge">Stage S10 GPU Loader</span>
    <div class="bn-note"><strong>বাংলা নোট:</strong> <code>Test</code> সেট আনসিল করার আগে শুধুমাত্র <code>X_train</code> এবং <code>X_val</code> দিয়ে মডেল ও <code>pos_weight</code> ভ্যালিডেট করুন।</div>
  </div>
  <pre><code>{html.escape(STAGE_S10_STARTER_CODE)}</code></pre>
</div>

</body>
</html>
"""


def main() -> None:
    os.makedirs(os.path.dirname(HTML_TEMP), exist_ok=True)
    os.makedirs(OUT_DIR, exist_ok=True)
    html_str = build_html()
    with open(HTML_TEMP, "w", encoding="utf-8") as f:
        f.write(html_str)

    browser = find_browser()
    file_uri = "file:///" + HTML_TEMP.replace("\\", "/")
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_OUT}",
        file_uri,
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0 or not os.path.isfile(PDF_OUT):
        raise RuntimeError(f"PDF export failed (rc={res.returncode}): {res.stderr}")
    size_kb = os.path.getsize(PDF_OUT) / 1024.0
    print(f"PDF GENERATED SUCCESSFULLY: {PDF_OUT} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
