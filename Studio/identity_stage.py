from pathlib import Path

from pipeline_stage import PipelineStage


class IdentityStage(PipelineStage):
    """Prepare an editable approved identity map."""

    name = "Identity Review"

    @property
    def source_path(self) -> Path:
        return (
            self.context.vision_folder
            / "vision_report.json"
        )

    @property
    def output_path(self) -> Path:
        return (
            self.context.identity_folder
            / "approved_identity.json"
        )

    def is_ready(self) -> bool:
        return self.output_path.exists()

    def run(self) -> None:
        if not self.source_path.exists():
            raise FileNotFoundError(
                f"Vision Report does not exist: "
                f"{self.source_path}"
            )

        self.print_start()

        self.output_path.write_text(
            self.source_path.read_text(
                encoding="utf-8"
            ),
            encoding="utf-8",
        )

        self.print_complete()
        print(f"Saved to: {self.output_path}")
        print(
            "Review and correct this file before "
            "building the production prompt."
        )