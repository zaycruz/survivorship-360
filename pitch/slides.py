"""Survivorship 360 pitch deck: slide list, speaker notes and the numbers each slide shows.

Every number on a slide is listed in CLAIMS with the module file that must contain it.
build_pptx.py reads this file for notes; check.py greps each claim against its source.
"""

ROOT = "~/projects/emerge-hackathon"

SLIDES = [
    {
        "name": "01 Title",
        "notes": (
            "Hi, we're Survivorship 360. A cancer-survivorship care team gets signals from everywhere: "
            "surveys, wearables, glucose sensors, coaching calls. We built one place to see who needs them today, and why. "
            "Four AI modules, one per challenge, joined into one care-team console for clinicians, nurse navigators and coaches, with a chat assistant; patients never use it. "
            "There is also an MCP server so ChatGPT or Claude can ask the same questions. "
            "Built in one day, all custom, all live on Cloudflare."
        ),
    },
    {
        "name": "02 Problem",
        "notes": (
            "The care team's problem is not a lack of data. It's too many signals and no ranking. "
            "Who is heading into a rough week? Who is likely to end up in the ER next year? "
            "Which daily habit actually moves this person's blood sugar? Is the coaching call going well, "
            "and did the participant just say something a person must act on today? "
            "Today the coach hears about a bad week at the next call, days late."
        ),
    },
    {
        "name": "03 Product",
        "notes": (
            "Two front doors over the same four modules. Patient 360 is the care team's console, for clinicians, nurse navigators and coaches; patients never see it: a Today list, patient roster, "
            "a 360 view per survivor, live coaching calls with a recap, and an AI assistant that can navigate and answer. "
            "And any AI assistant, ChatGPT or Claude, can use the 12 read-only MCP tools, for example 'who should we call today', "
            "one survivor across modules, or 'score this conversation'."
        ),
    },
    {
        "name": "04 Architecture",
        "notes": (
            "Two kinds of user: the care team (a clinician, nurse navigator or coach) working today's list, and anyone asking ChatGPT or Claude. "
            "Two front doors: Patient 360 with its AI assistant, and the challenge MCP server. The MCP server passes 120 of 120 end-to-end checks with the official MCP client, including injected-failure fallbacks. Each challenge is its own Cloudflare Worker "
            "with a CONTRACT.md generated from real responses; the front doors only read contracts, so modules ship independently. "
            "If a module is down, Patient 360 serves its saved snapshot and says so with a per-module chip; AI calls retry once and never block a tag. "
            "Splits are by person, and every module's E2E run against its live deployment is saved as an artifact. "
            "Models: a calibrated random forest for C1, two gradient-boosting models for C3, double ML within person for C4, "
            "and Workers AI through AI Gateway: the Clef classifier for C5 tags and flags, GLM-5.3-flash for cues, the assistant and recaps, "
            "Llama 3.3 for C4 rewrites. Real-data checks use MEPS, CGMacros, NHANES and AnnoMI."
        ),
    },
    {
        "name": "05 C1",
        "notes": (
            "C1: who may need acute care next year. The headline: our probabilities are significantly better than the organisers' "
            "baseline. Log loss, where lower is better, is 0.539 against 0.606, a significant gain, and a calibration slope of 1.10 against the baseline's 0.45, "
            "where 1 is ideal. When the model we serve says 50 percent risk or more, it is right 59 percent of the time, interval 46 to 71, versus 48 for the baseline, just short of significant. "
            "The data is real MEPS survey answers from 466 cancer survivors, 134 of whom had an ER visit or hospital stay. The model is "
            "a calibrated random forest chosen from 48 candidates, scored out of fold with 10 by 5 cross-validation; log loss and AUROC were also checked with nested cross-validation over 10 outer folds. "
            "Ranking is better too, AUROC 0.711 vs 0.672, but that gain is not significant, and we say so. The limit: it ranks NH Black "
            "survivors poorly, AUROC 0.48 on only 47 people, and the panel warns about it."
        ),
    },
    {
        "name": "06 C3",
        "notes": (
            "C3, the Bad Week Radar. Every evening it forecasts whether a rough patch starts in the next week, from the survivor's own "
            "check-ins against their usual, skipped check-ins, the wearable, and the treatment calendar. The calendar is the honest "
            "baseline, because most bad weeks follow a dose. We gave every method the same alert budget, 5 percent of quiet days, "
            "which is about one new alert per coach per day. On 750 patients split by patient, against the calendar baseline, it catches 48 percent of "
            "patches 2 to 7 days early versus 36, and 18 percent of alerts come true versus 11. "
            "A separate urgent tier, which flags the top 3 percent of days, catches 47 percent of ER visits and admissions 2 to 7 days early, against 36 percent for the calendar-only ER model, a lift of 2 to 19 points. An urgent flag means about 6 times the usual ER or hospital risk that week: a prompt to check in, not a prediction. About 1 urgent flag in 14 is followed by an ER visit. On top of that, a model-free escalation, red-flag diary notes, passive suicidal ideation in English, Spanish or Creole, or a day rated 1 of 5, raises it to 61 percent versus 47, interval plus 9 to plus 19 points, for about 4 more calls per coach per week. The limit: in a real fatigue study the wearable "
            "does not forecast the next day, AUC 0.482, so lead time is shown on synthetic data only. "
            "On later dates, trained before July 2025 and tested from October 2025, it is 44 percent versus 36, interval minus 1 to plus 17: same direction, not significant. "
            "And recall is clearly lower for sarcoma, 13 percent against 28 overall."
        ),
    },
    {
        "name": "07 C4",
        "notes": (
            "C4, the Glucose Guide. The real number first. In 44 real adults in the CGMacros study, a walk after a meal went with a rise only 3.2 mg/dL smaller, confidence interval minus 6.9 to plus 0.5: not distinguishable from zero. In the synthetic program, a walk after dinner shows minus 18.3 mg/dL, interval 16.6 to 20.1. "
            "The program is a synthetic 12-week cohort: 500 sensor wearers, 18,218 meal curves. We use double machine learning within each person, so each survivor is compared with themselves, "
            "and the walk effect passes a negative control. 10 to 19 minutes gets most of it. Dinner at 8 pm or later adds 9.2. The overnight fast barely moved HbA1c, minus 0.03. "
            "Personal advice appears only when the person's own data supports it, and every number in the advice traces to evidence. "
            "Walks were self-chosen, so this is an association, and we expect a much smaller effect in real people than in the program."
        ),
    },
    {
        "name": "08 C5",
        "notes": (
            "C5, the Coach's Co-pilot. The headline: the app's coach score agrees with each supervisor about as well as the two supervisors "
            "agree with each other: r = 0.75 with supervisor A and 0.70 with supervisor B, against 0.69 between A and B, over 477 held-out calls. "
            "It works in English and Spanish; Haitian Creole is tested only on the safety flag, so tags and scores are not validated in Creole. It follows a coaching call live "
            "and tags every line with a motivational-interviewing code using Cloudflare's Clef classifier. Model time is 0.3 to 0.5 seconds per line; a browser round trip takes longer, because it adds the network and, on participant lines, the parallel flag call. It tags a coach move from 12 labels and the client's talk as change, sustain or neutral. Tuning used 20 percent of participants; the other 80 percent, 1,085 calls with 56,001 answered lines, are held out for validation. "
            "On held-out calls it tags coach moves right 93.1 percent of the time, and it caught all 13 urgent lines. On an independent held-out set it now catches 44 of 54 suicide warning signs, up from 25. "
            "The cost: 244 false alarms in 25,785 lines, up from 9, which is about 1 call in 5. It still misses about 1 in 5 indirect warning signs, so every distress flag tells the coach to use their suicide-risk screening protocol now. As a transfer check we ran it, never tuned on it, against AnnoMI, an outside set of real "
            "counselling sessions labelled by experts: it agrees 75.0 percent, experts agree with the majority 83.9 percent, and "
            "where all experts agree it gets 91 to 93 percent."
        ),
    },
    {
        "name": "09 Honesty",
        "notes": (
            "How to read our numbers. Every number traces to a validation run in its module's repo: held-out patients for C3 and C5, "
            "nested out-of-fold cross-validation for C1, cross-fitted estimates with falsification checks for C4. Every headline sits "
            "next to its baseline. Each module shows its weak spot in the product itself, not only in the README: "
            "fairness gaps and real-data checks that do not confirm the synthetic effect. The cohorts are separate synthetic "
            "datasets that share no patient ids, so cross-module views use composite personas, labelled as such."
        ),
    },
    {
        "name": "10 Demo",
        "notes": (
            "Here is what you'll see live. Open Patient 360, the Today list. Open one survivor and see why they're on the list. "
            "Play a coaching call and watch the tags, the score and the banners appear. Ask the AI assistant a question. Then, from Claude or "
            "ChatGPT, connect the MCP server at emerge-mcp.raava.dev/mcp and ask who to call today. The console is at patient-360.raava.dev and the "
            "coach's call console at coach.raava.dev. Each module also has its own page if you want to dig into the model card."
        ),
    },
    {
        "name": "11 Next",
        "notes": (
            "What's next. C1: predict the first acute event, not last year's repeat users; that's the hard, useful part. "
            "C3: a causal scoring mask would let us use yesterday's rating, the strongest next-day signal in real data. "
            "And the big one: validate on real Sylvester survivorship data. "
            "Our proposal: a pilot with the survivorship care team. Thank you."
        ),
    },
]

# (literal on a slide, module, file that must contain it)
CLAIMS = [
    ("12 read-only tools", "survivorship-360", "README.md"),
    ("466", "c1-acute-risk", "README.md"),
    ("134 events", "c1-acute-risk", "README.md"),
    ("48 candidates", "c1-acute-risk", "README.md"),
    ("**0.539** | 0.606", "c1-acute-risk", "README.md"),
    ("0.45 [0.25, 0.69] | 1.09 | **1.10**", "c1-acute-risk", "README.md"),
    ("**0.711** | 0.672", "c1-acute-risk", "README.md"),
    ("right 59% of the time [46%, 71%]", "c1-acute-risk", "README.md"),
    ("AUROC 0.48 [0.25, 0.70], n = 47", "c1-acute-risk", "README.md"),
    ("750 patients", "c3-rough-patch", "README.md"),
    ("5% of quiet days", "c3-rough-patch", "README.md"),
    ("about one new alert per coach per day", "c3-rough-patch", "README.md"),
    ("Patches caught early: 48% vs 36% (95% CI +8 to +15 points over patients)", "c3-rough-patch", "README.md"),
    ("47% vs 36% of ER visits caught 2–7 days early (95% CI +2 to +19 points over patients", "c3-rough-patch", "README.md"),
    ("urgent tier + escalation catches 61% vs 47% of ER visits 2–7 days early (95% CI +9 to +19 points over patients)", "c3-rough-patch", "README.md"),
    ("about 6x the usual risk", "c3-rough-patch", "README.md"),
    ("about 1 in 14 urgent flags is followed by an ER visit", "c3-rough-patch", "README.md"),
    ("Alert precision: 18% vs 11%", "c3-rough-patch", "README.md"),
    ("Patches caught early: 44% vs 36% for the calendar. The 95% CI is -1 to +17 points", "c3-rough-patch", "README.md"),
    ("AUC 0.482", "c3-rough-patch", "README.md"),
    ("Only sarcoma is clearly below the overall 28% (13%, CI 0–26%)", "c3-rough-patch", "README.md"),
    ("500 sensor wearers, 18,218 clean meal curves", "c4-glucose-guide", "README.md"),
    ("**18.3 mg/dL lower** (16.6 to 20.1)", "c4-glucose-guide", "README.md"),
    ("**10-19 min gets most of it**", "c4-glucose-guide", "README.md"),
    ("**+9.2 mg/dL** (7.1 to 11.3)", "c4-glucose-guide", "README.md"),
    ("-0.03 points overall", "c4-glucose-guide", "README.md"),
    ("walk after a meal -3.2 (-6.9 to 0.5)", "c4-glucose-guide", "README.md"),
    ("44 real adults", "c4-glucose-guide", "README.md"),
    ("**93.1%**", "coach-copilot", "README.md"),
    ("The app's coach score agrees with each supervisor about as well as the two supervisors agree with each other: r = 0.75 with supervisor A and 0.70 with supervisor B, against 0.69 between A and B.", "coach-copilot", "README.md"),
    ("**Haitian Creole is tested only on the safety flag**", "coach-copilot", "README.md"),
    ("English and Spanish are measured separately", "coach-copilot", "README.md"),
    ("There are 477 validation calls", "coach-copilot", "README.md"),
    ("Where all 10 experts agreed, Clef gets 91.1% (counsellor, 112 lines) and 93.1% (client, 58)", "coach-copilot", "README.md"),
    ("The payload was tuned on synthetic cancer-coaching calls, not on AnnoMI", "coach-copilot", "README.md"),
    ("not significant (P(better) 0.93)", "c1-acute-risk", "README.md"),
    ("-0.067 [-0.115, -0.020], **significant**", "c1-acute-risk", "README.md"),
    ("**Baseline: calendar-only rough-patch model**", "c3-rough-patch", "README.md"),
    ("**Baseline: calendar-only ER model**", "c3-rough-patch", "README.md"),
    ("E2E 120/120 with the official MCP client", "survivorship-360", "README.md"),
    ("44 with walk data", "c4-glucose-guide", "README.md"),
    ("Walking was self-chosen, so this is an association", "c4-glucose-guide", "README.md"),
    ("-18 after dinner in the synthetic program", "c4-glucose-guide", "README.md"),
    ("a walk after a meal went with a sugar rise only 3.2 mg/dL smaller (95% CI −6.9 to +0.5): not distinguishable from zero", "c4-glucose-guide", "README.md"),
    ("In the synthetic program, a walk after dinner shows −18.3 mg/dL", "c4-glucose-guide", "README.md"),
    ("expect a much smaller effec", "c4-glucose-guide", "README.md"),
    ("1,085 calls", "coach-copilot", "README.md"),
    ("**13/13** (10 medical, 2 social, 1 distress)", "coach-copilot", "README.md"),
    ("**244 / 25,785**", "coach-copilot", "README.md"),
    ("suicide risk **44 / 54**", "coach-copilot", "README.md"),
    ("p50 ~0.3–0.5 s", "coach-copilot", "README.md"),
    ("Clef call time per line in the batch run", "coach-copilot", "README.md"),
    ("A `/api/turn` round trip from a browser takes longer", "coach-copilot", "README.md"),
    ("75.0%", "coach-copilot", "README.md"),
    ("83.9%", "coach-copilot", "README.md"),
    ("10 outer folds", "c1-acute-risk", "README.md"),
    ("≥ 50% that came true", "c1-acute-risk", "README.md"),
    ("2–7 d early", "c3-rough-patch", "README.md"),
    ("in the next 7 days", "c3-rough-patch", "README.md"),
    ("Synthetic 12-week program", "c4-glucose-guide", "README.md"),
    ("Dinner at 8 pm", "c4-glucose-guide", "README.md"),
    ("It passes a negative control", "c4-glucose-guide", "README.md"),
    ("the randomized arm changed HbA1c by -0.03", "c4-glucose-guide", "README.md"),
    ("1,085 calls, 56,001 answered lines", "coach-copilot", "README.md"),
    ("`move` (12 labels)", "coach-copilot", "README.md"),
    ("`talk` (change/sustain/neutral)", "coach-copilot", "README.md"),
    ("**dev 20%** (tuning) and **validation 80%**", "coach-copilot", "README.md"),
]
