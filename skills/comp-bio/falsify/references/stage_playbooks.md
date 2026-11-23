# Extended Reference & Recipes

Toolbox: *base rate* (what is the prior probability before this specific case? — do not let a vivid case override the prior), *inversion* (what would guarantee the wrong answer?).

**Hypothesis-set discipline** (ACH / Heuer): before choosing, generate **3–7 mutually exclusive candidates**. The set must include at least one *awkward hypothesis* you do not believe — if you cannot write one down, you have a blind spot. Two candidates is an incomplete map, not a debate. If exactly one candidate survives your current facts, do NOT conclude: halt and generate 2–3 stress tests — either you are right and the tests will fail, or your alternatives were too weak. "Best of the available" is not "true": exhaust the candidate space first.

**Pre-commit the prediction** (harsh-critic / preregistration method): write down your prediction — including a probability — BEFORE you look at the confirming evidence. Then keep it. A prediction written after the evidence is not a prediction, it is a rationalization. Make it scoreable: a probability p that will be scored against the actual outcome y (Brier score: (p−y)²). If you cannot write a scoreable prediction, the hypothesis is not yet falsifiable.

**Pre-registered update rules** (debiasing / Galef): before looking at the evidence, write the rule that will move you — "if I observe Z, I will update to W%" — plus the acceptance criteria for Z (what makes the evidence valid: source quality, sample size, freshness). Lock the rule in while you are still objective; when Z arrives, apply the rule mechanically instead of re-deciding. This kills cherry-picking, goalpost-moving, and asymmetric evidence standards.

**Argument-mapping discipline** (Toulmin / van Gelder): draw the hypothesis's argument tree before attacking it: **contention** (the claim) → **reasons** (the supports) → **co-premises** (the hidden assumptions each reason silently depends on — this is where arguments are weakest) → **warrant** (the logical principle connecting reason to claim; a missing warrant is the single most common flaw). Flag the weak links: inferences that do not hold, and load-bearing premises with no support. An argument you cannot map, you cannot defend.

### Stage 3 — Adversarialize (对抗)
Attack your own hypothesis before anyone else can.
1. Build the strongest counter-argument (steelman the opponent).
2. List the three most likely ways your hypothesis is wrong.
3. Ask: what evidence would I refuse to accept? (If nothing would change your mind, you are not reasoning — you are defending.)

Toolbox: *pre-mortem* (it is a year later and this failed — why?), *Chesterton's Fence* (do I understand why this exists before proposing to remove it?), *red team* (how would an adversary defeat this plan?), *survivorship bias* (am I only looking at winners?).

**Quantify the failure modes** (superforecaster method): list the ways this could fail, estimate probabilities only where justified, and assess overlap/dependence. Add probabilities only for disjoint events; for arbitrary failures the sum is an upper bound on their union, not the failure probability. Reconcile the joint failure risk with the decision confidence without inventing precision.

**Attack in parallel, from different angles** (pre-mortem skill): attack your own reasoning chain itself, not just the plan — how would an adversary exploit the step where you are most confident? If useful, assess several perspectives without spawning agents unless separately authorized: the user, the machine, the developer, the support desk. Finding failure modes is not the same as attacking them — do both.

**Diagnostic-evidence check** (ACH / Heuer): score each piece of evidence against **all** candidates — C (consistent) / I (inconsistent) / N (neutral) / NA (not applicable). Count the **I's, not the C's**: consistent evidence proves nothing; inconsistent evidence is what discriminates. The winner is the hypothesis with the fewest contradictions, not the most confirmations. If every row is non-diagnostic, the question is under-specified or the evidence is too weak — reframe the question or gather better evidence before concluding.

**Protective-belt check** (Lakatos): separate the hard core (the claim you refuse to abandon) from the protective belt (auxiliary assumptions). If you keep adding auxiliary assumptions to rescue a failing hypothesis, that is a **degenerating research programme** — a red flag, not a rescue. A progressive programme predicts new facts; a degenerating one explains them away.

**Structure ≠ truth** (van Gelder): an argument map can be formally perfect while every premise is false. After flagging the weak links, inspect the load-bearing premises themselves — "even if this logic holds, is this premise actually true?" — before spending more effort on the structure.

**Reversal test** (Galef, scout mindset): would you accept the same evidence pointing the OTHER way? If you would accept evidence that supports you but dismiss the equivalent reversed evidence ("this source is biased", "sample too small", "outlier" — only when it disagrees), that is motivated reasoning, not reasoning. Fix: reject it both ways, accept it both ways, or weight it appropriately both ways — and if you detect the double standard, reassess source weights and assumptions; no fixed probability adjustment follows from merely naming a bias.

### Stage 4 — Verify (验证)
Gather evidence deliberately looking for **disconfirming** cases first (survivorship bias is the default failure).
- Grade every piece: **direct evidence / indirect / hearsay / inference**
- **Triangulate**: seek at least two independent sources or methods before raising confidence — one source agreeing with you is a starting point, not a proof.
- Describe confidence from evidence quality, dependence and scope. Use a numeric probability only for a defined event with a justified model or tracked forecast calibration; evidence grades alone do not imply percentages.
- Within the user's authorized scope, run the cheapest real test that could break your hypothesis — an actual command, a data lookup, a minimal experiment. If you cannot run a test, say so and downgrade your confidence.

Toolbox: *Bayesian updating* (how should each piece of evidence shift confidence, not confirm it?), *correlation vs causation* (is there a mechanism, or just co-occurrence?).

**Causal-ladder check** (Pearl do-calculus): name which rung you are on — **association** (observed co-occurrence), **intervention** (do(x): what happens if you change x), or **counterfactual** (what would have happened otherwise). A correlation is a ladder step, not the top; claims of "X causes Y" require causal identification assumptions and evidence adequate to the question; observational designs can identify causal effects under explicit assumptions. When the evidence is observational:
- **Backdoor check**: is there a confounder you failed to condition on? A hidden common cause can manufacture the whole association.
- **Collider trap**: if a variable is a collider (the common outcome of two causes), conditioning on it opens a path between its parents and *creates* bias that was not there. "We filtered by X and saw Y" can be a pure selection artifact — the filter itself is the bias. Study design labels alone do not establish validity: assess bias, identification, measurement, applicability and precision for the specific causal question.

**Bias audit** (Galef / lex-bias): before locking confidence, run the six quick checks and name each hit with its direction and estimated magnitude:
- *Confirmation*: did I seek disconfirming evidence, or only supporting?
- *Availability*: am I relying on memorable/recent examples instead of representative data?
- *Anchoring*: did I form my own estimate before seeing the numbers that framed this?
- *Affect heuristic*: am I confusing what I WANT with what WILL happen?
- *Overconfidence*: are my confidence intervals too narrow for the reference class? (Surprise test: if outcomes fall outside your CIs more often than they should, recalibrate using held-out outcomes and the intended interval coverage; no universal widening factor is established.)
- *Sunk cost*: am I continuing a failing path because of what was already spent?
For each plausible bias, state how it could affect evidence selection and seek a concrete correction; do not assign a numeric adjustment without evidence. Full 25-bias quick reference (category / impact / detection / remediation): `references/bias-catalog.md`.

**Severity check** (Mayo): a test only counts if it would have caught a wrong hypothesis — low P(E|¬H). Evidence that would appear under both H and ¬H is weak evidence, no matter how consistent it looks. List the auxiliary assumptions explicitly (Duhem-Quine): if the test fails, the culprit may be any of them, not the core hypothesis.

**Fermi fallback** (cc-thinking-skills): when data is missing, do a bounded order-of-magnitude estimate instead of guessing or refusing. State the estimate, the visible bounds (best case / worst case), and what data would tighten it. An estimate with bounds is information; a bare guess is noise.

**Calibrate like a forecaster**: define the event and resolution criterion before assigning a probability; otherwise use a qualified verbal assessment — and state the kill criteria that would move that probability down. Score your own predictions over time (Brier: (p−y)²); if your 0.55 predictions are right as often as your 0.95 ones, you are overconfident, and honesty means reporting the discrepancy.

**Likelihood-ratio calibration** (Bayes, odds form): when new evidence arrives, update by the likelihood ratio, not by how the evidence feels. LR = P(E|H) / P(E|¬H). An LR >1 favors H relative to the specified alternative; <1 favors the alternative. No finite LR is definitive regardless of the prior, and invented likelihoods are not calibration. Posterior odds = prior odds × LR (multiply even when LR < 1); p = odds / (1 + odds). Use a previous posterior only for the same evolving model and avoid double-counting reused or dependent evidence; sequential likelihoods must be conditional on prior evidence. If you cannot state P(E|¬H), you have not yet stated what the evidence would look like if you were wrong — go back to Stage 3.

### Stage 5 — Converge (收束)
- Conclude only what the evidence supports; quote the graded evidence, not vibes.
- Make the verdict **checkable**: include the specific claim someone can verify or the test that would change your mind. An unverifiable verdict is a posture.
- State explicitly what remains **unknown**.
- If a hypothesis died, record the corpse in the ledger — dead hypotheses are assets.
- State a concise evidence-based conclusion and residual risk; include a probability only when justified and label subjective estimates.
- **Label the reasoning type** — say which inference you used, and calibrate to its strength:
  - *Deductive* (rules → conclusion): strong but brittle — verify the premises, not just the chain.
  - *Inductive* (cases → generalization): probabilistic — state the sample and its bias.
  - *Abductive* (evidence → best explanation): weakest — always list at least one alternative explanation.
  - *Analogical* (A is like B): similarity is not identity — name where they differ.
  - *Counterfactual* (what-if): state the actual world vs the imagined world explicitly.
- **Multi-perspective review** before finalizing (MetaCrit / empathy-audit): re-read the verdict as (1) the executor — will this actually work? (2) the stakeholder — does this serve the person acting on it? (3) the skeptic — what is the strongest objection left? If the three views disagree, the verdict is not converged yet.
- **Strong opinions, weakly held** (decision theory): commit to the verdict enough to act on it, but state the condition under which you would revise it.
- **Split the uncertainty signal** (arXiv 2606.19559): report action-confidence ("I am X% sure, act accordingly") separately from request-uncertainty ("the question itself was under-specified: 0 fully specified / 0.5 open parameters / 1 critical information missing"). A confident answer to an ambiguous question is not a good answer.
- **Sensitivity analysis** (ACH / Heuer): remove the load-bearing evidence and re-run the verdict. If the conclusion flips, it was fragile — name the single piece of evidence that, if wrong, would change the answer. A verdict that survives removal of any one piece is robust.
- **Self-reflection warning** (Huang et al. 2023, *LLMs Cannot Self-Correct Reasoning Yet*): re-reading your own reasoning is not verification. Without an external signal — a test, a data lookup, an independent source — reflection tends to drift, not improve. If the only thing that changed between draft and final is "I looked at it again", the extra confidence is not earned. Name the external signal, or keep the original confidence.
- **Expected-value decision rule** (decision theory): when the verdict feeds a choice, go one step further and make the choice explicit — EV = Σ(pᵢ × vᵢ) over mutually exclusive, exhaustive outcomes (probabilities must sum to 1.0). Guardrails: for one-shot, high-stakes bets use expected *utility* (risk aversion), not raw EV; never round low-probability tail risk to zero; exclude sunk costs — only future costs and benefits count; in sequential decisions, keep the option value (the choice to stop, pivot, or wait). Pick a rule and say which: maximize EV, maximize EU, minimize maximum regret, or satisfice. If you cannot write probabilities and payoffs, the decision is under-specified — say so.

**MUST/WANT decision analysis** (Kepner-Tregoe): when the choice has multiple criteria rather than clean probabilities, screen before you score — define pass/fail **MUSTs** and weighted **WANTs** (importance 1–10) BEFORE seeing the options; eliminate anything that fails a MUST; score survivors against each WANT on the same scale and total the weights. Then test the downside: for leading options, list adverse consequences with probability × impact, and check which weight change or assumption would reverse the ranking. A high total that conceals a ruinous failure mode is not a win — if no option passes the MUSTs, return "none" rather than force a winner.
- If the conclusion is a hard-to-reverse decision, record it (decision log / ADR: **Context → Decision → Alternatives considered → Consequences → Status**; for product/strategy calls, the **PR/FAQ** working-backwards variant — future-dated press release + internal FAQ holding the evidence, assumptions, constraints, and stop conditions — keeps the decision honest instead of a marketing story). Reversible decisions can stay in the conversation.

## The Nudge


When the question does not warrant full depth but the answer will still be acted on, do not run the five stages — append **at most 2–3 short questions**, once per conversation, each tied to something specific in the answer just given. **High-stakes ballparks are NOT nudge territory:** a rough medication dose, security capacity, or production sizing estimate is Depth — being wrong there costs more than the shortcut saves.

1. **Check a fact** — "which claim here would be worth verifying, and against what?"
2. **Probe a step** — "where did the reasoning take a jump you might want justified?"
3. **Surface missing context** — "what did I have to assume because you didn't say?"

Skip the nudge for creative writing, simple lookups, purely educational explanations, or when the user already asked you to double-check. Once per conversation only — repetition turns a light nudge into nagging.

## Best Practices

### Red Flags


These thoughts mean STOP — you are rationalizing:

| Thought | Reality |
|---|---|
| "This is obviously true" | Evidence, or it's an opinion. |
| "Everyone knows X" | Base rate + two independent sources, or it's hearsay. |
| "The data looks clear" | Did you hunt for disconfirming cases? |
| "I've seen this pattern before" | A prior, not proof. Re-check against this specific case. |
| "It should work" | Run the cheapest test, or downgrade the confidence. |
| "It's probably fine" | What would make it NOT fine? Name it. |
| "I don't need to verify this" | That is the moment verification matters most. |
| "I already know the answer" | Orientation check: is the conclusion pre-sealed? |

### Guardrails


- **Never fabricate evidence.** A name, number, date, quote, or source must come from the actual evidence or be labeled a guess.
- **Do not call a 90% prediction certain.** Use calibrated language and reserve certainty for appropriately established claims.
- **Never present "may" as "must".** Possibility is not probability; probability is not fact.
- **Never hide a failed hypothesis.** Record it; a skill that hides failures is a propaganda engine.
- **Never argue with the user's facts without evidence.** Challenge the claim, not the person. If their evidence is stronger, change your mind — publicly.
- **Never let the protocol outrank the answer.** Depth is a tool you reach for, not a costume you wear. Simple question → simple answer.
- **诚实先于体面**: admitting uncertainty is not weakness; it is the only thing that makes the rest of the answer trustworthy.
- **Circle of competence**: outside your (or the verified sources') area of competence, the correct answer is "I don't know" — not a hedged guess. Saying "I don't know" IS the calibrated answer.
- **Two-hypothesis discipline**: if you can only imagine one explanation, look for a second before concluding. A single surviving hypothesis is usually an unexamined assumption.
- **Never explain everything**: a hypothesis that post-hoc fits every possible outcome is unfalsifiable — name at least one outcome that would have contradicted it.
- **Structure ≠ truth**: a flawless argument map proves nothing if its premises are false — verify the load-bearing premises, not just the logic.
- **Reflection is not verification**: re-examining your own reasoning without an external signal adds no evidence (Huang et al. 2023) — name the test or the source that changed your confidence.
- **Desire ≠ forecast** (Galef): separate what you want from what will happen. If the desired outcome and the predicted outcome are the same number, check whether you are forecasting or hoping.
- **Sunk costs stay sunk**: what was already spent does not justify continuing — only future costs and benefits enter the decision.

## Limitations

- The protocol changes *how* an agent concludes, not *what* the agent knows — it cannot manufacture evidence the model was never given, and it must never be used to fabricate sources or confidence.
- No amount of internal falsification substitutes for an external signal: re-examining your own reasoning without new evidence adds no confidence (Huang et al. 2023). When a claim needs ground truth, the agent must name the test or the source that changed its confidence.
- The skill is contextual, not mandatory: it must not turn simple lookups or small talk into thesis defenses. Depth is a tool, not a costume.
- Outside the agent's (or the verified sources') area of competence, the calibrated answer is "I don't know" — not a hedged guess.

## Security & Safety Notes

- This is a pure reasoning protocol: it runs no shell commands, makes no network calls, and accesses no credentials by itself.
- When the protocol is applied to security-sensitive conclusions (auth, crypto, data handling), the agent must treat its own verdict as a hypothesis until verified against the actual system, environment, or threat model — never as a substitute for environment-specific validation or expert review.
- Do not use the protocol's confidence language to overstate certainty to a user. Numeric self-ratings are not measured reliability and must not determine authorization for high-impact actions.

## Common Pitfalls

- **Problem:** The agent concludes first, then reverse-engineers a falsification path.
  **Solution:** Write the hypothesis and its potential disproof *before* gathering supporting evidence; if the falsification path is written after the verdict, discard it and restart.
- **Problem:** The agent treats "structure" as proof — a clean argument map with false premises.
  **Solution:** Verify the load-bearing premises themselves, not just the logic (structure ≠ truth).
- **Problem:** A single explanation survives, so the agent concludes.
  **Solution:** Two-hypothesis discipline: if you can only imagine one explanation, look for a second before concluding — a single surviving hypothesis is usually an unexamined assumption.

## Related Skills

- `@test-driven-development` — When the claim is about code behavior, use TDD to make the falsification test explicit before writing code.
- `@systematic-debugging` — When the claim is about a bug's cause, run root-cause investigation before proposing fixes; falsify the root cause, don't patch symptoms.
- `@verification-before-completion` — When the claim is "the work is done", verify with real commands and evidence before asserting completion.

## The Thinking Ledger


When depth mode is active, provide a concise decision/evidence summary rather than private chain-of-thought or exhaustive internal deliberation. Use a compact ledger of claims, sources, tests, assumptions, alternatives and outcomes (see `assets/thinking-ledger.md`). The ledger records inspectable evidence and decisions; it does not prove that the protocol improved accuracy.

---

*Falsify is built on a simple inheritance: 公理 → 假设 → 对抗 → 验证 → 收束. Axiom → Hypothesis → Adversarialize → Verify → Converge. The five stages of the Unified Theory, turned into a thinking protocol anyone can run.*
