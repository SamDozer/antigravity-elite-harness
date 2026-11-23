# Multi-Agent State Ownership Patterns

1. **Single-Writer Coordinator:** Workers operate in read-only or isolated branch workspaces and return structured patch proposals; only the coordinator mutates canonical state.
2. **Disjoint Partitioning:** Parallel workers own strictly non-overlapping file paths (`write_paths`), verified prior to dispatch.
3. **Append-Only Event Ledger:** Workers emit immutable events with `idempotency_key`; a deterministic reducer computes state.
