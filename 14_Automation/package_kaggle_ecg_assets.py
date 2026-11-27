"""Stage-A Train/Val-Only ECG Asset Packager for Kaggle Stage S11 Execution.

Strictly reads ONLY `REL0001/train` and `REL0001/val` shards (NEVER `test`!),
applies deterministic Stage-A portrait-to-landscape `90° CCW` rotation,
FULL-RESOLUTION red millimeter grid suppression (`suppress_red_ecg_grid_rgb`) FIRST,
and then Ink-Preserving Min-Pooling downscale to `768x384` so thin 1-2px QRS traces
are NEVER blurred out by bilinear averaging, writing:
`05_Preprocessing_Alignment/processed/REL0001_ds0002_png_train_val.zip`.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cvd_mm.dataset import DEFAULT_REL0001_DIR, load_rel0001_partition
from src.cvd_mm.schema_ecg import normalize_cardiomled_image_stem


def sanitize_kaggle_filename(name: str) -> str:
    """Normalize basename via CRF contract so Kaggle archive filename checks pass cleanly."""
    p = Path(name)
    stem = re.sub(r"\s+", "_", normalize_cardiomled_image_stem(p.stem))
    suffix = p.suffix.strip().lower()
    clean = f"{stem}{suffix}"
    if not clean or any(ch.isspace() for ch in clean):
        raise ValueError(f"Unsafe Kaggle filename after sanitization: {name!r} -> {clean!r}")
    return clean


def collect_train_val_ds0002_png_map() -> list[dict[str, str]]:
    """Collect unique Train & Val DS0002 PNG paths strictly avoiding test shard."""
    entries: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    seen_clean_names: set[str] = set()
    for part in ("train", "val"):
        recs = load_rel0001_partition(part, rel_dir=DEFAULT_REL0001_DIR, dataset_scope="DS0002")
        for rec in recs:
            ecg_ref = rec.get("ECGReference") or {}
            for relp in ecg_ref.get("png_relpaths") or []:
                norm_p = relp.replace("\\", "/")
                if norm_p not in seen_paths:
                    seen_paths.add(norm_p)
                    src = REPO_ROOT / norm_p
                    if not src.is_file():
                        raise FileNotFoundError(f"Missing raw DS0002 PNG: {src}")
                    raw_name = Path(norm_p).name
                    clean_name = sanitize_kaggle_filename(raw_name)
                    if clean_name in seen_clean_names:
                        raise RuntimeError(f"Sanitized filename collision: {raw_name!r} -> {clean_name!r}")
                    seen_clean_names.add(clean_name)
                    entries.append({
                        "partition": part,
                        "encounter_id": rec["EncounterID"],
                        "raw_relpath": norm_p,
                        "raw_filename": raw_name,
                        "filename": clean_name,
                    })
    return entries


def main() -> int:
    entries = collect_train_val_ds0002_png_map()
    if not entries:
        raise RuntimeError("No Train/Val DS0002 PNG records discovered.")

    tmp_dir = REPO_ROOT / "05_Preprocessing_Alignment" / "processed" / "_tmp_ds0002_png"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    pairs_json = tmp_dir / "_jobs.json"
    jobs = [
        {"src": str(REPO_ROOT / e["raw_relpath"]), "dst": str(tmp_dir / e["filename"])}
        for e in entries
    ]
    pairs_json.write_text(json.dumps(jobs), encoding="utf-8")

    ps_script = f"""
$csCode = @"
using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

public static class EcgStageAMinPool {{
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

            // Step 1: Full-resolution red-grid suppression (preserves thin 1-2px QRS ink!)
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

            // Step 2: Ink-preserving block minimum downscale to 768x384 (24bpp grayscale PNG)
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
                        outBuf[pIdx] = m;
                        outBuf[pIdx + 1] = m;
                        outBuf[pIdx + 2] = m;
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
    [EcgStageAMinPool]::CleanFullResAndMinPool($j.src, $j.dst, 768, 384)
}}
Write-Output ("Cleaned full-res & MinPooled " + $jobs.Count + " Train/Val DS0002 PNGs to 768x384.")
"""
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=True)

    manifest_p = tmp_dir / "ds0002_png_train_val_manifest.json"
    manifest_p.write_text(
        json.dumps({
            "release_id": "REL0001",
            "dataset": "DS0002_CARDIO_ML_ED",
            "partitions_included": ["train", "val"],
            "test_partition_excluded": True,
            "target_size_wh": [768, 384],
            "stage_a_applied": [
                "portrait_90ccw_to_landscape",
                "full_res_suppress_red_ecg_grid_rgb",
                "ink_preserving_minpool_resize_768x384",
            ],
            "count": len(entries),
            "files": entries,
        }, indent=2),
        encoding="utf-8",
    )

    zip_out = REPO_ROOT / "05_Preprocessing_Alignment" / "processed" / "REL0001_ds0002_png_train_val.zip"
    with zipfile.ZipFile(zip_out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write(manifest_p, arcname="ds0002_png_train_val_manifest.json")
        for e in entries:
            zf.write(tmp_dir / e["filename"], arcname=f"ds0002_png/{e['filename']}")

    with zipfile.ZipFile(zip_out, "r") as zf_chk:
        bad_ws = [n for n in zf_chk.namelist() if any(ch.isspace() for ch in n)]
        bad_test = [n for n in zf_chk.namelist() if "test" in n.lower()]
        if bad_ws or bad_test:
            raise RuntimeError(f"Archive invariant failed: whitespace={bad_ws}, test={bad_test}")

    shutil.rmtree(tmp_dir)
    size_mb = zip_out.stat().st_size / (1024 * 1024)
    print(f"Created {zip_out} ({size_mb:.2f} MB) with {len(entries)} ink-preserved 768x384 PNGs (0 Test files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
