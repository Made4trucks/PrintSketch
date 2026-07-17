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
  "readiness_observations": {
    "truck_frame_coverage_percent": 0,
    "cab_fully_visible": false,
    "front_fully_visible": false,
    "roof_fully_visible": false,
    "bumper_fully_visible": false,
    "left_mirror_visible": false,
    "right_mirror_visible": false,
    "grille_clearly_visible": false,
    "headlights_clearly_visible": false,
    "brand_text_readable": false,
    "model_text_readable": false,
    "company_text_readable": false,
    "license_plate_readable": false,
    "perspective_suitability": "excellent|good|acceptable|poor",
    "crop_quality": "excellent|good|acceptable|poor",
    "obstructions_present": false,
    "obstructions": [],
    "background_complexity": "low|medium|high",
    "identity_visibility": "excellent|good|acceptable|poor"
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
},
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
  - Estimate truck_frame_coverage_percent as the approximate percentage of the
  complete photograph occupied by the visible truck or cab.
- cab_fully_visible is true only when the complete cab silhouette needed for
  the artwork is visible.
- front_fully_visible is true only when the main front geometry is not cropped
  or blocked.
- Mark each mirror, roof, bumper, grille and headlight field independently.
- A text field is readable only when its actual visible wording can be
  identified confidently. Do not mark it readable based only on its location.
- Record every object that blocks part of the truck in obstructions.
- Do not count normal truck accessories as obstructions.
- perspective_suitability evaluates whether the original angle is useful for
  producing recognizable circular PrintSketch wall art.
- crop_quality evaluates whether important parts of the cab are cut off by the
  photograph boundaries.
- identity_visibility evaluates whether the brand, model, company markings,
  grille, lights and owner-installed details can be preserved faithfully.
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