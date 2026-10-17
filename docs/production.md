# If this went into production: what we would do differently

Survivorship 360 was built in one day for a hackathon. It runs on sponsor-supplied, synthetic and public data, with no PHI. This page lists, area by area, what we built and what a real deployment at a cancer centre would need instead. The numbers cited here come from the [README](../README.md) and [`claims.tsv`](claims.tsv).

## 1. Data and identity

**Today (hackathon).** Each module uses its own sponsor cohort. The cohorts share no patient IDs, so the 360 view joins one record from each program into a labelled synthetic "linked demo record".

**In production.**
- Read from the EHR through FHIR (and the wearable, CGM and call platforms through their own feeds), not from static exports.
- One patient identity across all programs, from the hospital's master patient index. No composite records.
- Keep one `CONTRACT.md` per module, and validate every feed against it on arrival. Reject or quarantine rows that break it.
- Show data freshness on every tile ("data to …"), and alert when a feed is late.

## 2. Privacy and compliance

**Today (hackathon).** No PHI. Module data and saved calls sit in Cloudflare Workers, KV and Workers AI through AI Gateway, without a BAA.

**In production.**
- HIPAA scope for the whole stack, with a BAA from every processor that touches PHI: hosting, KV or its replacement, the model provider and the gateway. Where no BAA is possible, the data does not go there.
- Minimise PHI before any model call: send only the fields the prompt needs, with no names or MRNs.
- Written consent for call recording and transcription, captured before the call starts.
- A retention policy per data type (transcripts, audio, recaps, hand-offs), with deletion that actually runs.
- An audit log of who saw which patient, and when.

## 3. Access

**Today (hackathon).** The console has no login. The MCP server is open by design for the demo and supports an optional bearer key.

**In production.**
- Hospital SSO with roles: a coach, a nurse navigator and a physician each see what their job needs. A coach-only view shows calls and coaching, not hospital-risk drivers.
- Least privilege by default: a user sees only their own panel of patients unless their role says otherwise.
- The MCP server requires a key, with per-user scopes and the same patient-level access rules as the console. Every tool call is audited.

## 4. Clinical validation before use

**Today (hackathon).** Every number traces to a held-out or cross-validated run, but on sponsor data. The real-data checks are weak in places, and we say so.

**In production.**
- Run silent mode first: the models score real patients prospectively, nobody sees the output, and we compare against what happened. Then a pilot with outcome tracking.
- C1: external validation on the centre's own survivors, a decision curve at the alert line, and a comparison of the cohort with the Miami-Dade population.
- C3: prove the lead time on real wearables. In the real fatigue study the wearable did not forecast the next day (AUC 0.482).
- C4: an N-of-1, RCT-style check of the walk advice. In real adults the walk effect is small and not distinguishable from zero (−3.2 mg/dL, CI −6.9 to +0.5).
- C5: cut the false alarms (244 in 25,785 lines) on a fresh validation set without losing the suicide-risk catch (44 / 54), and validate tags and scores in Haitian Creole.

## 5. Safety operations

**Today (hackathon).** Red-flag rules raise banners and a fixed answer, and "Hand off to nurse" logs a hand-off. Nobody is on call to answer them.

**In production.**
- A named owner and a response time for each red-flag type, with after-hours routing to the on-call team.
- The crisis protocol (suicide risk, chest pain, fever on chemo) is owned by the clinical team and written into the product, not only into prompts.
- Every safety flag must be acknowledged and closed. "Close the loop" becomes a tracked task with an owner and a due time.
- Incident review for every missed or late flag, and its outcome feeds the next validation set.

## 6. Fairness monitoring

**Today (hackathon).** Each module reports subgroup results, and the weak spots are shown in the UI. For example, C1 ranks NH Black survivors poorly (AUROC 0.48, n = 47), so those cases carry `humanCheck.required` and a person reviews them before outreach.

**In production.**
- A subgroup dashboard per model (race and ethnicity, language, insurance, cancer type), with alert-line precision and recall and their CIs, refreshed on every data cycle.
- Extend the human-check safeguard to every group whose performance is not shown to be better than chance.
- A language field on every row and page, and an interpreter workflow: book the interpreter, then show clinician-reviewed scripts in the patient's language.

## 7. Model operations

**Today (hackathon).** Models are trained offline and served as committed JSON. Each module has a reproduce script and an E2E suite. C5 froze its stress sets before their first run.

**In production.**
- Version every model, prompt and Clef payload, and stamp the version and artifact hash on every response.
- Monitor drift in inputs and calibration in outputs, with recalibration triggers agreed in advance.
- A change-control gate: no model, prompt or payload change ships until it passes re-validation on frozen sets. Freezing the sets before the first run becomes policy.
- A model card per model: data, intended use, validation, subgroup results and known limits.

## 8. Generative AI

**Today (hackathon).** AI writes words only: the "Why now" summary, assistant answers, recaps and coaching cues. Every number, tier and queue row is fixed. Red-flag questions get a rule answer with no model call.

**In production.**
- Keep "words only". No model sets a tier, a number or a dose.
- Eval sets for the assistant, the recaps and the cues, with checks in CI for invented facts and any dosing or medical advice.
- A human reviews a sample of AI outputs every week, and the results are reported.
- Record where each label comes from (supervisor, clinician, model or LLM-written stress set), and keep the provenance with the data.

## 9. Reliability and capacity

**Today (hackathon).** All modules share one Workers AI per-minute quota. Clef slowed down when test runs competed with a demo. Tests ran against production with test-namespace isolation.

**In production.**
- Dedicated or reserved model capacity, and separate keys per environment.
- A staging environment separate from production. No judge, load or E2E traffic on production.
- Service-level objectives with alerting: first paint in 3–5 s at most, Clef tag latency, and fallback rate.
- Load tests at clinic scale before go-live.

## 10. Live calls

**Today (hackathon).** The coach toggles Coach or Patient by hand, and short mic clips are transcribed.

**In production.**
- Speaker diarization, or two-channel audio (one per speaker), so lines are attributed without a toggle.
- Integration with the telephony or video platform the coaches already use, with recording consent built into the call flow.

## 11. Regulatory

**Today (hackathon).** Designed as decision support: every number shows its basis, and the clinician decides.

**In production.**
- Assess the product against the FDA clinical decision support guidance, and keep it non-device CDS: the clinician can see the basis of every recommendation and makes the decision.
- IRB approval for the pilot, with an outcome-tracking protocol.

## 12. Workflow fit

**Today (hackathon).** A separate console with its own Today list and hand-off log.

**In production.**
- Put the queue into the EHR in-basket, so staff work in one place.
- Write documentation back to the chart: call recaps, hand-offs and outcomes.
- Training for coaches, nurses and physicians, including what each flag means and what it does not.
- Measure whether staff act on the queue (time to first contact, flags closed), and change the queue when they do not.

## What we would keep

- Fixed-rule ranking: one tiering rule builds the queue, not a model.
- AI writes words only.
- Red-flag rules run before any model call.
- Every number traces to a validation run.
- Honest limits are shown in the UI, not only in the docs.
