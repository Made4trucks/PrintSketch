def build_truck_identity(identity_notes: str) -> str:
    """Build truck identity section for the production prompt."""

    identity_notes = identity_notes.strip()

    if not identity_notes:
        identity_notes = "No additional identity elements specified."

    return (
        "TRUCK IDENTITY\n"
        "------------------------------\n"
        f"{identity_notes}"
    )