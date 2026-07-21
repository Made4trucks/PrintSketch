from io import BytesIO

from nicegui import events, run, ui
from PIL import Image

from dashboard_component import create_dashboard
from export import export_prompt
from identity_preservation import build_identity_preservation
from image_analyzer import analyze_image
from production_pipeline import ProductionPipeline
from prompt_compiler import PromptCompiler
from prompt_optimizer import calculate_prompt_quality, optimize_prompt


def _set_app_status(state, text: str) -> None:
    app_status = state.get("app_status")
    if app_status is not None:
        app_status.set_text(text)


def create_right_panel(
    state,
    left_refs,
    benchmark_factory,
):
    def refresh_dashboard() -> None:
        dashboard_container.clear()

        with dashboard_container:
            current_project = state.get("current_project")

            if current_project is None:
                with ui.card().classes("w-full"):
                    ui.label(
                        "Production Dashboard"
                    ).classes("text-xl font-semibold")

                    ui.label(
                        "Upload a truck photo to create "
                        "a project."
                    ).classes("text-sm text-gray-500")
                return

            create_dashboard(current_project.context)

    async def handle_generated_preview_upload(
        event: events.UploadEventArguments,
    ) -> None:
        image_bytes = await event.file.read()
        image = Image.open(BytesIO(image_bytes))

        generated_preview.set_source(image)
        generated_status.set_text(
            f"Loaded preview: {event.file.name} | "
            f"{image.width} × {image.height}px"
        )

        _set_app_status(
            state,
            "🖼️ Generated preview loaded",
        )

        ui.notify(
            "Generated preview uploaded successfully.",
            type="positive",
        )

    def handle_analyze() -> None:
        current_project = state.get("current_project")
        uploaded_image_path = state.get(
            "uploaded_image_path"
        )

        if (
            current_project is None
            or uploaded_image_path is None
        ):
            ui.notify(
                "Upload an image first.",
                type="warning",
            )
            return

        data = analyze_image(str(uploaded_image_path))

        last_image_analysis = (
            f"Filename: {data['filename']}\n\n"
            "IMAGE INFORMATION\n"
            "────────────────────────────\n"
            f"Resolution: {data['width']} × "
            f"{data['height']} px\n"
            f"Orientation: {data['orientation']}\n"
            f"Megapixels: {data['megapixels']}\n"
            f"Format: {data['format']}\n"
            f"Color mode: {data['mode']}\n\n"
            "TECHNICAL QUALITY\n"
            "────────────────────────────\n"
            f"Resolution Score : "
            f"{data['resolution_score']}/100\n"
            f"Sharpness        : "
            f"{data['sharpness_score']}/100 "
            f"({data['sharpness_status']})\n"
            f"Exposure         : "
            f"{data['exposure_score']}/100 "
            f"({data['exposure_status']})\n"
            f"Contrast         : "
            f"{data['contrast_score']}/100 "
            f"({data['contrast_status']})\n\n"
            "OVERALL RESULT\n"
            "────────────────────────────\n"
            f"Technical Score : "
            f"{data['technical_score']}/100\n"
            f"Photo Status    : "
            f"{data['photo_status']}\n"
            f"Recommendation  : "
            f"{data['recommendation']}"
        )

        state["last_image_analysis"] = (
            last_image_analysis
        )
        analysis_output.set_value(
            last_image_analysis
        )

        _set_app_status(state, "🔎 Image analyzed")
        ui.notify(
            "Image analysis completed.",
            type="positive",
        )

    async def handle_run_pipeline() -> None:
        current_project = state.get("current_project")

        if current_project is None:
            ui.notify(
                "Upload a truck photo first.",
                type="warning",
            )
            return

        pipeline = ProductionPipeline(current_project)
        await run.io_bound(pipeline.run)

        preview_path = (
            current_project.preview_folder
            / "preview_v1.png"
        )

        if preview_path.exists():
            generated_preview.set_source(
                Image.open(preview_path)
            )
            generated_status.set_text(
                f"Pipeline result: {preview_path.name}"
            )

        refresh_dashboard()
        _set_app_status(
            state,
            "⚙️ Pipeline finished",
        )

        ui.notify(
            "Production pipeline finished.",
            type="positive",
        )

    def handle_build_prompt() -> None:
        prompt = PromptCompiler().compile()

        project_name = (
            left_refs["project_name_input"].value
            or "Untitled Project"
        )
        print_size = (
            left_refs["print_size_select"].value
            or "200 mm"
        )
        style = (
            left_refs["style_select"].value
            or "Classic"
        )

        identity_input = left_refs[
            "identity_elements_input"
        ]
        identity_elements = (
            identity_input.value.strip()
            if identity_input.value
            else (
                "No additional identity elements "
                "specified."
            )
        )

        identity_preservation_text = (
            build_identity_preservation(
                company_identity=[
                    "Company logo",
                    "Company name",
                    "Fleet number",
                    "Custom decals",
                    "Model badges",
                ],
                truck_identity=[
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
                ],
                additional_notes=identity_elements,
            )
        )

        checklist_text = "\n".join(
            (
                f"{'✓' if checkbox.value else 'X'} "
                f"{item}"
            )
            for item, checkbox in left_refs[
                "checkboxes"
            ].items()
        )

        image_analysis_text = (
            state.get("last_image_analysis")
            or "Image analysis has not been performed."
        )

        project_header = (
            f"PROJECT NAME: {project_name}\n"
            f"PRINT SIZE: {print_size}\n"
            f"STYLE: {style}\n\n"
            f"{identity_preservation_text}\n\n"
            "IMAGE ANALYSIS:\n"
            f"{image_analysis_text}\n\n"
            "SVG PRESERVATION CHECKLIST:\n"
            f"{checklist_text}\n"
        )

        optimization_result = optimize_prompt(
            f"{project_header}\n{prompt}"
        )

        final_prompt = optimization_result["prompt"]
        quality_result = calculate_prompt_quality(
            final_prompt
        )

        prompt_output.set_value(final_prompt)
        state["last_generated_prompt"] = final_prompt

        _set_app_status(
            state,
            "🛠️ Prompt assembled",
        )

        ui.notify(
            (
                f"Prompt quality: "
                f"{quality_result['score']}/100 "
                f"— {quality_result['rating']}. "
                f"Duplicates removed: "
                f"{optimization_result['duplicates_removed']}"
            ),
            type="positive",
        )

    def handle_export_prompt() -> None:
        last_generated_prompt = state.get(
            "last_generated_prompt"
        )

        if not last_generated_prompt:
            ui.notify(
                "Build the prompt first.",
                type="warning",
            )
            return

        project_name = (
            left_refs["project_name_input"].value
            or "Untitled Project"
        )

        exported_file = export_prompt(
            project_name=project_name,
            prompt=last_generated_prompt,
            output_folder=state["prompt_folder"],
        )

        _set_app_status(state, "💾 Prompt exported")
        ui.notify(
            f"Prompt exported: {exported_file.name}",
            type="positive",
        )

    with ui.column().classes(
        "flex-1 min-w-0 gap-6"
    ):
        with ui.card().classes("w-full"):
            ui.label(
                "Preview Comparison"
            ).classes("text-xl font-semibold")

            with ui.row().classes(
                "w-full gap-4 items-stretch no-wrap"
            ):
                with ui.column().classes(
                    "w-1/2 min-w-0"
                ):
                    ui.label("Original").classes(
                        "font-semibold"
                    )
                    preview = ui.image().classes(
                        "w-full h-[520px] object-contain "
                        "bg-gray-100 rounded"
                    )

                with ui.column().classes(
                    "w-1/2 min-w-0"
                ):
                    ui.label("Generated").classes(
                        "font-semibold"
                    )

                    ui.upload(
                        label="Upload generated preview",
                        on_upload=(
                            handle_generated_preview_upload
                        ),
                        auto_upload=True,
                    ).props(
                        'accept=".jpg,.jpeg,.png,.webp"'
                    ).classes("w-full")

                    generated_status = ui.label(
                        "No generated preview uploaded."
                    ).classes("text-sm text-gray-500")

                    generated_preview = ui.image().classes(
                        "w-full h-[520px] object-contain "
                        "bg-gray-100 rounded"
                    )

        with ui.card().classes("w-full"):
            ui.label("Image Analysis").classes(
                "text-xl font-semibold"
            )

            with ui.row().classes("w-full gap-3"):
                ui.button(
                    "Analyze Image",
                    on_click=handle_analyze,
                    icon="search",
                ).classes("flex-1")

                ui.button(
                    "Run Production Pipeline",
                    on_click=handle_run_pipeline,
                    icon="play_arrow",
                ).classes("flex-1")

            dashboard_container = ui.column().classes(
                "w-full"
            )

            analysis_output = ui.textarea(
                label="Analysis result"
            ).props("readonly").classes(
                "w-full min-h-[260px]"
            )

        benchmark_factory()

        with ui.card().classes("w-full"):
            ui.label("Prompt Builder").classes(
                "text-xl font-semibold"
            )

            with ui.row().classes("w-full gap-3"):
                ui.button(
                    "Build Prompt",
                    on_click=handle_build_prompt,
                    icon="build",
                ).classes("flex-1")

                ui.button(
                    "Export Prompt",
                    on_click=handle_export_prompt,
                    icon="save",
                ).classes("flex-1")

            prompt_output = ui.textarea(
                label="Assembled prompt"
            ).props("readonly").classes(
                "w-full min-h-[360px]"
            )

    return {
        "preview": preview,
        "generated_preview": generated_preview,
        "generated_status": generated_status,
        "dashboard_container": dashboard_container,
        "analysis_output": analysis_output,
        "prompt_output": prompt_output,
        "refresh_dashboard": refresh_dashboard,
    }
