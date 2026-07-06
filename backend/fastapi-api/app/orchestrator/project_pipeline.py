"""
Project Pipeline

The Project Pipeline is the orchestration layer for Versio.

It does not replace existing API endpoints yet.
It gives future services one clean place to coordinate work.
"""

from typing import Any

from app.orchestrator.pipeline_context import PipelineContext
from app.orchestrator.project_state import ProjectState
from app.services.timeline_builder import build_timeline_from_storyboard


# =====================================================
# Project Pipeline
# Coordinates pipeline stages for a single project.
# =====================================================
class ProjectPipeline:
    def __init__(
        self,
        project_id: str,
        project_name: str,
        story_prompt: str,
    ) -> None:
        self.context = PipelineContext(
            project_id=project_id,
            project_name=project_name,
            story_prompt=story_prompt,
            state=ProjectState.CREATED,
        )

    # =====================================================
    # Load Storyboard
    # Stores existing storyboard scenes in the pipeline context.
    # =====================================================
    def load_storyboard(self, storyboard: list[dict[str, Any]]) -> PipelineContext:
        self.context.storyboard = storyboard
        self.context.set_state(ProjectState.STORYBOARD_GENERATED)
        return self.context

    # =====================================================
    # Build Timeline
    # Converts storyboard scenes into timeline entries.
    # =====================================================
    def build_timeline(self) -> PipelineContext:
        timeline = build_timeline_from_storyboard(self.context.storyboard)
        self.context.timeline = timeline
        self.context.set_state(ProjectState.TIMELINE_GENERATED)
        return self.context

    # =====================================================
    # Placeholder Character Memory Stage
    # This will be implemented in the Character Memory sprint.
    # =====================================================
    def build_character_memory(self) -> PipelineContext:
        self.context.characters = []
        self.context.set_state(ProjectState.CHARACTER_MEMORY_GENERATED)
        return self.context

    # =====================================================
    # Placeholder Prompt Stage
    # This will be implemented in Prompt Builder 2.0.
    # =====================================================
    def build_prompts(self) -> PipelineContext:
        self.context.prompts = []
        self.context.set_state(ProjectState.PROMPTS_GENERATED)
        return self.context

    # =====================================================
    # Pipeline Snapshot
    # Returns the current state of the pipeline.
    # =====================================================
    def snapshot(self) -> dict[str, Any]:
        return self.context.to_dict()
