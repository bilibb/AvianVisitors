#!/usr/bin/env python3
"""use_illustration_set.py: alpha renders crop cleanly, apt.js bust is idempotent.

Run: python3 tests/test_use_illustration_set.py
"""

import importlib.util
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "use_set", ROOT / "avian" / "scripts" / "use_illustration_set.py")
use_set = importlib.util.module_from_spec(spec)
spec.loader.exec_module(use_set)


def test_alpha_render_is_cropped_without_haze():
    with tempfile.TemporaryDirectory() as tmp:
        src, dst = Path(tmp) / "a.png", Path(tmp) / ".cut" / "a.png"
        im = Image.new("RGBA", (200, 200), (255, 0, 255, 1))  # qwen-style haze
        im.paste((10, 20, 30, 255), (50, 60, 150, 110))       # 100x50 bird
        im.save(src)
        use_set.cut(src, dst)
        out = Image.open(dst)
        assert out.size == (104, 54), out.size                # 2% margin
        assert out.getpixel((0, 0))[3] == 0


def test_bust_versions_is_idempotent():
    js = ("var SKETCH_VERSION = 'r12'; // c\n"
          "var IMG_VERSION = 'r12';\nvar TABLE_VERSION = 'r13';\n")
    once = use_set.bust_versions(js, "deadbeef")
    assert "var TABLE_VERSION = 'r13-deadbeef';" in once
    assert once.count("-deadbeef'") == 3
    assert use_set.bust_versions(once, "0badc0de").count("-0badc0de'") == 3


def test_shipped_apt_js_has_all_three_versions():
    js = (ROOT / "avian" / "frontend" / "apt.js").read_text()
    assert len(use_set.VERSION_LINE.findall(js)) == 3


if __name__ == "__main__":
    test_alpha_render_is_cropped_without_haze()
    test_bust_versions_is_idempotent()
    test_shipped_apt_js_has_all_three_versions()
    print("ok")
