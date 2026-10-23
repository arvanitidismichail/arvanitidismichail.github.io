# Google Scholar metrics: the line under the header figures, the citations-per-year
# chart beside it, and the citation count on each publication.
# Refresh with:  python3 update_scholar.py   (fetches the profile, rewrites this file, rebuilds)
# Or edit the numbers by hand and run build.py.
SCHOLAR = dict(citations=378, h_index=11, i10_index=11, as_of="2026-10-23")

BY_YEAR = {2017: 2, 2018: 2, 2019: 2, 2020: 3, 2021: 11, 2022: 35, 2023: 19, 2024: 61, 2025: 115, 2026: 126}

# (title on Scholar, citations)
PAPERS = [
    ('Pain-induced changes in motor unit discharge depend on recruitment threshold and contraction speed', 49),
    ('People with chronic low back pain display spatial alterations in high-density surface EMG-torque oscillations', 45),
    ('Spatial distribution of lumbar erector spinae muscle activity in individuals with and without chronic low back pain during a dynamic isokinetic fatiguing task', 43),
    ('Does pain influence control of muscle force? A systematic review and meta‐analysis', 30),
    ('Bipolar versus high-density surface electromyography for evaluating risk in fatiguing frequency-dependent lifting activities', 28),
    ('EMG activity of the serratus anterior and trapezius muscles during the different phases of the push-up plus exercise on different support surfaces and different hand positions', 27),
    ('Low back pain–Induced dynamic trunk muscle control impairments are associated with altered spatial EMG–Torque relationships', 21),
    ('Can visual feedback on upper trapezius high-density surface electromyography increase time to task failure of an endurance task?', 19),
    ('Eccentric exercise-induced delayed onset trunk muscle soreness alters high-density surface EMG-torque relationships and lumbar kinematics', 16),
    ('Achilles tendon morpho-mechanical parameters are related to triceps surae motor unit firing properties', 14),
    ('Does pain influence force steadiness? A protocol for a systematic review', 11),
    ('Load and muscle‐dependent changes in triceps surae motor unit firing properties in individuals with non‐insertional Achilles tendinopathy', 9),
    ('Is manual therapy of the diaphragm effective for people with obstructive lung diseases? A systematic review', 9),
    ('Cervical spine and muscle adaptation after spaceflight and relationship to herniation risk: protocol from ‘Cervical in Space’trial', 9),
    ('Validation of a novel device for assessing neck muscle strength', 8),
    ('Temporal differences in the myoelectric activity of lower limb muscles during rearfoot and forefoot running: A statistical parametric mapping approach', 7),
    ('Novel metrics for high-density sEMG analysis in the time–space domain during sustained isometric contractions', 6),
    ('Reduced knee extensor torque steadiness and increased motor unit discharge rate variability in young people with patellofemoral pain: a pilot study', 4),
    ('Diagnostic accuracy of physical examination tests for painful cervical radiculopathy: update of a systematic review and meta-analysis', 4),
    ('Load and muscle dependent changes in triceps surae motor unit firing properties and motor unit firing-torque relationships in individuals with non-insertional Achilles tendinopathy', 4),
    ('Fatigue-induced alterations in the spatial distribution of lumbar erector spinae activity in older versus young adults', 3),
    ('The effects of ageing on fatigue and endurance of the spinal extensor muscles: a systematic review and meta-analysis', 3),
    ('Association between neck muscle size and physical features in individuals with chronic non-specific neck pain: A systematic review', 3),
    ('Torque visuomotor feedback training versus standard eccentric exercise for the management of patellar tendinopathy: protocol for a randomised controlled trial', 2),
    ('Evaluating the efficacy of wearable biofeedback on the outcomes of exercise interventions in people with chronic non-specific spinal pain: protocol for a systematic review and\xa0…', 2),
    ('Does pain alter the spatial distribution of muscle activity in people experiencing spinal pain? A systematic review and meta-analysis', 1),
    ('Eccentric and Concentric Torque Feedback Training Induce Similar Clinical Improvements but Distinct Triceps Surae Motor Unit Adaptations in Non-Insertional Achilles\xa0…', 1),
    ('ERECTOR SPINAE MUSCLE FIBRE SIZE ESTIMATION USING HIGH-DENSITY SURFACE ELECTROMYOGRAPHY IN PEOPLE WITH AND WITHOUT NON-SPECIFIC CHRONIC LOW BACK PAIN', 0),
    ('Spaceflight-Associated Changes in Cervical Spine Structure, Muscle Function, and Disc Health in Astronauts', 0),
    ('Interactions between motor unit firing and fascicle dynamics during shortening and lengthening contractions', 0),
    ('The effect of eccentric exercise-induced delayed onset neck muscle soreness on force steadiness and the spatial distribution of neck extensor muscle activity', 0),
    ('Longitudinal Evaluation of cervical spine structures and function in astronauts and their relation to intervertebral disc herniation', 0),
    ('Age-related alterations in trunk extensor force control during isometric and isokinetic contractions', 0),
    ('Effects of microgravity on neuromuscular control of the spine: a protocol for a systematic review and meta-analysis', 0),
    ('Anpassung der Halswirbelsäule in der Schwerelosigkeit und das Risiko von Bandscheibenvorfällen', 0),
    ('Control of trunk muscle force in individuals with low back pain: new insights revealed by high-density surface electromyography', 0),
    ('Effect of high-density surface electromyography visual feedback on shoulder-abduction endurance: a pilot study', 0),
    ('Association Between Patellar Tendon Morphomechanical Characteristics, Quadriceps Muscle Architecture, and Motor Unit Firing Properties', 0),
    ('Author Affiliations', 0),
]
