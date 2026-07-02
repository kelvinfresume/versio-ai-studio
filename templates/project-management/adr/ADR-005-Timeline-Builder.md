# ADR-005 — Timeline Builder Service

Status: Accepted

## Context

Storyboard scenes need timing before they can be animated or assembled into video.

## Decision

Create a Timeline Builder service that converts storyboard scenes into timed scene entries.

## Consequences

Animation, beat sync, video workers, and export services can use a shared timeline contract.
