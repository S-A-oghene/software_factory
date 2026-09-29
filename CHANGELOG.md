# CHANGELOG — Software_Factory v0.1.0 GUI-FIRST

## v0.1.0-gui-first

This regeneration responds to the observed beginner UX failure where the guide required constant switching between GUI and CLI.

### Major changes

- GUI is now the normal operating front end.
- Codespaces automatically requests/forwards port 8787 and starts the GUI.
- Workspace creation and switching are available in the GUI.
- Shipped ZIP import is available in the GUI.
- ZIP integration and plan-only conflict inspection are available in the GUI.
- Specification validation is available in the GUI.
- Requirements/capability/task plan inspection is available in the GUI.
- Architecture generation is available in the GUI.
- Scaffold generation is available in the GUI.
- File create/read/update/delete/copy/move operations are available in the GUI.
- Git init/clone/status/diff operations are available in the GUI.
- Checkpoints are available in the GUI.
- Factory verification, self-test, workspace evidence and benchmark are available in the GUI.
- Frontier browser co-work session creation and context export are available in the GUI.
- Downloaded frontier solution ZIP integration is available in the GUI.
- Workspace export is available in the GUI.
- Automatic GUI startup is documented and configured.
- All user-facing command examples use `python3 -m factory ...`; the `.cli` form is not used for normal operation.
- A regression test covers the CLI entrypoint and a live HTTP test covers essential GUI flows.

### Correctness fix retained

The prior silent CLI defect is fixed: `factory.cli` has a module entrypoint guard, while `factory` is the canonical interface.
