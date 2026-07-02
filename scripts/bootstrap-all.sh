#!/usr/bin/env bash
set -euo pipefail

echo "Running Versio bootstrap scripts..."

if [ -x scripts/bootstrap-empty-structure.sh ]; then
  ./scripts/bootstrap-empty-structure.sh
fi

if [ -x scripts/bootstrap-project-management.sh ]; then
  ./scripts/bootstrap-project-management.sh
fi

echo "Bootstrap complete."
