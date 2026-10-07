# Significance of polynomial optimization with convex residual recourse

Date: 2026-10-02. This is an independent scope and significance assessment
of [the polynomial recourse theorem](smoothed-polynomial-box-recourse.md).
Its [separate completed-text proof review](../reviews/smoothed-polynomial-box-recourse-review.md)
has passed. This assessment does not establish publication priority.

The strongest capability is **expected exact implicit optimization with
a small supplied continuous core and a dense convex nonlinear residual
problem**. The exponential factor depends on the core dimension and its
positive upper coordinate curvature relative to noise. Residual dimension,
coupling density, and mixed derivative magnitudes enter only the polynomial
bit-work factor. This is a substantive scope and parameter improvement;
the convex recourse oracle itself is classical.

## What is added

| Existing result | Material difference here | Limit of the comparison |
|---|---|---|
| Quadratic negative-inertia methods | Fixed-degree nonlinear residual costs; no supplied fixed low-rank negative quadratic decomposition. The core-noise ratio can stay small despite large mixed derivatives. | The new feasible set is a continuous product box, whereas several QP results allow general polytopes and mixed variables. A small negative eigenspace need not give a small coordinate core. |
| Separable nonlinear low-rank recourse | Jointly convex, dense, nonseparable residuals and exact implicit completion under one finite law, without supplied growth. | Earlier separable results allow arbitrarily many integer coordinates; this theorem does not. Certified approximate recourse was already available in the earlier approximation result. |
| Sparse smoothed polynomial optimization | A dense residual graph is allowed. The bound is genuinely `f(k,L/sigma) poly_d(I)`, with an input exponent independent of `k`, rather than an `n^p`-type fixed-width bound. | The residual must admit certified global optimization after every rational box restriction. Sparse nonconvex residuals are not covered merely because their width is small. |
| Quadratic box-stable recourse | Approximate lower bounds and feasible completions suffice even when conditional optimizers and values are irrational. A varying nonlinear Hessian can still be closed exactly. | The core-cell count, excluded-region idea, and base-chosen finite-law strategy are inherited. The change is a careful nonlinear completion of that mechanism, not a new principle of conditional optimization. |

Partial minimization, nonlinear variable elimination, convex value oracles,
and optimization-based bound tightening should all receive prior credit.
The candidate contribution is their quantitative composition: only a
small core is gridded, certified excluded-region calls localize the other
variables, and a same-draw exact fallback completes every finite-noise atom.
The [focused nonlinear prior audit](../prior-art/smoothed-polynomial-box-recourse-prior.md)
credits Hooker's partial-convex global search and the classical GLS convex
oracle. It did not identify the same finite-noise expected exact guarantee;
that scoped comparison is not a proof of priority.

## A dense family that separates the structural parameters

Let the core be one variable `v in [0,1]`, let `z in [0,1]^m`, and set

```
P(z) = sum_i z_i^4 + (sum_i z_i)^4,
F(v,z) = (lambda/2)(v-v0)^2 + T v P(z) - b'z,
lambda > 0, T > 0.
```

This is an explicit degree-five polynomial. Its residual Hessian is
`T v Hess P(z) >= 0`, certified directly by sums of PSD matrices, and its
core curvature is exactly `lambda`, independent of `T`. The residual
interaction graph is dense. The theorem therefore has fixed core
parameter even when the sparse theorem would need large bags.

Moreover, any fixed PSD quadratic shift `K` making
`F(x)+(1/2)x'Kx` jointly convex must have rank at least `m`.
At `v=0` the original residual Hessian vanishes. A vector in `ker K_RR`
also annihilates the cross block of `K`; positivity of the corrected
Hessian then makes it orthogonal to every `grad P(z)`. Those gradients
span `R^m`, since their values at the unit coordinate vectors are
`4(e_i+1)`. Continuity from the full box interior justifies using the
boundary Hessian. The
[separate checked lemma](polynomial-recourse-rank-separation.md)
gives the full argument.

Thus pointwise Hessians can have at most one negative eigenvalue while
every fixed concave-quadratic decomposition requires unbounded rank.
This distinguishes a coordinate core from both sparse bags and a fixed
negative quadratic factor. It does not show hardness, and it does not
exclude every nonlinear difference-of-convex representation. Corrections
with singular boundary derivatives fall outside this rank argument.

The positive core quadratic matters. With `lambda=0`, the conditional
value is concave in `v`, and an endpoint core solve already suffices.
More generally, a function concave in each of `k` core coordinates is
minimized by `2^k` endpoint recourse calls. That easy class must not be
presented as the substantive nonlinear application.

For a simpler scale comparison, `v^2+z^2-2T v z`, with `T>1`, has core
curvature `2` and negative Hessian magnitude `2(T-1)`. Its mixed derivative
size does not enter the new numerical count. This quadratic is itself
easy; its role is only to make the parameter distinction transparent.

## Assumptions and solver limits

The recourse contract requires **global certified lower values**, feasible
rational completions, and polynomial bit work at arbitrary rational
accuracy on every residual subbox. A local nonlinear solve or an accurate
feasible value cannot replace it. Joint residual convexity supplies this
contract through rational convex optimization, without a strong-convexity
modulus. Convexity verification for an arbitrary input polynomial is not
free: a tractable structural certificate or a separately charged verifier
is essential. Core discovery is also outside the theorem.

The concrete oracle has a useful practical certificate: at a feasible
rational residual point, minimize its affine tangent over the residual
box. This gives an explicit rational lower bound; the difference from
the feasible value is directly checkable. The convex solver's internal
convergence claim need not be trusted or replayed. This is the classical
convex linearization gap, used here to make each nonlinear recourse call
verifiable, rather than a new convex optimization method.

The count charges the supplied upper bound on core diagonal curvature.
Large mixed derivatives, residual curvature, and higher derivatives enter
`G`, `M_1`, and `T` in the localization cutoff, hence their **logarithms**
enter the number of refinement levels and arithmetic precision. They are
not absent from runtime. A loose supplied curvature certificate can still
make the numerical parameter poor. Fixed degree, explicit polynomial
encoding, unit coordinate scales, and a uniform recourse exponent are
material assumptions.

The finite law perturbs every original linear coefficient. Only core noise
is used in the expected cell count, but residual noise is used to pay for
global point growth and active-bound separation in exact closure. The
theorem does not presently justify perturbing the core alone. Nor does it
return an exact optimizer of the unperturbed objective. Noise small enough
for a desired original-objective gap gives inverse-accuracy dependence
through `L/sigma`; this is not a new logarithmic-accuracy algorithm for
arbitrary unperturbed instances.

Usual output is a globally certified strongly convex patch with efficient
arbitrary-precision evaluation. It is more informative than naming the
original nonconvex argmin, but it is not an expanded algebraic optimizer.
The compact patch has polynomial length; the global pruning proof and
exceptional output have expected size bounds. The precise finite sampler,
very conservative elimination budgets, convex certificates, and fallback
remain implementation obligations. Existing fixtures establish the new
interfaces, not a practical runtime advantage over a global NLP solver.

## Strongest next target

The highest-payoff conceptual target is **noise only in the small core**,
with arbitrary convex residual degeneracy allowed. The expected core-cell
bound already conditions on an arbitrary residual objective. What fails
is the present exact closure: flat residual minimizers need not enter a
strongly convex full-coordinate patch, and core noise alone does not
isolate them. A useful advance would certify an entire convex residual
fiber or a convex value-function patch instead of forcing a unique full
point. This would remove a substantive perturbation assumption and directly
test whether the count and exact-output mechanisms can be separated. It
requires a new certificate, not merely another recourse example.

For a nearer solver-facing mixed-integer target, investigate an exact
polynomial-bit, box-stable **convex-cost integer network-flow oracle**.
Core-dependent nonnegative weights on convex polynomial arc costs preserve
convexity after core fixing and arc-bound restrictions. If the required
oracle guarantee is verified, the excluded-region mechanism could identify
arbitrarily many residual integer labels without enumerating their binary-
encoded capacities, then close the remaining continuous core. Generic
convex integer optimization is not such an oracle. The literature
researcher has been asked to check this specific interface before any
extension is claimed.

## Assessment record

This assessment read the actual nonlinear and quadratic recourse drafts,
the earlier approximate nonlinear recourse result, and the sparse polynomial
significance note, then the completed proof review and focused prior audit.
The structural separation has independent mathematical
checks by the coordinating researcher and the recourse author; its actual
saved lemma is linked above. No optimization diagnostic was rerun, no
external search was performed by this mathematical reviewer, and no root
index or KB files were edited.
An inline `python3` check passed for this note's local links, paired code
fences, and trailing whitespace. These are scoped document checks, not CI
results.
