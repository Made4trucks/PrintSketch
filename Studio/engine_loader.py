from pathlib import Path


ENGINE_ORDER = [
    "00_Mission.md",
    "01_General_Style.md",
    "02_Composition.md",
    "03_Truck_Identity.md",
    "04_Print_Rules.md",
    "05_Style_DNA.md",
    "06_Negative_Prompt.md",
    "07_Decision_Priority.md",
    "08_Decision_Hierarchy.md",
    "09_Print_Profile.md",
    "10_Identity_Protection.md",
    "11_Manufacturing_Reasoning.md",
    "12_Component_Simplification.md",
    "13_Final_Validation.md",
]


def load_engine() -> str:
    project_root = Path(__file__).resolve().parent.parent
    engine_folder = project_root / "Engine"

    parts = []

    for filename in ENGINE_ORDER:
        file_path = engine_folder / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Missing Engine module: {filename}"
            )

        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

        parts.append(content)

    return "\n\n---\n\n".join(parts)


if __name__ == "__main__":
    engine = load_engine()

    print("PrintSketch Engine loaded successfully.")
    print(f"Modules loaded: {len(ENGINE_ORDER)}")
    print(f"Total characters: {len(engine)}")

    ENGINE_ORDER = [
    "00_Mission.md",
    "01_General_Style.md",
    "02_Composition.md",
    "03_Truck_Identity.md",
    "04_Print_Rules.md",
    "05_Style_DNA.md",
    "06_Negative_Prompt.md",
    "07_Decision_Priority.md",
    "08_Decision_Hierarchy.md",
    "09_Print_Profile.md",
    "10_Identity_Protection.md",
    "11_Manufacturing_Reasoning.md",
    "12_Component_Simplification.md",
    "13_Final_Validation.md",
]