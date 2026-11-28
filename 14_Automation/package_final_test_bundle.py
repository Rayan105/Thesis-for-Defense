"""Stage S12–S15 Authorized Test & Freeze Packager for Kaggle Final Evaluation (`G11 PASS`).

Requires explicit G11 authorization (`TACC0002` logged in `test_access_log.csv` strictly
after `G11-20261128-02 PASS`), packages ONLY:
1. `REL0001/test` (`rel0001_test.jsonl`, `rel0001_manifest.json`)
2. `DS0002` Test PNGs processed via Stage-A full-res red-grid clean + 768x384 MinPool (`whitespace=0`)
3. All `15` SHA-256 verified frozen Stage S11 checkpoints (`CKPT0002-CKPT0016`)
4. Validation freeze artifacts (`frozen_validation_calibration.json`, `shap_background_ids.json`, `s11_validation_results.csv`)
into `05_Preprocessing_Alignment/processed/REL0001_kaggle_final_test_bundle.zip` (gitignored).
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from importlib.util import module_from_spec, spec_from_file_location
from src.cvd_mm.dataset import DEFAULT_REL0001_DIR, load_rel0001_partition

_pkg_spec = spec_from_file_location("package_kaggle_ecg_assets", REPO_ROOT / "14_Automation" / "package_kaggle_ecg_assets.py")
_pkg_mod = module_from_spec(_pkg_spec)
_pkg_spec.loader.exec_module(_pkg_mod)
sanitize_kaggle_filename = _pkg_mod.sanitize_kaggle_filename


def collect_test_ds0002_pngs() -> list[dict[str, str]]:
    recs = load_rel0001_partition(
        "test",
        rel_dir=DEFAULT_REL0001_DIR,
        dataset_scope="DS0002",
        gate_g11_unseal_token="G11-20261128-02-TACC0002",
        verify_shard_hash=True,
    )
    entries: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    seen_clean: set[str] = set()
    for rec in recs:
        ecg_ref = rec.get("ECGReference") or {}
        for relp in ecg_ref.get("png_relpaths") or []:
            norm_p = relp.replace("\\", "/")
            if norm_p not in seen_paths:
                seen_paths.add(norm_p)
                src = REPO_ROOT / norm_p
                if not src.is_file():
                    raise FileNotFoundError(f"Missing raw DS0002 Test PNG: {src}")
                raw_name = Path(norm_p).name
                clean_name = sanitize_kaggle_filename(raw_name)
                if clean_name in seen_clean:
                    raise RuntimeError(f"Collision: {raw_name!r} -> {clean_name!r}")
                seen_clean.add(clean_name)
                entries.append({
                    "partition": "test",
                    "encounter_id": rec["EncounterID"],
                    "raw_relpath": norm_p,
                    "raw_filename": raw_name,
                    "filename": clean_name,
                })
    return entries


def main() -> int:
    # Verify TACC0002 exists before opening Test
    tacc = (REPO_ROOT / "03_Datasets_Cohort" / "splits" / "test_access_log.csv").read_text(encoding="utf-8")
    if "TACC0002" not in tacc or "G11-20261128-02" not in tacc:
        raise PermissionError("G11 TACC0002 unseal entry missing in test_access_log.csv!")

    test_all = load_rel0001_partition(
        "test",
        rel_dir=DEFAULT_REL0001_DIR,
        dataset_scope="ALL_COHORTS",
        gate_g11_unseal_token="G11-20261128-02-TACC0002",
        verify_shard_hash=True,
    )
    entries = collect_test_ds0002_pngs()

    tmp_dir = REPO_ROOT / "05_Preprocessing_Alignment" / "processed" / "_tmp_final_test_bundle"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    (tmp_dir / "ds0002_png_test").mkdir(parents=True, exist_ok=True)

    pairs_json = tmp_dir / "_jobs_test.json"
    jobs = [{"src": str(REPO_ROOT / e["raw_relpath"]), "dst": str(tmp_dir / "ds0002_png_test" / e["filename"])} for e in entries]
    pairs_json.write_text(json.dumps(jobs), encoding="utf-8")

    # Reuse identical Stage-A full-res red-grid suppression + 768x384 MinPool C# pipeline
    ps_script = f"""
$csCode = @"
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

public static class EcgStageAMinPoolTest {{
    public static void CleanFullResAndMinPool(string src, string dst, int outW, int outH) {{
        using (var img = new Bitmap(src)) {{
            if (img.Width < img.Height) {{
                img.RotateFlip(RotateFlipType.Rotate270FlipNone);
            }}
            int W = img.Width, H = img.Height;
            var rect = new Rectangle(0, 0, W, H);
            var data = img.LockBits(rect, ImageLockMode.ReadOnly, img.PixelFormat);
            int bpp = Image.GetPixelFormatSize(img.PixelFormat) / 8;
            int stride = data.Stride;
            byte[] raw = new byte[stride * H];
            Marshal.Copy(data.Scan0, raw, 0, raw.Length);
            img.UnlockBits(data);

            byte[] fullGray = new byte[W * H];
            for (int y = 0; y < H; y++) {{
                int rOff = y * stride;
                int gOff = y * W;
                for (int x = 0; x < W; x++) {{
                    int idx = rOff + x * bpp;
                    int b = raw[idx], g = raw[idx + 1], r = raw[idx + 2];
                    int cmax = Math.Max(r, Math.Max(g, b));
                    int redEx = Math.Max(0, r - Math.Max(g, b));
                    int boost = (int)Math.Round(0.299 * r + 0.587 * g + 0.114 * b + 0.75 * redEx);
                    if (boost > 255) boost = 255;
                    fullGray[gOff + x] = (boost >= 155 && cmax >= 165) ? (byte)255 : (byte)boost;
                }}
            }}

            using (var outBmp = new Bitmap(outW, outH, PixelFormat.Format24bppRgb)) {{
                var outRect = new Rectangle(0, 0, outW, outH);
                var outData = outBmp.LockBits(outRect, ImageLockMode.WriteOnly, PixelFormat.Format24bppRgb);
                int outStride = outData.Stride;
                byte[] outBuf = new byte[outStride * outH];
                for (int oy = 0; oy < outH; oy++) {{
                    int y0 = (int)((long)oy * H / outH);
                    int y1 = Math.Max(y0 + 1, (int)((long)(oy + 1) * H / outH));
                    int dOff = oy * outStride;
                    for (int ox = 0; ox < outW; ox++) {{
                        int x0 = (int)((long)ox * W / outW);
                        int x1 = Math.Max(x0 + 1, (int)((long)(ox + 1) * W / outW));
                        byte m = 255;
                        for (int yy = y0; yy < y1; yy++) {{
                            int gRow = yy * W;
                            for (int xx = x0; xx < x1; xx++) {{
                                byte v = fullGray[gRow + xx];
                                if (v < m) m = v;
                            }}
                        }}
                        int pIdx = dOff + ox * 3;
                        outBuf[pIdx] = m; outBuf[pIdx + 1] = m; outBuf[pIdx + 2] = m;
                    }}
                }}
                Marshal.Copy(outBuf, 0, outData.Scan0, outBuf.Length);
                outBmp.UnlockBits(outData);
                outBmp.Save(dst, ImageFormat.Png);
            }}
        }}
    }}
}}
"@
Add-Type -TypeDefinition $csCode -ReferencedAssemblies System.Drawing
$jobs = Get-Content -Raw -Path '{pairs_json}' | ConvertFrom-Json
foreach ($j in $jobs) {{
    [EcgStageAMinPoolTest]::CleanFullResAndMinPool($j.src, $j.dst, 768, 384)
}}
Write-Output ("Cleaned full-res & MinPooled " + $jobs.Count + " Test DS0002 PNGs to 768x384.")
"""
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=True)

    test_man = tmp_dir / "ds0002_png_test_manifest.json"
    test_man.write_text(json.dumps({
        "release_id": "REL0001",
        "partition": "test",
        "authorized_by": "G11-20261128-02 / TACC0002",
        "test_encounters_total": len(test_all),
        "target_size_wh": [768, 384],
        "count": len(entries),
        "files": entries,
    }, indent=2), encoding="utf-8")

    # Package REL0001 test shard + DS0002 Test PNGs + Frozen S11 Checkpoints + Validation Freeze JSONs
    rel_test_p = Path(DEFAULT_REL0001_DIR) / "test" / "rel0001_test.jsonl"
    rel_man_p = Path(DEFAULT_REL0001_DIR) / "rel0001_manifest.json"
    s11_out = REPO_ROOT / "08_Checkpoints" / "binaries" / "S11" / "s11_outputs"
    ckpt_manifest = json.loads((s11_out / "s11_checkpoint_manifest.json").read_text(encoding="utf-8"))

    zip_out = REPO_ROOT / "05_Preprocessing_Alignment" / "processed" / "REL0001_kaggle_final_test_bundle.zip"
    with zipfile.ZipFile(zip_out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write(rel_test_p, arcname="rel0001_test/rel0001_test.jsonl")
        zf.write(rel_man_p, arcname="rel0001_test/rel0001_manifest.json")
        zf.write(test_man, arcname="ds0002_png_test_manifest.json")
        for e in entries:
            zf.write(tmp_dir / "ds0002_png_test" / e["filename"], arcname=f"ds0002_png_test/{e['filename']}")
        zf.write(s11_out / "s11_checkpoint_manifest.json", arcname="s11_checkpoints/s11_checkpoint_manifest.json")
        for c in ckpt_manifest:
            cp = s11_out / "checkpoints" / c["filename"]
            if hashlib.sha256(cp.read_bytes()).hexdigest() != c["sha256"]:
                raise RuntimeError(f"Checksum fail before bundling: {cp.name}")
            zf.write(cp, arcname=f"s11_checkpoints/{c['filename']}")
        for fn in ("frozen_validation_calibration.json", "shap_background_ids.json"):
            zf.write(REPO_ROOT / "09_Evaluation_Stats" / fn, arcname=f"freeze_bundle/{fn}")
        zf.write(REPO_ROOT / "07_Experiments" / "s11_validation_results.csv", arcname="freeze_bundle/s11_validation_results.csv")

    with zipfile.ZipFile(zip_out, "r") as zchk:
        ws = [n for n in zchk.namelist() if any(ch.isspace() for ch in n)]
        if ws:
            raise RuntimeError(f"Whitespace found in Kaggle zip entries: {ws}")

    shutil.rmtree(tmp_dir)
    print(f"Created {zip_out} ({zip_out.stat().st_size/(1024*1024):.2f} MB) | test_rows={len(test_all):,} | ds0002_test_pngs={len(entries)} | ckpts={len(ckpt_manifest)} | whitespace=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
