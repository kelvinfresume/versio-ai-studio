#!/usr/bin/env bash
set -euo pipefail

CREATED=0
SKIPPED=0
WARNED=0

create_from_template() {
  local template="$1"
  local target="$2"

  mkdir -p "$(dirname "$target")"

  if [ -f "$target" ]; then
    if cmp -s "$template" "$target"; then
      echo "SKIPPED identical: $target"
      SKIPPED=$((SKIPPED + 1))
    else
      echo "WARNING exists and differs, not touching: $target"
      WARNED=$((WARNED + 1))
    fi
  else
    cp "$template" "$target"
    echo "CREATED: $target"
    CREATED=$((CREATED + 1))
  fi
}

echo "==========================================="
echo "Versio Project Management Bootstrap"
echo "==========================================="

create_from_template templates/project-management/README.md project-management/README.md
create_from_template templates/project-management/architecture.md project-management/architecture.md
create_from_template templates/project-management/backlog.md project-management/backlog.md
create_from_template templates/project-management/milestones.md project-management/milestones.md
create_from_template templates/project-management/release-plan.md project-management/release-plan.md
create_from_template templates/project-management/sprint-template.md project-management/sprint-template.md
create_from_template templates/project-management/retrospective-template.md project-management/retrospective-template.md
create_from_template templates/project-management/technical-debt.md project-management/technical-debt.md
create_from_template templates/project-management/adr/README.md project-management/adr/README.md
create_from_template templates/project-management/adr/ADR-001-Repository.md project-management/adr/ADR-001-Repository.md
create_from_template templates/project-management/adr/ADR-002-Docker.md project-management/adr/ADR-002-Docker.md
create_from_template templates/project-management/adr/ADR-003-Vault.md project-management/adr/ADR-003-Vault.md
create_from_template templates/project-management/adr/ADR-004-AI-Director.md project-management/adr/ADR-004-AI-Director.md
create_from_template templates/project-management/adr/ADR-005-Timeline-Builder.md project-management/adr/ADR-005-Timeline-Builder.md
create_from_template templates/project-management/adr/ADR-006-Project-Pipeline.md project-management/adr/ADR-006-Project-Pipeline.md

echo "==========================================="
echo "Created: $CREATED"
echo "Skipped: $SKIPPED"
echo "Warnings: $WARNED"
echo "==========================================="
