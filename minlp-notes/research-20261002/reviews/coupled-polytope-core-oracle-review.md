# Independent review of core Cauchy output on a coupled polytope

Date: 2026-10-02. Verdict: the completed
[core-output addendum](../new-direction/coupled-polytope-core-oracle.md)
passes. Its explicitly stated coupled-value interface has now passed a
[separate actual-file review](coupled-polytope-core-value-review.md),
which I read before completing this status. I read
the actual addendum, value draft and polytope fallback/value interface,
and checked the saved noise-sign correction. This record does not
independently approve every implementation detail of the separate value
oracle, nor assert that fiber convexity alone provides one.

## Compact-domain projected growth

The modified conjugate is a maximum of a continuous function over the
compact full-variable feasible set. It is finite, convex and Lipschitz
in the core coefficient. Every maximizing core is a subgradient, and
all subgradients lie in the coordinate range of the core projection.
Thus differentiability identifies one maximizing core even if its
residual witnesses are different. This is exactly the property the
proximal argument needs.

The signs now agree with the objective convention. Maximizing
`c'v-F_0(v,z)+epsilon||v||^2` and choosing the common maximizing core
`a` yields projected growth for `gamma=-(c+2epsilon a)` in the objective
`F_0+gamma'v`. Reflecting the symmetric product noise leaves its law
unchanged. The root reviewer identified the earlier ambiguous sign; I
read and independently rederived the saved correction.

The proximal displacement bounds use only the coordinate widths of the
projected compact set. All subsequent area-formula, divergence and
coordinate-variation steps concern the coefficient-space convex function,
so the sharp continuous tail remains `k t/sigma`. No continuity of a
partially minimized value function is required. Compactness and continuity
on the original domain also prove closedness of the positive-growth
event directly through convergent full-variable witnesses.

Its exact good-event formula has one existential full feasible point and
one universally quantified feasible competitor, with the squared norm
only on core coordinates. Positive growth requires unique optimal core,
not unique optimal full point. Linear polytope membership adds no
quantifier block. The same fixed-block elimination and marginal replacement
therefore give the uniform finite-law additive term. Singleton core
projections and lower-dimensional feasible sets are covered.

## Hull retention and the common work factor

The new cell witness may lie anywhere in the queried cell. This does
not change either invariant. A cell containing a globally optimal full
point has lower bound at most its objective and survives. A feasible
incumbent has a containing cell; if still incumbent after subdivision,
the same full point witnesses that the appropriate child is nonempty.
Its cell lower bound is at most its true objective, so it cannot be
pruned against the final incumbent. Newly improving points satisfy the
same condition at insertion.

The retained coordinate hull consequently contains all optimal cores
and the current incumbent core. Its exact rational diameter test certifies
distance to the selected core without trusting growth. A retained cell's
gap-`4e_h` feasible witness is localized by projected growth, and any
other point in that cell is within `h` in each coordinate. Thus the same
bound `D h`, with `D=4k+k^2 alpha_+/g_0`, is valid despite infeasible
portions of the hull or cells. The hull is a geometric enclosure, not a
set from which the algorithm fabricates a feasible output point.

The enlarged finite grid makes the bad projected-growth probability at
most `1/B`. Failing the hull test at any future query implies that one
event, while hitting the inherited count cap implies `W>B`. A union
bound suffices; no independence of these events is needed. The extra
terminal depth and hull pass preserve the inherited pathwise work factor
and polynomial bit exponent. This reasoning is valid provided the value
interface supplies the stated lower bounds, gap witnesses, generated
count and height-separated fallback budget, as it explicitly claims.

## The selected fallback point is repaired feasibly

The polytope fallback's two-block lexicographic singleton formulas refer
to one selected optimizer. Core-first ordering is allowed. Refining its
coordinates gives a rational vector `w` within a certified error box,
which need not itself satisfy the coupled constraints.

The exact selected point proves feasibility of the rational LP
`x in P, |x_i-w_i|<=delta`. Any returned rational point is within
`2delta` in maximum norm of that same selected point. This is a valid
repair even on a lower-dimensional polytope. The selected and repaired
points have their whole segment in `P`, so the gradient bound controls
the objective difference by `2G delta`. The allocated precision also
gives core Euclidean error at most `2sqrt(k)delta`. Refining the exact
value for the other half of the error proves the full output contract.

LP work and precision have a fixed polynomial dependence on the sampled
height and accuracy. The existing base-only exponential fallback budget
absorbs algebraic representation sizes. This extension therefore does
not promise efficient residual coordinates or use invalid box clipping.

## Verification record

This review independently rederived the compact-domain tail, corrected
sign, arbitrary-witness retention, diameter bound, combined event budget
and error-box repair. It does not duplicate the separate coupled-cell
diagnostic or general convex-optimization source audit. A targeted check
of this review's links, whitespace and fences passed. No index edit,
external search, project-wide verification or CI inspection was performed.
