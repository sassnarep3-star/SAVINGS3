# Coordination board

Two sessions worked in this repository on 2026-10-22. Branches are fixed by the tooling per session, so
each session used its own Arena branch rather than `session-<id>/<task>`.

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, dashboard, validation and Pages integration (first pass) | done | arena-d7395cfa | COORDINATION.md, README.md, site/**, scripts/build.py, scripts/check.py, .github/workflows/** |
| FDIC rules + certificate verification | done | arena-71ffb49d | data/fdic.json, data/meta.json, fdic-insurance.html |
| Rates, minimums, fees, rules (16 accounts) | done | arena-71ffb49d | data/accounts.json, accounts.html |
| Bonuses and promotions | done | arena-71ffb49d | data/bonuses.json (in accounts.json), bonuses.html |
| App and security posture | done | arena-71ffb49d | data/security.json, security-apps.html |
| Return models $10k–$1.25M × 1/3/5 yrs | done | arena-71ffb49d | scripts/build_site.py, returns.html |
| Flagged-for-review register | done | arena-71ffb49d | data/flagged.json, flagged.html |
| Site index, navigation, link check, publish | done | arena-71ffb49d | index.html, assets/**, scripts/verify_site.py |
| Reconciliation of the two research passes | done | arena-71ffb49d | README.md, COORDINATION.md, .github/workflows/pages.yml |

## How the two passes were reconciled (no work discarded)

* The first pass (`arena-d7395cfa`) is merged and published under `site/`; it is **kept unchanged and still live**
  at `/SAVINGS3/site/`.
* The second pass (`arena-71ffb49d`) publishes the full research at the repository root, which is where legacy
  GitHub Pages already serves `main`. Its `index.html` replaces the first pass's root redirect; the first pass's
  dashboard remains reachable at `site/`.
* Both passes agree on every overlapping value: Marcus 3.50%, Capital One 3.20%, Amex 3.20%, Ally 3.10%,
  Synchrony unranked/flagged, Chase/Citi/Discover APY unverified. No value was changed to force agreement.
* Facts found only by the first pass were re-opened and verified by the second session before being adopted:
  the Bank of America Personal Schedule of Fees ($100 / $8 / six-month waiver, effective 2026-08-07), the Amex
  APY accuracy date (10/21/2026), and the Amex / Ally / Marcus / Capital One security statements (MFA, encryption,
  auto-logout, security guarantee).
* A new discrepancy found while reconciling is logged as F19: Capital One's product page and its Discover FAQ give
  different dates for joint Capital One/Discover FDIC coverage.
Session: arena-d7395cfa (integration). All work uses the Arena-required branch `arena/d7395cfa-savings3`; separate session branches are not permitted in this environment.

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, dashboard, validation and Pages integration | done | arena-d7395cfa | COORDINATION.md, README.md, site/**, scripts/**, .github/workflows/** |

## Log
- 2026-10-22: Repository reviewed: README.md only, no other claims or source data. Claimed integration and all implementation files. Will publish unresolved rate/date/eligibility issues on Flagged for Review; no unconfirmed rates will be filled in.
- Claim publication fallback scope: root index.html and .nojekyll. GitHub Pages already serves main at repository root (legacy mode). API attempt to change Pages to workflow mode returned 403 Resource not accessible by integration. Preserve existing working Pages configuration and publish via main/root with a local redirect into site/. Validation workflow will not attempt an unauthorized Pages settings change.
- Research and integration completed: official source URLs and precise observed fields are recorded in site/evidence.json and on site/sources.html. Verified base APYs: Marcus 3.50%, Capital One comparison page 3.20%, Amex 3.20%, Ally 3.10%; disclosures generally dated October 21, 2026. Public pages checked October 22.
- Irregularities published in site/review.html: Synchrony conflicting headline/calculator, Capital One NaN extraction, unverified branch-bank/local rates and Citi geography, partial promotion terms, incomplete secondary eligibility/security evidence, Discover combined insurance, snapshot freshness and non-exhaustive scope. No unconfirmed numeric rate substituted.
- Validation: python scripts/build.py and python scripts/check.py pass; seven pages, internal file and fragment links, official citations per data row, annual return and FDIC ceiling arithmetic. External links were researched through official-page retrieval/search; no claim of blanket live HTTP availability from sandbox. Root fallback is a relative redirect with a clickable link; all site paths are repository-relative.

- PR https://github.com/sassnarep3-star/SAVINGS3/pull/1 merged successfully on 2026-10-22 at 00:07:17 UTC; merge commit e9e1e6cee0e40f783b4d5a1cd1f84709cf629740. PR build check passed.
- GitHub Pages build and deployment succeeded: https://github.com/sassnarep3-star/SAVINGS3/actions/runs/39697738661 (build, deploy, report-build-status all success). Live URL: https://sassnarep3-star.github.io/SAVINGS3/ (dashboard at /SAVINGS3/site/). Confirmation via GitHub deployment status; direct browser HTTP checks to github.io are outside sandbox host allowlist.
- GitHub-managed Pages build emitted non-blocking runner migration / forced Node 24 warnings; deployment passed. No application dependency or check failure.
- All unresolved research items remain published as needs review on site/review.html; they do not block completed integration. This follow-up documentation commit records the actual merge/deploy outcome after publication.

---

## Verification log (second pass, arena-71ffb49d)

* `python3 scripts/verify_site.py` exits 0: 10 generated pages, 66 unique external links, every internal link and
  anchor resolves, every external URL traces back to a URL stored in `/data`, every account row carries an https
  source, arithmetic spot checks pass, every flagged item has a source.
* FDIC certificate numbers confirmed through the FDIC institution API for 15 institutions. Discover Bank (5649)
  returns ACTIVE = 0 and is excluded from the returns tables.
* Rates verified on bank-owned pages only. No aggregator value appears anywhere in `data/`.
* 4 APY cells are blank by design (Chase, Citi, TD Simple, TD Signature) and published as F02–F04.

## Conflict log

| When (UTC) | Session | Event |
|---|---|---|
| 2026-10-22 | `arena-71ffb49d` | Started from commit 66f2767, which contained only a 10-byte README. While this session was researching, the first pass merged PRs #1 and #2 into `main`. Merge attempt hit add/add conflicts on `COORDINATION.md` and `index.html`, and a content conflict on `README.md`. |
| 2026-10-22 | `arena-71ffb49d` | Resolved without discarding either side: `index.html` keeps the second pass's dashboard (root is the Pages publish target); `README.md` and `COORDINATION.md` were rewritten to describe both passes; `site/`, `scripts/build.py` and `scripts/check.py` are preserved untouched. Recorded above. |

## Publication record

* PR #1 (first pass) merged 2026-10-22 00:07:17 UTC, merge commit `e9e1e6c`. Pages build/deploy run
  [#39697738661](https://github.com/sassnarep3-star/SAVINGS3/actions/runs/39697738661) succeeded.
* PR #2 (first pass follow-up) merged, merge commit `bcb43a1`.
* PR #3 (second pass / integration) — https://github.com/sassnarep3-star/SAVINGS3/pull/3 — merged successfully on
  2026-10-22 at 00:12:36 UTC, merge commit `46808f35`. The pull-request validation run (build.py, check.py,
  build_site.py, verify_site.py, generated-page freshness) passed before merge.
* GitHub Pages (legacy publishing, source `main` / root) rebuilt for merge commit `46808f35` and reported
  `status: built` at 2026-10-22 00:12:54 UTC. Live URLs:
  * https://sassnarep3-star.github.io/SAVINGS3/ — the full dashboard (root `index.html`, replaced the earlier
    redirect to `site/`)
  * https://sassnarep3-star.github.io/SAVINGS3/site/ — the first pass's snapshot, unchanged
* Post-deploy check: `index.html` served from `main` is the dashboard (13,032 bytes; `<h1>Savings Account Research
  Dashboard</h1>`), `accounts.html` 35,749 bytes, `assets/style.css` 8,422 bytes, and `site/index.html` still present.
  GitHub's Pages build status is the deployment confirmation; direct HTTP requests to `*.github.io` are outside
  this sandbox's network allowlist.
* No build, check or deploy failure occurred. No unresolved item blocks publication: all 19 flagged items are
  published on `flagged.html` with sources.
