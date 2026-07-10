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
    file_size = round(path.stat().st_size / 1024, 1)
    aspect_ratio = round(width / height, 2)

    quality_score = 100

    if megapixels < 2:
        quality_score -= 40
    elif megapixels < 4:
        quality_score -= 20

    if mode != "RGB":
        quality_score -= 10

    if width < 1200:
        quality_score -= 20

    quality_score = max(0, quality_score)

    if quality_score >= 85:
        photo_status = "EXCELLENT"
        recommendation = "READY FOR SVG"

    elif quality_score >= 70:
        photo_status = "GOOD"
        recommendation = "READY FOR SVG"

    elif quality_score >= 50:
        photo_status = "AVERAGE"
        recommendation = "UPSCALING RECOMMENDED"

    else:
        photo_status = "POOR"
        recommendation = "BETTER PHOTO REQUIRED"

        

    return {
        "filename": path.name,
        "width": width,
        "height": height,
        "orientation": orientation,
        "megapixels": megapixels,
        "format": image_format,
        "mode": mode,
        "file_size_kb": file_size,
        "aspect_ratio": aspect_ratio,
        "quality_score": quality_score,
        "photo_status": photo_status,
        "recommendation": recommendation,
    }


if __name__ == "__main__":
    print("Image analyzer ready.")