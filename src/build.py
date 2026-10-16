#!/usr/bin/env python3
"""Generate index.html for arvanitidismichail.com from the CV publication dataset."""
import datetime
import difflib
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pubs import PUBS  # noqa: E402
from conferences import CONFS  # noqa: E402
from i18n import STRINGS, MONTHS  # noqa: E402
from scholar import SCHOLAR, BY_YEAR, PAPERS  # noqa: E402
from collab import HOME, CITIES  # noqa: E402
import worldmap  # noqa: E402

HERE = Path(__file__).parent


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def search_blob(p):
    parts = [strip_tags(p["authors"]), p["title"], p["journal"], p["topic"], str(p["year"])]
    if p.get("note"):
        parts.append(p["note"])
    if p["first"]:
        parts.append("first author arvanitidis")
    if p["status"] == "review":
        parts.append("under review preprint")
    if p["status"] == "prep":
        parts.append("in preparation")
    return html.escape(" ".join(parts).lower(), quote=True)


def _norm(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower().replace("\u2010", "-")).strip()


def scholar_cites(p):
    """Citations on Scholar for this paper, matched by title (Scholar truncates
    long titles with an ellipsis, so a long shared prefix counts as a match)."""
    n, best = _norm(p["title"]), (0.0, 0)
    for t, c in PAPERS:
        m = _norm(t.rstrip("\u2026."))
        r = 1.0 if len(m) > 40 and n.startswith(m) else difflib.SequenceMatcher(None, n, m).ratio()
        best = max(best, (r, c))
    return best[1] if best[0] >= 0.9 else 0


def render_item(p):
    cls = "publication-item" + (" is-first-author" if p["first"] else "")
    doi = p.get("doi")
    link = f"https://doi.org/{doi}" if doi else p.get("url")
    tags = []
    if p["status"] == "review":
        tags.append('<span class="badge badge-review">Under review</span>')
    elif p["status"] == "prep":
        tags.append('<span class="badge badge-review">In preparation</span>')
    if p["first"]:
        tags.append('<span class="badge badge-first">First author</span>')
    # <wbr> so two badges can fall on separate lines on a narrow phone;
    # without it they are one unbreakable run and push the page sideways
    badges = "<wbr>".join(tags)

    title = html.escape(p["title"])
    if link:
        title_html = (
            f'<a class="pub-title" href="{link}" target="_blank" rel="noopener">'
            f'{badges}{title}<span class="ext"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5h10v10M19 5L7 17"/></svg></span></a>'
        )
    else:
        title_html = f'<span class="pub-title">{badges}{title}</span>'

    venue = f'<em>{html.escape(p["journal"])}</em>'
    if p["vol"]:
        venue += " · " + html.escape(p["vol"])
    cites = scholar_cites(p)
    if cites:
        venue += f' <span class="cites"><span class="cl">Cited by</span> {cites}</span>'

    note = (
        f'<p class="pub-note">{html.escape(p["note"])}</p>' if p.get("note") else ""
    )

    return f"""      <article class="{cls}" data-year="{p['year']}" data-status="{p['status']}" data-first="{1 if p['first'] else 0}" data-cites="{cites}" data-search="{search_blob(p)}">
        {title_html}
        <div class="pub-authors">{p['authors']}</div>
        <div class="pub-venue">{venue}</div>
{note and '        ' + note}
      </article>"""


def render_confs():
    out = []
    for kind, heading in (("oral", "Oral"), ("poster", "Poster")):
        rows = [c for c in CONFS if c["kind"] == kind]
        rows.sort(key=lambda c: (-c["year"], -c["month"], strip_tags(c["authors"])))
        out.append(f'    <h3>{heading} &mdash; {len(rows)} presentation{"s" if len(rows) != 1 else ""}</h3>')
        out.append(f'    <div class="rows rise foldable" data-fold="5" data-fold-noun="{heading.lower()} presentations">')
        for c in rows:
            flag = ' <b>Invited talk.</b>' if c.get("invited") else ''
            out.append(f"""      <div class="row">
        <div class="when">{c['when']}</div>
        <div class="what">{flag} {html.escape(c['title'])}.
          <span class="sub">{c['authors']}
            <span class="conf-authors">{html.escape(c['venue'])} &middot; {html.escape(c['dates'])}</span>
          </span>
        </div>
      </div>""")
        out.append('    </div>')
    return "\n".join(out)



WEBSITE_LD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Michail Arvanitidis",
  "alternateName": [
    "Dr Michail Arvanitidis",
    "\u039c\u03b9\u03c7\u03b1\u03ae\u03bb \u0391\u03c1\u03b2\u03b1\u03bd\u03b9\u03c4\u03af\u03b4\u03b7\u03c2"
  ],
  "url": "https://arvanitidismichail.com/"
}
</script>

"""


LANG = {
    "en": {
        "href": "./el/", "code": "el", "label": "Ελληνικά", "short": "EL",
        "cur_flag": "gb", "cur_label": "English", "alt_flag": "gr",
        "canonical": "https://arvanitidismichail.com/",
    },
    "el": {
        "href": "../", "code": "en", "label": "English", "short": "EN",
        "cur_flag": "gr", "cur_label": "Ελληνικά", "alt_flag": "gb",
        "canonical": "https://arvanitidismichail.com/el/",
    },
}


MAP_TEXT = {
    "en": dict(paper="paper", papers="papers", inst="institutions", cities="cities",
               countries="countries", all="All institutions", home="Birmingham — home institution",
               label="World map of co-authors' institutions, each linked to Birmingham",
               src="Co-authors' affiliations on the papers listed here, from OpenAlex. "
                   "Dot size shows shared papers."),
    "el": dict(paper="δημοσίευση", papers="δημοσιεύσεις", inst="ιδρύματα", cities="πόλεις",
               countries="χώρες", all="Όλα τα ιδρύματα", home="Μπέρμιγχαμ — ίδρυμα υποδοχής",
               label="Παγκόσμιος χάρτης των ιδρυμάτων των συν-συγγραφέων, συνδεδεμένων με το Μπέρμιγχαμ",
               src="Ιδρύματα των συν-συγγραφέων στις δημοσιεύσεις αυτής της σελίδας, από το OpenAlex. "
                   "Το μέγεθος κάθε κουκκίδας δείχνει τις κοινές δημοσιεύσεις."),
}


def render_map(lang):
    """Collaboration map: a dot-grid world, an arc from Birmingham to each city
    whose institutions co-authored a paper, dots sized by shared papers."""
    T = MAP_TEXT[lang]
    k, top = worldmap.SCALE, worldmap.LAT_TOP

    def xy(lat, lon):
        return (lon + 180) * k, (top - lat) * k

    hx, hy = xy(HOME["lat"], HOME["lon"])
    arcs, dots = [], []
    for i, c in enumerate(sorted(CITIES, key=lambda c: c["lon"])):
        x, y = xy(c["lat"], c["lon"])
        # bow each arc upward, more for longer hops
        mx, my = (hx + x) / 2, (hy + y) / 2
        d = ((x - hx) ** 2 + (y - hy) ** 2) ** 0.5
        cy = max(my - min(d * 0.35, 160), 12)   # stay inside the frame
        arcs.append(f'<path class="arc" style="--n:{i}" pathLength="1" '
                    f'd="M{hx:.0f} {hy:.0f}Q{mx:.0f} {cy:.0f} {x:.0f} {y:.0f}"/>')
        r = 4 + 2.2 * c["papers"] ** 0.5
        papers = f'{c["papers"]} {T["paper"] if c["papers"] == 1 else T["papers"]}'
        tip = html.escape(f'{c["city"]}, {c["country"]} · {papers} · ' + "; ".join(c["institutions"]), quote=True)
        dots.append(f'<circle class="city" style="--n:{i}" cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" '
                    f'data-tip="{tip}"><title>{tip}</title></circle>')

    countries = sorted({c["country"] for c in CITIES})
    insts = sorted({i for c in CITIES for i in c["institutions"]})
    rows = "\n".join(
        f'        <li><b>{html.escape(c["city"])}</b>, {html.escape(c["country"])} '
        f'<span class="sub">{html.escape("; ".join(c["institutions"]))}</span></li>'
        for c in sorted(CITIES, key=lambda c: (c["country"], c["city"])))
    # crop the empty Pacific: 125°W to 165°E
    x0, x1 = (-125 + 180) * k, (165 + 180) * k
    return f"""    <figure class="cmap-fig rise">
      <div class="cmap-wrap">
        <svg class="cmap" viewBox="{x0} 0 {x1 - x0} {worldmap.HEIGHT}" role="img"
             aria-label="{T['label']}">
          <path class="land" d="{worldmap.DOTS}"/>
          <g class="arcs">{"".join(arcs)}</g>
          <g class="cities">{"".join(dots)}</g>
          <circle class="home" cx="{hx:.0f}" cy="{hy:.0f}" r="7"><title>{T['home']}</title></circle>
        </svg>
        <div class="cmap-tip" aria-hidden="true"></div>
      </div>
      <figcaption>
        <span class="cmap-n"><b>{len(insts)}</b> {T['inst']}</span>
        <span class="cmap-n"><b>{len(CITIES)}</b> {T['cities']}</span>
        <span class="cmap-n"><b>{len(countries)}</b> {T['countries']}</span>
        <span class="cmap-src">{T['src']}</span>
      </figcaption>
      <details class="cmap-list">
        <summary>{T['all']}</summary>
        <ul>
{rows}
        </ul>
      </details>
    </figure>"""


def cite_chart(lang):
    """Citations per year from Scholar: thin bars, the latest year labelled,
    every bar with a tooltip, and the figures as text for screen readers."""
    ys = sorted(BY_YEAR)
    top = max(BY_YEAR.values()) or 1
    word = "αναφορές" if lang == "el" else "citations"
    label = ("Αναφορές ανά έτος" if lang == "el" else "Citations per year") + ": " + \
        ", ".join(f"{y} {BY_YEAR[y]}" for y in ys)
    bars = "".join(
        f'<span class="cb" style="--h:{max(BY_YEAR[y] / top, 0.03):.3f};--n:{i}" data-tip="{y}: {BY_YEAR[y]} {word}">'
        f'{f"<b>{BY_YEAR[y]}</b>" if y == ys[-1] else ""}</span>'
        for i, y in enumerate(ys))
    return (f'<span class="cchart" role="img" aria-label="{label}">'
            f'<span class="cbars">{bars}</span>'
            f'<span class="caxis" aria-hidden="true"><span>{ys[0]}</span><span>{ys[-1]}</span></span></span>')


MONTHS_FULL = {
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
    # genitive, as Greek writes a day and month: 16 Οκτωβρίου 2026
    "el": ["Ιανουαρίου", "Φεβρουαρίου", "Μαρτίου", "Απριλίου", "Μαΐου", "Ιουνίου", "Ιουλίου",
           "Αυγούστου", "Σεπτεμβρίου", "Οκτωβρίου", "Νοεμβρίου", "Δεκεμβρίου"],
}


def stamp(doc, lang, day):
    """Fill in the footer's "Last update" date."""
    return (doc.replace("__UPDATED_ISO__", day.isoformat())
               .replace("__UPDATED__", f"{day.day} {MONTHS_FULL[lang][day.month - 1]} {day.year}"))


def last_update(pages):
    """The date to show: kept from the published pages when nothing else in them
    has changed (so a rebuild with no news leaves them untouched), otherwise today."""
    try:
        old = {dest: dest.read_text(encoding="utf-8") for dest, _, _ in pages}
    except FileNotFoundError:
        return datetime.date.today()
    m = re.search(r'<time datetime="(\d{4}-\d{2}-\d{2})"', next(iter(old.values())))
    if m:
        prev = datetime.date.fromisoformat(m.group(1))
        if all(stamp(doc, lang, prev) == old[dest] for dest, doc, lang in pages):
            return prev
    return datetime.date.today()


def fill(doc, lang):
    cfg = LANG[lang]
    # Google supports one site name per domain: declare WebSite on the root only
    doc = doc.replace("__WEBSITE_LD__", WEBSITE_LD if lang == "en" else "")
    doc = doc.replace("__LANG_HREF__", cfg["href"])
    doc = doc.replace("__LANG_CODE__", cfg["code"])
    doc = doc.replace("__LANG_LABEL__", cfg["label"])
    doc = doc.replace("__LANG_SHORT__", cfg["short"])
    doc = doc.replace("__CUR_FLAG__", cfg["cur_flag"])
    doc = doc.replace("__CUR_LABEL__", cfg["cur_label"])
    doc = doc.replace("__ALT_FLAG__", cfg["alt_flag"])
    doc = doc.replace("__CANONICAL__", cfg["canonical"])
    # "Oct 2026", with the month in the page's language
    y, m, _ = SCHOLAR["as_of"].split("-")
    mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(m) - 1]
    doc = doc.replace("__SCHOLAR_ASOF__", f'{MONTHS[mon] if lang == "el" else mon} {y}')
    # counts, computed so a new paper updates them everywhere
    published = [p for p in PUBS if p["status"] == "published"]
    doc = (doc.replace("__N_PUB__", str(len(published)))
              .replace("__N_FIRST__", str(sum(1 for p in published if p["first"])))
              .replace("__N_PENDING__", str(len(PUBS) - len(published))))
    doc = doc.replace("__CITE_CHART__", cite_chart(lang))
    assert "<!--COLLAB-->" in doc, "collaboration marker missing"
    doc = doc.replace("<!--COLLAB-->", render_map(lang))
    if lang == "el":
        doc = doc.replace('<html lang="en" data-theme="dark">', '<html lang="el" data-theme="dark">', 1)
    return doc


def to_greek(doc):
    """Apply every translation, loudly, so nothing goes missing unnoticed."""
    for src, dst, expected in STRINGS:
        # match on normalised whitespace so line wrapping in the template
        # never silently breaks a translation
        pattern = re.compile(r"\s+".join(re.escape(w) for w in src.split()))
        n = len(pattern.findall(doc))
        if expected is None:
            if n == 0:
                raise SystemExit(f"i18n: never found {src[:70]!r}")
        elif n != expected:
            raise SystemExit(f"i18n: expected {expected}x, found {n}x for {src[:70]!r}")
        doc = pattern.sub(lambda m, d=dst: d, doc)

    # month names, but only inside the date column
    def month(m):
        text = m.group(1)
        for en, gr in MONTHS.items():
            text = re.sub(rf"\b{en}\b", gr, text)
        return f'<div class="when">{text}</div>'

    return re.sub(r'<div class="when">([^<]*)</div>', month, doc)


def to_subdir(doc):
    """The Greek page lives one level down, so its relative links move up one."""
    doc = doc.replace('="./', '="../')
    doc = doc.replace(', ./', ', ../')
    doc = doc.replace('href="../el/"', 'href="../"')   # switcher already points home
    return doc


def leftover_english(doc):
    body = doc[doc.find("<body>"):]
    body = re.sub(r"<script.*?</script>", "", body, flags=re.S)
    body = re.sub(r"<(publication-item|article).*?</\1>", "", body, flags=re.S)
    suspects = ["Show all", "Show fewer", "Under review<", "First author<",
                "Curriculum vitae", "Postdoctoral Research Fellow<", "delivered annually"]
    return [w for w in suspects if w in body]


def main():
    pending = [p for p in PUBS if p["status"] != "published"]
    published = [p for p in PUBS if p["status"] == "published"]

    # order pending: review first, then prep
    pending.sort(key=lambda p: (p["status"] != "review", p["title"]))

    out = []

    if pending:
        out.append('      <div class="year-group">')
        out.append('        <h3 class="year-label pending">Under review &amp; in preparation</h3>')
        out.extend(render_item(p) for p in pending)
        out.append("      </div>")

    years = sorted({p["year"] for p in published}, reverse=True)
    for y in years:
        group = [p for p in published if p["year"] == y]
        group.sort(key=lambda p: (not p["first"], p["title"]))
        out.append('      <div class="year-group">')
        out.append(f'        <h3 class="year-label">{y}</h3>')
        out.extend(render_item(p) for p in group)
        out.append("      </div>")

    block = "\n".join(out)

    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    assert "<!--PUBLICATIONS-->" in tpl, "marker missing"
    result = tpl.replace("<!--PUBLICATIONS-->", block)
    assert "<!--CONFERENCES-->" in result, "conference marker missing"
    result = result.replace("<!--CONFERENCES-->", render_confs())
    result = (result.replace("__CITES__", str(SCHOLAR["citations"]))
                    .replace("__H_INDEX__", str(SCHOLAR["h_index"]))
                    .replace("__I10__", str(SCHOLAR["i10_index"])))

    en = fill(result, "en")
    dest = HERE.parent / "index.html"
    el = to_subdir(fill(to_greek(result), "el"))
    el_dest = HERE.parent / "el" / "index.html"
    day = last_update([(dest, en, "en"), (el_dest, el, "el")])
    en, el = stamp(en, "en", day), stamp(el, "el", day)

    dest.write_text(en, encoding="utf-8")
    print(f"wrote {dest} — {len(en):,} bytes")

    el_dest.parent.mkdir(parents=True, exist_ok=True)
    el_dest.write_text(el, encoding="utf-8")
    print(f"wrote {el_dest} — {len(el):,} bytes")
    left = leftover_english(el)
    if left:
        print("  ⚠ still English:", left)
    print(f"  {len(published)} published, {len(pending)} pending, {len(PUBS)} total")
    print(f"  {sum(1 for c in CONFS if c['kind']=='oral')} oral, "
          f"{sum(1 for c in CONFS if c['kind']=='poster')} poster")


if __name__ == "__main__":
    main()
