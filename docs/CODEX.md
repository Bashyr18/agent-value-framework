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

The AVF task skill uses this setting.

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

## Adapter rule

Never copy `templates/codex/.codex/config.toml.example` into an existing project without merging it against the installed Codex schema and the repository's current `.codex` settings.
