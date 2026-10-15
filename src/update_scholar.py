#!/usr/bin/env python3
"""Fetch citations, h-index and i10-index from the Google Scholar profile,
write them to scholar.py, then rebuild both pages.

Scholar has no API, so this reads the public profile page. It works from a
normal home or office connection; Scholar may refuse automated requests from
servers. If it fails, edit scholar.py by hand instead.
"""
import datetime
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
PROFILE = "https://scholar.google.com/citations?user=fHHpMb0AAAAJ&hl=en"
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

(HERE / "scholar.py").write_text(
    "# Google Scholar metrics, shown under the figures at the top of the page.\n"
    "# Refresh with:  python3 update_scholar.py   (fetches the profile, rewrites this file, rebuilds)\n"
    "# Or edit the numbers by hand and run build.py.\n"
    f'SCHOLAR = dict(citations={cites}, h_index={h}, i10_index={i10}, as_of="{today}")\n',
    encoding="utf-8")
print(f"Scholar: {cites} citations, h-index {h}, i10-index {i10} (as of {today})")

subprocess.run([sys.executable, str(HERE / "build.py")], check=True)
