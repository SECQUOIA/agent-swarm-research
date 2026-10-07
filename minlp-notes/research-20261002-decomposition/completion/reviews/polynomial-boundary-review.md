# Independent polynomial boundary implementation review

Date: 2026-10-03. Reviewed `solver/polynomial_boundary.py` and
`solver/verify_polynomial_boundary.py`, including their use of retained-box
certificates from the polynomial grid solver. The polynomial grid verifier's
containment contract was inspected; this review does not replace the separate
review of the full polynomial solver.

**Result:** no unresolved soundness defect was found. The implementation
certifies one original global optimizer, either as an explicit rational point
or as the unique minimizer of a uniformly strongly convex polynomial on a
rational face box. In the latter case, the artifact does not provide an
explicit rational optimizer or rational optimal value. The optimizer may be
irrational. Weak monotonicity reductions need not preserve every original
optimizer, so original uniqueness is not claimed.

## Argument checked

The replayed grid trace supplies a box containing every original global
optimizer. Given such a box, a nonnegative coordinate derivative permits
clamping that coordinate to its retained lower endpoint without increasing the
objective; a nonpositive derivative permits the analogous upper clamp.
Starting from one retained global optimizer and applying each recorded clamp
therefore preserves minimum value and at least one global optimizer. Repeating
the derivative scan after every reduction is necessary because one clamp can
resolve another derivative's sign. The implementation conservatively requires
the clamped endpoint to be an original endpoint.

After all integer coordinates and clamped continuous coordinates are fixed,
the remaining face box is convex and compact. Let `H0` be the midpoint Hessian
restricted to its free coordinates. The certificate computes an exact interval
for every restricted Hessian entry and a maximum row-sum error `delta` about
`H0`. Hessian errors are symmetric, so their spectral norm is at most that
row-sum bound. Thus `H0 - delta I` positive definite implies a uniformly
positive-definite Hessian on the entire face box. The restricted objective has
one unique minimizer, and preservation of an original optimizer makes that
minimizer globally optimal for the original problem.

A zero-gap grid certificate directly certifies its feasible rational point.
If no free coordinate remains after monotonicity reduction, the single face
point is globally optimal by preservation. Unfixed integer domains are rejected
before an implicit convex-face certificate can be issued.

## Review improvement

The first verifier used the producer model's derivative-bound and Hessian
methods to check the derivative and curvature claims. The author replaced
these calls with the polynomial grid verifier's independent monomial interval
calculation, evaluated on the current box or singleton midpoint as appropriate.
A monkeypatch test now makes both producer methods raise exceptions while the
certificate verifier still succeeds.

The automatic wrapper reruns certified global grids at accuracies
`1, 1/4, 1/16, ...`. Its documentation correctly describes a capped restart
search and makes no theorem-level FPT or dovetail complexity claim. Failure of
its sufficient interval tests is inconclusive, not failure of global
optimality, uniqueness, or class membership.

## Independent targeted checks

Run from the repository root:

```sh
python3 -B research-20261002-decomposition/completion/reviews/check_polynomial_boundary_review.py
```

The command passed. Its fixtures check:

- a discovered patch containing the irrational global optimizer `(sqrt(2), 0)`;
- independent replay with producer derivative/Hessian methods disabled;
- four corruptions of derivative signs, endpoint selection, Hessian values,
  and the Hessian error bound, all rejected;
- a coupled objective requiring a repeat monotonicity scan before returning
  the exact point `(1, 0)` with value `-1/2`;
- weak clamping that selects one member of a nonunique original optimal set;
- a restricted convex patch when the original full Hessian is indefinite;
- rejection of an unfixed native-integer domain;
- inconclusive termination on a zero runtime budget.

These checks establish bounded correctness evidence and are not performance
benchmarks. No project-wide verification or CI inspection was performed.
