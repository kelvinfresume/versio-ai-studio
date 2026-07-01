# AI Director

## Purpose

The AI Director is the creative brain of Versio AI Studio.

Its responsibility is to convert a user's project into a structured cinematic plan before any images or videos are generated.

The AI Director is intentionally independent from image generation, animation, and rendering so every downstream service receives the same creative direction.

---

# Pipeline

Song
↓

Story Prompt
↓

AI Director
↓

Scene Planner
↓

Timeline Builder
↓

Character Memory
↓

Prompt Builder
↓

Image Generator
↓

Animation Workers
↓

Video Workers
↓

Export Pipeline

---

# Responsibilities

The AI Director is responsible for:

- Understanding the user's story prompt
- Planning the complete story
- Maintaining narrative consistency
- Choosing pacing
- Defining emotional progression
- Selecting cinematic camera language
- Creating scene transitions
- Maintaining visual continuity

The AI Director DOES NOT generate images.

It only generates structured planning data.

---

# Current Version

Current version:

AI Director v1

Current output:

- Storyboard scenes
- Scene titles
- Visual descriptions
- Camera directions
- Emotional tone

Current model:

GPT-5.5

---

# Future Versions

## AI Director v2

Will additionally generate:

- Story Summary
- Main Theme
- Visual Style
- Animation Style
- Lighting Style
- Color Palette
- Transition Style
- Camera Language
- Recommended Aspect Ratio
- Scene Duration
- Estimated Video Length

---

## AI Director v3

Will understand:

- Uploaded lyrics
- Beat analysis
- Song structure
- BPM
- Chorus detection
- Verse detection
- Instrumental breaks
- Emotional peaks

---

## AI Director v4

Will integrate with:

- Timeline Builder
- Character Memory
- Prompt Builder
- Beat Sync Engine
- Transition Engine

This allows every service to receive one consistent creative vision.

---

# Current API Flow

POST

/projects/{project_id}/storyboard

↓

Backend loads project

↓

AI Director receives:

- Project Name
- Story Prompt

↓

OpenAI GPT

↓

Structured JSON

↓

PostgreSQL

↓

Frontend

---

# Example Output

{
  "storyboard": [
    {
      "scene": 1,
      "title": "Opening",
      "visual": "...",
      "camera": "...",
      "emotion": "..."
    }
  ]
}

---

# Design Goals

- Modular
- Stateless
- Deterministic JSON
- Easily testable
- Service-oriented
- Reusable by future workers

---

# Planned Integrations

- Character Memory
- Timeline Builder
- Prompt Builder
- Beat Sync
- Animation Engine
- Image Worker
- Video Worker
- Caption Worker
- Export Pipeline

---

# Notes

The AI Director should remain the single source of truth for creative planning.

No downstream worker should invent story details independently.

Every worker should consume AI Director output rather than generating its own narrative.
