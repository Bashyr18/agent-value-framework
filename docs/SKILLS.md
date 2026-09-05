# Skills and plugin governance

## Why skills matter

A skill can change search breadth, reasoning workflow, tool use, subagent spawning, mutation scope, review behavior, and context load. Therefore skill governance is part of cost governance.

## Classification

### GREEN

Safe for implicit use when narrowly matched:

- focused repository exploration;
- targeted TDD;
- formatting/copy/accessibility checks;
- verification wrappers;
- narrow debugging.

### YELLOW

Useful but root-orchestrator controlled:

- broad code review;
- research;
- domain modeling;
- architecture mapping;
- multi-file diagnosis.

### ORANGE

Explicit/manual invocation:

- architecture redesign;
- migration;
- broad refactoring;
- issue-generation workflows that can expand scope;
- provisioning/setup;
- multi-agent alternative generation;
- memory integrations.

### RED for automatic invocation

External side-effect capabilities such as deployment, publishing, account mutation, remote settings, destructive cleanup or credential-affecting setup unless the task explicitly authorizes them and project policy permits it.

RED does not necessarily mean uninstall. It means "never silently invoke."

## Codex progressive disclosure

Codex repo-local skills can live under `.agents/skills`. Current Codex supports `allow_implicit_invocation: false` in `agents/openai.yaml`, making a skill explicit-only while still available as `$skill-name`.

AVF's own project task skill is explicit-only by design. Starting an AVF workflow should be a deliberate user/root action, not something inferred from every coding prompt.

## Instruction precedence

AVF recommends making this explicit in the target project:

```text
explicit user intent
> project architecture/invariants/acceptance rules
> routing and safety contract
> bounded task contract
> skill methodology
> model defaults
```

Platform/system safety remains above all project-controlled instructions.

## Context budget

Installed skills are not free. Hosts may initially expose only metadata, but selected skills load their full instructions and can spawn additional work.

Avoid simultaneously invoking multiple broad behavioral skills. A long context with contradictory architecture, minimalism, TDD, review and provisioning philosophies can reduce effective intelligence even when the underlying model has not changed.
