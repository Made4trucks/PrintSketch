from dataclasses import dataclass

from project_context import ProjectContext


@dataclass(slots=True)
class ProjectStatus:
    """Checks which stages of a PrintSketch project already exist."""

    context: ProjectContext

    @property
    def photo_ready(self) -> bool:
        return self.context.photo.exists()

    @property
    def vision_ready(self) -> bool:
        return (
            self.context.vision_folder
            / "vision_report.json"
        ).exists()

    @property
    def identity_ready(self) -> bool:
        return (
            self.context.identity_folder
            / "approved_identity.json"
        ).exists()

    @property
    def prompt_ready(self) -> bool:
        return (
            self.context.prompt_folder
            / "assembled_prompt.txt"
        ).exists()

    @property
    def preview_ready(self) -> bool:
        return bool(
            list(self.context.preview_folder.glob("*.png"))
        )

    @property
    def svg_ready(self) -> bool:
        return bool(
            list(self.context.svg_folder.glob("*.svg"))
        )

    @property
    def fusion_ready(self) -> bool:
        if not self.context.fusion_folder.exists():
             return False

        return any(self.context.fusion_folder.iterdir())

    @property
    def exports_ready(self) -> bool:
        if not self.context.exports_folder.exists():
            return False

        return any(self.context.exports_folder.iterdir())

    def as_dict(self) -> dict[str, bool]:
        return {
            "photo": self.photo_ready,
            "vision": self.vision_ready,
            "identity": self.identity_ready,
            "prompt": self.prompt_ready,
            "preview": self.preview_ready,
            "svg": self.svg_ready,
            "fusion": self.fusion_ready,
            "exports": self.exports_ready,
        }

    def print_summary(self) -> None:
        print()
        print("PrintSketch Project Status")
        print(f"Project: {self.context.project_name}")
        print("-" * 32)

        for stage, ready in self.as_dict().items():
            symbol = "✓" if ready else "X"
            print(f"{symbol} {stage.capitalize()}")