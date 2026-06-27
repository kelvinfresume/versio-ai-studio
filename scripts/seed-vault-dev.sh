#!/usr/bin/env bash
set -euo pipefail

# =====================================================
# Load local environment values
# =====================================================
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

if [ -z "${VAULT_DEV_ROOT_TOKEN:-}" ]; then
  echo "ERROR: VAULT_DEV_ROOT_TOKEN is missing from .env"
  exit 1
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "ERROR: OPENAI_API_KEY is missing from .env"
  exit 1
fi

echo "Seeding persistent Vault secrets..."

docker compose exec -T vault sh <<VAULT_CMDS
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=${VAULT_DEV_ROOT_TOKEN}

vault kv put secret/versio/dev/postgres \
  username=versio \
  password=versio_dev_password \
  database=versio_dev \
  host=postgres \
  port=5432

vault kv put secret/versio/dev/minio \
  access_key=versio \
  secret_key=versio_dev_password \
  endpoint=http://minio:9000 \
  assets_bucket=versio-dev-assets \
  exports_bucket=versio-dev-exports

vault kv put secret/versio/dev/redis \
  host=redis \
  port=6379 \
  url=redis://redis:6379/0 \
  password=""

vault kv put secret/versio/dev/jenkins \
  url=http://jenkins:8080 \
  host=jenkins \
  port=8080 \
  username=versio_dev_admin \
  password=versio_dev_password

vault kv put secret/versio/dev/openai \
  api_key="${OPENAI_API_KEY}"

vault kv list secret/versio/dev
VAULT_CMDS

echo "Vault secrets seeded."
