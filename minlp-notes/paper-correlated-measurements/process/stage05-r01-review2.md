# Stage 5 independent review 2

## Assessment

No major issue found. The principal scalar, all-split, all-diagonal, spacing and
partial-observation claims are supported by the archived witnesses and by the
independent calculations described below. Two minor issues should be corrected
before accepting this stage. Neither changes a reported bound or invalidates a
result.

## Minor findings

1. **State the paired synthetic-array construction precisely.**
   `sections/05-computation.tex:106–108` calls the inputs “independent
   standard-normal sensitivity arrays.” The archived arrays satisfy
   `F_48(seed) == F_96(seed)[:48]` exactly for every seed 0, 1 and 2. Thus the
   six arrays are not independent experimental replications. The intended
   statement is presumably independent standard-normal entries within each
   generated array. Say that explicitly and disclose that each smaller array
   is the prefix of its same-seed larger array. This is a minor clarification:
   the deterministic certificate claims make no statistical inference requiring
   independence across the six cases.

2. **Check cardinality when replaying the all-diagonal witness.**
   `supplement/replay_certificates.py:56–57` calls `exact_diagonal_point()`
   directly to avoid reproposing the floating dual factor. That helper checks
   the cube and positive reference diagonal, but not `sum(z) == k`; the
   original `certify_diagonal_split.certify()` supplies that separate check.
   Add the exact cardinality assertion in the replay wrapper before describing
   the point as a feasible continuous witness, and include feasibility among
   its verified fields. I checked the actual saved point independently: its
   exact sum is 16, equal to k. The frozen result is therefore valid; this is
   a small omission in the standalone verifier's explicit mathematical checks.
   Hash validation protects the existing artifact, but is not a substitute for
   documenting and checking this premise in the witness computation itself.

## Independent computations

New reviewer scripts and JSON evidence are in
`verification/stage05-review2/`. They do not alter the frozen manuscript or
supplement.

`check.py` passed in about 9.24 seconds. Its substantive calculations are:

- Construct the full rational n=48 early-kinetic covariance and evaluate the
  dense resolvent through a general exact matrix inverse, independently of the
  archived tridiagonal oracle. The complete information matrix, all 48
  derivative entries and direct selected-covariance incumbent determinant
  agree exactly with the dense certificate.
- Reconstruct the all-scalar point by explicitly inverting its positive-support
  virtual covariance. Its determinant agrees exactly with the archived value.
- Reconstruct the all-diagonal point and its 48 split derivatives by a general
  exact virtual-covariance inverse. Construct the saved factor dual, check
  nonnegative corrections and diagonal domination, and reproduce the exact
  lower bound. This uses the rational logarithm enclosure helper after
  independently checking the matrix arithmetic. The all-diagonal reference
  need not be admissible, as correctly permitted by the proof.
- Check all 30 certified scalar-table gap/separation inequalities against the
  exact fractions. All displayed inequalities round in the claimed direction.
- Independently obtain ten scalar and two-mode local regressions/innovation
  variances from covariance Schur complements, including full eight-lag
  patterns, and compare them exactly with the filter helpers.
- Explicitly invert all four partial-observation incumbent covariances under
  the two-mode model, reproduce all exact trace lower bounds, and verify the
  four displayed relative-gap percentages round upward.

`spacing.py` passed in about 38.36 seconds. It reconstructs all 377 reached
conditional patterns by direct rational covariance inversion, evaluates all
31,900 reachable exact quadratic scores, compares each with the integer
interval result, and uses its own tuple-history dynamic programs for the two
prices. It verifies 418 increases of one unit, no decreases, no larger
increases, and the exact prices 299934500 and 299934501. Thus the bound
increase of 1/100000000 is reproduced independently of the archived certificate
driver. The interval component is reused after inspecting its outward
products, squares, signed quadratic handling and denominator derivation.

I also read the entire computation section and computational-model appendix,
the relevant certificate propositions, and the scalar, dense, all-scalar,
diagonal, spacing, partial and integer-score implementations. The scalar and
diagonal comparisons use the same rational model and cardinality family. The
partial prior is added once, the transfer inflates only data information, and
the two-mode normalization and rational square-root enclosure match the stated
model. The direct and interval spacing records use the same reference and
incumbent. Their archived total times are 36.608852 and 1.087171 seconds,
consistent with the manuscript, and distinct from older component-only times.

All 204 source files listed in `process/stage05-r01-freeze.json` remained
unchanged at the time of my hash check.

## Scope and limitations

This review concentrates on the requested archived certificate families and
their presentation. It does not independently rerun every numerical proposal,
all robust/separator certificates, all source-model rankings or the complete
fresh nested-anchor experiment; those are separate parts of the five-reviewer
gate. The checks are exact finite computations where stated, not Lean
verification or a substitute for the manuscript's general proofs. The Stage 6
introduction and synthesis are intentionally absent and are not treated as a
Stage 5 defect.
