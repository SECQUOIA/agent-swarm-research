# Independent solver and certificate review

The reviewed implementation and checker have no unresolved correctness
defect identified by this review. This conclusion concerns the rational
box-QP certificate contract and the stated approximation method. It is not
a proof of the software or evidence of competitive solver performance.

The review read `AGENTS.md`, the continuation `PROGRAM.md`, the solver,
checker, tests, README, and the October 2 `pruned-coordinate-grid.md`
theorem. It made no edits to the solver or checker. Source hashes and the
recorded check output are in [review-checks.txt](review-checks.txt).

## Mathematical checks

- The independent-factor initial lower bound minimizes each diagonal
  term over its actual continuous or integer interval, and each bilinear
  factor over the rectangle corners. Summing these minima is valid.
- The correction uses half the positive diagonal curvature times a
  variance bound of one quarter of interval length squared. Independent
  mean-preserving rounding reproduces every off-diagonal bilinear term.
  Adjacent integer unit intervals need no correction because a feasible
  integer cannot lie strictly between their endpoints.
- Nonpositive-diagonal coordinates can use only endpoints: conditional
  concavity gives an endpoint solution no worse than any interior point.
  Their zero correction is valid for the lower bound and for conditioned
  interval bounds. The implementation retains interval hulls, rather than
  asserting that all global optimizers are endpoints.
- Every directed message is checked against its full Bellman equality.
  On a tree these equations determine the messages from the leaves, so
  no unsupported circular message bound is accepted. The checker verifies
  complete separator coverage and every unary min-marginal independently.
- An interval whose endpoint min-marginals both exceed the feasible upper
  bound cannot contain a global optimizer. Taking the hull of retained
  intervals weakens pruning safely. Original-box lower bounds survive
  subsequent filtering and restarts.
- The PSD check verifies the full identity `A = L diag(D) L^T` with
  nonnegative `D`. Together with exact feasibility and box KKT signs this
  suffices even for a singular Hessian. A mixed-integer point accepted by
  this continuous certificate is globally optimal for the mixed domain.
  Failed presolve is correctly treated as inconclusive.

## Conditioning schedule

An additional read-only schedule audit found no discrepancy in the
default positive-tolerance algorithm. The trial stage cap matches the
theorem; cap failures restart before DP allocation; all previous proved
lower bounds remain available; and centers inside a trial are the
corrected-grid witnesses. A restart may use any original-box feasible
incumbent, whose squared distance to an optimizer is at most `n*s^2`.

The following proof qualifications were sent to the implementation author
for the README:

1. The width-and-conditioning bound applies to the default **pruned
   geometric** schedule. The uniform and unpruned ablations retain valid
   bounds, but do not inherit that complexity assertion.
2. Endpoint-only coordinates need a separate counting argument: they
   contribute zero correction and at most two labels. Their long intervals
   do not satisfy the geometric mesh estimate. Apply that estimate only
   to positive-diagonal coordinates.
3. Rational coordinate polishing introduces denominators beyond those in
   the original grid-only proof. Each update involves only the existing
   common denominator and fixed input coefficient factors. With a fixed
   number of sweeps, bit length grows polynomially over the bounded number
   of coordinate updates. This extends the arithmetic argument without
   changing the convergence or certificate proof.

Without growth or uniqueness, a sufficiently small trial slope makes the
positive-diagonal rounding error small enough at its final stage; the
coordinate cap admits this trial. This supports the stated eventual
positive-tolerance convergence when resource limits are removed. Zero
tolerance invokes a different schedule and does not promise general exact
continuous reconstruction.

## Independent finite checks

The targeted command actually run was:

```bash
timeout 10s python research-20261002-decomposition/solver/reviews/review_checks.py
```

It exited successfully. The deterministic 32-instance suite includes
continuous, integer, and mixed two-variable problems with positive and
negative diagonal terms and nonzero coupling. Its independent exact
reference enumerates box corners, edge stationary points, and interior
stationary points, or enumerates integer assignments and solves the
remaining scalar problem. For singular continuous systems, any interior
stationary optimum has an affine set of equally valued stationary points
reaching the boundary, so the boundary candidates suffice.

All returned bounds bracketed the exact optimum; all 88 completed stage
certificates replayed; and every retained product box contained at least
one enumerated exact minimizer. Presolve was disabled to exercise the DP
and filtering themselves.

Three additional controlled interruption checks passed:

- An interruption during initial primal improvement preserves a previously
  improved feasible upper bound in the initial proof record.
- An interruption during polishing after a complete DP preserves that DP
  certificate.
- A coordinate-cap trial abort consumes an attempted stage, restarts with
  the next trial, and retains a replayable result. This test injects the
  exception to isolate control flow; it does not measure actual cap growth.

A separate small manual check used `(x-y)^2` on `[0,1]^2`, tolerance
`1/1000`, no convex presolve, and 11 attempted stages. It exercised natural
restarts at completed stages 0 and 7, returned a valid incomplete bound
with gap `6561/524288`, and replayed all 742 table states. The saved core
test suite now also contains a natural-restart regression added by the
implementation author. Its test results are reported by that author, not
counted as independently rerun here.

## Limits of this review

Replay validates the rational model embedded in the certificate. A caller
must separately establish that this model is the intended original input.
The solver and checker share model parsing, structural validation, and
objective evaluation, so replay does not independently validate those
shared components. Code inspection and small exact examples support them
but do not remove this shared trust boundary.

The time limit remains cooperative and the table-state cap is not a byte
or total-proof-size bound. The reported scalability limits from exact
rational arithmetic, bag width, proof retention, and replay are material.
Coupled constraints, automatic decomposition, polynomial objectives,
inexact arithmetic, and exact continuous reconstruction are outside this
implementation. No project-wide checks or CI inspection were performed.
