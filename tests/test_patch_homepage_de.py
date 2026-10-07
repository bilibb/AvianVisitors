#!/usr/bin/env python3
"""Every German translation key must still match the shipped frontend.

Upstream merges rewrite UI strings; a stale key silently leaves English on
the dashboard. Run: python3 tests/test_patch_homepage_de.py
"""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "patch_de", ROOT / "avian" / "patch_homepage_de.py")
patch_de = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch_de)

TARGETS = [
    ("avian/frontend/index.html", patch_de.HTML_TRANSLATIONS),
    ("avian/frontend/apt.js", patch_de.JS_TRANSLATIONS),
    ("avian/api/wiki.php", patch_de.WIKI_PHP_TRANSLATIONS),
]

stale = []
for rel, translations in TARGETS:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for en in translations:
        if en not in text:
            stale.append((rel, en))

assert not stale, "stale translation keys:\n" + "\n".join(
    f"  {rel}: {en!r}" for rel, en in stale)
print(f"ok - {sum(len(t) for _, t in TARGETS)} keys all match")
