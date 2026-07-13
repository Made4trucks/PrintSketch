import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def is_ai_available() -> bool:
    """Check whether the API key is available."""

    return bool(os.getenv("OPENAI_API_KEY"))


def generate_ai_preview(
    source_image_path: Path,
    prompt: str,
    output_path: Path,
) -> Path:
    """Generate a preview from the source image and production prompt."""

    if not is_ai_available():
        raise RuntimeError("OPENAI_API_KEY is missing.")

    if not source_image_path.exists():
        raise FileNotFoundError(
            f"Source image not found: {source_image_path}"
        )

    if not prompt.strip():
        raise ValueError("Prompt is empty.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    client = OpenAI()

    with source_image_path.open("rb") as source_image:
        result = client.images.edit(
            model="gpt-image-2",
            image=source_image,
            prompt=prompt,
            size="1024x1024",
            quality="medium",
        )

    image_base64 = result.data[0].b64_json

    if not image_base64:
        raise RuntimeError("The API did not return image data.")

    image_bytes = base64.b64decode(image_base64)
    output_path.write_bytes(image_bytes)

    return output_path