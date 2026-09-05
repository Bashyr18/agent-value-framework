# AVF principles

1. **Optimize accepted work, not token price.** The unit of economics is a production-quality accepted change.
2. **Quality is a constraint, not a soft preference.** Cost optimization operates below a project-defined quality floor.
3. **Repository truth outranks conversation memory.** Code, version control, ADRs, tests, and explicit task state are durable; chat context is disposable.
4. **Expensive intelligence belongs at fan-out decisions.** Architecture, ambiguity resolution, high blast radius, and final adjudication justify premium reasoning more than mechanical edits do.
5. **Cheap workers need bounded contracts.** Reduce required intelligence by moving architecture and ambiguity out of the worker task.
6. **Use software to verify software.** Prefer deterministic checks to probabilistic reviewers where the property can be tested directly.
7. **Escalate on evidence.** A stronger model is purchased because uncertainty, failed validation, high risk, or repeated worker failure justifies it—not because it exists.
8. **Skills are methodology.** They never outrank project invariants, security, acceptance criteria, or routing policy.
9. **Subagents have a budget.** Parallelism is valuable only when tasks are genuinely independent and the expected coordination cost is lower than the saved work/time.
10. **Configuration must survive account changes.** Durable workflow policy lives in the repository; credentials, entitlements and personal UI preferences do not.
11. **Runtime behavior is verified.** Model names in config are intent, not proof. Where the host exposes effective runtime metadata, validate it.
12. **Compaction is expected.** Design rehydration rather than hoping long conversational history remains intact.
13. **Mature repositories are authoritative.** AVF integrates with existing governance instead of installing a competing engineering system.
14. **No false certainty.** Public benchmarks are priors. Project telemetry decides long-run routing.
