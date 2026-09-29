# Frontier Browser Co-Work

## Why this exists

The project needs a way to use high-quality browser-based frontier LLM experiences without forcing the entire factory to depend on small/free API endpoints.

## Supported pattern

Software_Factory prepares a structured session bundle containing:

- objective;
- specification excerpt;
- selected architecture facts;
- selected files;
- constraints;
- requested deliverables;
- acceptance criteria;
- expected artifact format.

The user opens the frontier provider in a normal browser tab, enters the prompt, attaches the requested ZIP/files using the provider's normal UI, and works with the model normally. After the provider returns a ZIP or other artifact, the user downloads it and uploads/imports it into Software_Factory.

## Explicit boundary

This package does not:

- scrape consumer chat webpages;
- inject scripts into third-party chat sessions;
- bypass authentication;
- bypass rate limits;
- bypass usage restrictions;
- pretend the consumer web UI is an unrestricted API.

## Browser workflow

```text
Software_Factory
    -> Create Frontier Session
    -> Copy prompt / export context ZIP
    -> Open browser provider
    -> Normal web-UI interaction
    -> Download returned ZIP
    -> Upload ZIP to Software_Factory
    -> Ingest / diff / integrate
    -> Validate
    -> Benchmark
```

## Provider-neutral URLs

The web UI uses configurable provider links. Users may configure the actual browser URLs available to them. No current product availability is assumed by the package.
