# Changelog

## 0.2.0 - Unreleased

### Added

- Provider-neutral capacity and entitlement states, tri-state route feasibility and fallback safety.
- Capacity opportunity-cost input and a manual capacity snapshot CLI command.
- Quota-transition checkpointing, reclassification and Codex/Luna Reserve guidance.
- Capacity-aware architecture documentation and deterministic tests.
- Trace-enabled interactive architecture walkthrough with four guided views.

### Changed

- ECAC optionally includes project-supplied scarcity cost; the default remains the v0.1 result.
- Routing checks feasibility before economic comparison and distinguishes intended from effective runtime routes.

### Preserved

- Provider-neutral core, hard quality floor, repository authority and dependency-free runtime.

### Not included

- Automatic Reserve detection, quota scraping, telemetry service, scheduler, deployment or release publication.

## 0.1.0 - 2026-09-05

- Initial open-source architecture.
- ECAC and break-even economics.
- Dependency-free repository audit/doctor CLI.
- Risk scoring scaffold.
- Codex adapter documentation and templates.
- Context compaction recovery pattern.
- Repo-local explicit AVF task skill.
- OpenAI/Codex money-first dated reference profile.
