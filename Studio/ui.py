from pathlib import Path

from nicegui import ui

from benchmark_lab import create_benchmark_lab
from components.footer import create_footer
from components.header import create_header
from components.layout import main_page, two_column_layout
from components.left_panel import create_left_panel
from components.right_panel import create_right_panel
from svg_checklist import SVG_CHECKLIST


PROJECT_ROOT = Path(__file__).resolve().parent.parent

state = {
    "upload_folder": PROJECT_ROOT / "Results" / "uploads",
    "prompt_folder": PROJECT_ROOT / "Results" / "prompts",
    "uploaded_image_path": None,
    "current_project": None,
    "last_generated_prompt": "",
    "last_image_analysis": "",
    "app_status": None,
    "preview": None,
    "generated_preview": None,
    "generated_preview_status": None,
    "dashboard_container": None,
    "refresh_dashboard": None,
}

state["upload_folder"].mkdir(parents=True, exist_ok=True)
state["prompt_folder"].mkdir(parents=True, exist_ok=True)

ui.page_title("PrintSketch Studio")

with main_page():
    create_header()

    with two_column_layout():
        left_refs = create_left_panel(
            state=state,
            svg_checklist=SVG_CHECKLIST,
        )

        right_refs = create_right_panel(
            state=state,
            left_refs=left_refs,
            benchmark_factory=create_benchmark_lab,
        )

state["preview"] = right_refs["preview"]
state["generated_preview"] = right_refs["generated_preview"]
state["generated_preview_status"] = right_refs["generated_status"]
state["dashboard_container"] = right_refs["dashboard_container"]
state["refresh_dashboard"] = right_refs["refresh_dashboard"]

state["app_status"] = create_footer()
state["refresh_dashboard"]()

ui.run(
    host="0.0.0.0",
    port=8081,
    reload=False,
    title="PrintSketch Studio",
    show=False,
)
