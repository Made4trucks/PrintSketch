# PrintSketch Benchmark Rules

## Purpose

The benchmark system is used to test GPT Image instructions in a controlled and repeatable way.

## Rules

1. Every benchmark should test one clear hypothesis.

2. Every generated result must have a unique filename.

3. Previous and rejected results must never be deleted.

4. Only verified improvements may be added to the PrintSketch Engine.

5. Every benchmark should record:
   - source image
   - tested instruction
   - positive effects
   - negative side effects
   - final decision

6. A new instruction becomes part of the baseline only when it improves the complete artwork, not just one isolated detail.

7. Important truck identity must never be improved at the cost of printability.

8. Printability must never be improved at the cost of losing:
   - truck brand
   - company identity
   - personalized names
   - model designation
   - important owner-installed accessories

## Current Baseline

Test06_PrintabilityAdapter

## Baseline Strengths

- trailer removed
- clean black-and-white composition
- bright windshield and side windows
- personalized names preserved
- simplified and printable headlights
- reduced cabin-interior noise
- cleaner grille geometry
- good use of white body areas

## Known Weaknesses

- model designation may disappear
- some rear chassis geometry may still need improvement
- important small labels need controlled enlargement

## Next Research Direction

Test the current baseline on multiple truck brands before adding more permanent Engine rules.