# Contributing

Contributions are welcome.

## Design bar

A change should improve at least one of:

- cost measurement;
- routing quality;
- portability;
- deterministic verification;
- state recovery;
- provider adapters;
- project-specific evaluation.

Avoid provider marketing claims in the core. Date-stamp model prices and benchmark snapshots.

## Development

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -e . pytest
pytest -q
python -m compileall -q src templates/codex/.codex/hooks
```

## Provider adapters

Adapters must document:

- authoritative source URLs;
- verification date;
- configuration assumptions;
- runtime limitations;
- a safe fallback when the named model/capability is unavailable.
