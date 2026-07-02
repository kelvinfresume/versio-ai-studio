# Technical Debt

## Active Debt

### TD-001 — main.py is too large
Priority: High

Current backend logic is concentrated in main.py. Refactor into routers, services, models, schemas, and database modules.

### TD-002 — Vault startup failure is too hard
Priority: High

Backend fails hard if Vault is sealed or token is invalid. Add clearer diagnostics and startup checks.

### TD-003 — Timeline is not persisted
Priority: Medium

Timeline is generated dynamically. Add timeline table later.

### TD-004 — Image prompts lack character continuity
Priority: High

Character Memory and Prompt Builder 2.0 needed.

### TD-005 — No automated smoke test
Priority: Medium

Add one-command local diagnostics script.
