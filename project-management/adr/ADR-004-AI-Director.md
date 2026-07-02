# ADR-004 — AI Director Service

Status: Accepted

## Context

Storyboard planning should not live directly inside main.py.

## Decision

Create a modular AI Director service responsible for cinematic story planning.

## Consequences

Future services like Character Memory, Prompt Builder, and Timeline Builder can reuse AI Director output.
