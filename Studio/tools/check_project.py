from pathlib import Path
from project import PrintSketchProject

APP_NAME = "PrintSketch Studio"
VERSION = "1.0.0"


def check_project():
    project = PrintSketchProject()

    print(f"Current project: {project.project_name}")
    print()

    required = [
        "Bible",
        "Engine",
        "Benchmark",
        "Evaluation",
        "Prompts",
        "Results",
        "Tests",
    ]

    root = Path(__file__).resolve().parent.parent

    print(f"{APP_NAME} {VERSION}")
    print("-" * 40)

    missing = []

    for folder in required:
        if (root / folder).exists():
            print(f"[OK] {folder}")
        else:
            print(f"[MISSING] {folder}")
            missing.append(folder)

    print("-" * 40)

    if missing:
        print("Project structure is incomplete.")
    else:
        print("Project structure verified successfully.")


if __name__ == "__main__":
    check_project()