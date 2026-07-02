
# Versio AI Studio Roadmap

## Current Phase

Current sprint: Sprint 5 — Timeline Builder

Current focus:

- Build Timeline Builder v1

- Convert storyboard scenes into timed production timeline

- Prepare for Character Memory and Prompt Builder 2.0

---

## Agile Streams

### Stream 1 — Platform Foundation

Goal:

Create the local developer platform needed to run Versio as a real engineering system.

Status: Done

Completed:

- Docker Compose stack

- FastAPI backend

- Next.js frontend

- PostgreSQL

- MinIO

- Redis

- pgAdmin

- RedisInsight

- Jenkins

- Vault

- GitHub Actions

- Git branch strategy

- Documentation foundation

---

### Stream 2 — Upload and Storage

Goal:

Allow users to upload audio, persist metadata, and download original files.

Status: Done

Completed:

- MP3/WAV upload

- Project metadata table

- MinIO audio storage

- Audio download endpoint

- Upload validation

- Frontend upload flow

- Project list display

---

### Stream 3 — Storyboard Engine

Goal:

Convert project prompts into storyboard scenes that can drive image/video generation.

Status: Done

Completed:

- Mock storyboard generator

- Storyboard table

- Storyboard persistence

- Storyboard API endpoints

- Frontend storyboard display

- Modular AI Director service

Current:

- AI Director v1 connected

- AI Director mode configurable

---

### Stream 4 — Image Generation

Goal:

Generate scene images from storyboard scenes and display them in the project UI.

Status: Done

Completed:

- Scene image table

- Mock image generation

- OpenAI image generation

- MinIO image storage

- Image metadata persistence

- Image gallery UI

- Image download endpoint

---

### Stream 5 — Secrets and Security

Goal:

Centralize secrets in Vault and remove hardcoded runtime credentials from the backend.

Status: Done

Completed:

- Vault added to Docker Compose

- OpenAI key stored in Vault

- PostgreSQL credentials stored in Vault

- MinIO credentials stored in Vault

- Redis credentials stored in Vault

- Jenkins credentials stored in Vault

- Backend reads secrets from Vault

- Persistent Vault storage added

- Vault seed script added

Known hardening backlog:

- Improve graceful startup when Vault is sealed

- Add one-command Vault unseal helper

- Add Vault policy separation

- Remove root token usage later

---

### Stream 6 — Timeline Builder

Goal:

Convert storyboard scenes into a timed production timeline for video workers.

Status: In Progress

Completed:

- Timeline Builder service created

- Scene timing logic added

- Transition resolver added

- Camera motion resolver added

- Music section resolver added

In Progress:

- Timeline API endpoint

- Timeline response validation

- Timeline frontend display

Todo:

- Store timeline in PostgreSQL

- Add scene duration controls

- Add song-duration-aware timing

- Integrate beat detection later

---

### Stream 7 — Character Memory

Goal:

Maintain consistent characters across storyboards, images, and future videos.

Status: Todo

Todo:

- Create character memory service

- Define character schema

- Add character table

- Extract characters from AI Director output

- Include character descriptions in image prompts

- Display characters on project detail page

---

### Stream 8 — Prompt Builder 2.0

Goal:

Generate consistent, production-quality prompts for image and video generation.

Status: Todo

Todo:

- Create prompt builder service

- Include character memory

- Include timeline context

- Include camera motion

- Include transition style

- Include visual style

- Add negative prompt strategy

- Add prompt version tracking

---

### Stream 9 — Workers and Video Pipeline

Goal:

Move heavy processing into workers and prepare for video generation.

Status: Todo

Todo:

- Image worker

- Video worker

- FFmpeg worker

- Whisper worker

- Beat worker

- Caption worker

- Export worker

- Redis queue integration

- Worker status tracking

---

### Stream 10 — DevOps and Deployment

Goal:

Prepare Versio for cloud deployment and production-grade workflows.

Status: Todo

Todo:

- Terraform AWS modules

- ECR

- S3

- RDS

- Redis

- EKS

- IAM

- Route53

- CloudFront

- ArgoCD apps

- Kubernetes manifests

- Tekton pipeline expansion

- Jenkins release pipeline

---

### Stream 11 — Product and UX

Goal:

Turn Versio from a developer dashboard into a usable product.

Status: Todo

Todo:

- Customer-facing UI

- Developer/admin UI separation

- Authentication

- User accounts

- Project history

- Export page

- Billing/credits

- Organization workspace

- Better error messages

- Loading states

- Empty states

---

### Stream 12 — QA and Hardening

Goal:

Stabilize the system and prevent regressions.

Status: Todo

Todo:

- Backend unit tests

- Frontend component tests

- API integration tests

- Docker health check script

- Vault diagnostics script

- Smoke test script

- CI quality gates

- Security scan

- Dependency scan

- Error handling pass

- Logging cleanup

---

## Sprint Plan

### Sprint 0 — Repository and Platform Setup

Status: Done

Goal:

Create the initial repo, branching model, Docker stack, and documentation base.

Done:

- Git repo initialized

- Branch strategy created

- Docker Compose created

- Backend scaffolded

- Frontend scaffolded

- Docs folder created

---

### Sprint 1 — Upload and Persistence

Status: Done

Goal:

Build the first vertical slice of upload, storage, database, and frontend visibility.

Done:

- Upload MP3/WAV

- Store audio in MinIO

- Store metadata in PostgreSQL

- View projects in UI

- Download original audio

---

### Sprint 2 — Storyboards

Status: Done

Goal:

Generate and persist storyboard scenes for uploaded projects.

Done:

- Storyboard API

- Storyboard persistence

- Storyboard frontend display

- pgAdmin verification

---

### Sprint 3 — Scene Images

Status: Done

Goal:

Generate images from storyboard scenes and display them in the UI.

Done:

- Scene image API

- Scene image table

- MinIO image storage

- Image gallery

- Image download

---

### Sprint 4 — Vault and OpenAI

Status: Done

Goal:

Move secrets into Vault and connect OpenAI.

Done:

- Vault added

- OpenAI key stored

- Backend reads OpenAI key from Vault

- Backend reads core service secrets from Vault

- Persistent Vault storage added

---

### Sprint 5 — Timeline Builder

Status: In Progress

Goal:

Create the first timeline contract for animation, beat sync, and video assembly.

In Progress:

- Timeline Builder service

- Timeline API endpoint

- Timeline testing

Todo:

- Timeline frontend section

- Timeline persistence

- Timeline docs

---

### Sprint 6 — Character Memory

Status: Todo

Goal:

Create reusable character identity context for consistent image/video generation.

Todo:

- Character schema

- Character memory table

- Character extraction

- Character prompt injection

---

### Sprint 7 — Prompt Builder 2.0

Status: Todo

Goal:

Centralize prompt generation for images and videos.

Todo:

- Prompt builder service

- Prompt versioning

- Scene prompt templates

- Character-aware prompts

- Timeline-aware prompts

---

### Sprint 8 — Worker Pipeline

Status: Todo

Goal:

Move AI/media processing to background workers.

Todo:

- Redis queue pattern

- Worker base template

- Image worker

- Video worker

- FFmpeg worker

- Export worker

---

### Sprint 9 — Video Assembly

Status: Todo

Goal:

Create first MP4 output from scene images and audio.

Todo:

- FFmpeg composition

- Scene duration mapping

- Crossfade transitions

- Audio sync

- Export endpoint

---

### Sprint 10 — Cloud and Production

Status: Todo

Goal:

Prepare AWS deployment.

Todo:

- Terraform modules

- Kubernetes manifests

- ArgoCD apps

- CI/CD release flow

- Monitoring stack

