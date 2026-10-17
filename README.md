# Survivorship 360

eMerge Hackathon · Sylvester Comprehensive Cancer Center healthcare track · built in one day, everything custom.

**Survivorship 360 gives a cancer-survivorship care team one place to see who needs them today, and why.** It joins four AI modules, one per challenge, into a single clinician console with a chat assistant. A patient-facing iOS app and an MCP server give the same data to survivors and to any AI assistant.

- **Who needs a call today.** A wearable model warns of a rough week 2–7 days ahead. A separate urgent tier flags a likely ER visit or admission.
- **Who is at risk of acute care.** A calibrated risk model whose probabilities can be trusted at face value.
- **What to change in daily life.** Personal, evidence-graded advice on meals, timing and movement against blood sugar.
- **How the coaching is going.** Every line of a coaching call is scored live for motivational-interviewing fidelity, with banners for anything a person must act on.

Every number in the product traces to held-out validation. Each module states where it is weak (fairness gaps, real-data checks that do not confirm the synthetic effect) in the UI, not only in the README.

## Try it

| What | Live |
|---|---|
| **Patient 360**: clinician console + Ellie assistant | https://patient-360.raava.dev |
| C1 Care-team risk | https://c1-acute-risk.zay-259.workers.dev |
| C3 Bad Week Radar | https://c3-rough-patch.zay-259.workers.dev |
| C4 Glucose Guide | https://c4-glucose-guide.zay-259.workers.dev |
| C5 Coach's Co-pilot | https://coach.raava.dev |
| MCP server (ChatGPT / Claude) | `https://emerge-mcp.raava.dev/mcp` |
| iOS patient app | TestFlight (in progress) |

## Modules

| Module | Challenge | What it does | Headline result (held out) | Repo |
|---|---|---|---|---|
| Patient 360 | all | Clinician console: Today list, patients, per-patient 360 view, live coaching calls with recap, Ellie chat assistant | E2E 77/77 against the deployed site | [`coach-console`](modules/coach-console) |
| C1 Care-team risk | C1 acute-care risk | Calibrated logistic model on MEPS survivors; risk tiers, factors, fairness by group | AUROC 0.666 (tie with baseline); calibration slope 1.09 vs 0.45 | [`c1-acute-risk`](modules/c1-acute-risk) |
| C3 Bad Week Radar | C3 wearables | Forecasts rough patches 2–7 days early; urgent ER/admission tier with a "call today" action | 64% of patches caught early vs 59% calendar-only; ER/admissions 54% vs 42% | [`c3-rough-patch`](modules/c3-rough-patch) |
| C4 Glucose Guide | C4 dose & timing | Within-person effects of evening walks, late dinners and overnight fasting on blood sugar; personal advice only when the person's own data supports it | Evening walk −18.7 mg/dL after dinner (CI 17.2–20.4); each claim tagged with a real-data check | [`c4-glucose-guide`](modules/c4-glucose-guide) |
| C5 Coach's Co-pilot | C5 coaching conversations | Tags every call line with an MI code in ~0.4 s (Cloudflare Clef), live fidelity score, safety banners, GLM coaching cues | 93.1% coach moves, 90.9% participant talk on 1,085 calls; 13/13 urgent lines caught | [`coach-copilot`](modules/coach-copilot) |
| Challenge MCP | all | 13 read-only tools over every module for ChatGPT and Claude, incl. "score this conversation" | E2E 67/67 with the official MCP client | [`challenge-mcp`](modules/challenge-mcp) |
| Patient app | all | iOS, the survivor's own view across modules, 5 synthetic personas | in progress | added when its first build lands |

## Architecture

![Survivorship 360 architecture](docs/architecture.png)

Each module is its own Cloudflare Worker with a small JSON contract (`CONTRACT.md` in each repo). Patient 360, the MCP server and the iOS app consume only those contracts, and fall back to a saved snapshot when a module is down.

## How each challenge works

Each panel shows the data, the model, how it was validated, what the user sees, the held-out results and the honest limits.

### C1 · Care-team risk

![C1 Care-team risk](docs/c1.png)

### C3 · Bad Week Radar

![C3 Bad Week Radar](docs/c3.png)

### C4 · Glucose Guide

![C4 Glucose Guide](docs/c4.png)

### C5 · Coach's Co-pilot

![C5 Coach's Co-pilot](docs/c5.png)

Diagrams are made in Paper; the PNGs in `docs/` are exports.

## Honest limits

- The module cohorts are separate synthetic datasets supplied by the sponsors; they share no patient ids. Cross-module views use composite synthetic personas, labelled as such.
- C1 ranks no better than its baseline; its gain is calibration. It ranks NH Black survivors poorly (n = 47) and under-predicts at 75+; the UI warns for both.
- C3's lead time is shown on synthetic data; in the real fatigue study the wearable does not forecast the next day.
- C4's real-data checks point the same way as the synthetic effects but do not prove them.
- C5 agrees with AnnoMI experts 75.0% of the time vs 83.9% expert-to-expert agreement (91–93% where all experts agree).

## Repo layout

`modules/` holds each module as a git submodule. Clone with:

```sh
git clone --recurse-submodules <this repo>
```

| Module | GitHub |
|---|---|
| coach-console | https://github.com/zaycruz/coach-console |
| c1-acute-risk | https://github.com/zaycruz/c1-acute-risk |
| c3-rough-patch | https://github.com/zaycruz/c3-rough-patch |
| c4-glucose-guide | https://github.com/zaycruz/c4-glucose-guide |
| coach-copilot | https://github.com/zaycruz/coach-copilot |
| challenge-mcp | https://github.com/zaycruz/challenge-mcp |
