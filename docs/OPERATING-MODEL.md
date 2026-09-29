# v0.1.0 Operating Model

## Mode A — deterministic factory

No model required. Specification parsing, import, inventory, CRUD, architecture templates, evidence and tests can run offline.

## Mode B — automated remote model

Uses a supported OpenAI-compatible adapter when a model endpoint and credentials are legitimately available.

## Mode C — frontier browser co-work

No API required. User operates the frontier model in its normal web application and exchanges artifacts with Software_Factory.

## Mode D — hybrid engineering

Recommended for difficult work:

- Software_Factory performs inventory/planning/validation/benchmark;
- frontier browser LLM performs high-level reasoning, design synthesis or code generation;
- Software_Factory ingests and critiques the returned artifacts;
- multiple candidate architectures can be compared before integration.

## Why hybrid is important

No single model should become the trust anchor. The factory is the durable system of record for requirements, artifacts, evidence and validation.
