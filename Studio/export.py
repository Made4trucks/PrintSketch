from pathlib import Path


def export_prompt(
    project_name: str,
    prompt: str,
    output_folder: Path,
) -> Path:
    """
    Save assembled prompt to a text file.

    Returns:
        Path to the exported file.
    """

    safe_name = project_name.strip()

    if not safe_name:
        safe_name = "Untitled_Project"

    safe_name = safe_name.replace(" ", "_")

    output_file = output_folder / f"{safe_name}_prompt.txt"

    output_file.write_text(
        prompt,
        encoding="utf-8",
    )

    return output_file