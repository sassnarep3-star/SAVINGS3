# Coordination board

Session: arena-d7395cfa (integration). All work uses the Arena-required branch `arena/d7395cfa-savings3`; separate session branches are not permitted in this environment.

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, dashboard, validation and Pages integration | in progress | arena-d7395cfa | COORDINATION.md, README.md, site/**, scripts/**, .github/workflows/** |

## Log
- 2026-10-22: Repository reviewed: README.md only, no other claims or source data. Claimed integration and all implementation files. Will publish unresolved rate/date/eligibility issues on Flagged for Review; no unconfirmed rates will be filled in.
- Claim publication fallback scope: root index.html and .nojekyll. GitHub Pages already serves main at repository root (legacy mode). API attempt to change Pages to workflow mode returned 403 Resource not accessible by integration. Preserve existing working Pages configuration and publish via main/root with a local redirect into site/. Validation workflow will not attempt an unauthorized Pages settings change.
- Research and integration completed: official source URLs and precise observed fields are recorded in site/evidence.json and on site/sources.html. Verified base APYs: Marcus 3.50%, Capital One comparison page 3.20%, Amex 3.20%, Ally 3.10%; disclosures generally dated October 21, 2026. Public pages checked October 22.
- Irregularities published in site/review.html: Synchrony conflicting headline/calculator, Capital One NaN extraction, unverified branch-bank/local rates and Citi geography, partial promotion terms, incomplete secondary eligibility/security evidence, Discover combined insurance, snapshot freshness and non-exhaustive scope. No unconfirmed numeric rate substituted.
- Validation: python scripts/build.py and python scripts/check.py pass; seven pages, internal file and fragment links, official citations per data row, annual return and FDIC ceiling arithmetic. External links were researched through official-page retrieval/search; no claim of blanket live HTTP availability from sandbox. Root fallback is a relative redirect with a clickable link; all site paths are repository-relative.
