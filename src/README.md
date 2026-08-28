# How this site is built

`index.html` and `el/index.html` are **generated**. Do not edit them by hand —
the next build overwrites your changes. Edit the sources here instead.

```
cd src
python3 build.py
```

That writes both pages. Then `git add -A && git commit && git push`.

## The files

| File | What it holds |
| --- | --- |
| `template.html` | The page itself: layout, CSS, JavaScript, and all the English text |
| `pubs.py` | The 36 publications, one dict each |
| `conferences.py` | The 22 conference presentations |
| `i18n.py` | The Greek translation — one line per phrase |
| `build.py` | Puts it together and writes both language versions |
| `cvpdf.py` | Builds `CV_Michail_Arvanitidis.pdf` (needs Playwright) |

## Adding a publication

Add a dict to the list in `pubs.py` and run `build.py`. The counts in the page
("29 published · 7 in progress"), the year filters and the search index all
update themselves — they are computed, not typed.

## How the Greek version works

There is no translation service. `i18n.py` is a hand-written list of pairs:

```python
("<h2>Positions</h2>", "<h2>Θέσεις</h2>", 1),
```

The third value is **how many times that phrase must appear** in the English
page. `build.py` generates English first, then walks this list and replaces
each phrase. If a phrase is not found the expected number of times, the build
**stops with an error** rather than quietly leaving English inside the Greek
page. So if you reword something in `template.html` and forget the Greek, you
find out immediately.

Matching ignores line breaks, so re-wrapping a paragraph in the template does
not break its translation.

Two things are handled separately:

- **Month names** in the date column, by a small regex — `Sep 2024 – present`
  becomes `Σεπ 2024 – σήμερα` everywhere at once.
- **Relative links**, because the Greek page sits one folder down: every
  `./photo.jpg` becomes `../photo.jpg`.

### What is deliberately NOT translated

Publication titles, journal names and conference names stay in English. They
are bibliographic references — a translated reference cannot be looked up.
They are not in `i18n.py` at all, so they stay English by construction.

## English stays the default

`arvanitidismichail.com` always serves English to everyone. There is no
redirect based on browser language. `/el/` is reached only through the globe
button in the footer, and `hreflang="x-default"` tells search engines to prefer
English when in doubt.
