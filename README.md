# arvanitidismichail.com

Academic homepage and CV for **Dr Michail Arvanitidis** — Postdoctoral Research Fellow,
Centre of Precision Rehabilitation for Spinal Pain (CPR Spine), University of Birmingham.

Live at <https://arvanitidismichail.com>

## Files

| File | Purpose |
| --- | --- |
| `index.html` | The whole site — single self-contained page (HTML + CSS + JS). |
| `CV_Michail_Arvanitidis.pdf` | Full academic CV, linked from the "Curriculum vitae" link. |
| `office-1.jpg` | Portrait. |
| `uob.png` | University of Birmingham mark. |

## Design

- **Type** — Avenir Next, falling back to Mulish (loaded from Google Fonts) for visitors
  without it, then to the system sans.
- **Colour** — navy `#103a63` as the accent, teal `#0d8b86` for awards and status markers,
  on a near-white paper background. Dark theme lightens both to `#7db4e8` / `#3fc9c0`.
- Dark is the default, set as `data-theme="dark"` on `<html>` so there is no flash of light
  before the script runs. Visitors can switch to light with the toggle and the choice is
  remembered in `localStorage`; system preference is deliberately not consulted.
- Section reveals are disabled automatically under `prefers-reduced-motion`.
- Structured data (schema.org `Person`, including ORCID) is embedded in `<head>`.
- Dedicated print styles — Ctrl/Cmd-P produces a clean document.

## Updating

Everything lives in `index.html`. Common edits:

- **Add a publication** — copy an existing `<article class="publication-item">` block into the
  right `.year-group`. Keep the four data attributes in sync, they drive the filter and search:
  - `data-year` — publication year
  - `data-status` — `published`, `review` or `prep`
  - `data-first` — `1` if first author, otherwise `0`
  - `data-search` — lowercase text blob searched by the search box (authors, title, journal, topic)
- **Update the counts** — the four figures in `<div class="tally">` and the
  `<span class="label aside">` next to the Publications heading.
- **Replace the CV PDF** — overwrite `CV_Michail_Arvanitidis.pdf`, keeping the filename.

No build step and no dependencies. Push to `main` and GitHub Pages redeploys. Hard-refresh
after a push — Pages caches `index.html` for about ten minutes.
