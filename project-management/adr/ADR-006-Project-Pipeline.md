# ADR-006 — Project Pipeline Orchestrator

Status: Accepted

## Context

Versio now has multiple backend stages: AI Director, Timeline Builder, image generation, and future Character Memory, Prompt Builder, workers, and exports.

Keeping orchestration inside `main.py` would make the backend harder to maintain.

## Decision

Create a Project Pipeline Orchestrator under:

```text
backend/fastapi-api/app/orchestrator/
