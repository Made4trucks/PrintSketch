from pathlib import Path

from engine_loader import load_engine


def load_prompt_template() -> str:
    project_root = Path(__file__).resolve().parent.parent
    prompt_folder = project_root / "Prompts"

    prompt_file = prompt_folder / "Prompt_Classic_v1.0_FINAL.md"

    if not prompt_file.exists():
        raise FileNotFoundError("Prompt template not found.")

    return prompt_file.read_text(encoding="utf-8").strip()


def build_prompt() -> str:
    engine = load_engine()
    template = load_prompt_template()

    return f"""
================ PRINTSKETCH ENGINE ================

{engine}

================ PROMPT TEMPLATE ===================

{template}
"""


if __name__ == "__main__":
    prompt = build_prompt()

    output_path = (
        Path(__file__).resolve().parent.parent
        / "Results"
        / "assembled_prompt.txt"
    )

    output_path.write_text(prompt, encoding="utf-8")

    print("Prompt assembled successfully.")
    print(f"Total characters: {len(prompt)}")
    print(f"Saved to: {output_path}")