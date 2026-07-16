import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Studio"))

from production_pipeline import ProductionPipeline
from project import PrintSketchProject


def main() -> None:
    project = PrintSketchProject("Scania_Koops")

    pipeline = ProductionPipeline(project)

    context = pipeline.run_initialization()

    vision_report_path = pipeline.analyze_photo()
    identity_map_path = pipeline.prepare_identity_map()
    prompt_path = pipeline.build_production_prompt()

    print()
    print("Pipeline initialized successfully.")
    print(f"Context project: {context.project_name}")
    print(f"Photo exists: {context.photo.exists()}")
    print(f"Vision report: {vision_report_path}")
    print(
        f"Vision report exists: "
        f"{vision_report_path.exists()}"
    )
    print(f"Identity map: {identity_map_path}")
    print(
        f"Identity map exists: "
        f"{identity_map_path.exists()}"
    )
    print(f"Production prompt: {prompt_path}")
    print(
        f"Production prompt exists: "
        f"{prompt_path.exists()}"
    )



if __name__ == "__main__":
    main()

    