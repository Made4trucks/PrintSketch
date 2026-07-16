import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Studio"))

from production_pipeline import ProductionPipeline
from project import PrintSketchProject


def main() -> None:
    project = PrintSketchProject("Scania_Koops")
    pipeline = ProductionPipeline(project)

    pipeline.run()


if __name__ == "__main__":
    main()