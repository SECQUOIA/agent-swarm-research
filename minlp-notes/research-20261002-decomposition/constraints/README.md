# Coupled constraints: completed continuation

The [main note](tu-filtered-grid.md) supplies a complete deterministic
optimization theorem for integral TU continuous fibers with explicitly
listed integer decisions. It combines the existing feasible TU rounding
lemma with min-marginal filtering and quadratic growth. Overlapping network
balances and interval resource rows are included. The result keeps exact
feasibility and gives exact rational output for quadratic objectives.

The [second-phase constrained solver](../completion/constrained-solver.md)
implements reusable branching-tree models, verified TU structure and
curvature, exact nonunique quadratic recovery, and independent trace replay.
The [further theorem](../completion/theory/nonunique-tu-exact.md) proves
unconditional exact recovery and gives a state bound when optimal coordinate
projections are finite. Retaining unions implements that extension. The
prototype and checks below remain first-release evidence.

The additions beyond earlier notes are:

- A full algorithm, restriction-history certificate, bit-cost account, and
  accuracy-independent coordinate state count. The complexity is polynomial
  at fixed width under polynomial conditioning; it is **not** FPT in width
  and conditioning because a power of the global continuous dimension
  remains.
- A constrained active-face height proof and exact optimizer reconstruction
  without knowing a growth constant. Native integer choices remain exact.
- A bound using curvature only along known equality directions. Large
  objective curvature normal to exact balances need not inflate the
  approximation allowance. The coefficient-based exact height bound can
  still increase with such coefficients.
- A checked common-mesh variant that avoids unnecessary initial enumeration
  when large capacities share common units. Arbitrary capacities or rational
  alignment denominators retain explicit pseudopolynomial initial costs.

This is a new completion of the deterministic constrained argument, not a
claim that feasible TU rounding, tree DP, box integrality, or rational
reconstruction is new. The note compares the relevant primary sources and
links the existing TU, affine-repair, and box-grid results.

## Targeted checks actually run

```sh
python3 -B research-20261002-decomposition/constraints/check_tu_filtered_grid.py
```

The [standard-library prototype](check_tu_filtered_grid.py) writes
[tu-filtered-grid-results.json](tu-filtered-grid-results.json). It passed:

- Two mixed continuous/binary network models, one nonconvex quadratic and
  one quartic, through nine levels each. There were 430 exact min-marginal
  comparisons with an independent feasible enumeration, 325 feasible
  growth-witness checks, and 119 removed states or cells.
- 67 exactly feasible mean-preserving corner distributions using 147 atoms;
  fixed native labels were preserved. Structural examples checked the need
  for full directional curvature, common meshes, and aligned right sides.
- Exact reconstruction of `(1/3,2/3)` and its value after 54 grid levels,
  using the theorem's explicit rational-height stopping rule. The largest
  continuous grid contained five nodes.
- Three projected-Hessian cases and 75 exact tangent-direction inequalities,
  including a normal penalty coefficient `10^80`.
- Eight levels with physical flow capacity and initial mesh `10^40`, again
  with at most five nodes per continuous coordinate.

These are bounded exact diagnostics. The two-bag prototype uses simple
neighbor summation; on an arbitrary high-degree decomposition that code
would need the theorem's finite-sum/infeasible-count exclusion optimization
to realize its stated table bound. It is not a production implementation,
a general certificate checker, or comparative solver-performance evidence.

The independent reviewer ran:

```sh
python research-20261002-decomposition/constraints/reviews/check_review_examples.py > research-20261002-decomposition/constraints/reviews/check_review_examples-results.json
```

The [completed-text review](reviews/tu-filtered-grid-review.md) checked the
proofs and required two corrections, both incorporated: only a qualifying
endpoint has a near-optimal witness, and rational constraint data require
an extra denominator factor in the exact-height bound. Its separate exact
fixtures passed eight levels and 212 conditional lower-bound checks for a
model whose continuous matrix is TU while its integer-column augmentation
is not. That script was run by the reviewer; it was not rerun here.
The reviewer also accepted the equality-tangent and common-unit additions,
and its rerun passed four projected-Hessian cases and eight feasible
penalty checks.

Scoped formatting checks used `git diff --no-index --check /dev/null`
on `tu-filtered-grid.md`, `README.md`, and `check_tu_filtered_grid.py`;
they produced no whitespace diagnostics (exit 1 records the new files).
A separate `python3 - <<'PY'` path check verified all 10 local links in
the two authored documents.

No project-wide checks, CI status inspection, or CI log inspection were
performed. The finite checks support the derivations; they do not establish
universal theorems or external peer review.

## Remaining boundaries

This result does not settle the one-draw exact smoothed TU theorem left
open by the earlier chamber-count note. It does not give a width-FPT
constrained algorithm, a general nonlinear-constraint extension, or
polynomial work for arbitrary large binary-encoded integer ranges.
Those are separate substantive problems. The deterministic constrained
theorems above are complete within their explicit assumptions.
