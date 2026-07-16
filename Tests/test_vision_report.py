from pathlib import Path
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Studio"))

from vision_report import create_vision_report


SOURCE_IMAGE = (
    PROJECT_ROOT
    / "Results"
    / "uploads"
    / "Scania_MyTruck.jpg"
)

OUTPUT_REPORT = (
    PROJECT_ROOT
    / "Results"
    / "vision_reports"
    / "Scania_MyTruck.json"
)


def main():

    print("Creating Vision Report...")

    report = create_vision_report(
        image_path=SOURCE_IMAGE,
        output_path=OUTPUT_REPORT,
    )

    print()
    print("Vision Report created.")
    print()
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()