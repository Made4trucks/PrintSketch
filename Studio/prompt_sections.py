from dataclasses import dataclass


@dataclass
class PromptSections:
    """Container for all prompt sections."""

    mission: str = ""
    design_rules: str = ""
    composition_rules: str = ""
    identity_rules: str = ""
    identity_map: str = ""
    printability_rules: str = ""
    prompt_template: str = ""

    def assemble(self) -> str:
        return f"""
================ PRINTSKETCH MISSION ================

{self.mission}

================ DESIGN RULES =======================

{self.design_rules}

================ COMPOSITION RULES ==================

{self.composition_rules}

================ IDENTITY RULES =====================

{self.identity_rules}

================ APPROVED IDENTITY MAP ==============

The information below describes the exact vehicle shown
in the source photograph.

These manually verified facts override automatic
interpretation.

Do not mirror, relocate, reinterpret or invent any
listed identity element.

{self.identity_map}

================ PRINTABILITY RULES =================

{self.printability_rules}

================ PROMPT TEMPLATE ====================

{self.prompt_template}
""".strip()
    