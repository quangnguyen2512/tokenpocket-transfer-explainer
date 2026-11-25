# TokenPocket Transfer Features — Multi-Format Content & Interactive Explainer Studio

Complete, fact-checked Track A submission kit for Superteam Earn bounty **Create & Earn: Explore TokenPocket's Transfer Features** (`superteam_2fe06f76c811`, **$500 USDC** across 10 winners, deadline `2026-12-07T02:30:59Z`).

## What's Inside

```text
superteam_2fe06f76c811_tokenpocket/
├── README.md                          # Quickstart & architecture overview
├── X_THREAD_READY.md                  # 6-tweet EN thread (<=275 chars each), 45s video script, VI thread + EN translation
├── GOOGLE_DOC_SUBMISSION.md           # Copy-paste-ready Google Doc pack matching Superteam Earn rules
├── explainer/
│   └── index.html                     # Self-contained 16:9 interactive + 45s auto-play animated walkthrough
├── assets/
│   ├── card-1-hook-overview.svg       # 1600x900 dark-fintech infographic source (Slide 1/4)
│   ├── card-2-solana-gasfree.svg      # 1600x900 dark-fintech infographic source (Slide 2/4)
│   ├── card-3-tron-flexible-fees.svg  # 1600x900 dark-fintech infographic source (Slide 3/4)
│   ├── card-4-cheat-sheet.svg         # 1600x900 dark-fintech infographic source (Slide 4/4)
│   └── png/
│       ├── card-1-hook-overview.png   # Rendered 1600x900 PNG ready to attach to Tweet 1
│       ├── card-2-solana-gasfree.png  # Rendered 1600x900 PNG ready to attach to Tweet 2
│       ├── card-3-tron-flexible-fees.png # Rendered 1600x900 PNG ready to attach to Tweet 4
│       └── card-4-cheat-sheet.png     # Rendered 1600x900 PNG ready to attach to Tweet 6
├── scripts/
│   ├── render_cards.py                # Headless Chrome/Edge renderer -> 1600x900 verified PNGs
│   └── build_google_doc_html.py       # Embeds all 4 1600x900 PNGs as base64 into 1-file Google Docs HTML
└── tests/
    └── test_content_compliance.py     # Automated pytest fact-check, character-limit & asset verification suite
```

## 5-Minute Launch Guide (Human-in-the-Loop)

1. **Follow `@TokenPocket_TP` on X** from your real account (mandatory campaign rule).
2. **Post the 6-Tweet X Thread** from `X_THREAD_READY.md`:
   - Attach `assets/png/card-1-hook-overview.png` to Tweet 1
   - Attach `assets/png/card-2-solana-gasfree.png` to Tweet 2
   - Attach `assets/png/card-3-tron-flexible-fees.png` to Tweet 4
   - Attach `assets/png/card-4-cheat-sheet.png` to Tweet 6
   - *(Optional Boost for Views/Engagement 50% weight)*: Open `explainer/index.html` in Chrome, click **Clean 16:9 Record Mode**, press **Auto-Play 45s Video**, record the 45-second walkthrough with OBS or Windows Game Bar (`Win + Alt + R`), and attach the MP4 to Tweet 1 or quote-post your thread!
3. **Create the Public Google Doc:**
   - Copy `GOOGLE_DOC_SUBMISSION.md` into a new Google Doc.
   - Replace `[PASTE PUBLISHED X LINK HERE]` with your live X thread URL.
   - Set sharing to **Anyone with the link → Viewer** (verify in an incognito tab).
4. **Submit on Superteam Earn:**
   - Open https://earn.superteam.fun/listings/bounty/create-and-earn-explore-tokenpockets-transfer-features
   - Submit the Google Doc link before `2026-12-07T02:30:59Z`.

## Local Re-Rendering & Compliance Verification

```powershell
# Re-render all 4 SVG infographic cards to verified 1600x900 PNGs
& "c:\Users\nqqua\OneDrive\Desktop\money\.venv\Scripts\python.exe" scripts/render_cards.py

# Build 1-file Google Docs import-ready HTML (with all 4 1600x900 PNGs embedded as base64)
& "c:\Users\nqqua\OneDrive\Desktop\money\.venv\Scripts\python.exe" scripts/build_google_doc_html.py

# Run full automated compliance, character-count & PNG integrity suite
& "c:\Users\nqqua\OneDrive\Desktop\money\.venv\Scripts\python.exe" -m pytest -v tests/test_content_compliance.py
```

## Official Fact-Checked Sources
- **Official Video Tutorial:** https://x.com/TokenPocket_TP/status/2118610097987596552
- **Official Website:** https://tokenpocket.pro
- **Solana Gas-Free FAQ:** https://help.tokenpocket.pro/en/wallet-faq-en/solana-wallet/gas-free-service-on-solana
- **TRON USDT Network Fee FAQ:** https://help.tokenpocket.pro/en/wallet-faq-en/tron-wallet/usdt-as-network-fee
- **TRON USDD Network Fee FAQ:** https://help.tokenpocket.pro/en/wallet-faq-en/tron-wallet/usdd-gas
