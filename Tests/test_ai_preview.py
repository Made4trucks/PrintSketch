import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "Studio"))

from ai_preview import generate_ai_preview


UPLOAD_FOLDER = PROJECT_ROOT / "Results" / "uploads"
OUTPUT_FOLDER = PROJECT_ROOT / "Results" / "ai_previews"


def find_newest_uploaded_image() -> Path:
    supported_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    images = [
        path
        for path in UPLOAD_FOLDER.iterdir()
        if path.is_file()
        and path.suffix.lower() in supported_extensions
    ]

    if not images:
        raise FileNotFoundError(
            "No source image found in Results/uploads."
        )

    return max(images, key=lambda path: path.stat().st_mtime)


def main() -> None:
    source_image = UPLOAD_FOLDER / "Scania_MyTruck.jpg"
    output_image = OUTPUT_FOLDER / "Test06_PrintabilityAdapter.png"

    test_prompt = """
Transform the uploaded truck photograph into a clean premium
black-and-white wall-art design.

Preserve the exact truck, camera angle, cab shape, grille,
headlights, mirrors, company markings, text and visible accessories.

Use only solid black and white.
No grayscale, shadows, gradients, textures or background.
Create bold, clean, printable geometry suitable as a future basis
for FDM 3D printing.

If the trailer does not contain essential identity elements, remove it from the composition and keep only the tractor unit. Focus the artwork on the truck cab.

The windshield and side windows are primary visual identity elements.

Keep all glass areas visually bright and clean.

Avoid filling the cabin interior behind the glass with solid black.

The interior should remain simplified but visually separated from the glass.

The viewer should clearly recognize the windshield and side windows as transparent glass.

Do not merge the rear wheel, chassis and fender into one solid black shape.

Decision hierarchy is critical.

When simplifying the artwork, always preserve elements according to the following priority:

1. Truck Identity
2. Company Identity
3. Owner Signatures

Owner signatures include personalized windshield names, truck model designation, registration plate, custom curtains and unique owner-installed accessories.

Remove only technical markings and visually insignificant details.

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

Preserve owner signatures such as personalized names, model designation, registration plate and custom curtains, but make them slightly larger or bolder when necessary for printability.

Keep the windshield and side windows bright and visually clean.

Do not merge wheels, fenders, chassis, steps or body panels into one solid black mass.

Prefer fewer strong printable shapes instead of many thin accurate details.

Before keeping any small detail, decide whether it would remain visible and printable at 200 mm with a 0.4 mm nozzle. If not, simplify or remove it.
"""

    print(f"Source image: {source_image}")
    print("Generating AI preview. This can take some time...")

    result_path = generate_ai_preview(
        source_image_path=source_image,
        prompt=test_prompt,
        output_path=output_image,
    )

    print("AI preview generated successfully.")
    print(f"Saved to: {result_path}")


if __name__ == "__main__":
    main()