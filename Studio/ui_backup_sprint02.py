
from io import BytesIO
from pathlib import Path
from nicegui import ui, run, events
from PIL import Image
from image_analyzer import analyze_image
from truck_identity import build_truck_identity
from identity_preservation import build_identity_preservation
from prompt_optimizer import calculate_prompt_quality, optimize_prompt
from prompt_builder import build_prompt
from ai_preview import generate_ai_preview
from svg_checklist import SVG_CHECKLIST
from export import export_prompt
from project_dashboard import get_project_status
from dashboard_component import create_dashboard
from project import PrintSketchProject
from production_pipeline import ProductionPipeline
from benchmark_lab import create_benchmark_lab




PROJECT_ROOT = Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = PROJECT_ROOT / "Results" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
PROMPT_FOLDER = PROJECT_ROOT / "Results" / "prompts"
PROMPT_FOLDER.mkdir(parents=True, exist_ok=True)

uploaded_image_path: Path | None = None

last_generated_prompt = ""
last_image_analysis = ""

preview = None
generated_preview = None
generated_preview_status = None
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
dashboard_container = None
current_project = None


async def handle_upload(event: events.UploadEventArguments) -> None:
    global uploaded_image_path
    global current_project

    image_bytes = await event.file.read()

    uploaded_image_path = UPLOAD_FOLDER / event.file.name
    uploaded_image_path.write_bytes(image_bytes)

    project_name = (
        project_name_input.value.strip()
        if project_name_input.value
        else uploaded_image_path.stem
)

    current_project = PrintSketchProject(project_name)
    current_project.create()

    current_project.import_photo(uploaded_image_path)

    

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

def load_generated_preview(image: Image.Image, status: str) -> None:
    generated_preview.set_source(image)

    generated_preview_status.set_text(status)

    app_status.set_text("🖼️ Generated preview loaded")
        
async def handle_generated_preview_upload(
    event: events.UploadEventArguments,
) -> None:
    image_bytes = await event.file.read()

    image = Image.open(BytesIO(image_bytes))

    load_generated_preview(
        image,
        f"Loaded preview: {event.file.name} | "
        f"{image.width} × {image.height}px",
    )

    ui.notify(
        "Generated preview uploaded successfully.",
        type="positive",
    )

def handle_analyze() -> None:
    global last_image_analysis
    global current_project

    if current_project is None:
        ui.notify(
            "Create or upload a project first.",
            type="warning",
        )
        return

    if uploaded_image_path is None:
        
        ui.notify(
            "Upload an image first.",
            type="warning",
        )
        return

    data = analyze_image(str(uploaded_image_path))

    last_image_analysis = (
    f"Filename: {data['filename']}\n\n"

    f"IMAGE INFORMATION\n"
    f"────────────────────────────\n"
    f"Resolution: {data['width']} × {data['height']} px\n"
    f"Orientation: {data['orientation']}\n"
    f"Megapixels: {data['megapixels']}\n"
    f"Format: {data['format']}\n"
    f"Color mode: {data['mode']}\n\n"

    f"TECHNICAL QUALITY\n"
    f"────────────────────────────\n"
    f"Resolution Score : {data['resolution_score']}/100\n"
    f"Sharpness        : {data['sharpness_score']}/100 ({data['sharpness_status']})\n"
    f"Exposure         : {data['exposure_score']}/100 ({data['exposure_status']})\n"
    f"Contrast         : {data['contrast_score']}/100 ({data['contrast_status']})\n\n"

    f"OVERALL RESULT\n"
    f"────────────────────────────\n"
    f"Technical Score : {data['technical_score']}/100\n"
    f"Photo Status    : {data['photo_status']}\n"
    f"Recommendation  : {data['recommendation']}"
)

    analysis_output.set_value(last_image_analysis)

    ui.notify(
        "Image analysis completed.",
        type="positive",
    )

    app_status.set_text("🔎 Image analyzed")
    

async def handle_run_pipeline() -> None:
    global current_project

    if current_project is None:
        ui.notify(
            "Upload a truck photo first.",
            type="warning",
        )
        return

    pipeline = ProductionPipeline(current_project)
    await run.io_bound(pipeline.run)
    
    preview_path = current_project.preview_folder / "preview_v1.png"
    generated_preview.set_source(Image.open(preview_path))

    refresh_dashboard()

    ui.notify(
        "Production pipeline finished.",
        type="positive",
    )

    app_status.set_text("⚙️ Pipeline finished")   

def refresh_dashboard() -> None:
    global dashboard_container
    global current_project

    if dashboard_container is None:
        return

    dashboard_container.clear()

    with dashboard_container:
        if current_project is None:
            with ui.card().classes("w-full"):
                ui.label("Production Dashboard").classes(
                    "text-xl font-semibold"
                )
                ui.label(
                    "Upload a truck photo to create a project."
                ).classes("text-sm text-gray-500")
            return

        create_dashboard(current_project.context)     

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
    global last_generated_prompt

    prompt = build_prompt()

    project_name = project_name_input.value or "Untitled Project"
    print_size = print_size_select.value or "200 mm"
    style = style_select.value or "Classic"

    identity_elements = (
        identity_elements_input.value.strip()
        if identity_elements_input.value
        else "No additional identity elements specified."
    )

    company_identity = [
        "Company logo",
        "Company name",
        "Fleet number",
        "Custom decals",
        "Model badges",
    ]

    truck_identity = [
        "Cab shape",
        "Roof type",
        "Sleeper cab",
        "Sun visor",
        "Side skirts",
        "Grille",
        "Headlights",
        "Bullbar",
        "Axle configuration",
        "Fuel tanks",
        "Roof lights",
        "Air horns",
        "Mirrors",
        "Exhaust stacks",
        "Beacon lights",
    ]

    identity_preservation_text = build_identity_preservation(
        company_identity=company_identity,
        truck_identity=truck_identity,
        additional_notes=identity_elements,
    )

    checklist_lines = []

    for item, checkbox in checklist_checkboxes.items():
        symbol = "✓" if checkbox.value else "X"
        checklist_lines.append(f"{symbol} {item}")

    checklist_text = "\n".join(checklist_lines)

    image_analysis_text = (
        last_image_analysis
        if last_image_analysis
        else "Image analysis has not been performed."
    )

    project_header = (
        f"PROJECT NAME: {project_name}\n"
        f"PRINT SIZE: {print_size}\n"
        f"STYLE: {style}\n\n"
        f"{identity_preservation_text}\n\n"
        f"IMAGE ANALYSIS:\n"
        f"{image_analysis_text}\n\n"
        f"SVG PRESERVATION CHECKLIST:\n"
        f"{checklist_text}\n"
    )

    raw_prompt = f"{project_header}\n{prompt}"

    optimization_result = optimize_prompt(raw_prompt)

    final_prompt = optimization_result["prompt"]
    quality_result = calculate_prompt_quality(final_prompt)

    prompt_output.set_value(final_prompt)
    ui.notify(
    (
        f"Prompt quality: {quality_result['score']}/100 "
        f"— {quality_result['rating']}. "
        f"Duplicates removed: "
        f"{optimization_result['duplicates_removed']}"
    ),
    type="positive",
)
    last_generated_prompt = final_prompt
    

    

    app_status.set_text("🛠️ Prompt assembled")


def handle_export_prompt() -> None:
    if not last_generated_prompt:
        ui.notify(
            "Build the prompt first.",
            type="warning",
        )
        return

    project_name = project_name_input.value or "Untitled Project"

    exported_file = export_prompt(
        project_name=project_name,
        prompt=last_generated_prompt,
        output_folder=PROMPT_FOLDER,
    )

    ui.notify(
        f"Prompt exported: {exported_file.name}",
        type="positive",
    )

    app_status.set_text("💾 Prompt exported")


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
        with ui.row().classes("w-full gap-4"):

            with ui.card().classes("w-1/2"):
                ui.label("Preview").classes(
                    "text-xl font-semibold"
                )

                preview = ui.image().classes(
                    "w-full max-h-[520px] object-contain "
                    "bg-gray-100 rounded"
                )
            with ui.card().classes("w-1/2"):
                ui.label("Generated Preview").classes(
                    "text-xl font-semibold"
                )

                ui.label(
                    "Upload an artwork generated from the exported prompt."
                ).classes(
                    "text-sm text-gray-500"
                )

                ui.upload(
                    label="Upload generated preview",
                    on_upload=handle_generated_preview_upload,
                    auto_upload=True,
                ).props(
                    'accept=".jpg,.jpeg,.png,.webp"'
                ).classes("w-full")

                generated_preview_status = ui.label(
                    "No generated preview uploaded."
                ).classes(
                    "text-sm text-gray-500"
                )

                generated_preview = ui.image().classes(
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

                ui.button(
                    "Run Production Pipeline",
                    on_click=handle_run_pipeline,
                    icon="play_arrow",
                ).classes("w-full")

                dashboard_container = ui.column().classes("w-full")
                create_benchmark_lab()

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

            ui.button(
                "Export Prompt",
                on_click=handle_export_prompt,
                icon="save",
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
refresh_dashboard()

ui.run(
    host="0.0.0.0",
    port=8081,
    reload=False,
    title="PrintSketch Studio",
    show=False,
)
