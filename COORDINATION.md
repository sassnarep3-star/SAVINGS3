# COORDINATION.md — Shared Multi-Session Task Board

Four parallel Arena agent sessions operated on `sassnarep3-star/SAVINGS3` on `2026-10-22` (UTC). Because Arena binds each sandbox strictly to its assigned branch (`arena/<session-id>-savings3`) and prohibits switching or creating additional git branches, each session commits on its assigned Arena branch, syncs with `origin/main` before every push, preserves all prior sessions' work losslessly, and records every claim, conflict resolution, source audit, irregularity, and publication result below.

## Unified Task Board Across Parallel Sessions

| Task ID | Task Description | Status | Owning Session | Branch | File Scope |
|---|---|---|---|---|---|
| `P1-ALL` | Official-source research, dashboard, validation and Pages integration (first pass) | `done` | `arena-d7395cfa` | `arena/d7395cfa-savings3` | `COORDINATION.md`, `README.md`, `site/**`, `scripts/build.py`, `scripts/check.py`, `.github/workflows/**` |
| `P2-FDIC` | FDIC rules + certificate verification | `done` | `arena-71ffb49d` | `arena/71ffb49d-savings3` | `data/fdic.json`, `data/meta.json`, `fdic-insurance.html` |
| `P2-ACCTS` | Rates, minimums, fees, rules (16 accounts) | `done` | `arena-71ffb49d` | `arena/71ffb49d-savings3` | `data/accounts.json`, `accounts.html` |
| `P2-BONUS` | Bonuses and promotions | `done` | `arena-71ffb49d` | `arena/71ffb49d-savings3` | `data/accounts.json`, `bonuses.html` |
| `P2-SEC` | App and security posture | `done` | `arena-71ffb49d` | `arena/71ffb49d-savings3` | `data/security.json`, `security-apps.html` |
| `P2-RET` | Return models $10k–$1.25M × 1/3/5 yrs | `done` | `arena-71ffb49d` | `arena/71ffb49d-savings3` | `scripts/build_site.py`, `returns.html` |
| `P2-FLAG` | Flagged-for-review register | `done` | `arena-71ffb49d` | `arena/71ffb49d-savings3` | `data/flagged.json`, `flagged.html` |
| `P2-SITE` | Site index, navigation, link check, publish & Pass 1–2 reconciliation | `done` | `arena-71ffb49d` | `arena/71ffb49d-savings3` | `index.html`, `assets/**`, `scripts/verify_site.py`, `README.md`, `COORDINATION.md`, `.github/workflows/pages.yml` |
| `P3-DOCS` | Parallel session claim observed on remote branch (`docs/**` scope) | `in progress` | `arena-dbe2ef46` | `arena/dbe2ef46-savings3` | `docs/**`, `COORDINATION.md`, `README.md` |
| `T1` | Official FOMC Sep 2026 policy rate, Fed Commercial Bank asset rankings, & complete FDIC BankFind CERT audit (resolving missing U.S. Bank CERT `#6548`, Amex CERT `#27471`, Morgan Stanley Private Bank CERT `#34221`, First-Citizens CERT `#11063`, BMO CERT `#16571`, Barclays CERT `#57203`) | `done` | `arena-36a5cee6` | `arena/36a5cee6-savings3` | `research/macro-and-fdic-audit.md` |
| `T2` | Primary-source verification of high-yield & branch national banks missing from Passes 1–2 (E*TRADE / Morgan Stanley Private Bank `3.75%` base / `4.25%` 6m boost + `SAVE800` `$400`/`$800`, CIT Bank / First-Citizens `3.75%` / `4.25%` `BOOST50` & `3.65%` Savings Connect, Barclays `3.65%` Tiered + `10/31/2026` `$200` bonus, BMO Alto `3.00%` & Savings Builder `$60` reward, U.S. Bank Elite MM `3.40%`, Citizens Access token audit) + full SoFi `10/20/2026` PDF & bank security centers | `done` | `arena-36a5cee6` | `arena/36a5cee6-savings3` | `research/national-banks-deep-audit.md` |
| `T3` | Return-by-investment-size & max-FDIC (`$250k` single principal vs `P_max` principal+accrued-interest ceiling, `$500k` joint/sweep, `$1M–$1.25M` POD/multi-bank) modeling anchored on current opening date `2026-10-22` across 6m, 1y, 2y, 3y, 5y | `done` | `arena-36a5cee6` | `arena/36a5cee6-savings3` | `research/return-and-lifespan-modeling.md` |
| `T4` | Final Integration Pass (`arena-36a5cee6`): Re-verify all rows across passes line by line, integrate expanded datasets + interactive calculator/filters + static tables, validate `build.py` + `check.py` + `build_site.py` + `verify_site.py`, merge PR to `main`, confirm live GitHub Pages deploy | `in progress` | `arena-36a5cee6` | `arena/36a5cee6-savings3` | `data/*.json`, `assets/**`, `scripts/build_site.py`, `scripts/verify_site.py`, `*.html`, `README.md`, `COORDINATION.md` |

---

## Cross-Session Change Requests & Merge Conflict Log

| When (UTC) | Session | Event & Lossless Resolution |
|---|---|---|
| `2026-10-22` | `arena-71ffb49d` | Started from commit `66f2767` (initial `README.md`). Merged `arena-d7395cfa` PRs #1 (`e9e1e6c`) and #2 (`bcb43a1`) preserving `site/**`, `scripts/build.py`, and `scripts/check.py` untouched while publishing full root dashboard at `/` via PR #3 (`46808f3`) and PR #4 (`4c96a94`). |
| `2026-10-22` | `arena-36a5cee6` | Initialized claim in `13aa063`, then merged `origin/main` (`4c96a94`). Encountered expected `CONFLICT (add/add)` on `COORDINATION.md` only (zero code/data file conflicts because `arena-36a5cee6` isolated research notes in `research/**`). Resolved `COORDINATION.md` losslessly by keeping every single table row, reconciliation note, verification log, and publication record from `arena-d7395cfa` and `arena-71ffb49d` verbatim below, while adding `arena-dbe2ef46` (`docs/**`) and `arena-36a5cee6` (`research/**` + final integration `T4`). Logged file change notice for `T4` shared integration files once `T1–T3` finish. |

---

## Preserved Record — First & Second Passes (`arena-d7395cfa` & `arena-71ffb49d`)

### How the first two passes were reconciled (no work discarded)

* The first pass (`arena-d7395cfa`) is merged and published under `site/`; it is **kept unchanged and still live** at `/SAVINGS3/site/`.
* The second pass (`arena-71ffb49d`) publishes the full research at the repository root, which is where legacy GitHub Pages already serves `main`. Its `index.html` replaces the first pass's root redirect; the first pass's dashboard remains reachable at `site/`.
* Both passes agree on every overlapping value: Marcus 3.50%, Capital One 3.20%, Amex 3.20%, Ally 3.10%, Synchrony unranked/flagged, Chase/Citi/Discover APY unverified. No value was changed to force agreement.
* Facts found only by the first pass were re-opened and verified by the second session before being adopted: the Bank of America Personal Schedule of Fees ($100 / $8 / six-month waiver, effective 2026-08-07), the Amex APY accuracy date (10/21/2026), and the Amex / Ally / Marcus / Capital One security statements (MFA, encryption, auto-logout, security guarantee).
* A discrepancy found while reconciling was logged as F19: Capital One's product page and its Discover FAQ give different dates for joint Capital One/Discover FDIC coverage.

### Session Log (`arena-d7395cfa`)
- 2026-10-22: Repository reviewed: README.md only, no other claims or source data. Claimed integration and all implementation files. Will publish unresolved rate/date/eligibility issues on Flagged for Review; no unconfirmed rates will be filled in.
- Claim publication fallback scope: root index.html and .nojekyll. GitHub Pages already serves main at repository root (legacy mode). API attempt to change Pages to workflow mode returned 403 Resource not accessible by integration. Preserve existing working Pages configuration and publish via main/root with a local redirect into site/. Validation workflow will not attempt an unauthorized Pages settings change.
- Research and integration completed: official source URLs and precise observed fields are recorded in site/evidence.json and on site/sources.html. Verified base APYs: Marcus 3.50%, Capital One comparison page 3.20%, Amex 3.20%, Ally 3.10%; disclosures generally dated October 21, 2026. Public pages checked October 22.
- Irregularities published in site/review.html: Synchrony conflicting headline/calculator, Capital One NaN extraction, unverified branch-bank/local rates and Citi geography, partial promotion terms, incomplete secondary eligibility/security evidence, Discover combined insurance, snapshot freshness and non-exhaustive scope. No unconfirmed numeric rate substituted.
- Validation: python scripts/build.py and python scripts/check.py pass; seven pages, internal file and fragment links, official citations per data row, annual return and FDIC ceiling arithmetic.
- PR https://github.com/sassnarep3-star/SAVINGS3/pull/1 merged successfully on 2026-10-22 at 00:07:17 UTC; merge commit e9e1e6cee0e40f783b4d5a1cd1f84709cf629740. PR #2 merged at commit bcb43a1d238a7c7cc2f3f392edd7453ac2292dfa.
- GitHub Pages build and deployment succeeded: https://github.com/sassnarep3-star/SAVINGS3/actions/runs/39697738661 (Live URL: https://sassnarep3-star.github.io/SAVINGS3/).

### Verification Log (`arena-71ffb49d`)
* `python3 scripts/verify_site.py` exits 0: 10 generated pages, 66 unique external links, every internal link and anchor resolves, every external URL traces back to a URL stored in `/data`, every account row carries an https source, arithmetic spot checks pass, every flagged item has a source.
* FDIC certificate numbers confirmed through the FDIC institution API for 15 institutions. Discover Bank (5649) returns ACTIVE = 0 and is excluded from the returns tables.
* PR #3 (https://github.com/sassnarep3-star/SAVINGS3/pull/3) merged on 2026-10-22 at 00:12:36 UTC (`46808f35`), Pages `status: built` at 00:12:54 UTC; PR #4 merged at `4c96a94`.
