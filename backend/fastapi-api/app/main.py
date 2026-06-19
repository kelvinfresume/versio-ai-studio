from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

class AITestRequest(BaseModel):
    project_name: str
    song_description: str
    story_prompt: str

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

@app.post("/ai/test-generation")
def test_ai_generation(request: AITestRequest):
    return {
        "project_name": request.project_name,
        "status": "mock_ai_generated",
        "input": {
            "song_description": request.song_description,
            "story_prompt": request.story_prompt
        },
        "storyboard": [
            {
                "scene": 1,
                "title": "Opening Field",
                "visual": "Wide anime shot of a green grass field with horses running through flowers.",
                "camera": "slow cinematic push-in",
                "emotion": "peaceful and hopeful"
            },
            {
                "scene": 2,
                "title": "Ancient Kingdom",
                "visual": "Ancient stone buildings glowing under supernatural golden light.",
                "camera": "aerial reveal",
                "emotion": "mystical and epic"
            },
            {
                "scene": 3,
                "title": "Conflict",
                "visual": "Two warriors clash with ancient magic and bright energy effects.",
                "camera": "fast cuts synced to beat",
                "emotion": "intense but all-ages safe"
            },
            {
                "scene": 4,
                "title": "Romantic Pause",
                "visual": "Two characters share a soft kiss as flowers float in the wind.",
                "camera": "close-up with gentle fade out",
                "emotion": "warm and emotional"
            }
        ],
        "audio_direction": {
            "fade_out": "Fade music down before romantic dialogue.",
            "dialogue_insert": "Add soft spoken line during quiet break.",
            "fade_in": "Bring music back smoothly into final scene."
        }
    }
