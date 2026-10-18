# Interactive lessons for the Teaching section, rendered by build.py (render_lessons).
#
# Each lesson is a small notebook: read, explore (a live model with sliders),
# run R in the page, answer a question. To add a lesson, copy one entry and
# change it; "kind" picks the live model (see the .lab script in template.html).
#
# Prose may contain simple HTML (<b>, <i>, <code>). The R code is shared by both
# languages; only its comments differ. "out" is what R prints, shown if R cannot
# be loaded in the visitor's browser: regenerate it with Rscript when you edit a chunk.

UI = {
    "en": dict(
        heading="Interactive lessons",
        intro="Short notebooks for my students: read, play with the model, then run the R yourself. "
              "They run entirely in your browser; nothing is installed or sent anywhere.",
        lesson="Lesson", read="Read", explore="Explore", code="R code", quiz="Check",
        run="Run", reset="Reset", loading="Loading R in your browser (first run only, a few seconds)…",
        running="Running…", out="Output", offline="R could not be loaded in this browser. Expected output:",
        error="R reported an error:", edit="Edit the code, then press Run.",
        correct="Correct.", wrong="Not quite.", webr="R runs in your browser with {link}",
    ),
    "el": dict(
        heading="Διαδραστικά μαθήματα",
        intro="Σύντομα notebooks για τους φοιτητές μου: διαβάστε, παίξτε με το μοντέλο και μετά τρέξτε μόνοι σας "
              "τον κώδικα R. Τρέχουν εξ ολοκλήρου στον browser σας· τίποτα δεν εγκαθίσταται και τίποτα δεν στέλνεται.",
        lesson="Μάθημα", read="Διαβάστε", explore="Δοκιμάστε", code="Κώδικας R", quiz="Έλεγχος",
        run="Εκτέλεση", reset="Επαναφορά", loading="Φόρτωση της R στον browser σας (μόνο την πρώτη φορά, λίγα δευτερόλεπτα)…",
        running="Εκτέλεση…", out="Αποτέλεσμα", offline="Η R δεν φόρτωσε σε αυτόν τον browser. Αναμενόμενο αποτέλεσμα:",
        error="Η R επέστρεψε σφάλμα:", edit="Αλλάξτε τον κώδικα και πατήστε Εκτέλεση.",
        correct="Σωστά.", wrong="Όχι ακριβώς.", webr="Η R τρέχει στον browser σας με το {link}",
    ),
}

LESSONS = [
    dict(
        id="emg", kind="emg",
        en=dict(
            title="From raw EMG to an amplitude",
            read=["Surface EMG swings above and below zero, because the electrode sees the electrical activity of "
                  "many muscle fibres as positive and negative phases. So the <b>average of the raw signal is "
                  "close to zero</b>, however hard the muscle works.",
                  "Two standard fixes: <b>rectify</b> the signal (take absolute values) and average it, or take "
                  "the <b>RMS</b> (root mean square). Computed over a short sliding window, either gives an "
                  "<b>envelope</b> that follows how much the muscle is working."],
            explore="Drag the window: a short one follows every detail, a long one is smooth but slow. "
                    "Switch rectification on to see the negative half folded up.",
            labels=["Raw EMG", "Envelope (RMS)", "Window", "ms"], rectify="Rectify",
            code_note="Ten samples of a raw signal (µV). Compare the three ways of averaging them:",
            code=["# Ten samples of raw EMG (microvolts)",
                  "emg <- c(-42, 65, -18, 90, -75, 31, -58, 77, -26, 48)",
                  "",
                  "mean(emg)               # raw: positive and negative cancel",
                  "rectified <- abs(emg)   # full-wave rectification",
                  "mean(rectified)         # mean rectified value",
                  "sqrt(mean(emg^2))       # RMS"],
            out="[1] 9.2\n[1] 53\n[1] 57.68189",
            tip="Try changing a number, or add <code>max(rectified)</code> on a new line.",
            question="Why is the EMG rectified before it is averaged?",
            options=[("To remove noise from the recording.", False,
                      "Rectifying does not remove noise; filtering does. Look at the first result: the raw mean is nearly 0."),
                     ("Positive and negative phases cancel, so the raw mean is close to zero whatever the effort.", True,
                      "The raw mean above is 9.2 µV, while the rectified mean is 53 µV."),
                     ("To make the signal larger.", False,
                      "Amplitude is not the point: without rectifying the average would be meaningless, not small.")],
        ),
        el=dict(
            title="Από το ακατέργαστο EMG σε ένα μέτρο πλάτους",
            read=["Το επιφανειακό EMG κυμαίνεται πάνω και κάτω από το μηδέν, επειδή το ηλεκτρόδιο «βλέπει» την "
                  "ηλεκτρική δραστηριότητα πολλών μυϊκών ινών ως θετικές και αρνητικές φάσεις. Έτσι ο "
                  "<b>μέσος όρος του ακατέργαστου σήματος είναι κοντά στο μηδέν</b>, όσο έντονα κι αν εργάζεται ο μυς.",
                  "Δύο βασικές λύσεις: <b>ανόρθωση</b> του σήματος (απόλυτες τιμές) και μέσος όρος, ή το "
                  "<b>RMS</b> (τετραγωνική ρίζα του μέσου τετραγώνου). Υπολογισμένα σε ένα κινούμενο παράθυρο, "
                  "δίνουν ένα <b>περίβλημα (envelope)</b> που ακολουθεί πόσο εργάζεται ο μυς."],
            explore="Σύρετε το παράθυρο: ένα μικρό ακολουθεί κάθε λεπτομέρεια, ένα μεγάλο είναι ομαλό αλλά αργό. "
                    "Ενεργοποιήστε την ανόρθωση για να δείτε το αρνητικό μισό να διπλώνει προς τα πάνω.",
            labels=["Ακατέργαστο EMG", "Περίβλημα (RMS)", "Παράθυρο", "ms"], rectify="Ανόρθωση",
            code_note="Δέκα δείγματα ενός ακατέργαστου σήματος (µV). Συγκρίνετε τους τρεις τρόπους μέσου όρου:",
            code=["# Δέκα δείγματα ακατέργαστου EMG (μV)",
                  "emg <- c(-42, 65, -18, 90, -75, 31, -58, 77, -26, 48)",
                  "",
                  "mean(emg)               # ακατέργαστο: θετικά και αρνητικά αλληλοαναιρούνται",
                  "rectified <- abs(emg)   # ανόρθωση πλήρους κύματος",
                  "mean(rectified)         # μέση ανορθωμένη τιμή",
                  "sqrt(mean(emg^2))       # RMS"],
            out="[1] 9.2\n[1] 53\n[1] 57.68189",
            tip="Δοκιμάστε να αλλάξετε έναν αριθμό ή προσθέστε <code>max(rectified)</code> σε νέα γραμμή.",
            question="Γιατί ανορθώνουμε το EMG πριν υπολογίσουμε τον μέσο όρο;",
            options=[("Για να αφαιρέσουμε θόρυβο από την καταγραφή.", False,
                      "Η ανόρθωση δεν αφαιρεί θόρυβο· αυτό το κάνει το φιλτράρισμα. Δείτε το πρώτο αποτέλεσμα: ο ακατέργαστος μέσος είναι σχεδόν 0."),
                     ("Οι θετικές και οι αρνητικές φάσεις αλληλοαναιρούνται, οπότε ο ακατέργαστος μέσος είναι κοντά στο μηδέν ανεξάρτητα από την προσπάθεια.", True,
                      "Ο ακατέργαστος μέσος παραπάνω είναι 9,2 μV, ενώ ο ανορθωμένος 53 μV."),
                     ("Για να μεγαλώσει το σήμα.", False,
                      "Το πλάτος δεν είναι το ζητούμενο: χωρίς ανόρθωση ο μέσος όρος θα ήταν άνευ νοήματος, όχι μικρός.")],
        ),
    ),
    dict(
        id="steadiness", kind="force",
        en=dict(
            title="Force steadiness and the coefficient of variation",
            read=["Hold a muscle at a fixed force and the force still wobbles. How much it wobbles is the "
                  "<b>force steadiness</b>, and it is a sensitive marker of how well the nervous system controls "
                  "the muscle; it worsens with fatigue, ageing and pain.",
                  "It is usually reported as the <b>coefficient of variation</b> (CoV): the standard deviation "
                  "<i>relative to the mean</i>, <code>CoV = SD / mean × 100</code>. Dividing by the mean makes "
                  "holds at different force levels comparable."],
            explore="Raise the variability and the trace wobbles more. Then move the target level and watch what "
                    "happens to the CoV when the SD stays the same.",
            labels=["Force", "Target", "Variability (SD)", "Target level", "CoV", "% MVC", "SD", "Mean"],
            code_note="Force (% of maximum) sampled during a hold at a target of 20 %:",
            code=["# Force (% of maximum) while holding a target of 20 %",
                  "force <- c(19.2, 20.5, 21.1, 18.8, 20.3, 19.6, 21.4, 18.5, 20.9, 19.7)",
                  "",
                  "m  <- mean(force)",
                  "s  <- sd(force)",
                  "cv <- s / m * 100        # coefficient of variation (%)",
                  "round(c(mean = m, sd = s, cv = cv), 2)"],
            out=" mean    sd    cv \n20.00  0.99  4.97 ",
            tip="Change the target to 40 (and the numbers with it) and run again.",
            question="The SD of the force stays the same but the target level doubles. What happens to the CoV?",
            options=[("It doubles.", False, "Doubling the mean in the denominator does the opposite."),
                     ("It halves.", True, "CoV = SD / mean × 100: the same SD over twice the mean is half the CoV."),
                     ("It stays the same.", False, "It would only stay the same if the SD doubled as well.")],
        ),
        el=dict(
            title="Σταθερότητα δύναμης και συντελεστής μεταβλητότητας",
            read=["Κρατήστε έναν μυ σε σταθερή δύναμη και η δύναμη εξακολουθεί να ταλαντώνεται. Πόσο ταλαντώνεται "
                  "είναι η <b>σταθερότητα δύναμης</b>, ένας ευαίσθητος δείκτης του πόσο καλά ελέγχει το νευρικό "
                  "σύστημα τον μυ· χειροτερεύει με την κόπωση, τη γήρανση και τον πόνο.",
                  "Συνήθως αναφέρεται ως <b>συντελεστής μεταβλητότητας</b> (CoV): η τυπική απόκλιση "
                  "<i>σε σχέση με τον μέσο όρο</i>, <code>CoV = SD / μέσος × 100</code>. Η διαίρεση με τον μέσο "
                  "καθιστά συγκρίσιμες τις συσπάσεις σε διαφορετικά επίπεδα δύναμης."],
            explore="Αυξήστε τη μεταβλητότητα και η καμπύλη ταλαντώνεται περισσότερο. Μετά αλλάξτε το επίπεδο "
                    "στόχου και δείτε τι γίνεται με τον CoV όταν η SD μένει ίδια.",
            labels=["Δύναμη", "Στόχος", "Μεταβλητότητα (SD)", "Επίπεδο στόχου", "CoV", "% MVC", "SD", "Μέσος"],
            code_note="Δύναμη (% του μέγιστου) που καταγράφηκε κατά τη διατήρηση στόχου 20 %:",
            code=["# Δύναμη (% του μέγιστου) κατά τη διατήρηση στόχου 20 %",
                  "force <- c(19.2, 20.5, 21.1, 18.8, 20.3, 19.6, 21.4, 18.5, 20.9, 19.7)",
                  "",
                  "m  <- mean(force)",
                  "s  <- sd(force)",
                  "cv <- s / m * 100        # συντελεστής μεταβλητότητας (%)",
                  "round(c(mean = m, sd = s, cv = cv), 2)"],
            out=" mean    sd    cv \n20.00  0.99  4.97 ",
            tip="Αλλάξτε τον στόχο σε 40 (και τους αριθμούς μαζί του) και τρέξτε ξανά.",
            question="Η SD της δύναμης μένει ίδια, αλλά το επίπεδο στόχου διπλασιάζεται. Τι γίνεται με τον CoV;",
            options=[("Διπλασιάζεται.", False, "Ο διπλασιασμός του μέσου στον παρονομαστή κάνει το αντίθετο."),
                     ("Υποδιπλασιάζεται.", True, "CoV = SD / μέσος × 100: η ίδια SD πάνω από διπλάσιο μέσο δίνει μισό CoV."),
                     ("Μένει ίδιος.", False, "Θα έμενε ίδιος μόνο αν διπλασιαζόταν και η SD.")],
        ),
    ),
]
