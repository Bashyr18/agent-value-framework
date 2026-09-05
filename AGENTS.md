# Agent Value Framework contributor instructions

Preserve AVF's separation between provider-neutral economics and versioned provider adapters.

Do not convert benchmark scores into project acceptance probabilities.

Do not make installation destructive. Existing repositories are authoritative; template/example files must never imply blind overwrite.

Keep runtime dependencies at zero unless a new dependency has a compelling deterministic benefit.

When changing provider-specific facts, update the snapshot date and `docs/SOURCES.md`.

Run the unit tests and Python compile checks before declaring code changes complete.
