# Independent review: exact dense recovery from surrogate cells

Date: 2026-09-06. Reviewer: independent subagent `screening_review1`.
Scope: the theorem and proofs in
[bilevel-reopened-approximate-structure.md](bilevel-reopened-approximate-structure.md).
The reviewer did not author the theorem or import its companion implementation.

**Verdict: the core exact-recovery theorem passes mathematical review.** The
perturbation enclosure, rational screening, arbitrary-size dense free-block
elimination, and exact KKT cover are sound under the stated positive-definite
box-QP assumptions. This is a correctness review, not an independent claim of
publication priority or demonstrated computational advantage.

## Proof audit

1. Write `e=z-y` and `p=(Q-Qhat)y`. The true follower VI gives
   `(Qz+a)^T e<=0`, and the surrogate VI gives `(Qhat y+a)^T e>=0`.
   Subtracting gives `e^T Qe+p^T e<=0`. Completing the square gives the
   stated ellipsoid. Its directional support formula is exact as a support
   calculation; it is correctly distinguished from the actual response set.
2. The surrogate response and residual are affine on a valid supplied cell.
   The maximum residual energy occurs at a vertex because that energy is a
   convex quadratic. This argument includes cells of lower affine dimension
   and singleton cells. Vertex enumeration is polynomial in fixed ambient
   dimension; it is essential that this dimension is fixed.
3. Applying the directional formula to a coordinate gives the stated primal
   center and radius. Applying it to the corresponding column of `Q` gives
   gradient center `ghat_i+p_i/2` and radius `sqrt(Q_ii eta)/2`.
   The signs and factors are correct.
4. Strict positive gradient forces the lower bound; strict negative gradient
   forces the upper bound. A primal upper enclosure at zero or lower enclosure
   at one permits a weak inequality because the true response lies in the
   box. The strict interior test forces zero gradient. Radical comparisons
   can be implemented by rational sign checks and squaring, with an explicit
   sign check before squaring.
5. Every principal free block of `Q` is positive definite. Its exact inverse
   therefore gives the stated rational affine free response without a bound
   on the free-set size. The remaining gradient signs and box restrictions
   are exactly the box KKT conditions. Sufficiency follows from convexity;
   uniqueness follows from positive definiteness.
6. Every true response has a completed status assignment compatible with
   all sound certificates. A bound coordinate with zero gradient can be
   represented as free, lower, or upper where applicable. Using weak
   inequalities in the recovery LPs retains these degeneracies. Duplicate
   representations do not lose or add true response points.
7. Each recovery LP is a closed subset of a compact cover cell, so every
   nonempty LP attains its rational optimum. The finite union covers the
   true feasible graph even with response-dependent upper equalities.
   Thus global feasibility and the minimum over all recovery LPs are exact.
8. The signed-output inner/outer bounds have the correct inequality
   directions. An outer minimizer need not be feasible; an inner minimizer
   does certify a true feasible leader. Empty inner sets do not prove
   infeasibility. No unproved objective-loss bound is being inferred.

One counting clarification was requested: `M 3^t` counts **recovery LPs**.
The screening procedure also describes affine LP calls. Alternatively, all
screening extrema can be evaluated at the already-enumerated cell vertices,
which needs no additional LP solves. This is a wording issue, not a runtime
or correctness obstruction.

## Useful strengthening found during review

The original strict interior screening rule can produce artificial ambiguity
on a closed surrogate cell even when `Q=Qhat`: a free response may touch a
clipping threshold only at the cell boundary. For zero gradient status `F`,
the following weak-closure certificate is sound:

```
min_P s_i >= R_i,       max_P s_i <= 1-R_i,
max_P s_i > R_i,        min_P s_i < 1-R_i.
```

Both affine slack functions `s_i-R_i` and `1-R_i-s_i` are nonnegative
and not identically zero on `P`. Each is therefore strictly positive on the
relative interior of `P`. The response is interior and its gradient is zero
there. The response is continuous in the leader (indeed the fixed strongly
convex box QP has a Lipschitz response), so the gradient vanishes throughout
its closure `P`. This argument also covers lower-dimensional cells. On a
singleton the conditions require actual strict interiority.

The same reasoning gives optional gradient refinements: `min_P t_i>=S_i`
and `max_P t_i>S_i` certify `L`; the sign-reversed version certifies `U`.
These are sound because the gradient has the required strict sign on the
relative interior, and the corresponding response bound extends by
continuity. The author was informed and agreed to adopt the refinement.

## Independent exact-arithmetic experiments

Run:

```
python code/bilevel_reopened/screening_review_checks.py
```

The [independent script](../code/bilevel_reopened/screening_review_checks.py)
uses SymPy rational arithmetic and no functions from the implementation
under review. It constructs diagonal surrogate cells for a scalar leader,
dense positive-definite rational true Hessians, and exhaustive true KKT
active-set descriptions. It checks exact interval coverage by the reduced
status enumeration, all certified statuses, directional ellipsoid bounds,
and exact optimum/feasibility agreement under randomly signed affine
objectives and response-dependent upper inequalities. Separate cases check
singleton cells, zero residual, zero-gradient bound degeneracy, and the
weak-closure free certificate at both clipping endpoints.

Recorded output on 2026-09-06:

```json
{
  "seed": 97013,
  "random_cases": 24,
  "cells": 61,
  "certified_statuses": 112,
  "recovery_assignments": 549,
  "full_assignments": 3213,
  "directional_checks": 918,
  "singleton_zero_residual_degeneracy": "passed",
  "weak_closure_free_status": "passed"
}
```

These are regression and arithmetic checks, not performance benchmarks.
They exercise scalar-leader diagonal surrogates and dense true followers;
the general fixed-dimensional surrogate-cover argument was checked
mathematically above. The counts do not support a claim about application
speed or typical ambiguity.

## Follow-up audit: explicit small-perturbation neighborhood

The completed Section 3a was independently checked after its addition.
**The corollary also passes.** In particular:

- A valid surrogate cell projects injectively to the leader coordinates.
  A linear projection injective on a polytope is injective on its affine
  hull: otherwise a small segment in a kernel direction through a relative
  interior point contradicts injectivity. The cell dimension is at most
  `r`, so triangulation with original vertices uses at most `r+1` vertices
  per simplex. The union of their transition coordinates has size at most
  `(r+1)q`.
- A nominal status outside that union has positive relevant margin at every
  simplex vertex. A zero margin would exactly be the defined transition
  condition. Affine interpolation preserves the minimum margin throughout
  the simplex. The finite nonempty margin list has a positive rational
  minimum; the stated empty-list convention is harmless.
- For symmetric `E`, `||E||_2<=||E||_infinity`. The computable reciprocal
  inverse-norm bound on `lambda_min(Qhat)` is valid because `Qhat^{-1}` is
  symmetric positive definite. Weyl's inequality then gives
  `lambda_min(Q)>=m/2` at the allowed radius.
- The VI yields `||z-y||_2<=2 eps R/m`. The identity
  `gtrue-ghat=Qhat(z-y)+Ez` gives the stated gradient perturbation bound.
  The factor four in the radius ensures both perturbations are at most
  `sigma/2`, including equality at the radius, so the required status
  signs and primal interior margins remain strict.
- These sensitivity-based status certificates can be supplied directly to
  the main theorem. They need not be inferred from the particular ellipsoid
  screening test. The corollary therefore guarantees its claimed ambiguity
  bound regardless of which optional screening refinements are implemented.
- Rational triangulation in fixed dimension has polynomial size and bit
  complexity. The text correctly allows the polynomial degree to increase
  and does not silently retain the earlier arrangement exponent.

An additional independent exact experiment in the same script uses an
8-coordinate dense true Hessian and identity surrogate. Every original
vertex has at most one transition coordinate; the guaranteed ambiguity is
at most two. The perturbation infinity norm is `51/100000`, the positive
vertex margin is `1/10`, and the observed maximum ambiguity is exactly two.
All coordinates outside each simplex's transition union are certified by
exact rational screening. This is an arithmetic illustration, not a claim
that a useful perturbation radius or low transition multiplicity is typical.

The LP-count wording has also been resolved: the theorem now explicitly
counts recovery LPs, and screening extrema may use the existing vertices.
