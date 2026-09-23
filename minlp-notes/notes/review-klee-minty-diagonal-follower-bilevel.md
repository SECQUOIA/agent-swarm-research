# Independent review: scalar leader and diagonal path follower

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the complete
[bilevel construction](klee-minty-diagonal-follower-bilevel.md) passes
this independent mathematical audit.** It proves ordinary NP-completeness
for the explicitly constructed family with one scalar leader, a unique
diagonal strictly convex quadratic follower, a fixed scalar path
polytope, and a nonconvex quadratic upper condition plus a dense slab.
The upper nonconvexity is essential to the stated reduction.

## Quantitative preservation of all vertex responses

Every Klee-Minty vertex coordinate has denominator dividing
`D=(8W)^(n-1)`. The endpoint coordinates are distinct by the already
reviewed invertible lower/upper recursion. Thus distinct endpoints
differ by at least `1/D`, and their squared difference is at least
`Delta=D^(-2)`.

The tangent-certificate score at `lambda_v=2v_n-1` is uniquely maximized
by vertex `v`, and its loss at another vertex `u` is exactly
`(u_n-v_n)^2`. For a general convex combination of vertices, let `a`
be the total coefficient on vertices other than `v`. Linearity gives
score loss at least `Delta*a`. Since all coordinates lie in `[0,1]`,
the displacement from `v` has infinity norm at most `a`. Expanding
the squared norm gives
`||z||^2-||v||^2>=-2n*a`. With `tau=Delta/(2n)`, the follower
objective difference is therefore at least `Delta*a/2`. If `z!=v`,
then `a>0` in every vertex decomposition, proving strict optimality.
No algorithm in the reduction must enumerate those decompositions.

Changing the leader parameter by `h` alters that difference by at most
`|h|a`. Consequently the same vertex remains the unique follower
response throughout the closed interval `|h|<=Delta/4`, clipped to
`[-1,1]`. These intervals have positive length even for endpoint
parameters. Since the response vertices are distinct, this yields
at least `2^n` distinct constant response pieces. For this geometric
statement alone, fixing `epsilon=1/4` gives the same proof with
`D=4^(n-1)` and requires no upper-level constraints.

The follower is strictly convex with Hessian `tau*I` for every leader
decision; its fixed compact feasible set is nonempty. Its response is
therefore unique everywhere. Multiplication of the whole objective by
`1/tau` preserves every minimizer and gives identity Hessian. The
linear coefficients can then be large, but their bit lengths remain
polynomial. Neither conditioning normalization nor the exponentially
small response intervals gives a strong-hardness or fixed-precision
robustness claim.

## Upper decision problem and its scope

The reviewed certificate `F>=0` vanishes only at original path vertices.
Thus the upper condition `F<=0` forces such a vertex. The slab and
the weighted rounding error at most `1/8` then give the same
SUBSET SUM equivalence as the earlier rank-one construction. Conversely,
every yes bit vector supplies a slab-feasible vertex and its rational
leader parameter `lambda_v`; the new response lemma proves follower
optimality at that parameter.

This bit vector is a polynomial-length NP certificate for the explicitly
parameterized family. Its vertex and parameter can be reconstructed
exactly, and the slab checked in polynomial bit time. The certificate
argument does not assert NP membership for arbitrary bilevel programs.
Uniqueness makes optimistic and pessimistic semantics coincide here.

The nonconvex upper condition can equivalently be placed in the upper
objective, asking whether its minimum subject to the linear slab is
at most zero. This optimization version has linear upper constraints
but still has a nonconvex quadratic upper objective. It is not a
hardness result with entirely linear upper data.

Deleting `F` makes the slab feasible for every target `0<=B<=W`.
The unique follower response on a fixed compact polytope is continuous
in the parameter. At `lambda=-1` it is the zero vertex; at the
parameter exposing the all-one-bit vertex its weighted sum is at least
`W-1/8`. The intermediate value theorem reaches every smaller integer
target, and the all-one-bit point itself lies in the endpoint slab
for `B=W`. The relevant second parameter is that of the all-one-bit
vertex, not necessarily `lambda=1`, whose response has only the last
coordinate equal to one. This also proves nonemptiness in the upper
optimization version. Continuity and compactness give attainment.

The path restriction concerns the follower's local linear constraints.
The upper quadratic has a dense linear part, and the slab is one
dense aggregate with two bounds. Diagonal curvature does not decouple
the follower variables because those local path constraints still
couple them. The example is therefore consistent with the positive
theorem requiring independent follower blocks.

## Prior scope and verification

I checked the primary abstract of
[Sugishita and Carvalho](https://arxiv.org/abs/2510.21126), which already
establishes NP-completeness with one leader variable in a linear bilevel
model. Thus scalar leader dimension alone is not a new hardness
boundary here. The draft also acknowledges established exponential
quadratic regularization paths. This review verifies the present
explicit diagonal/path construction, not its priority relative to all
prior formulations.

The core path identity, rational endpoint structure, and exact slab
reduction were checked in
[the earlier independent audit](review-klee-minty-rank-one-slab.md),
including exact clipped-polytope optimization. The new quantitative
response proof was checked directly above. The completed
[second independent audit](review-klee-minty-diagonal-follower-second.md)
reports 1,530 exact normal-cone KKT certificates through dimension
eight and 3,060 exact convex-combination gap checks, using
[its separate checker](../code/parametric_path_lp/exact_diagonal_follower_check.py).
I inspected that audit; its normal-cone equations and sign conventions
agree with the present proof. These checks support, and do not replace,
the global convex-combination argument.
