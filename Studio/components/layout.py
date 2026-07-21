from nicegui import ui


def main_page():
    return ui.column().classes(
        "w-full max-w-[1800px] mx-auto px-6 pt-6 pb-20 gap-6"
    )


def two_column_layout():
    return ui.row().classes("w-full gap-6 items-start no-wrap")


def left_column():
    return ui.column().classes("w-[38%] min-w-[360px] gap-6")


def right_column():
    return ui.column().classes("flex-1 min-w-0 gap-6")
