from dataclasses import dataclass
from pathlib import Path


@dataclass
class PrintSketchProject:
    project_name: str = "Untitled Project"
    image_path: str = ""
    image_width: int = 0
    image_height: int = 0
    orientation: str = ""
    size_cm: int = 20
    style: str = "Classic"
    prompt: str = ""

    @property
    def output_folder(self) -> Path:
        return Path("Results") / self.project_name