# Versio AI Studio

Versio AI Studio is an AI-powered anime/movie scene generation platform that turns songs, spoken words, lyrics, and story prompts into cinematic anime scenes with captions, lip-sync, beat sync, scene transitions, and fade-in/fade-out music control.

## Project Status

Current phase: **Dev Setup**

## Tech Stack

- Frontend: Next.js
- Backend: FastAPI
- AI Orchestrator: Python
- Workers: Python, FFmpeg, Whisper, future GPU video workers
- Database: PostgreSQL
- Queue: Redis
- Object Storage: MinIO for dev, S3 for cloud
- CI/CD: GitHub Actions, Jenkins, Tekton
- GitOps: ArgoCD
- Observability: Prometheus, Grafana, Loki, OpenTelemetry

## File Structure

```text
versio-ai-studio/
├── README.md
├── .gitignore
├── docker-compose.yml
├── docs/
│   ├── architecture.md
│   ├── commands.md
│   ├── cost-awareness.md
│   └── fade-transition-engine.md
├── frontend/
│   └── nextjs-app/
├── backend/
│   └── fastapi-api/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app/
│           └── main.py
├── orchestrator/
│   ├── beat_sync/
│   ├── director/
│   ├── fade_engine/
│   ├── lyric_analyzer/
│   ├── prompt_builder/
│   └── scene_planner/
├── workers/
│   ├── caption-worker/
│   ├── ffmpeg-worker/
│   ├── gpu-video-worker/
│   └── lip-sync-worker/
├── infra/
│   ├── ansible/
│   ├── scripts/
│   └── terraform/
│       ├── envs/
│       │   └── dev/
│       └── modules/
├── k8s/
│   ├── base/
│   └── overlays/
│       └── dev/
├── gitops/
│   └── argocd-apps/
│       └── README.md
├── tekton/
│   ├── README.md
│   ├── tasks/
│   │   └── backend-test-task.yaml
│   ├── pipelines/
│   │   └── dev-ci-pipeline.yaml
│   ├── pipelineruns/
│   │   └── dev-ci-run.yaml
│   └── triggers/
├── jenkins/
│   ├── Jenkinsfile.backend
│   ├── Jenkinsfile.release
│   └── Jenkinsfile.workers
└── .github/
    └── workflows/

## Branch Strategy
main
develop
feature/dev-setup
feature/frontend
feature/backend
feature/orchestrator
feature/gpu-workers
feature/infra
feature/gitops
feature/ci-cd
feature/observability
feature/video-sync
feature/fade-engine
release/v0.1.0
hotfix/*

## Naming Standard 

versio-{env}-{component}-{resource}

versio-dev-postgres
versio-dev-redis
versio-dev-minio
versio-dev-jenkins
versio-dev-backend
versio-dev-assets
versio-dev-exports

