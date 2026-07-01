"""
Versio AI Director Service

This module is intentionally standalone so the future backend refactor can move
AI planning out of main.py without breaking current routes.
"""

import json
from typing import Any


# =====================================================
# JSON Response Parser
# Keeps AI responses safe even if the model wraps JSON
# in markdown fences.
# =====================================================
def parse_json_response(raw_text: str) -> dict[str, Any]:
    cleaned = raw_text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "", 1).strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```", "", 1).strip()

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()

    return json.loads(cleaned)


# =====================================================
# AI Director Prompt Builder
# Creates the instruction sent to OpenAI.
# =====================================================
def build_ai_director_prompt(project_name: str, story_prompt: str) -> str:
    return f"""
You are Versio AI Director, a cinematic anime music-video planner.

Create a professional anime storyboard plan for this project.

Project name:
{project_name}

User story prompt:
{story_prompt}

Return ONLY valid JSON with this exact shape:

{{
  "story_summary": "short summary of the full anime story",
  "visual_style": "overall anime visual style",
  "mood": "overall emotional mood",
  "pacing": "slow, medium, fast, or mixed",
  "camera_language": "overall camera style",
  "transition_style": "overall transition style",
  "animation_style": "overall motion/animation direction",
  "storyboard": [
    {{
      "scene": 1,
      "title": "short scene title",
      "visual": "detailed anime visual direction",
      "camera": "camera movement and framing",
      "emotion": "emotional tone"
    }}
  ]
}}

Rules:
- Generate exactly 8 scenes.
- Keep every scene safe for all audiences.
- No gore.
- No explicit sexual content.
- No copyrighted characters.
- Make scenes cinematic and emotionally connected.
- Maintain visual continuity across scenes.
- Use anime movie language.
- Do not include markdown.
- Do not include explanations.
""".strip()


# =====================================================
# AI Director Normalizer
# Ensures every scene has the fields current database
# columns already support.
# =====================================================
def normalize_storyboard_scenes(ai_payload: dict[str, Any]) -> list[dict[str, Any]]:
    scenes = ai_payload.get("storyboard", [])

    if not isinstance(scenes, list) or len(scenes) == 0:
        raise ValueError("AI Director returned no storyboard scenes.")

    normalized_scenes = []

    for index, scene in enumerate(scenes, start=1):
        normalized_scenes.append(
            {
                "scene": int(scene.get("scene", index)),
                "title": str(scene.get("title", f"Scene {index}")),
                "visual": str(scene.get("visual", "Anime cinematic scene.")),
                "camera": str(scene.get("camera", "cinematic camera movement")),
                "emotion": str(scene.get("emotion", "emotional")),
            }
        )

    return normalized_scenes


# =====================================================
# AI Director Runner
# Receives an initialized OpenAI client from main.py so
# this service does not need direct Vault access yet.
# =====================================================
def generate_ai_director_storyboard(
    openai_client: Any,
    model: str,
    project_name: str,
    story_prompt: str,
) -> list[dict[str, Any]]:
    prompt = build_ai_director_prompt(
        project_name=project_name,
        story_prompt=story_prompt,
    )

    response = openai_client.responses.create(
        model=model,
        input=prompt,
    )

    ai_payload = parse_json_response(response.output_text)

    return normalize_storyboard_scenes(ai_payload)
