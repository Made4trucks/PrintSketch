def build_identity_preservation(
    company_identity: list[str],
    truck_identity: list[str],
    additional_notes: str,
) -> str:
    """Build Identity Preservation section for the production prompt."""

    lines = []

    lines.append("IDENTITY PRESERVATION")
    lines.append("=" * 40)
    lines.append("")

    lines.append("★★★★★ COMPANY IDENTITY (HIGHEST PRIORITY)")

    if company_identity:
        for item in company_identity:
            lines.append(f"✓ {item}")
    else:
        lines.append("None specified")

    lines.append("")
    lines.append(
        "These elements MUST remain clearly recognizable."
    )
    lines.append(
        "If necessary, they may be slightly emphasized (up to about 5–10%)"
    )
    lines.append(
        "while preserving a natural appearance."
    )

    lines.append("")
    lines.append("-" * 40)
    lines.append("")

    lines.append("OTHER TRUCK IDENTITY")

    if truck_identity:
        for item in truck_identity:
            lines.append(f"✓ {item}")
    else:
        lines.append("None specified")

    lines.append("")
    lines.append("ADDITIONAL NOTES")

    if additional_notes.strip():
        lines.append(additional_notes.strip())
    else:
        lines.append("None")

    return "\n".join(lines)