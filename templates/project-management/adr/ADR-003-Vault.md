# ADR-003 — HashiCorp Vault for Secrets

Status: Accepted

## Context

Versio uses secrets for OpenAI, PostgreSQL, MinIO, Redis, and Jenkins.

## Decision

Use Vault as the local and future production secrets manager.

## Consequences

Secrets are centralized. Backend reads runtime secrets from Vault. Persistent Vault storage is required to avoid data loss.
