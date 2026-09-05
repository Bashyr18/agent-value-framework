# Codex adapter

This document tracks Codex-specific integration. It is intentionally separate from AVF's provider-neutral core because Codex configuration evolves.

Snapshot verified: **2026-09-05**.

## Project configuration precedence

Current Codex precedence is:

```text
CLI flags / --config overrides
> trusted project .codex/config.toml (closest project layer wins)
> selected profile
> user ~/.codex/config.toml
> system config
> built-in defaults
```

If a project is untrusted, Codex skips project-local `.codex` config, hooks and rules. This means account/machine portability requires a bootstrap/trust step; a Git commit cannot manufacture project trust.

## Subagent defaults

Current Codex supports:

```toml
[agents]
enabled = true
max_concurrent_threads_per_session = 2
default_subagent_model = "..."
default_subagent_reasoning_effort = "..."
```

Explicit spawn values override the defaults. Custom agent files can also specify model, reasoning effort, sandbox and skill configuration.

AVF recommends low concurrency by default for money-first workflows and read-heavy parallelism over overlapping write-heavy work.

## Repo-local skills

Codex scans repo `.agents/skills` locations and supports `agents/openai.yaml` with:

```yaml
policy:
  allow_implicit_invocation: false
```

The AVF `value` skill uses this setting.

## Hooks

Current hook common input includes the active `model` slug. This enables runtime guards to compare intended and effective routing.

Relevant lifecycle events include:

- `SessionStart` (`startup`, `resume`, `clear`, `compact`)
- `SubagentStart`
- `SubagentStop`
- `PreCompact`
- `PostCompact`
- `Stop`

Codex warns that hook/plugin context accumulates and can degrade model performance. Keep additional context small.

## Luna Reserve and constrained capacity

Luna Reserve is an OpenAI/Codex product behavior, not part of AVF's provider-neutral core. AVF maps a confirmed reserve fallback onto `CapacityMode.RESERVE`, then reclassifies remaining work without changing the quality floor.

The official OpenAI guidance verified on **2026-09-05** says Luna Reserve:

- is available only to selected personal Plus and Pro accounts, not every account;
- depends on account and supported app version and is not available in Business or Enterprise workspaces;
- provides additional GPT-5.6 Luna usage after regular usage is exhausted;
- has a separate, finite allowance, is not unlimited, and is not API credit;
- does not restore regular usage or unlock the most capable models; and
- can disappear or vary, so reaching the regular limit does not guarantee access.

These are provider facts, not routing assumptions. A model name in configuration is intended routing. If a hook exposes only the effective model, `intended_model != effective_model` is a `ROUTING_MISMATCH`; it does not prove that Reserve caused the change. AVF should treat reserve entitlement, remaining allowance, reset timing and the transition reason as runtime-supplied unless a stable documented host signal exists.

When Reserve is confirmed, checkpoint, record intended/effective routes and the known or unknown reason, then reclassify the remaining task. Safe bounded work may continue; conditional work needs a complete checkpointed contract; prohibited high-risk work pauses. When regular capacity returns, reconcile repository state before restoring normal route assumptions.

## Adapter rule

Never copy `templates/codex/.codex/config.toml.example` into an existing project without merging it against the installed Codex schema and the repository's current `.codex` settings.
