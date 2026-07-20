from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectContext:
    project_name: str
    project_folder: Path
    photo: Path
    vision_folder: Path
    identity_folder: Path
    prompt_folder: Path
    preview_folder: Path
    svg_folder: Path
    fusion_folder: Path
    exports_folder: Path