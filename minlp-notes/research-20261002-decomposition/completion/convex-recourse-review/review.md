# Independent review of conditional convex value factors

Reviewed the implementation in [convex_recourse.py](../../solver/convex_recourse.py),
its focused tests, and the supporting [oracle composition theorem](../../negative-curvature/sparse-convex-value-factors.md).
The implementation uses continuous private box QPs, supplied private blocks,
and a residual tree decomposition whose complete factor scopes are checked.

No remaining bound, pruning, lifting, or exact-acceptance defect was found in
this reviewed scope. Two issues found during review were corrected: the
verifier now rejects an exact request paired with a nonzero-gap `certified`
status, and zero-tolerance refinement continues to reduce its internal accuracy
target instead of repeatedly stopping refinement at a fixed target.

## Mathematical and implementation checks

For every fixed private feasible point, its contribution is affine in the
retained parameters. The conditional minimum is therefore concave, including
at changes of active face and when the private Hessian is singular. Adding the
direct retained quadratic leaves a coordinate upper-curvature bound equal to
its positive diagonal part. The private box must be independent of the
retained point, as it is here.

The reviewer checked the incident-node correction directly. Every endpoint of
a rounding cell carries a radius at least that cell's width, so its penalty
covers the upper interpolation error. Native integer gaps greater than one
use the same admissible integer-endpoint rounding. Unit gaps need no
correction because every feasible integer is already an endpoint. Nonpositive
direct diagonals require only the two current interval endpoints and zero
correction. These statements concern upper curvature and remain valid when
the full original Hessian is indefinite.

Subtracting each unary correction once gives a lower-bounding finite objective.
For a retained coordinate lying in a cell, the smaller corrected min-marginal
at its two endpoints is a lower bound on every original feasible point with
that coordinate. Filtering at the incumbent therefore preserves every global
optimizer. Restarting a conditioning trial restores the original box; earlier
valid lower bounds and feasible incumbents remain valid. Growth and a correct
conditioning guess affect efficiency, not proof validity.

The implementation checks disjoint private blocks, rejects private integer
coordinates and interactions between distinct private blocks, and recomputes
all attachment scopes from the original Hessian. It checks complete factor
coverage in the residual decomposition. Each saved query is tied to its block
and parameter vector. PSD, private feasibility, nonnegative multipliers,
stationarity, complementary slackness, and its rational objective establish
each conditional value. The verifier rebuilds finite tables from these checked
values and the original model. Passing an expected model also checks the
embedded model, rather than trusting a claimed model identifier.

The exact-output gate uses the original quadratic's rational value-height
bound. If the feasible incumbent has denominator `q` and every original optimum
value has an attaining representative of denominator at most `R`, a positive
value difference is at least `1/(Rq)`. The independently certified smaller gap
therefore proves equality. Approximate candidate generation and guessed growth
constants do not establish acceptance. Private QP and LP optimization are not
called during certificate replay; finite-tree minimization is recomputed.

## Targeted checks actually run

The maintained independent harness is
[check_convex_recourse.py](check_convex_recourse.py). The commands run were:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -B research-20261002-decomposition/completion/convex-recourse-review/check_convex_recourse.py
python -B -m unittest discover -s research-20261002-decomposition/solver -p test_convex_recourse.py
```

The independent harness passed:

- 18 one-retained-coordinate instances with exact piecewise-quadratic reference
  minima, including clipped responses, zero-curvature private variables,
  fixed private variables, continuous and integer retained coordinates, and
  positive or nonpositive direct curvature.
- 24 four-variable instances against independent exact active-face enumeration,
  with two retained variables, coupled two-variable PSD private blocks,
  singular private Hessians, and mixed integer domains. Nine returned exact
  bounds and 15 met the requested `1/20` gap.
- 18 JSON certificate replays while QP and LP optimizers were replaced by
  functions that raise an exception if called.
- 126 altered or incomplete mathematical certificates and three invalid
  exact-request flags, all rejected.
- Four ordinary resource-limit cases, and four cases with no retained variables:
  zero levels, zero time, zero local QP faces, and a single allowed finite-table
  state. All returned valid original-model bounds with the appropriate status.

All nine focused implementation tests also passed. Separate direct probes
checked eight approximate/exact combinations with all-private, singular,
zero-block, and fixed-private models. A deliberately ill-conditioned example
with coupling `1023/1024`, with optional scalar tightening disabled, needed 44 completed levels across conditioning trials
`2,3,4,5`, with 912 local KKT records, to meet gap `10^-6`; its complete
certificate replayed successfully. At a 100-level cap its exact-mode run
correctly reported an incomplete result with valid bounds.

These are finite correctness and resource-behavior checks, not a performance
comparison. The local active-face QP implementation may take exponentially
many faces. Its limits are reported honestly. Cooperative time checks are not
hard operating-system deadlines. No project-wide verification or CI inspection
was run for this review.


## Integration of scalar piecewise curvature certificates

The scalar preprocessing hook was reviewed after its addition. It rebuilds
private-only `Block` data from the original objective, without allocating the
direct retained quadratic to that block. Coverage and the complete affine KKT
identities certify every private value piece. The maximum piece Hessian is
nonpositive. Each such bound is added to the original retained diagonal, and
the positive part is taken only after summing all contributing scalar blocks.
The verifier reconstructs the same original block, decodes exact rational
strings, checks the complete certificate, rejects duplicate block records,
and computes the bound itself. It never trusts a supplied curvature number.

The use of piece Hessians is justified across interfaces: after subtracting
the direct parameter quadratic, a private value function is concave, so its
one-sided derivative can jump only downward. The partition is complete and
its pieces equal that same value function. A maximum of their second
derivatives therefore gives an upper-curvature bound on the full interval,
including active-set changes. This reasoning would fail for arbitrary
piecewise quadratic functions with upward derivative jumps.

The extended independent harness additionally passed:

- Three changing-response instances
  `M(y1+y2-z)^2 + (y1-2z+1/2)^2 - z^2`, with `M=1,100,10^6`,
  `z` in `[0,3/4]`, and private variables in `[0,1]`. Their independently
  derived exact minima are `-(8M+9)/(16(M+1))`. All three used eight levels
  and nine local QP records and returned the identical gap `27/1048576`,
  below the requested `10^-4`. The certified retained curvature is six,
  while the direct curvature is `2M+6`.
- Replays of all three while private QP, LP, and scalar-partition construction
  were disabled. The saved partition is checked, not reconstructed.
- Nine corrupted scalar proofs, covering changed value coefficients,
  missing coverage, and duplicate records, all rejected.
- Two exact endpoint examples with two scalar blocks attached to one retained
  coordinate. Each block contributes curvature `-2`; summing with direct
  curvature three gives `-1`. Both continuous and integer retained domains
  were solved in one level with exact values `-1/2` and `-9/2`.

Including the conditioning example, the maintained harness now checks 48
instances against independent exact minima, 138 invalid mathematical or
metadata proofs, 21 optimization-free replays, and the eight explicit
resource cases described above. The local pattern constructor is deliberately
capped and requires positive definiteness and nonfixed intervals. Unsupported
blocks retain the direct bound. No general short-partition or negative-curvature
complexity conclusion follows from these implementation results.
