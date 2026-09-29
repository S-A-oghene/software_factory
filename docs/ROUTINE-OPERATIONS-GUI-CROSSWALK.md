# Routine Operations — GUI Crosswalk

| Operation | GUI location | CLI fallback |
|---|---|---|
| Start factory UI | Codespace forwarded port | `python3 -m factory web ...` |
| Create workspace | Workspace → Create & switch | `python3 -m factory repo-init ...` / create workspace API |
| Switch workspace | Workspace → Existing workspace | none required |
| Import ZIP | Workspace → Import as new workspace | `python3 -m factory import-zip ...` |
| Integrate ZIP | Workspace → Integrate | `python3 -m factory integrate-zip ...` |
| Validate target | Understand & design | `python3 -m factory spec-validate ...` |
| Show plan | Understand & design | `python3 -m factory plan ...` |
| Generate architecture | Understand & design | `python3 -m factory architecture ...` |
| Generate scaffold | Understand & design | `python3 -m factory scaffold ...` |
| File CRUD | Files & repository CRUD | `python3 -m factory crud-* ...` |
| Git status/diff | Build & evolve | `python3 -m factory repo-* ...` |
| Checkpoint | Build & evolve | state API / future CLI |
| Verification | Verify & benchmark | `python3 scripts/verify_factory.py` |
| Self-test | Verify & benchmark | `python3 -m factory self-test` |
| Workspace evidence | Verify & benchmark | `python3 -m factory ...` / report module |
| Frontier session | Frontier browser LLM | `python3 -m factory frontier-session ...` |
| Frontier context | Frontier browser LLM | `python3 -m factory frontier-context-export ...` |
| Export ZIP | Export / handoff | `python3 -m factory export-zip ...` |
