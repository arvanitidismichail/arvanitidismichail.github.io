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

    # ------------------------------------------------------------------ 3. filtering
    dict(
        id="filter", kind="filter", file="emg_filter_demo.csv", matlab_out=False,
        en=dict(
            short="Filtering",
            title="Filtering EMG: keeping the muscle, removing the rest",
            read=["A raw EMG recording carries more than muscle activity: slow <b>movement artefact</b> and cable "
                  "sway (below about 10–20 Hz) and <b>mains interference</b>, a sharp spike at 50 Hz (60 Hz in some "
                  "countries). The muscle signal itself lives mostly between about 20 and 450 Hz.",
                  "So the standard pipeline is a <b>high-pass</b> filter around 20 Hz, a <b>low-pass</b> filter near "
                  "450 Hz and, if needed, a <b>notch</b> at the mains frequency. Filtering forwards and then "
                  "backwards (<i>zero-phase</i>) stops the signal being shifted in time."],
            explore="The recording has slow drift and a 50 Hz hum added to the EMG. Move the cut-offs and watch the "
                    "filtered trace and the spectrum change. Raise the high-pass too far and you start cutting into "
                    "the EMG itself.",
            labels=["Recorded (µV)", "Filtered (µV)", "Spectrum (dB)", "µV", "Hz", "Recorded", "Filtered",
                    "RMS recorded", "RMS filtered", "50 Hz recorded", "50 Hz filtered"],
            ctl=[dict(k="hp", label="High-pass", min=1, max=80, step=1, value=20, unit="Hz"),
                 dict(k="lp", label="Low-pass", min=100, max=450, step=10, value=450, unit="Hz"),
                 dict(k="notch", label="Notch 50 Hz", check=True, value=True)],
            code_note="Zero-phase second-order Butterworth filters. In R they are written out so you can see what "
                      "they do; MATLAB's butter and filtfilt (Signal Processing Toolbox) do the same job. Values are "
                      "measured on the middle of the recording (0.5 to 4.5 s), away from the filter start-up. "
                      "MATLAB pads the ends differently, so expect tiny differences there.",
            rcode=["fs <- 1000",
                   "x  <- scan(\"emg_filter_demo.csv\", quiet = TRUE)   # as recorded: EMG + drift + 50 Hz hum (µV)",
                   "",
                   "hp <- {hp}                 # high-pass cut-off (Hz)",
                   "lp <- {lp}                # low-pass cut-off (Hz)",
                   "use_notch <- {notch}       # remove the 50 Hz mains?",
                   "",
                   "# second-order filters, applied forwards then backwards (zero phase)",
                   "butter2 <- function(fc, fs, type) {",
                   "  K <- tan(pi * fc / fs); n <- 1 / (1 + sqrt(2) * K + K^2)",
                   "  list(b = if (type == \"high\") n * c(1, -2, 1) else n * K^2 * c(1, 2, 1),",
                   "       a = c(1, 2 * (K^2 - 1) * n, (1 - sqrt(2) * K + K^2) * n))",
                   "}",
                   "notch <- function(f0, fs, Q = 35) {",
                   "  w0 <- 2 * pi * f0 / fs; be <- tan(w0 / Q / 2)",
                   "  list(b = c(1, -2 * cos(w0), 1) / (1 + be), a = c(1, -2 * cos(w0) / (1 + be), (1 - be) / (1 + be)))",
                   "}",
                   "once <- function(f, x) {",
                   "  v <- stats::filter(c(0, 0, x), f$b, sides = 1)[-(1:2)]",
                   "  as.numeric(stats::filter(v, -f$a[2:3], method = \"recursive\"))",
                   "}",
                   "zerophase <- function(f, x) rev(once(f, rev(once(f, x))))",
                   "",
                   "y <- x",
                   "if (use_notch) y <- zerophase(notch(50, fs), y)",
                   "y <- zerophase(butter2(hp, fs, \"high\"), y)",
                   "y <- zerophase(butter2(lp, fs, \"low\"), y)",
                   "",
                   "keep <- 501:4500            # skip the first and last 0.5 s, where the filters start up",
                   "amp <- function(v, f0) 2 * Mod(sum(v * exp(-2i * pi * f0 * (seq_along(v) - 1) / fs))) / length(v)",
                   "round(c(rms_before = sqrt(mean(x[keep]^2)), rms_after = sqrt(mean(y[keep]^2)),",
                   "        amp50_before = amp(x[keep], 50), amp50_after = amp(y[keep], 50)), 4)"],
            code=["fs = 1000;",
                  "x  = readmatrix('emg_filter_demo.csv');   % as recorded: EMG + drift + 50 Hz hum (µV)",
                  "",
                  "hp = {hp};                 % high-pass cut-off (Hz)",
                  "lp = {lp};                % low-pass cut-off (Hz)",
                  "use_notch = {notch};       % remove the 50 Hz mains?",
                  "",
                  "y = x;",
                  "if use_notch",
                  "    [b, a] = iirnotch(50/(fs/2), (50/(fs/2))/35);",
                  "    y = filtfilt(b, a, y);",
                  "end",
                  "[b, a] = butter(2, hp/(fs/2), 'high');  y = filtfilt(b, a, y);",
                  "[b, a] = butter(2, lp/(fs/2), 'low');   y = filtfilt(b, a, y);",
                  "",
                  "keep = 501:4500;           % skip the first and last 0.5 s",
                  "amp = @(v, f0) 2 * abs(sum(v(:) .* exp(-2i*pi*f0*(0:numel(v)-1)'/fs))) / numel(v);",
                  "rms_before   = sqrt(mean(x(keep).^2))",
                  "rms_after    = sqrt(mean(y(keep).^2))",
                  "amp50_before = amp(x(keep), 50)",
                  "amp50_after  = amp(y(keep), 50)"],
            tip="Try <code>hp</code> = 5, 20 and 80 and compare <code>rms_after</code>: the 80 Hz high-pass "
                "removes real EMG as well.",
            question="You raise the high-pass cut-off from 20 Hz to 80 Hz. What happens?",
            options=[("Nothing important: everything below 80 Hz was noise anyway.", False,
                      "Most EMG power lies between about 20 and 150 Hz, so a lot of real signal goes too: watch the filtered RMS fall."),
                     ("Part of the EMG itself is removed, so the filtered amplitude drops.", True,
                      "That is why the high-pass sits near 20 Hz: it must remove the artefact without cutting into the muscle's signal."),
                     ("The slow movement artefact comes back.", False,
                      "A higher cut-off removes even more of the slow drift, not less.")],
        ),
        el=dict(
            short="Φιλτράρισμα",
            title="Φιλτράρισμα EMG: κρατάμε τον μυ, αφαιρούμε τα υπόλοιπα",
            read=["Μια ακατέργαστη καταγραφή EMG περιέχει κάτι παραπάνω από τη μυϊκή δραστηριότητα: αργά "
                  "<b>τεχνήματα κίνησης</b> και ταλάντωση του καλωδίου (κάτω από περίπου 10–20 Hz) και "
                  "<b>παρεμβολή από το ρεύμα</b>, μια οξεία κορυφή στα 50 Hz (60 Hz σε ορισμένες χώρες). Το ίδιο το "
                  "μυϊκό σήμα βρίσκεται κυρίως μεταξύ περίπου 20 και 450 Hz.",
                  "Έτσι η συνηθισμένη διαδικασία είναι ένα φίλτρο <b>υψηλών συχνοτήτων</b> γύρω στα 20 Hz, ένα "
                  "φίλτρο <b>χαμηλών συχνοτήτων</b> κοντά στα 450 Hz και, αν χρειάζεται, ένα <b>notch</b> στη "
                  "συχνότητα του ρεύματος. Το φιλτράρισμα μπροστά και μετά πίσω (<i>μηδενικής φάσης</i>) δεν "
                  "μετατοπίζει το σήμα στον χρόνο."],
            explore="Στην καταγραφή έχουν προστεθεί αργή μετατόπιση και βόμβος 50 Hz. Μετακινήστε τις συχνότητες "
                    "αποκοπής και δείτε το φιλτραρισμένο σήμα και το φάσμα να αλλάζουν. Αν ανεβάσετε πολύ το φίλτρο "
                    "υψηλών συχνοτήτων, αρχίζετε να κόβετε το ίδιο το EMG.",
            labels=["Καταγραφή (µV)", "Φιλτραρισμένο (µV)", "Φάσμα (dB)", "µV", "Hz", "Καταγραφή", "Φιλτραρισμένο",
                    "RMS καταγραφής", "RMS φιλτραρισμένου", "50 Hz καταγραφής", "50 Hz φιλτραρισμένου"],
            ctl=[dict(k="hp", label="Υψηλές συχν.", min=1, max=80, step=1, value=20, unit="Hz"),
                 dict(k="lp", label="Χαμηλές συχν.", min=100, max=450, step=10, value=450, unit="Hz"),
                 dict(k="notch", label="Notch 50 Hz", check=True, value=True)],
            code_note="Φίλτρα Butterworth δεύτερης τάξης μηδενικής φάσης. Στην R είναι γραμμένα ολόκληρα, ώστε να "
                      "φαίνεται τι κάνουν· το butter και το filtfilt του MATLAB (Signal Processing Toolbox) κάνουν την "
                      "ίδια δουλειά. Οι τιμές μετρούνται στη μέση της καταγραφής (0,5 έως 4,5 s), μακριά από την "
                      "εκκίνηση των φίλτρων. Το MATLAB χειρίζεται τα άκρα διαφορετικά, οπότε περιμένετε μικρές "
                      "διαφορές εκεί.",
            rcode=["fs <- 1000",
                   "x  <- scan(\"emg_filter_demo.csv\", quiet = TRUE)   # όπως καταγράφηκε: EMG + μετατόπιση + βόμβος 50 Hz (µV)",
                   "",
                   "hp <- {hp}                 # συχνότητα αποκοπής υψηλών (Hz)",
                   "lp <- {lp}                # συχνότητα αποκοπής χαμηλών (Hz)",
                   "use_notch <- {notch}       # αφαίρεση των 50 Hz του ρεύματος;",
                   "",
                   "# φίλτρα δεύτερης τάξης, μπροστά και μετά πίσω (μηδενική φάση)",
                   "butter2 <- function(fc, fs, type) {",
                   "  K <- tan(pi * fc / fs); n <- 1 / (1 + sqrt(2) * K + K^2)",
                   "  list(b = if (type == \"high\") n * c(1, -2, 1) else n * K^2 * c(1, 2, 1),",
                   "       a = c(1, 2 * (K^2 - 1) * n, (1 - sqrt(2) * K + K^2) * n))",
                   "}",
                   "notch <- function(f0, fs, Q = 35) {",
                   "  w0 <- 2 * pi * f0 / fs; be <- tan(w0 / Q / 2)",
                   "  list(b = c(1, -2 * cos(w0), 1) / (1 + be), a = c(1, -2 * cos(w0) / (1 + be), (1 - be) / (1 + be)))",
                   "}",
                   "once <- function(f, x) {",
                   "  v <- stats::filter(c(0, 0, x), f$b, sides = 1)[-(1:2)]",
                   "  as.numeric(stats::filter(v, -f$a[2:3], method = \"recursive\"))",
                   "}",
                   "zerophase <- function(f, x) rev(once(f, rev(once(f, x))))",
                   "",
                   "y <- x",
                   "if (use_notch) y <- zerophase(notch(50, fs), y)",
                   "y <- zerophase(butter2(hp, fs, \"high\"), y)",
                   "y <- zerophase(butter2(lp, fs, \"low\"), y)",
                   "",
                   "keep <- 501:4500            # παράλειψη του πρώτου και τελευταίου 0,5 s, όπου ξεκινούν τα φίλτρα",
                   "amp <- function(v, f0) 2 * Mod(sum(v * exp(-2i * pi * f0 * (seq_along(v) - 1) / fs))) / length(v)",
                   "round(c(rms_before = sqrt(mean(x[keep]^2)), rms_after = sqrt(mean(y[keep]^2)),",
                   "        amp50_before = amp(x[keep], 50), amp50_after = amp(y[keep], 50)), 4)"],
            code=["fs = 1000;",
                  "x  = readmatrix('emg_filter_demo.csv');   % όπως καταγράφηκε: EMG + μετατόπιση + βόμβος 50 Hz (µV)",
                  "",
                  "hp = {hp};                 % συχνότητα αποκοπής υψηλών (Hz)",
                  "lp = {lp};                % συχνότητα αποκοπής χαμηλών (Hz)",
                  "use_notch = {notch};       % αφαίρεση των 50 Hz του ρεύματος;",
                  "",
                  "y = x;",
                  "if use_notch",
                  "    [b, a] = iirnotch(50/(fs/2), (50/(fs/2))/35);",
                  "    y = filtfilt(b, a, y);",
                  "end",
                  "[b, a] = butter(2, hp/(fs/2), 'high');  y = filtfilt(b, a, y);",
                  "[b, a] = butter(2, lp/(fs/2), 'low');   y = filtfilt(b, a, y);",
                  "",
                  "keep = 501:4500;           % παράλειψη του πρώτου και τελευταίου 0,5 s",
                  "amp = @(v, f0) 2 * abs(sum(v(:) .* exp(-2i*pi*f0*(0:numel(v)-1)'/fs))) / numel(v);",
                  "rms_before   = sqrt(mean(x(keep).^2))",
                  "rms_after    = sqrt(mean(y(keep).^2))",
                  "amp50_before = amp(x(keep), 50)",
                  "amp50_after  = amp(y(keep), 50)"],
            tip="Δοκιμάστε <code>hp</code> = 5, 20 και 80 και συγκρίνετε το <code>rms_after</code>: το φίλτρο των "
                "80 Hz αφαιρεί και πραγματικό EMG.",
            question="Ανεβάζετε τη συχνότητα αποκοπής του φίλτρου υψηλών συχνοτήτων από 20 Hz σε 80 Hz. Τι γίνεται;",
            options=[("Τίποτα σημαντικό: ό,τι ήταν κάτω από 80 Hz ήταν θόρυβος ούτως ή άλλως.", False,
                      "Το μεγαλύτερο μέρος της ισχύος του EMG βρίσκεται περίπου μεταξύ 20 και 150 Hz, οπότε φεύγει και πολύ πραγματικό σήμα: δείτε το RMS του φιλτραρισμένου να πέφτει."),
                     ("Αφαιρείται μέρος του ίδιου του EMG, οπότε το φιλτραρισμένο πλάτος μειώνεται.", True,
                      "Γι' αυτό το φίλτρο υψηλών συχνοτήτων μπαίνει κοντά στα 20 Hz: πρέπει να αφαιρεί το τέχνημα χωρίς να κόβει το σήμα του μυός."),
                     ("Το αργό τέχνημα κίνησης επιστρέφει.", False,
                      "Μια υψηλότερη συχνότητα αποκοπής αφαιρεί περισσότερο, όχι λιγότερο, από την αργή μετατόπιση.")],
        ),
    ),
    # ------------------------------------------------------------------ 4. normalisation
    dict(
        id="mvc", kind="mvc", file="mvc_demo.csv",
        en=dict(
            short="Normalisation",
            title="Normalising EMG to a maximal contraction",
            read=["The size of an EMG signal depends on things that have nothing to do with how hard the muscle "
                  "works: electrode position, skin, the fat layer, even the amplifier gain. So raw amplitudes from "
                  "different people, days or muscles <b>cannot be compared directly</b>.",
                  "The usual fix is to record a <b>maximal voluntary contraction</b> (MVC) and express the task as a "
                  "percentage of it: <code>%MVC = RMS(task) / RMS(MVC) × 100</code>. A change of gain scales both "
                  "recordings, so it cancels in the ratio."],
            explore="Two trials: the maximal contraction and a submaximal task. Change the electrode gain and watch "
                    "the raw amplitudes move while %MVC stays put; change the effort and %MVC follows.",
            labels=["MVC trial (µV)", "Task (µV)", "RMS", "µV", "RMS of MVC", "RMS of task", "Task as %MVC"],
            ctl=[dict(k="gain", label="Electrode gain", min=0.5, max=2, step=0.05, value=1, unit="×", dec=2),
                 dict(k="effort", label="Effort", min=10, max=60, step=1, value=30, unit="% MVC")],
            code_note="Download the two trials (3 s each, 1000 Hz) and compute the amplitude of the steady part of each.",
            rcode=["d <- read.csv(\"mvc_demo.csv\")      # two trials, 3 s at 1000 Hz (µV)",
                   "plateau <- 1001:2500                # the steady part of each contraction",
                   "rms <- function(x) sqrt(mean(x^2))",
                   "",
                   "rms_mvc  <- rms(d$mvc[plateau])     # maximal voluntary contraction",
                   "rms_task <- rms(d$task[plateau])    # the task",
                   "pct_mvc  <- rms_task / rms_mvc * 100   # task amplitude as % of MVC",
                   "",
                   "round(c(rms_mvc = rms_mvc, rms_task = rms_task, pct_mvc = pct_mvc), 4)"],
            code=["d = readtable('mvc_demo.csv');     % two trials, 3 s at 1000 Hz (µV)",
                  "plateau = 1001:2500;               % the steady part of each contraction",
                  "",
                  "rms_mvc  = sqrt(mean(d.mvc(plateau).^2))       % maximal voluntary contraction",
                  "rms_task = sqrt(mean(d.task(plateau).^2))      % the task",
                  "pct_mvc  = rms_task / rms_mvc * 100            % task amplitude as % of MVC"],
            tip="Move the gain, download again: the two RMS values change, but <code>pct_mvc</code> does not.",
            question="A second participant's electrodes give twice the amplitude for the same muscle effort. After "
                     "normalising to MVC, how do the two participants' task amplitudes compare?",
            options=[("Participant 2 shows twice the %MVC.", False,
                      "Both trials, the MVC and the task, are doubled, so the doubling cancels in the ratio."),
                     ("They are the same: the gain cancels in the ratio.", True,
                      "That is the point of normalising: %MVC does not depend on the gain."),
                     ("They cannot be compared at all.", False,
                      "Raw amplitudes cannot, but %MVC can.")],
        ),
        el=dict(
            short="Κανονικοποίηση",
            title="Κανονικοποίηση του EMG σε μέγιστη σύσπαση",
            read=["Το μέγεθος ενός σήματος EMG εξαρτάται από πράγματα που δεν έχουν σχέση με το πόσο εργάζεται ο "
                  "μυς: θέση ηλεκτροδίου, δέρμα, λιπώδης ιστός, ακόμη και το κέρδος του ενισχυτή. Γι' αυτό τα "
                  "ακατέργαστα πλάτη από διαφορετικά άτομα, ημέρες ή μύες <b>δεν συγκρίνονται άμεσα</b>.",
                  "Η συνηθισμένη λύση είναι να καταγράψουμε μια <b>μέγιστη εκούσια σύσπαση</b> (MVC) και να "
                  "εκφράσουμε την εργασία ως ποσοστό της: <code>%MVC = RMS(εργασίας) / RMS(MVC) × 100</code>. Μια "
                  "αλλαγή στο κέρδος πολλαπλασιάζει και τις δύο καταγραφές, οπότε απλοποιείται στον λόγο."],
            explore="Δύο δοκιμές: η μέγιστη σύσπαση και μια υπομέγιστη εργασία. Αλλάξτε το κέρδος των ηλεκτροδίων "
                    "και δείτε τα ακατέργαστα πλάτη να κινούνται ενώ το %MVC μένει ίδιο· αλλάξτε την προσπάθεια και "
                    "το %MVC ακολουθεί.",
            labels=["Δοκιμή MVC (µV)", "Εργασία (µV)", "RMS", "µV", "RMS της MVC", "RMS της εργασίας", "Εργασία ως %MVC"],
            ctl=[dict(k="gain", label="Κέρδος ηλεκτροδίων", min=0.5, max=2, step=0.05, value=1, unit="×", dec=2),
                 dict(k="effort", label="Προσπάθεια", min=10, max=60, step=1, value=30, unit="% MVC")],
            code_note="Κατεβάστε τις δύο δοκιμές (3 s η καθεμία, 1000 Hz) και υπολογίστε το πλάτος του σταθερού "
                      "τμήματος της καθεμίας.",
            rcode=["d <- read.csv(\"mvc_demo.csv\")      # δύο δοκιμές, 3 s στα 1000 Hz (µV)",
                   "plateau <- 1001:2500                # το σταθερό τμήμα κάθε σύσπασης",
                   "rms <- function(x) sqrt(mean(x^2))",
                   "",
                   "rms_mvc  <- rms(d$mvc[plateau])     # μέγιστη εκούσια σύσπαση",
                   "rms_task <- rms(d$task[plateau])    # η εργασία",
                   "pct_mvc  <- rms_task / rms_mvc * 100   # πλάτος εργασίας ως % της MVC",
                   "",
                   "round(c(rms_mvc = rms_mvc, rms_task = rms_task, pct_mvc = pct_mvc), 4)"],
            code=["d = readtable('mvc_demo.csv');     % δύο δοκιμές, 3 s στα 1000 Hz (µV)",
                  "plateau = 1001:2500;               % το σταθερό τμήμα κάθε σύσπασης",
                  "",
                  "rms_mvc  = sqrt(mean(d.mvc(plateau).^2))       % μέγιστη εκούσια σύσπαση",
                  "rms_task = sqrt(mean(d.task(plateau).^2))      % η εργασία",
                  "pct_mvc  = rms_task / rms_mvc * 100            % πλάτος εργασίας ως % της MVC"],
            tip="Μετακινήστε το κέρδος, κατεβάστε ξανά: οι δύο τιμές RMS αλλάζουν, αλλά το <code>pct_mvc</code> όχι.",
            question="Τα ηλεκτρόδια ενός δεύτερου συμμετέχοντα δίνουν διπλάσιο πλάτος για την ίδια προσπάθεια του "
                     "μυός. Μετά την κανονικοποίηση σε MVC, πώς συγκρίνονται τα πλάτη της εργασίας των δύο;",
            options=[("Ο συμμετέχων 2 δείχνει διπλάσιο %MVC.", False,
                      "Και οι δύο δοκιμές, η MVC και η εργασία, διπλασιάζονται, οπότε ο διπλασιασμός απλοποιείται στον λόγο."),
                     ("Είναι ίδια: το κέρδος απλοποιείται στον λόγο.", True,
                      "Αυτός είναι ο σκοπός της κανονικοποίησης: το %MVC δεν εξαρτάται από το κέρδος."),
                     ("Δεν μπορούν να συγκριθούν καθόλου.", False,
                      "Τα ακατέργαστα πλάτη δεν μπορούν, αλλά το %MVC μπορεί.")],
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
    # ------------------------------------------------------------------ 6. motor unit firing
    dict(
        id="spikes", kind="spikes", file="spikes_demo.csv",
        en=dict(
            short="Motor unit firing",
            title="From spike times to discharge rate and variability",
            read=["Decomposing high-density EMG gives, for each motor unit, a list of <b>discharge times</b>. Two "
                  "numbers summarise how a unit fires: the <b>mean discharge rate</b> (pulses per second, "
                  "<code>1 / mean ISI</code>) and the <b>variability</b> of the <b>inter-spike intervals</b> (ISI), "
                  "usually as a coefficient of variation.",
                  "Variability matters because a motor unit's firing is the neural drive to the muscle: more variable "
                  "firing goes with a less steady force, and it can increase in people with pain."],
            explore="Ten seconds of one motor unit. Change the mean rate and the variability: the spikes become "
                    "more irregular, the instantaneous rate scatters and the ISI histogram widens.",
            labels=["Discharge times and instantaneous rate (pps)", "Inter-spike intervals (ISI)", "s", "ms", "pps",
                    "Spikes", "Mean rate", "CoV of ISI"],
            ctl=[dict(k="rate", label="Mean rate", min=6, max=30, step=1, value=12, unit="pps"),
                 dict(k="cov", label="Variability (CoV)", min=3, max=40, step=1, value=15, unit="%")],
            code_note="The discharge times of one motor unit over 10 s, as a decomposition would give you.",
            rcode=["spikes <- scan(\"spikes_demo.csv\", quiet = TRUE)   # discharge times (s)",
                   "isi <- diff(spikes)                          # inter-spike intervals (s)",
                   "",
                   "rate    <- 1 / mean(isi)                     # mean discharge rate (pulses per second)",
                   "cov_isi <- sd(isi) / mean(isi) * 100         # variability of the intervals (%)",
                   "",
                   "round(c(n_spikes = length(spikes), rate = rate, cov_isi = cov_isi), 4)"],
            code=["spikes = readmatrix('spikes_demo.csv');   % discharge times (s)",
                  "isi = diff(spikes);                       % inter-spike intervals (s)",
                  "",
                  "n_spikes = numel(spikes)",
                  "rate     = 1 / mean(isi)                  % mean discharge rate (pulses per second)",
                  "cov_isi  = std(isi) / mean(isi) * 100     % variability of the intervals (%)"],
            tip="Set the variability to 5 % and then 35 %, download each time and compare <code>cov_isi</code>.",
            question="Two motor units fire at the same mean rate, but one has a higher CoV of the ISI. What does that mean?",
            options=[("Its firing is less regular: the intervals vary more around the same mean.", True,
                      "Same rate, different regularity: that is what the CoV of the ISI captures."),
                     ("It fires at a higher rate.", False,
                      "The mean rate is the same by definition here."),
                     ("It is made of more muscle fibres.", False,
                      "The CoV describes how regular the timing is, not the size of the unit.")],
        ),
        el=dict(
            short="Πυροδότηση κινητικής μονάδας",
            title="Από τους χρόνους εκφόρτισης στον ρυθμό και στη μεταβλητότητα",
            read=["Η αποσύνθεση του EMG υψηλής πυκνότητας δίνει, για κάθε κινητική μονάδα, μια λίστα με τους "
                  "<b>χρόνους εκφόρτισης</b>. Δύο αριθμοί περιγράφουν πώς πυροδοτεί μια μονάδα: ο <b>μέσος ρυθμός "
                  "εκφόρτισης</b> (παλμοί ανά δευτερόλεπτο, <code>1 / μέσο ISI</code>) και η <b>μεταβλητότητα</b> των "
                  "<b>διαστημάτων μεταξύ παλμών</b> (ISI), συνήθως ως συντελεστής μεταβλητότητας.",
                  "Η μεταβλητότητα έχει σημασία επειδή η πυροδότηση μιας κινητικής μονάδας είναι η νευρική ώθηση προς "
                  "τον μυ: πιο μεταβλητή πυροδότηση συνοδεύεται από λιγότερο σταθερή δύναμη και μπορεί να αυξάνεται "
                  "σε άτομα με πόνο."],
            explore="Δέκα δευτερόλεπτα μιας κινητικής μονάδας. Αλλάξτε τον μέσο ρυθμό και τη μεταβλητότητα: οι παλμοί "
                    "γίνονται πιο ακανόνιστοι, ο στιγμιαίος ρυθμός διασκορπίζεται και το ιστόγραμμα των ISI "
                    "διευρύνεται.",
            labels=["Χρόνοι εκφόρτισης και στιγμιαίος ρυθμός (pps)", "Διαστήματα μεταξύ παλμών (ISI)", "s", "ms",
                    "pps", "Παλμοί", "Μέσος ρυθμός", "CoV των ISI"],
            ctl=[dict(k="rate", label="Μέσος ρυθμός", min=6, max=30, step=1, value=12, unit="pps"),
                 dict(k="cov", label="Μεταβλητότητα (CoV)", min=3, max=40, step=1, value=15, unit="%")],
            code_note="Οι χρόνοι εκφόρτισης μιας κινητικής μονάδας για 10 s, όπως θα τους έδινε μια αποσύνθεση.",
            rcode=["spikes <- scan(\"spikes_demo.csv\", quiet = TRUE)   # χρόνοι εκφόρτισης (s)",
                   "isi <- diff(spikes)                          # διαστήματα μεταξύ παλμών (s)",
                   "",
                   "rate    <- 1 / mean(isi)                     # μέσος ρυθμός εκφόρτισης (παλμοί ανά δευτερόλεπτο)",
                   "cov_isi <- sd(isi) / mean(isi) * 100         # μεταβλητότητα των διαστημάτων (%)",
                   "",
                   "round(c(n_spikes = length(spikes), rate = rate, cov_isi = cov_isi), 4)"],
            code=["spikes = readmatrix('spikes_demo.csv');   % χρόνοι εκφόρτισης (s)",
                  "isi = diff(spikes);                       % διαστήματα μεταξύ παλμών (s)",
                  "",
                  "n_spikes = numel(spikes)",
                  "rate     = 1 / mean(isi)                  % μέσος ρυθμός εκφόρτισης (παλμοί ανά δευτερόλεπτο)",
                  "cov_isi  = std(isi) / mean(isi) * 100     % μεταβλητότητα των διαστημάτων (%)"],
            tip="Βάλτε τη μεταβλητότητα στο 5 % και μετά στο 35 %, κατεβάστε κάθε φορά και συγκρίνετε το <code>cov_isi</code>.",
            question="Δύο κινητικές μονάδες πυροδοτούν με τον ίδιο μέσο ρυθμό, αλλά η μία έχει υψηλότερο CoV των ISI. Τι σημαίνει αυτό;",
            options=[("Η πυροδότησή της είναι λιγότερο κανονική: τα διαστήματα μεταβάλλονται περισσότερο γύρω από τον ίδιο μέσο.", True,
                      "Ίδιος ρυθμός, διαφορετική κανονικότητα: αυτό αποτυπώνει το CoV των ISI."),
                     ("Πυροδοτεί με υψηλότερο ρυθμό.", False,
                      "Ο μέσος ρυθμός είναι εξ ορισμού ο ίδιος εδώ."),
                     ("Αποτελείται από περισσότερες μυϊκές ίνες.", False,
                      "Το CoV περιγράφει πόσο κανονικός είναι ο χρονισμός, όχι το μέγεθος της μονάδας.")],
        ),
    ),
    # ------------------------------------------------------------------ 7. statistics
    dict(
        id="stats", kind="stats", file="groups_demo.csv",
        en=dict(
            short="Statistics",
            title="Comparing two groups: t-test, p-value and effect size",
            read=["Suppose force steadiness (CoV, %) is measured in people without and with pain. The <b>t-test</b> "
                  "asks whether the difference between the group means is bigger than chance alone would produce: "
                  "<code>t = difference / standard error</code>. The <b>p-value</b> is the probability of a "
                  "difference at least this big if there were no real difference.",
                  "A p-value does not say how <i>big</i> the difference is. The <b>effect size</b> (Cohen's "
                  "<i>d</i>, the difference in SDs) and the <b>95% confidence interval</b> of the difference do. "
                  "Report them together."],
            explore="Left: the two groups (dots) with mean ± SD. Right: the difference between the means and its "
                    "95% confidence interval; when the interval excludes zero, p is below 0.05. Increase the sample "
                    "size with the same true difference and watch the interval narrow.",
            labels=["Force CoV (%)", "Without pain", "With pain", "Difference in means (%)", "95% CI",
                    "t", "df", "p", "Cohen's d", "95% CI of the difference"],
            ctl=[dict(k="diff", label="True difference", min=0, max=6, step=0.1, value=2, unit="%", dec=1),
                 dict(k="sd", label="SD", min=0.5, max=4, step=0.1, value=1.5, unit="%", dec=1),
                 dict(k="n", label="Per group", min=6, max=30, step=1, value=12, unit="n")],
            code_note="Welch's t-test on the values shown (one column per group).",
            rcode=["d <- read.csv(\"groups_demo.csv\")      # force CoV (%), one value per participant",
                   "",
                   "r  <- t.test(d$pain, d$free)            # Welch two-sample t-test",
                   "sp <- sqrt((var(d$pain) + var(d$free)) / 2)     # pooled SD (equal group sizes)",
                   "dcohen <- (mean(d$pain) - mean(d$free)) / sp    # effect size",
                   "ci <- r$conf.int                          # 95% CI of the difference",
                   "",
                   "round(c(t = unname(r$statistic), df = unname(r$parameter), p = r$p.value,",
                   "        dcohen = dcohen, ci_low = ci[1], ci_high = ci[2]), 4)"],
            code=["d = readtable('groups_demo.csv');      % force CoV (%), one value per participant",
                  "",
                  "[~, p, ci, st] = ttest2(d.pain, d.free, 'Vartype', 'unequal');   % Welch t-test",
                  "t  = st.tstat",
                  "df = st.df",
                  "p",
                  "dcohen = (mean(d.pain) - mean(d.free)) / sqrt((var(d.pain) + var(d.free)) / 2)",
                  "ci_low  = ci(1)",
                  "ci_high = ci(2)"],
            tip="Double the sample size, download again: <code>dcohen</code> stays similar while <code>p</code> gets smaller.",
            question="You double the number of participants, keeping the same true difference and variability. "
                     "What typically happens?",
            options=[("The p-value gets smaller, while the effect size stays about the same.", True,
                      "More participants shrink the standard error, so the same difference is easier to detect; d describes the size of the difference, which has not changed."),
                     ("The effect size doubles.", False,
                      "Effect size does not depend on how many people you test."),
                     ("The p-value cannot change.", False,
                      "p depends on both the size of the difference and the sample size.")],
        ),
        el=dict(
            short="Στατιστική",
            title="Σύγκριση δύο ομάδων: t-test, τιμή p και μέγεθος επίδρασης",
            read=["Έστω ότι η σταθερότητα δύναμης (CoV, %) μετριέται σε άτομα χωρίς και με πόνο. Το <b>t-test</b> "
                  "ρωτά αν η διαφορά των μέσων των ομάδων είναι μεγαλύτερη από όση θα έδινε μόνο η τύχη: "
                  "<code>t = διαφορά / τυπικό σφάλμα</code>. Η <b>τιμή p</b> είναι η πιθανότητα μιας διαφοράς "
                  "τουλάχιστον τόσο μεγάλης αν δεν υπήρχε πραγματική διαφορά.",
                  "Η τιμή p δεν λέει πόσο <i>μεγάλη</i> είναι η διαφορά. Αυτό το δείχνουν το <b>μέγεθος "
                  "επίδρασης</b> (d του Cohen, η διαφορά σε SD) και το <b>95% διάστημα εμπιστοσύνης</b> της "
                  "διαφοράς. Αναφέρετέ τα μαζί."],
            explore="Αριστερά: οι δύο ομάδες (κουκκίδες) με μέσο ± SD. Δεξιά: η διαφορά των μέσων και το 95% διάστημα "
                    "εμπιστοσύνης της· όταν το διάστημα δεν περιέχει το μηδέν, το p είναι κάτω από 0,05. Αυξήστε το "
                    "μέγεθος του δείγματος με την ίδια πραγματική διαφορά και δείτε το διάστημα να στενεύει.",
            labels=["CoV δύναμης (%)", "Χωρίς πόνο", "Με πόνο", "Διαφορά μέσων (%)", "95% ΔΕ",
                    "t", "df", "p", "d του Cohen", "95% ΔΕ της διαφοράς"],
            ctl=[dict(k="diff", label="Πραγματική διαφορά", min=0, max=6, step=0.1, value=2, unit="%", dec=1),
                 dict(k="sd", label="SD", min=0.5, max=4, step=0.1, value=1.5, unit="%", dec=1),
                 dict(k="n", label="Ανά ομάδα", min=6, max=30, step=1, value=12, unit="n")],
            code_note="Το t-test του Welch στις τιμές που φαίνονται (μία στήλη ανά ομάδα).",
            rcode=["d <- read.csv(\"groups_demo.csv\")      # CoV δύναμης (%), μία τιμή ανά συμμετέχοντα",
                   "",
                   "r  <- t.test(d$pain, d$free)            # t-test δύο δειγμάτων του Welch",
                   "sp <- sqrt((var(d$pain) + var(d$free)) / 2)     # συνδυασμένη SD (ίσα μεγέθη ομάδων)",
                   "dcohen <- (mean(d$pain) - mean(d$free)) / sp    # μέγεθος επίδρασης",
                   "ci <- r$conf.int                          # 95% διάστημα εμπιστοσύνης της διαφοράς",
                   "",
                   "round(c(t = unname(r$statistic), df = unname(r$parameter), p = r$p.value,",
                   "        dcohen = dcohen, ci_low = ci[1], ci_high = ci[2]), 4)"],
            code=["d = readtable('groups_demo.csv');      % CoV δύναμης (%), μία τιμή ανά συμμετέχοντα",
                  "",
                  "[~, p, ci, st] = ttest2(d.pain, d.free, 'Vartype', 'unequal');   % t-test του Welch",
                  "t  = st.tstat",
                  "df = st.df",
                  "p",
                  "dcohen = (mean(d.pain) - mean(d.free)) / sqrt((var(d.pain) + var(d.free)) / 2)",
                  "ci_low  = ci(1)",
                  "ci_high = ci(2)"],
            tip="Διπλασιάστε το μέγεθος του δείγματος, κατεβάστε ξανά: το <code>dcohen</code> μένει παρόμοιο ενώ το <code>p</code> μικραίνει.",
            question="Διπλασιάζετε τον αριθμό των συμμετεχόντων, με την ίδια πραγματική διαφορά και μεταβλητότητα. "
                     "Τι συμβαίνει συνήθως;",
            options=[("Η τιμή p μικραίνει, ενώ το μέγεθος επίδρασης μένει περίπου ίδιο.", True,
                      "Περισσότεροι συμμετέχοντες μειώνουν το τυπικό σφάλμα, οπότε η ίδια διαφορά ανιχνεύεται πιο εύκολα· το d περιγράφει το μέγεθος της διαφοράς, που δεν άλλαξε."),
                     ("Το μέγεθος επίδρασης διπλασιάζεται.", False,
                      "Το μέγεθος επίδρασης δεν εξαρτάται από το πόσα άτομα εξετάζετε."),
                     ("Η τιμή p δεν μπορεί να αλλάξει.", False,
                      "Το p εξαρτάται και από το μέγεθος της διαφοράς και από το μέγεθος του δείγματος.")],
        ),
    ),
]
