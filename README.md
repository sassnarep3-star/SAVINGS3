# SAVINGS3 — Savings Account Research

A verified, source-linked study of FDIC-insured savings accounts at large national banks, published as a
static dashboard on GitHub Pages.

**Live site:** https://sassnarep3-star.github.io/SAVINGS3/
**Earlier snapshot from a parallel session:** https://sassnarep3-star.github.io/SAVINGS3/site/

This repository was built by two independent sessions. The root dashboard is the full research pass
(16 accounts, per-row sources, returns to $1.25M, FDIC coverage structures, 19 flagged items). The `site/`
directory holds the earlier, shorter snapshot, preserved unchanged — see
[COORDINATION.md](COORDINATION.md) for how the two were reconciled.

---

## The short answer

| | |
|---|---|
| Best verified APY, all balances | **3.55%** — Synchrony Bank High Yield Savings |
| Best verified APY at a brand-name online bank | **3.50%** — Marcus by Goldman Sachs (as of 2026-10-21) |
| Best verified promotional rate at a branch network | **3.25%** — Wells Fargo Platinum Savings, new customers, $25,000+ |
| FDIC national savings rate (benchmark) | **0.38%** (effective 2026-10-19) |
| Interest on $250,000 for one year | **$8,875** at 3.55% vs **$950** at the national rate |
| Fully insured at one bank | **$1,250,000** (1 owner × 5 POD beneficiaries × $250,000) |
| Interest on $1,250,000 for one year | **$44,375** at 3.55%, fully insured |

On a $1.25M fully insured balance the difference between the best verified online rate and Bank of
America's 0.04% is about **$43,875 a year**.

## What is in this repo

```
index.html                    Dashboard: headline numbers, top rates, the $1.25M structures
accounts.html                 All 16 accounts: APY, as-of date, minimums, fees, waiver rules, sources
returns.html                  Growth tables for $10k → $1.25M at 1, 3 and 5 years + best per deposit size
fdic-insurance.html           How coverage works; per-bank certificate numbers and coverage capacity
bonuses.html                  Every promotion found, its qualifying rules, and what it is worth
rates-competitiveness.html    Each APY vs the FDIC national rate, priced over 1/3/5 years
security-apps.html            App and security statements, transcribed; unverified controls left blank
flagged.html                  Every blank value, contradiction and rejected number, with sources
methodology.html              Dates, inclusion rules, exact arithmetic, limits
sources.html                  All official sources, grouped by publisher
data/*.json                   The single source of truth: every fact with its source URL
scripts/build_site.py         Regenerates all pages from data/
scripts/verify_site.py        Fails the build on broken links, missing sources, or bad arithmetic
site/                         Earlier snapshot from a parallel session (kept as published)
scripts/build.py, check.py    That snapshot's generator and validator
.github/workflows/pages.yml   CI validation on push / PR to main
```

The root HTML is generated, not hand-edited. Change a number in `data/`, rebuild, and every page follows.

```bash
python3 scripts/build_site.py    # regenerate the dashboard
python3 scripts/verify_site.py   # gate: links, sources, arithmetic
python3 scripts/build.py         # regenerate the earlier snapshot in site/
python3 scripts/check.py         # that snapshot's own validator
```

## Method

* **Capture date:** 2026-10-22 (UTC). **Assumed opening date:** 2026-10-23.
* **Scope:** the large national branch networks (Chase, Bank of America, Wells Fargo, Citibank,
  U.S. Bank, PNC, Truist, TD, Fifth Third, Citizens) plus national digital banks that are themselves
  FDIC-insured (Capital One, Ally, American Express, Marcus/Goldman Sachs, Synchrony, SoFi, Schwab).
  Small local banks and credit unions are out of scope by request.
* **FDIC identity is checked, not assumed.** Certificate numbers come from the FDIC's own institution
  API, not from bank marketing. One brand in scope (Discover) is recorded by the FDIC as inactive and
  is excluded from the returns tables rather than counted as a separate $250,000 stack.
* **No aggregators.** NerdWallet, Bankrate, Forbes, depositaccounts and similar were not used as the
  source for any value, even where they agree.
* **Blank beats wrong.** Chase, Citi and TD will not render a savings APY without a ZIP code or
  client-side script. Their APY cells are blank, their rows are kept for fees and rules, and each gap
  is published on the Flagged for Review page with a link.
* **Arithmetic is stated.** Balance = deposit × (1 + APY)^years; interest = balance − deposit. An APY
  already reflects compounding, so this reproduces a bank's own annual disclosure at a constant rate.
  Every account is variable-rate except the CDs shown for context, so 3- and 5-year columns are
  models, not forecasts.

## Flagged for review

The headline irregularities, all published on `flagged.html` with sources:

1. **Synchrony** prints both 3.55% and 2.85% APY on the same page (headline vs its own calculator).
2. **Chase, Citi, TD** savings APYs could not be verified — gated by ZIP code or JavaScript.
3. **Bank of America** rendered its fee as the literal placeholder `$XXXX`; the real values ($100 to
   open, $8 monthly, six-month waiver) were taken from its Personal Schedule of Fees, effective
   2026-08-07.
4. **Capital One** rendered its savings APY as `NaN APY`; the rate was taken from Capital One's own
   comparison and application pages instead.
5. **American Express** and **U.S. Bank** FDIC certificate numbers were not retrieved from the FDIC API.
6. **Discover Bank** shows `ACTIVE = 0`. Capital One says Discover merged on 2025-05-18 and joint
   FDIC insurance began 2025-11-18 — but its own product page says "on or after May 18, 2025", so the
   two Capital One pages disagree. Both readings are recorded.
7. **Wells Fargo** and **U.S. Bank** rate pages defaulted to non-New-York ZIP codes; Wells Fargo prints
   no effective date.
8. **SoFi's "$3M FDIC"** is a sweep-network program, not a single-bank limit.

## Third pass highlights (`docs/`, verified 2026-10-22)

* League table of every verified APY across 13 FDIC charters, with CONDITIONAL labels where a headline
  rate needs a balance, linked product, new-customer status, or eligible ZIP (U.S. Bank Smartly 3.50%,
  U.S. Bank Elite 3.40%, Wells Platinum 3.25%, PNC HY 3.15%).
* Returns by deposit size ($10k/$50k/$100k/$250k) at 6 months–5 years from 2026-10-22, an interactive
  calculator, and the FDIC-safe maximum deposit table (e.g., $241,545.89 for 1 year at 3.50% — depositing
  the full $250,000 lets interest overflow single-category coverage).
* CD rates by term with maturity payouts and early-withdrawal penalties; fee break-even math showing when
  branch-account fees erase 0.01% interest; bonus simple-% comparisons with deadlines.
* Unverified values (Citi standard APY, TD Signature tiers, Citizens Access APY, PNC Standard/Premiere)
  left blank and published on `docs/flagged.html` with manual-verification steps.

## Licence / disclaimer

Research notes, not financial advice. Rates change without notice; re-verify before opening an
account. All trademarks belong to their owners. Government sources are public domain; each bank's
page is linked, not reproduced.
