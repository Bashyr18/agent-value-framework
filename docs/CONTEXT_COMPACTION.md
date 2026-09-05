# Context, compaction and state recovery

## Principle

Native context compaction is a transport optimization, not durable project memory.

Important state belongs in the repository.

## State capsule

Use a small task-state record. Store it in the project's existing issue/evidence system when one exists; otherwise `.avf/runtime/` is a reasonable local default and should normally be ignored by Git unless the team explicitly wants task state committed.

Recommended fields are in `templates/state/task-state.md`.

For v0.2 capacity transitions, add only the route facts needed to resume safely:

```text
EXECUTION_MODE
INTENDED_ROUTE
EFFECTIVE_ROUTE
CAPACITY_CONSTRAINTS
TRANSITION_REASON
FALLBACK_SAFETY
```

These fields record intent and observed evidence separately. Unknown capacity, entitlement, remaining allowance or transition reason stays unknown; do not infer Reserve from an effective model name.

## Rehydration protocol

After automatic/manual compaction, model switch, resumed session or fresh account:

1. read active task state;
2. read `git status`;
3. inspect current diff for owned files;
4. reload relevant project instructions/ADRs only as needed;
5. inspect last validation evidence;
6. reconcile capacity and intended/effective route mismatches;
7. reclassify remaining work before editing;
8. continue from `NEXT_CONCRETE_ACTION`.

Repository state wins over a stale capsule. Update the capsule when reconciliation changes the truth.

When regular capacity returns, checkpoint and reconcile first. Do not discard valid fallback work or change an atomic operation's route mid-flight merely because a stronger route is available again.

## Codex lifecycle support

Current Codex documentation exposes `PreCompact`, `PostCompact`, and `SessionStart` with `source=compact`. `SessionStart` additional context after compaction is delivered before the immediate continuation, including automatic mid-turn compaction.

Keep hook output short. Codex warns that context from multiple hooks/plugins adds up and can degrade model performance.

The included template hook emits only a compact rehydration instruction. It does not dump a transcript or state file into context.

## Fresh-thread threshold

A new clean thread can be economically superior to repeated compaction when:

- multiple compactions have occurred with little progress;
- the task's architecture has materially changed;
- the thread contains many abandoned approaches;
- the model repeatedly re-discovers the same facts;
- task state is complete enough to reconstruct work cheaply.

Checkpoint, start a fresh root session, and rehydrate from repository truth.
