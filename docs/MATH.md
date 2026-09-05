# The economics of coding-agent orchestration

## 1. Objective

Let a task `t` be executed under routing policy `π`. A policy may include planning, workers, tools, tests, review, retries and escalation.

AVF's primary objective is:

```text
minimize  E[C_total(t, π)] / P(Accepted(t, π))
subject to Q(t, π) >= Q_min(t)
```

For real telemetry, the preferred estimator is simpler:

```text
Empirical ECAC = total direct agent/tool spend / number of accepted changes
```

This is **Expected Cost per Accepted Change (ECAC)**.

`Q_min` is project-defined and can include functional correctness, tests, security, accessibility, compliance, review, domain approval, or release evidence. AVF never trades below this floor.

## 2. Cost decomposition

The front-page formula groups the implementation fields as follows:

- `C_base` — `base_cost`, including planned model work and workers for one attempt;
- `C_verify` — `verification_cost` for deterministic checks;
- `C_tools` — expected tool cost;
- `C_review` — expected reviewer cost;
- `C_escalation` — expected stronger-model or rescue cost;
- `C_rework` — expected retry and fix cost;
- `C_capacity` — `capacity_opportunity_cost`, a project-supplied scarcity term that may be zero.

For one attempt:

```text
C_attempt = C_plan
          + Σ C_worker_i
          + C_tools
          + C_verify
          + C_review
          + C_escalation
          + C_rework
          + C_capacity_opportunity
```

Token spend is only one component:

```text
C_model = Tin * Pin + Tcached * Pcached + Tout * Pout + tool fees
```

where token prices are expressed per token (or normalize to per million tokens).

## 3. Stationary retry approximation

If each attempt has expected cost `C` and independent probability `p` of acceptance, expected attempts until acceptance are `1/p`:

```text
ECAC ≈ C / p
```

This approximation is useful for planning but should be replaced by empirical workflow telemetry because real retries are not identical: later attempts have different context, models and failure modes.

## 4. Sequential escalation

A typical AVF route is conditional:

```text
orchestrator plan
→ cheap worker
→ deterministic gate
→ optional reviewer
→ rescue model only on failure
→ premium adviser only on unresolved high-leverage uncertainty
```

Expected direct cost is therefore:

```text
E[C] = Croot
     + Cworker
     + Cverify
     + P(review) * Creview
     + P(rescue) * Crescue
     + P(premium) * Cpremium
     + E[rework]
```

This is why "Astra costs $X" or "Luna costs $Y" is not enough. The important quantities are how frequently each conditional branch executes and how many failures it prevents.

## 5. Capacity opportunity cost

v0.2 adds an optional, project-supplied scarcity term:

```text
C_capacity_opportunity = Σ(λ_k × u_k)
```

`λ_k` is the project or user's shadow price for one unit of scarce pool `k`; `u_k` is expected consumption. It may be zero. AVF does not invent a provider or Reserve dollar value.

The implementation keeps the v0.1 additive cost model:

```text
C_attempt_v0.2 = C_attempt_v0.1 + C_capacity_opportunity
ECAC_capacity = C_attempt_v0.2 / P(Accepted)
```

This is an economic planning term, not a claim that benchmark scores are acceptance probabilities. When capacity data is unknown, record it as unknown and avoid fabricated units.

## 6. Upgrade break-even

Suppose route `c` is cheap and route `p` is premium.

- direct costs: `Cc`, `Cp`
- downstream failure probabilities: `fc`, `fp`
- average monetary loss of a failure: `L`

The premium route is economically justified when:

```text
Cp + fp * L <= Cc + fc * L
```

Rearranging:

```text
L >= (Cp - Cc) / (fc - fp)
```

This equation explains why premium reasoning belongs at high-blast-radius decisions. A $4 architecture consultation can be rational if it materially reduces the chance of an expensive multi-worker rework cascade.

AVF exposes this as:

```bash
avf break-even --cheap-cost ... --premium-cost ... --cheap-fail ... --premium-fail ...
```

## 7. Decomposition as economic compression

Let `D(t)` represent task difficulty and `I(m)` the effective capability of a model under a given effort level. A worker fails more often as the gap `D-I` grows.

An orchestrator changes the economics by converting a difficult task `t` into bounded subproblems `t1...tn`:

```text
D(t_i | architecture, invariants, ownership, tests) << D(t)
```

The worker does not need to equal the orchestrator's intelligence because it is no longer solving the same problem.

This is the core reason cheap-worker architectures can preserve quality.

## 8. Risk-adjusted routing

AVF provides an illustrative risk score based on normalized signals:

```text
R = Σ w_i * x_i / Σ w_i
```

Default signals:

- ambiguity;
- blast radius;
- coupling;
- domain criticality;
- irreversibility;
- weak deterministic verifiability.

The default weights are **policy defaults, not scientific constants**. Tune them using incident data and accepted-change telemetry.

Hard project rules should override numeric scoring. Example: "schema migrations are always RED" is better than hoping a weighted score captures it.

## 9. Deterministic verifiability changes optimal routing

A cheap worker becomes more attractive when a fast deterministic check catches its common failure modes.

If a task is:

- reversible;
- low blast radius;
- tightly scoped;
- covered by a focused test;

then a cheap worker plus a deterministic gate can dominate a stronger worker economically.

Conversely, if correctness is difficult to observe (security boundary, distributed concurrency, subtle public contract), model review or stronger reasoning becomes more valuable.

## 10. Why benchmark scores are not acceptance probabilities

A coding benchmark score is measured on a particular harness and task distribution. It is not `P(accept)` for your repository.

Never calculate:

```text
ECAC = benchmark_cost / (benchmark_index / 100)
```

unless the benchmark metric is explicitly a calibrated probability for the same acceptance event—which generic coding indexes are not.

Use benchmark results only as **priors for initial routing**. Then collect your own:

- direct spend;
- pass/fail of deterministic gates;
- retry count;
- reviewer findings;
- escalation rate;
- accepted/rejected changes;
- revert/incident rate.

## 11. Practical telemetry table

For each task record:

```text
task_id
risk_band
root_model
worker_model
worker_effort
skill_set
model_cost
hosted_tool_cost
verification_cost
review_cost
escalation_cost
retries
accepted
post_merge_revert_or_incident
```

Then compute ECAC by task class, risk band, model route and project area.

The best route is the cheapest route that remains above the quality floor **for that class of work**.
