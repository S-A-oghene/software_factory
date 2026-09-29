# Software_Factory v0.1.0 — GUI-First Operating Guide

## 1. The important UX rule

This release is intentionally **GUI-first**.

After the Software_Factory browser UI is running, use the GUI for routine operations:

- create and switch workspaces;
- import a shipped solution ZIP;
- integrate an external ZIP;
- inspect the engineering model;
- validate target specifications;
- inspect requirements and capabilities;
- generate architecture packages;
- generate scaffolds;
- perform file CRUD;
- initialize or inspect Git repositories;
- create checkpoints;
- run factory verification;
- run factory self-test;
- generate workspace evidence;
- run the frontier benchmark;
- prepare frontier LLM co-work sessions;
- download prompts/context bundles;
- integrate downloaded frontier artifacts;
- export the current workspace.

The CLI is intentionally retained only for:

1. bootstrapping the repository in GitHub;
2. starting the GUI when automatic start is unavailable;
3. diagnosing a Codespace/environment problem;
4. advanced automation that has no browser equivalent yet.

## 2. The only normal GUI-start command

If the Codespace does not open the GUI automatically, run exactly:

```bash
python3 -m factory web --workspace workspaces/demo-import --host 0.0.0.0 --port 8787
```

Do **not** write `python3 -m factory.cli ...`.

The canonical module is `factory`; `factory.cli` remains importable for compatibility but is not the normal documented invocation.

When the server starts it prints:

```text
Software_Factory browser UI: http://0.0.0.0:8787/
```

Use the forwarded port in the Codespace and open **Software_Factory GUI**.

## 3. First GUI session

Follow the numbered sections on the home page from top to bottom. The page is deliberately arranged as one continuous workflow so you should not need to jump back and forth between a terminal and browser instructions.

### Step A — Workspace

The Workspace section gives you three safe paths:

**Create & switch**

Use this to make an empty new engineering workspace.

**Import as new workspace**

Use this when you already have a shipped solution ZIP. The factory checks the ZIP, extracts it, inventories it, discovers the engineering model, writes provenance, and switches the GUI to the new workspace.

**Integrate non-conflicting files / Plan only**

Use this when you already have a current workspace and a separate ZIP that should be incorporated into it. Plan-only lets you inspect conflicts before making non-conflicting changes.

### Step B — Understand & design

Choose one of the four supplied targets:

- MOW;
- NG Opportunity Intelligence;
- Distributed Provider-Neutral Platform;
- AMPA-AI Digital Architecture.

Click **Validate specification**.

Then click **Show engineering plan**.

Then click **Generate architecture**.

Then click **Generate scaffold**.

The output stays in the GUI panel below those buttons. There is no CLI handoff.

### Step C — Files

The tree shows the current workspace. Click a file to load it into the editor.

Use:

- Create;
- Update;
- Read;
- Delete;
- Copy;
- Move.

Protected paths remain protected.

### Step D — Verification

Run:

**Run factory verification**

**Run self-test**

**Generate workspace report**

**Run frontier benchmark**

The benchmark is an acceptance/evidence gate, not a claim that a system is state of the art merely because an LLM says so.

### Step E — Frontier browser LLM

Use **Create co-work session**.

Software_Factory writes:

- a structured engineering prompt;
- a session manifest;
- a context ZIP.

Click **Open ChatGPT Web** (or another supported provider in a normal browser tab), work there normally, and download the resulting artifacts.

Return to the Software_Factory GUI and use **Integrate downloaded frontier ZIP**.

No API key is required for this browser co-work path.

This path deliberately does not scrape or impersonate a third-party consumer web interface.

### Step F — Export

Use **Download current workspace ZIP** to produce a portable artifact that can be handed to another engineer, another chat session, another Codespace, or a later Software_Factory release.

## 4. How to know what to do next

Use the numbered sections in order:

```text
Workspace
   ↓
Understand & design
   ↓
Build & evolve
   ↓
Files
   ↓
Verify & benchmark
   ↓
Frontier LLM
   ↓
Export
```

You are not expected to remember separate command syntax for each step.

## 5. Beginner test sequence

For the first test, use the included shipped solution ZIP.

1. Open **Workspace → Import as new workspace**.
2. Choose `examples/shipped_solution.zip` from the repository or download a copy and upload it.
3. Name the destination `demo-import`.
4. The GUI automatically switches to it.
5. Go to **Workspace tree / Files** and click `README.md`.
6. Confirm the content appears in the editor.
7. Click `src/app.py`.
8. Change a safe line.
9. Click **Update**.
10. Click **Git status**.
11. Create a checkpoint called `GUI CRUD test`.
12. Choose **MOW** under Design.
13. Validate.
14. Generate the engineering plan.
15. Generate the architecture package.
16. Generate the scaffold.
17. Run the benchmark.
18. Create a frontier co-work session.
19. Open the prompt and context bundle.
20. Optionally use your frontier web LLM.
21. Bring its downloaded ZIP back using **Integrate downloaded frontier ZIP**.
22. Run verification again.
23. Export the resulting workspace ZIP.

## 6. What remains CLI-only

The bootstrap process itself still uses GitHub's Actions UI and, where required, a one-time bootstrap token. Starting the Software_Factory web server may also require the single command shown above if automatic startup fails.

Those are setup/diagnostic operations, not normal application use.

## 7. If the GUI does not open

In the Codespace:

1. look at the **Ports** panel;
2. find port `8787`;
3. click the globe/open-browser control;
4. if the server is not running, run the single GUI-start command from Section 2.

If port 8787 is already in use, use the forwarded port that GitHub shows for the running server.

## 8. If a GUI operation fails

Read the red error output shown directly below the relevant section.

Do not immediately switch to a random CLI command. First retry the same GUI action once after correcting the exact input it identifies.

For advanced diagnosis, the GUI exposes the same deterministic verification path that the CLI uses.

## 9. Non-negotiable quality rule

A successful GUI operation means the operation completed.

It does **not** mean that the resulting system is frontier-quality.

Use the Verify & Benchmark section and the Frontier Acceptance Framework for evidence of system-level quality.
