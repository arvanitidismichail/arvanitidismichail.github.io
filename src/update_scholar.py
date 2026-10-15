#!/usr/bin/env python3
"""Fetch citations, h-index and i10-index from the Google Scholar profile,
write them to scholar.py, then rebuild both pages.

Scholar has no API, so this reads the public profile page. It works from a
normal home or office connection; Scholar may refuse automated requests from
servers. If it fails, edit scholar.py by hand instead.
"""
import datetime
import html
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
PROFILE = "https://scholar.google.com/citations?user=fHHpMb0AAAAJ&hl=en&cstart=0&pagesize=100"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")

# curl rather than urllib: it uses the system's certificates on every platform
page = subprocess.run(["curl", "-sL", "-A", UA, PROFILE],
                      capture_output=True, text=True, check=True).stdout

# the stats table: three rows (Citations, h-index, i10-index), the "All" column first
cells = re.findall(r'<td class="gsc_rsb_std">(\d+)</td>', page)
if len(cells) < 6:
    sys.exit("Could not read the metrics — Scholar may have asked for a CAPTCHA. "
             "Edit scholar.py by hand instead.")
cites, h, i10 = (int(cells[0]), int(cells[2]), int(cells[4]))
today = datetime.date.today().isoformat()

# citations per year: the bar chart's labels run oldest to newest, and each bar's
# z-index counts back from the newest year (1 = latest). Years with no
# citations have no bar.
years = [int(y) for y in re.findall(r'<span class="gsc_g_t"[^>]*>(\d{4})</span>', page)]
by_year = {y: 0 for y in years}
for z, n in re.findall(r'class="gsc_g_a" style="[^"]*z-index:(\d+)"><span class="gsc_g_al">(\d+)</span>', page):
    by_year[years[-int(z)]] = int(n)

# citations per paper, by Scholar's title (matched to pubs.py at build time)
papers = []
for row in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, flags=re.S):
    t = re.search(r'class="gsc_a_at">(.*?)</a>', row)
    c = re.search(r'class="gsc_a_ac gs_ibl">(\d*)</a>', row)
    if t:
        papers.append((html.unescape(t.group(1)), int(c.group(1)) if c and c.group(1) else 0))

lines = [
    "# Google Scholar metrics: the line under the header figures, the citations-per-year",
    "# chart beside it, and the citation count on each publication.",
    "# Refresh with:  python3 update_scholar.py   (fetches the profile, rewrites this file, rebuilds)",
    "# Or edit the numbers by hand and run build.py.",
    f'SCHOLAR = dict(citations={cites}, h_index={h}, i10_index={i10}, as_of="{today}")',
    "",
    "BY_YEAR = {" + ", ".join(f"{y}: {n}" for y, n in sorted(by_year.items())) + "}",
    "",
    "# (title on Scholar, citations)",
    "PAPERS = [",
] + [f"    ({t!r}, {n})," for t, n in papers] + ["]", ""]
(HERE / "scholar.py").write_text("\n".join(lines), encoding="utf-8")
print(f"Scholar: {cites} citations, h-index {h}, i10-index {i10} (as of {today}); "
      f"{len(papers)} papers, {len(by_year)} years")

if "--no-build" not in sys.argv:
    subprocess.run([sys.executable, str(HERE / "build.py")], check=True)
