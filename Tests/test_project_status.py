import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Studio"))

from project import PrintSketchProject
from project_status import ProjectStatus


def main() -> None:
    project = PrintSketchProject("Scania_Koops")

    status = ProjectStatus(project.context)

    status.print_summary()

    print()
    print(status.as_dict())


if __name__ == "__main__":
    main()