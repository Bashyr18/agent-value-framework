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

### Phase B — early telemetry

Track by task class:

- spend;
- gate pass/fail;
- retries;
- escalation;
- reviewer findings;
- acceptance.

### Phase C — mature routing

Route using local ECAC and quality metrics. Keep benchmark data as a sanity check for model-generation changes, not the primary optimizer.

## Minimum useful dataset

```csv
task_id,task_class,risk_band,route,model_spend,tool_spend,retries,reviewed,escalated,accepted
```

Add post-merge incident/revert signals when available.

## A/B changes carefully

When changing worker model or effort, compare similar task classes. Do not claim savings if the cheaper route shifts work into human review or post-merge repair that you failed to measure.

## Model upgrades

Re-evaluate when:

- model pricing changes;
- a promotional price expires;
- the coding-agent harness changes materially;
- context/tool capabilities change;
- your task distribution changes;
- a new model moves the quality-cost Pareto frontier.
