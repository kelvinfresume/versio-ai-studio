# Character Intelligence Engine

The Character Intelligence Engine, or CIE, owns character identity and continuity across the entire Versio pipeline.

                Project Pipeline
                       │
     ┌─────────────────┼─────────────────┐
     │                 │                 │
 AI Director     Character Intelligence   Timeline Builder
                     Engine (CIE)
     │                 │                 │
     └─────────────────┼─────────────────┘
                       │
                Prompt Builder
                       │
             Image Generation Worker
                       │
              Animation Pipeline
                       │
              Video Composition
                       │
                 Export Pipeline

## Purpose

CIE acts like the casting department of the AI production studio.

It is responsible for keeping characters visually, emotionally, and narratively consistent from scene to scene.

## Responsibilities

- Identify main characters from AI Director output
- Define canonical character profiles
- Track physical appearance
- Track clothing and accessories
- Track emotional progression
- Track relationships between characters
- Track which characters appear in each scene
- Generate reusable character reference prompts
- Prevent every image prompt from reinventing characters

## Future Data

Each character will eventually include:

- character_id
- name
- role
- age
- gender
- hair
- eyes
- skin tone
- height
- build
- clothing
- accessories
- personality
- emotional arc
- relationships
- scene appearances
- reference_prompt

## Pipeline Position

AI Director
→ Character Intelligence Engine
→ Prompt Builder
→ Image Worker
→ Animation Worker
→ Video Worker

## Design Rule

Downstream services should not invent character details independently.

They should request character context from CIE.
