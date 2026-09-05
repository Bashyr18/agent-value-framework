from __future__ import annotations

import argparse
import json
from math import isfinite
from pathlib import Path

from .audit import audit_repository
from .capacity import AvailabilityState, CapacitySnapshot
from .config import load_models
from .doctor import doctor
from .math import AttemptEconomics, empirical_ecac, upgrade_break_even_loss
from .risk import RiskSignals, recommend_path, risk_band, risk_score


def _print_checks(checks) -> None:
    for c in checks:
        print(f"[{c.status.upper():4}] {c.name}: {c.detail}")


def _nonnegative_float(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a number") from exc
    if not isfinite(parsed) or parsed < 0:
        raise argparse.ArgumentTypeError("must be finite and non-negative")
    return parsed


def _normalized_fraction(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a number in [0, 1]") from exc
    if not isfinite(parsed) or not 0 <= parsed <= 1:
        raise argparse.ArgumentTypeError("must be in [0, 1]")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="avf", description="Agent Value Framework")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("audit", help="Read-only repository inventory")
    a.add_argument("target", nargs="?", default=".")
    a.add_argument("--format", choices=["markdown", "json"], default="markdown")

    d = sub.add_parser("doctor", help="Check AVF/Codex integration prerequisites")
    d.add_argument("target", nargs="?", default=".")

    r = sub.add_parser("risk", help="Score task risk from normalized signals")
    for name in ["ambiguity", "blast-radius", "coupling", "domain-criticality", "irreversibility", "weak-verifiability"]:
        r.add_argument(f"--{name}", type=float, default=0.0)
    r.add_argument("--no-deterministic-verification", action="store_true")

    e = sub.add_parser("ecac", help="Calculate expected cost per accepted change")
    e.add_argument("--base-cost", type=float, required=True)
    e.add_argument("--verification-cost", type=float, default=0.0)
    e.add_argument("--tool-cost", type=float, default=0.0)
    e.add_argument("--review-cost", type=float, default=0.0)
    e.add_argument("--escalation-cost", type=float, default=0.0)
    e.add_argument("--rework-cost", type=float, default=0.0)
    e.add_argument("--capacity-opportunity-cost", type=_nonnegative_float, default=0.0, help="project-supplied scarcity cost per attempt")
    e.add_argument("--accept-prob", type=float, required=True)

    c = sub.add_parser("capacity", help="Inspect a manual runtime capacity snapshot; no provider scraping")
    states = [state.value for state in AvailabilityState]
    c.add_argument("--regular", choices=states, default=AvailabilityState.UNKNOWN.value, help="regular pool state")
    c.add_argument("--reserve", choices=states, default=AvailabilityState.UNKNOWN.value, help="fallback pool state; availability is runtime-supplied")
    c.add_argument("--intended-model", help="configured route/model, if known")
    c.add_argument("--effective-model", help="observed route/model, if known")
    c.add_argument("--reset", help="observed reset timestamp/text, if known")
    c.add_argument("--remaining", type=_normalized_fraction, help="optional normalized remaining value in [0, 1]")

    ee = sub.add_parser("empirical-ecac", help="Calculate observed spend per accepted change")
    ee.add_argument("--spend", type=float, required=True)
    ee.add_argument("--accepted", type=int, required=True)

    b = sub.add_parser("break-even", help="Failure-loss threshold where a premium route becomes cheaper")
    b.add_argument("--cheap-cost", type=float, required=True)
    b.add_argument("--premium-cost", type=float, required=True)
    b.add_argument("--cheap-fail", type=float, required=True)
    b.add_argument("--premium-fail", type=float, required=True)

    tc = sub.add_parser("token-cost", help="Estimate token spend from a model profile")
    tc.add_argument("--profile", required=True)
    tc.add_argument("--model", required=True)
    tc.add_argument("--input", type=int, default=0)
    tc.add_argument("--cached-input", type=int, default=0)
    tc.add_argument("--output", type=int, default=0)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "audit":
        report = audit_repository(args.target)
        print(report.to_json() if args.format == "json" else report.to_markdown(), end="")
        return 0
    if args.cmd == "doctor":
        _print_checks(doctor(args.target))
        return 0
    if args.cmd == "risk":
        signals = RiskSignals(
            ambiguity=args.ambiguity,
            blast_radius=args.blast_radius,
            coupling=args.coupling,
            domain_criticality=args.domain_criticality,
            irreversibility=args.irreversibility,
            weak_verifiability=args.weak_verifiability,
        )
        score = risk_score(signals)
        print(json.dumps({"risk_score": round(score, 4), "band": risk_band(score), "path": recommend_path(score, not args.no_deterministic_verification)}, indent=2))
        return 0
    if args.cmd == "ecac":
        x = AttemptEconomics(
            base_cost=args.base_cost,
            verification_cost=args.verification_cost,
            expected_tool_cost=args.tool_cost,
            expected_review_cost=args.review_cost,
            expected_escalation_cost=args.escalation_cost,
            expected_rework_cost=args.rework_cost,
            capacity_opportunity_cost=args.capacity_opportunity_cost,
            accept_probability=args.accept_prob,
        )
        payload = {"expected_attempt_cost": x.expected_attempt_cost, "ecac": x.ecac}
        if x.capacity_opportunity_cost:
            payload["capacity_opportunity_cost"] = x.capacity_opportunity_cost
        print(json.dumps(payload, indent=2))
        return 0
    if args.cmd == "capacity":
        snapshot = CapacitySnapshot(
            regular=AvailabilityState(args.regular),
            reserve=AvailabilityState(args.reserve),
            intended_model=args.intended_model,
            effective_model=args.effective_model,
            reset=args.reset,
            remaining=args.remaining,
        )
        print(json.dumps(snapshot.to_dict(), indent=2, sort_keys=True))
        return 0
    if args.cmd == "empirical-ecac":
        print(f"{empirical_ecac(args.spend, args.accepted):.6f}")
        return 0
    if args.cmd == "break-even":
        print(f"{upgrade_break_even_loss(cheap_cost=args.cheap_cost, premium_cost=args.premium_cost, cheap_failure_probability=args.cheap_fail, premium_failure_probability=args.premium_fail):.6f}")
        return 0
    if args.cmd == "token-cost":
        models = load_models(Path(args.profile))
        if args.model not in models:
            raise SystemExit(f"unknown model key {args.model!r}; choose one of: {', '.join(models)}")
        model = models[args.model]
        cost = model.prices.cost(input_tokens=args.input, cached_input_tokens=args.cached_input, output_tokens=args.output)
        print(json.dumps({"model": model.model, "effort": model.effort, "estimated_usd": round(cost, 8)}, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
