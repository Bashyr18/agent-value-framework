# FAQ

## Does AVF always choose the cheapest model?
No. It minimizes expected spend per accepted change under a quality floor.

## Why not run the strongest model everywhere?
Because high intelligence has highest leverage at decisions that fan out. Mechanical implementation can often be safely delegated once architecture, invariants and tests are fixed.

## Does AVF prevent context compaction?
No. It makes important state reconstructable after compaction.

## Is AVF Codex-only?
No. The core is host-neutral. Codex is the first documented adapter.

## Can I use AVF on an existing project?
Yes; that is a primary use case. Audit first and merge into existing governance.

## Does AVF replace tests?
No. Deterministic verification is central to the economics.

## Can public benchmark scores determine routing automatically?
They can seed a policy but should not be used as project acceptance probabilities. Replace them with your own telemetry.
