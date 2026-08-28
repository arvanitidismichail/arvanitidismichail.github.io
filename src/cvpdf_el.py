#!/usr/bin/env python3
"""Greek edition of the CV PDF.

Same content as the English CV — nothing added, nothing dropped. Built by
translating the generated English HTML, so the two can never drift apart in
structure. Publication titles, journal names and conference names stay in
English: they are bibliographic references.
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import cvpdf  # noqa: E402

OUT_HTML = Path(__file__).parent / "cv_print_el.html"
OUT_PDF = Path(__file__).parent.parent / "CV_Michail_Arvanitidis_EL.pdf"

# (english, greek, expected occurrences)
CV_EL = [
    # ---- masthead ----
    ("<title>CV — Dr Michail Arvanitidis</title>",
     "<title>Βιογραφικό — Δρ Μιχαήλ Αρβανιτίδης</title>", 1),
    ("<h1>Dr Michail Arvanitidis</h1>", "<h1>Δρ Μιχαήλ Αρβανιτίδης</h1>", 1),
    ("Postdoctoral Research Fellow &middot; Centre of Precision Rehabilitation for Spinal Pain (CPR Spine)",
     "Μεταδιδακτορικός Ερευνητής &middot; Κέντρο Εξατομικευμένης Αποκατάστασης για τον Πόνο της Σπονδυλικής Στήλης (CPR Spine)", 1),
    ("CPR Spine, School of Sport, Exercise and Rehabilitation Sciences, University of Birmingham, UK",
     "CPR Spine, Σχολή Αθλητισμού, Άσκησης και Επιστημών Αποκατάστασης, Πανεπιστήμιο του Μπέρμιγχαμ, Ηνωμένο Βασίλειο", None),
    ("CPR Spine, University of Birmingham, UK", "CPR Spine, Πανεπιστήμιο του Μπέρμιγχαμ, Ηνωμένο Βασίλειο", None),
    ("School of Sport, Exercise and Rehabilitation Sciences, University of Birmingham, UK",
     "Σχολή Αθλητισμού, Άσκησης και Επιστημών Αποκατάστασης, Πανεπιστήμιο του Μπέρμιγχαμ, Ηνωμένο Βασίλειο", None),
    (">University profile</a>", ">Προφίλ πανεπιστημίου</a>", 1),

    # ---- profile ----
    ("<h2>Profile</h2>", "<h2>Προφίλ</h2>", 1),
    ("""Dr Michail Arvanitidis (PT, PhD, MSc, MMACP) is a Postdoctoral Research Fellow at the
Centre of Precision Rehabilitation for Spinal Pain (CPR Spine), School of Sport, Exercise and
Rehabilitation Sciences, University of Birmingham, United Kingdom. His current research examines
cervical adaptations in NASA astronauts following spaceflight, aiming to enhance astronaut health
for future missions. His main interests involve studying motor adaptations in pain-affected or
vulnerable populations. He works principally with high-density surface electromyography, motor unit
decomposition and isokinetic dynamometry, and has published 29 peer-reviewed papers (10 as first
author). He holds a European Commission Seal of Excellence for the MSCA Postdoctoral Fellowship
proposal PRO-AGE (91.8/100).""",
     """Ο Δρ Μιχαήλ Αρβανιτίδης (PT, PhD, MSc, MMACP) είναι Μεταδιδακτορικός Ερευνητής στο Κέντρο
Εξατομικευμένης Αποκατάστασης για τον Πόνο της Σπονδυλικής Στήλης (CPR Spine), Σχολή Αθλητισμού,
Άσκησης και Επιστημών Αποκατάστασης, Πανεπιστήμιο του Μπέρμιγχαμ, Ηνωμένο Βασίλειο. Η τρέχουσα
έρευνά του εξετάζει τις προσαρμογές της αυχενικής μοίρας σε αστροναύτες της NASA μετά από
διαστημική πτήση, με στόχο τη βελτίωση της υγείας τους σε μελλοντικές αποστολές. Τα κύρια
ερευνητικά του ενδιαφέροντα αφορούν τις κινητικές προσαρμογές σε πληθυσμούς με πόνο ή αυξημένη
ευαλωτότητα. Εργάζεται κυρίως με ηλεκτρομυογραφία επιφανείας υψηλής πυκνότητας, αποσύνθεση
κινητικών μονάδων και ισοκινητική δυναμομέτρηση, και έχει δημοσιεύσει 29 εργασίες σε περιοδικά με
κριτές (10 ως πρώτος συγγραφέας). Του έχει απονεμηθεί Seal of Excellence της Ευρωπαϊκής Επιτροπής
για την πρόταση MSCA Postdoctoral Fellowship PRO-AGE (91,8/100).""", 1),

    # ---- experience ----
    ("<h2>Professional Experience</h2>", "<h2>Ερευνητική και Επαγγελματική Εμπειρία</h2>", 1),
    ("Post-doctoral Research Fellow", "Μεταδιδακτορική ερευνητική θέση (Post-doctoral Fellowship)", 1),
    ("Pre-doctoral Research Fellow", "Προδιδακτορική ερευνητική θέση (Pre-doctoral Fellowship)", 2),
    ("Specialist Musculoskeletal Physiotherapist (part-time)",
     "Εξειδικευμένος Μυοσκελετικός Φυσικοθεραπευτής (μερική απασχόληση)", 1),
    ("Musculoskeletal Physiotherapist</span>", "Μυοσκελετικός Φυσικοθεραπευτής</span>", 1),
    ("The Birmingham Back Pain Clinic, Birmingham, UK",
     "The Birmingham Back Pain Clinic, Μπέρμιγχαμ, Ηνωμένο Βασίλειο", 1),
    ("Private Physiotherapy Centre, Drama, Greece",
     "Ιδιωτικό Κέντρο Φυσικοθεραπείας, Δράμα, Ελλάδα", 1),
    ("Mentor: Prof. Deborah Falla. Project:", "Επιβλέπουσα: Καθ. Deborah Falla. Έργο:", None),
    ("— cervical spine and muscle adaptation after spaceflight and relationship to herniation risk.",
     "— προσαρμογές της αυχενικής μοίρας της σπονδυλικής στήλης και των μυών μετά από διαστημική πτήση και σχέση με τον κίνδυνο δισκοκήλης.", None),
    ("Employer: Dr David W. Evans.", "Εργοδότης: Δρ David W. Evans.", 1),
    ("Employer: Mr Panagiotis Gklavopoulos.", "Εργοδότης: κ. Παναγιώτης Γκλαβόπουλος.", 1),

    # ---- education ----
    ("<h2>Education</h2>", "<h2>Εκπαίδευση</h2>", 1),
    ("PhD, Sport, Exercise and Rehabilitation Sciences",
     "Διδακτορικό Δίπλωμα (PhD), Επιστήμες Αθλητισμού, Άσκησης και Αποκατάστασης", 1),
    ("MSc Advanced Manipulative Physiotherapy",
     "Μεταπτυχιακό Δίπλωμα Ειδίκευσης (MSc Advanced Manipulative Physiotherapy)", 1),
    ("BSc Physiotherapy (First Class Honours)", "Πτυχίο Φυσικοθεραπείας (BSc), Άριστα", 1),
    ("Department of Physiotherapy, University of Thessaly, Lamia, Greece",
     "Τμήμα Φυσικοθεραπείας, Πανεπιστήμιο Θεσσαλίας, Λαμία, Ελλάδα", 1),
    ("Supervisors: Dr Eduardo Martinez-Valdes, Prof. Deborah Falla. Funded scholarship.",
     "Επιβλέποντες: Δρ Eduardo Martinez-Valdes, Καθ. Deborah Falla. Με υποτροφία.", 1),
    ("Supervisors: Dr Eduardo Martinez-Valdes, Prof. Deborah Falla.",
     "Επιβλέποντες: Δρ Eduardo Martinez-Valdes, Καθ. Deborah Falla.", None),
    ("Supervisor: Prof. Georgios Gioftsos.", "Επιβλέπων: Καθ. Γεώργιος Γιόφτσος.", 1),

    # ---- awards ----
    ("<h2>Awards &amp; Distinctions</h2>", "<h2>Βραβεία και Διακρίσεις</h2>", 1),
    ("<b>Seal of Excellence</b>, European Commission — Horizon Europe MSCA Postdoctoral Fellowships 2025, proposal PRO-AGE (101274439), score 91.8/100; host: Aristotle University of Thessaloniki.",
     "<b>Seal of Excellence</b>, Ευρωπαϊκή Επιτροπή — Horizon Europe MSCA Postdoctoral Fellowships 2025, πρόταση PRO-AGE (101274439), βαθμολογία 91,8/100· ίδρυμα υποδοχής: Αριστοτέλειο Πανεπιστήμιο Θεσσαλονίκης.", 1),
    ("Shortlisted, Oral Student Presentation Awards, XXIV Congress of the International Society of Electrophysiology and Kinesiology.",
     "Υποψήφιος για τα Βραβεία Προφορικής Παρουσίασης Φοιτητών, XXIV Congress of the International Society of Electrophysiology and Kinesiology.", 1),
    ("Honorary fellowship for distinction in BSc studies, National Scholarships Foundation, University of Thessaly.",
     "Τιμητική υποτροφία για διάκριση στις προπτυχιακές σπουδές, Ίδρυμα Κρατικών Υποτροφιών, Πανεπιστήμιο Θεσσαλίας.", 1),

    # ---- funding ----
    ("<h2>Research Funding</h2>", "<h2>Χρηματοδότηση Έρευνας</h2>", 1),
    ("<b>UK Space Agency</b> (co-applicant) — <i>Cervical spine and muscle adaptation after spaceflight and relationship to herniation risk.</i>",
     "<b>UK Space Agency</b> (συνεργαζόμενος αιτών) — <i>Προσαρμογές της αυχενικής μοίρας της σπονδυλικής στήλης και των μυών μετά από διαστημική πτήση και σχέση με τον κίνδυνο δισκοκήλης.</i>", 1),
    ("<b>The Royal Society</b> (co-applicant) — <i>Real-time augmented reality feedback of muscle activity to enhance human performance.</i>",
     "<b>The Royal Society</b> (συνεργαζόμενος αιτών) — <i>Ανατροφοδότηση επαυξημένης πραγματικότητας σε πραγματικό χρόνο για τη μυϊκή δραστηριότητα, με σκοπό τη βελτίωση της ανθρώπινης απόδοσης.</i>", 1),
    ("Contributed to the writing of the application.", "Συμμετοχή στη συγγραφή της πρότασης.", 1),

    # ---- publications ----
    ("<h2>Publications — Under Review &amp; In Preparation</h2>",
     "<h2>Δημοσιεύσεις — Υπό Κρίση και Υπό Προετοιμασία</h2>", 1),
    ("<h2>Peer-Reviewed Publications</h2>", "<h2>Δημοσιεύσεις σε Περιοδικά με Κριτές</h2>", 1),
    ("Under review", "Υπό κρίση", None),
    ("In preparation", "Υπό προετοιμασία", None),

    # ---- conferences ----
    ("<h2>Refereed Conference Proceedings</h2>", "<h2>Ανακοινώσεις σε Συνέδρια με Κριτές</h2>", 1),
    ("An asterisk (*) signifies the presenter.", "Ο αστερίσκος (*) υποδηλώνει τον παρουσιαστή.", 1),
    ("Oral &mdash; 13 presentations", "Προφορικές &mdash; 13 ανακοινώσεις", 1),
    ("Poster &mdash; 9 presentations", "Αναρτημένες &mdash; 9 ανακοινώσεις", 1),

    # ---- teaching ----
    ("<h2>Teaching &amp; Mentoring</h2>", "<h2>Διδακτικό Έργο, Επίβλεψη και Καθοδήγηση</h2>", 1),
    ("<b>Neuromuscular Adaptations to Training</b> — postgraduate practical laboratories in isokinetic dynamometry and high-density EMG, University of Birmingham.",
     "<b>Νευρομυϊκές Προσαρμογές στην Προπόνηση</b> — μεταπτυχιακά εργαστήρια σε ισοκινητική δυναμομέτρηση και ηλεκτρομυογραφία υψηλής πυκνότητας, Πανεπιστήμιο του Μπέρμιγχαμ.", 1),
    ("<b>Analysis of Motor Performance</b> — undergraduate practical laboratories in isokinetic dynamometry and high-density EMG, University of Birmingham.",
     "<b>Ανάλυση Κινητικής Απόδοσης</b> — προπτυχιακά εργαστήρια σε ισοκινητική δυναμομέτρηση και ηλεκτρομυογραφία υψηλής πυκνότητας, Πανεπιστήμιο του Μπέρμιγχαμ.", 1),
    ("<b>Invited lecturer</b>, MSc Advanced Physiotherapy, University of Thessaly, Greece — “The role of high-density surface EMG in the assessment and treatment of musculoskeletal disorders: clinical applications”.",
     "<b>Προσκεκλημένη διάλεξη</b>, ΠΜΣ «Προηγμένη Φυσικοθεραπεία», Πανεπιστήμιο Θεσσαλίας — «Ο ρόλος της επιφανειακής ηλεκτρομυογραφίας υψηλής πυκνότητας στην αξιολόγηση και τη θεραπεία των μυοσκελετικών παθήσεων: κλινικές εφαρμογές».", 1),
    ("Annually", "Ετησίως", None),
    ("students</span>", "φοιτητές</span>", None),
    ("Mentoring &mdash; visiting doctoral and Master's researchers from Europe",
     "Καθοδήγηση &mdash; επισκέπτες διδακτορικοί και μεταπτυχιακοί ερευνητές από την Ευρώπη", 1),
    ("Co-supervision &mdash; doctoral theses and Master's / Bachelor's dissertations",
     "Συνεπίβλεψη &mdash; διδακτορικές διατριβές και μεταπτυχιακές / προπτυχιακές εργασίες", 1),
    ("Research placement supervision", "Επίβλεψη ερευνητικής πρακτικής άσκησης", 1),
    ("&ndash;present", "&ndash;σήμερα", None),
    ("trunk muscle function in ageing.", "λειτουργία των μυών του κορμού κατά τη γήρανση.", 1),
    ("neck morphological characteristics and chronic neck pain.",
     "μορφολογικά χαρακτηριστικά του αυχένα και χρόνιος αυχενικός πόνος.", 1),
    ("delayed-onset muscle soreness and neck muscle function.",
     "καθυστερημένος μυϊκός πόνος (DOMS) και λειτουργία των αυχενικών μυών.", 1),
    ("a novel system providing real-time augmented reality visual feedback on vasti and lumbar erector spinae HD-sEMG during functional tasks.",
     "νέο σύστημα οπτικής ανατροφοδότησης επαυξημένης πραγματικότητας σε πραγματικό χρόνο, με HD-sEMG των έσω/έξω πλατέων και του οσφυϊκού ορθωτήρα, κατά τη διάρκεια λειτουργικών δραστηριοτήτων.", 1),
    ("effect of exercise on trunk muscle behaviour in chronic non-specific low back pain: a systematic review and meta-analysis.",
     "επίδραση της άσκησης στη συμπεριφορά των μυών του κορμού σε χρόνια μη ειδική οσφυαλγία: συστηματική ανασκόπηση και μετα-ανάλυση.", 1),
    ("effect of neck-specific exercise on neck muscle morphology in chronic neck pain: a systematic review and meta-analysis.",
     "επίδραση της ειδικής άσκησης αυχένα στη μορφολογία των αυχενικών μυών σε χρόνιο αυχενικό πόνο: συστηματική ανασκόπηση και μετα-ανάλυση.", 1),
    ("exercise, inflammation and musculoskeletal pain: a systematic review.",
     "άσκηση, φλεγμονή και μυοσκελετικός πόνος: συστηματική ανασκόπηση.", 1),
    ("neuromuscular adaptations to machine versus free-weight lower-limb resistance training.",
     "νευρομυϊκές προσαρμογές στην προπόνηση αντίστασης κάτω άκρων με μηχανήματα έναντι ελεύθερων βαρών.", 1),
    ("effects of exercise on pain and force steadiness in neck pain.",
     "επιδράσεις της άσκησης στον πόνο και στη σταθερότητα της δύναμης σε άτομα με αυχενικό πόνο.", 1),
    ("lumbar erector spinae composition and trunk muscle function in chronic low back pain.",
     "σύσταση του οσφυϊκού ορθωτήρα και λειτουργία των μυών του κορμού σε χρόνια οσφυαλγία.", 1),
    ("effect of AR visual feedback on vasti HD-sEMG activity on knee extension endurance, with and without patellofemoral knee pain.",
     "επίδραση της οπτικής ανατροφοδότησης επαυξημένης πραγματικότητας με HD-sEMG των πλατέων στην αντοχή έκτασης γόνατος, με και χωρίς επιγονατιδομηριαίο πόνο.", 1),
    ("validation of a novel device for the measurement of neck strength.",
     "έλεγχος εγκυρότητας νέας συσκευής για τη μέτρηση της δύναμης του αυχένα.", 1),
    ("effects of delayed-onset muscle soreness on neck muscle force and activity.",
     "επιδράσεις του καθυστερημένου μυϊκού πόνου στη δύναμη και τη δραστηριότητα των αυχενικών μυών.", 1),
    ("differences in trunk muscle force control and activity during isometric, concentric and eccentric contractions, with and without chronic low back pain.",
     "διαφορές στον έλεγχο της δύναμης και τη δραστηριότητα των μυών του κορμού σε ισομετρικές, σύγκεντρες και έκκεντρες συσπάσεις, με και χωρίς χρόνια οσφυαλγία.", 1),
    ("training in HD-sEMG and isokinetic dynamometry.",
     "εκπαίδευση στην HD-sEMG και στην ισοκινητική δυναμομέτρηση.", 1),
    ("training in HD-sEMG and systematic review methods.",
     "εκπαίδευση στην HD-sEMG και στη μεθοδολογία των συστηματικών ανασκοπήσεων.", 1),
    ("training in systematic review methods.",
     "εκπαίδευση στη μεθοδολογία των συστηματικών ανασκοπήσεων.", 2),

    # ---- service ----
    ("<h2>Professional Service</h2>", "<h2>Επαγγελματική Προσφορά και Υπηρεσία</h2>", 1),
    ("<b>External examiner</b>, postgraduate research degrees — MSc by Research thesis examination of Mr Harry Clutterbuck, Manchester Metropolitan University, UK.",
     "<b>Εξωτερικός εξεταστής</b> μεταπτυχιακών διατριβών — εξέταση μεταπτυχιακής ερευνητικής διατριβής (MSc by Research) του κ. Harry Clutterbuck, Manchester Metropolitan University, Ηνωμένο Βασίλειο.", 1),
    ("<b>Journal peer reviewer</b>", "<b>Κριτής (peer reviewer) σε επιστημονικά περιοδικά</b>", 1),
    ("<b>Patient and Public Involvement</b> — presentations and interactive discussions with people living with chronic spinal pain via the CPR Spine PPI panel, integrating public feedback into study design, University of Birmingham.",
     "<b>Συναντήσεις Συμμετοχής Ασθενών και Κοινού (PPI)</b> — παρουσιάσεις και διαδραστικές συζητήσεις με άτομα που ζουν με χρόνιο πόνο στη σπονδυλική στήλη, μέσω του μητρώου του CPR Spine, με ενσωμάτωση της ανατροφοδότησης του κοινού στον σχεδιασμό των μελετών, Πανεπιστήμιο του Μπέρμιγχαμ.", 1),

    # ---- registrations ----
    ("<h2>Registrations, Memberships &amp; Certifications</h2>",
     "<h2>Εγγραφές, Επαγγελματικές Ενώσεις και Πιστοποιήσεις</h2>", 1),
    ("Registration &amp; membership", "Εγγραφές και επαγγελματικές ενώσεις", 1),
    ("Panhellenic Association of Physiotherapists, 2016.",
     "Πανελλήνιος Σύλλογος Φυσικοθεραπευτών (ΠΣΦ), 2016.", 1),
    ("Certifications &amp; continuing training", "Πιστοποιήσεις και συνεχιζόμενη κατάρτιση", 1),
]

MONTHS = {
    "Jan": "Ιαν", "Feb": "Φεβ", "Mar": "Μάρ", "Apr": "Απρ", "May": "Μάι", "Jun": "Ιούν",
    "Jul": "Ιούλ", "Aug": "Αύγ", "Sep": "Σεπ", "Oct": "Οκτ", "Nov": "Νοέ", "Dec": "Δεκ",
    "Present": "Σήμερα",
}


def translate(doc):
    for src, dst, expected in CV_EL:
        pattern = re.compile(r"\s+".join(re.escape(w) for w in src.split()))
        n = len(pattern.findall(doc))
        if expected is None:
            if n == 0:
                raise SystemExit(f"cv-i18n: never found {src[:70]!r}")
        elif n != expected:
            raise SystemExit(f"cv-i18n: expected {expected}x, found {n}x for {src[:70]!r}")
        doc = pattern.sub(lambda m, d=dst: d, doc)

    def month(m):
        text = m.group(1)
        for en, gr in MONTHS.items():
            text = re.sub(rf"\b{en}\b", gr, text)
        return f'<span class="when">{text}</span>'

    doc = re.sub(r'<span class="when">([^<]*)</span>', month, doc)
    return doc.replace('<html lang="en">', '<html lang="el">', 1)


def main():
    OUT_HTML.write_text(translate(cvpdf.build_html()), encoding="utf-8")
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
