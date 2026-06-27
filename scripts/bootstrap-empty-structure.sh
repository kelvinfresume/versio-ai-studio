#!/usr/bin/env bash
set -euo pipefail

echo "Creating missing planned Versio directories only..."

mkdir -p \
  backend/fastapi-api/app/models \
  backend/fastapi-api/app/routers \
  backend/fastapi-api/app/services \
  backend/fastapi-api/app/schemas \
  backend/fastapi-api/app/utils \
  frontend/nextjs-app/components \
  frontend/nextjs-app/hooks \
  frontend/nextjs-app/lib \
  frontend/nextjs-app/services \
  frontend/nextjs-app/types \
  frontend/nextjs-app/utils \
  configs/vault \
  configs/nginx \
  configs/prometheus \
  configs/grafana \
  configs/loki \
  gitops/argocd-apps \
  gitops/projects \
  infra/ansible/inventory/dev \
  infra/ansible/inventory/staging \
  infra/ansible/inventory/prod \
  infra/ansible/playbooks \
  infra/ansible/roles/docker \
  infra/ansible/roles/kubernetes \
  infra/ansible/roles/monitoring \
  infra/ansible/roles/security \
  infra/terraform/envs/dev \
  infra/terraform/envs/staging \
  infra/terraform/envs/prod \
  infra/terraform/modules/vpc \
  infra/terraform/modules/eks \
  infra/terraform/modules/ecr \
  infra/terraform/modules/s3 \
  infra/terraform/modules/rds \
  infra/terraform/modules/iam \
  infra/terraform/modules/cloudfront \
  infra/terraform/modules/route53 \
  infra/terraform/modules/acm \
  infra/terraform/modules/redis \
  infra/terraform/modules/monitoring \
  k8s/base \
  k8s/overlays/dev \
  k8s/overlays/staging \
  k8s/overlays/prod \
  orchestrator/character_memory \
  orchestrator/timeline_builder \
  orchestrator/transition_engine \
  orchestrator/animation \
  orchestrator/export_pipeline \
  workers/whisper-worker \
  workers/beat-worker \
  workers/image-worker \
  workers/video-worker \
  workers/export-worker

create_readme_if_missing() {
  local file="$1"
  local title="$2"
  local body="$3"

  if [ ! -f "$file" ]; then
    cat > "$file" <<DOC
# $title

$body
DOC
  else
    echo "Skipping existing file: $file"
  fi
}

create_readme_if_missing "backend/fastapi-api/app/models/README.md" "Models" "SQLAlchemy database models will be split here during the backend refactor."
create_readme_if_missing "backend/fastapi-api/app/routers/README.md" "Routers" "FastAPI route modules will live here."
create_readme_if_missing "backend/fastapi-api/app/services/README.md" "Services" "Business logic services will live here."
create_readme_if_missing "backend/fastapi-api/app/schemas/README.md" "Schemas" "Pydantic request and response schemas will live here."
create_readme_if_missing "backend/fastapi-api/app/utils/README.md" "Utils" "Shared backend helper functions will live here."

create_readme_if_missing "frontend/nextjs-app/components/README.md" "Components" "Reusable React UI components will live here."
create_readme_if_missing "frontend/nextjs-app/hooks/README.md" "Hooks" "Reusable React hooks will live here."
create_readme_if_missing "frontend/nextjs-app/lib/README.md" "Lib" "Frontend shared libraries and API clients will live here."
create_readme_if_missing "frontend/nextjs-app/services/README.md" "Services" "Frontend service wrappers for API calls will live here."
create_readme_if_missing "frontend/nextjs-app/types/README.md" "Types" "Shared TypeScript types will live here."
create_readme_if_missing "frontend/nextjs-app/utils/README.md" "Utils" "Frontend helper utilities will live here."

create_readme_if_missing "configs/README.md" "Configs" "Configuration for Vault, NGINX, Prometheus, Grafana, and Loki will live here."
create_readme_if_missing "gitops/README.md" "GitOps" "ArgoCD applications and project definitions will live here."
create_readme_if_missing "gitops/argocd-apps/README.md" "ArgoCD Apps" "Application manifests for ArgoCD will live here."
create_readme_if_missing "gitops/projects/README.md" "ArgoCD Projects" "ArgoCD project definitions will live here."
create_readme_if_missing "infra/ansible/README.md" "Ansible" "Ansible inventories, playbooks, and roles will live here."
create_readme_if_missing "infra/terraform/README.md" "Terraform" "Terraform environments and reusable modules will live here."
create_readme_if_missing "k8s/README.md" "Kubernetes" "Kubernetes manifests and overlays will live here."
create_readme_if_missing "orchestrator/README.md" "Orchestrator" "AI orchestration modules will live here."
create_readme_if_missing "workers/README.md" "Workers" "Background workers will live here."

echo "Done. No existing files were replaced."
