# v0.1.0 GUI-first Regeneration Notes — 2026-09-29

## Observed UX problems addressed

1. CLI-heavy operation was daunting for an absolute beginner.
2. The earlier guide became disjointed when it switched from GUI instructions back to CLI commands.
3. `python3 -m factory.cli ...` silently did nothing in the previously shipped module because the CLI module lacked a direct module entrypoint; the canonical `factory` entrypoint worked.
4. A browser file picker cannot select a ZIP that exists only inside the remote Codespace filesystem.
5. The earlier benchmark defaults could be mistaken for empirical frontier performance if used without measured evidence.
6. The direct full repository needed its post-bootstrap CI/security/release evidence workflows explicitly present.

## Corrections

- Browser GUI is now the normal operating front end.
- Routine operations are available through the GUI.
- Codespaces request/forward port 8787 and auto-start the GUI.
- `python3 -m factory ...` is the canonical CLI form.
- `python3 -m factory.cli ...` remains compatible but is not used for routine documentation.
- An **Use included demo ZIP** GUI action imports the supplied demo without relying on the browser file picker.
- A visible **Next step** banner keeps the beginner workflow continuous.
- The GUI can create/switch workspaces.
- The GUI supports ZIP import/integration, target validation, plans, architecture, scaffolding, CRUD, Git status/diff/init/clone, checkpoints, verification, reports, benchmark recording, frontier browser co-work, and export.
- Benchmarking without measured values is explicitly **NOT MEASURED**.
- CI, security baseline and release-evidence workflows are included in the direct repository.
- GUI HTTP behavior has a dedicated automated test.
