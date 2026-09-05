# Agent Value Framework (AVF)

**Spend less per accepted software change without lowering the quality bar.**

AVF is an open-source, repository-native framework for cost-aware coding-agent orchestration. It treats model selection as an engineering economics problem rather than a leaderboard problem.

The core objective is:

```text
minimize Expected Cost per Accepted Change (ECAC)
subject to project-defined quality, safety, and correctness constraints
```

AVF does **not** mean "always use the cheapest model." It means use the least expensive route that is expected to land a change cleanly, and buy stronger intelligence only where its extra cost is justified by avoided rework, reduced failure probability, or high downstream blast radius.

## Why this exists

Coding-agent spend is often optimized incorrectly:

- teams compare price per million tokens instead of price per accepted change;
- cheap agents are allowed to make architectural decisions they are poorly suited for;
- expensive agents are wasted on mechanical work;
- every task runs the full test suite and multiple reviewers;
- subagents multiply without a cost model;
- long contexts compact and lose operational state;
- user-level config makes the workflow change when an account or machine changes;
- installed skills silently inject competing instructions.

AVF separates these concerns:

```text
MODEL        provides intelligence
SKILL        provides methodology
ORCHESTRATOR decides routing and escalation
CAPACITY     represents scarce availability
ENTITLEMENT  constrains feasible routes
RUNTIME      supplies observed execution evidence
REPOSITORY   provides durable state and policy
TESTS/GATES  provide evidence of correctness
```

Price is considered only after entitlement, capacity, required capabilities, project policy and the quality floor make a route feasible. Unknown runtime facts stay unknown.

## The money-first reference architecture

A provider-specific profile can map roles to any models. The included OpenAI/Codex reference profile (snapshot: 2026-09-05) uses:

```text
Stable root/orchestrator:  GPT-5.6 Sol / medium
Default worker:            GPT-5.6 Luna / max
Optional reviewer:         GPT-5.6 Terra / high
Local rescue:              GPT-5.6 Sol / high
Critical technical adviser:GPT-6 Astra / high
```

This is a **profile**, not the framework. Replace the model names when pricing, capabilities, or your own evals change.

The OpenAI profile also documents Luna Reserve as a provider-specific fallback capacity example. It never stores account entitlement or assumes that an effective Luna model proves Reserve activation.

## The key metric: ECAC

If a route costs $0.30 but only 50% of its changes are accepted without another paid attempt, its stationary approximation is:

```text
ECAC = $0.30 / 0.50 = $0.60 per accepted change
```

If a $0.50 route lands 90% cleanly:

```text
ECAC = $0.50 / 0.90 = $0.556 per accepted change
```

The more expensive call is the better value.

v0.2 can include a project-assigned scarcity term for finite capacity:

```text
C_capacity_opportunity = Σ(shadow_price × expected_use)
ECAC_capacity = (attempt cost + capacity opportunity cost) / P(accepted)
```

An included allowance can have opportunity cost even when its immediate incremental cash charge is not represented as API billing. Set the shadow price to zero when that is the project's deliberate policy; do not invent provider values.

In production, use observed telemetry:

```text
Empirical ECAC = total model/tool spend / accepted production-quality changes
```

See [`docs/MATH.md`](docs/MATH.md) for the full model, break-even equations, escalation economics, and why benchmark scores must never be treated as acceptance probabilities.

## Existing project vs new project

### Existing / mature project

**Do not dump AVF templates into the repository.**

Use:

```bash
avf audit . > avf-audit.md
avf doctor .
```

Then give your coding agent the repository audit plus [`docs/AGENT_ADOPTION.md`](docs/AGENT_ADOPTION.md). The agent should merge AVF into the project's existing governance, scripts, tests, ADRs, CI, skills, and instruction hierarchy.

AVF's rule for mature repositories is:

> Existing project truth wins. Extend; do not duplicate.

### Greenfield project

Start with the framework contract before the codebase grows. Use the templates in `templates/` and the greenfield guide in [`docs/NEW_PROJECT.md`](docs/NEW_PROJECT.md). Keep the root instructions small; put detailed workflow policy in a dedicated project doc and expose one explicit task skill.

## Pointing an agent at AVF

An agent does not need this repository copied into the target project.

Give it the local path or public URL and say:

```text
Read docs/AGENT_ADOPTION.md in the Agent Value Framework.
Treat the target repository as authoritative.
Run the AVF read-only audit first.
Produce an integration plan before making changes.
Do not overwrite existing AGENTS.md, .codex, hooks, CI, skills, scripts,
or project governance. Adapt AVF to the repository rather than adapting the
repository to AVF.
```

The detailed agent contract is in [`docs/AGENT_ADOPTION.md`](docs/AGENT_ADOPTION.md).

## Context compaction is treated as an expected event

AVF does not attempt to eliminate native compaction. It makes compaction non-catastrophic by moving important task state out of conversation history.

A substantial task maintains a small state capsule containing:

```text
TASK
CURRENT_OBJECTIVE
DECISIONS
NON_NEGOTIABLE_INVARIANTS
FILES_OWNED
FILES_CHANGED
VALIDATION_PASSED
VALIDATION_FAILED
ASSUMPTIONS
UNRESOLVED_RISKS
LAST_DIFF_FINGERPRINT
NEXT_CONCRETE_ACTION
```

After compaction, the agent rehydrates from repository truth: state capsule, Git state, current diff, project instructions, relevant ADRs, and validation evidence.

Codex currently exposes `PreCompact`, `PostCompact`, and `SessionStart` with `source="compact"`; project hooks can use those lifecycle points while keeping injected context intentionally small. See [`docs/CONTEXT_COMPACTION.md`](docs/CONTEXT_COMPACTION.md).

## Skills are governed, not banned

AVF assumes developers may have large skill/plugin ecosystems. Skills are useful, but they are methodology—not authority.

Recommended precedence:

```text
platform/system safety
→ explicit user task
→ repository architecture and acceptance rules
→ AVF routing contract
→ task contract
→ optional skill methodology
→ model defaults
```

Broad architecture, migration, provisioning, deployment, or multi-agent skills should usually be explicit/manual. Narrow TDD, exploration, formatting, and accessibility skills can often be safely available to workers.

See [`docs/SKILLS.md`](docs/SKILLS.md).

## Quick start

Requires Python 3.11+ and has no runtime dependencies.

```bash
git clone <your-fork-or-repo-url>
cd agent-value-framework
python -m pip install -e .
avf --help
```

Audit a repository:

```bash
avf audit /path/to/repo
avf doctor /path/to/repo
```

Score an illustrative task risk profile:

```bash
avf risk \
  --ambiguity 0.2 \
  --blast-radius 0.3 \
  --coupling 0.2 \
  --domain-criticality 0.1 \
  --irreversibility 0.1 \
  --weak-verifiability 0.2
```

Calculate expected cost per accepted change:

```bash
avf ecac --base-cost 0.30 --verification-cost 0.05 --accept-prob 0.75
```

Inspect a manually supplied capacity snapshot with:

    avf capacity --regular exhausted --reserve available --intended-model gpt-5.6-sol --effective-model gpt-5.6-luna

This reports RESERVE plus any intended/effective route mismatch. It does not scrape quota or infer Reserve from a model name.

See the control plane in action in the [interactive architecture walkthrough](docs/agent-value-framework-architecture.html). Use **Guide → Play story** to trace economic control, capacity transitions, safe fallback and rehydration.

Find when an expensive route becomes economically justified:

```bash
avf break-even \
  --cheap-cost 0.30 \
  --premium-cost 1.20 \
  --cheap-fail 0.18 \
  --premium-fail 0.05
```

Estimate token cost using the included OpenAI snapshot:

```bash
avf token-cost \
  --profile examples/openai-codex-money-first/profile.toml \
  --model luna_worker \
  --input 500000 \
  --output 100000
```

## What AVF deliberately does not do

AVF does not:

- pretend public benchmark scores are your project's acceptance probabilities;
- replace project tests with model review;
- claim a model is safe for a domain merely because it scores well on coding benchmarks;
- bypass account, organization, sandbox, model-entitlement, or security policy;
- depend on one permanent model generation;
- parse private chain-of-thought;
- make native compaction a source of truth;
- treat unknown entitlement or capacity as available;
- lower the quality floor because a fallback route remains;
- claim that an effective model change proves a particular reserve mode;
- auto-deploy or perform external writes simply because an agent can;
- overwrite mature repository governance during installation.

## Project structure

```text
agent-value-framework/
├── src/agent_value_framework/  # dependency-free CLI and math
├── docs/                       # framework specification
├── templates/                  # provider-neutral + Codex templates
├── examples/                   # versioned reference profiles
├── tests/                      # deterministic unit tests
└── .github/workflows/          # framework CI
```

## Documentation map

- [docs/CAPACITY.md](docs/CAPACITY.md) — capacity, feasibility and fallback safety
- [docs/agent-value-framework-architecture.html](docs/agent-value-framework-architecture.html) — interactive, trace-enabled architecture walkthrough
- [`docs/PRINCIPLES.md`](docs/PRINCIPLES.md) — non-negotiable design principles
- [`docs/MATH.md`](docs/MATH.md) — ECAC, break-even and routing math
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — full system architecture
- [`docs/EXISTING_PROJECT.md`](docs/EXISTING_PROJECT.md) — mature repository integration
- [`docs/NEW_PROJECT.md`](docs/NEW_PROJECT.md) — greenfield setup
- [`docs/AGENT_ADOPTION.md`](docs/AGENT_ADOPTION.md) — point another coding agent at AVF
- [`docs/CODEX.md`](docs/CODEX.md) — current Codex adapter details
- [`docs/CONTEXT_COMPACTION.md`](docs/CONTEXT_COMPACTION.md) — state recovery
- [`docs/SKILLS.md`](docs/SKILLS.md) — skills/plugins governance
- [`docs/EVALUATION.md`](docs/EVALUATION.md) — project-specific evals and telemetry
- [`docs/SOURCES.md`](docs/SOURCES.md) — sources and date-sensitive facts

## Status

`0.2.0` is prepared as an unreleased capacity-aware update: generic capacity states, route feasibility, fallback safety, opportunity-cost economics, transition guidance and a Codex/Luna Reserve adapter note are present. Provider adapters still require validation against the installed runtime before activation.

## License

MIT.
