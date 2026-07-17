from nicegui import ui

from project_dashboard import get_project_status


def create_dashboard(context) -> None:
    """Display the current production status."""

    with ui.card().classes("w-full"):
        ui.label("Production Dashboard").classes(
            "text-xl font-semibold"
        )

        for stage, ready in get_project_status(context):
            symbol = "🟢" if ready else "⚪"
            ui.label(f"{symbol} {stage}")