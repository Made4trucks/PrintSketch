# PrintSketch Studio

# Sprint 01 Benchmark Report

---

## Project Information

| Item | Value |
|------|-------|
| Project | PrintSketch Studio |
| Sprint | 01 |
| Benchmark Run | 20260722_154348 |
| Baseline | v2_baseline |
| Pipeline | ProductionPipeline v1 |
| Prompt Version | Decision Workflow v1 |
| Printer Target | Bambu Lab P1S |
| Nozzle | 0.4 mm |
| Print Size | 170–250 mm |

---

# Purpose

The objective of Sprint 01 was to evaluate the complete image generation pipeline using a benchmark of ten different European trucks.

The benchmark focused on four key areas:

- Printability for FDM manufacturing
- Preservation of truck identity
- Readability of important markings
- Overall composition

All generated images were manually reviewed and discussed to identify recurring issues and define the priorities for the next development sprint.

---

# Executive Summary

Sprint 01 was the first full benchmark of the complete PrintSketch Studio production pipeline.

A benchmark consisting of ten different European trucks was used to evaluate image quality, printability, identity preservation and overall composition.

The overall quality of the generated artwork proved to be very high. Most generated designs successfully preserved the truck model, proportions and visual character.

However, the benchmark also revealed several recurring issues that appeared consistently across multiple truck brands.

The most significant finding of Sprint 01 is that the current AI model does not primarily struggle with creating visually attractive artwork. Instead, it struggles with making design decisions that take physical FDM manufacturing constraints into account while preserving the unique identity of each truck.

This observation changes the direction of future development.

Rather than improving image quality alone, future work will focus on building a decision engine that understands manufacturing constraints, prioritizes truck identity and produces artwork optimized for reliable FDM printing.

Sprint 01 therefore marks the transition from prompt engineering toward intelligent manufacturing-oriented design generation.

---

# Benchmark Results

| # | Truck | Score | Result |
|---|--------|:-----:|:------:|
| 1 | DAF 01 | 9.6 | PASS |
| 2 | DAF 02 | 9.7 | PASS |
| 3 | IVECO 01 | 9.3 | PASS |
| 4 | MAN 01 | 9.8 | PASS |
| 5 | MERCEDES 01 | 9.8 | PASS |
| 6 | RENAULT 01 | 9.9 | PASS |
| 7 | SCANIA 01 | 9.4 | PASS |
| 8 | SCANIA 02 | 9.5 | PASS |
| 9 | VOLVO 01 | 9.6 | PASS |
|10 | VOLVO 02 | 9.8 | PASS |

---

## Benchmark Statistics

| Metric | Value |
|---------|------:|
| Images Tested | 10 |
| Average Score | 9.64 |
| Highest Score | 9.9 |
| Lowest Score | 9.3 |
| Success Rate | 100% |

---

# Root Cause Analysis

The benchmark revealed that most recurring issues do not originate from poor image generation quality.

Instead, they originate from the AI model lacking knowledge about the physical limitations of FDM manufacturing and the relative importance of truck identity elements.

The generated artwork is visually attractive, but the model often attempts to preserve every visible detail equally. This leads to designs containing many elements that are either impossible to print reliably or visually less important than key identity features.

The benchmark demonstrated that successful truck artwork requires the AI to make intelligent design decisions rather than simple visual reproduction.

The system must understand:

- what must always be preserved,
- what may be simplified,
- what should be enlarged,
- what can be safely removed,
- what is physically printable using a 0.4 mm nozzle,
- how manufacturing constraints influence every design decision.

This finding fundamentally changes the future direction of PrintSketch Studio.

Future development will focus on building a manufacturing-aware decision engine rather than only improving prompt wording.

---

# Design Philosophy

PrintSketch Studio does not aim to create the most realistic truck illustration.

Its objective is to create the highest quality FDM printable wall artwork while preserving the visual identity of the original truck.

Every design decision should balance three equally important goals:

- Manufacturing reliability
- Visual aesthetics
- Vehicle identity

The AI should behave as an industrial product designer rather than a graphic artist.

Whenever a conflict occurs between preserving microscopic visual details and producing a clean, reliable printable design, the AI should prioritize the final physical product.

The generated artwork should not simply replicate a photograph.

It should interpret the photograph and redesign it into a premium product specifically optimized for additive manufacturing.

The customer purchases a personalized printed artwork, not a photographic reproduction.

Therefore, every design decision should increase the quality of the final printed object rather than maximize photographic accuracy.

---

# Systematic Findings

The benchmark identified four major categories of recurring issues.

These categories define the primary development priorities for the next sprint.

---

## 1. Printability

This category appeared in every benchmark image.

Recurring issues:

- Grilles contain excessive micro details.
- Headlights are too complex for reliable FDM printing.
- Wheels contain unnecessary fine geometry.
- Registration plates often preserve details that become unreadable after printing.
- Some individual lines are below the practical printable width for a 0.4 mm nozzle.

Conclusion:

The AI currently optimizes for visual realism instead of manufacturability.

---

## 2. Identity Preservation

The benchmark demonstrated that not all truck elements have equal importance.

Recurring issues:

- Incorrect number of auxiliary lights.
- Missing mirror cameras.
- Missing mirror lights.
- Missing Michelin figures.
- Additional lights invented by the AI.
- Characteristic accessories occasionally removed.
- Vehicle paint pattern not always preserved correctly.

Conclusion:

Truck identity must be treated as a priority hierarchy rather than a flat list of visual objects.

---

## 3. Readability

Recurring issues:

- Model names sometimes too small.
- Company names lose readability.
- Registration plates remain overly detailed instead of becoming readable.
- Important identity markings should scale intelligently according to available space.

Conclusion:

Readable identity information is more valuable than preserving microscopic typography.

---

## 4. Composition

Recurring issues:

- Truck positioned too close to the circular frame.
- Parts of the truck visually compete with the border.
- Some compositions appear too tight.
- Minor decorative stickers receive the same importance as key identity elements.

Conclusion:

Composition should maximize the visual impact of the final printed product rather than preserve every photographed detail equally.

---