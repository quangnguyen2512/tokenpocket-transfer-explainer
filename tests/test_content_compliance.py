"""Automated compliance, accuracy, character-limit, and PNG asset verification suite
for Superteam Earn bounty: Create & Earn: Explore TokenPocket's Transfer Features.
"""

from __future__ import annotations

import base64
import re
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

import pytest

WORKSPACE = Path(__file__).resolve().parent.parent
ASSETS_DIR = WORKSPACE / "assets"
PNG_DIR = ASSETS_DIR / "png"
EXPLAINER_HTML = WORKSPACE / "explainer" / "index.html"
X_THREAD_MD = WORKSPACE / "X_THREAD_READY.md"
GOOGLE_DOC_MD = WORKSPACE / "GOOGLE_DOC_SUBMISSION.md"
FINAL_GUIDE_MD = WORKSPACE / "FINAL_5MIN_SUBMIT_GUIDE.md"
GOOGLE_DOC_HTML = WORKSPACE / "GOOGLE_DOC_IMPORT_READY.html"
LAUNCH_PS1 = WORKSPACE / "OPEN_TOKENPOCKET_SUBMIT.ps1"

EXPECTED_CARDS = [
    "card-1-hook-overview",
    "card-2-solana-gasfree",
    "card-3-tron-flexible-fees",
    "card-4-cheat-sheet",
]

OFFICIAL_VIDEO_URL = "https://x.com/TokenPocket_TP/status/2118610097987596552"
OFFICIAL_WEBSITE = "https://tokenpocket.pro"
OFFICIAL_HANDLE = "@TokenPocket_TP"

BANNED_HYPERBOLIC_PHRASES = [
    "unlimited free",
    "guaranteed free forever",
    "always free forever",
    "100% free forever",
    "zero fees forever",
    "free for native sol",
    "free $sol transfer",
    "unconditional free",
]

URL_PATTERN = re.compile(r"https?://\S+")


def _extract_code_blocks(markdown_text: str, lang: str) -> list[str]:
    pattern = re.compile(rf"```{re.escape(lang)}\n(.*?)\n```", re.DOTALL)
    return [m.group(1).strip() for m in pattern.finditer(markdown_text)]


def _x_weighted_length(tweet_text: str) -> int:
    """Compute X character count where every URL counts as 23 chars via t.co."""
    return len(URL_PATTERN.sub("x" * 23, tweet_text))


@pytest.mark.parametrize("card_name", EXPECTED_CARDS)
def test_svg_and_png_assets_exist_and_valid_1600x900(card_name: str) -> None:
    svg_path = ASSETS_DIR / f"{card_name}.svg"
    png_path = PNG_DIR / f"{card_name}.png"

    assert svg_path.exists(), f"Missing SVG asset: {svg_path}"
    assert svg_path.stat().st_size > 1_000, f"SVG asset too small: {svg_path}"
    svg_text = svg_path.read_text(encoding="utf-8")
    assert 'viewBox="0 0 1600 900"' in svg_text

    assert png_path.exists(), f"Missing rendered PNG asset: {png_path}"
    raw = png_path.read_bytes()
    assert len(raw) > 10_000, f"Rendered PNG suspiciously small ({len(raw)} bytes): {png_path}"
    assert raw[:8] == b"\x89PNG\r\n\x1a\n", f"Invalid PNG magic signature in {png_path}"

    width, height = struct.unpack(">II", raw[16:24])
    assert (width, height) == (1600, 900), (
        f"Expected 1600x900 PNG for {png_path.name}, got {width}x{height}"
    )


@pytest.mark.parametrize("doc_path", [X_THREAD_MD, GOOGLE_DOC_MD])
def test_required_official_links_and_tag(doc_path: Path) -> None:
    text = doc_path.read_text(encoding="utf-8")
    assert OFFICIAL_HANDLE in text, f"{doc_path.name} missing mandatory handle {OFFICIAL_HANDLE}"
    assert OFFICIAL_VIDEO_URL in text, f"{doc_path.name} missing mandatory tutorial URL {OFFICIAL_VIDEO_URL}"
    assert OFFICIAL_WEBSITE in text, f"{doc_path.name} missing official website {OFFICIAL_WEBSITE}"


@pytest.mark.parametrize("doc_path", [X_THREAD_MD, GOOGLE_DOC_MD])
def test_solana_exact_facts_and_guardrails(doc_path: Path) -> None:
    text = doc_path.read_text(encoding="utf-8")
    lower = text.lower()
    assert "2.9.0" in text, f"{doc_path.name} missing Solana Android v2.9.0+"
    assert "2.11.0" in text, f"{doc_path.name} missing Solana iOS v2.11.0+"
    assert "3" in text and "gas-free" in lower, f"{doc_path.name} missing 3/day gas-free quota"
    assert "$sol" in lower and ("exclude" in lower or "ngoại trừ" in lower), (
        f"{doc_path.name} must explicitly exclude native $SOL transfers"
    )
    assert "spl" in lower, f"{doc_path.name} must specify SPL tokens"
    assert "50%" in text and "rent" in lower, (
        f"{doc_path.name} should preserve accurate Solana fee (50% burned) + Rent context"
    )


@pytest.mark.parametrize("doc_path", [X_THREAD_MD, GOOGLE_DOC_MD])
def test_tron_exact_facts_and_cost_savers(doc_path: Path) -> None:
    text = doc_path.read_text(encoding="utf-8")
    lower = text.lower()
    assert "usdt" in lower, f"{doc_path.name} missing TRON USDT fee payment"
    assert "usdd" in lower and "2.8.0" in text, f"{doc_path.name} missing TRON USDD fee payment (v2.8.0+)"
    assert "bandwidth" in lower and "energy" in lower, (
        f"{doc_path.name} must explain TRON Bandwidth & Energy"
    )
    assert "energy rental" in lower, f"{doc_path.name} missing TRON Energy Rental"
    assert "3,240" in text, f"{doc_path.name} missing TRON 3,240 daily subsidies allocation"
    assert "coupon" in lower and "redemption code" in lower, (
        f"{doc_path.name} missing TRON Fee Coupons / Redemption Codes"
    )
    assert "psm" in lower, f"{doc_path.name} missing TRON PSM 1:1 USDT<->USDD note"


@pytest.mark.parametrize("doc_path", [X_THREAD_MD, GOOGLE_DOC_MD, EXPLAINER_HTML])
def test_zero_banned_hyperbolic_claims(doc_path: Path) -> None:
    lower = doc_path.read_text(encoding="utf-8").lower()
    for banned in BANNED_HYPERBOLIC_PHRASES:
        assert banned not in lower, f"Banned hyperbolic phrase '{banned}' found in {doc_path.name}"


def test_english_x_thread_structure_and_280_char_limits() -> None:
    text = X_THREAD_MD.read_text(encoding="utf-8")
    en_tweets = _extract_code_blocks(text, "tweet-en")
    assert len(en_tweets) == 6, f"Expected 6 English tweets, found {len(en_tweets)}"

    combined = "\n".join(en_tweets)
    assert OFFICIAL_HANDLE in combined
    assert OFFICIAL_VIDEO_URL in combined
    assert OFFICIAL_WEBSITE in combined

    for idx, tweet in enumerate(en_tweets, start=1):
        raw_len = len(tweet)
        x_len = _x_weighted_length(tweet)
        assert raw_len <= 275, (
            f"English Tweet {idx} raw length is {raw_len} (> 275 chars): {tweet!r}"
        )
        assert x_len <= 275, (
            f"English Tweet {idx} X-weighted length is {x_len} (> 275 chars): {tweet!r}"
        )

    for card_name in EXPECTED_CARDS:
        assert f"assets/png/{card_name}.png" in text, (
            f"Missing PNG attachment marker for {card_name}.png in X_THREAD_READY.md"
        )


def test_vietnamese_thread_limits_and_english_translation_present() -> None:
    x_text = X_THREAD_MD.read_text(encoding="utf-8")
    vi_tweets = _extract_code_blocks(x_text, "tweet-vi")
    assert len(vi_tweets) == 6, f"Expected 6 Vietnamese tweets, found {len(vi_tweets)}"

    for idx, tweet in enumerate(vi_tweets, start=1):
        raw_len = len(tweet)
        x_len = _x_weighted_length(tweet)
        assert raw_len <= 280, (
            f"Vietnamese Tweet {idx} raw length is {raw_len} (> 280 chars): {tweet!r}"
        )
        assert x_len <= 275, (
            f"Vietnamese Tweet {idx} X-weighted length is {x_len} (> 275 chars): {tweet!r}"
        )

    assert x_text.count("English Translation") >= 6, (
        "X_THREAD_READY.md must include English translation for all 6 Vietnamese tweets"
    )

    gdoc_text = GOOGLE_DOC_MD.read_text(encoding="utf-8")
    assert "[PASTE PUBLISHED X LINK HERE]" in gdoc_text
    assert gdoc_text.count("EN Translation:") >= 6, (
        "GOOGLE_DOC_SUBMISSION.md must include English translation for all 6 Vietnamese items"
    )


def test_interactive_explainer_html_completeness() -> None:
    assert EXPLAINER_HTML.exists(), "Missing explainer/index.html"
    html = EXPLAINER_HTML.read_text(encoding="utf-8")
    for scene_id in ("scene-1", "scene-2", "scene-3", "scene-4"):
        assert f'id="{scene_id}"' in html, f"Explainer missing {scene_id}"

    for token in (
        OFFICIAL_HANDLE,
        OFFICIAL_VIDEO_URL,
        OFFICIAL_WEBSITE,
        "v2.9.0+",
        "v2.11.0+",
        "v2.8.0+",
        "3,240",
        "Energy Rental",
        "TRON PSM",
        "$SOL",
        "Auto-Play 45s Video",
        "Clean 16:9 Record Mode",
    ):
        assert token in html, f"Explainer HTML missing required element/fact: {token}"


def test_explainer_inline_javascript_syntax_valid() -> None:
    node_bin = shutil.which("node")
    assert node_bin is not None, "node executable is required to validate inline JS syntax"
    html = EXPLAINER_HTML.read_text(encoding="utf-8")
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.DOTALL)
    assert len(scripts) >= 1, "No inline <script> block found in explainer/index.html"
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as tmp:
        tmp.write("\n".join(scripts))
        tmp_path = Path(tmp.name)
    try:
        res = subprocess.run([node_bin, "--check", str(tmp_path)], capture_output=True, text=True, timeout=15)
        assert res.returncode == 0, f"node --check failed on explainer JS: {res.stderr}"
    finally:
        tmp_path.unlink(missing_ok=True)


@pytest.mark.skipif(not FINAL_GUIDE_MD.exists(), reason="Local private guide is gitignored in public clones")
def test_final_5min_submit_guide_completeness() -> None:
    guide = FINAL_GUIDE_MD.read_text(encoding="utf-8")
    lower = guide.lower()
    for banned in BANNED_HYPERBOLIC_PHRASES:
        assert banned not in lower, f"Banned hyperbolic phrase '{banned}' found in {FINAL_GUIDE_MD.name}"

    assert "@quangnguyen2512" in guide, "Guide must be tailored to @quangnguyen2512"
    assert "Anyone with the link" in guide, "Guide must include Google Doc sharing reminder"
    assert OFFICIAL_HANDLE in guide
    assert OFFICIAL_VIDEO_URL in guide
    assert OFFICIAL_WEBSITE in guide
    assert "2026-12-07T02:30:59Z" in guide

    tweets = _extract_code_blocks(guide, "tweet-en")
    assert len(tweets) == 6, f"Expected 6 copy-paste tweets in FINAL_5MIN_SUBMIT_GUIDE.md, found {len(tweets)}"
    for idx, tweet in enumerate(tweets, start=1):
        assert len(tweet) <= 275, f"Guide Tweet {idx} raw length > 275"
        assert _x_weighted_length(tweet) <= 275, f"Guide Tweet {idx} X-weighted length > 275"

    for card_name in EXPECTED_CARDS:
        expected_abs = str(PNG_DIR / f"{card_name}.png")
        assert expected_abs.lower() in lower, (
            f"Guide missing exact absolute PNG path: {expected_abs}"
        )

    for modal_token in (
        "Link to Your Work",
        "Tweet Link",
        "Please submit a Google Doc link containing your published content link and draft",
        "Anything Else",
    ):
        assert modal_token in guide, f"Guide missing Superteam Earn modal field: {modal_token}"


def test_google_doc_import_ready_html_and_embedded_pngs(tmp_path: Path) -> None:
    import importlib.util

    script_path = WORKSPACE / "scripts" / "build_google_doc_html.py"
    assert script_path.exists(), f"Missing HTML builder script: {script_path}"

    target_html = GOOGLE_DOC_HTML if GOOGLE_DOC_HTML.exists() else (tmp_path / "GOOGLE_DOC_IMPORT_READY.html")
    if not target_html.exists():
        spec = importlib.util.spec_from_file_location("build_google_doc_html", script_path)
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.OUTPUT_HTML = target_html
        mod.build_html()

    html = target_html.read_text(encoding="utf-8")
    lower = html.lower()
    for banned in BANNED_HYPERBOLIC_PHRASES:
        assert banned not in lower, f"Banned phrase '{banned}' in {target_html.name}"

    for token in (
        OFFICIAL_HANDLE,
        OFFICIAL_VIDEO_URL,
        OFFICIAL_WEBSITE,
        "[PASTE_PUBLISHED_X_THREAD_URL_HERE]",
        "v2.9.0+",
        "v2.11.0+",
        "v2.8.0+",
        "3,240",
        "Energy Rental",
        "PSM",
        "$SOL",
    ):
        assert token in html, f"Google Doc HTML missing required token: {token}"

    b64_matches = re.findall(r'src="data:image/png;base64,([A-Za-z0-9+/=]+)"', html)
    assert len(b64_matches) == 4, f"Expected 4 inline base64 PNGs, found {len(b64_matches)}"

    expected_bytes = [(PNG_DIR / f"{c}.png").read_bytes() for c in EXPECTED_CARDS]
    for idx, b64_str in enumerate(b64_matches):
        decoded = base64.b64decode(b64_str)
        assert decoded[:8] == b"\x89PNG\r\n\x1a\n"
        w, h = struct.unpack(">II", decoded[16:24])
        assert (w, h) == (1600, 900)
        assert decoded == expected_bytes[idx], f"Embedded PNG #{idx + 1} does not match {EXPECTED_CARDS[idx]}.png byte-for-byte"


@pytest.mark.skipif(not LAUNCH_PS1.exists(), reason="Local PowerShell HITL launcher is gitignored in public clones")
def test_open_tokenpocket_submit_ps1_targets() -> None:
    ps1 = LAUNCH_PS1.read_text(encoding="utf-8")
    for required in (
        "https://x.com/TokenPocket_TP",
        "https://x.com/compose/post",
        "https://drive.google.com",
        "https://earn.superteam.fun/listings/bounty/create-and-earn-explore-tokenpockets-transfer-features",
        r"assets\png",
        "FINAL_5MIN_SUBMIT_GUIDE.md",
    ):
        assert required in ps1, f"OPEN_TOKENPOCKET_SUBMIT.ps1 missing target: {required}"

