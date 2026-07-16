import base64
import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


VISION_MODEL = os.getenv(
    "PRINTSKETCH_VISION_MODEL",
    "gpt-4.1",
)


VISION_INSTRUCTIONS = """
Analyze the uploaded truck photograph for PrintSketch.

Your task is NOT to redesign the truck and NOT to suggest artistic changes.

Create a precise factual identity map of what is visibly present in the
source image. Pay special attention to exact position, quantity, layout,
perspective and readable text.

Return valid JSON only. Do not use Markdown.

Use this exact structure:

{
  "vehicle": {
    "brand": "",
    "model_designation": "",
    "model_designation_position": "",
    "cab_type": "",
    "viewing_angle": "",
    "camera_height": ""
  },
  "composition": {
    "tractor_only_or_trailer_visible": "",
    "truck_orientation": "",
    "important_crop_information": ""
  },
  "company_identity": [
    {
      "text": "",
      "position": "",
      "appearance": ""
    }
  ],
  "owner_signatures": [
    {
      "text_or_element": "",
      "position": "",
      "print_importance": "critical|important|optional"
    }
  ],
  "lighting_map": {
  "roof_lights": [
    {
      "count": 0,
      "position": "",
      "arrangement": "",
      "outer_shape": ""
    }
  ],
  "grille_lights": [
    {
      "count": 0,
      "position": "",
      "arrangement": "",
      "outer_shape": ""
    }
  ],
  "bumper_lights": [
    {
      "count": 0,
      "position": "",
      "arrangement": "",
      "outer_shape": ""
    }
  ],
  "main_headlights": {
    "count": 0,
    "position": "",
    "outer_shape": ""
  }
}
  "windows": {
    "windshield_contents": [],
    "side_window_contents": [],
    "curtains_present": false
  },
  "front_geometry": {
    "grille_bar_count": 0,
    "grille_description": "",
    "headlight_description": "",
    "bumper_description": ""
  },
  "do_not_move": [],
  "do_not_invent": [],
  "uncertain_items": []
}

Rules:

- Report only what can actually be seen.
- Preserve left and right positions from the viewer's perspective.
- Never guess missing text.
- If text is uncertain, place it in "uncertain_items".
- Count visible lights carefully.
- Describe distinctive arrangements such as pyramid, vertical row,
  horizontal row or symmetrical groups.
- Record the original location of every important identity marking.
- Left and right always refer to the viewer looking at the photograph.
- Never combine roof lights, grille lights, bumper lights and main headlights.
- Count each lighting group separately.
- For grille lights, record their exact spatial pattern, such as pyramid,
  triangle, vertical stack, horizontal row or rectangular grid.
- Text orientation must be reported explicitly as horizontal, vertical or angled.
- Do not describe horizontal lettering as vertical merely because it is positioned
  high or low on the vehicle.
- For every model badge, provide its exact side from the viewer's perspective.
- If the position cannot be determined confidently, place it in uncertain_items
  instead of guessing.
"""


def _image_to_data_url(image_path: Path) -> str:
    suffix = image_path.suffix.lower()

    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }

    mime_type = mime_types.get(suffix)

    if mime_type is None:
        raise ValueError(
            f"Unsupported image format: {image_path.suffix}"
        )

    encoded = base64.b64encode(
        image_path.read_bytes()
    ).decode("ascii")

    return f"data:{mime_type};base64,{encoded}"


def _clean_json_text(text: str) -> str:
    cleaned = text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]

    if cleaned.startswith("```"):
        cleaned = cleaned[3:]

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]

    return cleaned.strip()


def create_vision_report(
    image_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing."
        )

    client = OpenAI()
    image_data_url = _image_to_data_url(image_path)

    response = client.responses.create(
        model=VISION_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": VISION_INSTRUCTIONS,
                    },
                    {
                        "type": "input_image",
                        "image_url": image_data_url,
                    },
                ],
            }
        ],
    )

    raw_text = _clean_json_text(response.output_text)
    report = json.loads(raw_text)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return report