# Stage 1 author report

Completed scope, evidence inventory, primary-literature comparison, exact-model contract, initial introduction, and standalone LaTeX skeleton. No certificate implementation, benchmark input, historical result, or unrelated concurrent work was modified. The new directory is `paper-certified-minlp/`.

## Main decisions

1. The paper concerns replayable lower-bound certificates for convex MINLP through rational outer approximations. A verified primal upper bound is optional evidence for selected instances, not an assumed feature or prerequisite for a lower-bound paper.
2. The initial literature scout's novelty conclusion is too broad. Halbig et al. (2024) is direct prior work on computing and verifying convex-MINLP certificates. The manuscript now explains the precise distinction: checking nonlinear underestimator evidence and a rational discrete proof, with common exact model semantics.
3. Mathematical underestimation and master-bound transfer are classical components. Any novelty belongs to the explicit integration, supported implementation, formalization coverage, and empirical evidence.
4. The model contract requires one exact interpreted expression model. Merely saying “as constructed” cannot justify analyzing curvature and evaluating cuts on different expressions. Source float conversion is disclosed separately from subsequent exact arithmetic.
5. The historical claim of 269 certificates is treated as historical acceptance, not a new result. The coordinator reproduced a false complete-check acceptance using SOL0/{sol}. This repairable implementation bug does not invalidate the safe-cut mathematical concept. The coordinator's scan found no such derivation in the 11 historical SOL0 files, which limits the scope of this specific attack but does not replace rechecking.
6. The paper separates partial lemma checking, complete bound checking, and proof-assistant coverage. It promises no complete Lean verification of ordinary software or saved artifacts.

## Files authored

- `main.tex`, `references.bib`.
- `sections/01-introduction.tex`, `sections/02-model.tex`.
- `PROCESS.md`, `process/STATUS.md`.
- `evidence/repository-inventory.md`, `evidence/literature-review.md`.
- This report.

## Work remaining by stage

- Stage 2: repair SOL handling and checker success contract; audit supported VIPR inference/reference semantics; unify exact expression interpretation; audit domains and curvature/cut consistency; prove safe rounding with one-sided bounds and epigraph transfer; add regressions for actual failure modes. Correct false “iff” docstring. Either fix existing global checker or clearly delimit a sound supported proof subset; do not paper over the defect by labeling the entire checker trusted while making unconditional acceptance claims.
- Stage 3: formalize safe correction and bound transfer in Lean under explicit hypotheses; build and enumerate axioms/dependencies; report coverage honestly.
- Stage 4: replay available certificates with corrected checker/semantics, allowing reduced accepted counts; run a portable uniform experiment sufficient for the claimed use cases; generate size/time/quality tables and failure taxonomy; case-audit solver discrepancies with exact model identity caveat; add exact rational primal checks where feasible. Preserve historical records unchanged.
- Stage 5: complete all sections, abstract, contribution statement, numerical narrative, bibliography normalization, and reproduction instructions from accepted results; remove skeleton conditional inputs and development-oriented wording before final delivery.
- Stage 6: mandatory full-manuscript five-reviewer cycle, corrections, and final compilation/package check.

## Review requests

The five Stage 1 reviewers should independently examine literature positioning, exact-model contract, mathematical scope/assumptions, inventory completeness, and writing/structure. Current implementation defects are recorded stage dependencies, not claims that Stage 1 fixed them. Any flaw in the proposed scope or model definition itself is a Stage 1 issue. A conclusion that the integration lacks sufficient originality is substantive and should be assessed before investing in later stages.

## Verification performed

`latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` completed successfully and generated a 7-page initial PDF. The final LaTeX log has no undefined references/citations, overfull boxes, or duplicate destinations. The build transcript is `process/stage01-build.log`. The exact binary-coefficient counterexample was checked independently with Python `Fraction` and equals `-1/2**55`. No experiments were rerun and no checker correction is claimed in this stage.
