> Historical preparation record. The September 2026 submission revision and
> its current review status are recorded in
> [revision-20260907/PROCESS.md](revision-20260907/PROCESS.md).

# Manuscript process and current status

User requested a complete LaTeX paper on integer dimension for nonlinear approximation, substantive mathematical verification and development, sequential drafting stages, fifteen independent reviewers after each stage, a separate correction agent, repeated fifteen-reviewer rounds after major corrections, and a final whole-paper review loop and compiled PDF.

## Planned stages

1. Foundations and precision laws: definitions, parity/convexity methods, scalar and graph laws, quadratic systems and noncommutative rank, smooth and perspective extensions. Build the complete source/dependency inventory alongside the first draft.
2. Finite-accuracy quadratic theory: covariance characterization, rational algorithms, general error bodies, nonlinear input rank, structured quadratic refinements, and approximation hardness.
3. Scalar and separable nonlinear theory: curvature geometry and certified compilation, positive powers and polynomials, arbitrary convex polynomials, separable comparisons, and encoding issues.
4. Vector theory and synthesis: coupled outputs, curvature rank, oracle bodies, separable vector results, exact binary/general-integer separations, nonconvex constructions, remaining boundaries; write introduction, abstract, and conclusion around the verified final scope.
5. Whole-paper verification: fifteen independent full-manuscript reviews, correction and repeat rounds as required; coverage and citation audit, reproducible numerical/exact checks, LaTeX and PDF inspection.

Each mathematical stage is gated: no drafting of the next stage until the root agent has adjudicated all fifteen reports and accepted corrections, with a new full review round if major issues were found. Reviewers should identify precise claims, counterexamples, missing hypotheses, and material exposition problems. A root decision log records accepted and rejected criticisms with reasons. Supporting checks do not replace proofs. Literature priority and mathematical validity are separate.

## Current status

Stage 1: gate passed after fifteen independent reviews (0 major, 35 minor findings), nine consolidated accepted correction actions, and a separate correction pass. Root inspected the complete patch and confirmed a clean 19-page build and resolved labels/citations. The corrected inventory contains 43 canonical results and 194 supporting notes, with 32 explicit substantive supporting developments. Seven existing checks and the author's 455 folding-LP checks passed. Records: `reviews/stage1-round1/` and `verification/stage1-corrections.md`.

Stage 2: gate passed after fifteen independent reviews (0 major, 8 minor findings), five consolidated accepted corrections, and a separate correction pass. Root read the full stage and complete correction patch, checked key primary-source imports, and confirmed a clean 41-page combined build (125 labels, 22 bibliography entries). Thirteen supplementary scripts passed before review; focused certificate and correlated-budget checks passed after correction. Records: `reviews/stage2-round1/` and `verification/stage2-corrections.md`. The inventory contains 43 canonical results, 33 explicit substantive supporting developments and 196 notes/audits. Stage 3: gate passed after fifteen independent reviews (0 major, 3 minor findings), two consolidated accepted correction actions and a separate correction pass. Root read every report and the full correction patch, verified preserved inputs and archive hashes, and confirmed a clean 63-page combined build with 198 labels and 32 bibliography entries. Seventeen supplementary scripts passed before review; reviewer checks add independent exact geometry, inverse, interpolation and boundary cases. All eleven canonical and thirteen substantive stage 3 developments are covered. Records: `reviews/stage3-round1/` and `verification/stage3-corrections.md`. The inventory has 43 canonical results, 34 explicit substantive supporting developments and 196 notes/audits. Stage 4: gate passed after fifteen independent reviews (0 major, 0 minor), one root layout finding and a separate correction pass. Root read every full report, verified the complete patch and preserved source/report hashes, and inspected the corrected pages. All ten canonical and eleven substantive vector developments are covered. Nine supplementary scripts passed; the clean complete draft is 84 pages with 258 labels and 39 bibliography entries. Records: `reviews/stage4-round1/` and `verification/stage4-corrections.md`. Stage 5: gate passed after fifteen complete whole-paper reviews (0 major, 0 minor and no unresolved question). Root read every full report, completed the final coverage/synthesis audit, verified all eleven frozen source hashes and the inspected PDF hash, and confirmed the clean 84-page build. No correction was accepted in this round, so the repeat rule was not triggered. The interruption during root report reading was recovered without skipping any review. Records: `reviews/whole-round1/`, `verification/final-validation.json` and `FINAL-REPORT.md`. The complete process comprises 75 independent review reports across five rounds, four separate stage correction passes and 17 consolidated correction actions (including the root layout finding).

## Scope and honesty

Existing repository review labels are evidence to inspect, not proof of correctness. Unsupported statements must be repaired, explicitly weakened, or identified as unresolved; do not conceal gaps or claim every open question is solved. No claim of external peer review or guaranteed journal acceptance. Preserve existing research files; manuscript-specific corrections and provenance belong here.

## Optional author metadata

An asynchronous question requests author names, affiliations, and corresponding email. This is not a gate for mathematical work; leave the author block blank unless the user supplies metadata.

At the final whole-paper stage, repeat the fifteen-reviewer round after any accepted finding is corrected, including minor findings, until the complete round yields no remaining accepted issue. Root judgments must distinguish valid criticisms from unsupported or purely optional preferences.
