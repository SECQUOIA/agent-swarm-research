# Independent review: finite LP projection and attainment

Result: passed. Reviewed `Polyhedron.lean`, `PolyhedronAffine.lean`, and the
attainment adapter `affine_minimum_with_equalities` in `RowLower.lean`.
No source changes were made during this review.

## Mathematical checks

- `exists_scalar_inequalities` proves both directions of one-coordinate
  Fourier–Motzkin elimination. Negative coefficients supply lower bounds,
  positive coefficients supply upper bounds, and zero coefficients retain
  the required feasibility inequality. The witness construction covers an
  absent upper family, an absent lower family, and both families being empty.
- `isClosed_exists_linear` eliminates exactly the finitely many real auxiliary
  coordinates. Each stage has a finite zero-coefficient row family and a
  finite family of negative/positive row pairs. The transformed coefficients
  and right-hand sides have the correct signs. Continuity is preserved by
  division by fixed real constants and subtraction. This proves closedness
  of the projected set; it does not assume that projections of arbitrary
  closed convex sets are closed.
- `exists_minimum_linear_projection` uses nonemptiness, the proved
  closedness, and an explicit lower bound to put the infimum in the scalar
  projection. Its conclusion includes an actual auxiliary witness at that
  infimum. No compactness or boundedness of the auxiliary feasible region
  is required.
- `isClosed_exists_affine` expands each affine row in a finite real basis,
  retaining its constant term. The coordinate map is a linear equivalence,
  so both directions recover all points of the original auxiliary space.
  The source space is any finite-dimensional real module; it need not be
  presented as a coordinate space or carry a selected topology.
- `affine_minimum` imposes the scalar objective value by the two inequalities
  `T v ≤ t` and `-T v ≤ -t`. Thus it applies to arbitrary real affine
  objectives, including a constant term. Feasibility and lower boundedness
  are its only optimization assumptions.
- `affine_minimum_with_equalities` replaces each finite affine equality with
  its positive and negative inequalities. The final row-bound theorem also
  fixes the input coordinate using an equality before invoking attainment.
  These additional rows are used only to prove attainment. They do not alter
  the original inequality count `M` in the separate contact/counting theorem.

All coefficient types are real. The statements impose no rationality,
pointedness, bounded-fiber, full-dimensionality, or closure assumption beyond
the finite affine description itself. Empty row families and zero auxiliary
dimension are admitted. Finiteness of both the row family and auxiliary
dimension is essential and remains explicit.

## Targeted verification

From `formal/`, with `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.QuadraticPrecision.Polyhedron Formal.QuadraticPrecision.PolyhedronAffine Formal.QuadraticPrecision.RowLower
lake env lean -DwarningAsError=true /tmp/topic20-polyhedron-review.lean
```

Both final commands passed. The temporary independent elaboration checked
empty row families, zero auxiliary dimension, a one-sided scalar inequality,
and a constant affine objective on an entirely unconstrained two-dimensional
auxiliary space. It also printed the axioms of the six reviewed foundation
and attainment declarations. Each used only `propext`, `Classical.choice`,
and `Quot.sound`.

This was a targeted local review, not project-wide verification or a CI check.
The elimination proof establishes existence and closedness; it does not claim
a polynomial bound on Fourier–Motzkin intermediate row counts.
