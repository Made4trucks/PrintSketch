def remove_duplicate_lines(text: str) -> tuple[str, int]:
    """Remove repeated non-empty lines while preserving their order."""

    seen_lines: set[str] = set()
    cleaned_lines: list[str] = []
    duplicates_removed = 0

    for line in text.splitlines():
        normalized_line = line.strip().lower()

        if not normalized_line:
            cleaned_lines.append("")
            continue

        if normalized_line in seen_lines:
            duplicates_removed += 1
            continue

        seen_lines.add(normalized_line)
        cleaned_lines.append(line.rstrip())

    cleaned_text = "\n".join(cleaned_lines)

    return cleaned_text, duplicates_removed


def normalize_blank_lines(text: str) -> str:
    """Reduce multiple empty lines to one empty line."""

    cleaned_lines: list[str] = []
    previous_line_was_empty = False

    for line in text.splitlines():
        is_empty = not line.strip()

        if is_empty and previous_line_was_empty:
            continue

        cleaned_lines.append(line.rstrip())
        previous_line_was_empty = is_empty

    return "\n".join(cleaned_lines).strip()


def optimize_prompt(prompt: str) -> dict:
    """Clean the prompt and return the optimized text with statistics."""

    deduplicated_prompt, duplicates_removed = remove_duplicate_lines(prompt)
    optimized_prompt = normalize_blank_lines(deduplicated_prompt)

    return {
        "prompt": optimized_prompt,
        "characters": len(optimized_prompt),
        "lines": len(optimized_prompt.splitlines()),
        "duplicates_removed": duplicates_removed,
    }
def calculate_prompt_quality(prompt: str) -> dict:
    """Evaluate whether the prompt contains the required production sections."""

    required_sections = [
        "PROJECT NAME:",
        "IMAGE ANALYSIS:",
        "IDENTITY PRESERVATION",
        "SVG PRESERVATION CHECKLIST:",
        "PRINTSKETCH ENGINE",
        "PROMPT TEMPLATE",
    ]

    missing_sections = [
        section
        for section in required_sections
        if section not in prompt
    ]

    score = 100 - (len(missing_sections) * 15)
    score = max(0, score)

    if score >= 90:
        rating = "Excellent"
    elif score >= 75:
        rating = "Good"
    elif score >= 60:
        rating = "Needs review"
    else:
        rating = "Incomplete"

    return {
        "score": score,
        "rating": rating,
        "missing_sections": missing_sections,
    }