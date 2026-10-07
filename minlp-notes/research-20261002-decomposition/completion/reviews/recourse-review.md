# Independent review of the affine recourse pipeline

The reviewed affine path is mathematically sound and ready for bounded
experiments. This review covers `solver/recourse.py`,
`solver/verify_recourse.py`, and their composition with the existing exact
and approximate solvers. It does not establish solver competitiveness or
completeness of automatic block discovery.

## Mathematical checks

For a PSD private Hessian, every optimizer of the central convex QP has the
same private gradient. A strictly positive central component forces that
coordinate of any globally affine selector to be the lower bound: it is
locally fixed around the center, and an affine function locally fixed is
fixed everywhere. The negative case is symmetric. If a central gradient
component is zero, an affine selector's corresponding gradient must vanish
identically. This holds whether the coordinate is locally interior or
identically at a bound, because a nonzero affine gradient cannot have a
constant weak sign on a full-dimensional parameter box while vanishing at
its center. The LP encodes these alternatives, affine feasibility, and the
whole-box signs exactly. Singular private Hessians do not invalidate this
argument.

The verifier independently checks private PSD by Schur complements, exact
affine ranges, and whole-box KKT identities. These conditions are sufficient
for a private global optimizer at every retained point. Substitution uses
`M' A M`, `M' (A a + b)`, and the original objective at the offset. Fixed
continuous and integer coordinates, attachment indices, later original-index
remapping, and the case where all coordinates are removed were checked.
Integer attachments are safe because recognition certifies the stronger
whole continuous parameter box.

The verifier shares the elementary exact substitution and lift functions
with the producer. Those functions were inspected and checked against an
independent full-face optimization oracle and direct objective identities.
The verifier does not reuse the recognition LP or QP solver. Inner proofs
are bound to the rebuilt quadratic, and the final feasible point and value
are checked in the original model. The caller can also supply an expected
original instance to reject a certificate for another model.

## Defects found and corrected

- The original wrapper ignored `exact_requested`, so changing the request
  to a nonboolean value or to exact mode could pass verification. It now
  checks the Boolean type and binds the request to the inner proof schema
  or minimum-cut request.
- The original wrapper accepted `max_queries=0` in its parameter validation,
  while the minimum-cut backend required a positive value. Validation now
  consistently requires a positive query cap. Additive zero tolerance uses
  the grid route, whose contract permits it.

No unresolved mathematical defect was found in this scope. Limits are
cooperative and some exact linear algebra, substitutions, and backend
operations are atomic. They are not a strict operating-system timeout.
The reference LP/QP implementations also do not inherit the abstract
polynomial oracle bound. Both limitations are documented in the implementation
notes.

## Targeted checks actually run

From the repository root:

```sh
python3 research-20261002-decomposition/completion/reviews/check_affine_pipeline.py
```

This passed:

- 80 scalar affine/nonaffine classifications against an independent clipping
  characterization, including zero private curvature;
- 24 planted PSD private-block examples with varying ranks, singular
  blocks, and native integer attachments;
- independent active-face equality of original and reduced global minima
  for every accepted scalar example and every planted block;
- direct original/substituted objective identities at sampled rational
  parameter points;
- 24 original-model pipeline certificate replays and exact-reference bound
  containment checks;
- rejection of both exact-request protocol mutations.

From `research-20261002-decomposition/solver`:

```sh
python3 -B -m unittest test_recourse test_mincut_adapter -v
```

All 18 tests passed after the corrections. They cover the separate
minimum-cut adapter as well as affine pipeline regressions; the adapter's
larger independent audit is recorded in its own review. No project-wide
checks or CI inspection were run.

## Follow-up review: conditional convex and mixed submodular routes

The wrapper now composes two additional independently reviewed backends:
conditional convex-value search and mixed convex/concave submodular search.
This follow-up covers routing, original-model binding, request flags, and
resource-limit composition. The local optimization and certificate arguments
remain in those backends' own reviews.

The explicit convex route preserves the supplied original-coordinate private
blocks through fixed-coordinate substitution. Automatically chosen blocks
are disjoint PSD blocks without cross-block interactions, and the conditional
backend checks that structure again. The submodular route is also available
explicitly. Automatic mode tries it before minimum cuts when positive
curvature remains. An unsupported structure falls back to the general grid
route; a supported route that reaches its cap returns its valid incomplete
certificate. Exhausted cooperative deadlines retain valid original bounds.

The wrapper compares each inner mathematical model with the quadratic rebuilt
from accepted substitutions, binds the Boolean exact-output request, invokes
the corresponding backend verifier, and lifts its final point. One defect
was found and fixed: the conditional-convex replay route initially dropped
the caller's `max_table_states` cap. It now forwards that cap explicitly.

The additional command actually run was:

```sh
python3 research-20261002-decomposition/completion/reviews/check_recourse_routes.py
```

It passed 23 composed cases covering convex, submodular, and automatic routes;
exact and additive output; exhausted deadlines; zero QP operation budgets;
zero submodular cut budgets; and original-index mapping after fixed-variable
substitution. Every returned interval contained the independently enumerated
optimum. Six altered inner-model certificates and one deliberately inadequate
replay budget were rejected.

The further targeted command, from the solver directory, was:

```sh
python3 -B -m unittest test_recourse test_convex_recourse -v
```

All 19 tests passed. No unresolved routing, model-binding, or certificate
composition defect was found in this follow-up scope.

The final input-hardening suggestion was also implemented: wrapper time limits
must be finite, nonnegative numeric values. NaN, infinity, a negative value,
Boolean input, and a numeric string are now rejected. The zero-time regression
includes all five invalid cases. The targeted command
`python3 -B -m unittest test_recourse.RecourseTests.test_zero_time_returns_original_certified_bounds -v`
passed after this change. This review has no remaining open defect or
hardening request.

## Final review: forced affine-map recognition

A performance change now bypasses the selector LP when the common central
gradient leaves a nonsingular zero-gradient principal block. This is sound
for both acceptance and rejection. Every nonzero central gradient fixes its
coordinate at the corresponding bound. Every zero central gradient requires
an identically zero affine gradient, including a coordinate whose central
optimizer happens to lie at a bound with zero multiplier. If the remaining
principal block is nonsingular, those identities determine exactly one
possible affine offset and slope. Whole-box KKT verification accepts that
map or proves no affine selector exists. The full private Hessian may be
singular; only the remaining principal block needs to be nonsingular. A
singular remaining block still uses the complete LP procedure.

The candidate-order change tries fewer attachments and then smaller blocks.
It affects only a documented heuristic; all accepted blocks and composed
certificates receive the same exact checks.

The following additional targeted commands passed:

```sh
python3 research-20261002-decomposition/completion/reviews/check_affine_fastpath.py
python3 research-20261002-decomposition/completion/reviews/check_affine_pipeline.py
```

The first compared 63 examples against a forced complete-LP fallback; 54
used the new forced-map path. The examples include a singular full private
Hessian with a nonsingular free face, a strictly active zero-curvature
coordinate, and zero central multipliers at bounds. Every classification
agreed, and both implementations' accepted maps passed the exact verifier.
The second reran the earlier 80 scalar and 24 planted PSD-block checks and
both protocol-tamper rejections.

From the solver directory, the targeted regression
`python3 -B -m unittest test_recourse.RecourseTests.test_forced_affine_map_skips_lp_and_leaf_discovery_stays_small -v`
also passed. It forbids an unnecessary LP in the two forced-map rejection
cases and verifies the original-domain certificate on the 17-variable star.
No unresolved defect was found in the performance change.
