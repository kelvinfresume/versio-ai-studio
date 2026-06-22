import os
import uuid
from datetime import datetime

import boto3
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


app = FastAPI(
    title="Versio AI Studio API",
    version="0.3.0-dev"
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


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://versio:versio_dev_password@postgres:5432/versio_dev"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String, primary_key=True, index=True)
    project_name = Column(String, nullable=False)
    story_prompt = Column(Text, nullable=False)
    bucket = Column(String, nullable=False)
    object_key = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    status = Column(String, nullable=False, default="uploaded")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


class AITestRequest(BaseModel):
    project_name: str
    song_description: str
    story_prompt: str


S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://minio:9000")
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID", "versio")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY", "versio_dev_password")
S3_BUCKET_ASSETS = os.getenv("S3_BUCKET_ASSETS", "versio-dev-assets")

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY
)


def ensure_bucket(bucket_name: str) -> None:
    response = s3_client.list_buckets()
    bucket_names = [bucket.get("Name") for bucket in response.get("Buckets", [])]

    if bucket_name not in bucket_names:
        s3_client.create_bucket(Bucket=bucket_name)


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
        "version": "v0.3.0-dev"
    }


@app.get("/projects")
def list_projects():
    db = SessionLocal()
    try:
        projects = db.query(Project).order_by(Project.created_at.desc()).all()
        return [
            {
                "project_id": project.project_id,
                "project_name": project.project_name,
                "story_prompt": project.story_prompt,
                "bucket": project.bucket,
                "object_key": project.object_key,
                "filename": project.filename,
                "content_type": project.content_type,
                "status": project.status,
                "created_at": project.created_at.isoformat() + "Z"
            }
            for project in projects
        ]
    finally:
        db.close()


@app.get("/projects/{project_id}")
def get_project(project_id: str):
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()

        if not project:
            return {
                "status": "not_found",
                "project_id": project_id
            }

        return {
            "project_id": project.project_id,
            "project_name": project.project_name,
            "story_prompt": project.story_prompt,
            "bucket": project.bucket,
            "object_key": project.object_key,
            "filename": project.filename,
            "content_type": project.content_type,
            "status": project.status,
            "created_at": project.created_at.isoformat() + "Z"
        }
    finally:
        db.close()


@app.post("/uploads/song")
async def upload_song(
    project_name: str = Form(...),
    story_prompt: str = Form(...),
    file: UploadFile = File(...)
):
    ensure_bucket(S3_BUCKET_ASSETS)

    project_id = str(uuid.uuid4())
    original_filename = file.filename or "uploaded_audio.bin"

    if "." in original_filename:
        file_ext = original_filename.rsplit(".", 1)[1]
    else:
        file_ext = "bin"

    object_key = "projects/{}/audio/original.{}".format(project_id, file_ext)

    s3_client.upload_fileobj(
        file.file,
        S3_BUCKET_ASSETS,
        object_key,
        ExtraArgs={
            "ContentType": file.content_type or "application/octet-stream"
        }
    )

    db = SessionLocal()
    try:
        project = Project(
            project_id=project_id,
            project_name=project_name,
            story_prompt=story_prompt,
            bucket=S3_BUCKET_ASSETS,
            object_key=object_key,
            filename=original_filename,
            content_type=file.content_type,
            status="uploaded",
            created_at=datetime.utcnow()
        )

        db.add(project)
        db.commit()
    finally:
        db.close()

    return {
        "status": "uploaded",
        "project_id": project_id,
        "project_name": project_name,
        "story_prompt": story_prompt,
        "bucket": S3_BUCKET_ASSETS,
        "object_key": object_key,
        "filename": original_filename,
        "content_type": file.content_type,
        "created_at": datetime.utcnow().isoformat() + "Z"
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
