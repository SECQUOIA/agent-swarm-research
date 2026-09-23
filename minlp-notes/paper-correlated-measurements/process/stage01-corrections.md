# Stage 1 corrections

Correction author: `/root/stage01_corrections`. Date: 2026-09-13.
Read the coordinator assessment and all five Stage 1 independent review reports.
Addressed all seven consolidated accepted minor issues. No later section was
written and `PROCESS.md` was not edited.

## Accepted items and actual changes

1. **Estimable-subspace qualification.**
   `sections/01-foundations.tex:115–123` now limits simple information restriction
   to a declared reduced parameter model or common supported invariant range in
   an orthonormal basis. It requires nuisance-adjusted contrast covariance when
   complementary parameters remain unknown, and identifies inverse Schur
   information in the nonsingular block case. Exact arithmetic checks the
   reviewer's two-parameter example: the contrast variance is 2/3, while inverse
   compressed information is 1/2; the nuisance-adjusted inverse gives 2/3.

2. **Inherited corollary hypotheses.**
   `sections/01-foundations.tex:312–315` explicitly invokes Proposition
   `prop:kantorovich` and the definition of alpha in `eq:alpha` before stating
   the feasible-family assumption. The mathematical guarantee is unchanged.

3. **Sharpness extrema.**
   `sections/01-foundations.tex:360–364` states that efficiency has the sharp
   infimum and additive log-information loss the corresponding supremum.
   Rational approximation and the three-candidate construction remain intact.
   A symbolic limit and monotonicity check confirm the directions.

4. **Full-local-rank witness.**
   `sections/01-foundations.tex:145–154` supplies the ordered three-time
   sensitivity determinant at `(A_0,k_1,k_2)=(1,1,2)` and explicitly concludes
   positive definite local data information under any SPD observation covariance
   without a prior. Independent symbolic differentiation of the mean, before
   substituting parameters and times, gives exactly `-log(2)^2/2048`.
   The same script independently verifies the full trajectory rate-swap identity.

5. **Supplementary-table locator.**
   `sections/01-foundations.tex:412–416` identifies accepted-manuscript Table
   S-1, printed p.S-2/PDF p.46, and the A-DCM/C-DCM transposed entries 0.01 and
   0.1. Checked directly against the existing original-PDF extraction in review
   2's scratch folder. The symmetric code covariance and version boundary remain
   explicit; no claim is made about the uninspected publisher typeset article.

6. **Rotary-bed locator.**
   `process/literature.md:55` now gives lines 101–108. Read those exact numbered
   lines in the pinned checkout: they contain the variance vector, zero matrix,
   and diagonal assignments. Lines 111–120 are not cited for that construction.

7. **Prior reductions and general-covariance FPTAS handoff.**
   `process/coverage.md:86,93` and the source-family rows plus the new required
   handoff in `process/literature.md:136` explicitly record independent dummy
   padding, block-diagonal normalization, and the global-Gaussian-KL implication
   for relative precision/Fisher information. Stage 2 must explain the short
   arguments and compare precise hypotheses, constants, calendar windows and
   horizon dependence. Neither subset uniformity nor unbounded original
   diagonal blocks alone is presented as novelty. The concluding candidate-
   contribution wording is narrowed accordingly.

   The same files now assign the general-covariance note's Section 6 inherited
   weighted-trace FPTAS to Stage 3. They specify input-sized dimensions,
   explicitly encoded rational data, fixed decay and conditioning promises,
   complete packets, exact cardinality with optional mandatory/forbidden times,
   and the exclusion of a uniform scheme over unrestricted promises or an
   inverse-trace/multivariate-logdet FPTAS. Read the source note Sections 6 and 8
   and the FSAI priority audit Section 5 while preparing this handoff. This
   documentation does not substitute for later source and theorem review.

## Validation and deliverables

- `python verification/stage01-corrections/check.py`: passed. Script and saved
  `verification/stage01-corrections/results.txt` retain the symbolic determinant,
  swap identity, nuisance example, and extremum-direction checks.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`:
  successful eight-page PDF. Final `build/main.log` has no warnings, undefined
  references, overfull boxes, or underfull boxes. The first pass requested a
  cross-reference rerun; latexmk completed it automatically.
- Read back every revised manuscript passage and checked the source-table and
  rotary-bed locators. The only newly printed manuscript formula, the sensitivity
  determinant, was verified by differentiation independent of the reviewer scripts.
- Changed source files: `sections/01-foundations.tex`, `process/coverage.md`, and
  `process/literature.md`; added this record and the correction verification
  script/results. The normal `build/` outputs were regenerated.

All accepted Stage 1 corrections are complete. No major issue was accepted by the
coordinator, so this correction does not initiate another review round.
