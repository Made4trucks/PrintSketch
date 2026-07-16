from pathlib import Path

from pipeline_stage import PipelineStage
from prompt_builder import build_prompt


class PromptStage(PipelineStage):
    """Build the final production prompt from the approved identity map."""

    name = "Prompt Assembly"

    @property
    def identity_map_path(self) -> Path:
        return (
            self.context.identity_folder
            / "approved_identity.json"
        )

    @property
    def output_path(self) -> Path:
        return (
            self.context.prompt_folder
            / "assembled_prompt.txt"
        )

    def is_ready(self) -> bool:
        return self.output_path.exists()

    def run(self) -> None:
        if not self.identity_map_path.exists():
            raise FileNotFoundError(
                f"Approved Identity Map does not exist: "
                f"{self.identity_map_path}"
            )

        self.print_start()

        prompt = build_prompt(
            identity_map_path=self.identity_map_path
        )

        self.output_path.write_text(
            prompt,
            encoding="utf-8",
        )

        self.print_complete()
        print(f"Saved to: {self.output_path}")
        print(f"Total characters: {len(prompt)}")