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
    / "TestA3_IdentityLayout.png"
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
    printability_adapter = """
PRINTABILITY ADAPTER

This artwork must represent geometry that can realistically be converted into an FDM-printable design.

Target production:
- Printer: Bambu Lab P1S
- Nozzle: 0.4 mm
- Final artwork size: approximately 200 mm
- Minimum reliable line width: 0.6 mm

Use bold, continuous and clearly separated geometry.

Remove or strongly simplify:
- seat outlines and cabin-interior details behind the glass
- dashboard details
- tiny stickers and technical labels
- narrow decorative stripes
- dense grille meshes
- tiny grille openings
- internal reflector details inside lights
- lines that would disappear after slicing

Preserve owner-specific identity elements such as personalized names, model designation, registration plate and custom curtains whenever they remain printable.

Keep the windshield and side windows bright and visually clean.

Do not merge wheels, fenders, chassis, steps or body panels into one solid black mass.

Prefer fewer strong printable shapes instead of many thin accurate details.

Before keeping any small detail, decide whether it would remain visible and printable at 200 mm with a 0.4 mm nozzle. If not, simplify or remove it.
"""

    prompt = f"{prompt}\n\n{printability_adapter}"

    identity_layout_adapter = """
IDENTITY LAYOUT AND PRINTABILITY

Preserve the exact original location of all identity markings.

Do not mirror, relocate or move:
- model designation
- registration plate
- owner names
- company branding
- identity stickers

Preserve the exact visible model designation, including its original side and placement.

Preserve the original outer arrangement of auxiliary grille lights.
If six lights form a pyramid or another distinctive pattern, keep that exact arrangement.
Simplify only the internal details of each light.

Replace dense grille mesh with a few bold, clean and printable openings.
Do not generate tiny repeated mesh cells.

Windshield names and personalized lettering must remain bold, solid black and printable.
Avoid thin decorative script when it would not survive printing.

For small decorative labels such as "Since 1961", preserve only the main readable identity element when the smaller words would become unreadable.
Remove micro-text and tiny decorative marks.
"""

    prompt = f"{prompt}\n\n{identity_layout_adapter}"

    print(f"Source image: {SOURCE_IMAGE}")
    print(f"Prompt file: {PROMPT_FILE}")
    print("Generating Test A3 with Identity Layout Adapter...")

    result_path = generate_ai_preview(
        source_image_path=SOURCE_IMAGE,
        prompt=prompt,
        output_path=OUTPUT_FILE,
    )

    print("Test A3 generated successfully.")
    print(f"Saved to: {result_path}")


if __name__ == "__main__":
    main()