# COORDINATION.md — Shared Task Board

> Multiple agent sessions may work on this repo at the same time. Read this file before starting. Claim before you edit. Keep scopes non-overlapping.

**Repo:** https://github.com/sassnarep3-star/SAVINGS3
**Verification date basis for this build:** 2026-10-22 (account-open date used for all return projections)
**Integration branch for this session:** `arena/dbe2ef46-savings3` (Arena-fixed branch name; see Note on branch naming below)

## Note on branch naming (deviation logged)

The project brief asks for branches named `session-<id>/<task>`. This Arena session is locked to branch `arena/dbe2ef46-savings3` by the platform and cannot rename or switch branches. All work for session `dbe2ef46` is therefore done on `arena/dbe2ef46-savings3`. This is the integration branch for the final PR to `main`. No work is lost; only the branch *name* differs from the brief.

## How to claim a task

1. Add/Update a row below: status `in progress`, your session ID, exact file scope, timestamp (UTC).
2. Commit and push that claim immediately (`git pull --rebase` before every push).
3. Edit **only** files in your claimed scope. Need a file owned by someone else? Log a request under "Change requests" instead of editing it.
4. Small, frequent commits. On conflict: stop, resolve without discarding the other session's work, log it under "Conflict log".
5. When done: record sources + verification performed + irregularities in the task row / log, mark `done`.
6. `needs review` = published on the site's **Flagged for Review** page; it does **not** block merge.
7. A claim >60 minutes old with no commits may be taken over; note the handoff in the log.
8. Shared outputs (combined table data, site index/navigation) are changed only by the final integration session.

## Verification rule (applies to every session)

- Every table row must have a source link to an **official** site (bank's own domain, FDIC.gov, FederalReserve.gov, CFPB.gov).
- If a value cannot be confirmed from an official source, leave it **blank** and flag it **UNVERIFIED** on the Flagged for Review page. Never infer or fill in values.
- Record the "as of" date shown by the source and the date you verified it (2026-10-22).

## Task board

| # | Task | Status | Owner (session) | Branch | File scope | Claimed (UTC) |
|---|------|--------|-----------------|--------|------------|---------------|
| 1 | Create COORDINATION.md + repo review | done | dbe2ef46 | arena/dbe2ef46-savings3 | `COORDINATION.md` | 2026-10-22 00:05 |
| 2 | Research: define "big national banks" from official source (Federal Reserve Large Commercial Banks) + FDIC limit + national-average benchmark | in progress | dbe2ef46 | arena/dbe2ef46-savings3 | `docs/research-notes.md` (new) | 2026-10-22 00:05 |
| 3 | Research: traditional savings rates — Chase, Bank of America, Wells Fargo, Citi, U.S. Bank, PNC, Truist, TD, Capital One (branch savings) from official bank pages | in progress | dbe2ef46 | arena/dbe2ef46-savings3 | `docs/research-notes.md` | 2026-10-22 00:05 |
| 4 | Research: high-yield / online savings from big national banks — Capital One 360, Ally, Marcus (Goldman Sachs), Amex, Discover, Citizens Access, Citi Accelerate (if offered), PNC HY (if offered) | in progress | dbe2ef46 | arena/dbe2ef46-savings3 | `docs/research-notes.md` | 2026-10-22 00:05 |
| 5 | Research: money-market accounts + CDs (for lifespan comparison) from same big banks | in progress | dbe2ef46 | arena/dbe2ef46-savings3 | `docs/research-notes.md` | 2026-10-22 00:05 |
| 6 | Research: new-account bonuses/promotions, eligibility & opening rules (official offer pages only) | in progress | dbe2ef46 | arena/dbe2ef46-savings3 | `docs/research-notes.md` | 2026-10-22 00:05 |
| 7 | Return-on-investment tables: $10k / $50k / $100k / $250k (max FDIC single-account) × 6mo / 1yr / 2yr / 3yr / 5yr from 2026-10-22 | in progress | dbe2ef46 | arena/dbe2ef46-savings3 | `docs/research-notes.md`, site tables | 2026-10-22 00:05 |
| 8 | Build GitHub Pages site (landing dashboard + subpages by category + Flagged for Review + Methodology) | in progress | dbe2ef46 | arena/dbe2ef46-savings3 | `docs/index.html`, `docs/*.html`, `docs/assets/*`, `.github/workflows/*`, `README.md` | 2026-10-22 00:05 |
| 9 | Final integration: re-verify combined data line by line, check links/build, PR to main, merge, confirm Pages deploy | in progress | dbe2ef46 | arena/dbe2ef46-savings3 | all above (integration only) | 2026-10-22 00:05 |

> This session (dbe2ef46) is running as a single end-to-end session **and** final integration session, as instructed ("Work fully on your own from start to finish"). If a parallel session starts, it must claim a NEW non-overlapping task row before editing anything, and must not edit the files listed above without logging a change request.

## Change requests (file owned by another session)

_None as of 2026-10-22 00:05 UTC._

## Conflict log

_None as of 2026-10-22 00:05 UTC._

## Handoff log

_None as of 2026-10-22 00:05 UTC._

## Sources & verification log

_To be filled as each task completes. Each entry: value → official URL → source "as of" date → verified 2026-10-22. UNVERIFIED items listed here and on the Flagged for Review page._

## Irregularities flagged

_To be filled. Also published on `docs/flagged.html`._

## PR & deploy log

_To be filled at integration: PR link, merge result, Pages URL, deploy status._
