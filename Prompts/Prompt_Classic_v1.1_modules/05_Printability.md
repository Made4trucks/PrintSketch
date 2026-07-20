# Printability

<!--
Purpose:
Defines the physical constraints of FDM printing.
This module ensures that every generated design is optimized for reliable manufacturing rather than only visual appearance.
-->

Use black only where it improves readability after 3D printing.

Clean white separation lines.

Balanced contrast.

Smooth curves.

Vector-like appearance.

The design must look excellent after 3D printing, not only on a screen.

## Grille Strategy

Preserve the unique identity of every manufacturer's grille.

Maintain the overall grille layout and proportions.

Simplify repetitive micro geometry whenever necessary for reliable FDM printing.

Prefer bold printable shapes over highly accurate but fragile details.

The grille must remain instantly recognizable even after simplification.

## Standard vs Premium Detail Mode

Every design should be optimized primarily for reliable FDM printing with a 0.4 mm nozzle.

For standard production:

- simplify complex side graphics
- simplify wheel details
- simplify grille micro geometry
- simplify headlight internals
- remove decorative micro elements

For premium projects using a 0.2 mm nozzle, preserve additional detail whenever it significantly improves the final product.

Always prioritize consistent print quality over maximum visual complexity.