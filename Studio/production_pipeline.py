from pathlib import Path

from project import PrintSketchProject
from project_context import ProjectContext
from prompt_builder import build_prompt
from vision_report import create_vision_report
from project_status import ProjectStatus


class ProductionPipeline:
    """Orchestrates the PrintSketch production workflow."""

    def __init__(self, project: PrintSketchProject) -> None:
        self.project = project
        self.context: ProjectContext = project.context

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
    def analyze_photo(self) -> Path:
        """Create and save the project's general Vision Report."""

        self.validate_project()

        output_path = (
            self.context.vision_folder
            / "vision_report.json"
        )

        print()
        print("Analyzing project photo...")
        print(f"Source: {self.context.photo}")

        create_vision_report(
            image_path=self.context.photo,
            output_path=output_path,
        )

        print("Vision Report created successfully.")
        print(f"Saved to: {output_path}")

        return output_path
    
    def prepare_identity_map(self) -> Path:
        """Create an editable identity map from the Vision Report."""

        vision_report_path = (
            self.context.vision_folder
            / "vision_report.json"
        )

        if not vision_report_path.exists():
            raise FileNotFoundError(
                f"Vision Report does not exist: "
                f"{vision_report_path}"
            )

        output_path = (
            self.context.identity_folder
            / "approved_identity.json"
        )

        output_path.write_text(
            vision_report_path.read_text(
                encoding="utf-8"
            ),
            encoding="utf-8",
        )

        print()
        print("Identity Map prepared successfully.")
        print(f"Saved to: {output_path}")
        print(
            "Review and correct this file before "
            "building the production prompt."
        )

        return output_path
    
    def build_production_prompt(self) -> Path:
        """Build and save the final production prompt."""

        identity_map_path = (
            self.context.identity_folder
            / "approved_identity.json"
        )

        if not identity_map_path.exists():
            raise FileNotFoundError(
                f"Approved Identity Map does not exist: "
                f"{identity_map_path}"
            )

        output_path = (
            self.context.prompt_folder
            / "assembled_prompt.txt"
        )

        print()
        print("Building production prompt...")
        print(f"Identity Map: {identity_map_path}")

        prompt = build_prompt(
            identity_map_path=identity_map_path
        )

        output_path.write_text(
            prompt,
            encoding="utf-8",
        )

        print("Production prompt created successfully.")
        print(f"Saved to: {output_path}")
        print(f"Total characters: {len(prompt)}")

        return output_path

    def run(self) -> None:
        print()
        print("=" * 60)
        print("PrintSketch Production Pipeline")
        print("=" * 60)

        self.validate_project()

        status = ProjectStatus(self.context)

        if not status.vision_ready:
            self.analyze_photo()

        status = ProjectStatus(self.context)

        if not status.identity_ready:
            self.prepare_identity_map()

        status = ProjectStatus(self.context)

        if not status.prompt_ready:
            self.build_production_prompt()

        status = ProjectStatus(self.context)

        print()
        print("Current project status:")
        status.print_summary()

        print()
        print("Pipeline finished.")

        
    
    