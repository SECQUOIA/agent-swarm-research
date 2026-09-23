# Manuscript development and review

Started 2026-09-22. Moved to `notes/scalar-newton-paper/` at the user’s request during Stage 2 review; all subsequent work uses this location. The requested deliverable is a standalone research paper on
scalar Newton quantities and sparse inverse quadratic forms, with proofs,
careful prior-work attribution, and explicit access and output assumptions.

## Stages

1. Foundations, access models, classical estimators and sampling algorithms;
   inventory and routing of all relevant repository developments.
2. Sparse/SQ lower bounds, statistical lower bounds, composition and rational
   optimization realizations.
3. Coherent quantum bounds, scalar optimization outputs, structured cone
   systems and the limits of trajectory composition. To keep each proof
   review bounded, this stage has three sequential units, each with its own
   author, five independent reviews, assessment and correction cycle:
   3a coherent bounds and cyclic LP/SOCP scalar realizations;
   3b scalar trajectory composition and reuse limitations;
   3c structured Lorentz and generalized-power Newton systems.
4. Literature positioning, introduction, synthesis, complete integration,
   reproducibility, and standalone build.
5. Whole-manuscript independent review and final verification.

Each author stage is followed by five independent reviews. The lead agent
assesses every finding; a separate fixer resolves all accepted findings.
Any accepted major finding triggers another five-reviewer round after fixes.
All accepted minor findings are resolved before the next stage starts.
The same process applies to the final whole-manuscript review.

Review reports are internal evidence, not external peer review. A note's
"proved" or "audited" label is not treated as a proof. The manuscript must
retain only justified claims and distinguish exact arithmetic, query, gate,
bit, and whole-optimization costs. An unsolved stronger classification does
not authorize an unproved theorem.

## Status

- Stage 1: complete. Five independent reviews found no major issues; all
  accepted minor issues were corrected by a separate fixer and checked by
  root. Seven-page staged build and classical diagnostics pass.
- Stage 2: complete. All five reviews found no major issues. A separate
  fixer addressed all seven accepted minor findings, root checked the edits,
  and both diagnostic scripts and the 20-page build pass.
- Stage 3a: complete. All five independent reviews found no major issues;
  the separate fixer addressed all eleven accepted corrections, and root
  inspected every edit and the clean build logs. Cyclic diagnostics pass;
  the corrected staged manuscript has 32 pages.
- Stage 3b: complete. All five reviews found no major issues; the separate
  fixer addressed all six accepted corrections. Root inspected the edits,
  checked the clean build logs and reran the temporal diagnostics.
- Stage 3c: complete. All five reviews found no major issues; the separate
  fixer addressed all seven accepted groups and root checked every edit
  and the clean build logs. All 152 structured diagnostics pass; 54 pages.
- Stage 4: complete. Five independent reviews found no major issues;
  a separate fixer addressed all four accepted minor groups and root
  inspected the corrections. Standalone build and all five diagnostics pass. The introduction,
  comparison table, barrier conventions, related work, conclusion, and
  submission-source packaging are integrated. The 59-page build has no
  warnings or bad boxes; the 24-file archive rebuilds independently.
- Stage 5: complete. All five independent whole-manuscript reviews found
  no remaining major or minor issues. Root assessed all reports and
  verified the 24-file archive against current sources, extracted it into
  a fresh directory, and rebuilt the clean 59-page, 40-reference paper.
  All five diagnostics pass. No further correction or repeat review is
  required by the findings; see stage5-assessment.md.
