import json
from pathlib import Path

from pipeline_stage import PipelineStage
from vision_report import create_vision_report


class VisionStage(PipelineStage):
    """Analyze the project photo and create the Vision Report."""

    name = "Vision Analysis"

    @property
    def output_path(self) -> Path:
        return (
            self.context.vision_folder
            / "vision_report.json"
        )

    def is_ready(self) -> bool:
        return self.output_path.exists()

    def validate(self) -> None:
        if not self.output_path.exists():
            raise FileNotFoundError(
                f"Vision Report does not exist: "
                f"{self.output_path}"
            )

        try:
            data = json.loads(
                self.output_path.read_text(
                    encoding="utf-8"
                )
            )
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Vision Report contains invalid JSON: "
                f"{self.output_path}"
            ) from error

        if not isinstance(data, dict):
            raise ValueError(
                f"Vision Report must contain a JSON object: "
                f"{self.output_path}"
            )

    def run(self) -> None:
        if not self.context.photo.exists():
            raise FileNotFoundError(
                f"Project photo does not exist: "
                f"{self.context.photo}"
            )

        self.print_start()

        create_vision_report(
            image_path=self.context.photo,
            output_path=self.output_path,
        )

        self.validate()

        self.print_complete()
        print(f"Saved to: {self.output_path}")