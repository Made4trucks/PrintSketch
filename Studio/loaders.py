from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENGINE_FOLDER = PROJECT_ROOT / "Engine"

PROMPT_FOLDER = PROJECT_ROOT / "Prompts"

PROMPT_MODULE_FOLDER = (
    PROMPT_FOLDER
    / "Prompt_Classic_v1.1_modules"
)


def load_text_file(
    file_path: Path,
    *,
    required: bool = True,
) -> str:
    """Load a UTF-8 text file."""

    if not file_path.exists():

        if required:
            raise FileNotFoundError(
                f"Required prompt module not found: {file_path}"
            )

        return ""

    return file_path.read_text(
        encoding="utf-8"
    ).strip()


def load_engine_modules(
    filenames: list[str],
) -> str:
    """Load and join selected Engine modules."""

    modules: list[str] = []

    for filename in filenames:

        content = load_text_file(
            ENGINE_FOLDER / filename,
            required=False,
        )

        if content:
            modules.append(content)

    return "\n\n---\n\n".join(modules)


def load_prompt_modules(
    filenames: list[str],
) -> str:
    """Load and join Prompt modules."""

    modules: list[str] = []

    for filename in filenames:

        content = load_text_file(
            PROMPT_MODULE_FOLDER / filename
        )

        if content:
            modules.append(content)

    return "\n\n---\n\n".join(modules)


def load_identity_map(
    identity_map_path: Path | None,
) -> str:
    """Load approved vehicle identity map."""

    if identity_map_path is None:
        return (
            "No approved vehicle-specific identity map "
            "was supplied."
        )

    return load_text_file(identity_map_path)