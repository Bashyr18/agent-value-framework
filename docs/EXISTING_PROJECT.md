# Integrating AVF into an existing project

## Rule zero

**Do not copy the templates over a mature repository.**

The repository already has an engineering operating system. AVF should become a thin routing/economics layer around it.

## Phase 1 — read-only audit

Run:

```bash
avf audit . > avf-audit.md
avf doctor .
```

The audit inventories common instruction files, Codex configuration, repository skills, CI, automation and package scripts. It intentionally does not claim to understand every project-specific rule.

Then ask the coding agent to inspect only what is needed to answer:

- What is the authoritative project instruction hierarchy?
- Are there existing `AGENTS.md`, `.codex`, skill, hook, issue-state or ADR systems?
- What commands are canonical for fast, medium and full validation?
- What areas are high-risk or human-authority-only?
- Which current files must not be overwritten?
- Which user/global behaviors will disappear on another machine/account?

## Phase 2 — integration design

The agent should propose:

```text
FILES TO EXTEND
FILES TO ADD
FILES TO LEAVE ALONE
EXISTING SYSTEMS TO REUSE
MODEL ROUTING
RISK OVERRIDES
QUALITY COMMANDS
SKILL POLICY
STATE LOCATION
ACCOUNT PORTABILITY GAPS
```

No modifications are required to produce this plan.

## Phase 3 — minimal integration

Typical mature-repo result:

```text
small AGENTS.md amendment                optional
project workflow doc                     recommended
repo-local explicit AVF task skill       recommended
.codex/config.toml merge                 Codex adapter only
narrow custom agents                     optional
small runtime/compaction hooks            optional
existing issue/state area extension      preferred over new tracker
```

Avoid introducing a new `bin/`, issue tracker, glossary, ADR system, test runner, or CI layer when the project already has one.

## Phase 4 — validation

Before accepting the framework change:

- parse all TOML/YAML/JSON;
- syntax-check hook scripts;
- run AVF doctor;
- inspect the complete diff;
- verify existing instructions were preserved;
- verify no secrets or machine-specific paths were committed;
- verify the project config actually loads in the target runtime;
- spawn a harmless read-only worker and observe the effective model where supported;
- test compaction rehydration on a disposable branch/session;
- do not bundle unrelated application changes into the framework commit.

## Dirty worktrees

If `git status` is not clean, treat every changed/untracked entry as user work. Do not `git clean`, reset, mass-stage or reorganize files to make installation easier.
