# Greenfield bootstrap prompt

Read the Agent Value Framework documentation, especially `docs/AGENT_ADOPTION.md`, `docs/NEW_PROJECT.md`, `docs/MATH.md`, and the adapter relevant to this coding-agent host.

This is a greenfield repository with no established engineering governance unless you discover otherwise.

Before building product features:

1. establish concise root project instructions;
2. create a detailed agent-value workflow doc;
3. create one explicit repo-local `value` skill;
4. define a provider/model profile without embedding credentials;
5. establish a fast deterministic validation path;
6. define risk hard-rules for security, persistence, external side effects and irreversible changes;
7. define repository-backed task state for long work/compaction recovery;
8. define telemetry for model/tool spend, retries, escalation and accepted changes;
9. validate provider-specific config against the installed runtime before activation.

Keep the framework thin. Do not build a large orchestration platform before the application needs it.
