# Software_Factory v0.1.0 — GUI-FIRST ZERO-BUDGET EDITION

## Start here

This release is designed for an absolute beginner who wants the **browser to be the normal operating front end**.

### Normal operation

1. Open the GitHub Codespace.
2. Open the forwarded **Software_Factory GUI** port `8787`.
3. Follow the numbered sections on the GUI page from top to bottom.

The `.devcontainer/devcontainer.json` starts the GUI automatically and requests port 8787.

### Only when automatic startup does not happen

In the Codespace terminal run exactly:

```bash
python3 -m factory web --workspace workspaces/demo-import --host 0.0.0.0 --port 8787
```

**Do not add `.cli`.** The canonical module is `factory`.

## What this v0.1.0 is

This is not intended to be a basic “write some source code” demonstrator.

It is a GUI-first autonomous engineering factory foundation covering:

- existing shipped-solution ZIP ingestion;
- continuation and integration of existing software;
- repository/workspace lifecycle operations;
- file CRUD;
- engineering discovery;
- requirements and capability graphs;
- architecture generation;
- scaffold generation;
- deterministic verification;
- evidence and provenance;
- frontier acceptance benchmarking;
- browser-based frontier-LLM co-work handoff;
- returned artifact ZIP integration;
- provider-neutral architectural direction;
- zero-budget/bootstrap safeguards;
- checkpointing and export.

## Four supplied architecture targets

- MOW application platform;
- NG opportunity-intelligence platform;
- distributed provider-neutral platform;
- AMPA-AI digital/software/cyber-physical architecture.

## GUI-first philosophy

After bootstrap, routine actions belong in the GUI. The CLI remains available for startup, bootstrap recovery, diagnostics and advanced automation only.

## Quality principle

No generated result is called “state of the art” merely because a model says it is. The factory's Frontier Acceptance Framework and SFCB benchmark require evidence across functional correctness, architecture, non-functional quality, security, resilience, portability, autonomy of engineering, and traceability.

## Detailed guides

Start with:

- `docs/BEGINNER-STEP-BY-STEP-SETUP.md`
- `docs/GUI-FIRST-OPERATING-GUIDE.md`
- `docs/ROUTINE-OPERATIONS-GUI-CROSSWALK.md`

Then consult:

- `docs/FRONTIER-ACCEPTANCE-FRAMEWORK.md`
- `docs/SFCB-SOFTWARE-FACTORY-CONSTRUCTION-BENCHMARK.md`
- `docs/FRONTIER-BROWSER-COWORK.md`
- `docs/ZIP-INGESTION-AND-CONTINUATION.md`
- `docs/CRUD-AND-REPOSITORY-OPERATIONS.md`

## Browser frontier LLM boundary

The Frontier Browser Co-Work capability is deliberately designed around normal browser use: prepare prompt/context in Software_Factory → use the provider's normal web interface → download resulting artifacts → integrate the downloaded ZIP in Software_Factory.

It does not scrape, impersonate or bypass a third-party consumer web interface.
