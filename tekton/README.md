# Versio AI Studio - Tekton

Tekton is optional in dev and will be used for Kubernetes-native CI/CD.

## Purpose

- Build backend containers
- Build AI worker containers
- Run tests inside Kubernetes
- Push images to registry
- Update GitOps manifests
- Let ArgoCD deploy changes

## Dev Rule

For local Docker dev, use:

docker compose up --build

For Kubernetes dev, use Tekton after a local Kind/Minikube cluster is ready.
