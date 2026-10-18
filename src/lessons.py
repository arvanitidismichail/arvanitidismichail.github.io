# Interactive lessons for the Teaching section, rendered by build.py (render_lessons).
#
# Each lesson is a small notebook: read, explore (a live model with sliders),
# code, and a one-question check. The code comes in two languages. R runs in the
# page (webR) on the signal being shown. MATLAB cannot run in a web page, so the
# page does the next best thing: the code follows the sliders, an "Output in
# MATLAB" block shows the numbers it gives, and "Download the data" saves the
# very signal on screen as a CSV. Run on that file, either language gives the
# numbers on the page.
#
# To add a lesson, copy an entry and change it; "kind" picks the live model (see
# the "Interactive lessons" block in template.html). Prose may contain simple
# HTML (<b>, <i>, <code>). Lines of code are shared by both languages except for
# their % comments. {win} and {env} are filled in by the page.

UI = {
    "en": dict(
        heading="Interactive lessons",
        intro="Short notebooks for my students: read, play with the model, then run the code on the data you have "
              "just seen: R right here, or MATLAB on your own computer. The model runs in your browser; nothing is "
              "sent anywhere.",
        lesson="Lesson", read="Read", explore="Explore", code="Code", quiz="Check",
        copy="Copy code", copied="Copied", download="Download the data (CSV)",
        out="Output in MATLAB", correct="Correct.", wrong="Not quite.",
        run="Run", reset="Reset", loading="Loading R in your browser (first run only, a few seconds)…",
        running="Running…", edit="Edit the code, then press Run.", rout="Output in R",
        offline="R could not be loaded in this browser. It would give:", error="R reported an error:",
        webr="R runs in your browser with {link}",
    ),
    "el": dict(
        heading="Διαδραστικά μαθήματα",
        intro="Σύντομα notebooks για τους φοιτητές μου: διαβάστε, παίξτε με το μοντέλο και μετά τρέξτε τον κώδικα "
              "πάνω στα δεδομένα που μόλις είδατε: την R εδώ, ή το MATLAB στον δικό σας υπολογιστή. Το μοντέλο τρέχει "
              "στον browser σας· τίποτα δεν στέλνεται πουθενά.",
        lesson="Μάθημα", read="Διαβάστε", explore="Δοκιμάστε", code="Κώδικας", quiz="Έλεγχος",
        copy="Αντιγραφή κώδικα", copied="Αντιγράφηκε", download="Λήψη δεδομένων (CSV)",
        out="Αποτέλεσμα στο MATLAB", correct="Σωστά.", wrong="Όχι ακριβώς.",
        run="Εκτέλεση", reset="Επαναφορά", loading="Φόρτωση της R στον browser σας (μόνο την πρώτη φορά, λίγα δευτερόλεπτα)…",
        running="Εκτέλεση…", edit="Αλλάξτε τον κώδικα και πατήστε Εκτέλεση.", rout="Αποτέλεσμα στην R",
        offline="Η R δεν φόρτωσε σε αυτόν τον browser. Θα έδινε:", error="Η R επέστρεψε σφάλμα:",
        webr="Η R τρέχει στον browser σας με το {link}",
    ),
}

LESSONS = [
    dict(
        id="emg", kind="emg", file="emg_demo.csv",
        en=dict(
            short="EMG amplitude",
            title="From raw EMG to an amplitude",
            read=["Surface EMG swings above and below zero, because the electrode sees the electrical activity of "
                  "many muscle fibres as positive and negative phases. So the <b>average of the raw signal is "
                  "close to zero</b>, however hard the muscle works.",
                  "Two standard fixes: <b>rectify</b> the signal (take absolute values) and average it, or take "
                  "the <b>RMS</b> (root mean square). Computed over a short sliding window, either gives an "
                  "<b>envelope</b> that follows how much the muscle is working."],
            explore="Raw EMG on top; below it the rectified signal and its envelope. Drag the window: a short one "
                    "follows every detail, a long one is smooth but slow, and the peak it reports gets lower.",
            # canvas: raw, rectified, envelope, window, ms, µV ; readout: mean raw, mean rectified, envelope peak
            labels=["Raw EMG", "Rectified EMG", "Envelope", "Window", "ms", "µV",
                    "Mean of raw", "Mean of rectified", "Peak of envelope"],
            env_label="Envelope", env_options=["RMS", "Mean rectified"],
            rcode=["# Demo recording: 5 s of surface EMG at 1000 Hz (µV): the signal shown above",
                   "emg <- scan(\"emg_demo.csv\", quiet = TRUE)",
                   "",
                   "# centred moving average, like MATLAB's movmean (cumulative-sum trick)",
                   "movmean <- function(x, k) {",
                   "  n <- length(x); cs <- c(0, cumsum(x)); i <- 1:n",
                   "  lo <- pmax(1, i - k %/% 2); hi <- pmin(n, i + k - 1 - k %/% 2)",
                   "  (cs[hi + 1] - cs[lo]) / (hi - lo + 1)",
                   "}",
                   "",
                   "win <- {win}                   # window length (ms = samples at 1000 Hz)",
                   "",
                   "rect <- abs(emg)               # 1) full-wave rectification",
                   "{env}",
                   "",
                   "round(c(m_raw = mean(emg), m_rect = mean(rect), peak = max(env)), 4)"],
            renv_code=["env  <- sqrt(movmean(rect^2, win))   # 2) moving RMS",
                       "env  <- movmean(rect, win)            # 2) moving mean of the rectified signal"],
            code_note="The same steps in R (it runs right here, on the signal above) and in MATLAB (copy it, and download "
                      "the 5 s recording to run it yourself). The three values match the ones on this page.",
            code=["% Demo recording: 5 s of surface EMG at 1000 Hz (µV), downloaded from this page",
                  "emg = readmatrix('emg_demo.csv');",
                  "",
                  "win = {win};                    % window length (ms = samples at 1000 Hz)",
                  "",
                  "rect = abs(emg);                % 1) full-wave rectification",
                  "{env}",
                  "",
                  "m_raw  = mean(emg)              % positive and negative phases cancel",
                  "m_rect = mean(rect)             % mean rectified value",
                  "peak   = max(env)               % peak of the envelope"],
            env_code=["env  = sqrt(movmean(rect.^2, win));   % 2) moving RMS",
                      "env  = movmean(rect, win);             % 2) moving mean of the rectified signal"],
            tip="Change <code>win</code> to 20 or 300 and compare <code>peak</code>: it changes with the window "
                "here too.",
            question="Why is the EMG rectified before it is averaged?",
            options=[("To remove noise from the recording.", False,
                      "Rectifying does not remove noise; filtering does. Look at m_raw: the raw mean is nearly 0."),
                     ("Positive and negative phases cancel, so the raw mean is close to zero whatever the effort.", True,
                      "That is why m_raw is almost 0 while m_rect is not."),
                     ("To make the signal larger.", False,
                      "Amplitude is not the point: without rectifying the average would be meaningless, not small.")],
        ),
        el=dict(
            short="Πλάτος EMG",
            title="Από το ακατέργαστο EMG σε ένα μέτρο πλάτους",
            read=["Το επιφανειακό EMG κυμαίνεται πάνω και κάτω από το μηδέν, επειδή το ηλεκτρόδιο «βλέπει» την "
                  "ηλεκτρική δραστηριότητα πολλών μυϊκών ινών ως θετικές και αρνητικές φάσεις. Έτσι ο "
                  "<b>μέσος όρος του ακατέργαστου σήματος είναι κοντά στο μηδέν</b>, όσο έντονα κι αν εργάζεται ο μυς.",
                  "Δύο βασικές λύσεις: <b>ανόρθωση</b> του σήματος (απόλυτες τιμές) και μέσος όρος, ή το "
                  "<b>RMS</b> (τετραγωνική ρίζα του μέσου τετραγώνου). Υπολογισμένα σε ένα κινούμενο παράθυρο, "
                  "δίνουν ένα <b>περίβλημα (envelope)</b> που ακολουθεί πόσο εργάζεται ο μυς."],
            explore="Πάνω το ακατέργαστο EMG· από κάτω το ανορθωμένο σήμα και το περίβλημά του. Σύρετε το παράθυρο: "
                    "ένα μικρό ακολουθεί κάθε λεπτομέρεια, ένα μεγάλο είναι ομαλό αλλά αργό, και η κορυφή που "
                    "αναφέρει μικραίνει.",
            labels=["Ακατέργαστο EMG", "Ανορθωμένο EMG", "Περίβλημα", "Παράθυρο", "ms", "µV",
                    "Μέσος ακατέργαστου", "Μέσος ανορθωμένου", "Κορυφή περιβλήματος"],
            env_label="Περίβλημα", env_options=["RMS", "Μέση ανορθωμένη"],
            rcode=["# Καταγραφή: 5 s επιφανειακού EMG στα 1000 Hz (µV): το σήμα που φαίνεται παραπάνω",
                   "emg <- scan(\"emg_demo.csv\", quiet = TRUE)",
                   "",
                   "# κεντραρισμένος κινούμενος μέσος, όπως το movmean του MATLAB (κόλπο αθροιστικού αθροίσματος)",
                   "movmean <- function(x, k) {",
                   "  n <- length(x); cs <- c(0, cumsum(x)); i <- 1:n",
                   "  lo <- pmax(1, i - k %/% 2); hi <- pmin(n, i + k - 1 - k %/% 2)",
                   "  (cs[hi + 1] - cs[lo]) / (hi - lo + 1)",
                   "}",
                   "",
                   "win <- {win}                   # μήκος παραθύρου (ms = δείγματα στα 1000 Hz)",
                   "",
                   "rect <- abs(emg)               # 1) ανόρθωση πλήρους κύματος",
                   "{env}",
                   "",
                   "round(c(m_raw = mean(emg), m_rect = mean(rect), peak = max(env)), 4)"],
            renv_code=["env  <- sqrt(movmean(rect^2, win))   # 2) κινούμενο RMS",
                       "env  <- movmean(rect, win)            # 2) κινούμενος μέσος του ανορθωμένου"],
            code_note="Τα ίδια βήματα στην R (τρέχει εδώ, πάνω στο σήμα από πάνω) και στο MATLAB (αντιγράψτε το και "
                      "κατεβάστε την καταγραφή των 5 s για να το τρέξετε μόνοι σας). Οι τρεις τιμές ταιριάζουν με της σελίδας.",
            code=["% Καταγραφή: 5 s επιφανειακού EMG στα 1000 Hz (µV), από αυτή τη σελίδα",
                  "emg = readmatrix('emg_demo.csv');",
                  "",
                  "win = {win};                    % μήκος παραθύρου (ms = δείγματα στα 1000 Hz)",
                  "",
                  "rect = abs(emg);                % 1) ανόρθωση πλήρους κύματος",
                  "{env}",
                  "",
                  "m_raw  = mean(emg)              % θετικές και αρνητικές φάσεις αλληλοαναιρούνται",
                  "m_rect = mean(rect)             % μέση ανορθωμένη τιμή",
                  "peak   = max(env)               % κορυφή του περιβλήματος"],
            env_code=["env  = sqrt(movmean(rect.^2, win));   % 2) κινούμενο RMS",
                      "env  = movmean(rect, win);             % 2) κινούμενος μέσος του ανορθωμένου"],
            tip="Αλλάξτε το <code>win</code> σε 20 ή 300 και συγκρίνετε το <code>peak</code>: αλλάζει με το "
                "παράθυρο και εδώ.",
            question="Γιατί ανορθώνουμε το EMG πριν υπολογίσουμε τον μέσο όρο;",
            options=[("Για να αφαιρέσουμε θόρυβο από την καταγραφή.", False,
                      "Η ανόρθωση δεν αφαιρεί θόρυβο· αυτό το κάνει το φιλτράρισμα. Δείτε το m_raw: ο ακατέργαστος μέσος είναι σχεδόν 0."),
                     ("Οι θετικές και οι αρνητικές φάσεις αλληλοαναιρούνται, οπότε ο ακατέργαστος μέσος είναι κοντά στο μηδέν ανεξάρτητα από την προσπάθεια.", True,
                      "Γι' αυτό το m_raw είναι σχεδόν 0 ενώ το m_rect όχι."),
                     ("Για να μεγαλώσει το σήμα.", False,
                      "Το πλάτος δεν είναι το ζητούμενο: χωρίς ανόρθωση ο μέσος όρος θα ήταν άνευ νοήματος, όχι μικρός.")],
        ),
    ),
    dict(
        id="steadiness", kind="force", file="force_demo.csv",
        en=dict(
            short="Force steadiness",
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
            rcode=["# Force (% of maximum), 6 s at 50 Hz: the trace shown above",
                   "force <- scan(\"force_demo.csv\", quiet = TRUE)",
                   "",
                   "m  <- mean(force)              # mean force",
                   "s  <- sd(force)                # standard deviation",
                   "cv <- s / m * 100              # coefficient of variation (%)",
                   "",
                   "round(c(mean = m, sd = s, cv = cv), 2)"],
            code_note="Run it in R right here, or copy the MATLAB and download the force trace on the screen "
                      "(6 s at 50 Hz): the values match the ones on this page.",
            code=["% Force (% of maximum), 6 s at 50 Hz, downloaded from this page",
                  "force = readmatrix('force_demo.csv');",
                  "",
                  "m  = mean(force)                % mean force",
                  "s  = std(force)                 % standard deviation",
                  "cv = s / m * 100                % coefficient of variation (%)"],
            tip="Move the sliders, download again and see how the three values change.",
            question="The SD of the force stays the same but the target level doubles. What happens to the CoV?",
            options=[("It doubles.", False, "Doubling the mean in the denominator does the opposite."),
                     ("It halves.", True, "CoV = SD / mean × 100: the same SD over twice the mean is half the CoV."),
                     ("It stays the same.", False, "It would only stay the same if the SD doubled as well.")],
        ),
        el=dict(
            short="Σταθερότητα δύναμης",
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
            rcode=["# Δύναμη (% του μέγιστου), 6 s στα 50 Hz: η καμπύλη που φαίνεται παραπάνω",
                   "force <- scan(\"force_demo.csv\", quiet = TRUE)",
                   "",
                   "m  <- mean(force)              # μέση δύναμη",
                   "s  <- sd(force)                # τυπική απόκλιση",
                   "cv <- s / m * 100              # συντελεστής μεταβλητότητας (%)",
                   "",
                   "round(c(mean = m, sd = s, cv = cv), 2)"],
            code_note="Τρέξτε το στην R εδώ, ή αντιγράψτε το MATLAB και κατεβάστε την καμπύλη δύναμης που φαίνεται "
                      "(6 s στα 50 Hz): οι τιμές ταιριάζουν με της σελίδας.",
            code=["% Δύναμη (% του μέγιστου), 6 s στα 50 Hz, από αυτή τη σελίδα",
                  "force = readmatrix('force_demo.csv');",
                  "",
                  "m  = mean(force)                % μέση δύναμη",
                  "s  = std(force)                 % τυπική απόκλιση",
                  "cv = s / m * 100                % συντελεστής μεταβλητότητας (%)"],
            tip="Μετακινήστε τα sliders, κατεβάστε ξανά και δείτε πώς αλλάζουν οι τρεις τιμές.",
            question="Η SD της δύναμης μένει ίδια, αλλά το επίπεδο στόχου διπλασιάζεται. Τι γίνεται με τον CoV;",
            options=[("Διπλασιάζεται.", False, "Ο διπλασιασμός του μέσου στον παρονομαστή κάνει το αντίθετο."),
                     ("Υποδιπλασιάζεται.", True, "CoV = SD / μέσος × 100: η ίδια SD πάνω από διπλάσιο μέσο δίνει μισό CoV."),
                     ("Μένει ίδιος.", False, "Θα έμενε ίδιος μόνο αν διπλασιαζόταν και η SD.")],
        ),
    ),

    # ------------------------------------------------------------------ 5. HD-sEMG map
    dict(
        id="map", kind="map", file="hdemg_map.csv",
        en=dict(
            short="HD-sEMG map",
            title="The HD-sEMG map: where is the muscle working?",
            read=["High-density EMG records from a grid of electrodes, so the RMS amplitude at each electrode forms "
                  "a <b>map</b> of activity across the muscle. Where that activity sits, and how it moves, changes "
                  "with fatigue, pain and training.",
                  "Two simple summaries: the <b>peak</b> electrode, and the <b>centroid</b>, the amplitude-weighted "
                  "mean position, <code>x̄ = Σ(amplitude × column) / Σ amplitude</code>. The centroid is less "
                  "sensitive to one noisy electrode and moves smoothly."],
            explore="A grid of 4 rows × 8 columns. Move the hotspot along and across the muscle and widen it; watch "
                    "the peak (circle) and the centroid (cross) follow.",
            labels=["Column (along the muscle)", "Row (across)", "Centroid", "Peak", "Amplitude (µV)",
                    "Centroid column", "Centroid row", "Peak electrode (row, column)", "Mean amplitude", "µV"],
            ctl=[dict(k="along", label="Hotspot along", min=1, max=8, step=0.1, value=5, unit="", dec=1),
                 dict(k="across", label="Hotspot across", min=1, max=4, step=0.1, value=2, unit="", dec=1),
                 dict(k="spread", label="Spread", min=0.5, max=2.5, step=0.1, value=1, unit="", dec=1)],
            code_note="The map as a 4 × 8 matrix (RMS in µV, one value per electrode). The centroid is a weighted "
                      "mean of the column and row numbers.",
            rcode=["M <- as.matrix(read.csv(\"hdemg_map.csv\", header = FALSE))   # 4 rows x 8 columns, RMS (µV)",
                   "",
                   "cx <- sum(M * col(M)) / sum(M)          # centroid: amplitude-weighted mean column",
                   "cy <- sum(M * row(M)) / sum(M)          # ... and mean row",
                   "peak <- which(M == max(M), arr.ind = TRUE)   # the electrode with the highest RMS",
                   "",
                   "round(c(cx = cx, cy = cy, peak_row = peak[1], peak_col = peak[2], mean_amp = mean(M)), 4)"],
            code=["M = readmatrix('hdemg_map.csv');       % 4 rows x 8 columns, RMS (µV)",
                  "[col_no, row_no] = meshgrid(1:size(M, 2), 1:size(M, 1));",
                  "",
                  "cx = sum(M(:) .* col_no(:)) / sum(M(:))     % centroid: amplitude-weighted mean column",
                  "cy = sum(M(:) .* row_no(:)) / sum(M(:))     % ... and mean row",
                  "[~, k] = max(M(:));",
                  "[peak_row, peak_col] = ind2sub(size(M), k) % the electrode with the highest RMS",
                  "mean_amp = mean(M(:))"],
            tip="Move the hotspot to column 7, download again and compare <code>cx</code> with <code>peak_col</code>: "
                "close, but not the same.",
            question="After fatigue the centroid column moves from 3.2 to 5.1. What has changed?",
            options=[("Activity has shifted along the muscle towards the higher-numbered columns.", True,
                      "The centroid is where the activity is centred: a higher column number means it moved that way."),
                     ("The muscle is producing more force.", False,
                      "The centroid says where the activity is, not how much: that is the mean amplitude."),
                     ("One electrode has failed.", False,
                      "A failed electrode changes one value; the centroid shifts smoothly with the whole pattern.")],
        ),
        el=dict(
            short="Χάρτης HD-sEMG",
            title="Ο χάρτης HD-sEMG: πού εργάζεται ο μυς;",
            read=["Το EMG υψηλής πυκνότητας καταγράφει από ένα πλέγμα ηλεκτροδίων, οπότε το πλάτος RMS σε κάθε "
                  "ηλεκτρόδιο σχηματίζει έναν <b>χάρτη</b> δραστηριότητας πάνω στον μυ. Το πού βρίσκεται αυτή η "
                  "δραστηριότητα και πώς μετακινείται αλλάζει με την κόπωση, τον πόνο και την προπόνηση.",
                  "Δύο απλές περιλήψεις: το ηλεκτρόδιο της <b>κορυφής</b> και το <b>κέντρο βάρους</b> (centroid), η "
                  "θέση-μέσος όρος με βάρος το πλάτος, <code>x̄ = Σ(πλάτος × στήλη) / Σ πλάτος</code>. Το centroid "
                  "επηρεάζεται λιγότερο από ένα θορυβώδες ηλεκτρόδιο και κινείται ομαλά."],
            explore="Ένα πλέγμα 4 γραμμών × 8 στηλών. Μετακινήστε το σημείο δραστηριότητας κατά μήκος και κατά πλάτος "
                    "του μυός και διευρύνετέ το· δείτε την κορυφή (κύκλος) και το centroid (σταυρός) να ακολουθούν.",
            labels=["Στήλη (κατά μήκος του μυός)", "Γραμμή (κατά πλάτος)", "Centroid", "Κορυφή", "Πλάτος (µV)",
                    "Στήλη centroid", "Γραμμή centroid", "Ηλεκτρόδιο κορυφής (γραμμή, στήλη)", "Μέσο πλάτος", "µV"],
            ctl=[dict(k="along", label="Θέση κατά μήκος", min=1, max=8, step=0.1, value=5, unit="", dec=1),
                 dict(k="across", label="Θέση κατά πλάτος", min=1, max=4, step=0.1, value=2, unit="", dec=1),
                 dict(k="spread", label="Εύρος", min=0.5, max=2.5, step=0.1, value=1, unit="", dec=1)],
            code_note="Ο χάρτης ως πίνακας 4 × 8 (RMS σε µV, μία τιμή ανά ηλεκτρόδιο). Το centroid είναι ένας σταθμισμένος "
                      "μέσος των αριθμών στήλης και γραμμής.",
            rcode=["M <- as.matrix(read.csv(\"hdemg_map.csv\", header = FALSE))   # 4 γραμμές x 8 στήλες, RMS (µV)",
                   "",
                   "cx <- sum(M * col(M)) / sum(M)          # centroid: μέση στήλη σταθμισμένη με το πλάτος",
                   "cy <- sum(M * row(M)) / sum(M)          # ... και μέση γραμμή",
                   "peak <- which(M == max(M), arr.ind = TRUE)   # το ηλεκτρόδιο με το υψηλότερο RMS",
                   "",
                   "round(c(cx = cx, cy = cy, peak_row = peak[1], peak_col = peak[2], mean_amp = mean(M)), 4)"],
            code=["M = readmatrix('hdemg_map.csv');       % 4 γραμμές x 8 στήλες, RMS (µV)",
                  "[col_no, row_no] = meshgrid(1:size(M, 2), 1:size(M, 1));",
                  "",
                  "cx = sum(M(:) .* col_no(:)) / sum(M(:))     % centroid: μέση στήλη σταθμισμένη με το πλάτος",
                  "cy = sum(M(:) .* row_no(:)) / sum(M(:))     % ... και μέση γραμμή",
                  "[~, k] = max(M(:));",
                  "[peak_row, peak_col] = ind2sub(size(M), k) % το ηλεκτρόδιο με το υψηλότερο RMS",
                  "mean_amp = mean(M(:))"],
            tip="Μετακινήστε το σημείο δραστηριότητας στη στήλη 7, κατεβάστε ξανά και συγκρίνετε το <code>cx</code> με το "
                "<code>peak_col</code>: κοντά, αλλά όχι ίδια.",
            question="Μετά την κόπωση η στήλη του centroid μετακινείται από 3,2 σε 5,1. Τι έχει αλλάξει;",
            options=[("Η δραστηριότητα έχει μετατοπιστεί κατά μήκος του μυός προς τις στήλες με μεγαλύτερο αριθμό.", True,
                      "Το centroid είναι εκεί όπου επικεντρώνεται η δραστηριότητα: μεγαλύτερος αριθμός στήλης σημαίνει ότι μετακινήθηκε προς τα εκεί."),
                     ("Ο μυς παράγει περισσότερη δύναμη.", False,
                      "Το centroid λέει πού βρίσκεται η δραστηριότητα, όχι πόση είναι: αυτό το δείχνει το μέσο πλάτος."),
                     ("Ένα ηλεκτρόδιο έχει χαλάσει.", False,
                      "Ένα χαλασμένο ηλεκτρόδιο αλλάζει μία τιμή· το centroid μετατοπίζεται ομαλά με ολόκληρο το μοτίβο.")],
        ),
    ),
]
