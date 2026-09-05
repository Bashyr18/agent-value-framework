# Architecture

## Control plane vs execution plane

AVF separates policy from implementation.

```text
CONTROL PLANE (repository-owned)
  project invariants
  risk and capacity rules
  model-role profile
  skill governance
  quality gates
  state/rehydration contract
  telemetry schema

EXECUTION PLANE (coding-agent runtime)
  root/orchestrator
  runtime capacity evidence
  workers
  specialist reviewers
  tools
  tests/builds
```

Changing a model, account, or provider should not require redesigning the control plane.

The [static architecture diagram](agent-value-framework-architecture.html) shows the same control flow. Its authored source is [agent-value-framework-architecture.json](agent-value-framework-architecture.json).

## Stable root pattern

The default architecture keeps one capable root model stable through the normal task lifecycle. Other models are bounded children or advisers rather than repeated replacements of the root conversation. Capacity and entitlement are checked before price optimization.

```text
developer/agent → AVF interface → stable orchestrator
                         ↑       ↑       ↑       ↑
                 profile/price capacity skills task-state
                         │       │       │       │
                         └───────┴───────┴───────┘
                                  │
                         bounded worker → repository
                                               │
                                         deterministic gates
                                           │ pass → accepted
                                           └ fail/uncertain → review/rescue
                                                               │
                                                               └→ orchestrator

provider adapter → runtime observations → capacity/route verification
```

Benefits:

- less root context pollution;
- fewer model-switch continuity failures;
- cheaper implementation volume;
- explicit escalation;
- easier telemetry attribution;
- unavailable or unentitled routes are removed before economic comparison.

## Worker contract

Every mutating worker should receive:

```text
OBJECTIVE
OWNED_FILES_OR_SUBSYSTEM
RELEVANT_INTERFACES
DECISIONS_ALREADY_MADE
INVARIANTS
ACCEPTANCE_CRITERIA
REQUIRED_VALIDATION
ESCALATION_CONDITIONS
```

The worker should return:

```text
FILES_CHANGED
SUMMARY
VALIDATION
ASSUMPTIONS
RISKS_BLOCKERS
```

This is semantic compression: expensive reasoning is converted into an executable contract.

## Quality architecture

Use five layers:

1. **Feasibility** — check entitlement, capacity, capabilities, policy and the quality floor.
2. **Decomposition** — remove ambiguity before cheap execution.
3. **Deterministic gates** — tests, typecheck, lint, build, static analysis, schema checks.
4. **Risk-based review** — only for properties tests do not adequately establish.
5. **Escalation** — strong reasoning when evidence shows the cheap path is insufficient.

## Parallelism

Parallelize when work is independent and read-heavy. Be conservative for overlapping mutation.

Expected benefit:

```text
B_parallel = saved_wall_time_value + quality_gain - extra_model_cost - coordination_cost - merge_conflict_cost
```

Only parallelize when `B_parallel > 0` for your objective. For a money-first policy that ignores human wait cost, the bar for parallelism is intentionally high.

## Account portability

Store in repository:

- project instructions;
- routing intent;
- risk rules;
- quality commands or references to existing commands;
- explicit project skill;
- state schema;
- runtime diagnostics.

Do not store:

- credentials;
- account tokens;
- model entitlements;
- private machine paths;
- browser sessions;
- organization policy copies.

A new account may lack the requested model. AVF should detect and report the capability gap rather than silently claim equivalence.
