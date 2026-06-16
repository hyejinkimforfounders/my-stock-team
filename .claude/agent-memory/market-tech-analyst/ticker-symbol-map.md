---
name: ticker-symbol-map
description: Confirmed FinanceDataReader ticker codes for Korean stocks and major indices
metadata:
  type: reference
---

## Korean Stocks (KRX)
| 종목명 | 티커 |
|---|---|
| 삼성전자 | 005930 |

## Indices
| 지수명 | 티커 |
|---|---|
| KOSPI | KS11 |
| KOSDAQ | KQ11 |
| S&P 500 | US500 |

**Notes:**
- KRX tickers are 6-digit zero-padded strings (e.g., '005930')
- `fdr.DataReader('005930', start_date)` returns columns: Open, High, Low, Close, Volume, Change
- Index codes may differ; always verify against FDR docs if a new index is requested
