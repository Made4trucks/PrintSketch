import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Studio"))

from project import PrintSketchProject


SOURCE_IMAGE = (
    PROJECT_ROOT
    / "Results"
    / "uploads"
    / "Scania_MyTruck.jpg"
)


def main() -> None:
    project = PrintSketchProject("Scania_Koops")

    project.create()

    imported_photo = project.import_photo(
        SOURCE_IMAGE
    )

    print("Project created successfully.")
    print(f"Project folder: {project.project_folder}")
    print(f"Imported photo: {imported_photo}")
    print(f"Photo exists: {project.photo.exists()}")


if __name__ == "__main__":
    main()