import json
from pathlib import Path

from pipeline_stage import PipelineStage
from printsketch_readiness import create_readiness_report


class ReadinessStage(PipelineStage):
    """Calculate PrintSketch production readiness."""

    name = "PrintSketch Readiness"

    @property
    def vision_report_path(self) -> Path:
        return (
            self.context.vision_folder
            / "vision_report.json"
        )

    @property
    def output_path(self) -> Path:
        return (
            self.context.vision_folder
            / "readiness_report.json"
        )

    def is_ready(self) -> bool:
        return self.output_path.exists()

    def validate(self) -> None:
        if not self.output_path.exists():
            raise FileNotFoundError(
                f"Readiness Report does not exist: "
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
                f"Readiness Report contains invalid JSON: "
                f"{self.output_path}"
            ) from error

        if not isinstance(data, dict):
            raise ValueError(
                f"Readiness Report must contain a JSON object: "
                f"{self.output_path}"
            )

    def run(self) -> None:
        if not self.vision_report_path.exists():
            raise FileNotFoundError(
                f"Vision Report does not exist: "
                f"{self.vision_report_path}"
            )

        self.print_start()

        create_readiness_report(
            vision_report_path=self.vision_report_path,
            output_path=self.output_path,
        )

        self.validate()

        self.print_complete()
        print(f"Saved to: {self.output_path}")