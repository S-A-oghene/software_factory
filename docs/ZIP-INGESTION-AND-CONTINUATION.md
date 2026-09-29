# Existing ZIP Ingestion and Continuation

## Input contract

An uploaded bundle may contain an application, monorepo, service, library, infrastructure code, generated artifact set, or previous Software_Factory export.

## Ingestion stages

1. Calculate SHA-256 before extraction.
2. Validate archive member names.
3. Reject absolute paths and `..` traversal.
4. Reject unsafe symlink semantics.
5. Extract into a quarantine workspace.
6. Inventory files.
7. Identify likely languages/frameworks/configuration.
8. Detect repository metadata.
9. Discover tests and entry points.
10. Discover dependency manifests.
11. Detect secrets using redaction patterns.
12. Build a repository/architecture inventory.
13. Generate an engineering model.
14. Record an import manifest.
15. Make the workspace available for continuing engineering.

## Continuation model

The factory should preserve provenance:

```text
imported artifact
  -> original hash
  -> import event
  -> analysis
  -> task
  -> modification
  -> validation
  -> benchmark
  -> exported artifact
```

This makes an imported shipped solution a first-class predecessor rather than a loose file dump.
