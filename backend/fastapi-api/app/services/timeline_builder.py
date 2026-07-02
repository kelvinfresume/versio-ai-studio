"""
Versio Timeline Builder Service

This service converts storyboard scenes into a simple production timeline.
It is intentionally standalone so future workers can consume the same timing
contract without depending directly on FastAPI route code.
"""

from typing import Any

# =====================================================
# Timeline Defaults
# These values keep the first version predictable.
# Later, beat detection and song duration will replace
# these fixed assumptions.
# =====================================================
DEFAULT_SCENE_DURATION_SECONDS = 6.0
DEFAULT_TRANSITION_SECONDS = 0.75


# =====================================================
# Music Section Resolver
# Assigns rough music-video sections based on scene order.
# This gives downstream workers an early structure before
# real beat/lyrics analysis exists.
# =====================================================
def resolve_music_section(scene_index: int, total_scenes: int) -> str:
    if scene_index == 1:
        return "intro"

    if scene_index == total_scenes:
        return "outro"

    midpoint = total_scenes / 2

    if scene_index < midpoint:
        return "verse"

    if scene_index == int(midpoint) or scene_index == int(midpoint) + 1:
        return "hook"

    return "bridge"


# =====================================================
# Transition Resolver
# Chooses simple transitions for the first timeline version.
# Later, AI Director and beat sync will make this smarter.
# =====================================================
def resolve_transition(scene_index: int, total_scenes: int) -> str:
    if scene_index == 1:
        return "fade_in"

    if scene_index == total_scenes:
        return "fade_out"

    if scene_index % 3 == 0:
        return "flash_cut"

    return "crossfade"


# =====================================================
# Camera Motion Resolver
# Converts broad camera language into worker-friendly
# camera motion labels.
# =====================================================
def resolve_camera_motion(camera_text: str) -> str:
    camera_lower = camera_text.lower()

    if "push" in camera_lower or "push-in" in camera_lower:
        return "slow_push_in"

    if "aerial" in camera_lower or "reveal" in camera_lower:
        return "aerial_reveal"

    if "close" in camera_lower:
        return "close_up"

    if "fast" in camera_lower or "cut" in camera_lower:
        return "fast_cut"

    if "pan" in camera_lower:
        return "slow_pan"

    return "cinematic_hold"


# =====================================================
# Build Scene Timeline Item
# Creates one normalized timeline entry for a storyboard scene.
# =====================================================
def build_timeline_item(
    scene: dict[str, Any],
    scene_index: int,
    total_scenes: int,
    start_time: float,
    duration: float,
) -> dict[str, Any]:
    end_time = round(start_time + duration, 2)

    return {
        "scene": int(scene.get("scene", scene_index)),
        "title": str(scene.get("title", f"Scene {scene_index}")),
        "start_time": round(start_time, 2),
        "end_time": end_time,
        "duration": round(duration, 2),
        "transition": resolve_transition(scene_index, total_scenes),
        "transition_duration": DEFAULT_TRANSITION_SECONDS,
        "camera_motion": resolve_camera_motion(str(scene.get("camera", ""))),
        "music_section": resolve_music_section(scene_index, total_scenes),
        "emotion": str(scene.get("emotion", "emotional")),
    }


# =====================================================
# Timeline Builder
# Converts storyboard scenes into a timed scene list.
# =====================================================
def build_timeline_from_storyboard(
    storyboard_scenes: list[dict[str, Any]],
    scene_duration: float = DEFAULT_SCENE_DURATION_SECONDS,
) -> dict[str, Any]:
    if not storyboard_scenes:
        return {
            "status": "empty",
            "total_duration": 0,
            "timeline": [],
        }

    timeline = []
    current_time = 0.0
    total_scenes = len(storyboard_scenes)

    for index, scene in enumerate(storyboard_scenes, start=1):
        item = build_timeline_item(
            scene=scene,
            scene_index=index,
            total_scenes=total_scenes,
            start_time=current_time,
            duration=scene_duration,
        )

        timeline.append(item)
        current_time = item["end_time"]

    return {
        "status": "timeline_generated",
        "scene_count": total_scenes,
        "total_duration": round(current_time, 2),
        "timeline": timeline,
    }
