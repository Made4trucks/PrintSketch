import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Studio"))

from ai_preview import generate_ai_preview


SOURCE_IMAGE = (
    PROJECT_ROOT
    / "Results"
    / "uploads"
    / "Scania_MyTruck.jpg"
)

PROMPT_FILE = (
    PROJECT_ROOT
    / "Results"
    / "prompts"
    / "Scania_MyTruck_prompt.txt"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "Results"
    / "ai_previews"
    / "TestA_FullPrompt_ImageAPI.png"
)


def main() -> None:
    if not SOURCE_IMAGE.exists():
        raise FileNotFoundError(
            f"Source image not found: {SOURCE_IMAGE}"
        )

    if not PROMPT_FILE.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {PROMPT_FILE}"
        )

    prompt = PROMPT_FILE.read_text(
        encoding="utf-8"
    ).strip()

    print(f"Source image: {SOURCE_IMAGE}")
    print(f"Prompt file: {PROMPT_FILE}")
    print("Generating Test A with the full PrintSketch prompt...")

    result_path = generate_ai_preview(
        source_image_path=SOURCE_IMAGE,
        prompt=prompt,
        output_path=OUTPUT_FILE,
    )

    print("Test A generated successfully.")
    print(f"Saved to: {result_path}")


if __name__ == "__main__":
    main()