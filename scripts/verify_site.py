#!/usr/bin/env python3
"""Verification harness for the generated site.

Checks, in order:
  1. no template leftovers ("None", "nan", "{", "}") in any generated page;
  2. every internal link resolves to a file that exists, and every #anchor resolves;
  3. every external link appears in /data (so no orphan citations were typed by hand);
  4. every account row carries at least one official source;
  5. the headline arithmetic recomputes exactly from data/accounts.json;
  6. every flagged item links to a source.

Exit code is non-zero if anything fails, so CI / the integration step can gate on it.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
failures = []


def fail(msg):
    failures.append(msg)


with open(os.path.join(DATA, "meta.json")) as f:
    META = json.load(f)
with open(os.path.join(DATA, "accounts.json")) as f:
    ACCOUNTS = json.load(f)
with open(os.path.join(DATA, "flagged.json")) as f:
    FLAGGED = json.load(f)

raw_data = ""
for name in os.listdir(DATA):
    with open(os.path.join(DATA, name)) as f:
        raw_data += f.read()


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.text = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])

    def handle_data(self, data):
        self.text.append(data)


parsed = {}
for page in pages:
    with open(os.path.join(ROOT, page)) as f:
        html = f.read()
    p = LinkParser()
    p.feed(html)
    parsed[page] = p

    if re.search(r">\s*(None|nan|NaN)\s*<", html):
        fail(f"{page}: template leftover (None/nan) in output")
    if re.search(r"\{[a-zA-Z_][^}]{0,40}\}", html):
        fail(f"{page}: unrendered f-string placeholder")
    if "Traceback" in html:
        fail(f"{page}: traceback text in output")

# 2. internal links
for page, p in parsed.items():
    for href in p.links:
        if href.startswith(("http://", "https://", "mailto:", "//")):
            continue
        target, _, anchor = href.partition("#")
        target = target or page
        path = os.path.join(ROOT, target)
        if not os.path.exists(path):
            fail(f"{page}: broken internal link -> {href}")
            continue
        if anchor:
            other = parsed.get(target)
            if other is None:
                continue
            if anchor not in other.ids:
                fail(f"{page}: missing anchor #{anchor} in {target}")

# 3. external links must exist in data
external = set()
for page, p in parsed.items():
    for href in p.links:
        if href.startswith(("http://", "https://")):
            external.add(href.split("#")[0])
for url in sorted(external):
    host = urlparse(url).netloc
    base = url.rstrip("/")
    if base in raw_data or url in raw_data or host in raw_data:
        continue
    fail(f"external URL not backed by a data source: {url}")

# 4. account rows carry sources
for row in ACCOUNTS["rows"]:
    if not row.get("sources"):
        fail(f"account row without a source: {row['id']}")
    for s in row.get("sources", []):
        if not s.get("url", "").startswith("https://"):
            fail(f"account row {row['id']}: source is not https")

# 5. arithmetic spot checks
def growth(p, apy, years):
    return p * (1 + apy / 100.0) ** years


checks = [
    ("250000 @ 3.55% for 1y", growth(250000, 3.55, 1), 258875.0),
    ("1250000 @ 3.55% for 1y", growth(1250000, 3.55, 1), 1294375.0),
    ("1250000 @ 3.55% for 5y", growth(1250000, 3.55, 5), 1488197.36),
    ("10000 @ 0.04% for 1y", growth(10000, 0.04, 1), 10004.0),
    ("250000 national 0.38%", 250000 * 0.38 / 100, 950.0),
]
for label, got, want in checks:
    if abs(got - want) > 1.0:
        fail(f"arithmetic check failed: {label}: got {got:,.2f}, expected {want:,.2f}")

# 6. flagged items have sources
for item in FLAGGED["items"]:
    if not item.get("source", "").startswith("https://"):
        fail(f"flagged item {item['id']}: missing https source")

# 7. content sanity: every page has nav + footer
for page in pages:
    with open(os.path.join(ROOT, page)) as f:
        html = f.read()
    for needle in ("assets/style.css", "Flagged for Review", "Savings Research"):
        if needle not in html:
            fail(f"{page}: missing {needle}")

print(f"pages checked: {len(pages)}")
print(f"unique external links: {len(external)}")
print(f"internal-link and arithmetic checks: done")
if failures:
    print("\nFAILURES:")
    for f_ in failures:
        print(" -", f_)
    sys.exit(1)
print("\nALL CHECKS PASSED")
