
from io import BytesIO
from pathlib import Path

from nicegui import events, ui
from PIL import Image

from image_analyzer import analyze_image
from prompt_builder import build_prompt
from svg_checklist import SVG_CHECKLIST


PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = PROJECT_ROOT / "Results" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

uploaded_image_path: Path | None = None

preview = None
status_label = None
analysis_output = None
prompt_output = None
project_name_input = None
print_size_select = None
style_select = None
identity_elements_input = None
checklist_checkboxes = {}
checklist_progress_label = None
checklist_status_label = None
app_status = None


async def handle_upload(event: events.UploadEventArguments) -> None:
    global uploaded_image_path

    image_bytes = await event.file.read()

    uploaded_image_path = UPLOAD_FOLDER / event.file.name
    uploaded_image_path.write_bytes(image_bytes)

    image = Image.open(BytesIO(image_bytes))
    preview.set_source(image)

    status_label.set_text(
        f"Loaded: {event.file.name} | "
        f"{image.width} × {image.height}px"
    )

    ui.notify(
        "Image uploaded successfully.",
        type="positive",
    )

    app_status.set_text("📷 Image uploaded")


def handle_analyze() -> None:
    if uploaded_image_path is None:
        ui.notify(
            "Upload an image first.",
            type="warning",
        )
        return

    data = analyze_image(str(uploaded_image_path))

    analysis_output.set_value(
        f"Filename: {data['filename']}\n"
        f"Resolution: {data['width']} × {data['height']} px\n"
        f"Orientation: {data['orientation']}\n"
        f"Megapixels: {data['megapixels']}\n"
        f"Quality Score: {data['quality_score']}/100\n"
        f"Photo Status: {data['photo_status']}\n"
        f"Recommendation: {data['recommendation']}\n"
        f"Format: {data['format']}\n"
        f"Color mode: {data['mode']}"
    )

    ui.notify(
        "Image analysis completed.",
        type="positive",
    )

    app_status.set_text("🔎 Image analyzed")

def update_checklist_progress() -> None:
    completed = sum(
        1
        for checkbox in checklist_checkboxes.values()
        if checkbox.value
    )

    total = len(SVG_CHECKLIST)

    checklist_progress_label.set_text(
        f"Progress: {completed} / {total}"
    )

    if completed == total:
        checklist_status_label.set_text(
            "🟢 Status: Ready for SVG Production"
        )
    elif completed >= total // 2:
        checklist_status_label.set_text(
            "🟡 Status: Review Required"
        )
    else:
        checklist_status_label.set_text(
            "🔴 Status: Incomplete"
        )
def handle_build_prompt() -> None:
    prompt = build_prompt()

    project_name = project_name_input.value or "Untitled Project"
    print_size = print_size_select.value or "200 mm"
    style = style_select.value or "Classic"

    identity_elements = (
        identity_elements_input.value.strip()
        if identity_elements_input.value
        else "No additional identity elements specified."
    )

    checklist_lines = []

    for item, checkbox in checklist_checkboxes.items():
        symbol = "✓" if checkbox.value else "✗"
        checklist_lines.append(f"{symbol} {item}")

    checklist_text = "\n".join(checklist_lines)

    project_header = (
        f"PROJECT NAME: {project_name}\n"
        f"PRINT SIZE: {print_size}\n"
        f"STYLE: {style}\n"
        f"IMPORTANT IDENTITY ELEMENTS:\n"
        f"{identity_elements}\n\n"
        f"SVG PRESERVATION CHECKLIST:\n"
        f"{checklist_text}\n"
    )

    final_prompt = f"{project_header}\n{prompt}"

    prompt_output.set_value(final_prompt)

    ui.notify(
        "Prompt assembled successfully.",
        type="positive",
    )

    app_status.set_text("🛠️ Prompt assembled")


ui.page_title("PrintSketch Studio")

with ui.column().classes("w-full max-w-7xl mx-auto p-6 gap-6"):
    with ui.row().classes("w-full items-center justify-between"):
        with ui.column().classes("gap-0"):
            ui.label("🚛 PrintSketch Studio").classes(
                "text-3xl font-bold"
            )

            ui.label("Professional 3D Truck Wall Art").classes(
                "text-lg text-gray-500"
            )

        ui.badge("READY", color="green").classes(
            "text-sm px-4 py-2"
        )

    with ui.row().classes("w-full gap-6 items-start"):
        with ui.column().classes("w-full lg:w-1/2 gap-6"):
            with ui.card().classes("w-full"):
                ui.label("Truck Photo").classes(
                    "text-xl font-semibold"
                )

                ui.upload(
                    label="Upload truck image",
                    on_upload=handle_upload,
                    auto_upload=True,
                ).props(
                    'accept=".jpg,.jpeg,.png,.webp"'
                ).classes("w-full")

                status_label = ui.label(
                    "No image uploaded."
                ).classes(
                    "text-sm text-gray-500"
                )

            with ui.card().classes("w-full"):
                ui.label("Preview").classes(
                    "text-xl font-semibold"
                )

                preview = ui.image().classes(
                    "w-full max-h-[520px] object-contain "
                    "bg-gray-100 rounded"
                )

        with ui.column().classes("w-full lg:w-1/2 gap-6"):
            with ui.card().classes("w-full"):
                ui.label("Project Settings").classes(
                    "text-xl font-semibold"
                )

                project_name_input = ui.input(
                    label="Project name",
                    placeholder="Example: Scania_KOOPS",
                ).classes("w-full")

                print_size_select = ui.select(
                    [
                        "150 mm",
                        "175 mm",
                        "200 mm",
                        "225 mm",
                    ],
                    value="200 mm",
                    label="Print size",
                ).classes("w-full")

                style_select = ui.select(
                    ["Classic"],
                    value="Classic",
                    label="Style",
                ).classes("w-full")

                identity_elements_input = ui.textarea(
                    label="Important identity elements",
                    placeholder=(
                        "Example:\n"
                        "- KOOPS visor text\n"
                        "- orange grille lights\n"
                        "- R420 badge\n"
                        "- red wheel hubs\n"
                        "- keep trailer"
                    ),
                ).classes("w-full")

            with ui.card().classes("w-full"):
                ui.label("SVG Preservation Checklist").classes(
                    "text-xl font-semibold"
                )

                ui.label(
                    "Verify that the final SVG preserves "
                    "the customer's real vehicle identity."
                ).classes(
                    "text-sm text-gray-500"
                )

                checklist_progress_label = ui.label(
                    f"Progress: 0 / {len(SVG_CHECKLIST)}"
                ).classes(
                    "font-semibold"
                )

                for item in SVG_CHECKLIST:
                    checklist_checkboxes[item] = ui.checkbox(
                        item,
                        on_change=lambda event: update_checklist_progress(),
                    )

            with ui.card().classes("w-full"):
                ui.label("Image Analysis").classes(
                    "text-xl font-semibold"
                )

                ui.button(
                    "Analyze Image",
                    on_click=handle_analyze,
                    icon="search",
                ).classes("w-full")

                analysis_output = ui.textarea(
                    label="Analysis result"
                ).props(
                    "readonly"
                ).classes("w-full")

            with ui.card().classes("w-full"):
                ui.label("Prompt Builder").classes(
                    "text-xl font-semibold"
                )

                ui.button(
                    "Build Prompt",
                    on_click=handle_build_prompt,
                    icon="build",
                ).classes("w-full")

                prompt_output = ui.textarea(
                    label="Assembled prompt"
                ).props(
                    "readonly"
                ).classes(
                    "w-full h-64"
                )


with ui.footer(fixed=True).classes(
    "justify-between items-center "
    "bg-gray-900 text-white px-6"
):
    ui.label("PrintSketch Studio v1.0").classes(
        "text-sm"
    )

    app_status = ui.label("🟢 Ready").classes(
        "font-bold"
    )


ui.run(
    host="0.0.0.0",
    port=8080,
    reload=False,
    title="PrintSketch Studio",
)
