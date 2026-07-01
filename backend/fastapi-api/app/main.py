import base64
import json
import os
import uuid
from datetime import datetime

import boto3
import hvac
from app.services.ai_director import generate_ai_director_storyboard
from botocore.exceptions import ClientError
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text,
                        create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

# =====================================================
# FastAPI App Configuration
# =====================================================
app = FastAPI(title="Versio AI Studio API", version="0.9.0-dev")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Vault Configuration
# Vault is the source of truth for local dev secrets.
# =====================================================
VAULT_ADDR = os.getenv("VAULT_ADDR", "http://vault:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN", "")


def get_vault_client() -> hvac.Client:
    client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

    if not client.is_authenticated():
        raise RuntimeError(
            "Vault authentication failed. Check VAULT_TOKEN and Vault status."
        )

    return client


def get_vault_secret(secret_path: str, field: str) -> str:
    """
    Read a single field from Vault KV v2.
    """

    client = get_vault_client()

    secret = client.secrets.kv.v2.read_secret_version(
        path=secret_path,
        mount_point="secret",
    )

    return secret["data"]["data"][field]


def get_vault_secret_map(secret_path: str) -> dict:
    """
    Read an entire Vault KV v2 secret as a dictionary.
    """

    client = get_vault_client()

    secret = client.secrets.kv.v2.read_secret_version(
        path=secret_path,
        mount_point="secret",
    )

    return secret["data"]["data"]


# =====================================================
# Load Secrets From Vault
# =====================================================
postgres_secret = get_vault_secret_map("versio/dev/postgres")
minio_secret = get_vault_secret_map("versio/dev/minio")
redis_secret = get_vault_secret_map("versio/dev/redis")
OPENAI_API_KEY = get_vault_secret("versio/dev/openai", "api_key")

print("✓ Backend secrets loaded from Vault")


# =====================================================
# Database Configuration
# =====================================================
DATABASE_URL = (
    f"postgresql://{postgres_secret['username']}:{postgres_secret['password']}"
    f"@{postgres_secret['host']}:{postgres_secret['port']}/{postgres_secret['database']}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# =====================================================
# Object Storage Configuration
# =====================================================
S3_ENDPOINT_URL = minio_secret["endpoint"]
S3_ACCESS_KEY_ID = minio_secret["access_key"]
S3_SECRET_ACCESS_KEY = minio_secret["secret_key"]
S3_BUCKET_ASSETS = minio_secret["assets_bucket"]
S3_BUCKET_EXPORTS = minio_secret["exports_bucket"]

s3_client = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
)


# =====================================================
# Redis Configuration
# Loaded now for future worker queue usage.
# =====================================================
REDIS_URL = redis_secret["url"]


# =====================================================
# OpenAI / AI Director Configuration
# =====================================================
IMAGE_GENERATION_MODE = os.getenv("IMAGE_GENERATION_MODE", "mock")
AI_DIRECTOR_MODE = os.getenv("AI_DIRECTOR_MODE", "mock")
AI_DIRECTOR_FALLBACK_TO_MOCK = (
    os.getenv("AI_DIRECTOR_FALLBACK_TO_MOCK", "true").lower() == "true"
)

OPENAI_TEXT_MODEL = os.getenv("OPENAI_TEXT_MODEL", "gpt-5.5")
OPENAI_IMAGE_MODEL = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
OPENAI_IMAGE_SIZE = os.getenv("OPENAI_IMAGE_SIZE", "1024x1024")
OPENAI_IMAGE_QUALITY = os.getenv("OPENAI_IMAGE_QUALITY", "low")

openai_client = OpenAI(api_key=OPENAI_API_KEY)

print("✓ OpenAI key loaded from Vault")


# =====================================================
# Database Models
# =====================================================
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


class StoryboardScene(Base):
    __tablename__ = "storyboards"

    storyboard_id = Column(String, primary_key=True, index=True)
    project_id = Column(
        String, ForeignKey("projects.project_id"), nullable=False, index=True
    )
    scene_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    visual = Column(Text, nullable=False)
    camera = Column(Text, nullable=False)
    emotion = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class SceneImage(Base):
    __tablename__ = "scene_images"

    image_id = Column(String, primary_key=True, index=True)
    project_id = Column(
        String, ForeignKey("projects.project_id"), nullable=False, index=True
    )
    scene_number = Column(Integer, nullable=False)
    bucket = Column(String, nullable=False)
    object_key = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="generated")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# =====================================================
# Request Models
# =====================================================
class AITestRequest(BaseModel):
    project_name: str
    song_description: str
    story_prompt: str


# =====================================================
# Serialization Helpers
# =====================================================
def serialize_project(project: Project) -> dict:
    return {
        "project_id": project.project_id,
        "project_name": project.project_name,
        "story_prompt": project.story_prompt,
        "bucket": project.bucket,
        "object_key": project.object_key,
        "filename": project.filename,
        "content_type": project.content_type,
        "status": project.status,
        "created_at": project.created_at.isoformat() + "Z",
    }


def serialize_storyboard_scene(scene: StoryboardScene) -> dict:
    return {
        "storyboard_id": scene.storyboard_id,
        "project_id": scene.project_id,
        "scene": scene.scene_number,
        "title": scene.title,
        "visual": scene.visual,
        "camera": scene.camera,
        "emotion": scene.emotion,
        "created_at": scene.created_at.isoformat() + "Z",
    }


def serialize_scene_image(image: SceneImage) -> dict:
    return {
        "image_id": image.image_id,
        "project_id": image.project_id,
        "scene": image.scene_number,
        "bucket": image.bucket,
        "object_key": image.object_key,
        "prompt": image.prompt,
        "status": image.status,
        "created_at": image.created_at.isoformat() + "Z",
        "download_url": f"/projects/{image.project_id}/images/{image.image_id}/download",
    }


# =====================================================
# Storage Helper
# =====================================================
def ensure_bucket(bucket_name: str) -> None:
    response = s3_client.list_buckets()
    bucket_names = [bucket.get("Name") for bucket in response.get("Buckets", [])]

    if bucket_name not in bucket_names:
        s3_client.create_bucket(Bucket=bucket_name)


# =====================================================
# Mock Storyboard Generator
# Safe fallback when AI Director is disabled or fails.
# =====================================================
def mock_storyboard_scenes(
    project_name: str = "Versio Project", story_prompt: str = ""
) -> list[dict]:
    return [
        {
            "scene": 1,
            "title": "Opening Field",
            "visual": "Wide anime shot of a green grass field with horses running through flowers.",
            "camera": "slow cinematic push-in",
            "emotion": "peaceful and hopeful",
        },
        {
            "scene": 2,
            "title": "Ancient Kingdom",
            "visual": "Ancient stone buildings glowing under supernatural golden light.",
            "camera": "aerial reveal",
            "emotion": "mystical and epic",
        },
        {
            "scene": 3,
            "title": "Conflict",
            "visual": "Two warriors clash with ancient magic and bright energy effects.",
            "camera": "fast cuts synced to beat",
            "emotion": "intense but all-ages safe",
        },
        {
            "scene": 4,
            "title": "Romantic Pause",
            "visual": "Two characters share a soft emotional moment as flowers float in the wind.",
            "camera": "close-up with gentle fade out",
            "emotion": "warm and emotional",
        },
    ]


# =====================================================
# JSON Extraction Helper
# Allows AI Director to return clean JSON even if the model
# wraps the response in markdown by mistake.
# =====================================================
def parse_json_response(raw_text: str) -> dict:
    cleaned = raw_text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "", 1).strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```", "", 1).strip()

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()

    return json.loads(cleaned)


# =====================================================
# AI Director
# Delegates storyboard planning to the modular
# AI Director service.
# =====================================================
def ai_director_storyboard(project: Project) -> list[dict]:
    return generate_ai_director_storyboard(
        openai_client=openai_client,
        model=OPENAI_TEXT_MODEL,
        project_name=project.project_name,
        story_prompt=project.story_prompt,
    )


# =====================================================
# Storyboard Router
# Chooses AI Director or mock storyboard.
# =====================================================
def generate_storyboard_scenes(project: Project) -> list[dict]:
    if AI_DIRECTOR_MODE != "openai":
        return mock_storyboard_scenes(project.project_name, project.story_prompt)

    try:
        return ai_director_storyboard(project)
    except Exception as exc:
        print(f"WARNING: AI Director failed: {exc}")

        if AI_DIRECTOR_FALLBACK_TO_MOCK:
            print("WARNING: Falling back to mock storyboard scenes.")
            return mock_storyboard_scenes(project.project_name, project.story_prompt)

        raise HTTPException(
            status_code=500,
            detail=f"AI Director failed: {str(exc)}",
        )


# =====================================================
# Mock Image Fallback
# =====================================================
def placeholder_png_bytes() -> bytes:
    png_base64 = (
        "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAIAAADTED8xAAAAA3NCSVQICAjb4U/g"
        "AAABJElEQVR4nO3BMQEAAADCoPVPbQwfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAgG0B8AABJzQnCgAAAABJRU5ErkJggg=="
    )
    return base64.b64decode(png_base64)


# =====================================================
# OpenAI Image Generator
# =====================================================
def openai_image_bytes(prompt: str) -> bytes:
    try:
        response = openai_client.images.generate(
            model=OPENAI_IMAGE_MODEL,
            prompt=prompt,
            size=OPENAI_IMAGE_SIZE,
            quality=OPENAI_IMAGE_QUALITY,
            n=1,
        )

        image_base64 = response.data[0].b64_json

        if not image_base64:
            raise HTTPException(
                status_code=500,
                detail="OpenAI did not return base64 image data.",
            )

        return base64.b64decode(image_base64)

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI image generation failed: {str(exc)}",
        )


# =====================================================
# Image Generation Router
# =====================================================
def generate_image_bytes(prompt: str) -> bytes:
    if IMAGE_GENERATION_MODE == "openai":
        return openai_image_bytes(prompt)

    return placeholder_png_bytes()


# =====================================================
# Health / Root
# =====================================================
@app.get("/")
def root():
    return {
        "service": "versio-ai-studio-backend",
        "env": "dev",
        "status": "running",
        "version": "0.9.0-dev",
        "image_generation_mode": IMAGE_GENERATION_MODE,
        "ai_director_mode": AI_DIRECTOR_MODE,
        "vault": "enabled",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "image_generation_mode": IMAGE_GENERATION_MODE,
        "ai_director_mode": AI_DIRECTOR_MODE,
        "vault": "enabled",
    }


# =====================================================
# Projects
# =====================================================
@app.get("/projects")
def list_projects():
    db = SessionLocal()
    try:
        projects = db.query(Project).order_by(Project.created_at.desc()).all()
        return [serialize_project(project) for project in projects]
    finally:
        db.close()


@app.get("/projects/{project_id}")
def get_project(project_id: str):
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        return serialize_project(project)
    finally:
        db.close()


# =====================================================
# Audio Download
# =====================================================
@app.get("/projects/{project_id}/download")
def download_project_audio(project_id: str):
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        try:
            response = s3_client.get_object(
                Bucket=project.bucket,
                Key=project.object_key,
            )
        except ClientError:
            raise HTTPException(
                status_code=404, detail="Audio file not found in object storage"
            )

        return StreamingResponse(
            response["Body"],
            media_type=project.content_type or "application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{project.filename}"'
            },
        )
    finally:
        db.close()


# =====================================================
# Upload Song
# =====================================================
@app.post("/uploads/song")
async def upload_song(
    project_name: str = Form(...),
    story_prompt: str = Form(...),
    file: UploadFile = File(...),
):
    ensure_bucket(S3_BUCKET_ASSETS)

    project_id = str(uuid.uuid4())
    original_filename = file.filename or "uploaded_audio.bin"
    lower_filename = original_filename.lower()

    if not lower_filename.endswith(".mp3") and not lower_filename.endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="Only MP3 and WAV uploads are supported right now.",
        )

    file_ext = (
        original_filename.rsplit(".", 1)[1] if "." in original_filename else "bin"
    )
    object_key = f"projects/{project_id}/audio/original.{file_ext}"

    s3_client.upload_fileobj(
        file.file,
        S3_BUCKET_ASSETS,
        object_key,
        ExtraArgs={"ContentType": file.content_type or "application/octet-stream"},
    )

    created_at = datetime.utcnow()

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
            created_at=created_at,
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
        "created_at": created_at.isoformat() + "Z",
        "download_url": f"/projects/{project_id}/download",
    }


# =====================================================
# Storyboard Generation
# Uses AI Director when enabled.
# =====================================================
@app.post("/projects/{project_id}/storyboard")
def generate_and_save_storyboard(project_id: str):
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        existing = (
            db.query(StoryboardScene)
            .filter(StoryboardScene.project_id == project_id)
            .order_by(StoryboardScene.scene_number.asc())
            .all()
        )

        if existing:
            return {
                "project_id": project_id,
                "project_name": project.project_name,
                "status": "already_exists",
                "storyboard": [serialize_storyboard_scene(scene) for scene in existing],
            }

        saved_scenes = []

        for item in generate_storyboard_scenes(project):
            scene = StoryboardScene(
                storyboard_id=str(uuid.uuid4()),
                project_id=project_id,
                scene_number=item["scene"],
                title=item["title"],
                visual=item["visual"],
                camera=item["camera"],
                emotion=item["emotion"],
                created_at=datetime.utcnow(),
            )
            db.add(scene)
            saved_scenes.append(scene)

        project.status = "storyboard_generated"
        db.commit()

        return {
            "project_id": project_id,
            "project_name": project.project_name,
            "status": "storyboard_generated",
            "ai_director_mode": AI_DIRECTOR_MODE,
            "storyboard": [serialize_storyboard_scene(scene) for scene in saved_scenes],
            "audio_direction": {
                "fade_out": "Fade music down before important story dialogue.",
                "dialogue_insert": "Insert short spoken narration during the quiet break.",
                "fade_in": "Bring music back smoothly into the next cinematic scene.",
            },
        }
    finally:
        db.close()


@app.get("/projects/{project_id}/storyboard")
def get_project_storyboard(project_id: str):
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        scenes = (
            db.query(StoryboardScene)
            .filter(StoryboardScene.project_id == project_id)
            .order_by(StoryboardScene.scene_number.asc())
            .all()
        )

        return {
            "project_id": project_id,
            "project_name": project.project_name,
            "status": "found" if scenes else "empty",
            "storyboard": [serialize_storyboard_scene(scene) for scene in scenes],
        }
    finally:
        db.close()


# =====================================================
# Scene Image Generation
# =====================================================
@app.post("/projects/{project_id}/images")
def generate_scene_images(project_id: str):
    ensure_bucket(S3_BUCKET_ASSETS)

    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        existing = (
            db.query(SceneImage)
            .filter(SceneImage.project_id == project_id)
            .order_by(SceneImage.scene_number.asc())
            .all()
        )

        if existing:
            return {
                "project_id": project_id,
                "project_name": project.project_name,
                "status": "already_exists",
                "images": [serialize_scene_image(image) for image in existing],
            }

        scenes = (
            db.query(StoryboardScene)
            .filter(StoryboardScene.project_id == project_id)
            .order_by(StoryboardScene.scene_number.asc())
            .all()
        )

        if not scenes:
            raise HTTPException(
                status_code=400,
                detail="Generate storyboard before generating images.",
            )

        saved_images = []

        for scene in scenes:
            image_id = str(uuid.uuid4())
            object_key = f"projects/{project_id}/images/scene-{scene.scene_number}.png"

            prompt = (
                "Cinematic anime production still. "
                f"Scene title: {scene.title}. "
                f"Visual direction: {scene.visual}. "
                f"Camera direction: {scene.camera}. "
                f"Emotional tone: {scene.emotion}. "
                "High detail, vibrant lighting, dramatic composition, "
                "clean anime style, no text, no watermark."
            )

            image_bytes = generate_image_bytes(prompt)

            s3_client.put_object(
                Bucket=S3_BUCKET_ASSETS,
                Key=object_key,
                Body=image_bytes,
                ContentType="image/png",
            )

            image = SceneImage(
                image_id=image_id,
                project_id=project_id,
                scene_number=scene.scene_number,
                bucket=S3_BUCKET_ASSETS,
                object_key=object_key,
                prompt=prompt,
                status=(
                    "generated_openai"
                    if IMAGE_GENERATION_MODE == "openai"
                    else "generated_mock"
                ),
                created_at=datetime.utcnow(),
            )

            db.add(image)
            saved_images.append(image)

        project.status = "images_generated"
        db.commit()

        return {
            "project_id": project_id,
            "project_name": project.project_name,
            "status": "images_generated",
            "image_generation_mode": IMAGE_GENERATION_MODE,
            "images": [serialize_scene_image(image) for image in saved_images],
        }
    finally:
        db.close()


@app.get("/projects/{project_id}/images")
def get_project_images(project_id: str):
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.project_id == project_id).first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        images = (
            db.query(SceneImage)
            .filter(SceneImage.project_id == project_id)
            .order_by(SceneImage.scene_number.asc())
            .all()
        )

        return {
            "project_id": project_id,
            "project_name": project.project_name,
            "status": "found" if images else "empty",
            "images": [serialize_scene_image(image) for image in images],
        }
    finally:
        db.close()


@app.get("/projects/{project_id}/images/{image_id}/download")
def download_scene_image(project_id: str, image_id: str):
    db = SessionLocal()
    try:
        image = (
            db.query(SceneImage)
            .filter(
                SceneImage.project_id == project_id,
                SceneImage.image_id == image_id,
            )
            .first()
        )

        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        try:
            response = s3_client.get_object(Bucket=image.bucket, Key=image.object_key)
        except ClientError:
            raise HTTPException(
                status_code=404, detail="Image file not found in object storage"
            )

        return StreamingResponse(
            response["Body"],
            media_type="image/png",
            headers={
                "Content-Disposition": f'inline; filename="scene-{image.scene_number}.png"'
            },
        )
    finally:
        db.close()


# =====================================================
# Legacy Mock AI Test Endpoint
# =====================================================
@app.post("/ai/test-generation")
def test_ai_generation(request: AITestRequest):
    return {
        "project_name": request.project_name,
        "status": "mock_ai_generated",
        "input": {
            "song_description": request.song_description,
            "story_prompt": request.story_prompt,
        },
        "storyboard": mock_storyboard_scenes(
            request.project_name, request.story_prompt
        ),
        "audio_direction": {
            "fade_out": "Fade music down before romantic dialogue.",
            "dialogue_insert": "Add soft spoken line during quiet break.",
            "fade_in": "Bring music back smoothly into final scene.",
        },
    }
