# Versio AI Studio - Vault Dev Setup

## Overview

HashiCorp Vault is used to manage local development secrets for Versio AI Studio.

Vault serves as the centralized secrets manager for:

* PostgreSQL credentials
* MinIO credentials
* Redis configuration
* Jenkins credentials
* Future AI provider API keys
* Future AWS credentials

⸻

Vault UI

URL:

http://localhost:8200

Authentication Method:

Token

Development Root Token:

versio-dev-root-token

⸻

Docker Service

Vault runs as a local Docker Compose service.

Verify Vault is running:

docker compose ps vault

View Vault logs:

docker compose logs vault

⸻

Development Warning

This configuration uses Vault Dev Mode.

Do NOT use the following in production:

VAULT_DEV_ROOT_TOKEN_ID
Vault Dev Mode
Hardcoded Tokens

Production deployments should use:

* Auto-unseal
* Proper authentication methods
* TLS certificates
* Secret rotation
* Least-privilege policies

⸻

Stored Development Secrets

Current Vault paths:

secret/versio/dev/postgres
secret/versio/dev/minio
secret/versio/dev/redis
secret/versio/dev/jenkins

⸻

PostgreSQL Secret

Vault Path:

secret/versio/dev/postgres

Stored Values:

username=versio
password=<stored in Vault>
database=versio_dev
host=postgres
port=5432

⸻

MinIO Secret

Vault Path:

secret/versio/dev/minio

Stored Values:

access_key=versio
secret_key=<stored in Vault>
endpoint=http://minio:9000
assets_bucket=versio-dev-assets
exports_bucket=versio-dev-exports

⸻

Redis Secret

Vault Path:

secret/versio/dev/redis

Stored Values:

host=redis
port=6379
url=redis://redis:6379/0
password=<stored in Vault or empty>

⸻

Jenkins Secret

Vault Path:

secret/versio/dev/jenkins

Stored Values:

url=http://jenkins:8080
host=jenkins
port=8080
username=versio_dev_admin
password=<stored in Vault>

⸻

Accessing Vault

Enter Vault container:

docker compose exec vault sh

Configure environment variables:

export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=versio-dev-root-token

⸻

Read Secrets

Read PostgreSQL secret:

vault kv get secret/versio/dev/postgres

Read MinIO secret:

vault kv get secret/versio/dev/minio

Read Redis secret:

vault kv get secret/versio/dev/redis

Read Jenkins secret:

vault kv get secret/versio/dev/jenkins

⸻

Future Enhancements

Planned Vault integrations:

* FastAPI secret retrieval
* Dynamic PostgreSQL credentials
* Dynamic AWS credentials
* Jenkins Vault Plugin integration
* Kubernetes Vault Agent Injector
* OIDC Authentication
* Secret rotation workflows

⸻

Architecture

Applications
     │
     ▼
HashiCorp Vault
     │
     ├── PostgreSQL Secrets
     ├── MinIO Secrets
     ├── Redis Secrets
     ├── Jenkins Secrets
     └── Future AI/API Secrets

Vault acts as the centralized source of truth for application secrets throughout the Versio AI Studio platform.