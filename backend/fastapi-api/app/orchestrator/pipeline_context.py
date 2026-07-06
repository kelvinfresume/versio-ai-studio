"""
Pipeline Context

A shared context object passed through the Versio pipeline.

This keeps future services from passing many separate variables around.
"""

from dataclasses import dataclass, field
from typing import Any

from app.orchestrator.project_state import ProjectState


# =====================================================
# Pipeline Context
# Holds the current project and every artifact generated
# by the pipeline.
# =====================================================
@dataclass
class PipelineContext:
    project_id: str
    project_name: str
    story_prompt: str
    state: ProjectState = ProjectState.CREATED

    storyboard: list[dict[str, Any]] = field(default_factory=list)
    timeline: dict[str, Any] = field(default_factory=dict)
    characters: list[dict[str, Any]] = field(default_factory=list)
    prompts: list[dict[str, Any]] = field(default_factory=list)
    images: list[dict[str, Any]] = field(default_factory=list)
    animations: list[dict[str, Any]] = field(default_factory=list)
    exports: list[dict[str, Any]] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    # =====================================================
    # State Update Helper
    # Keeps state transitions centralized.
    # =====================================================
    def set_state(self, state: ProjectState) -> None:
        self.state = state

    # =====================================================
    # Dictionary Serializer
    # Useful for API responses and future logging.
    # =====================================================
    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "story_prompt": self.story_prompt,
            "state": self.state.value,
            "storyboard": self.storyboard,
            "timeline": self.timeline,
            "characters": self.characters,
            "prompts": self.prompts,
            "images": self.images,
            "animations": self.animations,
            "exports": self.exports,
            "metadata": self.metadata,
        }
