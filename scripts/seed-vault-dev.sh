#!/usr/bin/env bash
set -euo pipefail

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "ERROR: OPENAI_API_KEY is missing from .env"
  exit 1
fi

echo "Seeding Vault dev secrets..."

docker compose exec -T vault sh <<VAULT_CMDS
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=versio-dev-root-token

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

echo "Vault dev secrets restored."
