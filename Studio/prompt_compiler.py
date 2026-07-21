from loaders import (
    load_engine_modules,
    load_identity_map,
    load_prompt_modules,
)
from prompt_context import PromptContext
from prompt_sections import PromptSections


class PromptCompiler:
    """Compiles the final PrintSketch production prompt."""

    def __init__(
        self,
        context: PromptContext | None = None,
    ) -> None:
        self.context = context or PromptContext()

    def compile(self) -> str:
        """Compile the complete production prompt."""

        sections = PromptSections(
            mission=load_engine_modules(
                [
                    "00_Mission.md",
                ]
            ),
            design_rules=load_engine_modules(
                [
                    "01_General_Style.md",
                    "05_Style_DNA.md",
                    "06_Negative_Prompt.md",
                    "07_Decision_Priority.md",
                ]
            ),
            composition_rules=load_engine_modules(
                [
                    "02_Composition.md",
                ]
            ),
            identity_rules=load_engine_modules(
                [
                    "03_Truck_Identity.md",
                    "08_Decision_Hierarchy.md",
                ]
            ),
            identity_map=load_identity_map(
                self.context.identity_map_path
            ),
            printability_rules=load_engine_modules(
                [
                    "04_Print_Rules.md",
                ]
            ),
            prompt_template=load_prompt_modules(
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
            ),
        )

        return sections.assemble()


if __name__ == "__main__":
    compiler = PromptCompiler()
    prompt = compiler.compile()

    print("Prompt Compiler OK")
    print(f"Characters: {len(prompt)}")