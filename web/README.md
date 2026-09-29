# Software_Factory Browser GUI

The browser UI is the normal operational front end for v0.1.0.

Start it automatically in Codespaces via `.devcontainer/devcontainer.json`, or manually with:

```bash
python3 -m factory web --workspace workspaces/demo-import --host 0.0.0.0 --port 8787
```

The GUI exposes routine operations that otherwise would be CLI actions. See `docs/GUI-FIRST-OPERATING-GUIDE.md` for the complete flow.

## HTTP surface

The web server provides:

- workspace status/list/create/switch;
- shipped ZIP import;
- ZIP integration and plan-only inspection;
- target discovery and specification validation;
- engineering planning;
- architecture generation;
- scaffold generation;
- file CRUD/copy/move;
- Git init/clone/status/diff;
- checkpoints;
- factory verification/self-test/report;
- benchmark recording;
- frontier browser co-work sessions and context download;
- workspace export;
- file download.

This is intentionally a standard-library-only browser application for the zero-budget baseline.
