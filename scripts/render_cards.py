"""Render the 4 TokenPocket SVG infographic cards into crisp 1600x900 PNGs using headless Chrome/Edge."""

from __future__ import annotations

import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = WORKSPACE_ROOT / "assets"
PNG_DIR = ASSETS_DIR / "png"

CARD_NAMES = [
    "card-1-hook-overview",
    "card-2-solana-gasfree",
    "card-3-tron-flexible-fees",
    "card-4-cheat-sheet",
]

BROWSER_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]


def find_browser() -> Path:
    for candidate in BROWSER_CANDIDATES:
        if candidate.exists():
            return candidate
    for name in ("chrome", "msedge", "google-chrome", "chromium"):
        found = shutil.which(name)
        if found:
            return Path(found)
    raise FileNotFoundError(
        "Neither Chrome nor Edge was found. Install Chrome or Edge to render PNG cards."
    )


def read_png_dimensions(png_path: Path) -> tuple[int, int]:
    raw = png_path.read_bytes()
    if len(raw) < 24 or raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{png_path} is not a valid PNG file")
    width, height = struct.unpack(">II", raw[16:24])
    return width, height


def render_svg_to_png(browser: Path, svg_path: Path, out_png: Path, width: int = 1600, height: int = 900) -> tuple[int, int]:
    svg_markup = svg_path.read_text(encoding="utf-8")
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  html, body {{
    margin: 0;
    padding: 0;
    width: {width}px;
    height: {height}px;
    overflow: hidden;
    background: #060A14;
  }}
  svg {{
    display: block;
    width: {width}px;
    height: {height}px;
  }}
</style>
</head>
<body>
{svg_markup}
</body>
</html>
"""
    with tempfile.TemporaryDirectory(prefix="tp_card_render_") as tmpdir:
        tmp_path = Path(tmpdir)
        html_file = tmp_path / f"{svg_path.stem}.html"
        profile_dir = tmp_path / "profile"
        html_file.write_text(html_doc, encoding="utf-8")

        cmd = [
            str(browser),
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--user-data-dir={profile_dir}",
            f"--window-size={width},{height}",
            f"--screenshot={out_png}",
            html_file.as_uri(),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        if result.returncode != 0 or not out_png.exists():
            raise RuntimeError(
                f"Failed to render {svg_path.name} (code={result.returncode}): {result.stderr.strip()}"
            )

    return read_png_dimensions(out_png)


def main() -> int:
    browser = find_browser()
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Using headless browser: {browser}")

    for name in CARD_NAMES:
        svg_path = ASSETS_DIR / f"{name}.svg"
        if not svg_path.exists():
            raise FileNotFoundError(f"Missing SVG source: {svg_path}")
        out_png = PNG_DIR / f"{name}.png"
        w, h = render_svg_to_png(browser, svg_path, out_png)
        size_kb = out_png.stat().st_size / 1024
        print(f"Rendered {out_png.name}: {w}x{h} px ({size_kb:.1f} KB)")
        if (w, h) != (1600, 900):
            raise RuntimeError(f"Unexpected dimensions for {out_png.name}: got {w}x{h}, expected 1600x900")

    print("All 4 PNG infographic cards rendered and verified at 1600x900.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
