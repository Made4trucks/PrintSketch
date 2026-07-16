from pathlib import Path

from PIL import Image


def create_vision_crops(
    image_path: Path,
    output_folder: Path,
) -> dict[str, Path]:
    """Create detailed image regions for multi-pass truck analysis."""

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    with Image.open(image_path) as image:
        width, height = image.size

        crop_boxes = {
            "full": (
                0,
                0,
                width,
                height,
            ),
            "roof_windshield": (
                int(width * 0.10),
                0,
                int(width * 0.90),
                int(height * 0.48),
            ),
            "grille": (
                int(width * 0.15),
                int(height * 0.30),
                int(width * 0.85),
                int(height * 0.78),
            ),
            "lower_front": (
                int(width * 0.10),
                int(height * 0.58),
                int(width * 0.90),
                height,
            ),
        }

        results: dict[str, Path] = {}

        for crop_name, crop_box in crop_boxes.items():
            crop = image.crop(crop_box)

            crop_path = (
                output_folder
                / f"{image_path.stem}_{crop_name}.png"
            )

            crop.save(
                crop_path,
                format="PNG",
            )

            results[crop_name] = crop_path

    return results