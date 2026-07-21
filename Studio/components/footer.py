from nicegui import ui


def create_footer():
    with ui.footer(fixed=True).classes(
        "justify-between items-center bg-gray-900 text-white px-6"
    ):
        ui.label("PrintSketch Studio v2.0").classes("text-sm")
        app_status = ui.label("🟢 Ready").classes("font-bold")
    return app_status
