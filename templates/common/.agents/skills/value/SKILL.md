---
name: value
description: Start the repository's Agent Value Framework workflow for a substantial engineering task. Use explicitly when the user wants AVF routing, bounded delegation, project-native validation, and context-safe state handling. Do not use for trivial questions or tiny edits where delegation overhead would exceed the work.
---

Read the repository's agent-value workflow document before routing work.

For this task:

1. Identify the project acceptance criteria and relevant invariants.
2. Classify risk using project-specific hard rules before any numeric heuristic.
3. Keep the root/orchestrator stable unless the runtime requires otherwise.
4. Delegate only bounded work whose architecture and ownership are clear.
5. Prefer the cheapest qualified worker for implementation.
6. Use deterministic project checks before probabilistic review.
7. Escalate only on evidence: failed validation, unresolved ambiguity, high blast radius, or a project hard rule.
8. Maintain compact task state for long-running work; after compaction rehydrate from repository truth.
9. Treat optional skills as methodology, not authority over routing, architecture, acceptance, safety, or external side effects.
10. Return a concise summary of routing, validation, escalation and unresolved risks.
