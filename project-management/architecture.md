# Versio Engineering Architecture

## Current Architecture

Frontend:
- Next.js

Backend:
- FastAPI

Persistence:
- PostgreSQL

Object Storage:
- MinIO

Secrets:
- HashiCorp Vault

AI:
- OpenAI

Current pipeline:

Upload
→ Project Metadata
→ AI Director
→ Storyboard
→ Timeline Builder
→ Image Generation
→ MinIO
→ Frontend Gallery

## Target Architecture

Upload
→ AI Director
→ Project Pipeline
→ Timeline Builder
→ Character Memory
→ Prompt Builder
→ Image Worker
→ Animation Worker
→ FFmpeg Worker
→ Export Pipeline
