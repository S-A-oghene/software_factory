# Software_Factory v0.1.0 — Absolute-Beginner Step-by-Step Setup

This is the **one path to follow** when you are new to Software_Factory.

The design goal is simple:

> **After the GUI opens, do almost everything from the GUI.**

You should not have to alternate between a long CLI manual and a browser screen just to perform ordinary Software_Factory work.

## Part 1 — One-time GitHub bootstrap

Use the bootstrap instructions packaged under `BOOTSTRAP_UPLOAD/` and the GitHub Actions workflow.

If the bootstrap workflow needs permission to push `.github/workflows/`, create the one-time least-privilege bootstrap token documented in `GITHUB-BOOTSTRAP-PERMISSION-FIX.md` and store it as `BOOTSTRAP_TOKEN`.

Once bootstrap succeeds, create/open a GitHub Codespace.

## Part 2 — Automatic GUI startup

This release's `.devcontainer/devcontainer.json` requests port `8787` and starts the Software_Factory GUI automatically.

When the Codespace opens, look for the forwarded **Software_Factory GUI** port and open it.

You normally do not need to type a command.

### Backup/startup command

If automatic startup did not happen, use exactly one command in the Codespace terminal:

```bash
python3 -m factory web --workspace workspaces/demo-import --host 0.0.0.0 --port 8787
```

Never add `.cli` to that command.

## Part 3 — Your first GUI screen

You will see:

1. Start;
2. Workspace;
3. Understand & design;
4. Build & evolve;
5. Files & repository CRUD;
6. Verify, benchmark & evidence;
7. Frontier browser-LLM co-work;
8. Export / handoff;
9. Help.

Follow them top-to-bottom for your first demonstration.

## Part 4 — Import the supplied shipped solution

Go to **Workspace**.

Click **Use included demo ZIP**. This is the fastest path because the ZIP already lives in the Codespace; no browser file picker is needed.

For the supplied example, the ZIP is:

```text
examples/shipped_solution.zip
```

Name the new workspace:

```text
Demo Import
```

The GUI performs:

```text
ZIP safety check
    ↓
extraction
    ↓
file inventory
    ↓
engineering discovery
    ↓
engineering-model.json
    ↓
import-manifest.json
    ↓
provenance event
    ↓
switch GUI to imported workspace
```

You do not need to type a separate CLI command for any of these steps.

## Part 5 — Inspect the imported project

Stay on the same GUI page and scroll to **Files & repository CRUD**.

Click `README.md` in the tree.

The content appears in the editor.

Click `src/app.py`.

The content appears in the editor.

This is the point at which you know the ZIP has really become a Software_Factory workspace.

## Part 6 — Make a harmless change

With `src/app.py` selected, make a small text change.

Click **Update**.

Click **Git status**.

You should see the changed file in the repository status output.

Create a checkpoint named:

```text
First GUI CRUD change
```

## Part 7 — Validate a target

Go to **Understand & design**.

Choose `Marketing Operations Workbench (MOW)`.

Click **Validate specification**.

Expected output contains:

```json
"valid": true
```

Then click **Show engineering plan**.

Then click **Generate architecture**.

Then click **Generate scaffold**.

The important point is that you never leave the GUI to perform those actions.

## Part 8 — Verify the factory

Go to **Verify, benchmark & evidence**.

Click **Run factory verification**.

Then **Run self-test**.

Then **Generate workspace report**.

Finally click **Run frontier benchmark**.

The benchmark is evidence about the generated solution and factory process. It is not a marketing claim that every generated implementation is state of the art.

## Part 9 — Use a frontier web LLM

Go to **Frontier browser-LLM co-work**.

Enter an engineering task such as:

```text
Review the current workspace and propose a provider-neutral architecture that can evolve from the present system toward a resilient distributed platform. Return complete architecture artifacts, implementation boundaries, migration steps, verification strategy, failure modes, security boundaries and evidence requirements.
```

Choose context files if appropriate.

Click **Create co-work session**.

The GUI gives you:

- the prepared prompt;
- a context ZIP download;
- the session identifier.

Click **Open ChatGPT Web** and work there normally.

When the frontier web LLM produces a solution ZIP, return to this GUI and use **Integrate downloaded frontier ZIP**.

## Part 10 — Re-verify after integration

Run:

**Git status**

**Run factory verification**

**Generate workspace report**

**Run frontier benchmark**

If conflicts appear, use the GUI to inspect the incoming artifact and current file content before deciding how to resolve them.

## Part 11 — Export

Click **Download current workspace ZIP**.

This is your portable handoff artifact.

## Part 12 — The mental model

From this point onward, think:

```text
IMPORT
  ↓
UNDERSTAND
  ↓
DESIGN
  ↓
BUILD
  ↓
VERIFY
  ↓
BENCHMARK
  ↓
FRONTIER CO-WORK
  ↓
INTEGRATE
  ↓
VERIFY AGAIN
  ↓
EXPORT
```

The GUI is the operational front end for that loop.

## Part 13 — CLI rule

The correct command form is:

```bash
python3 -m factory ...
```

Not:

```bash
python3 -m factory.cli ...
```

For normal work, use the GUI instead.
