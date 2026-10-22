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
