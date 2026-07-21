from pathlib import Path

from prompt_compiler import PromptCompiler
from prompt_context import PromptContext


def build_prompt(
    identity_map_path: Path | None = None,
) -> str:
    """Legacy compatibility wrapper."""

    context = PromptContext(
        identity_map_path=identity_map_path,
    )

    return PromptCompiler(context).compile()


if __name__ == "__main__":
    prompt = build_prompt()

    print("Prompt Builder OK")
    print(f"Characters: {len(prompt)}")