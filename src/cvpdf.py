#!/usr/bin/env python3
"""Build a clean, standalone academic CV PDF (no MSCA participating-organisation section)."""
import html
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/home/claude")
from pubs import PUBS  # noqa: E402
from conferences import CONFS  # noqa: E402

OUT_HTML = Path("/home/claude/build/cv_print.html")
OUT_PDF = Path("/home/claude/out/CV_Michail_Arvanitidis.pdf")

CSS = """
@page { size: A4; margin: 15mm 16mm 16mm; }
* { box-sizing: border-box; }
body {
  font-family: "Source Serif 4", Georgia, "Times New Roman", serif;
  font-size: 9.6pt; line-height: 1.42; color: #14181d; margin: 0;
}
h1 { font-size: 20pt; margin: 0 0 2pt; letter-spacing: -.2pt; }
.creds { font-family: Inter, Helvetica, Arial, sans-serif; font-size: 8.6pt; letter-spacing: 1.1pt;
         color: #103a63; font-weight: 600; margin-bottom: 5pt; }
.contact { font-family: Inter, Helvetica, Arial, sans-serif; font-size: 8.4pt; color: #4a545f; }
.contact a { color: #103a63; text-decoration: none; }
.rule { height: 2px; background: #103a63; margin: 9pt 0 0; }
h2 {
  font-family: Inter, Helvetica, Arial, sans-serif;
  font-size: 9.4pt; font-weight: 700; letter-spacing: 1.1pt; text-transform: uppercase;
  color: #103a63; margin: 14pt 0 6pt; padding-bottom: 2.5pt;
  border-bottom: .6pt solid #c2ccd8; break-after: avoid;
}
h2:first-of-type { margin-top: 11pt; }
.entry { margin-bottom: 7pt; break-inside: avoid; }
.entry .hd { display: flex; justify-content: space-between; gap: 10pt; align-items: baseline; }
.entry .role { font-weight: 700; font-size: 10pt; }
.entry .when { font-family: Inter, Helvetica, Arial, sans-serif; font-size: 8pt;
               color: #103a63; font-weight: 600; white-space: nowrap; }
.entry .where { font-size: 9.2pt; color: #333c46; font-style: italic; }
.entry .det { font-size: 9pt; color: #4a545f; margin-top: 1pt; }
.summary { font-size: 9.6pt; color: #333c46; margin: 0; text-align: justify; }
ul.plain { list-style: none; margin: 0; padding: 0; }
ul.plain > li { margin-bottom: 4.5pt; padding-left: 10pt; position: relative; break-inside: avoid; }
ul.plain > li::before { content: "\\2022"; position: absolute; left: 0; color: #103a63; }
.meta { font-family: Inter, Helvetica, Arial, sans-serif; font-size: 8pt; color: #6b7581; display: block; }
.yr { font-family: Inter, Helvetica, Arial, sans-serif; font-size: 8pt; color: #0d8b86; font-weight: 600; }
ol.pubs { margin: 0; padding-left: 15pt; }
ol.pubs li { margin-bottom: 5pt; break-inside: avoid; font-size: 9.1pt; }
ol.pubs li b { color: #101821; }
.jr { font-style: italic; }
.doi { font-family: Inter, Helvetica, Arial, sans-serif; font-size: 7.6pt; color: #6b7581; }
.subhd { font-family: Inter, Helvetica, Arial, sans-serif; font-size: 8.6pt; font-weight: 700;
         color: #333c46; margin: 8pt 0 4pt; break-after: avoid; }
.tag-line { font-size: 8.8pt; color: #4a545f; }
.two { column-count: 2; column-gap: 14pt; }
.two > * { break-inside: avoid; }
footer.pg { position: fixed; bottom: -9mm; left: 0; right: 0; text-align: center;
            font-family: Inter, sans-serif; font-size: 7.4pt; color: #97a0ab; }
"""


def esc(s):
    return html.escape(s)


def pub_li(p, n):
    if p.get("doi"):
        doi = f' <span class="doi">doi: {p["doi"]}</span>'
    elif p.get("url"):
        doi = f' <span class="doi">{p["url"]}</span>'
    else:
        doi = ""
    vol = f' {esc(p["vol"])}.' if p["vol"] else ""
    return (
        f'<li>{p["authors"]}. {esc(p["title"])}. '
        f'<span class="jr">{esc(p["journal"])}.</span>{vol}{doi}</li>'
    )


def conf_block(kind):
    rows = [c for c in CONFS if c["kind"] == kind]
    rows.sort(key=lambda c: (-c["year"], -c["month"], c["title"]))
    items = []
    for c in rows:
        flag = "<b>Invited talk.</b> " if c.get("invited") else ""
        items.append(
            f'<li>{c["authors"]}. {flag}{esc(c["title"])}. '
            f'<span class="jr">{esc(c["venue"])}.</span> '
            f'<span class="yr">{esc(c["dates"])}</span></li>'
        )
    return "\n".join(items)


def build_html():
    pending = [p for p in PUBS if p["status"] != "published"]
    pending.sort(key=lambda p: (p["status"] != "review", p["title"]))
    published = [p for p in PUBS if p["status"] == "published"]
    published.sort(key=lambda p: (-p["year"], p["title"]))

    pend_items = "\n".join(pub_li(p, i) for i, p in enumerate(pending, 1))
    pub_items = "\n".join(pub_li(p, i) for i, p in enumerate(published, 1))
    oral = conf_block("oral")
    poster = conf_block("poster")
    n_oral = sum(1 for c in CONFS if c["kind"] == "oral")
    n_poster = sum(1 for c in CONFS if c["kind"] == "poster")

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>CV — Dr Michail Arvanitidis</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>

<h1>Dr Michail Arvanitidis</h1>
<div class="creds">PT &middot; PhD &middot; MSc &middot; MMACP</div>
<div class="contact">
  Postdoctoral Research Fellow &middot; Centre of Precision Rehabilitation for Spinal Pain (CPR Spine)<br>
  School of Sport, Exercise and Rehabilitation Sciences, University of Birmingham, UK<br>
  <a href="mailto:m.arvanitidis@bham.ac.uk">m.arvanitidis@bham.ac.uk</a> &middot;
  <a href="https://arvanitidismichail.com">arvanitidismichail.com</a> &middot;
  <a href="https://www.birmingham.ac.uk/staff/profiles/sportex/arvanitidis-michail.aspx">University profile</a> &middot;
  <a href="https://scholar.google.com/citations?user=fHHpMb0AAAAJ">Google Scholar</a> &middot;
  <a href="https://orcid.org/0000-0002-3339-6668">ORCID 0000-0002-3339-6668</a>
</div>
<div class="rule"></div>

<h2>Profile</h2>
<p class="summary">Dr Michail Arvanitidis (PT, PhD, MSc, MMACP) is a Postdoctoral Research Fellow at the
Centre of Precision Rehabilitation for Spinal Pain (CPR Spine), School of Sport, Exercise and
Rehabilitation Sciences, University of Birmingham, United Kingdom. His current research examines
cervical adaptations in NASA astronauts following spaceflight, aiming to enhance astronaut health
for future missions. His main interests involve studying motor adaptations in pain-affected or
vulnerable populations. He works principally with high-density surface electromyography, motor unit
decomposition and isokinetic dynamometry, and has published 29 peer-reviewed papers (10 as first
author). He holds a European Commission Seal of Excellence for the MSCA Postdoctoral Fellowship
proposal PRO-AGE (91.8/100).</p>

<h2>Professional Experience</h2>
<div class="entry">
  <div class="hd"><span class="role">Post-doctoral Research Fellow</span><span class="when">Sep 2024 – Present</span></div>
  <div class="where">CPR Spine, School of Sport, Exercise and Rehabilitation Sciences, University of Birmingham, UK</div>
  <div class="det">Mentor: Prof. Deborah Falla. Project: <i>Cervical in Space</i> — cervical spine and muscle adaptation after spaceflight and relationship to herniation risk.</div>
</div>
<div class="entry">
  <div class="hd"><span class="role">Pre-doctoral Research Fellow</span><span class="when">Sep 2022 – Sep 2024</span></div>
  <div class="where">CPR Spine, University of Birmingham, UK</div>
  <div class="det">Mentor: Prof. Deborah Falla. Project: <i>Cervical in Space</i>.</div>
</div>
<div class="entry">
  <div class="hd"><span class="role">Pre-doctoral Research Fellow</span><span class="when">Feb 2021 – Aug 2022</span></div>
  <div class="where">CPR Spine, University of Birmingham, UK</div>
  <div class="det">Mentor: Prof. Deborah Falla. Project: <i>Cervical in Space</i>.</div>
</div>
<div class="entry">
  <div class="hd"><span class="role">Specialist Musculoskeletal Physiotherapist (part-time)</span><span class="when">Jun 2018 – Jul 2023</span></div>
  <div class="where">The Birmingham Back Pain Clinic, Birmingham, UK</div>
  <div class="det">Employer: Dr David W. Evans.</div>
</div>
<div class="entry">
  <div class="hd"><span class="role">Musculoskeletal Physiotherapist</span><span class="when">Nov 2016 – Aug 2017</span></div>
  <div class="where">Private Physiotherapy Centre, Drama, Greece</div>
  <div class="det">Employer: Mr Panagiotis Gklavopoulos.</div>
</div>

<h2>Education</h2>
<div class="entry">
  <div class="hd"><span class="role">PhD, Sport, Exercise and Rehabilitation Sciences</span><span class="when">Feb 2019 – Sep 2024</span></div>
  <div class="where">CPR Spine, University of Birmingham, UK</div>
  <div class="det">Supervisors: Dr Eduardo Martinez-Valdes, Prof. Deborah Falla. Funded scholarship.</div>
</div>
<div class="entry">
  <div class="hd"><span class="role">MSc Advanced Manipulative Physiotherapy</span><span class="when">Sep 2017 – Feb 2019</span></div>
  <div class="where">School of Sport, Exercise and Rehabilitation Sciences, University of Birmingham, UK</div>
  <div class="det">Supervisors: Dr Eduardo Martinez-Valdes, Prof. Deborah Falla.</div>
</div>
<div class="entry">
  <div class="hd"><span class="role">BSc Physiotherapy (First Class Honours)</span><span class="when">Sep 2011 – Nov 2015</span></div>
  <div class="where">Department of Physiotherapy, University of Thessaly, Lamia, Greece</div>
  <div class="det">Supervisor: Prof. Georgios Gioftsos.</div>
</div>

<h2>Awards &amp; Distinctions</h2>
<ul class="plain">
  <li><b>Seal of Excellence</b>, European Commission — Horizon Europe MSCA Postdoctoral Fellowships 2025,
      proposal PRO-AGE (101274439), score 91.8/100; host: Aristotle University of Thessaloniki. <span class="yr">2026</span></li>
  <li>Level 2 CPD Award (&pound;1,500), Musculoskeletal Association of Chartered Physiotherapists. <span class="yr">2024</span></li>
  <li>Level 2 Research Award (&pound;1,500), Musculoskeletal Association of Chartered Physiotherapists. <span class="yr">2024</span></li>
  <li>Shortlisted, Oral Student Presentation Awards, XXIV Congress of the International Society of
      Electrophysiology and Kinesiology. <span class="yr">2022</span></li>
  <li>IFOMPT Travel Bursary Award (&pound;500), Musculoskeletal Association of Chartered Physiotherapists. <span class="yr">2020</span></li>
  <li>Honorary fellowship for distinction in BSc studies, National Scholarships Foundation,
      University of Thessaly. <span class="yr">2011–12</span></li>
</ul>

<h2>Research Funding</h2>
<ul class="plain">
  <li><b>UK Space Agency</b> (co-applicant) — <i>Cervical spine and muscle adaptation after spaceflight and
      relationship to herniation risk.</i> &pound;97,000 (2025–26); &pound;486,183 (2022–25); &pound;116,341 (2021–22).</li>
  <li><b>The Royal Society</b> (co-applicant) — <i>Real-time augmented reality feedback of muscle activity to
      enhance human performance.</i> &pound;11,907 (2022). Contributed to the writing of the application.</li>
</ul>

<h2>Publications — Under Review &amp; In Preparation</h2>
<ol class="pubs">
{pend_items}
</ol>

<h2>Peer-Reviewed Publications</h2>
<ol class="pubs">
{pub_items}
</ol>

<h2>Refereed Conference Proceedings</h2>
<p class="tag-line" style="margin:0 0 5pt">An asterisk (*) signifies the presenter.</p>
<div class="subhd">Oral &mdash; {n_oral} presentations</div>
<ol class="pubs">
{oral}
</ol>
<div class="subhd">Poster &mdash; {n_poster} presentations</div>
<ol class="pubs">
{poster}
</ol>

<h2>Teaching &amp; Mentoring</h2>
<ul class="plain">
  <li><b>Neuromuscular Adaptations to Training</b> — postgraduate practical laboratories in isokinetic
      dynamometry and high-density EMG, University of Birmingham. <span class="meta">Annually 2020–2025 · ~204 students</span></li>
  <li><b>Analysis of Motor Performance</b> — undergraduate practical laboratories in isokinetic dynamometry
      and high-density EMG, University of Birmingham. <span class="meta">Annually 2022–2025 · ~357 students</span></li>
  <li><b>Invited lecturer</b>, MSc Advanced Physiotherapy, University of Thessaly, Greece — “The role of
      high-density surface EMG in the assessment and treatment of musculoskeletal disorders: clinical
      applications”. <span class="meta">Annually 2021–2025 · ~66 students</span></li>
</ul>

<div class="subhd">Mentoring &mdash; visiting doctoral and Master's researchers from Europe</div>
<ul class="plain">
  <li><b>Martina Parrella</b> (PhD), 2025&ndash;present &mdash; trunk muscle function in ageing.</li>
  <li><b>Georgios Sidiropoulos</b> (PhD), 2024&ndash;2026 &mdash; neck morphological characteristics and chronic neck pain.</li>
  <li><b>Hirofumi Sageshima</b> (PhD), 2024&ndash;2026 &mdash; delayed-onset muscle soreness and neck muscle function.</li>
  <li><b>Martina Sergi</b> (MSc), 2022 &mdash; a novel system providing real-time augmented reality visual
      feedback on vasti and lumbar erector spinae HD-sEMG during functional tasks.</li>
</ul>

<div class="subhd">Co-supervision &mdash; doctoral theses and Master's / Bachelor's dissertations</div>
<ul class="plain">
  <li><b>Annie Jain</b> (MSc), 2026&ndash;present &mdash; effect of exercise on trunk muscle behaviour in
      chronic non-specific low back pain: a systematic review and meta-analysis.</li>
  <li><b>Jessica McIntosh</b> (MSc), 2026 &mdash; effect of neck-specific exercise on neck muscle morphology
      in chronic neck pain: a systematic review and meta-analysis.</li>
  <li><b>Dhruv Intwala</b> (MSc), 2025 &mdash; exercise, inflammation and musculoskeletal pain: a systematic review.</li>
  <li><b>Rongda Zhang</b> (PhD), 2024&ndash;present &mdash; neuromuscular adaptations to machine versus
      free-weight lower-limb resistance training.</li>
  <li><b>Anna Gray</b> (MSc), 2024 &mdash; effects of exercise on pain and force steadiness in neck pain.</li>
  <li><b>Shilpa Purushotham</b> (PhD), 2023&ndash;present &mdash; lumbar erector spinae composition and trunk
      muscle function in chronic low back pain.</li>
  <li><b>Cillian Worrall, Xuemin Jiang, Yu Zha</b> (MSc), 2023 &mdash; effect of AR visual feedback on vasti
      HD-sEMG activity on knee extension endurance, with and without patellofemoral knee pain.</li>
  <li><b>Hon Ken Mak</b> (BSc), 2022 &mdash; validation of a novel device for the measurement of neck strength.</li>
  <li><b>Hoi Lau, Sara Lilley</b> (BSc), 2022 &mdash; effects of delayed-onset muscle soreness on neck muscle
      force and activity.</li>
  <li><b>Joseph Ford, Joel Nathan, Luci Owen</b> (BSc), 2022 &mdash; differences in trunk muscle force control
      and activity during isometric, concentric and eccentric contractions, with and without chronic low back pain.</li>
</ul>

<div class="subhd">Research placement supervision</div>
<ul class="plain">
  <li><b>Mayowa Akinnifesi</b> (MSc), 2024 &mdash; training in HD-sEMG and isokinetic dynamometry.</li>
  <li><b>William Price</b> (MSc), 2024 &mdash; training in HD-sEMG and systematic review methods.</li>
  <li><b>Lily Brewster</b> (BSc), 2023 &mdash; training in systematic review methods.</li>
  <li><b>Sze Chan</b> (BSc), 2023 &mdash; training in systematic review methods.</li>
</ul>

<h2>Professional Service</h2>
<ul class="plain">
  <li><b>External examiner</b>, postgraduate research degrees — MSc by Research thesis examination
      of Mr Harry Clutterbuck, Manchester Metropolitan University, UK. <span class="yr">20 May 2026</span></li>
  <li><b>Journal peer reviewer</b> — <span class="tag-line">Applied Psychophysiology and Biofeedback;
      BMC Musculoskeletal Disorders; Clinical Biomechanics; European Journal of Applied Physiology;
      European Spine Journal; Journal of Applied Biomechanics; Journal of Applied Physiology;
      Journal of Biomechanics; Journal of Electromyography and Kinesiology; Journal of Sports Sciences;
      Musculoskeletal Science and Practice; Occupational and Environmental Medicine; PLOS ONE;
      Scientific Reports.</span></li>
  <li><b>Patient and Public Involvement</b> — presentations and interactive discussions with people living
      with chronic spinal pain via the CPR Spine PPI panel, integrating public feedback into study design,
      University of Birmingham. <span class="yr">2019–2024</span></li>
</ul>

<h2>Registrations, Memberships &amp; Certifications</h2>
<div class="subhd">Registration &amp; membership</div>
<div class="tag-line">Health and Care Professions Council (HCPC), 2018 &middot; Chartered Society of Physiotherapy (CSP), 2018 &middot;
Musculoskeletal Association of Chartered Physiotherapists (MACP), 2019 &middot;
International Society of Electrophysiology and Kinesiology (ISEK), 2020 &middot;
Association of Chartered Physiotherapists in Occupational Health and Ergonomics (ACPOHE), 2026 &middot;
Panhellenic Association of Physiotherapists, 2016.</div>
<div class="subhd">Certifications &amp; continuing training</div>
<div class="tag-line">Vehicle Ergonomics Online Training, ACPOHE, 2026 &middot; Office Ergonomics (DSE), ACPOHE, 2026 &middot;
Supervised Machine Learning: Regression and Classification, DeepLearning.AI / Stanford Online, 2025 &middot;
R Programming, Johns Hopkins University, 2024 &middot; The Data Scientist's Toolbox, Johns Hopkins University, 2023 &middot;
Certified Peer Reviewer Course, Elsevier, 2021 &middot; Introduction to Programming with MATLAB, Vanderbilt University, 2019 &middot;
Otago Exercise Programme (OEP) Leader Award, Later Life Training, 2015.</div>

</body></html>"""


def main():
    OUT_HTML.write_text(build_html(), encoding="utf-8")
    subprocess.run(
        [
            "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            "--headless", "--disable-gpu", "--no-sandbox",
            "--no-pdf-header-footer",
            "--virtual-time-budget=8000",
            f"--print-to-pdf={OUT_PDF}",
            OUT_HTML.as_uri(),
        ],
        check=True, capture_output=True,
    )
    print("PDF:", OUT_PDF, OUT_PDF.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
