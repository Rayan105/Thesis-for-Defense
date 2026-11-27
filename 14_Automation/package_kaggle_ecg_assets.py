"""Stage-A Train/Val-Only ECG Asset Packager for Kaggle Stage S11 Execution.

Strictly reads ONLY `REL0001/train` and `REL0001/val` shards (NEVER `test`!),
applies deterministic Stage-A portrait-to-landscape `90° CCW` rotation,
aspect-preserving downscale (`384x192`), and exact `suppress_red_ecg_grid_rgb`
red millimeter grid suppression using native compiled C# `.NET System.Drawing`,
and writes `05_Preprocessing_Alignment/processed/REL0001_ds0002_png_train_val.zip`.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cvd_mm.dataset import DEFAULT_REL0001_DIR, load_rel0001_partition


def collect_train_val_ds0002_png_map() -> list[dict[str, str]]:
    """Collect unique Train & Val DS0002 PNG paths strictly avoiding test shard."""
    entries: list[dict[str, str]] = []
    seen_paths: set[str] = set()
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
                    entries.append({
                        "partition": part,
                        "encounter_id": rec["EncounterID"],
                        "raw_relpath": norm_p,
                        "filename": Path(norm_p).name,
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
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

public static class EcgStageAPng {{
    public static void CleanAndSave(string src, string dst, int width, int height) {{
        using (var img = Image.FromFile(src)) {{
            if (img.Width < img.Height) {{
                img.RotateFlip(RotateFlipType.Rotate270FlipNone);
            }}
            using (var bmp = new Bitmap(width, height, PixelFormat.Format24bppRgb)) {{
                using (var g = Graphics.FromImage(bmp)) {{
                    g.InterpolationMode = InterpolationMode.HighQualityBicubic;
                    g.DrawImage(img, 0, 0, width, height);
                }}
                var rect = new Rectangle(0, 0, width, height);
                var data = bmp.LockBits(rect, ImageLockMode.ReadWrite, PixelFormat.Format24bppRgb);
                int stride = data.Stride;
                byte[] buf = new byte[stride * height];
                Marshal.Copy(data.Scan0, buf, 0, buf.Length);
                for (int y = 0; y < height; y++) {{
                    int rowOff = y * stride;
                    for (int x = 0; x < width; x++) {{
                        int idx = rowOff + x * 3;
                        int b = buf[idx];
                        int gCol = buf[idx + 1];
                        int r = buf[idx + 2];
                        int cmax = Math.Max(r, Math.Max(gCol, b));
                        int redEx = Math.Max(0, r - Math.Max(gCol, b));
                        int boost = (int)Math.Round(0.299 * r + 0.587 * gCol + 0.114 * b + 0.75 * redEx);
                        if (boost > 255) boost = 255;
                        byte gray = (boost >= 155 && cmax >= 165) ? (byte)255 : (byte)boost;
                        buf[idx] = gray;
                        buf[idx + 1] = gray;
                        buf[idx + 2] = gray;
                    }}
                }}
                Marshal.Copy(buf, 0, data.Scan0, buf.Length);
                bmp.UnlockBits(data);
                bmp.Save(dst, ImageFormat.Png);
            }}
        }}
    }}
}}
"@
Add-Type -TypeDefinition $csCode -ReferencedAssemblies System.Drawing
$jobs = Get-Content -Raw -Path '{pairs_json}' | ConvertFrom-Json
foreach ($j in $jobs) {{
    [EcgStageAPng]::CleanAndSave($j.src, $j.dst, 384, 192)
}}
Write-Output ("Cleaned & packaged " + $jobs.Count + " Train/Val DS0002 PNGs to Stage-A 384x192.")
"""
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=True)

    manifest_p = tmp_dir / "ds0002_png_train_val_manifest.json"
    manifest_p.write_text(
        json.dumps({
            "release_id": "REL0001",
            "dataset": "DS0002_CARDIO_ML_ED",
            "partitions_included": ["train", "val"],
            "test_partition_excluded": True,
            "target_size_wh": [384, 192],
            "stage_a_applied": ["portrait_90ccw_to_landscape", "aspect_preserving_resize_384x192", "suppress_red_ecg_grid_rgb"],
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

    shutil.rmtree(tmp_dir)
    size_mb = zip_out.stat().st_size / (1024 * 1024)
    print(f"Created {zip_out} ({size_mb:.2f} MB) with {len(entries)} Stage-A PNGs (0 Test files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
