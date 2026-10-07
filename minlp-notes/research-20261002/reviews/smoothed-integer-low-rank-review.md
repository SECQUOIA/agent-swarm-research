# Independent review of the smoothed integer low-rank theorem

Date: 2026-10-02. Reviewed the completed
[proof](../new-direction/smoothed-integer-low-rank.md), including its
general convex quartics, normalized long-interval example, and deterministic
binary and explicit-label baselines. No mathematical blocker found.

The exact recourse proof is valid for every rational polynomial of degree
at most four that is convex on its coordinate interval. Its forward
differences are nondecreasing, so binary search gives an exact integer
minimizer with polynomial bit cost. The neighbor certificates allow ties.
Singleton intervals require no convexity test or search.

The auxiliary domain is fixed before sampling and contains every required
point `Tx-d/alpha`. Subtracting `alpha||a||^2/2` from the recourse value
leaves a concave lower envelope of affine functions. The square-completion
identity transfers the cell certificate to an original integer witness
without increasing its gap. The levelwise incumbent is updated before
pruning, and the non-strict retention rule preserves minimizing cells
when bounds tie.

The finite-noise count uses deterministic neighboring-node comparisons.
Its interior-coordinate intervals depend only on the base value function
and grid; independence is therefore applied before adaptive selection.
The refined-coordinate spacing inequality gives the claimed curvature
factor. For every level through `J`, `m_ij<=2^j<=M`, so the atomic term
contributes at most one per coordinate. Zero, constant, and dependent rows
do not invalidate this argument.

The objective lattice is the decisive distinction. If every base
denominator divides `Q`, then `D0=2Q^3` clears the original negative
quadratic and all unary coefficients. The common noise denominator adds
only a factor `M-1`. Thus both an original feasible value and the original
optimum lie in `[D0(M-1)]^-1 Z`. No corresponding lattice statement is
needed for the auxiliary values or the square-completion shift.

Choosing `M` as the least power of two at least
`max(2,r alpha s^2 D0)` gives `J=log2 M` and
`B_J<=1/(8D0 M)<1/[D0(M-1)]`, while simultaneously controlling the noise
atoms. The noise law is selected once from base data. Its sampling bits,
all mesh coordinates, oracle arithmetic, and certificate values have
polynomial bit length. This establishes exactness on every draw and the
stated expected bit bound. The numerical width-to-noise factor remains
explicit; binary encoding alone does not make it polynomially bounded.

The scope statements are justified. The recourse argument does not cover
coupled integer constraints, and the original lattice does not extend to
general continuous quartic variables. The normalized long-interval example
keeps the projected widths independent of the interval length. Binary and
explicit-label deterministic baselines are consistent with the lifted
concave objective and do not contradict the theorem.

The targeted command actually run was:

```sh
python research-20261002/new-direction/check_smoothed_integer_low_rank.py
```

It passed using exact rational arithmetic:

- 124 discrete recourse cases matched exhaustive minimization, including
  affine, singleton, cubic, shifted quartic, and interval-only convex cases.
- One recourse case found the known interior optimizer `2^80` on
  `[-2^100,2^100]` without enumerating the interval.
- 756 original objective values with rational base coefficients and three
  finite noise-grid sizes satisfied the claimed denominator lattice.
- Seven cell-solver fixtures passed 73 prescribed draws, including 15 draws
  with multiple original minimizers. They used 448 levels, 2,437 processed
  cells, and 8,434 corner calls. The 246 original values enumerated for
  these draws also satisfied the lattice.

Every processed cell bound was checked against its exact minimum, computed
independently by minimizing each original feasible point's quadratic well
on the cell. Every corner oracle was checked against exhaustive recourse.
Every level passed the global certificate and witness-gap inequalities,
and every terminal witness matched exhaustive original optimization.
The fixtures include signed projection coefficients, unequal widths,
nonzero constant rows, zero rows, entirely constant projections, and the
smallest permitted noise grid `M=2`.

These finite deterministic checks exercise the implementation and proof
boundaries. They do not establish the probabilistic theorem by sampling.
The scoped command
`git diff --check -- research-20261002/new-direction/check_smoothed_integer_low_rank.py research-20261002/reviews/smoothed-integer-low-rank-review.md`
passed. A targeted `python - <<'PY'` check also passed for final newlines,
trailing whitespace, and the review's local file link.
No project-wide checks, CI inspection, or literature search were performed.
