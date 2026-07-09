# World Intelligence Engine

The World Intelligence Engine, or WIE, owns world, setting, and environment continuity across the Versio pipeline.

## Purpose

WIE acts like the art department and worldbuilding department of the AI production studio.

It keeps the visual world consistent across scenes.

## Responsibilities

- Define the project world
- Track locations
- Track architecture style
- Track weather
- Track time of day
- Track lighting
- Track color palette
- Track technology level
- Track magic/sci-fi rules
- Track environmental mood
- Prevent visual style drift across generated scenes

## Future Data

Each world profile will eventually include:

- world_id
- project_id
- genre
- era
- primary_locations
- architecture_style
- color_palette
- lighting_style
- weather_pattern
- technology_level
- magic_system
- visual_rules
- environment_reference_prompt

## Pipeline Position

AI Director
→ World Intelligence Engine
→ Prompt Builder
→ Image Worker
→ Animation Worker
→ Video Worker

## Design Rule

Downstream services should not invent world details independently.

They should request world context from WIE.
