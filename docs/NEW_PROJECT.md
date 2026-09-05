# Greenfield setup

A new project can adopt AVF before local conventions accumulate.

## Recommended baseline

```text
project/
├── AGENTS.md
├── docs/
│   └── agents/
│       └── agent-value-workflow.md
├── .agents/
│   └── skills/
│       └── value/
│           ├── SKILL.md
│           └── agents/openai.yaml
├── .avf/
│   ├── policy.toml
│   ├── model-profile.toml
│   └── capacity-policy.toml
└── provider-specific adapter files
```

For Codex, the adapter can additionally create `.codex/config.toml`, custom agents and small hooks after validating the installed Codex schema.

## Keep root instructions small

`AGENTS.md` should contain durable project invariants and a pointer to the detailed workflow. Do not paste every skill, routing formula, test command and model instruction into the root context.

## Establish validation early

Create one fast verification path before broadening the codebase. A greenfield project that has no deterministic tests forces the framework to buy model review for properties software could otherwise prove cheaply.

## Start collecting telemetry immediately

Even simple CSV/JSONL is enough:

```text
timestamp, task_class, risk_band, route, spend, retries, accepted
```

Public model benchmarks become less important as your own accepted-change history grows.

Add a small capacity policy beside the model profile. It should define unknown-entitlement handling, checkpoint-on-fallback, reserve permissions and pause rules. It must not claim that a particular account has reserve capacity.
