#!/usr/bin/env python3
"""AvianVisitors fork - switch the shipped illustrations to one local set.

A set is a folder of raw model renders, one per image model:

    avian/assets/illustrations/<set>/<slug>.png     (+ <slug>-2.png flight)

The folders are committed as plain git. This cuts every render (cached in <set>/.cut/),
copies the cutouts over avian/assets/illustrations/<slug>.png, rebuilds
dims.json + masks.json and cache-busts apt.js. Commit the result.

Renders that already carry a real alpha channel (qwen-image) are only
cropped. Renders on a flat ground (flux) go through rembg/BiRefNet like
cutout.py; that is slow on CPU, but only runs once per new/changed render.

Usage:
    python3 avian/scripts/use_illustration_set.py                 # default set
    python3 avian/scripts/use_illustration_set.py flux.2-dev
    ILLUSTRATION_SET=flux.2-dev python3 avian/scripts/use_illustration_set.py

After merging upstream, re-run it: it re-applies the set and regenerates
the files that conflict (dims.json, masks.json, the apt.js versions).
"""
from __future__ import annotations
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_SET = "qwen-image-2.1"
AVIAN = Path(__file__).resolve().parents[1]
ILLUS = AVIAN / "assets" / "illustrations"
APT_JS = AVIAN / "frontend" / "apt.js"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MARGIN = 0.02     # same even margin as cutout.py
ALPHA_FLOOR = 8   # qwen leaves alpha 1..8 haze on the ground; drop it
VERSION_LINE = re.compile(r"(var (?:SKETCH|IMG|TABLE)_VERSION = '[^'-]+)(?:-[0-9a-f]{8})?'")

_session = None


def cut(src: Path, dst: Path) -> None:
    from PIL import Image
    im = Image.open(src)
    if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] <= ALPHA_FLOOR:
        a = im.getchannel("A").point(lambda v: 0 if v <= ALPHA_FLOOR else v)
        im.putalpha(a)
    else:
        global _session
        from rembg import new_session, remove
        _session = _session or new_session("birefnet-general")
        im = remove(im.convert("RGB"), session=_session)
    bbox = im.getchannel("A").getbbox()
    if bbox:
        pad = round(MARGIN * max(bbox[2] - bbox[0], bbox[3] - bbox[1]))
        im = im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad),
                      min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad)))
    dst.parent.mkdir(exist_ok=True)
    im.save(dst)


def bust_versions(js: str, digest: str) -> str:
    """Suffix the three apt.js cache versions with the set's digest."""
    return VERSION_LINE.sub(lambda m: f"{m.group(1)}-{digest}'", js)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("set", nargs="?", default=os.environ.get("ILLUSTRATION_SET", DEFAULT_SET),
                    help=f"Set folder under avian/assets/illustrations/ (default: {DEFAULT_SET})")
    args = ap.parse_args()

    src_dir = ILLUS / args.set
    renders = sorted(p for p in src_dir.glob("*.png") if SLUG.fullmatch(p.stem))
    if not renders:
        sets = sorted(d.name for d in ILLUS.iterdir() if d.is_dir() and not d.name.startswith("."))
        print(f"error: no renders in {src_dir} (sets: {', '.join(sets) or 'none'})", file=sys.stderr)
        return 1

    # ponytail: species only in the previously used set stay in place; delete
    # them by hand (or git checkout the upstream file) if sets ever diverge.
    digest = hashlib.sha1()
    for i, p in enumerate(renders, 1):
        c = src_dir / ".cut" / p.name
        if not c.exists() or c.stat().st_mtime < p.stat().st_mtime:
            print(f"  [{i}/{len(renders)}] cut {p.name}", flush=True)
            cut(p, c)
        shutil.copyfile(c, ILLUS / p.name)
        digest.update(p.name.encode() + c.read_bytes())
    digest = digest.hexdigest()[:8]
    print(f"copied {len(renders)} cutouts from {args.set}")

    subprocess.run([sys.executable, str(AVIAN / "scripts" / "build_masks.py")], check=True)
    APT_JS.write_text(bust_versions(APT_JS.read_text(), digest))
    print(f"apt.js cache versions suffixed -{digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
