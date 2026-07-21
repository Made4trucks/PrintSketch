from io import BytesIO

from nicegui import events, ui
from PIL import Image

from project import PrintSketchProject


def _set_app_status(state, text: str) -> None:
    app_status = state.get("app_status")
    if app_status is not None:
        app_status.set_text(text)


def create_left_panel(state, svg_checklist):
    checkboxes = {}

    def update_checklist_progress() -> None:
        completed = sum(
            1 for checkbox in checkboxes.values() if checkbox.value
        )
        total = len(svg_checklist)

        progress_label.set_text(f"Progress: {completed} / {total}")

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

    async def handle_upload(
        event: events.UploadEventArguments,
    ) -> None:
        image_bytes = await event.file.read()

        uploaded_image_path = (
            state["upload_folder"] / event.file.name
        )
        uploaded_image_path.write_bytes(image_bytes)

        project_name = (
            project_name_input.value.strip()
            if project_name_input.value
            else uploaded_image_path.stem
        )

        current_project = PrintSketchProject(project_name)
        current_project.create()
        current_project.import_photo(uploaded_image_path)

        state["uploaded_image_path"] = uploaded_image_path
        state["current_project"] = current_project

        image = Image.open(BytesIO(image_bytes))

        preview = state.get("preview")
        if preview is not None:
            preview.set_source(image)

        upload_status.set_text(
            f"Loaded: {event.file.name} | "
            f"{image.width} × {image.height}px"
        )

        refresh_dashboard = state.get("refresh_dashboard")
        if refresh_dashboard is not None:
            refresh_dashboard()

        _set_app_status(state, "📷 Image uploaded")
        ui.notify(
            "Image uploaded successfully.",
            type="positive",
        )

    with ui.column().classes(
        "w-[38%] min-w-[360px] gap-6"
    ):
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

            upload_status = ui.label(
                "No image uploaded."
            ).classes("text-sm text-gray-500")

        with ui.card().classes("w-full"):
            ui.label("Project Settings").classes(
                "text-xl font-semibold"
            )

            project_name_input = ui.input(
                label="Project name",
                placeholder="Example: Scania_KOOPS",
            ).classes("w-full")

            print_size_select = ui.select(
                ["150 mm", "175 mm", "200 mm", "225 mm"],
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
            ui.label(
                "SVG Preservation Checklist"
            ).classes("text-xl font-semibold")

            ui.label(
                "Verify that the final SVG preserves the "
                "customer's real vehicle identity."
            ).classes("text-sm text-gray-500")

            progress_label = ui.label(
                f"Progress: 0 / {len(svg_checklist)}"
            ).classes("font-semibold")

            checklist_status_label = ui.label(
                "🔴 Status: Incomplete"
            ).classes("text-sm font-semibold")

            for item in svg_checklist:
                checkboxes[item] = ui.checkbox(
                    item,
                    on_change=update_checklist_progress,
                )

    return {
        "upload_status": upload_status,
        "project_name_input": project_name_input,
        "print_size_select": print_size_select,
        "style_select": style_select,
        "identity_elements_input": identity_elements_input,
        "checkboxes": checkboxes,
        "progress_label": progress_label,
        "status_label": checklist_status_label,
    }
