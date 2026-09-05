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

## What makes a route feasible?
The route must be entitled, available, capable of the required work, allowed by project policy and above the quality floor. An unknown material fact remains unknown and is not treated as permission.

## Is Luna Reserve a new AVF model tier?
No. It is a provider-specific fallback capacity mode mapped to the generic RESERVE mode.

## Is Luna Reserve free?
Its immediate incremental cash charge is not an AVF pricing assumption. A finite included allowance can still have opportunity cost, so projects may assign it a zero or positive shadow price without inventing a Luna dollar value.

## Does an effective Luna model prove Reserve is active?
No. A model mismatch is ROUTING_MISMATCH evidence only. Reserve requires explicit runtime/account evidence.

## What happens to high-risk work when the preferred route is unavailable?
Checkpoint and reclassify. Safe bounded work may continue, conditional work needs a complete frozen contract and strong gates, and prohibited high-risk work returns PAUSE_REQUIRED. The quality floor never drops.

## What happens when regular capacity returns?
Record the restoration event, checkpoint and reconcile repository truth before restoring normal route assumptions. Valid fallback work is not discarded.
