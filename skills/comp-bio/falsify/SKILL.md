---
name: falsify
description: "Applies the scientific falsification thinking protocol for high-stakes scientific, architectural, and diagnostic hypotheses: hypothesis formulation, adversarial disproof, Bayesian evidence updates, and Brier calibration. Use when investigating ambiguous scientific anomalies, root-cause hypotheses, or irreversible architectural trade-offs. Do NOT use when answering trivial single-lookup facts or routine boilerplate edits."
source_repo: sickn33/agentic-awesome-skills
risk: safe
---


# Falsify — The Scientific Thinking Protocol

> Think like a first-rate scientist: doubt first, verify, then believe.
> 像一流科学家一样思考：先证伪，再相信；先标不确定，再下结论。

## Overview

falsify is a Markdown reasoning framework with bundled references and a ledger template. It can help organize hypotheses and external evidence; it does not guarantee accuracy, calibration or compatibility with every agent. Named concepts are prompts for review, not a validated combined scientific protocol; the complete claimed 70-source derivation is not documented here.

## The Iron Law


```
NO VERDICT WITHOUT A FALSIFIABLE HYPOTHESIS.
没有可证伪的假设，就没有结论。
```

<EXTREMELY-IMPORTANT>
For empirical claims, identify observations that could change the conclusion. Definitions, mathematics, value judgments and underdetermined evidence require a different validation method; do not force a falsification test onto every answer. A confident answer with no falsification path is not an answer — it is a guess wearing a lab coat. There is no exception for "obvious" or "well-known" or "everyone knows" — those are exactly the claims that need falsifying most.
</EXTREMELY-IMPORTANT>

## MODE SELECTION — route BEFORE answering (mandatory)

First decide which mode this question is, then act accordingly. **Do not run the five stages unless you picked Depth.** The wrong mode is itself a protocol failure.

| If the ask is... | Mode | Do |
|---|---|---|
| Live incident / production down / outage / "act now" / degrading | **Incident (OODA)** | **Follow the authorized incident runbook** with the evidence needed for the risk with a known rollback and a time box. Do NOT run the five stages. Stabilize, then falsify the effect. Never demand certainty before a reversible action under time pressure. |
| Trivial / one-lookup fact / small talk / zero consequence | **Simple** | Answer briefly and directly. No protocol, no follow-up questions, no stage labels. |
| Rough estimate / ballpark / "about how much" / "大概" (low-stakes, reversible) | **Nudge** | Give the helpful estimate with its main assumption stated, then 2–3 targeted questions. No five-stage ledger. If being wrong costs time/money/trust, escalate to Depth. |
| Under-specified / unfalsifiable / missing key inputs | **Question** | Ask only the few missing inputs that block a safe answer; provide a default only where justified. Do not conclude, do not fabricate a default justification. |
| High-stakes / correctness gate / "why" about a failing system / will be acted on | **Depth** | Run the five stages below. |

In an incident, the Iron Law means "act reversibly, then falsify the effect" — never "analyze first, act later".

## When to Use This Skill


**Activate (depth mode)** for:
- Architecture / design decisions with trade-offs
- "Why" questions about a failing system or data anomaly
- Recommendations that will be acted on (a library, a fix, a strategy)
- Claims about what a user, market, or system "will" do
- Anything where being wrong costs time, money, or trust


**Default to Nudge (not depth) when the ask is a rough ballpark** — "rough estimate", "ballpark", "about how much", "大概", "粗略": give the helpful estimate directly with its main assumption stated, then 2–3 questions. A rough number is not a correctness gate; forcing a five-stage ledger onto it is protocol theater. **Exception — high-stakes ballparks go to Depth:** if the estimate will be acted on and an error costs time, money, or trust (a rough medication dose, security capacity, production sizing), do NOT nudge: gather the key inputs, state the uncertainty, and falsify before giving the number. The shortcut only pays when the error is cheap.

**Do NOT activate (answer simply)** for:
- Factual recall you can verify in one lookup
- Trivial questions where the answer is obvious and consequences are zero
- Small talk. Not everything is a thesis defense.

Every rule below is contextual: read the question first, then pull only what fits. When in doubt, default to a **one-line answer + one-line reason** — then offer depth.

## How It Works


Each stage has a deliverable. Do not skip ahead. The protocol is the point. A compact mental-model toolbox sits under each stage (full catalog: `references/mental-models.md`).

### Stage 0 — Read the room (读题)
Restate the actual question in one sentence. Name the stakes: who acts on this answer, and what happens if it is wrong. If the question is ambiguous, state your reading and proceed — do not stall.

**Orientation check** — before reasoning, notice if the answer is already emotionally committed (this is not about the user; it is about you):
- *Conclusion-preserving*: already leaning one way and explaining away the rest → ask "what would have to be true for the other side to win?"
- *Completion-seeking*: wants *an* answer, not *the right* answer → insert a pause before settling.
- *Authority-preserving*: attached to sounding expert → stress-test the idea as if advising someone else.
- If you catch any of these, name it silently and compensate. Orientation is the most common failure; the five stages cannot fix a conclusion that was pre-sealed.

**Frontier questioning** — if you need input from the user, ask the whole open frontier in **one round**: number each question and give your recommended answer next to it. Never ask for anything you could look up yourself. One question at a time is interrogation, not collaboration. The user's answers unblock the next frontier; recompute and repeat.

**Effort routing** (Kahneman dual-process / Simon bounded rationality): before choosing depth, route the question explicitly. Low stakes, reversible, or one cheap lookup → **System 1**: answer fast, keep it light. High stakes, irreversible, or a correctness gate (tests, security, "did the fix work?") → **System 2**: run the full protocol. Treat effort as a depletable budget with five states — automatic / fluent / effortful / strained / depleted — and when the budget is strained or depleted, say so instead of pretending to still be in deep mode. When a search has no natural endpoint, **satisfice**: pre-declare the pass/fail aspiration threshold BEFORE looking, search in encounter order, stop at the first option that clears it, and never move the goalposts after failure — relax only a criterion predeclared as non-load-bearing, and record the relaxation.

**Situation routing** (Cynefin / Snowden): before choosing a method, classify the cause–effect domain — the wrong-domain method is itself the failure mode. **Clear** (cause→effect obvious): sense, categorize, respond with a runbook — do not run a research project. **Complicated** (several valid expert answers): sense, analyze, respond — hypothesis testing fits here. **Complex** (emergent): probe with safe-to-fail experiments, sense what happens, amplify what works — you cannot predict your way out. **Chaotic** (no time to sense safely): act first to stabilize, then sense, then respond. **Disorder**: split the problem into parts and classify each. If the chosen domain's method stops working, reclassify — a runbook that fails on a Clear problem was not Clear.

**Time-pressure mode** (Boyd OODA): when the situation is moving and waiting for certainty costs more than a reversible action, do not run the full protocol — choose an authorized bounded mitigation with a known rollback, then immediately re-observe and loop: observe → orient (≥2 candidate explanations) → decide (action + predicted effect + next observation + time box) → act → re-observe. Exit the loop as soon as the system is stable or the next move is irreversible — then switch to the full protocol. Never OODA an irreversible launch; never demand 100% certainty for a reversible mitigation under time pressure.

### Stage 1 — Axiomatize (公理化)
Separate everything you know into three lists:
- **Established facts** — observations or accepted premises, with sources and relevant uncertainty
- **Assumptions** — things you are treating as true but have not checked
- **Hearsay** — claims with no evidence behind them

Toolbox: *first principles* (what is fundamentally true?), *MECE* (are my categories gap-free?). Output: three explicit lists. Anything not listed is not yet allowed into your reasoning. For problems that recur despite local fixes, add *systems leverage* (intervene at the highest feasible level: goals/paradigm → rules/information → loop structure → stock/flow → buffers/parameters — never polish a parameter when a rule is the lever).

**Outside view first** (superforecaster method): before reasoning about this specific case, name its reference class and the base rate — what usually happens in situations like this? Then decompose the question into parts and estimate each; reconcile against the reference-class benchmark, and if the gap is larger than ~20 points, investigate why before proceeding. The vivid details of the current case must not override the prior.

**Two-hypothesis discipline** (LessWrong): maintain at least two hypotheses that fit everything you currently know. If only one hypothesis survives your current facts, that is a signal your facts are incomplete, not that the hypothesis is proven.

**IS/IS-NOT bounding** (Kepner-Tregoe): for a selective defect — affects some objects/places/times/cohorts but not comparable others — bound the problem before theorizing. Build the matrix: for WHAT / WHERE / WHEN / EXTENT, record the **IS** side, the **closest comparable IS-NOT** side, and the **distinction** unique to the IS side; then list the **changes** near the first occurrence. A candidate cause survives only if it explains BOTH sides of the boundary — a cause that fits "only on Mondays" must also explain why not on Tuesdays.

### Stage 2 — Hypothesize (假设化)
Write the hypothesis as a falsifiable prediction:
```
If [H], then we should observe [O].
If [¬O] is reliably observed, reassess H and the auxiliary/model assumptions; probabilistic predictions are not refuted by every non-occurrence.
```
A hypothesis with no observable consequence is decoration. Rewrite it until it has one.


## Extended Reference
See `references/stage_playbooks.md` for full recipes, advanced workflows, and edge-case specifications.

## Deterministic Bayesian & Brier Scorer
Compute calibrated posteriors with `scripts/score_ledger.py`, record hypotheses in `assets/thinking-ledger.md`, and consult `references/stage_playbooks.md`.
