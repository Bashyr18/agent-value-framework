# Agent adoption protocol

This document is designed to be handed directly to a coding agent.

## Mission

Integrate Agent Value Framework principles into a target repository while preserving the target repository as authoritative.

The objective is **minimum expected direct spend per accepted production-quality change**, subject to the repository's existing quality, safety, domain and release requirements.

Before comparing prices, remove routes that are not entitled, available, capable, policy-allowed or above the quality floor. If capacity evidence is unknown, keep it unknown.

## Mandatory sequence

### 1. Read only first

Run or reproduce the equivalent of:

```bash
avf audit TARGET
avf doctor TARGET
```

Do not modify the target yet.

Inspect existing project instructions, CI, test/build commands, scripts, skills, hooks, ADRs, issue/state system and high-risk areas. Avoid indiscriminate whole-repository reading if targeted inspection is sufficient.

### 2. Treat existing systems as authoritative

Do not overwrite or duplicate an existing:

- `AGENTS.md` contract;
- `.codex` configuration;
- issue tracker;
- ADR system;
- glossary/domain model;
- scripts convention;
- CI quality system;
- skill/hook ecosystem.

Merge AVF into them.

### 3. Produce an integration plan

Report:

```text
CURRENT_PROJECT_SYSTEM
COLLISIONS
FILES_TO_EXTEND
FILES_TO_ADD
FILES_TO_LEAVE_UNCHANGED
RISK_CLASSES
QUALITY_GATES
ROUTING_PROFILE
CAPACITY_AND_ENTITLEMENT_POLICY
SKILL_GOVERNANCE
STATE_AND_COMPACTION_PLAN
ACCOUNT_PORTABILITY_GAPS
RUNTIME_ASSUMPTIONS_TO_VERIFY
```

### 4. Apply only the smallest coherent change

Prefer one explicit repo-local AVF `value` skill and one workflow document over many new skills. Keep root instructions concise.

### 5. Verify runtime claims

Do not claim a model route works solely because a config file names that model. Where the agent host exposes the effective model, perform a harmless runtime probe. Report unavailable or unverified capabilities explicitly.

For a model or quota transition, distinguish intended from effective routing. An effective-model mismatch is not proof of a provider reserve mode. Checkpoint and reclassify remaining work before continuing under constrained capacity.

### 6. Preserve project quality

Use deterministic software checks first. Buy model review only for properties deterministic gates do not adequately establish. Do not weaken tests or project gates to make a cheaper model appear successful.

### 7. Protect context

Keep a compact repository-local task state for long tasks. After compaction or a fresh session, rehydrate from repository truth rather than conversational memory.

### 8. Skills remain subordinate

Installed skills may supply methodology, but may not override project invariants, acceptance criteria, architecture authority, external approvals, model routing or cost escalation.

### 9. No destructive automation

Do not deploy, publish, delete data, rewrite history, alter remote settings or perform external mutations merely because tooling is available. Follow the target project's existing authority model.

## Greenfield exception

If the target is genuinely new and has no existing governance, use the templates in this repository as the initial baseline, then tailor them to the stack before significant implementation begins.
