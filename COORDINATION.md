# COORDINATION.md — Shared Task Board

**Repository:** sassnarep3-star/SAVINGS3
**Purpose:** Multi-session coordination for the Savings Account research + GitHub Pages site.
**Last updated:** 2026-10-22 (UTC)

## Rules (as given by the repo owner)

1. Read this file before starting any task.
2. Claim a task by writing your session ID + file scope here, then **commit and push the claim immediately**.
3. Never start a task another session has claimed.
4. Keep scopes non-overlapping. Sessions work on their own branch/worktree named `session-<id>/<task>`.
   (This session is pinned by the tooling to `arena/71ffb49d-savings3`.)
5. If a task needs a change to a file owned by another session, log the request here — do not edit the file.
6. Small, frequent commits. `git pull --rebase` before every push.
7. On merge conflict: stop, resolve without discarding the other session's work, log what happened.
8. On completion: record sources, verification performed, irregularities; mark the task `done`.
9. Never mark anything verified without an official source link.
10. Shared outputs (table data, site index/nav) are changed only by the final integration session.
11. A claim >60 minutes old with no commits may be taken over; note the handoff.

## Status legend

| Status | Meaning |
|---|---|
| `unclaimed` | Available for any session to claim |
| `in progress` | Claimed; owner + file scope recorded |
| `needs review` | Published on the site's **Flagged for Review** page; does not block other work |
| `done` | Complete, verified against official sources, sources logged |

## Task board

| # | Task | Status | Session ID | File scope | Notes |
|---|---|---|---|---|---|
| T1 | Repo scaffold, build script, site CSS/JS shell | in progress | `arena-71ffb49d` | `/COORDINATION.md`, `/README.md`, `/scripts/`, `/assets/`, `/data/`, `/.nojekyll` | Claimed 2026-10-22 |
| T2 | Research: FDIC insurance rules + per-bank FDIC certificate verification | in progress | `arena-71ffb49d` | `/data/fdic.json`, `/pages/fdic.html` | FDIC.gov + api.fdic.gov only |
| T3 | Research: national-bank savings rates, minimums, fees, rules | in progress | `arena-71ffb49d` | `/data/accounts.json`, `/pages/accounts.html` | Bank official pages only |
| T4 | Research: sign-up bonuses / promotions + qualifying rules | in progress | `arena-71ffb49d` | `/data/bonuses.json`, `/pages/bonuses.html` | Bank official pages only |
| T5 | Research: digital app + security posture | in progress | `arena-71ffb49d` | `/data/security.json`, `/pages/security.html` | Bank official pages only |
| T6 | Return-on-deposit models ($10k–$1.25M), compounding math | in progress | `arena-71ffb49d` | `/scripts/build_site.py`, `/pages/returns.html` | Derived from T3 APYs; formula documented |
| T7 | Flagged-for-review page: unverified values, irregularities, conflicts | in progress | `arena-71ffb49d` | `/pages/flagged.html` | Never blocks merge |
| T8 | Site index + navigation + link check + GitHub Pages publish | in progress | `arena-71ffb49d` | `/index.html`, `/pages/*.html`, repo settings | Final integration |
| T9 | PR to `main` + merge + confirm Pages deploy + record result | in progress | `arena-71ffb49d` | `/COORDINATION.md` | Final integration |

> All rows above were claimed by a single session (`arena-71ffb49d`) because no other session had
> written a claim at the time of the first commit. Any later session must claim from `unclaimed`
> rows only; if none exist, add new rows rather than editing these.

## Handoff / conflict log

| When (UTC) | Session | Event |
|---|---|---|
| 2026-10-22 | `arena-71ffb49d` | Repo found empty (single 10-byte README). Created this board. No prior claims, no conflicts. |

## Verification policy used in this repo

* Every table row that states a number must carry a link to the **official** page (bank, FDIC,
  or other primary source) on which the number appears.
* If a number cannot be confirmed on an official page, it is left **blank** and listed on
  `pages/flagged.html` as `unverified`. Values are never inferred, estimated, or carried over
  from third-party rate aggregators.
* Every rate row records the **rate effective date printed by the source**, plus the
  capture timestamp.
* Return projections are clearly labelled as arithmetic models of the quoted APY, not promises.

## Completion log

_(filled in as tasks finish — see bottom of file)_

---

## Completion log

### T1 — Scaffold, build script, site shell — `done`
* Session `arena-71ffb49d`, 2026-10-22.
* Files: `README.md`, `.nojekyll`, `assets/style.css`, `scripts/build_site.py`, `scripts/verify_site.py`.
* Verification: `python3 scripts/build_site.py` regenerates all 10 pages from `data/*.json`; `python3 scripts/verify_site.py`
  exits 0 (10 pages, 61 unique external links, all internal links and anchors resolve, all external links trace back to
  a URL stored in `/data`, arithmetic spot checks pass, every account row carries an https source).

### T2 — FDIC insurance rules + certificate verification — `done`
* Sources: FDIC deposit-insurance overview, FAQ, "Are My Deposit Accounts Insured", National Rates and Rate Caps
  (October 2026, revised 2026-10-19), When a Bank Fails, and the FDIC institution API (`api.fdic.gov/banks/institutions`).
* Verified: $250,000 per depositor / per bank / per ownership category; joint = $250,000 per co-owner; trust formula
  owners × beneficiaries × $250,000 capped at $1,250,000 per owner; branches of one bank are not separately insured;
  national savings rate 0.38%.
* Certificate numbers confirmed via the FDIC API for 15 institutions (Chase 628, BofA 3510, Wells Fargo 3511,
  Citibank 7213, PNC 6384, Truist 9846, TD 18409, Fifth Third 6672, Citizens 57957, Capital One 4297, Ally 57803,
  Goldman Sachs Bank USA 33124, Synchrony 27314, SoFi 26881, Schwab 57450). **Discover Bank (5649) returns ACTIVE = 0.**
* Irregularities: Amex and U.S. Bank certificate numbers not retrieved (F06, F07); Discover inactive (F08).

### T3 — Savings rates, minimums, fees, rules — `done`
* 16 accounts across 16 banks. 12 have a rate printed on the bank's own page; 4 are blank and flagged
  (Chase F02, Citi F03, TD F04 ×2 rows).
* Highest verified: Synchrony 3.55%. Lowest verified standard branch rate: Bank of America / Truist / Wells Fargo 0.01%.
* Irregularities: Synchrony prints two different APYs (F01); BofA fee rendered as `$XXXX` (F05); Capital One rendered
  `NaN APY` (F11); Amex and Schwab print no APY effective date (F12); Wells Fargo and U.S. Bank rate pages defaulted to
  non-New-York ZIP codes (F09, F10).

### T4 — Bonuses and promotions — `done`
* Verified: Chase $100/$200 (expires 2027-01-27, 30-day deposit, 90-day hold); SoFi +1.10% APY for 6 months and
  $50/$400 cash bonus; Marcus +1.00% for 3 months (up to 5 referrals); Wells Fargo 3.25% new-customer tier at $25,000+.
* No promotion found on the official pages captured for BofA, Citi, U.S. Bank, Truist, TD, Schwab, Ally, Amex, Capital One.
* Irregularity: SoFi bonus tier thresholds not fully extracted (F14).

### T5 — App and security posture — `done`
* 14 banks tabulated; app claims are recorded only where the bank's own page describes an app. 2FA / passkey support
  is **not** verified for any bank and is left blank on purpose.
* Irregularity: Truist app/security claims not on the captured page (F17).

### T6 — Return models — `done`
* Deposits $10,000 → $1,250,000; horizons 1, 3, 5 years; formula `deposit × (1 + APY)^years`, tiered APYs selected by
  balance. Assumed opening date 2026-10-23 (capture 2026-10-22).
* Headline: $250,000 at 3.55% = $8,875/yr vs $950 at the FDIC national rate; $1,250,000 fully insured at one bank via
  5 POD beneficiaries = $44,375 in year 1.
* Every returns row and every best-per-deposit row carries a rate-source link; the $1.25M structure rows carry both the
  rate source and the FDIC rule link.

### T7 — Flagged for review — `done`
* 18 items (4 high, 6 medium, 8 low) published at `flagged.html`, each with the value used, the value rejected, the
  action to take and an official source link.

### T8 — Index, navigation, link check, publish — `done`
* `verify_site.py` gate passes: internal links, anchors, external-link provenance, arithmetic, nav/footer presence.
