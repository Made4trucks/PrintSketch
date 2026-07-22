import base64
import mimetypes
from pathlib import Path

from nicegui import ui


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_ROOT = PROJECT_ROOT / "Benchmark" / "Batch_01"
ORIGINALS_FOLDER = BENCHMARK_ROOT / "Originals"
CURRENT_RUN_FOLDER = max(
    (BENCHMARK_ROOT / "Runs").iterdir(),
    key=lambda p: p.stat().st_mtime,
)

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".webp"}

original_files = sorted(
    path
    for path in ORIGINALS_FOLDER.iterdir()
    if path.suffix.lower() in SUPPORTED_FORMATS
)

current_index = 0
original_image = None
current_image = None
case_label = None


def image_to_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def update_images() -> None:
    if not original_files:
        case_label.set_text("No benchmark images found.")
        return

    case = original_files[current_index]

    preview = (
        CURRENT_RUN_FOLDER
        / case.stem
        / "preview"
        / "preview_v1.png"
    )

    original_image.set_source(image_to_data_url(case))

    if preview.exists():
        current_image.set_source(image_to_data_url(preview))
    else:
        current_image.set_source("")

    case_label.set_text(
        f"{case.stem} ({current_index + 1}/{len(original_files)})"
    )


def previous_case() -> None:
    global current_index

    if not original_files:
        return

    current_index = (current_index - 1) % len(original_files)
    update_images()


def next_case() -> None:
    global current_index

    if not original_files:
        return

    current_index = (current_index + 1) % len(original_files)
    update_images()


def create_benchmark_lab() -> None:
    global original_image
    global current_image
    global case_label

    with ui.card().classes("w-full"):
        ui.label("Benchmark Lab").classes("text-2xl font-semibold")

        with ui.row().classes(
            "w-full flex-nowrap justify-center items-start gap-6"
        ):
            with ui.column().classes(
                "w-1/2 min-w-0 items-center gap-2"
            ):
                ui.label("ORIGINAL").classes("font-bold")

                original_image = ui.image().classes(
                    "w-full max-w-[560px] border rounded-lg"
                )

            with ui.column().classes(
                "w-1/2 min-w-0 items-center gap-2"
            ):
                ui.label(
                    f"CURRENT — {CURRENT_RUN_FOLDER.name}"
                ).classes("font-bold")
                
                current_image = ui.image().classes(
                    "w-full max-w-[560px] border rounded-lg"
                )

        with ui.row().classes(
            "w-full justify-between items-center mt-4"
        ):
            ui.button(
                "◀ Previous",
                on_click=previous_case,
            )

            case_label = ui.label().classes(
                "font-semibold text-lg"
            )

            ui.button(
                "Next ▶",
                on_click=next_case,
            )

    update_images()