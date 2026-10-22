# SAVINGS3 — Savings Account Research

A verified, source-linked study of the best FDIC-insured savings account for a large balance at a
large national bank, published as a static dashboard on GitHub Pages.

**Live site:** https://sassnarep3-star.github.io/SAVINGS3/

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

On a $1.25M fully insured balance the difference between the best verified online rate and
Bank of America's 0.04% is about **$43,875 a year**.

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
```

Nothing is hand-edited in the HTML. Change a number in `data/`, rebuild, and every page follows.

```bash
python3 scripts/build_site.py   # regenerate
python3 scripts/verify_site.py  # gate: links, sources, arithmetic
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
* **Arithmetic is stated.** Balance = deposit × (1 + APY)^years; interest = balance − deposit. APY
  already includes compounding, so this reproduces a bank's own annual disclosure at a constant rate.
  Every account is variable-rate except the CDs shown for context, so 3- and 5-year columns are
  models, not forecasts.

## Flagged for review

The headline irregularities, all published on `flagged.html` with sources:

1. **Synchrony** prints both 3.55% and 2.85% APY on the same page (headline vs its own calculator).
2. **Chase, Citi, TD** savings APYs could not be verified — gated by ZIP code or JavaScript.
3. **Bank of America** rendered its fee as the literal placeholder `$XXXX`.
4. **Capital One** rendered its savings APY as `NaN APY`; the rate was taken from Capital One's own
   comparison and application pages instead.
5. **American Express** and **U.S. Bank** FDIC certificate numbers were not retrieved from the FDIC API.
6. **Discover Bank** shows `ACTIVE = 0`; Capital One counts Discover deposits with its own from
   2025-05-18 onward, so the two brands are one $250,000 limit.
7. **Wells Fargo** and **U.S. Bank** rate pages defaulted to non-New-York ZIP codes and print no
   effective date (Wells Fargo only).

## Licence / disclaimer

Research notes, not financial advice. Rates change without notice; re-verify before opening an
account. All trademarks belong to their owners. Government sources are public domain; each bank's
page is linked, not reproduced.
