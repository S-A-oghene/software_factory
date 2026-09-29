# Beginner Deployment Guide

For normal use, follow `docs/BEGINNER-STEP-BY-STEP-SETUP.md`. It is the canonical GUI-first procedure for v0.1.0.

This document remains as a compatibility entry point so earlier manuals do not strand a beginner in a CLI-heavy workflow.

The normal sequence is:

```text
GitHub bootstrap
   ↓
Codespace
   ↓
Software_Factory GUI on port 8787
   ↓
Workspace
   ↓
ZIP import / integration
   ↓
Understand & design
   ↓
Build & files
   ↓
Verify & benchmark
   ↓
Frontier browser LLM co-work
   ↓
Integrate returned artifact
   ↓
Verify again
   ↓
Export
```

The only normal CLI startup command is:

```bash
python3 -m factory web --workspace workspaces/demo-import --host 0.0.0.0 --port 8787
```
