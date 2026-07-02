# ADR-006 — Project Pipeline Orchestrator

Status: Proposed

## Context

main.py should not coordinate AI Director, Timeline Builder, Character Memory, Prompt Builder, workers, and exports.

## Decision

Create a Project Pipeline orchestration layer.

## Consequences

Future AI and media services plug into one pipeline instead of spreading orchestration logic across route handlers.
