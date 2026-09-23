# Independent review: square epigraph row lower bound

Status: passed. The final unconditional theorem for arbitrary finite continuous
linear extended formulations discharges Z1. The finite-LP attainment adapter
and its composition have been independently reviewed.

## Scope reviewed

Reviewed `RowLowerContact.lean`, `RowLowerCounting.lean`, `RowLower.lean`,
`Polyhedron.lean`, and `PolyhedronAffine.lean`, including their actual Lean
hypotheses and proofs. The reviewer did not author these modules.

- `finite_rows_small_step` proves a positive feasible step from finitely many
  affine residuals. Tight rows require a nonpositive direction. For every slack
  row, the explicit bound `-r / (|d| + 1)` is strictly positive. This handles
  zero directions and the empty inequality family.
- `square_contact_of_active_rows` derives the distance bound from an attained
  fiber minimum. Its attainment assumption is substantive and is not itself
  a theorem about all finite LPs.
- `affine_contact_step` and `square_contact_of_minimum_lifts` correctly realize
  that numerical argument on actual affine rows. The perturbation from `p`
  toward `z - (p+q)/2` keeps the input fixed. Every equality remains zero because
  it holds at all three points. Equalities contribute no active-pattern bits.
  The argument imposes no pointedness, boundedness, or restriction on lineality.
  Only inclusion of the active rows at `p` among those at `q` is needed; equality
  of the two patterns supplies that inclusion in the application.
- `grid_pattern_count` uses `N+1` distinct points on a mesh of spacing `1/N` and
  at most `N` colors. A repeated color yields squared separation at least
  `1/N^2`, so the diameter condition implies `1 <= 4 eps N^2`. The positive
  denominator hypothesis is explicit. This proves the exact constant without
  assuming intervals or counting projected facets.
- `square_row_bound_of_attainment` applies this argument with the actual subsets
  of tight rows as colors. There are exactly `2^M` possible subsets. Graph
  containment supplies the contact at the midpoint, including when that
  midpoint is not one of the selected grid points. The theorem therefore uses
  a genuine interval-wide formulation, rather than assuming that a sampled
  model is a relaxation on the full interval.
- `row_log_lower_bound` correctly converts the exponential inequality to
  `M >= (1/2) log_2(1/eps) - 1`, assuming `eps > 0`. It takes logarithms only
  of positive expressions. No strict threshold or ceiling is lost.

## Final formulation and minimum attainment

`exists_scalar_inequalities` in `Polyhedron.lean` proves an actual Fourier–Motzkin elimination step. It handles zero coefficients,
missing upper bounds, missing lower bounds, and an empty constraint family.
`isClosed_exists_linear` eliminates all auxiliary coordinates by induction.
Its coefficient matrix is fixed; continuous parameter-dependent right-hand
sides remain continuous after elimination. The resulting scalar projection is
therefore closed. This is a proof of projection closedness for finite linear
systems, not an assumption that projections of arbitrary closed sets are closed.

`isClosed_exists_affine` transfers this result through a finite basis of an
arbitrary finite-dimensional real vector space. `affine_minimum` represents the
objective value by two inequalities, obtains a nonempty closed scalar image,
and uses its supplied lower bound to show that its infimum belongs to that
image. Neither a bounded feasible set nor a vertex is required. Thus unbounded
fibers, lineality, arbitrary real coefficients, and zero-dimensional auxiliary
spaces cause no missing case.

`affine_minimum_with_equalities` replaces each of the finitely many equalities
by two inequalities only for the attainment proof. The final counting argument
still colors contacts by subsets of the original `Fin M` inequality rows.
Consequently equalities, including the fixed-input equality, do not increase
`M` in the conclusion.

`square_epigraph_row_lower_bound_algebraic` obtains each fiber's feasible point
from graph containment and its lower bound from the asserted approximation
error. It then invokes the proved minimum theorem. The final headline
`square_epigraph_row_lower_bound` has no attainment, face-count, partition, or
boundedness premise. Its hypotheses are arbitrary finite-dimensional real
space, finitely many affine inequality/equality constraints, affine input and
output projections, full square graph containment, and the lower error bound
on inputs in `[0,1]`. These are weaker than full epigraph containment, so every
finite linear extended formulation in Z1 satisfies them. The algebraic theorem
also rules out zero error for finite `M`; the logarithmic theorem explicitly
requires positive error.

The original source's face-count proof is replaced by a complete active-pattern
argument with the same constant. No unresolved premise remains in Z1.

## Targeted verification

Run from `formal`, with `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.RowLowerContact Formal.QuadraticPrecision.RowLowerCounting
```

Result: passed. After reviewing the final adapter, also ran:

```text
lake build --wfail Formal.QuadraticPrecision.RowLower
lake env lean /tmp/Topic20RowReview.lean
```

The build passed. The temporary review file imported `RowLower` and printed
axioms for `isClosed_exists_linear`, `affine_minimum`,
`affine_minimum_with_equalities`, `square_epigraph_row_lower_bound_algebraic`,
and `square_epigraph_row_lower_bound`. All used only `propext`,
`Classical.choice`, and `Quot.sound`. No project-wide verification or CI
inspection was run.
