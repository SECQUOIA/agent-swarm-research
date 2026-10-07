# Independent review of exact rational output

The exact-output wrapper and its verifier have no remaining blocking
correctness finding from this review. The review covers
[`exact_output.py`](../solver/exact_output.py), the exact-schema dispatch in
[`verify_certificate.py`](../solver/verify_certificate.py), and the warm-start
and stage-accounting changes in
[`certified_grid.py`](../solver/certified_grid.py). It does not independently
review the later shared `finite_dp` implementation or automatic decomposition;
those have separate reviews.

## Mathematical checks

Let `D` clear the denominators of `A/2`, the linear coefficients, the constant,
and the original box endpoints. Fix an optimal integer slice and choose a
continuous optimal box face of minimum dimension. At an optimizer in its
relative interior, the free Hessian is positive semidefinite and nonsingular.
Otherwise a null direction has zero linear and quadratic change, so it reaches
a smaller optimal face. This argument covers ties and singular full Hessians.

After substituting `u = D x`, the free stationarity system has integer matrix
`D A[J,J]` and an integer right-hand side. The product `H` of the maximum of
one and each original continuous row's absolute row sum bounds the absolute
determinant of every nonsingular free principal submatrix. Cramer's rule gives
one optimizer with a common coordinate denominator at most `R = D H`.
Its objective therefore has denominator at most `V = D R^2`. Fixed rational
coordinates and integer coordinates share this common denominator. The bound
uses original endpoints, so refinement does not change it.

A feasible rational candidate of value `v`, whose reduced denominator is `W`,
is globally optimal if a valid lower bound `LB` satisfies
`v - LB < 1/(V W)`. Two distinct rationals with denominators at most `V` and
exactly `W` differ by at least this quantity. The strict inequality in the
implementation is necessary. No stationarity, face-identification, or supplied
growth assumption is needed for this acceptance rule.

Under unique-optimizer quadratic growth, the default conditioning schedule
can eventually certify sufficiently small errors as resource caps increase.
Once an incumbent is within `1/(4 R^2)` of the unique optimizer, bounded-
denominator coordinate reconstruction recovers it. Once the certified value
gap is below `1/V^2`, the separation gate accepts. This particular argument
does not rely on the face proposal. The separately reviewed near-set recovery
argument below extends finite termination to arbitrary nonunique optimal
sets, without an efficient general complexity bound. Arbitrary optional
schedules, especially a fixed-slope adaptive schedule, remain outside that
termination statement.

## Certificate and resource checks

The verifier recomputes the heights from the original model, verifies every
nested lower-bound certificate, checks each recovered proposal's original
feasibility and objective, and checks the exact separation inequality.
Warm starts and recovered stationary points only improve feasible upper
bounds. Their claimed source or stationarity does not establish exactness.

The review found one resource issue: singular-face LP recovery originally
omitted the wrapper's time-budget callback. The call now passes the callback,
so checks occur during the LP rather than only before and after it. A single
rational operation or pivot can still finish after a cooperative time cap.
Certificate validity does not authenticate reported runtime statistics.

## Reproducible targeted checks

Run from the repository root:

```sh
python research-20261002-decomposition/completion/reviews/check_exact_output_review.py
```

The [review script](reviews/check_exact_output_review.py) uses SymPy only for
an independent exhaustive face oracle. It enumerates integer slices and box
faces, solves nonsingular free stationarity equations, and evaluates all
feasible candidates. It does not use the solver's candidate generator or LP
oracle to obtain reference optima. The seeded sample contains 36 rational
problems of dimension one through three, including mixed-integer and fixed-
coordinate cases.

The command passed after the shared-DP and automatic-decomposition changes:

- All 36 computed reference optima and witnesses satisfied the height bounds.
- All 36 generated certificates replayed and their bounds contained the
  independently computed optimum. Twenty runs returned exact answers and
  sixteen stopped at their stage cap.
- The singular stationary face of `(x+y-1/3)^2 + z(1-z)` produced the feasible
  optimal candidate `(0, 1/3, 0)`. Its capped wrapper certificate replayed with
  `round_limit` status.
- Four corruptions were rejected: an altered height bound, a different nested
  model, an infeasible recovered proposal, and an incorrect final upper bound.
- Separate time, stage, and table limit results retained valid certificates.

The checks use small finite samples and are evidence against implementation
regressions, not proofs of unrestricted convergence or performance. Runtime
limits can change the distribution of statuses on a slower machine; the
script requires correct bounds and certificates regardless of status. No
project-wide checks or CI inspection were performed for this review.

## Addendum: arbitrary nonunique optimal sets

The strengthened theorem in [exact-output.md](exact-output.md), under
"General finite recovery, including nonunique optimal sets," survives the
additional adversarial review. It proves finite completion of the default
algorithm for every bounded rational mixed box QP as all relevant resource
caps increase. It does not prove a general efficient rate or construct a
representation of the entire optimal set.

The two additional arguments are sound, including the following details.

1. **Snapping near the optimal set.** Choose a nearest optimizer `s` to a
   feasible point within `tau/2`, where `tau=1/(4nR)`. Integer labels agree.
   Original distinct endpoints differ by at least `1/D`, so a coordinate
   active at `s` cannot be snapped to its opposite endpoint. Fixed rational
   coordinates remain fixed. The original-face stationary polytope `P` is
   nonempty and compact; all its points have the same optimal objective.
   At a vertex, independent stationarity rows together with bound rows have
   determinant controlled by `H`. Expanding the bound rows leaves a
   potentially **nonprincipal** minor, which is still bounded by the same
   product of original continuous row norms. Thus the sum of the additional
   endpoint slacks, if positive at a minimizing vertex, is at least `1/R`.
   At `s` that sum is at most `3n tau/2=3/(8R)`. It must therefore have minimum
   zero. This supplies an optimal anchor satisfying every extra snap
   simultaneously. Any feasible solution of the implemented remaining
   stationarity equations differs from the anchor by a vector in the
   reduced Hessian's nullspace, and has exactly the same objective. This
   last assertion does not require the reduced system to be nonsingular.

2. **Approximation without growth.** For a target accuracy, let `J` be the
   existing last trial stage. At any trial with
   `mu>=max(2,J)`, its slope obeys `theta<=2^-J`. At stage `J`, every gap
   requiring a positive-curvature correction is at most `2h_J`; integer
   unit gaps require no correction. The feasible grid minimizer and its
   corrected bound have gap at most `Ln h_J^2/2 <= 4 epsilon/7`.
   The coordinate cap cannot prevent this trial: continuous steps are at
   least `h_j`; integer steps are at least `h_j/2` when `h_j>=1` and at least
   one otherwise. Since every retained interval has width at most the
   original scale, every coordinate grid through stage `J` has at most
   `2*2^J+3` nodes. This is below the trial cap. All preceding trials are
   finite. Sufficiently large external stage and table caps therefore
   permit completion. Zero original width and zero positive coordinate
   curvature have direct exact or finite endpoint-DP treatment.

Compactness then makes sufficiently accurate feasible incumbents close to
the full optimal set. The first argument supplies an exact candidate, and
the existing value-separation gate eventually accepts. Each relevant exact
LP terminates under Bland's rule with enough pivots. Only finitely many
integer assignments and snapped faces occur for a fixed bounded input, so
finite resource caps sufficient for a successful finite prefix exist.
No quantitative distance-to-set estimate is required for this existence
argument.

The reproducible review script now also checks six near-set recoveries on a
model with two disconnected optimal line segments, an integer coordinate,
a fixed rational coordinate coupled to a free variable, and a singular free
Hessian. The six points exercise both integer labels and interior, extra
lower-bound, and extra upper-bound snaps. Each point is explicitly within
`tau/2` of a known optimizer; every recovered solution has the exact optimal
value. The lower and upper cases each require two extra snaps to hold
simultaneously. A separate nonconvex problem with two continuous optimal
segments certifies the target `1/100` using the grid with convex presolve and
polishing disabled. Its certificate replays with gap `421601/67108864`.

The command above was rerun successfully with these added checks. The
previous 36 reference comparisons, four tamper checks, and three limit
checks still pass. These examples exercise the argument's delicate cases;
the finite-completion theorem rests on the proof, not on this finite sample.
