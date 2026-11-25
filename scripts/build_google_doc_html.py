"""Build a self-contained, Google-Docs-Import-Ready HTML file (`GOOGLE_DOC_IMPORT_READY.html`)
that embeds all 4 verified 1600x900 PNG infographics as inline base64 data URIs alongside
the complete fact-checked Google Doc submission content from `FINAL_5MIN_SUBMIT_GUIDE.md`.

Workflow supported:
1. Upload `GOOGLE_DOC_IMPORT_READY.html` to https://drive.google.com -> Right-click -> Open with -> Google Docs
2. Or open `GOOGLE_DOC_IMPORT_READY.html` locally in Chrome/Edge -> Ctrl+A -> Ctrl+C -> Paste into https://docs.new
"""

from __future__ import annotations

import base64
import struct
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
PNG_DIR = WORKSPACE / "assets" / "png"
OUTPUT_HTML = WORKSPACE / "GOOGLE_DOC_IMPORT_READY.html"

CARDS = {
    "card-1-hook-overview": {
        "filename": "card-1-hook-overview.png",
        "alt": "TokenPocket Dual-Chain Overview Infographic (1600x900): Stop Getting Stuck With Zero Gas on Solana & TRON",
        "caption": "Original Infographic 1/4 — card-1-hook-overview.png (1600×900): Stop Getting Stuck With Zero Gas — Solana & TRON Overview",
    },
    "card-2-solana-gasfree": {
        "filename": "card-2-solana-gasfree.png",
        "alt": "TokenPocket Solana Daily Gas-Free Transfers Infographic (1600x900): 3/Account/Day Quota, SPL Tokens, $SOL Excluded",
        "caption": "Original Infographic 2/4 — card-2-solana-gasfree.png (1600×900): Solana 3 Gas-Free Token Transfers Every Day (3-Step UI + Quota & $SOL Guardrail)",
    },
    "card-3-tron-flexible-fees": {
        "filename": "card-3-tron-flexible-fees.png",
        "alt": "TokenPocket TRON Flexible Network Fees Infographic (1600x900): Pay in USDT or USDD + Energy Rental, 3,240 Subsidies & Coupons",
        "caption": "Original Infographic 3/4 — card-3-tron-flexible-fees.png (1600×900): TRON Without TRX — Pay in USDT / USDD + Energy Rental, 3,240 Subsidies & Coupons",
    },
    "card-4-cheat-sheet": {
        "filename": "card-4-cheat-sheet.png",
        "alt": "TokenPocket Complete Solana vs TRON Fee-Saving Cheat Sheet Infographic (1600x900)",
        "caption": "Original Infographic 4/4 — card-4-cheat-sheet.png (1600×900): Complete Solana vs. TRON Fee-Saving Cheat Sheet",
    },
}


def _load_card_data_uri(card_key: str) -> str:
    png_path = PNG_DIR / CARDS[card_key]["filename"]
    raw = png_path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Invalid PNG header: {png_path}")
    width, height = struct.unpack(">II", raw[16:24])
    if (width, height) != (1600, 900):
        raise ValueError(f"Expected 1600x900 for {png_path.name}, got {width}x{height}")
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{b64}"


def _render_figure(card_key: str, data_uri: str) -> str:
    meta = CARDS[card_key]
    # 624x351 matches standard Google Docs 6.5-inch printable width at exact 16:9 while preserving full 1600x900 PNG data.
    return f"""
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="width:624px; max-width:100%; margin:12px 0 18px 0; border:1px solid #cbd5e1; border-collapse:collapse; background-color:#f8fafc;">
      <tr>
        <td style="padding:8px; text-align:center; background-color:#0f172a;">
          <img src="{data_uri}" width="608" height="342" alt="{meta['alt']}" style="width:608px; height:342px; max-width:100%; display:block; margin:0 auto; border:0;" />
        </td>
      </tr>
      <tr>
        <td style="padding:8px 12px; font-family:Arial, Helvetica, sans-serif; font-size:10pt; color:#334155; background-color:#f8fafc; border-top:1px solid #cbd5e1;">
          <strong>{meta['caption']}</strong>
        </td>
      </tr>
    </table>
    """.strip()


def build_html() -> Path:
    uris = {key: _load_card_data_uri(key) for key in CARDS}

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>TokenPocket Transfer Features — Superteam Earn Submission (@quangnguyen2512)</title>
</head>
<body style="font-family:Arial, Helvetica, sans-serif; font-size:11pt; line-height:1.55; color:#111827; background-color:#ffffff; max-width:680px; margin:24px auto; padding:0 16px;">

  <h1 style="font-family:Arial, Helvetica, sans-serif; font-size:20pt; line-height:1.25; color:#0f172a; margin:0 0 8px 0; padding-bottom:8px; border-bottom:2px solid #2563eb;">
    Explore TokenPocket’s Transfer Features — Superteam Earn Submission
  </h1>
  <p style="font-size:10.5pt; color:#475569; margin:0 0 18px 0;">
    <strong>Bounty:</strong> Create &amp; Earn: Explore TokenPocket’s Transfer Features (500 USDC Prize Pool · 10 Winners) &nbsp;|&nbsp;
    <strong>Format:</strong> 6-Post English X Thread + 4 Original 1600×900 Infographics + Fact-Checked Technical Breakdown
  </p>

  <h2 style="font-family:Arial, Helvetica, sans-serif; font-size:15pt; color:#1e3a8a; margin:22px 0 10px 0;">
    1. Submission Metadata &amp; Published Links
  </h2>
  <table cellpadding="6" cellspacing="0" border="1" style="width:100%; border-collapse:collapse; border:1px solid #cbd5e1; font-size:10.5pt; margin-bottom:18px;">
    <tr style="background-color:#f8fafc;">
      <td style="width:34%; border:1px solid #cbd5e1;"><strong>Superteam Earn Profile</strong></td>
      <td style="border:1px solid #cbd5e1;"><a href="https://earn.superteam.fun/t/quangnguyen2512" style="color:#1d4ed8;">https://earn.superteam.fun/t/quangnguyen2512</a> (<code>@quangnguyen2512</code>)</td>
    </tr>
    <tr>
      <td style="border:1px solid #cbd5e1;"><strong>Published X Thread URL</strong></td>
      <td style="border:1px solid #cbd5e1; background-color:#fef9c3;"><strong>[PASTE_PUBLISHED_X_THREAD_URL_HERE]</strong></td>
    </tr>
    <tr style="background-color:#f8fafc;">
      <td style="border:1px solid #cbd5e1;"><strong>Author X Handle</strong></td>
      <td style="border:1px solid #cbd5e1; background-color:#fef9c3;"><strong>[YOUR_X_HANDLE]</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid #cbd5e1;"><strong>Sponsor Followed &amp; Tagged</strong></td>
      <td style="border:1px solid #cbd5e1;"><a href="https://x.com/TokenPocket_TP" style="color:#1d4ed8;">@TokenPocket_TP</a></td>
    </tr>
    <tr style="background-color:#f8fafc;">
      <td style="border:1px solid #cbd5e1;"><strong>Official Video Tutorial Included in X Thread</strong></td>
      <td style="border:1px solid #cbd5e1;"><a href="https://x.com/TokenPocket_TP/status/2118610097987596552" style="color:#1d4ed8;">https://x.com/TokenPocket_TP/status/2118610097987596552</a></td>
    </tr>
    <tr>
      <td style="border:1px solid #cbd5e1;"><strong>Official TokenPocket Website Included</strong></td>
      <td style="border:1px solid #cbd5e1;"><a href="https://tokenpocket.pro" style="color:#1d4ed8;">https://tokenpocket.pro</a></td>
    </tr>
    <tr style="background-color:#f8fafc;">
      <td style="border:1px solid #cbd5e1;"><strong>Language</strong></td>
      <td style="border:1px solid #cbd5e1;">English (full original draft + supporting technical notes below)</td>
    </tr>
    <tr>
      <td style="border:1px solid #cbd5e1;"><strong>Required Coverage</strong></td>
      <td style="border:1px solid #cbd5e1;">Covers <strong>BOTH</strong> (1) TokenPocket Daily Free Transfers on Solana <strong>AND</strong> (2) Paying TRON Network Fees with Supported Tokens (USDT &amp; USDD) + Energy Rental, 3,240 Daily Subsidies, and Network Fee Redemption Codes / Coupons.</td>
    </tr>
  </table>

  <hr style="border:0; border-top:1px solid #e2e8f0; margin:20px 0;" />

  <h2 style="font-family:Arial, Helvetica, sans-serif; font-size:15pt; color:#1e3a8a; margin:22px 0 10px 0;">
    2. Full Published X Thread Draft (English) &amp; Inline Original Infographics
  </h2>

  <h3 style="font-family:Arial, Helvetica, sans-serif; font-size:12.5pt; color:#0f172a; margin:16px 0 6px 0;">
    Tweet 1/6 — Hook &amp; Dual-Chain Overview
  </h3>
  <table cellpadding="10" cellspacing="0" border="1" style="width:100%; border-collapse:collapse; border:1px solid #cbd5e1; background-color:#f8fafc; margin-bottom:8px;">
    <tr>
      <td style="font-family:Arial, Helvetica, sans-serif; font-size:11pt; color:#111827;">
        Ever hold USDT on Solana or TRON, only to get stuck with 0 SOL or 0 TRX for gas?<br /><br />
        @TokenPocket_TP tackles both chains inside one wallet:<br />
        &bull; Solana: 3 daily gas-free SPL transfers<br />
        &bull; TRON: Pay fees in USDT/USDD + subsidies<br /><br />
        Full guide (exact rules &amp; limits) &#129525;&#128071;
      </td>
    </tr>
  </table>
  {_render_figure("card-1-hook-overview", uris["card-1-hook-overview"])}

  <h3 style="font-family:Arial, Helvetica, sans-serif; font-size:12.5pt; color:#0f172a; margin:18px 0 6px 0;">
    Tweet 2/6 — Solana Daily Gas-Free Transfers (Conditions &amp; Limits)
  </h3>
  <table cellpadding="10" cellspacing="0" border="1" style="width:100%; border-collapse:collapse; border:1px solid #cbd5e1; background-color:#f8fafc; margin-bottom:8px;">
    <tr>
      <td style="font-family:Arial, Helvetica, sans-serif; font-size:11pt; color:#111827;">
        1/ Solana Daily Gas-Free Transfers:<br /><br />
        &bull; Quota: 3 gas-free transfers/account/day<br />
        &bull; Covers: ALL SPL tokens (USDT, USDC, etc.)<br />
        &bull; Excludes: Native $SOL transfers<br />
        &bull; Version: Android v2.9.0+ &amp; iOS v2.11.0+<br /><br />
        Removes SOL gas-spike stress within the daily quota.
      </td>
    </tr>
  </table>
  {_render_figure("card-2-solana-gasfree", uris["card-2-solana-gasfree"])}

  <h3 style="font-family:Arial, Helvetica, sans-serif; font-size:12.5pt; color:#0f172a; margin:18px 0 6px 0;">
    Tweet 3/6 — Solana 3-Step Flow &amp; On-Chain Fee Context
  </h3>
  <table cellpadding="10" cellspacing="0" border="1" style="width:100%; border-collapse:collapse; border:1px solid #cbd5e1; background-color:#f8fafc; margin-bottom:14px;">
    <tr>
      <td style="font-family:Arial, Helvetica, sans-serif; font-size:11pt; color:#111827;">
        2/ Solana Gas-Free in 3 taps:<br /><br />
        1. Solana wallet &rarr; SPL token (e.g. USDT) &rarr; [Send]<br />
        2. Fee defaults to SOL (or pick USDT/USDC) &mdash; all show &quot;Gas-Free&quot; within 3/day<br />
        3. Confirm &quot;Gas-Free&quot; &rarr; [Confirm]<br /><br />
        (Solana&#39;s native fee&mdash;50% burned&mdash;+ Rent apply outside quota.)
      </td>
    </tr>
  </table>

  <h3 style="font-family:Arial, Helvetica, sans-serif; font-size:12.5pt; color:#0f172a; margin:18px 0 6px 0;">
    Tweet 4/6 — TRON Without TRX: Pay Network Fees in USDT or USDD
  </h3>
  <table cellpadding="10" cellspacing="0" border="1" style="width:100%; border-collapse:collapse; border:1px solid #cbd5e1; background-color:#f8fafc; margin-bottom:8px;">
    <tr>
      <td style="font-family:Arial, Helvetica, sans-serif; font-size:11pt; color:#111827;">
        3/ TRON Without TRX: Pay Fees in USDT or USDD<br /><br />
        TRC20 needs Bandwidth + Energy (or burns TRX).<br /><br />
        &bull; USDT: Transfer &rarr; pick USDT fee &rarr; Confirm<br />
        &bull; USDD (v2.8.0+): [Transfer] &rarr; [Pay With] &rarr; USDD &rarr; Confirm<br /><br />
        Bonus: swap USDT&harr;USDD 1:1 losslessly via TRON PSM in Swap.
      </td>
    </tr>
  </table>
  {_render_figure("card-3-tron-flexible-fees", uris["card-3-tron-flexible-fees"])}

  <h3 style="font-family:Arial, Helvetica, sans-serif; font-size:12.5pt; color:#0f172a; margin:18px 0 6px 0;">
    Tweet 5/6 — TRON Cost-Saving Features (Energy Rental, Daily Subsidies, Coupons)
  </h3>
  <table cellpadding="10" cellspacing="0" border="1" style="width:100%; border-collapse:collapse; border:1px solid #cbd5e1; background-color:#f8fafc; margin-bottom:14px;">
    <tr>
      <td style="font-family:Arial, Helvetica, sans-serif; font-size:11pt; color:#111827;">
        4/ Stack 3 TRON cost-savers on the send screen:<br /><br />
        &bull; Energy Rental: Rent Energy vs. burning TRX (varies with rates)<br />
        &bull; Daily Subsidies: 3,240/day (FCFS) &mdash; eligible sends show 0 fee<br />
        &bull; Fee Coupons: Enter redemption codes for partial or full discounts
      </td>
    </tr>
  </table>

  <h3 style="font-family:Arial, Helvetica, sans-serif; font-size:12.5pt; color:#0f172a; margin:18px 0 6px 0;">
    Tweet 6/6 — Complete Solana vs. TRON Cheat Sheet &amp; Official Tutorial CTA
  </h3>
  <table cellpadding="10" cellspacing="0" border="1" style="width:100%; border-collapse:collapse; border:1px solid #cbd5e1; background-color:#f8fafc; margin-bottom:8px;">
    <tr>
      <td style="font-family:Arial, Helvetica, sans-serif; font-size:11pt; color:#111827;">
        5/ Save the Solana vs. TRON cheat sheet &amp; watch @TokenPocket_TP&#39;s official tutorial:<br />
        <a href="https://x.com/TokenPocket_TP/status/2118610097987596552" style="color:#1d4ed8;">https://x.com/TokenPocket_TP/status/2118610097987596552</a><br /><br />
        Wallet: <a href="https://tokenpocket.pro" style="color:#1d4ed8;">https://tokenpocket.pro</a><br /><br />
        Which saves you more friction &mdash; Solana 3/day Gas-Free or TRON USDT/USDD fees?
      </td>
    </tr>
  </table>
  {_render_figure("card-4-cheat-sheet", uris["card-4-cheat-sheet"])}

  <hr style="border:0; border-top:1px solid #e2e8f0; margin:22px 0;" />

  <h2 style="font-family:Arial, Helvetica, sans-serif; font-size:15pt; color:#1e3a8a; margin:22px 0 10px 0;">
    3. Fact-Checked Breakdown of Both Required Features
  </h2>

  <h3 style="font-family:Arial, Helvetica, sans-serif; font-size:12.5pt; color:#0f172a; margin:14px 0 6px 0;">
    A. Daily Free Transfers on Solana
  </h3>
  <ul style="margin:6px 0 14px 20px; padding:0;">
    <li style="margin-bottom:6px;">
      <strong>User Problem Solved:</strong> Users holding SPL stablecoins (such as USDT or USDC) on Solana often encounter transfer friction when their wallet holds 0 SOL or during temporary network congestion spikes.
    </li>
    <li style="margin-bottom:6px;">
      <strong>Applicable Conditions &amp; Limits:</strong>
      <ul style="margin:6px 0 6px 20px; padding:0;">
        <li><strong>Quota:</strong> 3 gas-free transfers per account per day.</li>
        <li><strong>Eligible Assets:</strong> All SPL token transfers on Solana, <strong>excluding native $SOL transfers</strong>.</li>
        <li><strong>Minimum App Versions:</strong> TokenPocket Android <code>v2.9.0+</code> and iOS <code>v2.11.0+</code>.</li>
        <li><strong>Network Context:</strong> Solana natively charges a base transaction fee (50% of transaction fees are burned on-chain) plus account Rent for storage. Outside the 3/day SPL quota&mdash;or when transferring native <code>$SOL</code>&mdash;standard network fees apply.</li>
      </ul>
    </li>
    <li style="margin-bottom:6px;">
      <strong>How to Access &amp; Use:</strong>
      <ol style="margin:6px 0 6px 20px; padding:0;">
        <li>Open TokenPocket and enter your Solana wallet.</li>
        <li>Select the SPL token to send (e.g., USDT) and tap <code>[Send]</code> (bottom-left).</li>
        <li>On the transfer interface, the default network fee payment asset is SOL, and users can also select USDT or USDC &mdash; all display <code>Gas-Free</code> while the daily 3/account quota remains.</li>
        <li>Verify <code>Gas-Free</code> in the transaction details and tap <code>[Confirm]</code>.</li>
      </ol>
    </li>
  </ul>

  <h3 style="font-family:Arial, Helvetica, sans-serif; font-size:12.5pt; color:#0f172a; margin:16px 0 6px 0;">
    B. Pay Network Fees with Tokens on TRON (USDT &amp; USDD) + Additional Cost-Savers
  </h3>
  <ul style="margin:6px 0 14px 20px; padding:0;">
    <li style="margin-bottom:6px;">
      <strong>User Problem Solved:</strong> Transferring TRC20 tokens (like USDT or USDD) requires both <strong>Bandwidth</strong> (transaction data) and <strong>Energy</strong> (smart contract execution). Without enough resources, TRON burns TRX &mdash; stranding users who hold USDT/USDD with 0 TRX.
    </li>
    <li style="margin-bottom:6px;">
      <strong>Practical Option 1 &mdash; Pay TRON Fees Directly with USDT:</strong>
      <ol style="margin:6px 0 6px 20px; padding:0;">
        <li>Open TokenPocket &rarr; TRON wallet &rarr; select <code>USDT</code> &rarr; tap <code>Transfer</code>.</li>
        <li>Enter the recipient TRC20 address and transfer amount (ensure enough USDT to cover both amount and fee; brand-new unactivated TRON addresses follow on-screen activation prompts first).</li>
        <li>Optionally claim an available daily subsidy or enter a redemption code, select <code>USDT</code> as the network fee asset, verify the displayed fee quote, and tap <code>Confirm</code>.</li>
      </ol>
    </li>
    <li style="margin-bottom:6px;">
      <strong>Practical Option 2 &mdash; Pay TRON Fees Directly with USDD (<code>iOS &amp; Android v2.8.0+</code>):</strong>
      <ol style="margin:6px 0 6px 20px; padding:0;">
        <li>Open TokenPocket &rarr; select your token (e.g., <code>USDD</code>) &rarr; tap <code>[Transfer]</code> (bottom-left).</li>
        <li>Tap <code>[Pay With]</code> (default is TRX) and choose <code>USDD</code> (the detail screen shows Bandwidth &amp; Energy rental parameters plus an optional 20 TRX purchase button).</li>
        <li>Verify the network fee displays in <code>USDD</code> and tap <code>[Confirm Payment]</code>.</li>
        <li><em>TRON PSM Tip:</em> Users can swap <code>USDT &lt;-&gt; USDD</code> at a lossless 1:1 ratio via the TRON Peg Stability Module (PSM) inside TokenPocket <code>[Swap]</code>.</li>
      </ol>
    </li>
    <li style="margin-bottom:6px;">
      <strong>Additional TokenPocket TRON Cost-Savers:</strong>
      <ul style="margin:6px 0 6px 20px; padding:0;">
        <li><strong>Energy Rental:</strong> Rent Energy on the transfer screen instead of burning TRX directly (exact savings are dynamic and depend on live TRON resource rates, recipient USDT balance status, and network conditions &mdash; always check the in-wallet quote).</li>
        <li><strong>Daily Subsidies:</strong> TokenPocket currently allocates <strong>3,240 subsidized TRON transfers per day</strong> on a first-come, first-served basis. Eligible users who claim an available subsidy on the transfer page see <code>0</code> network fee.</li>
        <li><strong>Network Fee Redemption Codes / Transfer Fee Coupons:</strong> Earned via official TokenPocket campaigns and redeemed on the transfer page for partial or full fee coverage depending on code terms.</li>
      </ul>
    </li>
  </ul>

  <hr style="border:0; border-top:1px solid #e2e8f0; margin:22px 0;" />

  <h2 style="font-family:Arial, Helvetica, sans-serif; font-size:15pt; color:#1e3a8a; margin:22px 0 10px 0;">
    4. Original Infographics Created for This Submission (Embedded Inline Above)
  </h2>
  <ol style="margin:6px 0 14px 20px; padding:0;">
    <li><code>card-1-hook-overview.png</code> (1600&times;900): Stop Getting Stuck With Zero Gas &mdash; Solana &amp; TRON Overview (Tweet 1/6)</li>
    <li><code>card-2-solana-gasfree.png</code> (1600&times;900): Solana: 3 Gas-Free Token Transfers Every Day &mdash; 3-Step UI + Quota &amp; $SOL Guardrail (Tweet 2/6)</li>
    <li><code>card-3-tron-flexible-fees.png</code> (1600&times;900): TRON Without TRX: Pay in USDT / USDD + Energy Rental, 3,240 Subsidies &amp; Coupons (Tweet 4/6)</li>
    <li><code>card-4-cheat-sheet.png</code> (1600&times;900): Complete Solana vs. TRON Fee-Saving Cheat Sheet (Tweet 6/6)</li>
  </ol>

  <hr style="border:0; border-top:1px solid #e2e8f0; margin:22px 0;" />

  <h2 style="font-family:Arial, Helvetica, sans-serif; font-size:15pt; color:#1e3a8a; margin:22px 0 10px 0;">
    5. Official Reference Sources Used
  </h2>
  <ul style="margin:6px 0 24px 20px; padding:0;">
    <li><strong>Official Video Tutorial:</strong> <a href="https://x.com/TokenPocket_TP/status/2118610097987596552" style="color:#1d4ed8;">https://x.com/TokenPocket_TP/status/2118610097987596552</a></li>
    <li><strong>TokenPocket Website:</strong> <a href="https://tokenpocket.pro" style="color:#1d4ed8;">https://tokenpocket.pro</a></li>
    <li><strong>Solana Gas-Free Service FAQ:</strong> <a href="https://help.tokenpocket.pro/en/wallet-faq-en/solana-wallet/gas-free-service-on-solana" style="color:#1d4ed8;">https://help.tokenpocket.pro/en/wallet-faq-en/solana-wallet/gas-free-service-on-solana</a></li>
    <li><strong>TRON USDT Network Fee FAQ:</strong> <a href="https://help.tokenpocket.pro/en/wallet-faq-en/tron-wallet/usdt-as-network-fee" style="color:#1d4ed8;">https://help.tokenpocket.pro/en/wallet-faq-en/tron-wallet/usdt-as-network-fee</a></li>
    <li><strong>TRON USDD Network Fee FAQ:</strong> <a href="https://help.tokenpocket.pro/en/wallet-faq-en/tron-wallet/usdd-gas" style="color:#1d4ed8;">https://help.tokenpocket.pro/en/wallet-faq-en/tron-wallet/usdd-gas</a></li>
  </ul>

</body>
</html>
"""
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    return OUTPUT_HTML


if __name__ == "__main__":
    out = build_html()
    print(f"Generated {out} ({out.stat().st_size:,} bytes)")
