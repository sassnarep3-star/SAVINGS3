# Federal Reserve Policy, FDIC National Benchmarks, & Complete Institution `CERT` Audit

**Audit Date:** `2026-10-22` (UTC)  
**Assumed Account Opening Date:** `2026-10-22`  
**Session:** `arena-36a5cee6` (`arena/36a5cee6-savings3`)

---

## 1. Federal Reserve Monetary Policy Benchmark (Official Primary Sources)

| Metric | Official Verified Value | Effective Date | Primary Official URL |
|---|---|---|---|
| **Federal Funds Target Range** | **`3.75% – 4.00%`** (+25 bps unanimous FOMC vote) | `2026-09-17` | https://www.federalreserve.gov/monetarypolicy/openmarket.htm |
| **Interest on Reserve Balances (IORB)** | **`3.90%`** | `2026-09-17` | https://www.federalreserve.gov/monetarypolicy/fomcminutes20260916.htm |
| **Overnight Reverse Repo Offering Rate (ON RRP)** | **`3.75%`** | `2026-09-17` | https://www.federalreserve.gov/monetarypolicy/fomcminutes20260916.htm |
| **Primary Credit (Discount Window) Rate** | **`4.00%`** | `2026-09-17` | https://www.federalreserve.gov/monetarypolicy/fomcminutes20260916.htm |
| **FOMC Minutes Release Date** | Minutes of Sep 15–16, 2026 meeting published **`2026-10-07`** | `2026-10-07` | https://www.federalreserve.gov/monetarypolicy/fomcminutes20260916.htm |

**Key Rate-Competitiveness Takeaway:** In October 2026, FDIC-insured banks earn **`3.90%` risk-free overnight IORB** directly at the Federal Reserve (`12 C.F.R. § 204.10`).
- Top unconditional national savings leaders (**E\*TRADE / Morgan Stanley Private Bank `3.75%` base / `4.25%` 6m boost** and **CIT Bank / First-Citizens `3.75%` Platinum / `4.25%` 6m `BOOST50`**) pass through **96.2% of IORB unconditionally** and **109.0% of IORB during their 6-month promotional windows**.
- Brick-and-mortar branch megabanks (**`0.01%–0.05%` standard APY**) pass through **0.26%–1.28% of IORB**, capturing **`385–389 bps` of net interest spread** (`~$9,625–$9,725/year` per `$250,000` deposit).

---

## 2. FDIC National Deposit Rates & Statutory Rate Caps (`2026-10-19` Revision)

Source: https://www.fdic.gov/national-rates-and-rate-caps (*Monthly Rate Update: October 20, 2026, accurate as of October 19, 2026*).

| Deposit Product / Maturity | National Rate (`< $100,000` non-jumbo / `$2,500` savings tier) | FDIC Statutory Rate Cap | Year-1 Interest on `$250,000` at National Rate |
|---|---|---|---|
| **Savings** | **`0.38%`** | `4.63%` | **`$950.00`** |
| **Interest Checking** | `0.07%` | `4.32%` | `$175.00` |
| **Money Market** | `0.63%` | `4.88%` | `$1,575.00` |
| **1-Month CD** | `0.94%` | `4.83%` | `$2,350.00` |
| **3-Month CD** | `1.14%` | `4.95%` | `$2,850.00` |
| **6-Month CD** | `1.39%` | `5.10%` | `$3,475.00` |
| **12-Month CD** | **`1.76%`** | `5.33%` | **`$4,400.00`** |
| **24-Month CD** | `1.55%` | `5.04%` | `$3,875.00` |
| **36-Month CD** | `1.39%` | `4.90%` | `$3,475.00` |
| **60-Month CD** | `1.41%` | `5.02%` | `$3,525.00` |

**Term-Structure Observation:** The FDIC national CD curve peaks at **12 months (`1.76%`)** and slopes downward at **24–60 months (`1.55% → 1.39% → 1.41%`)**, reflecting market pricing for lower equilibrium policy rates beyond 12 months. This confirms that 3-year and 5-year variable-rate savings tables must be treated strictly as **constant-APY mathematical projections**, while 6-month promo boosts (`4.25%–4.40%`) lock in top returns across the immediate post-opening window (`2026-10-22` to `2027-04-22`).

---

## 3. Complete 21-Institution FDIC `api.fdic.gov` & Fed Large-Bank Audit

Sources:
- Federal Reserve Statistical Release — *Large Commercial Banks* (as of `2026-06-30`, published `2026-10-02`): https://www.federalreserve.gov/releases/lbr/current/default.htm
- FDIC Public Institution API (`ACTIVE`, `INSFDIC`, `CERT`, `ASSET`, `CITY`, `STALP`, updated `2026-10-16`): https://api.fdic.gov/banks/institutions

| U.S. Asset Rank (Fed LBR) | Consumer Brand | Official FDIC Legal Charter Name | FDIC `CERT` | HQ (`CITY, ST`) | Total Assets (`api.fdic.gov` `$M`) | `ACTIVE` / `INSFDIC` | Audit Status & Notes |
|---:|---|---|---:|---|---:|---|---|
| **#1** | Chase | JPMorgan Chase Bank, National Association | **`628`** | Columbus, OH | `$4,089,899` (`$4.09T`) | `1` / `1` | Verified |
| **#2** | Bank of America | Bank of America, National Association | **`3510`** | Charlotte, NC | `$2,645,427` (`$2.65T`) | `1` / `1` | Verified |
| **#3** | Citibank | Citibank, N.A. | **`7213`** | Sioux Falls, SD | `$1,981,967` (`$1.98T`) | `1` / `1` | Verified |
| **#4** | Wells Fargo | Wells Fargo Bank, National Association | **`3511`** | Sioux Falls, SD | `$1,908,901` (`$1.91T`) | `1` / `1` | Verified |
| **—** (IBHC) | Marcus by Goldman Sachs | Goldman Sachs Bank USA | **`33124`** | New York, NY | `$758,832` (`$758.8B`) | `1` / `1` | Verified |
| **#5** | U.S. Bank | U.S. Bank National Association | **`6548`** | Cincinnati, OH | `$705,555` (`$705.6B`) | `1` / `1` | **Resolved Pass 2 `F07`** via `CERT:6548` |
| **#6** | Capital One 360 / Discover | Capital One, National Association | **`4297`** | McLean, VA | `$662,155` (`$662.2B`) | `1` / `1` | Verified (Discover merged into `4297`) |
| **#7** | PNC Bank | PNC Bank, National Association | **`6384`** | Wilmington, DE | `$609,814` (`$609.8B`) | `1` / `1` | Verified |
| **#8** | Truist | Truist Bank | **`9846`** | Charlotte, NC | `$548,303` (`$548.3B`) | `1` / `1` | Verified |
| **#10** | TD Bank | TD Bank, N.A. | **`18409`** | Wilmington, DE | `$342,848` (`$342.8B`) | `1` / `1` | Verified |
| **#12** | Charles Schwab Bank | Charles Schwab Bank, SSB | **`57450`** | Westlake, TX | `$280,145` (`$280.1B`) | `1` / `1` | Verified |
| **#16** | BMO / Alto Online Savings | BMO Bank National Association | **`16571`** | Chicago, IL | `$254,968` (`$255.0B`) | `1` / `1` | **Added in Pass 3** (`Alto` shares `CERT 16571`) |
| **#17** | E\*TRADE from Morgan Stanley | Morgan Stanley Private Bank, National Association | **`34221`** | Purchase, NY | `$250,428` (`$250.4B`) | `1` / `1` | **Added in Pass 3** (`$500k` single / `$1M` joint sweep) |
| **#18** | CIT Bank (Division of First-Citizens) | First-Citizens Bank & Trust Company | **`11063`** | Raleigh, NC | `$236,317` (`$236.3B`) | `1` / `1` | **Added in Pass 3** (CIT + First Citizens share `11063`) |
| **#19** | Citizens / Citizens Access | Citizens Bank, National Association | **`57957`** | Providence, RI | `$232,519` (`$232.5B`) | `1` / `1` | Verified (Citizens + Citizens Access share `57957`) |
| **#20** | American Express National Bank | American Express National  Bank | **`27471`** | Sandy, UT | `$213,946` (`$213.9B`) | `1` / `1` | **Resolved Pass 2 `F06`** (double-space in FDIC `NAME`) |
| **#22** | Fifth Third Bank | Fifth Third Bank, National Association | **`6672`** | Cincinnati, OH | `$212,243` (`$212.2B`) | `1` / `1` | Verified |
| **#24** | Ally Bank | Ally Bank | **`57803`** | Sandy, UT | `$188,243` (`$188.2B`) | `1` / `1` | Verified |
| **#31** | Synchrony Bank | Synchrony Bank | **`27314`** | Draper, UT | `$115,244` (`$115.2B`) | `1` / `1` | Verified |
| **#48** | SoFi Bank | SoFi Bank, National Association | **`26881`** | Cottonwood Heights, UT | `$56,777` (`$56.8B`) | `1` / `1` | Verified (`$3M` multi-bank sweep network) |
| **#58** | Barclays US Consumer Bank | Barclays Bank Delaware | **`57203`** | Wilmington, DE | `$43,453` (`$43.5B`) | `1` / `1` | **Added in Pass 3** |
| *(Merged)* | Discover Bank *(inactive charter)* | Discover Bank | **`5649`** | Greenwood, DE | *Merged into `4297`* | **`0`** / `0` | Inactive since `2025-05-18` merger into Capital One |

### Technical Root Causes Documented During FDIC Audit
1. **Why Pass 2 missed `American Express National Bank` (`F06`)**: In the FDIC public database (`api.fdic.gov/banks/institutions?filters=CERT:27471`), the `NAME` column is stored with **two consecutive spaces**: `"American Express National  Bank"`. Exact phrase searches with a single space return `total: 0`. Querying `CERT:27471` confirms active FDIC coverage (`Sandy, UT`, `$213.95B` assets).
2. **Why `Capital One` (`May 18, 2025` vs `November 18, 2025`) is legally consistent (`F19`)**: Under `12 U.S.C. § 1818(q)` (FDIC assumption/merger rule), existing depositors holding separate accounts at two merging institutions receive a **six-month post-merger separate insurance grace period** (`May 18, 2025 + 6 months = November 18, 2025`), while *newly opened* deposits post-merger aggregate immediately under surviving charter `CERT #4297` (and time deposits with maturities beyond 6 months remain separately insured until first maturity). Today (`2026-10-22`), **Capital One 360 and Discover share one `$250,000` single-owner cap (`CERT #4297`)**.
