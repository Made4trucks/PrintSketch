# Simplification

<!--
Purpose:
Defines how visual complexity should be reduced while preserving truck identity.
This module controls simplification decisions required for high-quality FDM printing.
-->

Design for a 0.4 mm nozzle.

Minimum printable line width about 0.6 mm.

Avoid extremely thin lines.

Avoid floating elements.

Every important element should connect naturally with the design.

## Headlight Strategy

Preserve the exact number, position and overall shape of all headlights and auxiliary lights.

Do not redesign or reposition any lighting elements.

Simplify only the internal geometry of each light to ensure reliable printing with a 0.4 mm nozzle.

Avoid tiny circles, thin rings and decorative micro details inside the lamps.

The vehicle should remain instantly recognizable by its lighting signature even after simplification.

## Intelligent Detail Filtering

Not every visible detail from the original photo should be preserved.

Automatically remove or simplify elements that fall below the minimum printable size for a 0.4 mm nozzle.

Examples include:

- tiny stickers
- micro logos
- decorative symbols
- very small text
- thin ornamental lines

Preserve recognizable identity instead of photographic completeness.

Removing insignificant details is preferred over generating fragile or unreadable geometry.

## Wheel Strategy

Preserve the overall appearance and recognizable design of the wheels.

Maintain the number of wheels, rim proportions and characteristic style.

Reduce tiny holes, thin rings and micro details that cannot be reproduced reliably with a 0.4 mm nozzle.

The wheel should immediately look correct, even if some internal details are simplified.

Prioritize visual identity over mechanical accuracy.
