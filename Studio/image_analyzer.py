from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter, ImageStat


def _clamp_score(score: float) -> int:
    """Keep a score inside the 0–100 range."""
    return max(0, min(100, round(score)))


def _calculate_resolution_score(
    width: int,
    height: int,
    megapixels: float,
) -> int:
    """Evaluate whether the image resolution is suitable for PrintSketch."""

    shortest_side = min(width, height)

    if megapixels >= 8 and shortest_side >= 2000:
        return 100

    if megapixels >= 5 and shortest_side >= 1600:
        return 90

    if megapixels >= 3 and shortest_side >= 1500:
        return 80

    if megapixels >= 2 and shortest_side >= 1200:
        return 65

    if shortest_side >= 1000:
        return 50

    return 30


def _calculate_sharpness(image: Image.Image) -> dict[str, Any]:
    """
    Estimate image sharpness using edge variance.

    A sharper image normally contains stronger differences between
    neighbouring edge pixels.
    """

    grayscale = image.convert("L")

    # Resize very large images to make analysis faster and more consistent.
    grayscale.thumbnail((1600, 1600))

    edges = grayscale.filter(ImageFilter.FIND_EDGES)
    edge_statistics = ImageStat.Stat(edges)

    edge_variance = edge_statistics.var[0]

    if edge_variance >= 1800:
        score = 100
        status = "EXCELLENT"
    elif edge_variance >= 1100:
        score = 90
        status = "VERY GOOD"
    elif edge_variance >= 650:
        score = 78
        status = "GOOD"
    elif edge_variance >= 350:
        score = 62
        status = "ACCEPTABLE"
    elif edge_variance >= 180:
        score = 42
        status = "SOFT"
    else:
        score = 20
        status = "BLURRY"

    return {
        "score": score,
        "status": status,
        "edge_variance": round(edge_variance, 2),
    }


def _calculate_exposure(image: Image.Image) -> dict[str, Any]:
    """Evaluate average brightness and clipped dark/light areas."""

    grayscale = image.convert("L")
    grayscale.thumbnail((1600, 1600))

    histogram = grayscale.histogram()
    total_pixels = sum(histogram)

    mean_brightness = ImageStat.Stat(grayscale).mean[0]

    dark_pixels = sum(histogram[:25])
    bright_pixels = sum(histogram[231:])

    dark_percentage = (
        dark_pixels / total_pixels * 100
        if total_pixels
        else 0
    )

    bright_percentage = (
        bright_pixels / total_pixels * 100
        if total_pixels
        else 0
    )

    score = 100

    # Penalty for an image that is globally too dark or too bright.
    if mean_brightness < 55:
        score -= 35
        status = "TOO DARK"
    elif mean_brightness < 80:
        score -= 15
        status = "SLIGHTLY DARK"
    elif mean_brightness > 210:
        score -= 35
        status = "TOO BRIGHT"
    elif mean_brightness > 185:
        score -= 15
        status = "SLIGHTLY BRIGHT"
    else:
        status = "BALANCED"

    # Penalty for heavily clipped shadows or highlights.
    if dark_percentage > 25:
        score -= 20
    elif dark_percentage > 12:
        score -= 10

    if bright_percentage > 25:
        score -= 20
    elif bright_percentage > 12:
        score -= 10

    score = _clamp_score(score)

    return {
        "score": score,
        "status": status,
        "mean_brightness": round(mean_brightness, 2),
        "dark_pixels_percent": round(dark_percentage, 2),
        "bright_pixels_percent": round(bright_percentage, 2),
    }


def _calculate_contrast(image: Image.Image) -> dict[str, Any]:
    """Evaluate tonal separation using luminance standard deviation."""

    grayscale = image.convert("L")
    grayscale.thumbnail((1600, 1600))

    standard_deviation = ImageStat.Stat(grayscale).stddev[0]

    if 45 <= standard_deviation <= 75:
        score = 100
        status = "EXCELLENT"
    elif 35 <= standard_deviation < 45:
        score = 85
        status = "GOOD"
    elif 75 < standard_deviation <= 90:
        score = 82
        status = "HIGH"
    elif 25 <= standard_deviation < 35:
        score = 65
        status = "LOW"
    elif standard_deviation > 90:
        score = 60
        status = "VERY HIGH"
    else:
        score = 35
        status = "VERY LOW"

    return {
        "score": score,
        "status": status,
        "standard_deviation": round(
            standard_deviation,
            2,
        ),
    }


def _get_photo_status(quality_score: int) -> tuple[str, str]:
    """Translate the overall score into a user-facing recommendation."""

    if quality_score >= 90:
        return (
            "EXCELLENT",
            "READY FOR PREMIUM PRINTSKETCH",
        )

    if quality_score >= 80:
        return (
            "GOOD",
            "READY FOR PRINTSKETCH",
        )

    if quality_score >= 65:
        return (
            "ACCEPTABLE",
            "IMAGE IMPROVEMENT RECOMMENDED",
        )

    if quality_score >= 45:
        return (
            "POOR",
            "BETTER PHOTO RECOMMENDED",
        )

    return (
        "VERY POOR",
        "BETTER PHOTO REQUIRED",
    )


def analyze_image(image_path: str) -> dict[str, Any]:
    """
    Analyze the technical quality of a source photograph.

    This function performs local image analysis only.
    It does not identify the truck, model, text or accessories.
    """

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    try:
        with Image.open(path) as source_image:
            width, height = source_image.size
            image_format = source_image.format
            original_mode = source_image.mode

            # All quality calculations use a consistent RGB image.
            analysis_image = source_image.convert("RGB")

    except OSError as error:
        raise ValueError(
            f"Unable to open image: {image_path}"
        ) from error

    if width > height:
        orientation = "landscape"
    elif height > width:
        orientation = "portrait"
    else:
        orientation = "square"

    megapixels = round(
        (width * height) / 1_000_000,
        2,
    )

    file_size = round(
        path.stat().st_size / 1024,
        1,
    )

    aspect_ratio = round(
        width / height,
        2,
    )

    resolution_score = _calculate_resolution_score(
        width=width,
        height=height,
        megapixels=megapixels,
    )

    sharpness = _calculate_sharpness(
        analysis_image,
    )

    exposure = _calculate_exposure(
        analysis_image,
    )

    contrast = _calculate_contrast(
        analysis_image,
    )

    # Resolution and sharpness matter most because missing details
    # cannot be recovered reliably during SVG generation.
    technical_score = _clamp_score(
        resolution_score * 0.30
        + sharpness["score"] * 0.30
        + exposure["score"] * 0.20
        + contrast["score"] * 0.20
    )

    photo_status, recommendation = _get_photo_status(
        technical_score
    )

    return {
        # Existing keys kept for UI compatibility.
        "filename": path.name,
        "width": width,
        "height": height,
        "orientation": orientation,
        "megapixels": megapixels,
        "format": image_format,
        "mode": original_mode,
        "file_size_kb": file_size,
        "aspect_ratio": aspect_ratio,
        "quality_score": technical_score,
        "photo_status": photo_status,
        "recommendation": recommendation,

        # New Preview Quality Engine results.
        "resolution_score": resolution_score,
        "sharpness_score": sharpness["score"],
        "sharpness_status": sharpness["status"],
        "sharpness_edge_variance": sharpness[
            "edge_variance"
        ],
        "exposure_score": exposure["score"],
        "exposure_status": exposure["status"],
        "mean_brightness": exposure[
            "mean_brightness"
        ],
        "dark_pixels_percent": exposure[
            "dark_pixels_percent"
        ],
        "bright_pixels_percent": exposure[
            "bright_pixels_percent"
        ],
        "contrast_score": contrast["score"],
        "contrast_status": contrast["status"],
        "contrast_standard_deviation": contrast[
            "standard_deviation"
        ],
        "technical_score": technical_score,
    }


if __name__ == "__main__":
    print("Image analyzer ready.")