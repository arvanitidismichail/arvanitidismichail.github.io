#!/usr/bin/env python3
"""Generate index.html for arvanitidismichail.com from the CV publication dataset."""
import html
import re
import sys
from pathlib import Path

from pubs import PUBS  # noqa: E402
from conferences import CONFS  # noqa: E402
from i18n import STRINGS, MONTHS  # noqa: E402

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


def render_item(p):
    cls = "publication-item" + (" is-first-author" if p["first"] else "")
    doi = p.get("doi")
    link = f"https://doi.org/{doi}" if doi else p.get("url")
    badges = ""
    if p["status"] == "review":
        badges += '<span class="badge badge-review">Under review</span>'
    elif p["status"] == "prep":
        badges += '<span class="badge badge-review">In preparation</span>'
    if p["first"]:
        badges += '<span class="badge badge-first">First author</span>'

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

    note = (
        f'<p class="pub-note">{html.escape(p["note"])}</p>' if p.get("note") else ""
    )

    return f"""      <article class="{cls}" data-year="{p['year']}" data-status="{p['status']}" data-first="{1 if p['first'] else 0}" data-search="{search_blob(p)}">
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
        "canonical": "https://arvanitidismichail.com/",
    },
    "el": {
        "href": "../", "code": "en", "label": "English", "short": "EN",
        "canonical": "https://arvanitidismichail.com/el/",
    },
}


def fill(doc, lang):
    cfg = LANG[lang]
    # Google supports one site name per domain: declare WebSite on the root only
    doc = doc.replace("__WEBSITE_LD__", WEBSITE_LD if lang == "en" else "")
    doc = doc.replace("__LANG_HREF__", cfg["href"])
    doc = doc.replace("__LANG_CODE__", cfg["code"])
    doc = doc.replace("__LANG_LABEL__", cfg["label"])
    doc = doc.replace("__LANG_SHORT__", cfg["short"])
    doc = doc.replace("__CANONICAL__", cfg["canonical"])
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

    en = fill(result, "en")
    dest = HERE.parent / "index.html"
    dest.write_text(en, encoding="utf-8")
    print(f"wrote {dest} — {len(en):,} bytes")

    el = fill(to_greek(result), "el")
    el = to_subdir(el)
    el_dest = HERE.parent / "el" / "index.html"
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
