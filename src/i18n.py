#!/usr/bin/env python3
"""Greek strings for arvanitidismichail.com.

Every entry is an exact fragment of the generated English page and its Greek
replacement. Each one is asserted to appear the expected number of times, so a
wording change in the template fails the build instead of silently leaving
English behind.

Publication titles, journal names and conference names are NOT translated:
they are bibliographic references, and a translated reference cannot be looked
up. That is deliberate, not an omission.
"""

# (english, greek, expected occurrences)
STRINGS = [
    # ---------- chrome ----------
    ("Skip to content", "Μετάβαση στο περιεχόμενο", 1),
    ('<li><a href="#research">Research</a></li>', '<li><a href="#research">Έρευνα</a></li>', 1),
    ('<li><a href="#positions">Positions</a></li>', '<li><a href="#positions">Επαγγελματική πορεία</a></li>', 1),
    ('<li><a href="#publications">Publications</a></li>', '<li><a href="#publications">Δημοσιεύσεις</a></li>', 1),
    ('<li><a href="#awards">Awards</a></li>', '<li><a href="#awards">Διακρίσεις</a></li>', 1),
    ('<li><a href="#talks">Conferences</a></li>', '<li><a href="#talks">Συνέδρια</a></li>', 1),
    ('<li><a href="#teaching">Teaching</a></li>', '<li><a href="#teaching">Διδασκαλία</a></li>', 1),
    ('<li><a href="#service">Service</a></li>', '<li><a href="#service">Ακαδημαϊκή προσφορά</a></li>', 1),

    ('<a class="nav-cta" href="#contact">', '<a class="nav-cta" href="#contact">', 1),
    ("<span>Contact</span>", "<span>Επικοινωνία</span>", 1),
    ('<div class="foot-col" id="contact">', '<div class="foot-col" id="contact">', 1),

    # ---------- head ----------
    ("<title>Michail Arvanitidis — Postdoctoral Research Fellow, University of Birmingham</title>",
     "<title>Μιχαήλ Αρβανιτίδης — Μεταδιδακτορικός Ερευνητής, Πανεπιστήμιο του Μπέρμιγχαμ</title>", 1),
    ('content="Dr Michail Arvanitidis (PT, PhD, MSc, MMACP) is a Postdoctoral Research Fellow at the Centre of Precision Rehabilitation for Spinal Pain, University of Birmingham. Research on cervical adaptations in astronauts after spaceflight and motor adaptations in pain-affected populations."',
     'content="Ο Δρ Μιχαήλ Αρβανιτίδης (PT, PhD, MSc, MMACP) είναι Μεταδιδακτορικός Ερευνητής στο Κέντρο Αποκατάστασης Ακριβείας για τον Πόνο στη Σπονδυλική Στήλη (CPR Spine) του Πανεπιστημίου του Μπέρμιγχαμ. Έρευνα στις προσαρμογές της αυχενικής μοίρας αστροναυτών μετά από διαστημική πτήση και στις κινητικές προσαρμογές σε πληθυσμούς με πόνο."', 1),
    ('<meta property="og:title" content="Michail Arvanitidis — Postdoctoral Research Fellow">',
     '<meta property="og:title" content="Μιχαήλ Αρβανιτίδης — Μεταδιδακτορικός Ερευνητής">', 1),
    ('<meta name="twitter:title" content="Michail Arvanitidis — Postdoctoral Research Fellow">',
     '<meta name="twitter:title" content="Μιχαήλ Αρβανιτίδης — Μεταδιδακτορικός Ερευνητής">', 1),
    ('content="Cervical adaptations in astronauts after spaceflight, and motor adaptations in pain-affected populations. CPR Spine, University of Birmingham."',
     'content="Προσαρμογές της αυχενικής μοίρας σε αστροναύτες μετά από διαστημική πτήση και κινητικές προσαρμογές σε πληθυσμούς με πόνο. CPR Spine, Πανεπιστήμιο του Μπέρμιγχαμ."', 2),

    # ---------- header ----------
    ('<a href="#top" class="nav-name">Michail Arvanitidis</a>',
     '<a href="#top" class="nav-name">Μιχαήλ Αρβανιτίδης</a>', 1),
    ('<nav class="nav" aria-label="Sections">', '<nav class="nav" aria-label="Ενότητες">', 1),
    ('<div class="eyebrow">Curriculum Vitae</div>',
     '<div class="eyebrow">Ακαδημαϊκό προφίλ</div>', 1),
    ("<h1>Dr Michail Arvanitidis</h1>", "<h1>Δρ Μιχαήλ Αρβανιτίδης</h1>", 1),
    ('<span>Postdoctoral Research Fellow</span>',
     '<span>Μεταδιδακτορικός Ερευνητής</span>', 1),
    (">Centre of Precision Rehabilitation for Spinal Pain</a><br>",
     ">Κέντρο Αποκατάστασης Ακριβείας για τον Πόνο στη Σπονδυλική Στήλη (CPR Spine)</a><br>", 1),
    ("          School of Sport, Exercise and Rehabilitation Sciences<br>\n"
     "          University of Birmingham, United Kingdom",
     "          Σχολή Αθλητισμού, Άσκησης και Επιστημών Αποκατάστασης<br>\n"
     "          Πανεπιστήμιο του Μπέρμιγχαμ, Ηνωμένο Βασίλειο", 1),
    ('alt="Michail Arvanitidis" class="portrait"', 'alt="Μιχαήλ Αρβανιτίδης" class="portrait"', 1),

    # ---------- header links ----------
    (">Curriculum vitae (PDF)</a>", ">Αναλυτικό βιογραφικό (PDF)</a>", 2),
    ('href="./CV_Michail_Arvanitidis.pdf"', 'href="./CV_Michail_Arvanitidis_EL.pdf"', 2),
    ("        University profile</a>", "        Προφίλ πανεπιστημίου</a>", 1),

    # ---------- tally ----------
    ('<div class="t">Peer-reviewed papers</div>', '<div class="t">Δημοσιεύσεις σε περιοδικά με κριτές</div>', 1),
    ('<div class="t">As first author</div>', '<div class="t">Ως πρώτος συγγραφέας</div>', 1),
    ('<div class="t">Funding, co-applicant</div>', '<div class="t">Χρηματοδότηση ως συναιτών</div>', 1),
    ('<div class="t">Journals reviewed for</div>', '<div class="t">Περιοδικά ως κριτής</div>', 1),

    # ---------- research ----------
    ("<h2>Research</h2>", "<h2>Έρευνα</h2>", 1),
    ('<span class="k">About</span>', '<span class="k">Ερευνητικό προφίλ</span>', 1),
    ("Dr Michail Arvanitidis (PT, PhD, MSc, MMACP) is a Postdoctoral Research Fellow at the\n"
     "      Centre of Precision Rehabilitation for Spinal Pain (CPR Spine), School of Sport, Exercise\n"
     "      and Rehabilitation Sciences, University of Birmingham, United Kingdom. His current research\n"
     "      examines cervical adaptations in NASA astronauts following spaceflight, aiming to enhance\n"
     "      astronaut health for future missions. His main interests involve studying motor adaptations\n"
     "      in pain-affected or vulnerable populations.",
     "Ο Δρ Μιχαήλ Αρβανιτίδης (PT, PhD, MSc, MMACP) είναι Μεταδιδακτορικός Ερευνητής στο\n"
     "      Κέντρο Αποκατάστασης Ακριβείας για τον Πόνο στη Σπονδυλική Στήλη (CPR Spine), Σχολή\n"
     "      Αθλητισμού, Άσκησης και Επιστημών Αποκατάστασης, Πανεπιστήμιο του Μπέρμιγχαμ, Ηνωμένο\n"
     "      Βασίλειο. Η τρέχουσα έρευνά του εξετάζει τις προσαρμογές της αυχενικής μοίρας της\n"
     "      σπονδυλικής στήλης και των αυχενικών μυών σε αστροναύτες της NASA μετά από διαστημική\n"
     "      πτήση, με στόχο τη βελτίωση της υγείας των αστροναυτών σε μελλοντικές αποστολές. Τα\n"
     "      κύρια ερευνητικά του ενδιαφέροντα αφορούν τις κινητικές προσαρμογές σε πληθυσμούς με\n"
     "      πόνο ή αυξημένη ευαλωτότητα.", 1),
    ("<h3>Methods and tools</h3>", "<h3>Μέθοδοι και εργαλεία</h3>", 1),
    ('aria-label="Methods and tools"', 'aria-label="Μέθοδοι και εργαλεία"', 1),
    (">High-density surface electromyography</span>", ">Ηλεκτρομυογραφία επιφανείας υψηλής πυκνότητας</span>", 1),
    (">Motor unit decomposition</span>", ">Αποσύνθεση κινητικών μονάδων</span>", 1),
    (">Analysis of B-mode ultrasound data</span>", ">Ανάλυση δεδομένων υπερηχογραφίας B-mode</span>", 1),
    (">Isokinetic dynamometry</span>", ">Ισοκινητική δυναμομέτρηση</span>", 1),
    (">Signal processing</span>", ">Επεξεργασία σήματος</span>", 1),
    (">Augmented reality biofeedback systems</span>", ">Συστήματα βιοανάδρασης επαυξημένης πραγματικότητας</span>", 1),
    (">Systematic review &amp; meta-analysis</span>", ">Συστηματική ανασκόπηση και μετα-ανάλυση</span>", 1),

    # ---------- photograph captions ----------
    ("<b>NASA Lyndon B. Johnson Space Center</b><br>Houston, Texas",
     "<b>NASA Lyndon B. Johnson Space Center</b><br>Χιούστον, Τέξας", 1),
    ("<b>Space Center Houston</b><br>Houston, Texas",
     "<b>Space Center Houston</b><br>Χιούστον, Τέξας", 1),
    ("<b>Patient and Public Involvement session</b><br>CPR Spine, University of Birmingham",
     "<b>Συνάντηση συμμετοχής ασθενών και κοινού</b><br>CPR Spine, Πανεπιστήμιο του Μπέρμιγχαμ", 1),
    ('alt="Michail Arvanitidis outside the NASA Lyndon B. Johnson Space Center sign, Houston"',
     'alt="Ο Μιχαήλ Αρβανιτίδης έξω από την πινακίδα του NASA Lyndon B. Johnson Space Center, Χιούστον"', 1),
    ('alt="Michail Arvanitidis in front of the Shuttle Carrier Aircraft at Space Center Houston"',
     'alt="Ο Μιχαήλ Αρβανιτίδης μπροστά από το Shuttle Carrier Aircraft στο Space Center Houston"', 1),
    ('alt="Michail Arvanitidis presenting beside a projected acknowledgements slide"',
     'alt="Ο Μιχαήλ Αρβανιτίδης παρουσιάζει δίπλα σε προβαλλόμενη διαφάνεια ευχαριστιών"', 1),
    ('alt="Michail Arvanitidis beside his poster on neck force control in astronauts"',
     'alt="Ο Μιχαήλ Αρβανιτίδης δίπλα στο poster του για τον έλεγχο δύναμης του αυχένα σε αστροναύτες"', 1),
    ('alt="Michail Arvanitidis beside his poster on motor unit behaviour in patellofemoral pain"',
     'alt="Ο Μιχαήλ Αρβανιτίδης δίπλα στο poster του για τη συμπεριφορά κινητικών μονάδων στο επιγονατιδομηριαίο πόνο"', 1),
    ('alt="Michail Arvanitidis presenting low back pain research to a Patient and Public Involvement audience"',
     'alt="Ο Μιχαήλ Αρβανιτίδης παρουσιάζει έρευνα για την οσφυαλγία σε κοινό ασθενών"', 1),

    # ---------- positions ----------
    ("<h2>Positions</h2>", "<h2>Επαγγελματική πορεία</h2>", 1),
    ('<div class="role">Postdoctoral Research Fellow</div>',
     '<div class="role">Μεταδιδακτορικός Ερευνητής</div>', 1),
    ('<div class="role">Pre-doctoral Research Fellow</div>',
     '<div class="role">Προδιδακτορικός Ερευνητής</div>', 2),
    ('<div class="role">Specialist Musculoskeletal Physiotherapist</div>',
     '<div class="role">Εξειδικευμένος Μυοσκελετικός Φυσικοθεραπευτής</div>', 1),
    ('<div class="role">Musculoskeletal Physiotherapist</div>',
     '<div class="role">Μυοσκελετικός Φυσικοθεραπευτής</div>', 1),
    ('<div class="org">CPR Spine, University of Birmingham</div>',
     '<div class="org">CPR Spine, Πανεπιστήμιο του Μπέρμιγχαμ</div>', 3),
    ('<div class="org">The Birmingham Back Pain Clinic, United Kingdom</div>',
     '<div class="org">The Birmingham Back Pain Clinic, Ηνωμένο Βασίλειο</div>', 1),
    ('<div class="org">Private Physiotherapy Centre, Drama, Greece</div>',
     '<div class="org">Ιδιωτικό Κέντρο Φυσικοθεραπείας, Δράμα, Ελλάδα</div>', 1),
    ("Project: <em>Cervical in Space</em> — cervical spine and muscle adaptation after\n"
     "          spaceflight and relationship to herniation risk. Mentor: Prof. Deborah Falla.",
     "Έργο: <em>Cervical in Space</em> — προσαρμογές της αυχενικής μοίρας της σπονδυλικής στήλης\n"
     "          και των μυών μετά από διαστημική πτήση και σχέση με τον κίνδυνο δισκοκήλης.\n"
     "          Επιστημονική επόπτρια: Καθ. Deborah Falla.", 1),
    ("Data collection, analysis and dissemination for the <em>Cervical in Space</em> programme\n"
     "          alongside doctoral studies.",
     "Συλλογή, ανάλυση και διάχυση δεδομένων για το πρόγραμμα <em>Cervical in Space</em>,\n"
     "          παράλληλα με τις διδακτορικές σπουδές.", 1),
    ("Astronaut neck strength and neuromuscular assessment protocols; HD-sEMG and\n"
     "          dynamometry pipeline development.",
     "Πρωτόκολλα αξιολόγησης δύναμης αυχένα και νευρομυϊκής λειτουργίας αστροναυτών· ανάπτυξη\n"
     "          ροής ανάλυσης HD-sEMG και δυναμομέτρησης.", 1),
    ("Part-time clinical practice. Assessment and management of complex spinal and\n"
     "          musculoskeletal presentations. Employer: Dr David W. Evans.",
     "Κλινική πρακτική μερικής απασχόλησης. Αξιολόγηση και αντιμετώπιση σύνθετων περιστατικών\n"
     "          σπονδυλικής στήλης και μυοσκελετικού συστήματος. Εργοδότης: Δρ David W. Evans.", 1),
    ("Outpatient musculoskeletal and post-surgical rehabilitation.",
     "Μυοσκελετική και μετεγχειρητική αποκατάσταση σε εξωτερικούς ασθενείς.", 1),

    # ---------- education ----------
    ("<h3>Education</h3>", "<h3>Σπουδές</h3>", 1),
    ('<div class="role">PhD, Sport, Exercise and Rehabilitation Sciences</div>',
     '<div class="role">Διδακτορικό (PhD), Επιστήμες Αθλητισμού, Άσκησης και Αποκατάστασης</div>', 1),
    ('<div class="role">MSc Advanced Manipulative Physiotherapy</div>',
     '<div class="role">Μεταπτυχιακό Δίπλωμα Ειδίκευσης (MSc Advanced Manipulative Physiotherapy)</div>', 1),
    ('<div class="role">BSc Physiotherapy, First Class Honours</div>',
     '<div class="role">Πτυχίο Φυσικοθεραπείας (BSc), Άριστα</div>', 1),
    ('<div class="org">University of Birmingham</div>',
     '<div class="org">Πανεπιστήμιο του Μπέρμιγχαμ</div>', 2),
    ('<div class="org">University of Thessaly, Lamia, Greece</div>',
     '<div class="org">Τμήμα Φυσικοθεραπείας, Πανεπιστήμιο Θεσσαλίας, Λαμία, Ελλάδα</div>', 1),
    ("Control of trunk muscle force in chronic low back pain, using high-density\n"
     "          surface EMG and isokinetic dynamometry. Supervisors: Dr Eduardo Martinez-Valdes,\n"
     "          Prof. Deborah Falla.",
     "Έλεγχος της δύναμης των μυών του κορμού στη χρόνια οσφυαλγία, με ηλεκτρομυογραφία\n"
     "          επιφανείας υψηλής πυκνότητας και ισοκινητική δυναμομέτρηση. Επιβλέποντες:\n"
     "          Δρ Eduardo Martinez-Valdes, Καθ. Deborah Falla.", 1),
    ("MMACP-accredited programme. Supervisors: Dr Eduardo Martinez-Valdes,\n"
     "          Prof. Deborah Falla.",
     "Πρόγραμμα πιστοποιημένο από το MMACP. Επιβλέποντες: Δρ Eduardo Martinez-Valdes,\n"
     "          Καθ. Deborah Falla.", 1),
    ("Supervisor: Prof. Georgios Gioftsos. Honorary fellowship, National\n"
     "          Scholarships Foundation (2011–12).",
     "Επιβλέπων: Καθ. Γεώργιος Γιόφτσος. Τιμητική υποτροφία, Ίδρυμα Κρατικών\n"
     "          Υποτροφιών (2011–12).", 1),

    # ---------- publications ----------
    ("<h2>Publications ", "<h2>Δημοσιεύσεις ", 1),
    (">29 published · 7 in progress<", ">29 δημοσιευμένες · 7 σε εξέλιξη<", 1),
    (">Search publications<", ">Αναζήτηση δημοσιεύσεων<", 1),
    ('placeholder="Search title, author, journal or topic"',
     'placeholder="Αναζήτηση τίτλου, συγγραφέα, περιοδικού ή θέματος"', 1),
    ('aria-label="Filter publications"', 'aria-label="Φίλτρα δημοσιεύσεων"', 1),
    ('data-filter="all" aria-pressed="true">All<', 'data-filter="all" aria-pressed="true">Όλες<', 1),
    ('data-filter="first" aria-pressed="false">First author<', 'data-filter="first" aria-pressed="false">Πρώτος συγγραφέας<', 1),
    ('data-filter="pending" aria-pressed="false">Under review<', 'data-filter="pending" aria-pressed="false">Υπό κρίση<', 1),
    ('data-filter="published" aria-pressed="false">Published<', 'data-filter="published" aria-pressed="false">Δημοσιευμένες<', 1),
    (">No publications match that search.<", ">Καμία δημοσίευση δεν ταιριάζει με την αναζήτηση.<", 1),
    ('<h3 class="year-label pending">Under review &amp; in preparation</h3>',
     '<h3 class="year-label pending">Υπό κρίση και υπό προετοιμασία</h3>', 1),
    ('<span class="badge badge-review">Under review</span>',
     '<span class="badge badge-review">Υπό κρίση</span>', None),
    ('<span class="badge badge-review">In preparation</span>',
     '<span class="badge badge-review">Υπό προετοιμασία</span>', None),
    ('<span class="badge badge-first">First author</span>',
     '<span class="badge badge-first">Πρώτος συγγραφέας</span>', None),
    ("· Under review · preprint on medRxiv", "· Υπό κρίση · προδημοσίευση στο medRxiv", None),
    ("· Under review", "· Υπό κρίση", None),
    ("· In preparation", "· Υπό προετοιμασία", None),
    (">Show all publications<", ">Όλες οι δημοσιεύσεις<", 1),

    # ---------- awards ----------
    ("<h2>Awards</h2>", "<h2>Διακρίσεις</h2>", 1),
    ("<b>Seal of Excellence, European Commission</b>",
     "<b>Seal of Excellence — Ευρωπαϊκή Επιτροπή</b>", 1),
    ('Horizon Europe MSCA Postdoctoral Fellowships 2025, for the proposal PRO-AGE (101274439), scored <span class="sum">91.8 / 100</span>. Host: Aristotle University of Thessaloniki.',
     'Horizon Europe, MSCA Postdoctoral Fellowships 2025, για την πρόταση PRO-AGE (101274439), με βαθμολογία <span class="sum">91,8 / 100</span>· ίδρυμα υποδοχής: Αριστοτέλειο Πανεπιστήμιο Θεσσαλονίκης.', 1),
    ("<b>Level 2 CPD Award</b>", "<b>Level 2 CPD Award</b>", 1),
    ("<b>Level 2 Research Award</b>", "<b>Level 2 Research Award</b>", 1),
    ("<b>Shortlisted, Oral Student Presentation Award</b>",
     "<b>Επιλογή στη βραχεία λίστα για το Oral Student Presentation Award</b>", 1),
    ("<span class=\"sub\">Musculoskeletal Association of Chartered Physiotherapists</span>",
     "<span class=\"sub\">Musculoskeletal Association of Chartered Physiotherapists</span>", 3),
    ("<b>IFOMPT Travel Bursary</b>", "<b>IFOMPT Travel Bursary</b>", 1),
    ("<b>Honorary fellowship for distinction in undergraduate studies</b>",
     "<b>Τιμητική υποτροφία για διάκριση στις προπτυχιακές σπουδές</b>", 1),
    ("National Scholarships Foundation, University of Thessaly",
     "Ίδρυμα Κρατικών Υποτροφιών, Πανεπιστήμιο Θεσσαλίας", 1),

    # ---------- funding ----------
    ("<h3>Funding</h3>", "<h3>Χρηματοδότηση</h3>", 1),
    ("Cervical spine and muscle adaptation after spaceflight and\n"
     "          relationship to herniation risk.",
     "Προσαρμογές της αυχενικής μοίρας της σπονδυλικής στήλης και των μυών μετά από\n"
     "          διαστημική πτήση και σχέση με τον κίνδυνο δισκοκήλης.", 1),
    ("Real-time augmented reality feedback of muscle activity to\n"
     "          enhance human performance.",
     "Ανατροφοδότηση επαυξημένης πραγματικότητας σε πραγματικό χρόνο για τη μυϊκή\n"
     "          δραστηριότητα, με σκοπό τη βελτίωση της ανθρώπινης απόδοσης.", 1),
    ("Co-applicant.", "Συναιτών.", 1),
    ("Co-applicant,", "Συναιτών,", 1),
    (". Contributed to the writing of the application.", ". Συμμετοχή στη συγγραφή της πρότασης.", 1),

    # ---------- conferences ----------
    ("<h2 id=\"talks-t\">Conference presentations ", "<h2 id=\"talks-t\">Παρουσιάσεις σε συνέδρια ", 1),
    (">13 oral · 9 poster<", ">13 προφορικές · 9 αναρτημένες παρουσιάσεις<", 1),
    ("Refereed conference proceedings. An asterisk marks the presenter.",
     "Παρουσιάσεις κατόπιν αξιολόγησης. Ο αστερίσκος (*) δηλώνει τον παρουσιαστή.", 1),
    ("<h3>Oral &mdash; 13 presentations</h3>", "<h3>Προφορικές &mdash; 13 παρουσιάσεις</h3>", 1),
    ("<h3>Poster &mdash; 9 presentations</h3>", "<h3>Αναρτημένες (posters) &mdash; 9 παρουσιάσεις</h3>", 1),
    ('data-fold-noun="oral presentations"', 'data-fold-noun="προφορικές παρουσιάσεις"', 1),
    ('data-fold-noun="poster presentations"', 'data-fold-noun="αναρτημένες παρουσιάσεις"', 1),
    ("<b>Invited talk.</b>", "<b>Προσκεκλημένη ομιλία.</b>", None),

    # ---------- teaching ----------
    ("<h2>Teaching and mentoring</h2>", "<h2>Διδασκαλία και επίβλεψη</h2>", 1),
    ("<b>Neuromuscular Adaptations to Training</b> — postgraduate practical laboratories in\n"
     "          isokinetic dynamometry and high-density EMG.",
     "<b>Νευρομυϊκές προσαρμογές στην προπόνηση</b> — μεταπτυχιακά εργαστήρια σε ισοκινητική\n"
     "          δυναμομέτρηση και ηλεκτρομυογραφία υψηλής πυκνότητας.", 1),
    ("<b>Analysis of Motor Performance</b> — undergraduate practical laboratories in isokinetic\n"
     "          dynamometry and high-density EMG.",
     "<b>Ανάλυση κινητικής απόδοσης</b> — προπτυχιακά εργαστήρια σε ισοκινητική\n"
     "          δυναμομέτρηση και ηλεκτρομυογραφία υψηλής πυκνότητας.", 1),
    ("<b>Invited lecturer</b>, MSc Advanced Physiotherapy — “The role of high-density\n"
     "          surface EMG in the assessment and treatment of musculoskeletal disorders: clinical applications”.",
     "<b>Προσκεκλημένη διάλεξη</b>, ΠΜΣ «Προηγμένη Φυσικοθεραπεία» — «Ο ρόλος της\n"
     "          επιφανειακής ηλεκτρομυογραφίας υψηλής πυκνότητας στην αξιολόγηση και τη θεραπεία των\n"
     "          μυοσκελετικών παθήσεων: κλινικές εφαρμογές».", 1),
    ("<b>Doctoral and Master's supervision</b> — co-supervision of more than twenty PhD,\n"
     "          MSc and BSc research projects spanning trunk and neck neuromuscular control,\n"
     "          tendinopathy, AR biofeedback and systematic review methodology.",
     "<b>Επίβλεψη διδακτορικών και μεταπτυχιακών</b> — συνεπίβλεψη περισσότερων από είκοσι\n"
     "          ερευνητικών εργασιών διδακτορικού, μεταπτυχιακού και προπτυχιακού επιπέδου, σε νευρομυϊκό\n"
     "          έλεγχο κορμού και αυχένα, τενοντοπάθειες, βιοανάδραση επαυξημένης πραγματικότητας και\n"
     "          μεθοδολογία συστηματικών ανασκοπήσεων.", 1),
    ("<b>Host and mentor to visiting doctoral researchers</b> from partner institutions across\n"
     "          Europe, covering HD-sEMG acquisition, decomposition and analysis, alongside\n"
     "          supervision of MSc and BSc research placements.",
     "<b>Υποδοχή και καθοδήγηση επισκεπτών διδακτορικών ερευνητών</b> από συνεργαζόμενα ιδρύματα\n"
     "          της Ευρώπης, σε καταγραφή, αποσύνθεση και ανάλυση HD-sEMG, παράλληλα με την επίβλεψη\n"
     "          ερευνητικών πρακτικών μεταπτυχιακού και προπτυχιακού επιπέδου.", 1),
    ("University of Birmingham · delivered annually · approximately 200 students",
     "Πανεπιστήμιο του Μπέρμιγχαμ · ετησίως · περίπου 200 φοιτητές", 1),
    ("University of Birmingham · delivered annually · approximately 350 students",
     "Πανεπιστήμιο του Μπέρμιγχαμ · ετησίως · περίπου 350 φοιτητές", 1),
    ("University of Thessaly, Greece · delivered annually",
     "Πανεπιστήμιο Θεσσαλίας · ετησίως", 1),

    # ---------- service ----------
    ("<h2>Service</h2>", "<h2>Ακαδημαϊκή προσφορά</h2>", 1),
    ("<b>External examiner</b>, postgraduate research degrees — MSc by Research thesis examination.",
     "<b>Εξωτερικός εξεταστής</b> σε πρόγραμμα MSc by Research — αξιολόγηση μεταπτυχιακής ερευνητικής διατριβής.", 1),
    ("Manchester Metropolitan University, United Kingdom",
     "Manchester Metropolitan University, Ηνωμένο Βασίλειο", 1),
    ("<b>Patient and Public Involvement</b> — presentations and discussions with people\n"
     "          living with chronic spinal pain through the CPR Spine PPI panel, feeding public\n"
     "          input into study design.",
     "<b>Συναντήσεις συμμετοχής ασθενών και κοινού (PPI)</b> — παρουσιάσεις και διαδραστικές\n"
     "          συζητήσεις με άτομα που ζουν με χρόνιο πόνο στη σπονδυλική στήλη, από το μητρώο του\n"
     "          CPR Spine, με ενσωμάτωση της ανατροφοδότησής τους στον σχεδιασμό νέων μελετών.", 1),
    ("<h3>Journal peer review</h3>", "<h3>Κριτής επιστημονικών περιοδικών</h3>", 1),
    ('aria-label="Journals reviewed for"', 'aria-label="Περιοδικά ως κριτής"', 1),
    ("<h3>Registration and membership</h3>", "<h3>Επαγγελματικές εγγραφές και επιστημονικές εταιρείες</h3>", 1),
    ("<h3>Certification and training</h3>", "<h3>Πιστοποιήσεις και κατάρτιση</h3>", 1),
    (">Panhellenic Association of Physiotherapists<", ">Πανελλήνιος Σύλλογος Φυσικοθεραπευτών<", 1),
    (">Vehicle Ergonomics<", ">Vehicle Ergonomics<", 1),
    (">Office Ergonomics (DSE)<", ">Office Ergonomics (DSE)<", 1),
    (">Supervised Machine Learning: Regression and Classification<",
     ">Supervised Machine Learning: Regression and Classification<", 1),
    (">R Programming<", ">R Programming<", 1),
    (">Certified Peer Reviewer Course<", ">Certified Peer Reviewer Course<", 1),
    (">Introduction to Programming with MATLAB<", ">Introduction to Programming with MATLAB<", 1),
    (">Otago Exercise Programme Leader Award<", ">Otago Exercise Programme Leader Award<", 1),

    # ---------- footer ----------
    ('<div class="foot-name">Michail Arvanitidis</div>',
     '<div class="foot-name">Μιχαήλ Αρβανιτίδης</div>', 1),
    ("<p class=\"foot-blurb\">Postdoctoral Research Fellow, Centre of Precision Rehabilitation\n"
     "        for Spinal Pain, School of Sport, Exercise and Rehabilitation Sciences,\n"
     "        University of Birmingham.</p>",
     "<p class=\"foot-blurb\">Μεταδιδακτορικός Ερευνητής, Κέντρο Αποκατάστασης Ακριβείας για τον Πόνο στη Σπονδυλική Στήλη\n"
     "        (CPR Spine), Σχολή Αθλητισμού, Άσκησης και Επιστημών Αποκατάστασης,\n"
     "        Πανεπιστήμιο του Μπέρμιγχαμ.</p>", 1),
    ("<h2>Site</h2>", "<h2>Πλοήγηση</h2>", 1),
    ("<h2>Profiles</h2>", "<h2>Ακαδημαϊκά προφίλ</h2>", 1),
    ("<h2>Contact me on social</h2>", "<h2>Επικοινωνία</h2>", 1),
    ('<div class="or">or e-mail me</div>', '<div class="or">ή επικοινωνήστε μέσω e-mail</div>', 1),
    ('aria-label="Sections of this site"', 'aria-label="Ενότητες της σελίδας"', 1),
    ('aria-label="Academic profiles"', 'aria-label="Ακαδημαϊκά προφίλ"', 1),
    ('<a href="#research">Research</a>', '<a href="#research">Έρευνα</a>', 1),
    ('<a href="#publications">Publications</a>', '<a href="#publications">Δημοσιεύσεις</a>', 1),
    ('<a href="#teaching">Teaching</a>', '<a href="#teaching">Διδασκαλία και επίβλεψη</a>', 1),
    (">University of Birmingham</a>", ">Πανεπιστήμιο του Μπέρμιγχαμ</a>", 1),
    ("<span>&copy; 2026 Dr Michail Arvanitidis. All rights reserved.</span>",
     "<span>&copy; 2026 Δρ Μιχαήλ Αρβανιτίδης. Με επιφύλαξη παντός δικαιώματος.</span>", 1),
    ("<span>Last update: August 2026</span>", "<span>Τελευταία ενημέρωση: Αύγουστος 2026</span>", 1),
    ('aria-label="LinkedIn"', 'aria-label="LinkedIn"', 1),
    ('aria-label="Personal e-mail (Gmail)"', 'aria-label="Προσωπικό e-mail (Gmail)"', 1),
    ('aria-label="University e-mail (Outlook)"', 'aria-label="Πανεπιστημιακό e-mail (Outlook)"', 1),

    # ---------- theme toggle ----------
    ('aria-label="Switch colour theme"', 'aria-label="Εναλλαγή θέματος"', 1),

    # ---------- localisation pass ----------
    (">R language</span>", ">R</span>", 1),
    ('<span class="sub">University of Birmingham</span>',
     '<span class="sub">Πανεπιστήμιο του Μπέρμιγχαμ</span>', 2),

    # ---------- key findings under each publication ----------
    ('First synthesis showing neck-specific exercise may induce structural cervical muscle adaptation.',
     'Πρώτη σύνθεση δεδομένων που δείχνει ότι η ειδική άσκηση αυχένα μπορεί να επιφέρει δομικές προσαρμογές στους αυχενικούς μυς.', 1),
    ('Greater dynamic trunk extensor fatigue resistance in older adults despite poorer torque steadiness.',
     'Μεγαλύτερη αντοχή στην κόπωση των εκτεινόντων του κορμού σε ηλικιωμένους, παρά τη χαμηλότερη σταθερότητα ροπής.', 1),
    ('Load-dependent impairments in fibularis longus neural drive and motor unit rate coding.',
     'Διαταραχές εξαρτώμενες από το φορτίο στη νευρική ώση του μακρού περονιαίου και στην κωδικοποίηση συχνότητας των κινητικών μονάδων.', 1),
    ('Non-invasive HD-sEMG approach to estimate erector spinae muscle fibre size.',
     'Μη επεμβατική προσέγγιση με HD-sEMG για την εκτίμηση του μεγέθους των μυϊκών ινών του ορθωτήρα της ράχης.', 1),
    ('Similar clinical improvements but distinct neuromechanical adaptations between training modes.',
     'Παρόμοια κλινική βελτίωση, αλλά διακριτές νευρομηχανικές προσαρμογές μεταξύ των δύο μορφών προπόνησης.', 1),
    ('AR HD-sEMG biofeedback modified spatial muscle activation and improved knee extensor endurance by 27%.',
     'Η βιοανάδραση HD-sEMG με επαυξημένη πραγματικότητα μετέβαλε τη χωρική ενεργοποίηση του μυός και βελτίωσε την αντοχή των εκτεινόντων του γόνατος κατά 27%.', 1),
    ('Simultaneous HD-sEMG and ultrasound via transparent electrodes revealed contraction-dependent neuromechanical coupling.',
     'Η ταυτόχρονη καταγραφή HD-sEMG και υπερηχογραφίας με διαφανή ηλεκτρόδια ανέδειξε νευρομηχανική σύζευξη εξαρτώμενη από το είδος της σύσπασης.', 1),
    ('Adaptive redistribution of neck muscle activity during experimentally induced soreness.',
     'Προσαρμοστική ανακατανομή της δραστηριότητας των αυχενικών μυών κατά τον πειραματικά προκλητό μυϊκό πόνο.', 1),
    ('Age-related impairments in trunk force control with distinct HD-sEMG patterns.',
     'Διαταραχές του ελέγχου δύναμης του κορμού με την ηλικία, με διακριτά πρότυπα HD-sEMG.', 1),
    ('Updated diagnostic accuracy evidence informing evidence-based clinical decision-making.',
     'Επικαιροποιημένα δεδομένα διαγνωστικής ακρίβειας, χρήσιμα για τεκμηριωμένη κλινική λήψη αποφάσεων.', 1),
    ('First demonstration of load- and muscle-dependent motor unit changes in Achilles tendinopathy.',
     'Πρώτη τεκμηρίωση μεταβολών των κινητικών μονάδων ανάλογα με το φορτίο και τον μυ στην τενοντοπάθεια του Αχιλλείου.', 1),
    ('Revealed regional differences in lumbar erector spinae activity in people with spinal pain.',
     'Ανέδειξε τοπικές διαφορές στη δραστηριότητα του οσφυϊκού ορθωτήρα σε άτομα με πόνο στη σπονδυλική στήλη.', 1),
    ('Novel insight into neuromuscular impairments in patellofemoral pain during single-joint exercise.',
     'Νέα δεδομένα για τις νευρομυϊκές διαταραχές στον επιγονατιδομηριαίο πόνο κατά την άσκηση μίας άρθρωσης.', 1),
    ('First evidence of age-related differences in spatial lumbar activation under fatigue.',
     'Πρώτα δεδομένα για διαφορές της χωρικής ενεργοποίησης των οσφυϊκών μυών με την ηλικία υπό συνθήκες κόπωσης.', 1),
    ('First meta-analysis showing reduced trunk muscle endurance in older adults.',
     'Πρώτη μετα-ανάλυση που δείχνει μειωμένη αντοχή των μυών του κορμού σε ηλικιωμένους.', 1),
    ('The NOD is a valid, reliable, portable alternative to laboratory dynamometry.',
     'Το NOD αποτελεί έγκυρη, αξιόπιστη και φορητή εναλλακτική της εργαστηριακής δυναμομέτρησης.', 1),
    ('Will inform countermeasures to reduce spinal pain and injury risk in astronauts.',
     'Θα καθοδηγήσει τον σχεδιασμό αντίμετρων για τη μείωση του πόνου και του κινδύνου τραυματισμού της σπονδυλικής στήλης σε αστροναύτες.', 1),
    ('First trial of torque-based visual feedback training for patellar tendinopathy.',
     'Πρώτη δοκιμή προπόνησης με οπτική ανατροφοδότηση βάσει ροπής στην τενοντοπάθεια του επιγονατιδικού τένοντα.', 1),
    ('Force steadiness is impaired in musculoskeletal pain — a candidate rehabilitation target.',
     'Η σταθερότητα της δύναμης διαταράσσεται στον μυοσκελετικό πόνο — πιθανός στόχος αποκατάστασης.', 1),
    ('Novel link between motor unit firing behaviour and Achilles tendon mechanical properties.',
     'Νέα σύνδεση μεταξύ της πυροδότησης των κινητικών μονάδων και των μηχανικών ιδιοτήτων του Αχιλλείου τένοντα.', 1),
    ('New HD-sEMG spatial metrics that characterise fatigue and predict muscle endurance.',
     'Νέοι χωρικοί δείκτες HD-sEMG που χαρακτηρίζουν την κόπωση και προβλέπουν τη μυϊκή αντοχή.', 1),
    ('First study of how DOMS influences trunk HD-sEMG–torque relationships and lumbar kinematics.',
     'Πρώτη μελέτη για την επίδραση του καθυστερημένου μυϊκού πόνου στις σχέσεις HD-sEMG–ροπής του κορμού και στην οσφυϊκή κινηματική.', 1),
    ('First evidence of impaired torque steadiness and altered HD-sEMG–torque relationships in dynamic trunk contractions in CLBP.',
     'Πρώτα δεδομένα για μειωμένη σταθερότητα ροπής και μεταβολή των σχέσεων HD-sEMG–ροπής σε δυναμικές συσπάσεις του κορμού στη χρόνια οσφυαλγία.', 1),
    ('Novel HD-sEMG approach overcoming decomposition challenges in the lumbar erector spinae.',
     'Νέα προσέγγιση HD-sEMG που ξεπερνά τις δυσκολίες αποσύνθεσης στον οσφυϊκό ορθωτήρα.', 1),
    ('International project on cervical spine adaptation after spaceflight and preventive strategies for astronauts.',
     'Διεθνές ερευνητικό έργο για τις προσαρμογές της αυχενικής μοίρας μετά από διαστημική πτήση και τις στρατηγικές πρόληψης για αστροναύτες.', 1),
    ('Pain affects motor unit behaviour differently across contraction speeds.',
     'Ο πόνος επηρεάζει διαφορετικά τη συμπεριφορά των κινητικών μονάδων ανάλογα με την ταχύτητα σύσπασης.', 1),
    ('HD-sEMG discriminates biomechanical risk earlier and more accurately than traditional sEMG.',
     'Η HD-sEMG διακρίνει τον βιομηχανικό κίνδυνο νωρίτερα και με μεγαλύτερη ακρίβεια από τη συμβατική sEMG.', 1),
    ('Altered, potentially less efficient lumbar erector spinae activation during dynamic fatigue in CLBP.',
     'Μεταβολή —πιθανώς λιγότερο αποδοτική— της ενεργοποίησης του οσφυϊκού ορθωτήρα κατά τη δυναμική κόπωση στη χρόνια οσφυαλγία.', 1),
    ('First study to test whether humans can selectively modify trapezius activity using HD-sEMG visual feedback.',
     'Πρώτη μελέτη που εξέτασε αν είναι δυνατή η επιλεκτική τροποποίηση της δραστηριότητας του τραπεζοειδούς με οπτική ανατροφοδότηση HD-sEMG.', 1),

    # ---------- javascript strings ----------
    ("'Show fewer'", "'Λιγότερα'", 2),
    ("'Show all ' + items.length + ' ' + noun", "'Όλες οι ' + items.length + ' ' + noun", 1),
    ("'Show all ' + n + ' publications'", "'Όλες οι ' + n + ' δημοσιεύσεις'", 1),
    ("'Showing all ' + total + ' publications'", "'Εμφανίζονται και οι ' + total + ' δημοσιεύσεις'", 1),
    ("'Showing ' + shown + ' of ' + n + (n === total ? ' publications' : ' matching publications')",
     "'Εμφανίζονται ' + shown + ' από ' + n + (n === total ? ' δημοσιεύσεις' : ' που ταιριάζουν')", 1),
]

# month abbreviations inside the date column only
MONTHS = {
    "Jan": "Ιαν", "Feb": "Φεβ", "Mar": "Μάρ", "Apr": "Απρ", "May": "Μάι", "Jun": "Ιούν",
    "Jul": "Ιούλ", "Aug": "Αύγ", "Sep": "Σεπ", "Oct": "Οκτ", "Nov": "Νοέ", "Dec": "Δεκ",
    "present": "σήμερα",
}
