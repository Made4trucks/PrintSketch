from nicegui import ui


def create_header() -> None:
    with ui.row().classes("w-full items-center justify-between"):
        with ui.column().classes("gap-0"):
            ui.label("🚛 PrintSketch Studio").classes("text-3xl font-bold")
            ui.label("Professional 3D Truck Wall Art").classes("text-lg text-gray-500")
        ui.badge("READY", color="green").classes("text-sm px-4 py-2")
