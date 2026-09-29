# Known Limitations

1. The browser co-work layer does not automate third-party consumer web GUIs.
2. The baseline runtime deliberately does not expose unrestricted shell commands to the LLM.
3. ZIP import handles path traversal checks but cannot prove a bundle is semantically safe to execute; imported code is treated as untrusted.
4. The frontier benchmark provides the measurement harness and scorecard; a genuine state-of-the-art claim still requires a frozen reference and actual benchmark results.
5. AMPA-AI support is for digital/software/cyber-physical architecture and simulation/control interfaces. It is not physical factory autonomy.
6. Mature infrastructure components remain provider implementations. The factory defines capability contracts instead of reimplementing every database, queue, scheduler or simulator.
7. Actual hosted-provider availability, pricing and model quality can change over time and are intentionally not hard-coded into the core architecture.
