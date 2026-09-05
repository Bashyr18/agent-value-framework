# Agent value workflow

## Objective

Minimize expected direct spend per accepted production-quality change. Quality and project safety requirements are constraints.

## Default flow

```text
root understands task → classify risk → check entitlement/capacity/capabilities
→ bounded worker → deterministic gates → conditional review/rescue only when justified
→ root integrates
```

## Durable state

Conversation history is not authoritative. For substantial work, keep a compact task-state record in the project's existing issue/evidence system or the locally agreed AVF state location.

## Worker contract

Workers receive objective, ownership, interfaces, decisions, invariants, acceptance criteria, required validation and escalation conditions. Workers do not silently redesign architecture or cross a project-defined high-risk boundary.

If regular capacity is constrained, checkpoint first. Safe bounded work may continue; conditional work requires reclassification and a complete contract; prohibited high-risk work pauses. An effective model mismatch is evidence to reconcile, not proof of a particular provider fallback.

## Skills

Skills supply methodology. They do not override explicit user intent, project architecture, acceptance criteria, safety rules, routing, or external authority.
