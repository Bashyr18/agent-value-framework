# Capacity-aware routing

AVF v0.2 treats model capacity, entitlement, capabilities and finite allowance as routing inputs. Reserve is a provider-specific example of a generic fallback capacity pool; it is not an AVF model tier.

## Source-of-truth boundaries

Keep these facts separate:

- **Framework invariant:** the least expensive currently feasible route must preserve the project's quality floor.
- **Project policy:** which risk classes may use a fallback, how a shadow price is chosen, and when a checkpoint is required.
- **Runtime evidence:** effective model, observed capability, capacity state and any reset or remaining value the host actually exposes.
- **Provider behavior:** account eligibility, product surfaces and reserve semantics documented by that provider.

Configuration expresses intended routing. It does not prove entitlement, capacity, effective model or reserve activation.

## Availability and operating modes

Each capacity pool uses one of four states:

```text
AVAILABLE | EXHAUSTED | UNAVAILABLE | UNKNOWN
```

`UNKNOWN` is not a synonym for available. It prevents AVF from fabricating quota or silently treating an unverified route as feasible.

The compact operating modes are:

- `NORMAL` — intended regular capacity is available.
- `CONSTRAINED` — preferred capacity is limited or a relevant state is unknown.
- `RESERVE` — a confirmed fallback pool is being used.
- `DEGRADED` — execution continues but intended/effective route or capability assumptions differ.
- `PAUSE_REQUIRED` — no currently known route satisfies quality, risk and policy constraints.

Restoration is an event, `REGULAR_CAPACITY_RESTORED`, that returns routing to `NORMAL`; it is not a permanent operating mode.

## Feasibility before economics

For every candidate route, check entitlement, availability, required capabilities, project policy, hard risk overrides, reserve permission and the quality floor. `RouteFeasibility.feasible` is `True`, `False` or `None` when material evidence is unknown. An unknown result is not promoted to `True`, especially for high-risk work.

Price optimization runs only over the feasible set:

```text
route* = argmin ECAC_capacity(route)
         subject to quality(route) >= project_quality_floor
                    and route is feasible
```

## Fallback safety

The provider-neutral classification is:

- `FALLBACK_SAFE` — bounded, low-risk work such as exploration, documentation, focused tests or mechanical edits with strong gates.
- `FALLBACK_CONDITIONAL` — moderate or multi-file work only after a durable checkpoint, explicit objective, frozen decisions, ownership, invariants, validation and stop conditions are recorded.
- `FALLBACK_PROHIBITED` — default for authentication, authorization, security architecture, migrations, destructive or irreversible work, tenant isolation, distributed consistency, incident/release decisions, secrets and broad redesign.

Fallback capacity may implement a frozen contract. It does not inherit architectural authority when the intended route disappears.

## Transition protocol

When a confirmed transition leaves regular capacity:

1. checkpoint durable task state;
2. record intended/effective route, operating mode and known or unknown reason;
3. record objective, decisions, invariants, changed files and validation;
4. reclassify the remaining work;
5. continue narrowly for safe work, continue conditionally only when the contract is complete, otherwise return `PAUSE_REQUIRED`.

When regular capacity returns, checkpoint and reconcile repository truth before changing execution assumptions. Preserve valid fallback work.

## Capacity opportunity cost

AVF preserves v0.1 ECAC and adds an optional project-supplied term:

```text
C_capacity_opportunity = Σ(shadow_price_k × expected_use_k)
C_attempt_v0.2 = C_attempt_v0.1 + C_capacity_opportunity
ECAC_capacity = C_attempt_v0.2 / P(accepted)
```

The shadow price may be zero or positive. AVF does not assign a universal cash value to an included reserve allowance and does not infer remaining units from tokens, UI behavior or model identity.

## Manual snapshot CLI

The dependency-free CLI accepts evidence supplied by a user or adapter:

```bash
avf capacity \
  --regular exhausted \
  --reserve available \
  --intended-model gpt-5.6-sol \
  --effective-model gpt-5.6-luna
```

This reports `RESERVE` plus a routing mismatch. The mismatch alone does not prove why the effective model changed. No quota scraper, scheduler or undocumented provider endpoint is required.
