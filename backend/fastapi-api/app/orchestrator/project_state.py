"""
Project State

Defines the lifecycle states a Versio project can move through.
"""

from enum import Enum


# =====================================================
# Project Pipeline States
# These states will eventually power frontend progress
# indicators and worker status tracking.
# =====================================================
class ProjectState(str, Enum):
    CREATED = "created"
    UPLOADED = "uploaded"
    PLANNING = "planning"
    STORYBOARD_GENERATED = "storyboard_generated"
    TIMELINE_GENERATED = "timeline_generated"
    CHARACTER_MEMORY_GENERATED = "character_memory_generated"
    PROMPTS_GENERATED = "prompts_generated"
    IMAGES_GENERATED = "images_generated"
    ANIMATION_GENERATED = "animation_generated"
    EXPORTING = "exporting"
    COMPLETED = "completed"
    FAILED = "failed"
