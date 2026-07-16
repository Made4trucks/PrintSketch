import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Studio"))

from project import PrintSketchProject
from vision_stage import VisionStage


def main() -> None:
    project = PrintSketchProject("Scania_Koops")
    stage = VisionStage(project.context)

    print(f"Stage: {stage.name}")
    print(f"Ready before run: {stage.is_ready()}")

    if stage.is_ready():
        stage.print_skip()
    else:
        stage.run()

    print(f"Ready after run: {stage.is_ready()}")
    print(f"Output: {stage.output_path}")


if __name__ == "__main__":
    main()