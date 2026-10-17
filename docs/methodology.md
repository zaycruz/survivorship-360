# Methodology

This page says, for each AI and ML component, how it was built and how it was checked. Each section is a short summary. The full method is in each module's `METHODOLOGY.md`, which follows the same ten steps: question and target, data, features, split, model and selection, baseline, metrics with 95% CIs, robustness, limits, reproduce. Each module file cites the source file of every number and names the code that does each step.

Numbers on this page are copied from the module table in [`README.md`](../README.md). Their sources in each module are listed in [`claims.tsv`](claims.tsv).

| Component | Kind | Full method |
|---|---|---|
| C1 Care-team risk | Random forest | [c1-acute-risk/METHODOLOGY.md](https://github.com/zaycruz/c1-acute-risk/blob/main/METHODOLOGY.md) |
| C3 Bad Week Radar | Gradient boosting, plus rules | [c3-rough-patch/METHODOLOGY.md](https://github.com/zaycruz/c3-rough-patch/blob/main/METHODOLOGY.md) |
| C4 Glucose Guide | Double ML, forecast, Llama wording | [c4-glucose-guide/METHODOLOGY.md](https://github.com/zaycruz/c4-glucose-guide/blob/main/METHODOLOGY.md) |
| C5 Coach's Co-pilot | Clef classifier, rules, GLM | [coach-copilot/METHODOLOGY.md](https://github.com/zaycruz/coach-copilot/blob/main/METHODOLOGY.md) |
| Patient 360 | GLM, Llama fallback, Whisper, rules | [coach-console/METHODOLOGY.md](https://github.com/zaycruz/coach-console/blob/main/METHODOLOGY.md) |

## C1 · Care-team risk (random forest)

- Question: from a survivor's 2017 MEPS answers, the chance of an ER visit or a hospital stay in 2018. Data: real MEPS survey, cancer survivors, one row per person.
- Model: a sigmoid-calibrated random forest, picked from 48 candidates. Penalties and calibration are fitted inside training folds only.
- Honest estimate: a nested cross-validation puts the model search inside the evaluation. Out of fold, log loss 0.539 vs 0.606 for the organisers' baseline (significant). Calibration slope 1.10 vs 0.45. AUROC 0.711 vs 0.672, not significant.
- The search was not blind: later rounds were written after reading earlier ones, on the same survivors. The module file says which numbers are after selection.
- Checks: fairness by subgroup with a pre-registered mitigation, a Synthea transport test, and a check of held-out inputs against the development range. The only real data is MEPS; there is no external or temporal validation.
- No generative AI: all text comes from templates.

## C3 · Bad Week Radar (gradient boosting, urgent tier, rules)

- Question: will a person have a rough patch in the next days, forecast 2–7 days early. Unit: person-day. Data: the organisers' synthetic wearables, check-ins and treatment calendar.
- Leakage control: check-in ratings enter only with a 3-day lag. Split by person, with a temporal holdout as a second check.
- Result at a 5% alert budget, held out: 48% of patches caught early vs 36% for a calendar-only model at the same budget.
- Urgent tier (top 3% of days) vs a calendar-only ER model at the same budget: 47% vs 36% of ER visits and admissions (CI +2 to +19). A model-free escalation (red-flag diary notes, passive suicidal ideation in EN/ES/HT, a 1-of-5 day) raises this to 61% vs 47% (CI +9 to +19).
- Honest points: some research rounds looked at test patients; there is no nested CV and one split seed. The real-data check on a real fatigue study fits a separate simple model; it does not run the Radar.
- No generative AI: all coach text comes from templates.

## C4 · Glucose Guide (double ML, forecast, advice wording)

- Question: within one person, how evening walks, late dinners and overnight fasting change blood sugar after meals. Method: double ML with cross-fitting.
- Real adults (CGMacros, 44): walk after a meal −3.2 mg/dL (CI −6.9 to +0.5), not distinguishable from zero. Synthetic program: −18.3 (CI 16.6–20.1). So the advice offers the walk as a low-risk habit.
- Checks: a negative control, an E-value, an instrument, CGMacros and NHANES, fairness groups. All in `ROBUSTNESS.md` in the module.
- Honest points: the engine choice was changed after a look (quoted in `ML_COMPARISON.md`). Cross-fitting folds are not split by person, which fits the within-person question.
- Generative AI: Llama on Workers AI may only reword template advice. A code check rejects new numbers or causal words and falls back to the template. There is no dedicated dosing filter.

## C5 · Coach's Co-pilot (Clef classifier, rules, GLM)

- Question: tag every call line with an MI code. Unit: one line. The Clef classifier is tuned through its labels and examples in `src/payload.json`, not through its weights.
- Held out: 93.1% on coach moves and 90.9% on participant talk, on 1,085 calls. Coach score vs each supervisor r 0.75 / 0.70, vs 0.69 between supervisors.
- Safety: a model-free red-flag screen runs first and can only raise a flag. 13/13 urgent lines caught; false alarms 244 / 25,785 lines.
- Stress sets were written by a separate agent and committed before their first run. After distress was widened to suicide warning signs, 44/54 were caught on an independent held-out set (was 25/54).
- Real-data check: AnnoMI, against 10 experts. Lines below 0.3 confidence go to GLM review. Cues fire only from rules; GLM writes the wording.
- Honest points: the README discloses a reverted draft tuned after a look. Speech-to-text accuracy and cue quality are not rated.

## Patient 360 (generative AI and rules)

- The assistant, AI Insight and call recap run on GLM-5.3-flash, with Llama 3.3 as the fallback. Speech to text uses Whisper.
- Red-flag rules run before any model call in the assistant. The model never ranks patients or makes decisions.
- The Today list is ranked by fixed rules in code, not by a model. The module file lists each rule and its weight.
- Labels: the module file quotes the exact strings users see, and says where a label is missing or shown on fixed text.
- Measured: the E2E run against the live site, 110/114 (the 4 misses are phone-width layout; the console is desktop-only). Not evaluated: faithfulness, medical quality, speech-to-text word error, and multilingual quality of the generated text.
