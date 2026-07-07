"""
Pipeline Exceptions

Custom exceptions for pipeline-level errors.
"""


# =====================================================
# Base Pipeline Exception
# =====================================================
class PipelineException(Exception):
    """Base exception for all Versio pipeline errors."""


# =====================================================
# Stage-Specific Exceptions
# =====================================================
class StoryboardPipelineException(PipelineException):
    """Raised when storyboard generation fails."""


class TimelinePipelineException(PipelineException):
    """Raised when timeline generation fails."""


class CharacterMemoryPipelineException(PipelineException):
    """Raised when character memory generation fails."""


class PromptPipelineException(PipelineException):
    """Raised when prompt generation fails."""


class ImagePipelineException(PipelineException):
    """Raised when image generation fails."""


class ExportPipelineException(PipelineException):
    """Raised when export generation fails."""
