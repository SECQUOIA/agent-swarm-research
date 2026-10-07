# Independent review of the noisy convex core evaluator

Date: 2026-10-02. Status: actual-file mathematical review passed.
No unresolved correction is requested. Focused prior comparison remains
separate; this review makes no novelty claim.

This review covers the complete saved
[joint-convex-core-point-oracle.md](joint-convex-core-point-oracle.md),
including the homothetic-copy inner ball, the precise weak-optimization
contract, every-draw correctness, and the simultaneous precision bound.
The reviewer did not edit the main note.

## Interfaces and scope

The theorem concerns an explicit fixed-degree rational polynomial convex
on a bounded rational polytope. Convexity verification is supplied or
charged. The polynomial-time claim is for feasible objective approximation
and distance to the selected optimizer's perturbed coordinates. It does
not approximate unperturbed residual coordinates to any optimizer.

The independently reviewed
[convex-polytope interface](convex-polytope-value-interface.md) supplies
the needed rational feasible value approximation and exact lexicographic
fallback. Its [review](../reviews/convex-polytope-value-interface-review.md)
is now saved and its status is synchronized. Rational relative-coordinate
reduction handles lower-dimensional polytopes, while singleton domains
are evaluated directly. The fallback's base exponential factor is
independent of sampled coefficient height and requested precision.

Only Section 2 of the
[coupled core note](coupled-polytope-core-oracle.md) is used for the
projected-growth tail. That compact-domain proof and its two-block
finite-format transfer do not depend on the separate coupled-value
cell-count theorem. The present proof therefore has no dependency on
the pending review of that cell algorithm. Residual ties are allowed;
positive projected growth forces a unique optimal core unless the
projected domain is already a singleton.

## Buffered sublevel geometry

A feasible incumbent of value gap at most `delta` gives the convex set
`K={F_gamma<=U+delta} intersect P`. It contains the incumbent and every
global optimizer; every point in it has gap at most `2delta`.

In relative coordinates, let the polytope contain `B(0,r_R)` and let
`W>=max(1,sup_R |psi|)`. With the main note's
`lambda=min(1/2,delta/(8W))`, the whole set

```text
(1-lambda) w_y + lambda R
```

lies below `U+delta/4`. Indeed convexity bounds its objective by
`(1-lambda)U+lambda W<=U+2lambda W`. This proves the inner ball of
radius `r=lambda r_R` around `c=(1-lambda)w_y`. It does not require a
gradient bound or interiority of an optimizer. The outer radius
`2R_R` around `c` is valid because both `c` and the sublevel set lie
in `R subset B(0,R_R)`.

All relevant rational encodings have length polynomial in `I+b+q`.
The radii can be numerically small, but their inverse logarithms have
that same bit bound. Fixed degree ensures that affine substitution
and coefficient bounds have polynomial size. Separation first checks
the linear domain, so tangents use convexity only on the polytope.
A violated sublevel query inside the polytope has a nonzero tangent
normal, since the sublevel is nonempty.

## The weak-optimization contract and outward extrema

The reviewer read the local primary-source statement in
[GLS, Definition 2.1.10, printed p. 50, and Corollary 4.2.7, printed p. 106](../../literature/papers/grotschel1988-geometric-algorithms-and-combinatorial-optimization/fulltext.md).
Definition 2.1.10 accepts an arbitrary rational objective vector and
uses an absolute objective error `eta`. It does not impose a unit-norm
objective restriction. This distinction matters after a nonorthogonal
relative-coordinate transformation.

For either original coordinate objective `p=+v_i` or `p=-v_i`, its
range width on the sublevel is at most one. Homothety toward the known
ball maps a maximizer to the eroded body and loses at most `eta/r` in
objective. The eroded body is nonempty when `eta<=r/2`. GLS therefore
returns a rational weak point satisfying

```text
p(w_hat) >= max_K p - eta(1+1/r).
```

Its distance at most `eta` to the sublevel also gives
`p(w_hat)<=max_K p+A_i eta`, with rational `A_i>=||a_i||_2`.
Thus `p(w_hat)+eta(1+1/r)` is a certified outward extremum with error
at most `eta(A_i+1+1/r)`. Choosing the stated `eta_i` makes the error
at most `zeta`. No nonlinear feasibility repair of `w_hat` is needed.
Affine constant terms are added after linear optimization.

These are exactly `2k` polynomial-time calls. Large numerical affine
coefficients are accounted for by their rational bit lengths and by
`eta_i`; they introduce no numerical inverse-condition factor. Clipping
the resulting intervals to `[0,1]` preserves both every optimal core
and the saved feasible incumbent core.

## Correctness, fallback, and one event for all precisions

The rational squared-diameter test is sound on every draw, without a
growth assumption. If it passes, the saved incumbent is within the
requested Euclidean core distance of the fixed lexicographic optimizer.
The incumbent also supplies exact feasibility and the certified value
interval. The possibly infeasible weak extrema points are never returned
as the primal solution.

On `g>=g_0`, every sublevel core lies within
`sqrt(2delta/g_0)<=epsilon/(8sqrt(k))` of the optimal core. Its true
coordinate range is at most `epsilon/(4sqrt(k))`. Adding both outward
errors gives width at most

```text
epsilon/(4sqrt(k)) + epsilon/(4k) <= epsilon/(2sqrt(k)).
```

The hull diameter is therefore at most `epsilon/2`, so the test passes.
The calculation holds for every precision and every valid answer of the
underlying convex oracles. Hence every fallback, at any requested
precision, lies in the single event `g<g_0`; no union over queries is
required.

On fallback, the exact core-first lexicographic selector is unchanged.
Rational LP repair within the error box about its algebraic approximation
preserves feasibility and gives at most `2tau` max-norm error. The
chosen `tau` bounds the core Euclidean error by `epsilon` and objective
error by `epsilon/2`. Combining it with the refined exact value interval
proves the same output contract on rare draws, including core ties.

The choices of `B`, `g_0`, and the fixed finite grid give
`Pr(g<g_0)<=1/B`. Sampled coefficient length is polynomial in base input
length. The pathwise factor `1+B_0 1_{g<g_0}` controls work and record
size for every `q`, and has expectation at most two. All dimension
dependence outside the supplied base-only constants is ordinary
polynomial; the latter constants are paid for by the finite-law choice
and the rare fallback. This verifies the claimed polynomial exponent
independent of `k` and residual dimension.

## Verification-record meaning and limits

For the coordinate enclosure, replaying the fixed deterministic rational
weak-optimization algorithm and its exact separation queries verifies
the asserted bound using the known-ball and homothety calculations.
The record has polynomial size on the ordinary branch. This is a
computation transcript, not an assertion that each extremum has a short
rational KKT certificate. Verification still uses the charged convexity
premise. The fallback can have a larger exact record, covered by the
same expected-size bound.

Selector consistency concerns the core: each returned core approximates
one fixed lexicographic optimal core. It does not require consecutive
residual outputs to approach one residual minimizer. Taking all variables
as core changes the perturbation model to independent noise in all those
coordinates. These restrictions are necessary and are stated clearly;
the result does not contradict the unperturbed-residual point barrier.

## Checks performed

The reviewer read the complete actual theorem, the relevant interface
and review, the compact-domain growth argument, and the two local GLS
statements above. No external search was used. Scoped document checks
passed local-link existence, paired code fences, forbidden control
characters, trailing whitespace, and the final newline for this review.
The exact command `git diff --check --no-index /dev/null
research-20261002/new-direction/joint-convex-core-point-oracle-review.md`
emitted no whitespace diagnostics; its exit status was 1 for the
new-file comparison. No numerical fixture, general solver test, project-wide
verification, or CI inspection was run by this reviewer. The author's
separate exact hull diagnostic was not duplicated.
