import json
from pathlib import Path
from typing import Any


RATING_SCORES = {
    "excellent": 100,
    "good": 85,
    "acceptable": 65,
    "poor": 35,
}


def _clamp_score(score: float) -> int:
    """Keep a numeric score inside the 0–100 range."""

    return max(0, min(100, round(score)))


def _rating_to_score(value: Any) -> int:
    """Convert a Vision rating into a numeric score."""

    normalized_value = str(value or "").strip().lower()

    return RATING_SCORES.get(
        normalized_value,
        50,
    )


def _boolean_score(
    value: Any,
    true_score: int = 100,
    false_score: int = 0,
) -> int:
    """Convert a boolean observation into a score."""

    if value is True:
        return true_score

    if value is False:
        return false_score

    return 50


def _calculate_truck_size_score(
    coverage_percent: Any,
) -> int:
    """
    Evaluate how much of the photograph is occupied by the truck.

    A truck that is too small loses identity detail.
    A truck that fills almost the entire image may be cropped.
    """

    try:
        coverage = float(coverage_percent)
    except (TypeError, ValueError):
        return 50

    if 55 <= coverage <= 85:
        return 100

    if 45 <= coverage < 55:
        return 85

    if 85 < coverage <= 92:
        return 85

    if 35 <= coverage < 45:
        return 65

    if 92 < coverage <= 97:
        return 60

    if 25 <= coverage < 35:
        return 45

    if coverage > 97:
        return 30

    return 25


def _calculate_visibility_score(
    observations: dict[str, Any],
) -> int:
    """Evaluate visibility of important truck geometry."""

    visibility_values = [
        _boolean_score(
            observations.get("cab_fully_visible")
        ),
        _boolean_score(
            observations.get("front_fully_visible")
        ),
        _boolean_score(
            observations.get("roof_fully_visible")
        ),
        _boolean_score(
            observations.get("bumper_fully_visible")
        ),
        _boolean_score(
            observations.get("left_mirror_visible")
        ),
        _boolean_score(
            observations.get("right_mirror_visible")
        ),
        _boolean_score(
            observations.get("grille_clearly_visible")
        ),
        _boolean_score(
            observations.get("headlights_clearly_visible")
        ),
    ]

    return _clamp_score(
        sum(visibility_values) / len(visibility_values)
    )


def _calculate_identity_score(
    observations: dict[str, Any],
) -> int:
    """Evaluate how well truck identity can be preserved."""

    visual_identity_score = _rating_to_score(
        observations.get("identity_visibility")
    )

    text_scores = [
        _boolean_score(
            observations.get("brand_text_readable"),
            true_score=100,
            false_score=35,
        ),
        _boolean_score(
            observations.get("model_text_readable"),
            true_score=100,
            false_score=45,
        ),
        _boolean_score(
            observations.get("company_text_readable"),
            true_score=100,
            false_score=60,
        ),
        _boolean_score(
            observations.get("license_plate_readable"),
            true_score=100,
            false_score=75,
        ),
    ]

    average_text_score = (
        sum(text_scores) / len(text_scores)
    )

    return _clamp_score(
        visual_identity_score * 0.65
        + average_text_score * 0.35
    )


def _calculate_obstruction_score(
    observations: dict[str, Any],
) -> int:
    """Evaluate whether objects block important truck details."""

    obstructions_present = observations.get(
        "obstructions_present"
    )

    obstruction_list = observations.get(
        "obstructions",
        [],
    )

    if obstructions_present is False:
        return 100

    if obstructions_present is not True:
        return 60

    if not isinstance(obstruction_list, list):
        return 45

    obstruction_count = len(obstruction_list)

    if obstruction_count == 0:
        return 65

    if obstruction_count == 1:
        return 55

    if obstruction_count == 2:
        return 35

    return 20


def _calculate_background_score(
    observations: dict[str, Any],
) -> int:
    """Evaluate how difficult background removal may be."""

    background_complexity = str(
        observations.get(
            "background_complexity",
            "",
        )
    ).strip().lower()

    scores = {
        "low": 100,
        "medium": 75,
        "high": 45,
    }

    return scores.get(
        background_complexity,
        60,
    )


def _get_readiness_status(
    score: int,
) -> tuple[str, str]:
    """Create an internal production recommendation."""

    if score >= 90:
        return (
            "EXCELLENT",
            "READY FOR PREMIUM PRODUCTION",
        )

    if score >= 80:
        return (
            "GOOD",
            "READY FOR PRODUCTION",
        )

    if score >= 65:
        return (
            "ACCEPTABLE",
            "MANUAL REVIEW RECOMMENDED",
        )

    if score >= 45:
        return (
            "POOR",
            "BETTER SOURCE PHOTO RECOMMENDED",
        )

    return (
        "NOT READY",
        "BETTER SOURCE PHOTO REQUIRED",
    )


def calculate_printsketch_readiness(
    vision_report: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate PrintSketch production readiness.

    The function does not analyze the image directly.
    It uses observations already created by Vision Analysis.
    """

    observations = vision_report.get(
        "readiness_observations",
        {},
    )

    if not isinstance(observations, dict):
        observations = {}

    truck_size_score = _calculate_truck_size_score(
        observations.get(
            "truck_frame_coverage_percent"
        )
    )

    visibility_score = _calculate_visibility_score(
        observations
    )

    identity_score = _calculate_identity_score(
        observations
    )

    perspective_score = _rating_to_score(
        observations.get(
            "perspective_suitability"
        )
    )

    crop_score = _rating_to_score(
        observations.get(
            "crop_quality"
        )
    )

    obstruction_score = _calculate_obstruction_score(
        observations
    )

    background_score = _calculate_background_score(
        observations
    )

    readiness_score = _clamp_score(
        truck_size_score * 0.15
        + visibility_score * 0.25
        + identity_score * 0.25
        + perspective_score * 0.15
        + crop_score * 0.10
        + obstruction_score * 0.07
        + background_score * 0.03
    )

    status, recommendation = _get_readiness_status(
        readiness_score
    )

    return {
        "truck_size_score": truck_size_score,
        "visibility_score": visibility_score,
        "identity_score": identity_score,
        "perspective_score": perspective_score,
        "crop_score": crop_score,
        "obstruction_score": obstruction_score,
        "background_score": background_score,
        "printsketch_readiness_score": readiness_score,
        "status": status,
        "recommendation": recommendation,
    }


def create_readiness_report(
    vision_report_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    """Read the Vision Report and save a readiness report."""

    if not vision_report_path.exists():
        raise FileNotFoundError(
            f"Vision Report does not exist: "
            f"{vision_report_path}"
        )

    try:
        vision_report = json.loads(
            vision_report_path.read_text(
                encoding="utf-8"
            )
        )
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Vision Report contains invalid JSON: "
            f"{vision_report_path}"
        ) from error

    readiness_report = calculate_printsketch_readiness(
        vision_report
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            readiness_report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return readiness_report


if __name__ == "__main__":
    print("PrintSketch Readiness Engine ready.")