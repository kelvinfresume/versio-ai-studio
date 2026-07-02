# ADR-002 — Docker Compose Development Platform

Status: Accepted

## Context

Versio requires multiple local services: FastAPI, Next.js, PostgreSQL, MinIO, Redis, Vault, Jenkins, pgAdmin, and RedisInsight.

## Decision

Use Docker Compose as the local development runtime.

## Consequences

Developers can run the full platform locally with one command.
