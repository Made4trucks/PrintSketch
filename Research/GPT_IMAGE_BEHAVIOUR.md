# GPT Image Behaviour Research

This document records verified observations about GPT Image behaviour during PrintSketch benchmark testing.

---

## Discovery 001

Benchmark:
Test01_Baseline

Observation:
GPT Image preserves truck identity and company identity very well.

Confidence:
High

Status:
Verified

---

## Discovery 002

Benchmark:
Test02_RemoveTrailer

Observation:
GPT Image correctly removes the trailer when explicitly instructed.

Confidence:
High

Status:
Verified

---

## Discovery 003

Benchmark:
Test03_VisualHierarchy

Observation:
GPT Image simplifies tiny details successfully, but may also remove owner-specific identity elements such as personalized windshield names.

Confidence:
High

Status:
Verified

## Discovery 004

Benchmark:
Test06_PrintabilityAdapter

Observation:
Explicit FDM printability constraints significantly improve the result.

Positive effects:
- simpler and more printable headlights
- cleaner grille geometry
- brighter windows
- preserved personalized windshield names
- reduced interior and decorative noise
- better use of white body areas

Confidence:
High

Status:
New baseline

## Discovery 005

Benchmark:
Test07_ModelDesignation

Observation:
A strong model-designation priority restores the model badge, but can unintentionally increase detail density and reduce printability in other areas.

Side effects:
- more complex headlights
- denser grille geometry
- unwanted black body areas
- weaker overall visual balance

Decision:
Rejected as baseline.

Confidence:
High

Status:
Verified