# Witness Hierarchy & Evidence Grading

1. **Tier 1 (Strongest):** Immutable platform state, cryptographic digests, exit codes, and external system records.
2. **Tier 2:** Durable harness event logs (`transcript.jsonl`) with correlated `request_id` and `output_digest`.
3. **Tier 3:** Ephemeral stdout/stderr snippets captured during execution.
4. **Tier 4 (Weakest - Never Sufficient Alone):** Agent conversational prose claiming "all tests passed".
