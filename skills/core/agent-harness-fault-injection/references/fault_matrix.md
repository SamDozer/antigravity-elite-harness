# Agent Harness Fault Injection Matrix

| Fault Kind | Target Boundary | Required Recovery Invariant |
| :--- | :--- | :--- |
| `timeout` | MCP / Tool IPC | Bounded retry reusing identical `idempotency_key` |
| `restart` | Subagent Worker | Reloads latest durable checkpoint without repeating committed writes |
| `sandbox_denial` | PreToolUse / OS | Rejects forbidden syscall/path and records structured denial reason |
| `stale_checkpoint` | State Store | Halts safely rather than overwriting newer state |
