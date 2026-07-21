from dataclasses import dataclass
from pathlib import Path


@dataclass
class PromptContext:
    """
    Central project context used by the Prompt Compiler.

    This object will gradually become the single source of truth
    for everything required to compile a production prompt.
    """

    # Identity
    identity_map_path: Path | None = None

    # Future pipeline data
    vision_report_path: Path | None = None
    readiness_report_path: Path | None = None

    # Project settings
    project_name: str = ""
    style_name: str = "Classic"

    # Manufacturing
    manufacturing_profile: str = "FDM_STANDARD_04"

    # Future
    preview_path: Path | None = None
    svg_path: Path | None = None