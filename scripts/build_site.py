#!/usr/bin/env python3
"""
Static-site generator for the SAVINGS3 research site.

Reads everything from /data (banks, accounts, bonuses, security, FDIC rules, flagged items,
sources) and writes flat HTML pages to the repository root, which GitHub Pages serves directly.

Design rules enforced here:
  * every numeric cell in an accounts/returns table is either taken from data/accounts.json
    (which cites an official source per row) or is arithmetic derived from it, and the formula
    is printed on the page;
  * a missing value stays blank and is linked to the Flagged for Review page - it is never
    guessed, defaulted, or filled from a third-party aggregator.
"""

import json
import os
from datetime import date
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

with open(os.path.join(DATA, "meta.json")) as f:
    META = json.load(f)
with open(os.path.join(DATA, "accounts.json")) as f:
    ACCOUNTS = json.load(f)
with open(os.path.join(DATA, "security.json")) as f:
    SECURITY = json.load(f)
with open(os.path.join(DATA, "fdic.json")) as f:
    FDIC = json.load(f)
with open(os.path.join(DATA, "flagged.json")) as f:
    FLAGGED = json.load(f)
with open(os.path.join(DATA, "sources.json")) as f:
    SOURCES = json.load(f)

BANKS = {b["id"]: b for b in META["banks"]}
ROWS = ACCOUNTS["rows"]
CAPTURE = META["capture_date"]
OPEN_DATE = META["open_date"]
NATIONAL = META["fdic_national_savings_rate"]
DEPOSITS = META["deposits"]
TERMS = META["terms"]
MAX_COVERED = 1250000


# ----------------------------------------------------------------------------- helpers
def money(value, decimals=None):
    if value is None:
        return ""
    if decimals is None:
        decimals = 0 if abs(value) >= 100 else 2
    return f"${value:,.{decimals}f}"


def pct(value, decimals=2):
    if value is None:
        return ""
    return f"{value:.{decimals}f}%"


def growth(principal, apy, years):
    """Future value of a lump sum at a quoted APY, held for `years`.

    APY already includes compounding, so the one-year factor is (1 + APY). Holding the same
    APY for N years compounds it N times. This is an arithmetic projection, not a promise.
    """
    if apy is None:
        return None
    return principal * ((1 + apy / 100.0) ** years)


def tier_apy(row, deposit):
    """APY that applies to `deposit` for a row, using the highest qualifying tier."""
    tiers = row.get("tiers") or []
    if not tiers:
        return row.get("apy")
    best = None
    for t in tiers:
        if deposit >= t.get("min", 0):
            if best is None or t["min"] >= best["min"]:
                best = t
    return best["apy"] if best else row.get("apy")


def tier_label(row, deposit):
    tiers = row.get("tiers") or []
    best = None
    for t in tiers:
        if deposit >= t.get("min", 0):
            if best is None or t["min"] >= best["min"]:
                best = t
    if best and best.get("label"):
        return best["label"]
    return ""


def verified_rows():
    return [r for r in ROWS if r.get("apy") is not None]


def badge(ok, text_ok="Verified", text_no="Unverified"):
    cls = "ok" if ok else "warn"
    return f'<span class="badge {cls}">{text_ok if ok else text_no}</span>'


def src_links(row, limit=None):
    links = row.get("sources") or []
    if limit:
        links = links[:limit]
    out = []
    for s in links:
        out.append(f'<a href="{escape(s["url"])}" target="_blank" rel="noopener">{escape(s["label"])}</a>')
    return "<br>".join(out)


def bank_link(bank_id):
    b = BANKS.get(bank_id)
    if not b:
        return ""
    return escape(b["brand"])


NAV = [
    ("index.html", "Dashboard"),
    ("accounts.html", "Accounts"),
    ("returns.html", "Returns"),
    ("fdic-insurance.html", "FDIC Coverage"),
    ("bonuses.html", "Bonuses"),
    ("rates-competitiveness.html", "Rate Check"),
    ("security-apps.html", "App & Security"),
    ("flagged.html", "Flagged"),
    ("methodology.html", "Method"),
    ("sources.html", "Sources"),
]


def page(title, subtitle, body, active, extra_head="", body_class=""):
    parts = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        parts.append(f'<a href="{href}"{cls}>{label}</a>')
    nav_html = "".join(parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · Savings Account Research</title>
<link rel="stylesheet" href="assets/style.css">
{extra_head}
</head>
<body class="{body_class}">
<header class="topbar">
  <div class="wrap topbar-inner">
    <a class="brand" href="index.html"><span class="dot"></span> Savings Research</a>
    <nav class="nav">{nav_html}</nav>
  </div>
</header>
<main class="wrap">
  <div class="page-head">
    <h1>{escape(title)}</h1>
    <p class="sub">{subtitle}</p>
  </div>
  {body}
</main>
<footer class="foot">
  <div class="wrap">
    <p><strong>Captured {CAPTURE} (UTC).</strong> Projected opening date {OPEN_DATE}. Every rate, fee and rule
    on this site is transcribed from the official page linked in the same row. Blank means the value could
    not be confirmed on an official page — see <a href="flagged.html">Flagged for Review</a>.
    Nothing here is financial advice.</p>
  </div>
</footer>
</body>
</html>
"""


# ----------------------------------------------------------------------------- derived tables
TOP = sorted(verified_rows(), key=lambda r: -(r.get("apy") or 0))


def best_for(deposit):
    best = None
    for r in verified_rows():
        a = tier_apy(r, deposit)
        if a is None:
            continue
        if best is None or a > best[1]:
            best = (r, a)
    return best


# ----------------------------------------------------------------------------- index page
def build_index():
    best = TOP[0]
    best_apy = best["apy"]
    inter_250k = 250000 * best_apy / 100.0
    nat_250k = 250000 * NATIONAL / 100.0
    bofa = next(r for r in ROWS if r["id"] == "bofa-advantage")
    plan_1 = MAX_COVERED * best_apy / 100.0
    plan_bofa = MAX_COVERED * bofa["apy"] / 100.0

    stacked = [r for r in TOP if r["apy"] is not None][:5]
    blended = sum(tier_apy(r, 250000) for r in stacked) / len(stacked)
    stacked_yield = 250000 * sum(tier_apy(r, 250000) for r in stacked) / 100.0

    cards = f"""
<section class="grid cards">
  <div class="card hero-card">
    <span class="label">Best verified APY · all balances</span>
    <span class="big">{pct(best_apy)}</span>
    <span class="muted">{bank_link(best["bank_id"])} — {escape(best["product"])}</span>
    <span class="fine">No minimum deposit, no monthly fee. Rate is variable.</span>
  </div>
  <div class="card">
    <span class="label">FDIC national savings rate</span>
    <span class="big">{pct(NATIONAL)}</span>
    <span class="muted">Effective {META["fdic_national_rate_effective"]}</span>
    <span class="fine">Official benchmark the banks are measured against.</span>
  </div>
  <div class="card">
    <span class="label">Interest on $250,000 · 1 year</span>
    <span class="big">{money(inter_250k)}</span>
    <span class="muted">at {pct(best_apy)} vs {money(nat_250k)} at the national rate</span>
    <span class="fine">+{money(inter_250k - nat_250k)} for the same insured deposit.</span>
  </div>
  <div class="card">
    <span class="label">Fully insured at one bank</span>
    <span class="big">{money(MAX_COVERED)}</span>
    <span class="muted">1 owner × 5 POD beneficiaries × $250,000</span>
    <span class="fine">Structure matters more than the number of banks.</span>
  </div>
</section>
"""

    rows = ""
    for r in TOP[:8]:
        b = BANKS[r["bank_id"]]
        cert = b.get("fdic_cert") or "not captured"
        legal = "" if b["legal_name"] == b["brand"] else f'<span class="cell-sub">{escape(b["legal_name"])}</span>'
        promo = ' <span class="badge warn">promo</span>' if r.get("promos") else ""
        rows += f"""<tr>
  <td data-label="Rank"><span class="rank">{TOP.index(r) + 1}</span></td>
  <td data-label="Bank"><strong>{escape(b["brand"])}</strong>{legal}</td>
  <td data-label="Account">{escape(r["product"])}{promo}<span class="cell-sub">FDIC cert {escape(cert)}</span></td>
  <td data-label="APY" class="num strong">{pct(r["apy"])}</td>
  <td data-label="APY as of">{escape(r["apy_as_of"] or "not printed")}</td>
  <td data-label="Interest on $250k / yr" class="num">{money(250000 * tier_apy(r, 250000) / 100.0)}</td>
  <td data-label="Source"><a href="{escape(r["sources"][0]["url"])}" target="_blank" rel="noopener">Official page</a></td>
</tr>"""

    findings = f"""
<section class="section">
  <h2>What the research found</h2>
  <ol class="findings">
    <li><strong>The gap is enormous.</strong> The best verified savings APY is {pct(best_apy)}
        ({escape(BANKS[best['bank_id']]['brand'])}). The weakest verified big-branch rate is
        {pct(bofa['apy'])} ({escape(BANKS[bofa['bank_id']]['brand'])}). On $250,000 that is
        {money(inter_250k)} versus {money(250000 * bofa['apy'] / 100.0)} a year — both fully FDIC-insured.</li>
    <li><strong>Rate is not the only requirement.</strong> Chase, Citi and TD do not publish a readable
        savings APY without a ZIP code or a script, so their rates are left blank here rather than copied
        from a rate aggregator. They are still listed with their fees, minimums and rules.</li>
    <li><strong>Standard branch-network rates are not built to hold large balances.</strong> Every
        non-promotional rate verified at a branch network on this site falls between
        {pct(min(r["apy"] for r in ROWS if r["bank_id"] in ("bofa","wellsfargo","usbank","truist","schwab","chase","citi","td") and r["apy"] is not None))}
        and {pct(max(r["apy"] for r in ROWS if r["bank_id"] in ("bofa","wellsfargo","usbank","truist","schwab","chase","citi","td") and r["apy"] is not None))} APY.
        At Bank of America's {pct(bofa['apy'])} a $1.25M balance earns {money(plan_bofa)} a year before fees.
        The same $1.25M at {pct(best_apy)} earns {money(plan_1)}, roughly {plan_1 / plan_bofa:.0f}× more.</li>
    <li><strong>FDIC coverage is a design problem, not a bank problem.</strong> $250,000 per depositor per bank
        per ownership category, or up to $1,250,000 per owner through a payable-on-death structure with five
        beneficiaries. The <a href="fdic-insurance.html">coverage page</a> prices out four structures.</li>
    <li><strong>Promotions move the answer more than the APY does.</strong> Chase pays a $200 bonus on a
        $10,000 deposit held 90 days; SoFi and Wells Fargo run APY boosts. Those are priced on the
        <a href="bonuses.html">bonuses page</a>.</li>
  </ol>
</section>
"""

    body = cards + f"""
<section class="section">
  <div class="section-head">
    <h2>Highest verified rates</h2>
    <a class="link-more" href="accounts.html">Full account table →</a>
  </div>
  <p class="note">Sorted by APY. A rate appears here only if a number was printed on the bank's own page
  during this session. "APY as of" is the date the bank printed, not the date this site was built.
  Rows tagged <span class="badge warn">promo</span> depend on eligibility conditions — see
  <a href="bonuses.html">Bonuses</a>.</p>
  <div class="table-scroll">
  <table class="table">
    <thead><tr>
      <th>#</th><th>Bank</th><th>Account</th><th class="num">APY</th><th>APY as of</th>
      <th class="num">Interest on $250k / yr</th><th>Source</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
</section>
{findings}
<section class="section">
  <h2>Best fully insured structure for $1.25M</h2>
  <div class="grid two">
    <div class="panel">
      <h3>One bank, five beneficiaries</h3>
      <p class="muted">FDIC trust formula: 1 owner × 5 beneficiaries × $250,000 = $1,250,000 insured.</p>
      <table class="mini">
        <tr><td>Holder</td><td>{escape(BANKS[best["bank_id"]]["brand"])} — {escape(best["product"])}</td></tr>
        <tr><td>APY used</td><td>{pct(best_apy)}</td></tr>
        <tr><td>Year-1 interest</td><td class="num strong">{money(plan_1)}</td></tr>
        <tr><td>Year-3 balance</td><td class="num">{money(growth(MAX_COVERED, best_apy, 3))}</td></tr>
        <tr><td>Year-5 balance</td><td class="num">{money(growth(MAX_COVERED, best_apy, 5))}</td></tr>
        <tr><td>Sources</td><td><a href="{escape(best["sources"][0]["url"])}" target="_blank" rel="noopener">Rate</a> ·
        <a href="https://www.fdic.gov/resources/deposit-insurance/financial-products-insured" target="_blank" rel="noopener">FDIC trust rule</a></td></tr>
      </table>
      <p class="fine">Every figure above is arithmetic on the linked rate; the structure limit is the FDIC trust formula.</p>
    </div>
    <div class="panel">
      <h3>Five banks, $250,000 each</h3>
      <p class="muted">Splits the same money across the five highest verified APYs. No beneficiary paperwork.</p>
      <table class="mini">
        <tr><td>Blended APY</td><td>{pct(blended)}</td></tr>
        <tr><td>Year-1 interest</td><td class="num strong">{money(stacked_yield)}</td></tr>
        <tr><td>Difference vs one bank</td><td class="num">{money(stacked_yield - plan_1)}</td></tr>
        <tr><td>Year-5 balance</td><td class="num">{money(sum(growth(250000, tier_apy(r, 250000), 5) for r in stacked))}</td></tr>
        <tr><td>Sources</td><td><a href="{escape(stacked[0]["sources"][0]["url"])}" target="_blank" rel="noopener">Rate 1</a> ·
        <a href="{escape(stacked[1]["sources"][0]["url"])}" target="_blank" rel="noopener">Rate 2</a> ·
        <a href="{escape(stacked[2]["sources"][0]["url"])}" target="_blank" rel="noopener">Rate 3</a> ·
        <a href="{escape(stacked[3]["sources"][0]["url"])}" target="_blank" rel="noopener">Rate 4</a> ·
        <a href="{escape(stacked[4]["sources"][0]["url"])}" target="_blank" rel="noopener">Rate 5</a></td></tr>
      </table>
      <p class="fine">Every figure above is arithmetic on the linked rates; the $250,000-per-bank limit is the FDIC rule.</p>
    </div>
  </div>
  <p class="note">Both structures are fully insured at $1.25M. The single-bank POD route earns more because it
  puts the whole balance at the top rate — but it requires the bank to accept five POD beneficiaries, which
  varies by bank. Confirm that before relying on it. Interest also accrues above the cap, so a balance sitting
  exactly at $1,250,000 will drift over it; see <a href="fdic-insurance.html">FDIC Coverage</a>.</p>
</section>
"""
    return page(
        "Savings Account Research Dashboard",
        f"FDIC-insured savings options at large national banks and national online banks, verified line by line "
        f"against official sources on {CAPTURE}. Models use a {OPEN_DATE} account opening.",
        body,
        "index.html",
    )


# ----------------------------------------------------------------------------- accounts page
def build_accounts():
    ordered = sorted(ROWS, key=lambda r: (r.get("apy") is None, -(r.get("apy") or 0)))
    rows = ""
    for r in ordered:
        b = BANKS[r["bank_id"]]
        cert = b.get("fdic_cert") or "not captured"
        apy_cell = pct(r["apy"]) if r.get("apy") is not None else '<span class="blank">blank</span>'
        min_open = r["min_open_text"] or money(r.get("min_open"))
        fee = r["fee_text"] or money(r.get("monthly_fee"))
        flags = ""
        if r.get("flags"):
            flags = '<ul class="flags">' + "".join(f"<li>{escape(f)}</li>" for f in r["flags"]) + "</ul>"
        first_src = r["sources"][0]
        legal = "" if b["legal_name"] == b["brand"] else f'<span class="cell-sub">{escape(b["legal_name"])}</span>'
        rows += f"""<tr>
  <td data-label="Bank">
    <strong>{escape(b["brand"])}</strong>
    {legal}
    <span class="cell-sub">FDIC cert {escape(cert)}</span>
    <span class="cell-sub">{badge(b.get("verified", False), "FDIC verified", "FDIC unconfirmed")}</span>
  </td>
  <td data-label="Account">
    <strong>{escape(r["product"])}</strong>
    <span class="cell-sub">{escape(r["rate_type"])}</span>
    {badge(r.get("apy") is not None, "Rate verified", "Rate unverified")}
  </td>
  <td data-label="APY" class="num strong">{apy_cell}
    <span class="cell-sub">{escape(r["apy_as_of_text"])}</span>
  </td>
  <td data-label="Minimums">{escape(min_open)}
    <span class="cell-sub">{escape(r["min_to_earn_text"])}</span>
  </td>
  <td data-label="Monthly fee">{escape(fee)}
    <span class="cell-sub">{escape(r["fee_waiver"])}</span>
  </td>
  <td data-label="Rules">{escape(r["withdrawal_rule"])}
    <span class="cell-sub">{escape(r["atm"])}</span>
  </td>
  <td data-label="Source">{src_links(r)}</td>
</tr>
<tr class="flagrow"><td colspan="6">{flags if flags else '<span class="muted">No irregularities logged for this row.</span>'}</td>
  <td><a href="{escape(first_src['url'])}" target="_blank" rel="noopener">Row source</a></td></tr>"""

    body = f"""
<p class="lede">Every savings account reviewed, with the exact value the bank printed and a link to the page
it was printed on. Rows marked <span class="badge warn">Rate unverified</span> are kept because their fees,
minimums and rules are real and useful — the APY cell is deliberately empty.</p>

<div class="statline">
  <span><strong>{len(ROWS)}</strong> accounts reviewed</span>
  <span><strong>{len(verified_rows())}</strong> with a verified APY</span>
  <span><strong>{len(ROWS) - len(verified_rows())}</strong> with APY left blank</span>
  <span><strong>{len([b for b in BANKS.values() if b.get("verified")])}</strong> FDIC records confirmed</span>
</div>

<div class="table-scroll">
<table class="table wide">
  <thead><tr>
    <th>Bank / FDIC</th><th>Account</th><th class="num">APY</th><th>Minimums</th>
    <th>Monthly fee &amp; waiver</th><th>Rules / access</th><th>Sources</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
</div>

<section class="section">
  <h2>How to read the APY column</h2>
  <ul class="list">
    <li><strong>A number</strong> means the bank's own page printed that percentage, and the "as of" date is
        what the bank printed next to it. If the bank printed no date, the cell says so.</li>
    <li><strong>blank</strong> means no official page in this session displayed a rate. Chase, Citi and TD
        all gate their rate tables behind a ZIP code or client-side script. Third-party rate trackers do
        publish numbers for those banks; none of them are used here.</li>
    <li><strong>Tiered accounts</strong> (U.S. Bank, Wells Fargo Platinum) show the standard rate; the tiers
        are spelled out in the row and used in the <a href="returns.html">returns tables</a>.</li>
    <li><strong>Variable</strong> means the bank can change the APY at any time, including right after the
        account is opened. Only CDs are fixed.</li>
  </ul>
</section>
"""
    return page(
        "Accounts & Rates",
        "Sixteen savings accounts across branch and online national banks, with minimums, fees, waiver rules and the official source for each value.",
        body,
        "accounts.html",
    )


# ----------------------------------------------------------------------------- returns page
def build_returns():
    rows_verified = sorted(verified_rows(), key=lambda r: -(tier_apy(r, 250000) or 0))

    tables = ""
    for years in TERMS:
        head = "".join(f"<th class='num'>{money(d)}</th>" for d in DEPOSITS)
        head += "<th>Rate source</th>"
        body_rows = ""
        for r in rows_verified:
            cells = ""
            for d in DEPOSITS:
                apy = tier_apy(r, d)
                fv = growth(d, apy, years)
                gain = fv - d
                cells += (
                    f"<td class='num'>{money(fv)}"
                    f"<span class='cell-sub'>+{money(gain)} @ {pct(apy)}</span></td>"
                )
            note = ""
            if r["id"] in ("wellsfargo-platinum-promo",):
                note = "<span class='cell-sub'>promo: new customers, $25k+</span>"
            elif r["id"] == "usbank-smartly":
                note = "<span class='cell-sub'>tiers need a U.S. Bank checking relationship</span>"
            src = r["sources"][0]
            body_rows += (
                f"<tr><td><strong>{escape(BANKS[r['bank_id']]['brand'])}</strong>"
                f"<span class='cell-sub'>{escape(r['product'])}</span>{note}</td>{cells}"
                f"<td><a href='{escape(src['url'])}' target='_blank' rel='noopener'>Official page</a>"
                f"<span class='cell-sub'>{escape(r['apy_as_of_text'][:70])}</span></td></tr>"
            )
        tables += f"""
<h2 id="term-{years}">{years}-year horizon</h2>
<p class="note">Total balance if the quoted APY applied unchanged for {years} year{'s' if years > 1 else ''},
compounded annually (APY already includes compounding). Interest is the small line under each balance.</p>
<div class="table-scroll">
<table class="table returns">
  <thead><tr><th>Account</th>{head}</tr></thead>
  <tbody>{body_rows}</tbody>
</table>
</div>
"""

    best_rows = ""
    for d in DEPOSITS:
        r, apy = best_for(d)
        best_rows += f"""<tr>
  <td class="num strong">{money(d)}</td>
  <td>{escape(BANKS[r["bank_id"]]["brand"])} — {escape(r["product"])}</td>
  <td class="num strong">{pct(apy)}</td>
  <td class="num">{money(d * apy / 100)}</td>
  <td class="num">{money(growth(d, apy, 3) - d)}</td>
  <td class="num">{money(growth(d, apy, 5) - d)}</td>
  <td class="num">{money(d * apy / 100 - d * NATIONAL / 100)}</td>
  <td><a href="{escape(r["sources"][0]["url"])}" target="_blank" rel="noopener">Official page</a></td>
</tr>"""

    # fully insured 1.25M plans
    top5 = [r for r in rows_verified][:5]
    blended = sum(tier_apy(r, 250000) for r in top5) / 5
    plan_single = growth(MAX_COVERED, rows_verified[0]["apy"], 1) - MAX_COVERED
    plan_five = sum(growth(250000, tier_apy(r, 250000), 1) - 250000 for r in top5)

    plan_rows = ""
    for label, apy, amount in [
        (f"Single bank POD, 5 beneficiaries — {escape(BANKS[rows_verified[0]['bank_id']]['brand'])}", rows_verified[0]["apy"], MAX_COVERED),
    ]:
        plan_rows += (
            f"<tr><td>{label}</td><td class='num'>{money(amount)}</td><td class='num'>{pct(apy)}</td>"
            f"<td class='num'>{money(growth(amount, apy, 1) - amount)}</td>"
            f"<td class='num'>{money(growth(amount, apy, 3) - amount)}</td>"
            f"<td class='num'>{money(growth(amount, apy, 5) - amount)}</td>"
            f"<td><a href='{escape(rows_verified[0]['sources'][0]['url'])}' target='_blank' rel='noopener'>Rate</a><br>"
            f"<a href='https://www.fdic.gov/resources/deposit-insurance/financial-products-insured' target='_blank' rel='noopener'>FDIC trust rule</a></td></tr>"
        )
    plan_rows += (
        f"<tr><td>Five banks, $250,000 each — {', '.join(escape(BANKS[r['bank_id']]['brand']) for r in top5)}</td><td class='num'>{money(MAX_COVERED)}</td>"
        f"<td class='num'>{pct(blended)}</td><td class='num'>{money(plan_five)}</td>"
        f"<td class='num'>{money(sum(growth(250000, tier_apy(r, 250000), 3) - 250000 for r in top5))}</td>"
        f"<td class='num'>{money(sum(growth(250000, tier_apy(r, 250000), 5) - 250000 for r in top5))}</td>"
        f"<td><a href='{escape(top5[0]['sources'][0]['url'])}' target='_blank' rel='noopener'>Top rate</a><br>"
        f"<a href='https://www.fdic.gov/resources/deposit-insurance/faq' target='_blank' rel='noopener'>FDIC $250k rule</a></td></tr>"
    )

    body = f"""
<p class="lede">What a deposit actually earns at the size you are planning. All figures are arithmetic on the
APY the bank printed — no projections, no assumptions about future rate moves. A {OPEN_DATE} opening is assumed;
year 1 ends {OPEN_DATE[:4]}-10-23 of the following year.</p>

<div class="callout">
  <strong>Formula used:</strong> balance = deposit × (1 + APY)<sup>years</sup>, interest = balance − deposit.
  The FDIC requires advertised APY to reflect compounding, so this reproduces a bank's own annual disclosure
  while holding the rate constant. Variable-rate accounts will not hold the rate for 3 or 5 years; those columns
  show what the same rate would produce, not a forecast.
</div>

<section class="section">
  <h2>Best verified rate by deposit size</h2>
  <div class="table-scroll">
  <table class="table">
    <thead><tr>
      <th class="num">Deposit</th><th>Best verified account</th><th class="num">APY</th>
      <th class="num">Year-1 interest</th><th class="num">3-yr interest</th>
      <th class="num">5-yr interest</th><th class="num">Extra vs national rate (yr 1)</th><th>Rate source</th>
    </tr></thead>
    <tbody>{best_rows}</tbody>
  </table>
  </div>
  <p class="note">"National rate" is the FDIC national savings rate of {pct(NATIONAL)} effective
  {META['fdic_national_rate_effective']}. Deposits above $250,000 are only fully insured with the
  structures on the <a href="fdic-insurance.html">FDIC Coverage page</a>.</p>
</section>

<section class="section">
  <h2>Full $1.25M, fully insured</h2>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th>Structure</th><th class="num">Insured</th><th class="num">APY</th>
    <th class="num">Year-1 interest</th><th class="num">3-yr interest</th><th class="num">5-yr interest</th><th>Sources</th></tr></thead>
    <tbody>{plan_rows}</tbody>
  </table>
  </div>
  <p class="note">Included in the five-bank split: {', '.join(escape(BANKS[r['bank_id']]['brand']) for r in top5)}.
  U.S. Bank's 3.50% tier requires a U.S. Bank checking/debit relationship, so that leg carries a condition the
  others do not.</p>
  <p class="note">The single-bank route beats the five-bank split by {money(plan_single - plan_five)} in year 1
  purely because the whole balance sits at the top rate. It depends on the bank accepting five POD
  beneficiaries — confirm that first.</p>
</section>

<section class="section">
  {tables}
</section>
"""
    return page(
        "Return on Deposit",
        "Interest and ending balances for deposits from $10,000 to $1,250,000 at every verified APY, for 1, 3 and 5 years.",
        body,
        "returns.html",
    )


# ----------------------------------------------------------------------------- FDIC page
def build_fdic():
    structures = ""
    for s in FDIC["structures"]:
        structures += (
            f"<tr><td>{escape(s['structure'])}<span class='cell-sub'>{escape(s['formula'])}</span></td>"
            f"<td class='num strong'>{money(s['coverage'])}</td>"
            f"<td><a href='{escape(s['source'])}' target='_blank' rel='noopener'>FDIC</a></td></tr>"
        )

    bank_rows = ""
    for r in sorted(ROWS, key=lambda x: -(x.get("apy") or 0)):
        b = BANKS[r["bank_id"]]
        cert = b.get("fdic_cert") or '<span class="blank">not captured</span>'
        cap = 250000
        bank_rows += f"""<tr>
  <td><strong>{escape(b["brand"])}</strong><span class="cell-sub">{escape(b["legal_name"])}</span></td>
  <td class="num">{escape(cert)}</td>
  <td>{badge(b.get("verified", False), "Confirmed in FDIC API", "Not confirmed")}</td>
  <td class="num">{money(cap)}</td>
  <td class="num">{money(cap * 2)}<span class="cell-sub">joint, 2 owners</span></td>
  <td class="num">{money(MAX_COVERED)}<span class="cell-sub">POD, 5 beneficiaries</span></td>
  <td><a href="{escape(b['fdic_bankfind'])}" target="_blank" rel="noopener">BankFind</a></td>
</tr>"""

    flagged_cert = [b for b in BANKS.values() if not b.get("fdic_cert")]
    cert_note = ""
    if flagged_cert:
        names = ", ".join(escape(b["brand"]) for b in flagged_cert)
        cert_note = (
            f'<p class="note"><strong>Certificate numbers not captured:</strong> {names}. '
            f'Their coverage is advertised by the bank but the FDIC record was not retrieved here; '
            f'see <a href="flagged.html">Flagged for Review</a>. Do not treat the number as confirmed.</p>'
        )

    rules = "".join(f"<li>{escape(x)}</li>" for x in FDIC["insurance"]["covered_products"])
    not_covered = "".join(f"<li>{escape(x)}</li>" for x in FDIC["insurance"]["not_covered"])

    body = f"""
<p class="lede">The requirement was "max FDIC insurance". That is set at <strong>$250,000 per depositor, per
FDIC-insured bank, per ownership category</strong>, and it is automatic once the money sits in a deposit
account at an FDIC-insured bank. What changes is how many <em>ownership categories</em> you use.</p>

<section class="grid cards">
  <div class="card"><span class="label">Per depositor, per bank</span><span class="big">$250,000</span>
    <span class="muted">Single-owner savings account</span></div>
  <div class="card"><span class="label">Joint account, 2 owners</span><span class="big">$500,000</span>
    <span class="muted">$250,000 per co-owner</span></div>
  <div class="card"><span class="label">POD with 5 beneficiaries</span><span class="big">$1,250,000</span>
    <span class="muted">Capped at $1,250,000 per owner</span></div>
  <div class="card"><span class="label">Five separate banks</span><span class="big">$1,250,000</span>
    <span class="muted">$250,000 single-owner each</span></div>
</section>

<section class="section">
  <h2>Coverage by ownership structure</h2>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th>Structure</th><th class="num">Insured amount</th><th>Source</th></tr></thead>
    <tbody>{structures}</tbody>
  </table>
  </div>
  <p class="note">The trust formula is quoted directly from the FDIC:
  <em>"# of Owners × # of Beneficiaries × $250,000 = Amount Insured (not to exceed $1,250,000 per owner for
  all trust accounts)"</em>. Whether a specific bank will let you name five POD beneficiaries on its savings
  account is a bank-level question and is not assumed here.</p>
</section>

<section class="section">
  <h2>Per-bank coverage capacity</h2>
  <p class="note">Bank identity comes from the FDIC's own institution records; certificate numbers below were
  returned by the FDIC API during this session unless marked otherwise.</p>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th>Bank</th><th class="num">FDIC cert</th><th>FDIC record</th>
    <th class="num">Single</th><th class="num">Joint</th><th class="num">Trust</th><th>Verify</th></tr></thead>
    <tbody>{bank_rows}</tbody>
  </table>
  </div>
  {cert_note}
</section>

<section class="section">
  <h2>Why splitting across five banks is harder than it looks</h2>
  <ul class="list">
    <li><strong>Interest drifts you over the limit.</strong> Coverage is principal plus interest through the
        date of failure, so a balance parked at exactly $250,000 will grow past the cap. Leave headroom or
        sweep interest out.</li>
    <li><strong>Brands are not banks.</strong> Capital One and Discover count as one bank for coverage from
        May 18, 2025 onward, per Capital One's own page. The FDIC record for Discover Bank shows it as
        inactive. Two logos can be one $250,000 limit.</li>
    <li><strong>Network programs have their own terms.</strong> SoFi advertises coverage up to $3M "through a
        network of participating banks". That is a sweep arrangement, not a single-bank limit, and it carries
        program risk that a POD account at one bank does not.</li>
    <li><strong>Ownership category is the real lever.</strong> A single-owner savings account, an IRA, a joint
        account and a POD account at the same bank are separate categories — they can stack at one bank.</li>
  </ul>
</section>

<section class="section">
  <h2>What FDIC insurance does and does not cover</h2>
  <div class="grid two">
    <div class="panel"><h3>Covered</h3><ul class="list">{rules}</ul></div>
    <div class="panel"><h3>Not covered</h3><ul class="list">{not_covered}</ul></div>
  </div>
  <p class="note">Verify any specific balance with the FDIC's own calculator,
  <a href="{escape(FDIC['insurance']['edie'])}" target="_blank" rel="noopener">EDIE</a>, and confirm the
  institution in <a href="{escape(FDIC['insurance']['bankfind'])}" target="_blank" rel="noopener">BankFind</a>.</p>
</section>
"""
    return page(
        "FDIC Coverage",
        "How the $250,000 limit actually works, which structures reach $1,250,000, and the FDIC record for every bank reviewed.",
        body,
        "fdic-insurance.html",
    )


# ----------------------------------------------------------------------------- bonuses page
def build_bonuses():
    rows = ""
    extra_rows = ""
    for r in ROWS:
        for p in r.get("promos", []):
            rows += f"""<tr>
  <td><strong>{escape(BANKS[r["bank_id"]]["brand"])}</strong><span class="cell-sub">{escape(r["product"])}</span></td>
  <td><strong>{escape(p["title"])}</strong><span class="cell-sub">{escape(p["detail"])}</span></td>
  <td><a href="{escape(p["source"])}" target="_blank" rel="noopener">Official terms</a></td>
</tr>"""

    # priced promotions
    chase = next(r for r in ROWS if r["id"] == "chase-savings")
    chase_bonus = 200
    chase_dep = 10000
    chase_hold_days = 90
    chase_apy = None  # deliberately not priced: rate unverified
    wf = next(r for r in ROWS if r["id"] == "wellsfargo-platinum-promo")
    wf_promo_apy = tier_apy(wf, 25000)
    wf_base_apy = 0.01
    wf_dep = 25000
    wf_extra = wf_dep * (wf_promo_apy - wf_base_apy) / 100 * 0.25  # only guaranteed for one quarter-ish? no - use 1 year
    wf_extra_year = wf_dep * (wf_promo_apy - wf_base_apy) / 100
    sofi = next(r for r in ROWS if r["id"] == "sofi-savings")
    sofi_boost = 1.10
    sofi_base = sofi["apy"]
    sofi_dep = 10000
    sofi_boost_val = sofi_dep * sofi_boost / 100 * 0.5
    marcus = next(r for r in ROWS if r["id"] == "marcus-osa")
    marcus_boost = 1.00
    marcus_dep = 10000
    marcus_boost_val = marcus_dep * marcus_boost / 100 * 0.25

    extra_rows = f"""
<tr>
  <td><strong>Chase</strong><span class="cell-sub">Chase Savings, $200 tier</span></td>
  <td>{money(chase_dep)} for 90 days</td>
  <td class="num strong">{money(chase_bonus)}</td>
  <td class="num">{pct(chase_bonus / chase_dep * 100 * 365 / chase_hold_days)}<span class="cell-sub">annualised on the hold</span></td>
  <td>Equivalent to about {pct(chase_bonus / chase_dep * 100)} on the deposit. Chase's savings APY was not
      verified, so the base interest is not included.</td>
  <td><a href="https://account.chase.com/consumer/banking/savingsoffer" target="_blank" rel="noopener">Chase offer</a></td>
</tr>
<tr>
  <td><strong>Wells Fargo</strong><span class="cell-sub">Platinum Savings promo tier</span></td>
  <td>{money(wf_dep)} at {pct(wf_promo_apy)} instead of {pct(wf_base_apy)}</td>
  <td class="num strong">{money(wf_extra_year)}</td>
  <td class="num">{pct(wf_promo_apy - wf_base_apy)}<span class="cell-sub">APY uplift</span></td>
  <td>Extra interest in year 1 versus the standard rate, if the promotional rate held for a full year. It is
      variable, so it may not.</td>
  <td><a href="https://www.wellsfargo.com/savings-cds/rates/" target="_blank" rel="noopener">Wells Fargo rates</a></td>
</tr>
<tr>
  <td><strong>SoFi</strong><span class="cell-sub">+1.10% direct-deposit boost</span></td>
  <td>{money(sofi_dep)} at {pct(sofi_base + sofi_boost)} instead of {pct(sofi_base)}</td>
  <td class="num strong">{money(sofi_boost_val)}</td>
  <td class="num">{pct(sofi_boost)}<span class="cell-sub">for 6 months</span></td>
  <td>Boost is capped at six months. Cash bonus of $50 or $400 is separate.</td>
  <td><a href="https://www.sofi.com/banking/high-yield-savings-account/" target="_blank" rel="noopener">SoFi terms</a></td>
</tr>
<tr>
  <td><strong>Marcus</strong><span class="cell-sub">Referral +1.00%</span></td>
  <td>{money(marcus_dep)} for 3 months</td>
  <td class="num strong">{money(marcus_boost_val)}</td>
  <td class="num">{pct(marcus_boost)}<span class="cell-sub">for 3 months</span></td>
  <td>Marcus' own example: one referral in a year lifts the effective APY to 3.75%.</td>
  <td><a href="https://www.marcus.com/us/en/savings/referrals#termsandconditions" target="_blank" rel="noopener">Marcus terms</a></td>
</tr>
"""

    body = f"""
<p class="lede">Every promotion found on an official bank page, with its qualifying rules transcribed. A
promotion counts only when the bank's own page states it — "no bonus found" means nothing was on the account
page when it was captured, not that no bonus exists.</p>

<section class="section">
  <h2>Promotions and their rules</h2>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th>Bank</th><th>Offer and rules</th><th>Source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
</section>

<section class="section">
  <h2>What the promotions are worth</h2>
  <p class="note">Priced against the deposit each offer requires. Cash bonuses and APY boosts are kept
  separate because a bonus is paid once while a boost lasts for a stated period.</p>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th>Bank / offer</th><th>Requirement</th><th class="num">Value</th>
    <th class="num">Rate equivalent</th><th>Notes</th><th>Source</th></tr></thead>
    <tbody>{extra_rows}</tbody>
  </table>
  </div>
</section>

<section class="section">
  <h2>Rules that void or reduce a bonus</h2>
  <ul class="list">
    <li><strong>Chase:</strong> not available to existing Chase savings customers, or accounts closed in the
        last 90 days, or closed with a negative balance in the last 3 years. Money must be <em>new</em> to
        Chase. Bonus determined on day 30; balance must be held 90 days from enrollment. Offer expires
        01/27/2027.</li>
    <li><strong>Wells Fargo:</strong> the 3.25% APY is for <em>new savings customers only</em> and requires
        $25,000+ deposited and maintained within 30 days. Below $25,000 the standard Platinum Savings rate is
        0.01%. The $12 monthly fee is waived only with a $3,500 daily balance.</li>
    <li><strong>SoFi:</strong> the +1.10% boost needs an eligible direct deposit set up within 60 days and
        maintained, and lasts up to six months. Opening a SoFi Savings account also opens a SoFi Checking
        account.</li>
    <li><strong>Marcus:</strong> the +1.00% runs three months; after that the standard APY applies.</li>
    <li><strong>Fees can eat a bonus.</strong> A $5 monthly fee on a $1,000 balance is 0.50% a year — larger
        than most of the APY differences on this site.</li>
  </ul>
</section>

<section class="section">
  <h2>Banks with no promotion found on the official page</h2>
  <p class="note">Bank of America, Citi, U.S. Bank, Truist, TD, Schwab, Ally, American Express and Capital One
  had no savings sign-up bonus or APY promotion on the pages captured. Capital One, American Express and Wells
  Fargo do publish CD specials; those are fixed-rate products, listed on the
  <a href="rates-competitiveness.html">rate check page</a>. Absence of a promotion on one captured page is not
  proof none exists — promotional offers are frequently targeted.</p>
</section>
"""
    return page(
        "Bonuses & Promotions",
        "Sign-up bonuses and APY boosts found on official bank pages, their qualifying rules, and what each is actually worth.",
        body,
        "bonuses.html",
    )


# ----------------------------------------------------------------------------- competitiveness
def build_competitiveness():
    rows = ""
    ranked = sorted(verified_rows(), key=lambda r: -tier_apy(r, 250000))
    for i, r in enumerate(ranked, 1):
        apy = tier_apy(r, 250000)
        multiple = apy / NATIONAL if NATIONAL else None
        rows += f"""<tr>
  <td class="num">{i}</td>
  <td><strong>{escape(BANKS[r["bank_id"]]["brand"])}</strong><span class="cell-sub">{escape(r["product"])}</span></td>
  <td class="num strong">{pct(apy)}</td>
  <td class="num">{multiple:.1f}×</td>
  <td class="num">{money(250000 * apy / 100)}</td>
  <td class="num">{money(250000 * apy / 100 - 250000 * NATIONAL / 100)}</td>
  <td class="num">{money(250000 * ((1 + apy / 100) ** 5 - (1 + NATIONAL / 100) ** 5))}</td>
  <td><a href="{escape(r["sources"][0]["url"])}" target="_blank" rel="noopener">Official page</a></td>
</tr>"""

    unverified = [r for r in ROWS if r.get("apy") is None]
    unv_rows = "".join(
        f"<tr><td><strong>{escape(BANKS[r['bank_id']]['brand'])}</strong></td>"
        f"<td>{escape(r['product'])}</td><td class='blank'>blank</td>"
        f"<td>{escape(r['apy_as_of_text'])}</td>"
        f"<td><a href='{escape(r['sources'][1]['url'] if len(r['sources']) > 1 else r['sources'][0]['url'])}' "
        f"target='_blank' rel='noopener'>Official page</a></td></tr>"
        for r in unverified
    )

    cds = [
        ("Bank of America", "7-month Featured CD", "3.75% APY under $100,000; 4.00% APY at $100,000+", "$1,000",
         "https://media.bac-assets.com/DigitalDeposit_NY_NY_Tri_State_Area.pdf"),
        ("Wells Fargo", "4-month Special Fixed Rate CD", "3.49% APY standard; 3.75% relationship APY", "not captured",
         "https://www.wellsfargo.com/savings-cds/rates/"),
        ("Capital One", "360 CD (up to 60 months)", "up to 4.40% APY, fixed", "no minimum balance",
         "https://www.capitalone.com/bank/open-an-account/"),
        ("American Express", "CD (terms up to 5 years)", "up to 4.40% APY, fixed", "not captured",
         "https://www.americanexpress.com/en-us/banking/online-savings/account/"),
    ]
    cd_rows = "".join(
        f"<tr><td><strong>{escape(b)}</strong></td><td>{escape(p)}</td><td>{escape(a)}</td>"
        f"<td>{escape(m)}</td><td><a href='{escape(u)}' target='_blank' rel='noopener'>Official page</a></td></tr>"
        for b, p, a, m, u in cds
    )

    body = f"""
<p class="lede">APY on its own says nothing. This page measures each verified rate against the FDIC's published
national savings rate of <strong>{pct(NATIONAL)}</strong> (effective {META['fdic_national_rate_effective']}) and
prices the gap over the life of the deposit.</p>

<div class="callout">
  <strong>Benchmark definition.</strong> The FDIC national rate is the deposit-weighted average of rates paid by
  all insured institutions — the official version of "what a savings account pays". Source:
  <a href="{escape(META['fdic_national_rate_source'])}" target="_blank" rel="noopener">FDIC National Rates and
  Rate Caps, October 2026</a>. Savings rates there are based on the $2,500 product tier.
</div>

<section class="section">
  <h2>Every verified rate against the benchmark</h2>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th class="num">#</th><th>Account</th><th class="num">APY at $250k</th>
    <th class="num">vs national</th><th class="num">Interest / yr</th>
    <th class="num">Extra vs national / yr</th><th class="num">Extra over 5 yrs</th><th>Rate source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
</section>

<section class="section">
  <h2>How to read the life of the deposit</h2>
  <div class="grid two">
    <div class="panel">
      <h3>Why a 1-year view flatters branch banks</h3>
      <p class="muted">A 0.01% and a 3.55% APY differ by $3.54 per $1,000 per year. Held five years the gap
      compounds: $1,000 grows to $1,000.05 at 0.01% but $1,190.34 at 3.55% — a $190 difference on a $1,000
      deposit. The longer the horizon, the more the rate matters and the less the sign-up bonus does.</p>
    </div>
    <div class="panel">
      <h3>Why a 5-year view overstates a savings account</h3>
      <p class="muted">Every account in the returns tables is <strong>variable</strong>. None of these banks
      promises {pct(ranked[0]['apy'])} for five years. Only a CD locks a rate, and the CD rates found on
      official pages are listed below so the trade-off is visible.</p>
    </div>
  </div>
  <p class="note">Break-even against a bonus: a $200 one-time bonus equals one year of the rate gap on about
  {money(200 / ((ranked[0]['apy'] - NATIONAL) / 100))} at {pct(ranked[0]['apy'])} versus {pct(NATIONAL)}. Above
  that balance the APY dominates; below it, take the bonus.</p>
</section>

<section class="section">
  <h2>Fixed-rate alternatives at the same banks (context only)</h2>
  <p class="note">These are CDs, not savings accounts — the money is locked for the term and early withdrawal
  carries a penalty. They are listed because they beat most of the savings APYs above, and the requirement was
  the highest return consistent with full FDIC coverage.</p>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th>Bank</th><th>Product</th><th>APY</th><th>Minimum</th><th>Source</th></tr></thead>
    <tbody>{cd_rows}</tbody>
  </table>
  </div>
</section>

<section class="section">
  <h2>Rates that could not be benchmarked</h2>
  <p class="note">These accounts are real and reviewed, but no official page printed a rate during this session,
  so they are excluded from every comparison rather than estimated.</p>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th>Bank</th><th>Account</th><th class="num">APY</th><th>Why blank</th><th>Source</th></tr></thead>
    <tbody>{unv_rows}</tbody>
  </table>
  </div>
</section>
"""
    return page(
        "Rate Competitiveness",
        "Each verified APY measured against the FDIC national savings rate, priced over 1, 3 and 5 years, with fixed-rate CDs for context.",
        body,
        "rates-competitiveness.html",
    )


# ----------------------------------------------------------------------------- security page
def build_security():
    rows = ""
    for r in SECURITY["rows"]:
        b = BANKS.get(r["bank_id"])
        if not b:
            continue
        app_badge = badge("Verified" in r["app_status"], "App verified", "App not verified")
        rows += f"""<tr>
  <td><strong>{escape(b["brand"])}</strong><span class="cell-sub">{escape(b["legal_name"])}</span></td>
  <td>{escape(r["app"]) or '<span class="blank">blank</span>'}<span class="cell-sub">{app_badge}</span></td>
  <td>{escape(r["security"])}</td>
  <td>{escape(r["two_factor"]) or '<span class="blank">blank</span>'}</td>
  <td>{escape(r["notes"])}</td>
  <td><a href="{escape(r["source"])}" target="_blank" rel="noopener">Official page</a></td>
</tr>"""

    body = f"""
<p class="lede">{escape(SECURITY["intro"])}</p>

<div class="callout">
  <strong>What is not claimed here.</strong> No bank's multi-factor authentication, passkey support or
  device-binding behaviour was tested or verified in this session. Those cells are blank on purpose. The
  "App" column only records that the bank's own page describes a mobile app; the app stores were not opened.
</div>

<section class="section">
  <h2>App and security posture, as printed by each bank</h2>
  <div class="table-scroll">
  <table class="table wide">
    <thead><tr><th>Bank</th><th>Mobile app</th><th>Security statement on the official page</th>
    <th>2FA / passkeys</th><th>Notes</th><th>Source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
</section>

<section class="section">
  <h2>The security questions that actually matter for a large insured balance</h2>
  <ul class="list">
    <li><strong>Deposit insurance is the real backstop.</strong> A bank's app security protects your access; the
        FDIC protects the balance if the bank fails. Both matter, and they are not substitutes.</li>
    <li><strong>Check the certificate, not the logo.</strong> Every bank here is checked against FDIC institution
        records; two brands can share one certificate, and one inactive record (Discover Bank) is excluded from
        the returns tables.</li>
    <li><strong>Turn on the strongest login the bank offers.</strong> Where a bank publishes a security
        guarantee (Ally publishes an online and mobile security guarantee), read its conditions before relying
        on reimbursement.</li>
    <li><strong>Prefer push or app-based approval over SMS.</strong> This is general guidance, not a claim about
        any specific bank on this page.</li>
    <li><strong>Verify transfers out.</strong> Every account here allows external transfers. A large balance in a
        single-bank savings account is reachable by anyone who gets account access.</li>
  </ul>
</section>
"""
    return page(
        "App & Security",
        "Which banks publish a mobile app and a security statement, transcribed from their own pages — with unverified controls left blank.",
        body,
        "security-apps.html",
    )


# ----------------------------------------------------------------------------- flagged page
def build_flagged():
    order = {"High": 0, "Medium": 1, "Low": 2}
    items = sorted(FLAGGED["items"], key=lambda x: (order.get(x["severity"], 3), x["id"]))
    rows = ""
    for f in items:
        sev_cls = {"High": "sev-high", "Medium": "sev-med", "Low": "sev-low"}.get(f["severity"], "")
        rows += f"""<tr id="{escape(f['id'])}">
  <td><span class="sev {sev_cls}">{escape(f["severity"])}</span><span class="cell-sub">{escape(f["id"])}</span></td>
  <td><strong>{escape(f["topic"])}</strong><span class="cell-sub">{escape(f["detail"])}</span></td>
  <td>{escape(f["value_used"]) or '—'}</td>
  <td>{escape(f["value_not_used"]) or '—'}</td>
  <td>{escape(f["action"])}</td>
  <td><a href="{escape(f["source"])}" target="_blank" rel="noopener">Official source</a></td>
</tr>"""

    high = len([f for f in items if f["severity"] == "High"])
    med = len([f for f in items if f["severity"] == "Medium"])
    low = len([f for f in items if f["severity"] == "Low"])

    body = f"""
<p class="lede">Nothing on this site was invented to fill a gap. Where an official source would not give up a
number, the number is blank and the reason is recorded here with a link. These items do not block anything —
they are the list to review after the site is live.</p>

<div class="statline">
  <span><strong>{high}</strong> high</span>
  <span><strong>{med}</strong> medium</span>
  <span><strong>{low}</strong> low</span>
  <span><strong>{len(items)}</strong> total</span>
</div>

<section class="section">
  <div class="table-scroll">
  <table class="table wide">
    <thead><tr><th>Severity</th><th>Issue</th><th>Value used here</th>
    <th>Value deliberately not used</th><th>What to do</th><th>Source</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  </div>
</section>

<section class="section">
  <h2>Patterns worth knowing about</h2>
  <ul class="list">
    <li><strong>The biggest banks hide rates behind a ZIP code.</strong> Chase, Citi, TD and Bank of America all
        render rates client-side or per location. That is a marketing choice, not a data gap on this side — and
        it is why those banks' APY cells are blank while their fees and rules are fully transcribed.</li>
    <li><strong>Marketing pages contain template and arithmetic defects.</strong> Bank of America printed
        "$XXXX" as a fee, Capital One printed "NaN APY", and Synchrony printed both 3.55% and 2.85% as its own
        APY. None of those defects were smoothed over.</li>
    <li><strong>Second-hand numbers on first-party pages are still second-hand.</strong> Bank comparison widgets
        quote competitor rates sourced from Curinos. They are not treated as verification for anything here.</li>
  </ul>
</section>
"""
    return page(
        "Flagged for Review",
        "Every value left blank, every contradiction between official pages, and every number that was not used.",
        body,
        "flagged.html",
    )


# ----------------------------------------------------------------------------- methodology
def build_method():
    body = f"""
<p class="lede">The rules this repository was built under, so the tables can be audited rather than trusted.</p>

<section class="section">
  <h2>Dates</h2>
  <table class="mini wide">
    <tr><td>Research capture date</td><td>{CAPTURE} (UTC)</td></tr>
    <tr><td>Assumed account opening date</td><td>{OPEN_DATE}</td></tr>
    <tr><td>FDIC national rate effective</td><td>{META["fdic_national_rate_effective"]}
        (<a href="{escape(META['fdic_national_rate_source'])}" target="_blank" rel="noopener">FDIC source</a>)</td></tr>
    <tr><td>Rates used</td><td>The rate printed on the bank's page at capture, with the bank's own "as of" date
        recorded beside it. Where the bank printed no date, the cell says "not printed".</td></tr>
    <tr><td>Sources for the rows above</td><td>
        <a href="{escape(META['fdic_national_rate_source'])}" target="_blank" rel="noopener">FDIC National Rates</a> ·
        <a href="data/meta.json">data/meta.json</a></td></tr>
  </table>
</section>

<section class="section">
  <h2>Inclusion rules</h2>
  <ul class="list">
    <li><strong>Large national banks first.</strong> The list covers the largest branch networks (Chase, Bank of
        America, Wells Fargo, Citibank, U.S. Bank, PNC, Truist, TD, Fifth Third, Citizens) plus national
        digital banks that are themselves FDIC-insured and app-first (Capital One, Ally, American Express,
        Marcus/Goldman Sachs, Synchrony, SoFi, Schwab). Small local banks and credit unions are out of scope by
        request.</li>
    <li><strong>Every bank must be an FDIC-insured institution.</strong> Confirmed through FDIC institution
        records, not the bank's marketing.</li>
    <li><strong>A rate row needs a number from the bank.</strong> If the bank would not print it, the row keeps
        its fees and rules but the APY is blank.</li>
    <li><strong>No aggregators.</strong> NerdWallet, Bankrate, Forbes, depositaccounts and similar were not used
        as sources for any value on this site, even where they agree with the numbers shown.</li>
  </ul>
</section>

<section class="section">
  <h2>Arithmetic</h2>
  <table class="mini wide">
    <tr><td>Ending balance</td><td>deposit × (1 + APY / 100)<sup>years</sup>
        (<a href="https://www.fdic.gov/resources/deposit-insurance/faq" target="_blank" rel="noopener">APY definition</a>)</td></tr>
    <tr><td>Interest</td><td>ending balance − deposit</td></tr>
    <tr><td>Annual interest (displayed)</td><td>deposit × APY / 100</td></tr>
    <tr><td>Tier selection</td><td>The highest tier whose minimum balance is at or below the deposit
        (<a href="https://www.usbank.com/bank-accounts/savings-accounts/bank-smartly-savings/savings-account-interest-rates.html" target="_blank" rel="noopener">tiered example</a>)</td></tr>
    <tr><td>Benchmark</td><td>FDIC national savings rate {pct(NATIONAL)}, effective {META["fdic_national_rate_effective"]}
        (<a href="{escape(META['fdic_national_rate_source'])}" target="_blank" rel="noopener">FDIC source</a>)</td></tr>
    <tr><td>Annualised bonus equivalent</td><td>bonus ÷ deposit × 365 ÷ required holding days
        (<a href="https://account.chase.com/consumer/banking/savingsoffer" target="_blank" rel="noopener">example offer</a>)</td></tr>
  </table>
  <p class="note">APY is required to reflect compounding, so (1 + APY) is the correct one-year factor for a
  lump sum. Holding the same APY for N years is a <em>model</em>: every account on this site is variable-rate
  except the CDs in the context table.</p>
</section>

<section class="section">
  <h2>Limits of this research</h2>
  <ul class="list">
    <li>Rates were read from public pages, not from inside an authenticated account. A logged-in customer may
        see a different, personalised rate — U.S. Bank and TD both say so explicitly.</li>
    <li>Rate pages that require a ZIP code or client-side rendering may show different values for a New York
        address than the ones captured. Those cases are flagged.</li>
    <li>APYs are variable unless labelled fixed. Nothing here forecasts where rates go.</li>
    <li>Tax is not modelled. Interest is taxable income in the year it is credited.</li>
    <li>Account-opening identity requirements, funding windows and bonus eligibility were transcribed where the
        bank printed them; they were not tested by opening an account.</li>
  </ul>
</section>

<section class="section">
  <h2>Reproducing the site</h2>
  <p class="note">The pages are generated, not hand-edited: <code>python3 scripts/build_site.py</code> reads
  <code>data/*.json</code> and rewrites the HTML. Every fact lives in the JSON with its source URL, so a change
  to a rate is one edit and one rebuild.</p>
</section>
"""
    return page(
        "Methodology",
        "Dates, inclusion rules, the exact arithmetic, and the limits of what was verified.",
        body,
        "methodology.html",
    )


# ----------------------------------------------------------------------------- sources
def build_sources():
    blocks = ""
    for g in SOURCES["groups"]:
        items = "".join(
            f"<tr><td><a href='{escape(i['url'])}' target='_blank' rel='noopener'>{escape(i['label'])}</a></td>"
            f"<td>{escape(i['used_for'])}</td></tr>"
            for i in g["items"]
        )
        blocks += f"""
<section class="section">
  <h2>{escape(g["group"])}</h2>
  <div class="table-scroll">
  <table class="table">
    <thead><tr><th>Source</th><th>Used for</th></tr></thead>
    <tbody>{items}</tbody>
  </table>
  </div>
</section>
"""

    body = f"""
<p class="lede">Every link below was opened during the {CAPTURE} session. Government sources first, then each
bank's own pages. Third-party rate aggregators are deliberately absent.</p>
{blocks}
"""
    return page(
        "Sources",
        "The official pages behind every number on this site, grouped by publisher.",
        body,
        "sources.html",
    )


# ----------------------------------------------------------------------------- write
PAGES = {
    "index.html": build_index,
    "accounts.html": build_accounts,
    "returns.html": build_returns,
    "fdic-insurance.html": build_fdic,
    "bonuses.html": build_bonuses,
    "rates-competitiveness.html": build_competitiveness,
    "security-apps.html": build_security,
    "flagged.html": build_flagged,
    "methodology.html": build_method,
    "sources.html": build_sources,
}

if __name__ == "__main__":
    for name, fn in PAGES.items():
        with open(os.path.join(ROOT, name), "w") as f:
            f.write(fn())
        print("wrote", name)
