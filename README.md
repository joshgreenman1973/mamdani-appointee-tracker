# Mamdani administration personnel tracker

A two-column searchable feed of senior and mid-level political (non-civil-service)
appointees brought into the Mamdani administration since Jan. 1, 2026 — **Added**
on the left with name, title and salary in green — and those who have left on the
right (**Departed**).

## Run it locally

```
cd mamdani-appointee-tracker
python3 -m http.server 8147
# open http://localhost:8147
```

`index.html` reads `data.json` at load, so it must be served over http (not opened
as a `file://`).

## Files

- `index.html` — the dual-feed interface (search, filter by area, filter new vs. retained, sort by date/name/salary).
- `data.json` — the dataset. `appointees[]` and `departed[]`. Edit this to update.
- `refresh.py` — weekly helper that surfaces new personnel press releases to review.

## Who is included

Mayoral and agency political appointees in the civil-service **exempt class**:
deputy mayors, commissioners, agency heads, chiefs, senior advisors, press and
policy staff, and board appointees. Rank-and-file civil servants — police
officers, firefighters, sanitation workers, public school teachers — are excluded
by design.

`status` is `"new"` (brought in by Mamdani) or `"retained"` (kept on from the
Adams administration). The departed list includes Adams-era holdovers who left as
the administration changed.

## Salaries

A green dollar figure appears **only** where the city publishes an official base
salary for that title (the Quadrennial Advisory Commission's *Select New York City
Mayoral Appointees* schedule — e.g. First Deputy Mayor $256,819; Police, Fire,
Health commissioners and Corporation Counsel $214,413). Everyone else reads
"salary not yet disclosed" until they surface in the **Citywide Payroll** dataset
on NYC Open Data, which lags by fiscal year. **No salary is estimated or invented.**

To backfill salaries later, pull from the Citywide Payroll dataset
(`k397-673e` on data.cityofnewyork.us) once FY2026 records post, matching by name
and agency.

## Keeping it current

Run the helper weekly:

```
python3 refresh.py
```

It scans the Mayor's Office news index for appointment/resignation releases newer
than `meta.lastUpdated`, prints candidate URLs, and leaves the editing to a human
so nothing unsourced is added. After verifying a release, add a source-linked
entry to `data.json` and bump `meta.lastUpdated`.

Sources beyond the Mayor's Office to watch: City & State New York's "Who's who"
roster, Politico New York Playbook, The City, and Gothamist.

## Seed sources

Mayor's Office press releases (nyc.gov), City & State New York, FOX 5 New York,
and the New York Building Congress administration tracker. Each entry links to its
own source.
