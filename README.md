# arvanitidismichail.github.io

Academic homepage and CV for **Dr Michail Arvanitidis** — Postdoctoral Research Fellow,
Centre of Precision Rehabilitation for Spinal Pain (CPR Spine), University of Birmingham.

Live at <https://arvanitidismichail.github.io>

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole site — single self-contained page (HTML + CSS + JS). |
| `CV_Michail_Arvanitidis.pdf` | Full academic CV, linked from the "Download full CV" button. |
| `office-1.jpg` | Profile photograph. |
| `uob.png` | University of Birmingham mark. |

## Updating

Everything lives in `index.html`. Common edits:

- **Add a publication** — copy an existing `<article class="publication-item">` block into the
  right `.year-group`. Keep the four data attributes in sync, they drive the filter and search:
  - `data-year` — publication year
  - `data-status` — `published`, `review` or `prep`
  - `data-first` — `1` if first author, otherwise `0`
  - `data-search` — lowercase text blob searched by the search box (authors, title, journal, topic)
- **Update the header counts** — the four tiles in `<div class="metrics">` and the
  `<span class="count">` next to the Publications heading.
- **Replace the CV PDF** — overwrite `CV_Michail_Arvanitidis.pdf`, keeping the filename.

No build step and no dependencies. Push to `main` and GitHub Pages redeploys.

## Notes

- Theme follows the visitor's system preference and can be toggled; the choice is remembered
  in `localStorage`.
- The starfield background is disabled automatically under `prefers-reduced-motion`.
- Structured data (schema.org `Person`) is embedded in `<head>` for search engines.
- The page has dedicated print styles — Ctrl/Cmd-P produces a clean document.
