import base64
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Studio"))

from vision_crops import create_vision_crops


load_dotenv()


SOURCE_IMAGE = (
    PROJECT_ROOT
    / "Results"
    / "uploads"
    / "Scania_MyTruck.jpg"
)

CROP_FOLDER = (
    PROJECT_ROOT
    / "Results"
    / "vision_crops"
)

OUTPUT_REPORT = (
    PROJECT_ROOT
    / "Results"
    / "vision_reports"
    / "Scania_MyTruck_grille.json"
)


def image_to_data_url(image_path: Path) -> str:
    encoded = base64.b64encode(
        image_path.read_bytes()
    ).decode("ascii")

    return f"data:image/png;base64,{encoded}"


def main() -> None:
    crops = create_vision_crops(
        image_path=SOURCE_IMAGE,
        output_folder=CROP_FOLDER,
    )

    grille_crop = crops["grille"]

    client = OpenAI()

    instructions = """
Analyze only this cropped front-grille region.

Left and right always mean the viewer's perspective.

Return valid JSON only:

{
  "model_designation": {
    "text": "",
    "side": "viewer_left|viewer_right|center|uncertain",
    "position_description": ""
  },
  "grille_lights": {
    "count": 0,
    "arrangement": "",
    "row_structure": "",
    "outer_shape": ""
  },
  "grille": {
    "horizontal_bar_count": 0,
    "mesh_present": false,
    "description": ""
  },
  "visible_text": [
    {
      "text": "",
      "side": "",
      "orientation": "horizontal|vertical|angled|uncertain",
      "position_description": ""
    }
  ],
  "uncertain_items": []
}

Rules:
- Do not analyze roof lights.
- Do not include main headlights unless they overlap the grille crop.
- Count only the six small auxiliary lights mounted on the grille.
- Describe their exact arrangement spatially.
- Never guess unreadable text.
- Do not call horizontal text vertical because of its position.
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": instructions,
                    },
                    {
                        "type": "input_image",
                        "image_url": image_to_data_url(
                            grille_crop
                        ),
                    },
                ],
            }
        ],
    )

    report = json.loads(response.output_text)

    OUTPUT_REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_REPORT.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("Grille Vision Report created.")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()