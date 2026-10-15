#!/usr/bin/env python3
"""Weekly refresh, run by .github/workflows/weekly-update.yml (or by hand).

1. Publications — asks OpenAlex and Crossref for every work linked to the
   ORCID. A paper listed here as under review / in preparation that now has a
   journal DOI becomes "published"; a published paper still waiting for its
   volume and pages gets them; a journal article not listed at all is added.
   Abstracts, preprints, theses and supplementary files are skipped, as is
   anything in ignore_dois.txt.
2. Google Scholar figures (update_scholar.py) — best effort: Scholar often
   refuses requests from cloud servers, and then last week's numbers stay.
3. Collaboration map (update_collab.py).
4. Rebuilds both pages.

Prints a summary of what changed (also written to the GitHub job summary).
"""
import difflib
import html
import json
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from pubs import PUBS  # noqa: E402

ORCID = "0000-0002-3339-6668"
MAILTO = "site@arvanitidismichail.com"
PUBS_FILE = HERE / "pubs.py"
IGNORE_FILE = HERE / "ignore_dois.txt"
PAPER_TYPES = {"article", "review", "letter"}
NOT_PAPERS = ("10.6084/",)          # figshare: supplementary files

log = []


def get_json(url):
    out = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", f"site-weekly (mailto:{MAILTO})", url],
                         capture_output=True, text=True)
    return json.loads(out.stdout) if out.returncode == 0 and out.stdout.strip() else None


def norm(t):
    t = html.unescape(re.sub(r"<[^>]+>", "", t or ""))
    return re.sub(r"[^a-z0-9]+", " ", t.lower().replace("‐", "-")).strip()


def similar(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


# ---------------------------------------------------------------- discovery
def candidate_dois():
    """DOIs of journal papers linked to the ORCID, from OpenAlex and Crossref."""
    found = {}
    oa = get_json(f"https://api.openalex.org/works?filter=author.orcid:{ORCID}&per-page=200"
                  f"&select=doi,title,type&mailto={MAILTO}")
    for w in (oa or {}).get("results", []):
        doi = (w.get("doi") or "").replace("https://doi.org/", "").lower()
        if doi and w.get("type") in PAPER_TYPES:
            found[doi] = w.get("title") or ""
    cr = get_json(f"https://api.crossref.org/works?filter=orcid:{ORCID}&rows=200&mailto={MAILTO}")
    for w in (cr or {}).get("message", {}).get("items", []):
        if w.get("type") == "journal-article" and w.get("DOI"):
            found.setdefault(w["DOI"].lower(), (w.get("title") or [""])[0])
    if oa is None and cr is None:
        log.append("Could not reach OpenAlex or Crossref; publications not checked this week.")
    return found


def crossref(doi):
    m = get_json(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}")
    return (m or {}).get("message")


# ---------------------------------------------------------------- formatting
def year_of(m):
    # the issue's year once there is one (as the site cites), else first appearance
    for k in ("published-print", "journal-issue", "issued", "published-online"):
        v = m.get(k)
        if k == "journal-issue":
            v = (v or {}).get("published-print")
        parts = (v or {}).get("date-parts") or [[None]]
        if parts[0][0]:
            return int(parts[0][0])
    return None


def vol_of(m):
    y, v, i = year_of(m), m.get("volume"), m.get("issue")
    p = (m.get("page") or m.get("article-number") or "").replace("-", "–")
    if not v:
        return str(y) if y else ""
    s = f"{y};{v}"
    if i:
        s += f"({i})"
    if p:
        s += f":{p}"
    return s


def authors_of(m):
    out = []
    for a in m.get("author", []):
        fam = a.get("family") or a.get("name") or ""
        ini = "".join(part[0] for part in re.split(r"[\s.\-]+", a.get("given") or "") if part)
        name = f"{fam} {ini}".strip()
        me = ORCID in (a.get("ORCID") or "") or fam.lower() == "arvanitidis"
        out.append(f"<b>{name}</b>" if me else name)
    return ", ".join(out)


def journal_of(m):
    return html.unescape((m.get("container-title") or [""])[0])


# ---------------------------------------------------------------- editing pubs.py
def block_span(src, title):
    """Start and end of the dict(...) in pubs.py whose title is `title`."""
    i = src.index(repr(title)[1:-1][:60])
    a = src.rfind("    dict(", 0, i)
    b = src.index("),\n", i) + 3
    return a, b


def set_field(block, key, value):
    pat = re.compile(rf'(\b{key}=)(None|"(?:[^"\\]|\\.)*"|\d+|True|False)')
    return pat.sub(lambda mm: mm.group(1) + value, block, count=1)


def q(s):
    return json.dumps(s, ensure_ascii=False)


def main():
    src = PUBS_FILE.read_text(encoding="utf-8")
    ignore = {l.strip().lower() for l in IGNORE_FILE.read_text().splitlines()
              if l.strip() and not l.startswith("#")} if IGNORE_FILE.exists() else set()
    known = {(p.get("doi") or "").lower() for p in PUBS if p.get("doi")}

    # papers already published but listed without volume/pages yet
    for p in PUBS:
        if p["status"] == "published" and p.get("doi") and re.fullmatch(r"\d{4}", p.get("vol") or ""):
            m = crossref(p["doi"])
            if m and m.get("volume"):
                a, b = block_span(src, p["title"])
                blk = set_field(src[a:b], "vol", q(vol_of(m)))
                y = year_of(m)
                if y and y != p["year"]:
                    blk = set_field(blk, "year", str(y))
                src = src[:a] + blk + src[b:]
                log.append(f"Volume and pages added: {p['title'][:80]} → {vol_of(m)}")

    for doi, title in candidate_dois().items():
        if doi in known or doi in ignore or doi.startswith(NOT_PAPERS):
            continue
        # a published paper we list under another DOI (e.g. the preprint's)?
        if any(p["status"] == "published" and similar(title, p["title"]) >= 0.9 for p in PUBS):
            continue
        m = crossref(doi)
        if not m or m.get("type") != "journal-article":
            continue
        jtitle = html.unescape(re.sub(r"<[^>]+>", "", (m.get("title") or [title])[0]))
        pending = [p for p in PUBS if p["status"] != "published" and similar(jtitle, p["title"]) >= 0.85]
        y = year_of(m)
        if pending:
            p = pending[0]
            a, b = block_span(src, p["title"])
            blk = src[a:b]
            blk = set_field(blk, "status", q("published"))
            blk = set_field(blk, "year", str(y or p["year"]))
            blk = set_field(blk, "journal", q(journal_of(m)))
            blk = set_field(blk, "vol", q(vol_of(m)))
            blk = set_field(blk, "doi", q(m["DOI"]))
            src = src[:a] + blk + src[b:]
            log.append(f"Now published: {p['title'][:80]} — {journal_of(m)} {vol_of(m)}")
        else:
            auth = authors_of(m)
            if not auth:
                continue
            first = auth.startswith("<b>")
            entry = (f"    dict(year={y}, status=\"published\", first={first},\n"
                     f"         authors={q(auth)},\n"
                     f"         title={q(jtitle)},\n"
                     f"         journal={q(journal_of(m))}, vol={q(vol_of(m))}, doi={q(m['DOI'])},\n"
                     f"         topic=\"\",\n"
                     f"         note=None),\n")
            end = src.rindex("]")
            src = src[:end] + "\n    # ---- added automatically by weekly.py ----\n" + entry + src[end:]
            log.append(f"New paper added: {jtitle[:80]} — {journal_of(m)} {vol_of(m)}")
        known.add(doi)

    if src != PUBS_FILE.read_text(encoding="utf-8"):
        PUBS_FILE.write_text(src, encoding="utf-8")

    # Scholar: best effort
    r = subprocess.run([sys.executable, str(HERE / "update_scholar.py"), "--no-build"],
                       capture_output=True, text=True)
    log.append((r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip()
               else "Scholar refused the request this week; its figures were left as they were.")

    r = subprocess.run([sys.executable, str(HERE / "update_collab.py"), "--no-build"],
                       capture_output=True, text=True)
    log.append(("Map: " + r.stdout.strip().splitlines()[-1]) if r.returncode == 0 and r.stdout.strip()
               else "Could not refresh the collaboration map this week.")

    subprocess.run([sys.executable, str(HERE / "build.py")], check=True)

    summary = "\n".join(f"- {l}" for l in log)
    print(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write("## Weekly site update\n\n" + summary + "\n")
    (HERE.parent / ".weekly-summary.txt").write_text(summary + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
