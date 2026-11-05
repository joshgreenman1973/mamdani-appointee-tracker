#!/usr/bin/env python3
"""
Refresh helper for the Mamdani appointee tracker.

Every nyc.gov path 403s to curl, to urllib and to WebFetch, and the news index
is JS-rendered besides, so this script cannot fetch the listing itself. What it
can do is hand you the exact one-shot query to run, already scoped to the window
you have not checked yet, plus the roster to diff the answer against.

The listing is backed by a plain JSON endpoint, /bin/nyc/articlesearch.json,
which takes a date range and a page size. One call replaces the old routine of
clicking "Show 10 more results" until the page reached the date you needed.

Usage:  python3 refresh.py
"""
import json, datetime
from pathlib import Path

DATA = Path(__file__).with_name("data.json")

# Headlines that carry a personnel move. Roughly four in five releases are
# transcripts, executive orders and program announcements; these are the rest.
PATTERN = r"appoint|nominat|names |sworn|resign|steps down|departs|chief |commissioner of|director of|acting |personnel|deputy mayor|chancellor|leadership"


def main():
    data = json.loads(DATA.read_text())
    since = data["meta"].get("lastUpdated", "2026-01-01")
    today = datetime.date.today().isoformat()

    print(f"Unchecked window: {since} to {today}")
    print(f"Roster: {len(data['appointees'])} appointees, {len(data['departed'])} departed\n")

    print("1. Open the news index in the in-app browser, which renders the page and")
    print("   carries a real session:\n")
    print("     https://www.nyc.gov/office-of-the-mayor/news.page\n")
    print("2. Run this from inside that page. Same origin, so no 403:\n")
    print(f"""(async () => {{
  const r = await fetch('/bin/nyc/articlesearch.json?pageSize=400&currentPage=1'
    + '&categories=&types=&fromDate={since}&toDate={today}');
  const j = await r.json();
  const re = /{PATTERN}/i;
  return {{ total: j.totalResults,
           hits: j.results.filter(x => re.test(x.title))
                          .map(x => x.articleDate + ' | ' + x.title + ' | ' + x.link) }};
}})()\n""")
    print("3. Open each hit, confirm name, title, agency and date against the release,")
    print("   and append a source-linked entry to appointees[] or departed[].")
    print("   Salary stays null unless the Quadrennial schedule publishes one for that")
    print("   title. Never estimate.\n")
    print("4. Bump meta.lastUpdated, then rebuild the org chart:")
    print("     cd ../mamdani-org-chart && python3 build.py\n")

    print("Sources that do NOT cover the gap, so you do not go looking:")
    print("  - City Record 'Changes in Personnel' (dg92-zbpx) stalled 2026-06-18;")
    print("    every other section of that dataset is current, so this is the")
    print("    section going unpublished, not the mirror going down. Re-check it.")
    print("  - The Green Book head list is a useful cross-check for agency heads")
    print("    but lags, and covers no one below the head of an agency.")
    print("  - The outside trackers (Building Congress, Fontas, City & State's")
    print("    who's-who) all trail this roster.")


if __name__ == "__main__":
    main()
