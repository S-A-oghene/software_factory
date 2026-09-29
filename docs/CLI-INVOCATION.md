# CLI Invocation Policy — Software_Factory v0.1.0

## Canonical form

Use:

```bash
python3 -m factory <command>
```

Do not document or teach routine use as:

```bash
python3 -m factory.cli <command>
```

The latter is now supported only as a compatibility entry point because earlier v0.1.0 material used it, but the GUI-first release deliberately makes the top-level `factory` module canonical.

## GUI-first policy

Routine usage should occur in the browser UI. The CLI is for:

- one-time bootstrap tasks;
- starting the web UI if automatic startup fails;
- diagnostics;
- future advanced automation not yet represented in the browser UI.

## GUI startup

```bash
python3 -m factory web --workspace workspaces/demo-import --host 0.0.0.0 --port 8787
```
