def get_project_status(context) -> list[tuple[str, bool]]:
    """
    Returns the current production status of the project.
    """

    return [

        (
            "Technical Analysis",
            True,
        ),

        (
            "Vision Report",
            (
                context.vision_folder
                / "vision_report.json"
            ).exists(),
        ),

        (
            "PrintSketch Readiness",
            (
                context.vision_folder
                / "readiness_report.json"
            ).exists(),
        ),

        (
            "Identity Map",
            (
                context.identity_folder
                / "approved_identity.json"
            ).exists(),
        ),

        (
            "Production Prompt",
            (
                context.prompt_folder
                / "assembled_prompt.txt"
            ).exists(),
        ),

        (
            "Preview",
            (
                context.preview_folder
                / "preview.png"
            ).exists(),
        ),

        (
            "SVG",
            (
                context.svg_folder
                / "truck.svg"
            ).exists(),
        ),

        (
            "Fusion",
            (
                context.fusion_folder
                / "truck.f3d"
            ).exists(),
        ),

        (
            "STL Export",
            (
                context.exports_folder
                / "truck.stl"
            ).exists(),
        ),

    ]