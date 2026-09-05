# Evaluation and telemetry

## The benchmark-to-telemetry transition

Public benchmarks are useful for bootstrapping a route. They should lose decision weight as repository-specific evidence accumulates.

### Phase A — no local data

Use:

- public coding-agent benchmark priors;
- official model prices;
- task risk class;
- deterministic verifiability;
- conservative escalation rules.
- observed capacity and entitlement when the host exposes them; otherwise record unknown.

### Phase B — early telemetry (future v0.3)

Track by task class:

- spend;
- gate pass/fail;
- retries;
- escalation;
- reviewer findings;
- acceptance;
- capacity mode, pool and fallback safety;
- intended/effective route and transition reason;
- entitlement/availability state and any project-assigned capacity opportunity cost.

### Phase C — mature routing

Route using local ECAC and quality metrics. Keep benchmark data as a sanity check for model-generation changes, not the primary optimizer.

## Minimum useful dataset

```csv
task_id,task_class,risk_band,route,model_spend,tool_spend,retries,reviewed,escalated,accepted,capacity_mode,capacity_pool,intended_route,effective_route,entitlement_state,availability_state,fallback_safety,transition_reason,capacity_opportunity_cost
```

Add post-merge incident/revert signals when available.

## A/B changes carefully

When changing worker model or effort, compare similar task classes. Do not claim savings if the cheaper route shifts work into human review or post-merge repair that you failed to measure. Do not estimate unavailable quota from model identity, token count or UI assumptions.

## Model upgrades

Re-evaluate when:

- model pricing changes;
- a promotional price expires;
- the coding-agent harness changes materially;
- context/tool capabilities change;
- your task distribution changes;
- a new model moves the quality-cost Pareto frontier.
