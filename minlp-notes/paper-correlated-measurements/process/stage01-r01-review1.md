# Stage 1 independent review 1

Assessment: **PASS (no major issues); three minor issues should be resolved.**

Scope: `main.tex`, `macros.tex`, `sections/01-foundations.tex`, bibliography,
author report, coverage map, and literature record. I did not read other reviewers'
reports, edit the manuscript, or spawn agents. The absent abstract, introduction,
and later sections are intentional and are not defects of this stage.

## Findings

1. **MINOR — complete the positive-definite-information illustration.**
   `sections/01-foundations.tex:130–143` correctly proves the rate-swap ambiguity,
   but does not explicitly show that the example can have positive definite local
   information, the premise of the opening sentence. This is readily repaired and
   does not invalidate the claim. For example, take `A_0=1, k_1=1, k_2=2`, observe B
   at `t=log(2), 2 log(2), 3 log(2)`, and take any positive definite observation
   covariance. The resulting three-by-three sensitivity matrix has determinant
   `-log(2)^2/2048`, so its information matrix is positive definite. A sentence
   providing this witness makes the distinction between local information rank
   and global identifiability completely self-contained. I verified the
   determinant independently in the review script.

2. **MINOR — identify which quantity has a sharp supremum.**
   `sections/01-foundations.tex:345–348` says the efficiency `1/b^2` approaches
   `1/alpha` and then calls the bound sharp “as a supremum.” For efficiency the
   limiting worst-case value is an **infimum**; the corresponding log-objective
   loss approaches its **supremum** `log(alpha)`. The construction and constant
   are correct. Replace the phrase by “the lower efficiency bound is sharp as an
   infimum,” or explicitly identify the log loss as the quantity whose supremum
   is sharp. This also avoids implying that the unique-optimizer example attains
   the boundary at `b^2=alpha`.

3. **MINOR — correct a source locator in the audit record.**
   `process/literature.md:55` says that `rotary_bed_MO.py` lines 111–120 provide
   the diagonal covariance. In the inspected local immutable software snapshot,
   the variance vector, zero initialization, and diagonal assignments are at
   **lines 101–108**. Lines 111–120 begin the sensitivity CSV description and
   measurement-index list. The manuscript's substantive diagonal-covariance
   statement is correct; fix the locator to keep the evidence trail reliable.

## Mathematical checks and conclusions

- The score and expected score outer product yield exactly
  `F_S^T R_SS^{-1} F_S` for the stated differentiable-mean, fixed-covariance
  Gaussian model. The parameter-dependent covariance contribution, nonlinear
  posterior caveat, and singular-likelihood restriction are correct.
- The linear-model estimability statement and pseudoinverse variance are valid
  under the stated no-prior Gaussian model. Coordinate-change and determinant
  concavity statements are correct. Singular designs are excluded appropriately
  for inverse criteria and assigned negative infinity for log determinant.
- Block inversion gives the inflation identity and the exact equality condition.
  The conditional-noise experiment and actual-response conditioning are correctly
  distinguished: the latter requires the sensitivity correction displayed in
  the draft. Both rational counterexamples check exactly. The information
  increment is positive semidefinite and does not imply submodularity.
- The elementary Kantorovich proof is valid. In particular, compressing
  `R + m M R^{-1} <= (M+m)I` does not interchange inversion and compression.
  The subsequent scalar inequality applies to the selected covariance's
  eigenvalues. Adding a PSD prior preserves the sandwich. Equality of kernels,
  the cross-block rank bound, and the log determinant refinement follow.
- The D, weighted-trace, and conventional A optimizer comparisons have the
  correct order and factor. The singular prior case is safe because the sandwich
  gives a common positive definite domain; empty/full selections give equality.
  A scalar sharpness example suffices for the claimed universal constant.
- Diagonal and selectable-block changes of response coordinates preserve both
  information matrices. The weak-correlation order is correct for the stated
  fixed-matrix perturbation family.
- Independent-time pattern enumeration gives the exact selected-covariance
  information. It properly retains same-time cross-channel correlation and does
  not assert an independent-channel decomposition.
- The certificate inequality and achieved D-efficiency are valid; a gated upper
  bound is reusable while its original incumbent gap need not certify the true
  objective. The text appropriately separates arithmetic certificates from
  physical-model fidelity and nominal sensitivities.

## Evidence inspected

I read `literature/AGENTS.md` before accessing local literature. The following
original sources support the checked claims:

- Liu et al., local full text and corresponding source passages on the selected
  covariance, weak-correlation model, Proposition 2, and information increment.
  These support the manuscript's established-prior-work attribution.
- Wang et al., accepted-manuscript original PDF pages 9–11 extracted directly
  with `pdftotext -layout`: full inverse entries/blocks in Eqs. (8)–(10) and
  pair gating in Eq. (11). The qualification about mixed-modality conventions
  avoids extending the single-modality witness beyond what it establishes.
- The preserved public `measurement-opt` source: full covariance pseudoinverse
  before extraction in `measure_optimize.py`; eight time points and the
  SCM/DCM covariance construction in `kinetics_MO.py`; diagonal covariance
  initialization in `rotary_bed_MO.py`.
- Patan–Bogacka, local full text model and information discussion: covariance
  parameter dependence is explicitly part of the prior work.
- Moradi et al., local original PDF page 1 extracted directly: Eq. (1) states
  precisely the normalized-positive-map inverse Kantorovich inequality used
  here and attributes it to earlier work. The draft does not claim that matrix
  inequality as new.

Focused exact arithmetic is retained in
`verification/stage01-review1/check.py`. It tests all 16 subsets of a rational
four-response covariance under zero, singular, and positive definite priors,
checking both PSD sandwich directions, common kernels, the exact Schur
identity/equality condition, and the cross-block rank bound. All **48 cases
passed**. The kinetic sensitivity determinant above was also verified exactly.
These checks supplement, rather than replace, the proof review. No source PDFs
or extracted copyrighted pages are retained in the review folder.

## Stage assessment

The mathematical foundations are sound and their novelty language is appropriately
restrained. I found no coverage or interface defect that prevents the later stages
from proceeding once the three minor items are adjudicated and addressed.
