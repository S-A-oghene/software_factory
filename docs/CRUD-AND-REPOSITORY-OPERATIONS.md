# CRUD and Repository Operations

## File CRUD

Supported in the baseline runtime:

- create file;
- read file;
- update file;
- delete file;
- copy file;
- move/rename file;
- list tree;
- search text;
- compare file contents;
- export selected files.

## Repository operations

Supported at the local workspace boundary:

- create repository;
- initialize git repository;
- clone a repository URL when the runtime has network/credentials;
- inspect repository;
- checkpoint changes;
- diff;
- branch metadata inspection;
- export workspace as ZIP.

Remote hosted-service CRUD is intentionally adapter-driven; no vendor API is hard-coded into the core.

## Safety

Deletion and replacement of protected paths require a human-authorized mode in the surrounding deployment. The baseline agent tool contract does not expose arbitrary shell execution.
