from fastapi import FastAPI

app = FastAPI(
    title="Versio AI Studio API",
    version="0.1.0-dev"
)

@app.get("/")
def root():
    return {
        "service": "versio-ai-studio-backend",
        "env": "dev",
        "status": "running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/projects")
def create_project(name: str):
    return {
        "message": "Project created",
        "project_name": name,
        "version": "v0.1.0-dev"
    }
