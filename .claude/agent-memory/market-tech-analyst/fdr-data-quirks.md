---
name: fdr-data-quirks
description: FinanceDataReader column names, KRX data behaviors, and analysis conventions confirmed in this project
metadata:
  type: reference
---

## Column Names (KRX stocks)
`fdr.DataReader('005930', start_date)` returns a DataFrame with these columns:
- Open, High, Low, Close, Volume, Change
- Index is `Date` (datetime)

## Data Coverage
- Requesting ~380 days back yields ~253 trading days — sufficient for a full 52-week window
- Requesting ~190 days back yields ~126 trading days — use for 6-month analysis
- For 52-week metrics, always fetch at least 380 calendar days back to cover ~252 trading days

## 삼성전자 (005930) — Historical Reference (as of 2026-06-16)
- 52주 고가: 360,500원 (2026-06-02)
- 52주 저가: 56,800원 (2025-06-02) — reflects major drawdown in mid-2025
- Latest close (2026-06-16): 343,000원
- The stock recovered dramatically (+503% from 52w low) over the 1-year window

## Chart Conventions Used
- Chart saved to: `assets/charts/{ticker}.png`
- Matplotlib Agg backend (headless); English-only labels to avoid font issues
- Figure size: 12x5 inches, dpi=150

## Output Format Preferences (from user request 2026-06-16)
- PPTX-ready markdown output
- Key figures in **bold** in the markdown table
- Volume expressed as ratio vs 60-day average (e.g., 0.57x)
- Separate 출처 line below the table: `(출처: FinanceDataReader, 기준일: YYYY-MM-DD)`
- Trend comments: 2-3 bullet points, factual only, no buy/sell/hold verdicts
