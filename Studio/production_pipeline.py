from project import PrintSketchProject
from project_context import ProjectContext
from project_status import ProjectStatus
from vision_stage import VisionStage
from readiness_stage import ReadinessStage
from identity_stage import IdentityStage
from prompt_stage import PromptStage
from preview_stage import PreviewStage


class ProductionPipeline:
    """Orchestrates the PrintSketch production workflow."""

    def __init__(self, project: PrintSketchProject) -> None:
        self.project = project
        self.context: ProjectContext = project.context

        self.stages = [
        VisionStage(self.context),
        ReadinessStage(self.context),
        IdentityStage(self.context),
        PromptStage(self.context),
        PreviewStage(self.context),
]

    def validate_project(self) -> None:
        """Check whether the project is ready for processing."""

        if not self.context.project_folder.exists():
            raise FileNotFoundError(
                f"Project folder does not exist: "
                f"{self.context.project_folder}"
            )

        if not self.context.photo.exists():
            raise FileNotFoundError(
                f"Project photo does not exist: "
                f"{self.context.photo}"
            )

    def print_status(self) -> None:
        """Display the current project paths."""

        print("PrintSketch Production Pipeline")
        print(f"Project: {self.context.project_name}")
        print(f"Project folder: {self.context.project_folder}")
        print(f"Photo: {self.context.photo}")
        print(f"Vision folder: {self.context.vision_folder}")
        print(f"Identity folder: {self.context.identity_folder}")
        print(f"Prompt folder: {self.context.prompt_folder}")
        print(f"Preview folder: {self.context.preview_folder}")
        print(f"SVG folder: {self.context.svg_folder}")
        print(f"Fusion folder: {self.context.fusion_folder}")
        print(f"Exports folder: {self.context.exports_folder}")

    def run_initialization(self) -> ProjectContext:
        """Validate and initialize the project pipeline."""

        self.validate_project()
        self.print_status()

        return self.context
    

    def run(self) -> None:
        """Run all production stages in the correct order."""

        print()
        print("=" * 60)
        print("PrintSketch Production Pipeline")
        print("=" * 60)

        self.validate_project()

        for stage in self.stages:
            if stage.is_ready():
                stage.validate()
                stage.print_skip()
                continue

            stage.run()

        status = ProjectStatus(self.context)

        print()
        print("Current project status:")
        status.print_summary()

        print()
        print("Pipeline finished.")