#!/usr/bin/env python3
"""
Weekly refresh helper for the Mamdani appointee tracker.

Cheap, no-API-key scan: pulls the NYC Mayor's Office news index and prints any
press releases whose URL/headline suggests a personnel move (appoint, name,
commissioner, deputy mayor, resign, etc.) published since data.json's
lastUpdated. It does NOT auto-edit data.json — it surfaces candidates for a
human (or Claude) to verify and append, so nothing unsourced slips in.

Usage:  python3 refresh.py
"""
import json, re, sys, urllib.request
from pathlib import Path

DATA = Path(__file__).with_name("data.json")
INDEX = "https://www.nyc.gov/office-of-the-mayor/news.page"
KEYWORDS = ("appoint", "names", "commissioner", "deputy-mayor", "deputy mayor",
            "chief", "resign", "steps-down", "departs", "leadership")

def main():
    meta = json.loads(DATA.read_text())["meta"]
    since = meta.get("lastUpdated", "2026-01-01")
    print(f"Scanning Mayor's Office news for personnel moves since {since}\n")
    try:
        req = urllib.request.Request(INDEX, headers={"User-Agent": "Mozilla/5.0"})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"Could not fetch index ({e}). Open {INDEX} manually.")
        sys.exit(1)

    links = set(re.findall(r'/mayors-office/news/[^\s"\'<>]+', html))
    hits = sorted(l for l in links if any(k in l.lower() for k in KEYWORDS))
    if not hits:
        print("No obvious personnel releases found in the index markup.")
        print(f"Check by hand: {INDEX}")
        return
    print(f"{len(hits)} candidate release(s) to review:\n")
    for l in hits:
        print("  https://www.nyc.gov" + l)
    print("\nNext: open each, confirm name/title/agency/date, add a source-linked")
    print("entry to data.json (appointees[] or departed[]), and bump meta.lastUpdated.")

if __name__ == "__main__":
    main()
