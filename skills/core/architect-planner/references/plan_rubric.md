# Architectural Plan Evaluation Rubric

Every implementation plan submitted by an agent or human architect is evaluated against these non-negotiable criteria:

| Dimension | Passing Standard | Failure Condition |
| :--- | :--- | :--- |
| **Atomicity** | Each task can be completed and verified in 2 to 15 minutes. | Monolithic multi-hour tasks that touch 10+ files simultaneously. |
| **Contract Freeze** | Types, schemas, and API contracts are fully defined in the plan before code is written. | Vague placeholders ("will determine API payload later"). |
| **Acyclic Beads DAG** | Dependencies are strictly ordered with no circular blocking relationships. | Circular dependencies or missing upstream prerequisite IDs. |
| **Grounded Verification** | Concrete CLI commands specified for each task with expected outputs. | Vague assurances ("verify manually" or "test should pass"). |
| **Rollback & Blast Radius** | Rollback mechanism and affected blast radius explicitly documented. | Zero risk analysis or assuming 100% first-pass perfection. |
| **SLOC Debloat** | Reuses existing repository helpers before proposing new utility abstractions. | Unprompted generic frameworks and speculative wrappers. |
