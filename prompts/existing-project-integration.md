# Existing-project integration prompt

Read the Agent Value Framework documentation, especially `docs/AGENT_ADOPTION.md`, `docs/EXISTING_PROJECT.md`, `docs/MATH.md`, and the adapter relevant to this coding-agent host.

Target repository: **the repository currently open in this agent session**.

This is an existing project. The target repository is authoritative.

Do not modify files yet.

1. Run or reproduce the AVF read-only audit.
2. Inspect existing agent instructions, provider configuration, skills/plugins/hooks, CI, scripts, test commands, ADRs/domain docs, and any existing task/evidence system.
3. Identify high-risk areas where cheap workers must not independently decide architecture or semantics.
4. Identify the cheapest deterministic validation commands for small, medium, and release-scale changes.
5. Identify account/machine-local behavior that would disappear on a fresh clone.
6. Produce an AVF integration plan that extends existing systems rather than creating competing ones.
7. Explicitly distinguish verified runtime capabilities from desired model-routing intent.

Only after the plan is coherent should you make the smallest project-native integration changes.

Never overwrite existing `AGENTS.md`, `.codex`, hooks, CI, skills, issue tracking, ADRs, or scripts blindly. Never weaken project quality requirements to reduce model spend.

The optimization target is minimum expected direct spend per accepted production-quality change, not minimum cost per call.
