This package verifies the unbounded-ratio disproof in
[`positive-multilinear-gap.md`](../../../results/positive-multilinear-gap.md),
using a weaker bound than its exact hull formula.

| Mathematical obligation | Lean declaration or module |
|---|---|
| Finite dyadic partitions with exact block sizes and partition sum identity | `Construction`: `block_card`, `blockCount_mul_blockSize`, `sum_blocks` |
| Distinct squarefree supports and coefficient-one representation | `support_injective`, `polynomial_eq_supportPolynomial` |
| Separately affine polynomial and strictly interior means | `polynomial_separatelyAffine`, `means_strict` |
| Continuous graph hull equals binary-law representation | Reused `CubicGap.mem_cubeGraph_hull_iff` |
| Individual monomial lower envelope is exactly zero, with all means preserved | `monomial_minimum_zero_of_anchor`, `support_monomial_minimum` |
| Exact individual upper envelopes and total termwise gap T=L | `support_monomial_maximum`, `support_monomial_gap`, `termwiseGap_eq` |
| Pointwise partition deficiency bound | `level_lower_bound`, `polynomial_lower_bound` |
| Deterministic selected-scale bound and its finite-law consequence | `Deficiency`: `dyadic_selected_bound`, `dyadic_deficiency_bound` |
| Mean leaf failure count is one; every admissible law has the required polynomial lower bound | `failureCount_expect`, `law_polynomial_lower_bound` |
| Full polynomial upper envelope is L and is attained | `polynomial_maximum` |
| Actual graph value is strictly below L | `polynomial_at_means_lt` |
| Actual hull gap is positive and at most s+2L/2^s | `hullGap_positive`, `hullGap_bound` |
| Parameters exceed every real constant | `exists_levels`, `unbounded_gap_ratio` |
| Uniform positive multilinear bound is false already for unit coefficients on unit cubes | `no_uniform_positive_multilinear_bound` |

Module qualifiers in this table identify files; all new declarations belong
to namespace `MultilinearGap`.

Not formalized by this package:

- The exact formula H=s+(L−s)2^(-s), its optimality, or its attaining
  bit-reversal/XOR construction.
- The sharp asymptotics R(d)~ln(d)/ln ln(d) and C(n)~ln(n)/ln ln(n),
  including leading constant one and dimension interpolation.
- The harmonic coupling or any general-degree upper bound.
- General nonnegative-box transfer, sparsity asymptotics, or serialized
  construction size. The finite coordinate type and block/support sizes
  used by the proof are explicit.
- Novelty, literature completeness, or publication priority.

The actual partitions are specified by finite equivalences. Their nesting
is not needed for the bound proved here; no claim of the exact dyadic hull
formula is inferred from this formalization.
