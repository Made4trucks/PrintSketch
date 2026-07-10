from pathlib import Path
from PIL import Image


def analyze_image(image_path: str) -> dict:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with Image.open(path) as image:
        width, height = image.size
        image_format = image.format
        mode = image.mode

    if width > height:
        orientation = "landscape"
    elif height > width:
        orientation = "portrait"
    else:
        orientation = "square"

    megapixels = round((width * height) / 1_000_000, 2)

    return {
        "filename": path.name,
        "width": width,
        "height": height,
        "orientation": orientation,
        "megapixels": megapixels,
        "format": image_format,
        "mode": mode,
    }


if __name__ == "__main__":
    print("Image analyzer ready.")