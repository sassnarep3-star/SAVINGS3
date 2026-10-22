# SAVINGS3 — Savings Account Comparison (Big National Banks)

A line-by-line verified comparison of savings accounts at big national U.S. banks — high-yield savings, traditional savings, money market accounts and CDs — with returns by deposit size up to the $250,000 FDIC limit, bonus math, opening rules, and a public list of everything that could **not** be verified.

**Live site (GitHub Pages):** https://sassnarep3-star.github.io/SAVINGS3/

**Verified:** October 22, 2026 · **Account-open date for projections:** October 22, 2026

## Headline findings (Oct 22, 2026)

| Finding | Value |
|---|---|
| Best verified unconditional HYSA | Marcus Online Savings (Goldman Sachs Bank USA) — **3.50% APY** |
| Best verified CDs | **4.40% APY** — Marcus (12 mo–6 yr), Ally 18-mo, Capital One 11-mo special, Amex 10/22-mo |
| FDIC national average (savings / MMA / 12-mo CD) | 0.38% / 0.63% / 1.76% APY (Oct 19, 2026) |
| Interest on $250,000, 1 year | $8,750 at 3.50% vs. $950 at the national average vs. $25 at 0.01% |
| FDIC-safe deposit for 1 year at 3.50% | $241,545.89 (depositing the full $250,000 lets interest overflow coverage) |

## Site structure (`docs/`)

| Page | Contents |
|---|---|
| `index.html` | Dashboard: bottom line, league table of every verified APY, traps, category links |
| `high-yield-savings.html` | HYSAs: APYs, conditions, minimums, fees, withdrawal limits |
| `traditional-savings.html` | Branch savings + fee break-even math |
| `money-market.html` | Money market deposit accounts |
| `cds.html` | CD rates by term, maturity payouts, early-withdrawal penalties |
| `returns.html` | Interest at $10k/$50k/$100k/$250k × 6 mo–5 yr, FDIC-safe deposit planner, calculator |
| `bonuses.html` | Bonuses/promotions with deadlines and simple-% math |
| `opening-and-security.html` | Eligibility, documents, app access, how to verify FDIC membership in BankFind/EDIE |
| `methodology.html` | Scope (13 FDIC charters), verification protocol, ranking rules, formulas |
| `flagged.html` | ⚠ Flagged for Review: every unverified value and irregularity (F-01–F-20) |

## Verification rules

- **Official sources only** — each bank's own domain (incl. official rate-sheet PDFs), FDIC.gov, FederalReserve.gov. Every table row carries its source link and the source's own as-of date.
- **Blank beats guessed** — values that could not be confirmed on an official page are left blank, excluded from rankings/ROI, and listed on the Flagged for Review page (e.g., Citi standard APY, TD Signature tiers, Citizens Access APY, PNC Standard Savings).
- Full audit trail: [`docs/research-notes.md`](docs/research-notes.md). Multi-session task coordination: [`COORDINATION.md`](COORDINATION.md).

## Math

`FV = P × (1 + APY)^t` — deposits $10k/$50k/$100k/$250k; horizons 6 mo/1/2/3/5 yr from Oct 22, 2026. Variable-APY figures are hypothetical illustrations (APY assumed constant, before fees/taxes); only CD APYs are fixed to maturity. FDIC-safe maximum deposit: `Pmax = $250,000 ÷ (1 + APY)^t` (the limit covers principal + interest, combined per ownership category at one bank).

## Scope

13 FDIC charters from the [Federal Reserve's U.S. Domestically Chartered Commercial Banks ranking](https://www.federalreserve.gov/releases/lbr/current/) (June 30, 2026): JPMorgan Chase, Bank of America, Citibank, Wells Fargo, Goldman Sachs (Marcus), U.S. Bank, Capital One (incl. Discover — merged May 18, 2025, one FDIC limit), PNC, Truist, TD, Citizens (incl. Citizens Access), American Express, Ally. Custody/wealth-only banks and the next tier of regionals are listed as out-of-scope/deferred on the Flagged and Methodology pages. This is not a list of every U.S. bank.

## Developing

Pure static HTML/CSS/JS in `docs/` — no build step. Preview locally:

```sh
python3 -m http.server 8000 --directory docs
# open http://localhost:8000/
```

Deployed to GitHub Pages by [`.github/workflows/pages.yml`](.github/workflows/pages.yml) on push to `main`.

## Disclaimer

Research snapshot as of October 22, 2026, for manual review. Not financial advice; not affiliated with any bank. Rates change frequently and can vary by ZIP — always confirm on the official page before opening. Bank and product names are trademarks of their respective owners.
