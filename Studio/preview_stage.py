from pathlib import Path

from ai_preview import generate_ai_preview
from pipeline_stage import PipelineStage


class PreviewStage(PipelineStage):
    """Generate the AI artwork preview for the current project."""

    name = "AI Preview Generation"

    @property
    def prompt_path(self) -> Path:
        return (
            self.context.prompt_folder
            / "assembled_prompt.txt"
        )

    @property
    def output_path(self) -> Path:
        return (
            self.context.preview_folder
            / "preview_v1.png"
        )

    def is_ready(self) -> bool:
        return self.output_path.exists()
    
    def validate(self) -> None:
        if not self.output_path.exists():
            raise FileNotFoundError(
                f"AI Preview does not exist: "
                f"{self.output_path}"
        )

        if self.output_path.stat().st_size == 0:
            raise ValueError(
                f"AI Preview file is empty: "
                f"{self.output_path}"
        )

    def run(self) -> None:
        if not self.context.photo.exists():
            raise FileNotFoundError(
                f"Project photo does not exist: "
                f"{self.context.photo}"
            )

        if not self.prompt_path.exists():
            raise FileNotFoundError(
                f"Production prompt does not exist: "
                f"{self.prompt_path}"
            )

        prompt = self.prompt_path.read_text(
            encoding="utf-8"
        ).strip()

        if not prompt:
            raise ValueError(
                f"Production prompt is empty: "
                f"{self.prompt_path}"
            )

        self.context.preview_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.print_start()

        print(f"Source image: {self.context.photo}")
        print(f"Prompt: {self.prompt_path}")
        print("Generating AI preview...")

        generate_ai_preview(
            source_image_path=self.context.photo,
            prompt=prompt,
            output_path=self.output_path,
        )

        if not self.output_path.exists():
            raise RuntimeError(
                "Preview generation finished, but the "
                f"output file was not created: {self.output_path}"
            )
        
        self.validate()

        self.print_complete()
        print(f"Saved to: {self.output_path}")