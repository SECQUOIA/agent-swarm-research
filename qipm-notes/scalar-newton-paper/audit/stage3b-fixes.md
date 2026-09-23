# Stage 3b corrections

All six accepted items in `stage3b-assessment.md` are addressed. The earlier
author-stage corrections were retained, and no later stage was started.

1. **Hard-ray normalization.** In `09-reuse.tex`, the signed unit
   coordinates are explicitly those of A^{-1}e. The text then identifies
   M^{-1}e as its public sqrt(8) multiple and states that their normalized
   states agree. The inverse-norm estimate uses absolute row and column
   sums. This addresses reviewer 1 item 1, reviewer 2 item 1, reviewer 3
   item 1, and reviewer 4 item 1.
2. **Trajectory indices and block domain.** In `08-temporal.tex`, B is
   explicitly a positive integer. Both trajectory output definitions use
   j=1,...,B, and the theorems request all B increments or predictor
   decrements. The endpoint proof handles B=1 by the one-block lower bound
   and invokes strong XOR only for B>=2. This addresses reviewer 3 item 2
   and the lead's domain clarification.
3. **KKT access contract.** Proposition `prop:fixed-kkt` now expressly
   promises constant-overhead sparse-access simulation. It makes no generic
   full-SQ claim from bidirectional sparse access. This addresses reviewer
   4 item 2.
4. **Mori comparison.** The paragraph cites Mori et al., Theorem 1,
   explicitly for a constant-sparsity family under coherent sparse
   position/value access, Euclidean normalized-state error
   0<epsilon_state<=1/11, and negligible right-hand-side preparation cost.
   This addresses reviewer 4 item 3. I verified Problem 1, Definition 1,
   and Theorem 1 against the local primary PDF via direct text extraction:
   `mori2026-sparsity-dependent-complexity-lower-bound`, pages 2--4. The
   comparator remains separate from this paper's scalar-output theorem.
5. **Source-routing evidence.** `stage3b-author.md` and `source-map.md`
   no longer assert that the excluded one-Lorentz counting and simplex
   search constructions already occur in broader manuscripts. They state
   the actual scope decision and retain the narrower description of access
   and output lessons represented here. No section was invented to support
   the withdrawn assertion. This addresses reviewer 5 item 1.
6. **Numerical-width domain.** Theorem `thm:robust-reuse` now defines D
   as system dimension and takes integer 1<=r<=D. This addresses the lead's
   integration clarification.

## Validation

- Ran `checks/check_temporal_identities.py` with the absolute qipm
  interpreter. Kernel/leakage, threshold/XOR, sparse-KKT, and rank/volume
  diagnostics all passed. The kernel diagnostics explicitly include B=1
  and precisely the j=1,...,B output range.
- Ran a clean forced build with `conda run -n qipm --live-stream`, first
  `make clean` and then `make -B` in `notes/scalar-newton-paper/`.
- The resulting staged PDF has 44 pages. The final LaTeX and BibTeX logs
  contain no warnings, undefined references/citations, or box warnings.
- `workflow.md` now marks Stage 3b corrected and pending root verification.

Verdict: all accepted Stage 3b corrections are complete. No further issue
was identified during the correction check.
