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
| `cvpdf.py` | Builds `CV_Michail_Arvanitidis.pdf` (needs headless Chromium) |
| `cvpdf_el.py` | Builds the Greek CV PDF by translating the English one |

## Adding a publication

Add a dict to the list in `pubs.py` and run `build.py`. The counts in the page
("29 published · 7 in progress"), the year filters and the search index all
update themselves — they are computed, not typed.

## Adding an interactive lesson

The lessons under Teaching are written in `src/lessons.py`: one entry per
lesson, with the English text, the Greek text and the code in both languages
together. Each is a small notebook: **read**, **explore** (a live model with
sliders), **code** and a one-question **check**.

The code comes in two languages. **R** runs in the visitor's browser (webR,
nothing to install) on the very signal being shown. **MATLAB** cannot run in a
web page, so its tab shows the code, a Copy button and the output it gives;
"Download the data (CSV)" saves the signal on screen, and running either
language on that file gives the numbers shown on the page. Both codes follow the
sliders (the R box stops following once a student edits it; Reset brings it
back).

There are three lessons: EMG amplitude, force steadiness and the HD-sEMG map
(centroid and peak).

To add a lesson, copy an entry in `lessons.py`: the text, the code and a `ctl`
list that describes its sliders (a range or a checkbox each; `{name}` in the
code is replaced by the slider's current value). Then add a small model named
after its `kind` to `labModels` in the "Interactive lessons" block of
`template.html`: `setup()` builds the data once, `compute()` the numbers for the
current sliders, `draw()` the picture, and `read()`, `out()`, `vals()` and
`csv()` the readouts, the MATLAB-style output, the code values and the CSV. Run
`python3 build.py`.

Every number on the page comes from the model's own maths, so check a new
lesson the same way the existing ones were checked: download the CSV, run the R
code on it with Rscript and compare. Set `matlab_out=False` on a lesson whose
MATLAB output cannot be matched exactly. The first Run of R downloads it (about 10 MB, once);
nothing else on the page depends on it.

## The weekly automatic update

Every Monday a GitHub Action (`.github/workflows/weekly-update.yml`) runs
`src/weekly.py`, which:

- marks a paper listed as under review or in preparation as **published**
  once it appears with a journal DOI, with its journal, volume and pages;
- fills in volume and pages for published papers that were still waiting
  for them;
- **adds** any new journal article linked to the ORCID that is not listed
  yet (topic and note left blank: add them by hand if you want);
- refreshes the Google Scholar figures (best effort: Scholar often refuses
  cloud servers, and then the previous numbers stay) and the collaboration map;
- rebuilds both pages and publishes them if anything changed.

Each run lists what it changed on its page in the repository's Actions tab,
and in the commit message. To run it now: Actions → Weekly site update →
Run workflow. To stop something being added (a conference abstract, say), put
its DOI in `src/ignore_dois.txt`. The CV PDFs are not regenerated
automatically.

Google Scholar refuses GitHub's servers, so the Scholar figures are refreshed
from the Mac instead: a launchd job
(`~/Library/LaunchAgents/com.arvanitidismichail.scholar.plist`) runs
`~/.site-scholar/update.sh` every day at 09:00 and 15:00 (or on waking, if the
Mac was asleep). It waits up to ten minutes for the network, retries if a push
is refused, and works in its own copy of the site at `~/.site-scholar/site`.
It runs `update_scholar.py` and publishes only if the numbers changed, so most
runs do nothing. Log: `~/Library/Logs/site-scholar.log`. To stop it:
`launchctl bootout gui/$(id -u)/com.arvanitidismichail.scholar`.

## Updating the Google Scholar figures

The citations, h-index and i10-index under the header figures, the
citations-per-year chart beside them and the "Cited by" count on each
publication all come from `scholar.py`. To refresh them from the live
profile and rebuild:

```
cd src
python3 update_scholar.py
```

Scholar has no API, so this reads the public profile page. It works from a home
or office connection; if Scholar ever answers with a CAPTCHA, edit the three
numbers and the date in `scholar.py` by hand and run `build.py`.

## Updating the collaboration map

The map in Research is built from `collab.py`: the institutions of co-authors
on the papers in `pubs.py`, taken from OpenAlex (open data, no account needed)
and grouped by city. After adding papers, refresh it and rebuild:

```
cd src
python3 update_collab.py
```

The dotted land behind it is `worldmap.py`, generated once by
`make_worldmap.py` from Natural Earth; it never needs rerunning.

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
