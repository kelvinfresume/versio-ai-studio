from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Versio AI Studio API",
    version="0.1.0-dev"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
