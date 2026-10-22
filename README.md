# Savings Brief

Official-source savings research and a dependency-free GitHub Pages dashboard.

**Live site:** https://sassnarep3-star.github.io/SAVINGS3/

Snapshot checked October 22, 2026. Rates are variable. Projections are explicitly modeled, not guaranteed. Unconfirmed values remain empty; limitations appear on **Flagged for Review**. This is a curated shortlist, not an exhaustive market scan.

## Build and validate

```sh
python scripts/build.py
python scripts/check.py
```

`site/` is the deployable site. `scripts/build.py` holds the evidence ledger and content; `site/evidence.json` exports source notes and account fields. Validation checks internal paths/fragments, official-domain citations in every data row, and core model arithmetic. It does not claim a successful HTTP check for all external URLs: official source pages were researched separately, and this sandbox limits direct network access to bank hosts.

GitHub Actions validates pull requests and main. Existing GitHub Pages legacy publishing serves main at the repository root; the root landing redirect opens `site/`. Pages settings cannot be changed by the current integration (403), so the existing configuration is preserved. All CSS/JS assets are local; no packages, tracking, external fonts, or runtime API calls are required.
