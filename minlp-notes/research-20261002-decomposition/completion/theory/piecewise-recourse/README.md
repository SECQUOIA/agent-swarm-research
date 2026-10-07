# Piecewise convex recourse

The [theorem](piecewise-curvature.md) removes stiff positive curvature
across changing private active sets. It uses local piecewise-affine KKT
certificates, retains the original attachment scopes, and avoids the
global overlay of local partitions. The reduced upper curvature is the
maximum local piece curvature. The [independent review](review.md) records
its mathematical scope and verification.

The explicit family has three pieces per block, fixed bag size four,
uniform growth and negative-curvature bounds, and arbitrarily many
negative eigenvalues. Its direct retained curvature grows with stiffness
`M`, while certified reduced curvature stays at most `41/4` for the full
sparse family. No global affine recourse selector exists for its private
blocks. With `m` blocks, the avoided global overlay has `3^m` cells.

[scalar_piecewise.py](scalar_piecewise.py) implements complete exact
active-pattern construction for positive-definite box QPs with one
retained parameter. It supplies an independent PSD/KKT/coverage verifier
and exact value/response queries. The constructor has an explicit pattern
budget and exponential worst-case cost. Its exact piece serialization
supports independent replay in the [convex recourse engine](../../../solver/convex_recourse.py),
which integrates scalar piece curvature with a default cap of 81 active
patterns per private block. General polyhedral recognition and BSP
construction are proof-level algorithms.

Run the targeted diagnostic from the repository root:

```sh
python3 -B research-20261002-decomposition/completion/theory/piecewise-recourse/check_piecewise.py
```

The saved [result](check-results.json) reports five stiffness examples,
485 independent analytic response comparisons, 900 reduced-curvature
interpolation checks, 540 full-vector growth checks, 20 random blocks,
1,980 feasible-value comparisons, 65 singular downward-kink checks,
four empty-private exact queries, two cooperative interruptions,
six serialization roundtrips, 14 rejected invalid serializations, and
14 rejected invalid inputs/certificates. These are exact rational
diagnostics, not a solver performance study. No project-wide or CI
checks were run.
