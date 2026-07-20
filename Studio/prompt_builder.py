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
    """Load and join selected Prompt v1.1 modules."""

    modules: list[str] = []

    for filename in filenames:
        content = load_text_file(
            PROMPT_MODULE_FOLDER / filename
        )

        if content:
            modules.append(content)

    return "\n\n---\n\n".join(modules)


def load_prompt_template() -> str:
    prompt_file = (
        PROMPT_FOLDER
        / "Prompt_Classic_v1.0_FINAL.md"
    )

    return load_text_file(prompt_file)


def load_identity_map(
    identity_map_path: Path | None,
) -> str:
    """Load a manually approved vehicle identity map."""

    if identity_map_path is None:
        return (
            "No approved vehicle-specific identity map "
            "was supplied."
        )

    return load_text_file(identity_map_path)

def load_prompt_v11() -> str:
    """Load Prompt Classic v1.1 assembled from modules."""

    return load_prompt_modules(
        [
            "01_General_Style.md",
            "02_Composition.md",
            "03_Truck_Identity.md",
            "04_Text_Rules.md",
            "05_Printability.md",
            "06_Simplification.md",
            "07_Negative_Rules.md",
            "08_Style_DNA.md",
            "09_Final_Validation.md",
        ]
    )    


def build_prompt(
    identity_map_path: Path | None = None,
) -> str:
    """Assemble the final PrintSketch production prompt."""

    mission = load_engine_modules(
        [
            "00_Mission.md",
        ]
    )

    design_rules = load_engine_modules(
        [
            "01_General_Style.md",
            "05_Style_DNA.md",
            "06_Negative_Prompt.md",
            "07_Decision_Priority.md",
        ]
    )

    composition_rules = load_engine_modules(
        [
            "02_Composition.md",
        ]
    )

    identity_rules = load_engine_modules(
        [
            "03_Truck_Identity.md",
            "08_Decision_Hierarchy.md",
        ]
    )

    printability_rules = load_engine_modules(
        [
            "04_Print_Rules.md",
        ]
    )

    identity_map = load_identity_map(
        identity_map_path
    )

    prompt_template = load_prompt_v11()

    return f"""
================ PRINTSKETCH MISSION ================

{mission}

================ DESIGN RULES =======================

{design_rules}

================ COMPOSITION RULES ==================

{composition_rules}

================ IDENTITY RULES =====================

{identity_rules}

================ APPROVED IDENTITY MAP ==============

The information below describes the exact vehicle shown
in the source photograph.

These manually verified facts override automatic
interpretation.

Do not mirror, relocate, reinterpret or invent any
listed identity element.

{identity_map}

================ PRINTABILITY RULES =================

{printability_rules}

================ PROMPT TEMPLATE ====================

{prompt_template}
""".strip()


if __name__ == "__main__":
    prompt = build_prompt()

    output_path = (
        PROJECT_ROOT
        / "Results"
        / "assembled_prompt.txt"
    )

    output_path.write_text(
        prompt,
        encoding="utf-8",
    )

    print("Prompt assembled successfully.")
    print(f"Total characters: {len(prompt)}")
    print(f"Saved to: {output_path}")