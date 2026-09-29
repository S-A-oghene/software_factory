# GUI Troubleshooting

## The GUI is not visible

Check the Codespace **Ports** panel for port `8787`.

If there is no running Software_Factory GUI, run:

```bash
python3 -m factory web --workspace workspaces/demo-import --host 0.0.0.0 --port 8787
```

Open the forwarded port from the Ports panel.

## A GUI button returns an error

Read the error block directly below that section. The GUI reports the server-side exception as JSON so you do not need to reproduce the same action with a terminal command.

## The tree is empty

An empty workspace is valid. Use Workspace → Import as new workspace or Create & switch, then refresh the tree.

## ZIP import says workspace is not empty

Use a new workspace name for a fresh import. Use **Integrate** when you intentionally want to merge an external ZIP into an existing workspace.

## A ZIP integration shows conflicts

Choose **Plan only** first. Review the conflict paths. Non-conflicting files can be applied automatically; conflicting files remain isolated under `.factory/conflicts/` for review.

## A target button appears to do nothing

Do not use `python3 -m factory.cli` to reproduce it. The GUI calls the canonical Python module directly. For CLI diagnostics use `python3 -m factory ...`.

## The browser LLM does not return a ZIP

The browser co-work workflow does not force a particular provider output format. Ask the provider to return/download the requested artifacts as a ZIP, then use the GUI's frontier artifact integration control.
