# Resume Testing via GUI — Exact Procedure

This is the shortest path from the point at which CLI testing stopped.

## 1. Rebuild/use the GUI-first repository

Make sure the current GitHub repository contains the GUI-first v0.1.0 files, including `.devcontainer/devcontainer.json`.

## 2. Open/recreate the Codespace

When the Codespace loads, the devcontainer starts the Software_Factory GUI automatically and requests port `8787`.

Open the forwarded port labeled **Software_Factory GUI**.

## 3. Start with the included demo

In **Workspace**, click:

**Use included demo ZIP**

This bypasses the browser file-picker problem for the demonstration ZIP because the factory already has the ZIP in the Codespace repository.

The GUI automatically creates/switches to `demo-import`.

## 4. Confirm ingestion

The ZIP result should show:

- SHA-256;
- inventory;
- engineering model;
- discovered tests/entry points/hints.

Then go to Files and click `src/app.py`.

## 5. Test CRUD

Update `src/app.py`, click **Update**, then click **Git status**.

Create a checkpoint.

Then read/copy/move/delete a non-protected test file.

## 6. Test target workflow

Choose **MOW** and perform:

```text
Validate specification
        ↓
Show engineering plan
        ↓
Generate architecture
        ↓
Generate scaffold
```

The GUI's **Next step** banner tells you what to do next.

## 7. Test verification

Use:

- Run factory verification;
- Run self-test;
- Generate workspace report.

## 8. Test benchmark behavior

Click **Run frontier benchmark** before entering measurement values.

It should report the benchmark as **not measured**, not silently claim a frontier pass.

Then enter actual independently obtained measurements as JSON and run it again.

## 9. Test frontier browser co-work

Create a co-work session, open the prepared prompt, download the context ZIP, use the frontier web LLM normally, and then integrate the returned ZIP through the GUI.

## 10. Continue iteration

After every external integration:

```text
Integrate
  ↓
Verify
  ↓
Benchmark
  ↓
Checkpoint
  ↓
Export
```

The CLI is not part of this normal testing loop.
