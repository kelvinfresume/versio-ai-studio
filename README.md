# Versio AI Studio

## Project Overview

Versio AI Studio is an AI-powered anime/movie scene generation platform...

---

## Current Status

Current Version: v0.6.0-dev

Current Phase:
- Scene Image Generation

---

## Architecture

Frontend
↓
FastAPI
↓
PostgreSQL
↓
MinIO
↓
Redis
↓
Vault

---

## Tech Stack

...

---

## Local Tool Versions

...

---

## Current File Structure

```text
<tree output here>
```

---

## Runtime Components

| Component | Purpose |
|------------|------------|
| Next.js | Frontend |
| FastAPI | Backend |
| PostgreSQL | Metadata |
| MinIO | Object Storage |
| Redis | Cache |
| Vault | Secrets |
| Jenkins | CI/CD |
| GitHub Actions | Validation |
| pgAdmin | DB UI |
| RedisInsight | Redis UI |

---

## Local URLs

| Service | URL |
|----------|----------|
| Frontend | http://localhost:3000 |
| API Docs | http://localhost:8000/docs |
| pgAdmin | http://localhost:5050 |
| MinIO | http://localhost:9001 |
| Vault | http://localhost:8200 |
| Jenkins | http://localhost:8080 |
| RedisInsight | http://localhost:5540 |

---

## Dev Credentials

### PostgreSQL

...

### Jenkins

...

### Vault

...

---

## Naming Standard

...

---

## Branch Strategy

...

---

## Development Workflow

feature/*
↓
develop
↓
main

---

## Docker Commands

```bash
docker compose up -d --build
docker compose ps
docker compose logs backend
...
```

---

## API Endpoints

### Uploads

POST /uploads/song

### Storyboards

POST /projects/{project_id}/storyboard

GET /projects/{project_id}/storyboard

### Images

POST /projects/{project_id}/images

GET /projects/{project_id}/images

---

## Database Schema

### projects

...

### storyboards

...

### scene_images

...

---

## Storage Layout

```text
projects/
└── project_id/
    ├── audio/
    └── images/
```

---

## Vault Setup

...

---

## Jenkins Setup

...

---

## CI/CD

GitHub Actions:
- Compose validation
- Backend validation
- Frontend build

Jenkins:
- Integration tests
- Future deployments

---

## Current Features

✓ Audio Upload

✓ Audio Download

✓ Storyboard Persistence

✓ Scene Image Persistence

✓ Project Details Page

✓ MinIO Storage

✓ PostgreSQL Persistence

✓ Vault Integration

---

## Roadmap

### Next

- Frontend Image Gallery

### Future

- Real AI Image Generation
- Video Generation
- Timeline Editor
- Customer Portal
- Admin Portal

---

## Version History

### v0.6.0-dev

- Storyboards
- Scene Images
- Project Details Page

### v0.5.0-dev

- Audio Upload
- Audio Download
- PostgreSQL Persistence