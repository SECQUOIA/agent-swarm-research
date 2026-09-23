# Independent proof review: bilinear interaction-graph complexity

Date: 2026-09-05. Reviewer: an agent independent of the root author.
Reviewed source: `results/bilinear-graph-binary-complexity.md`.
Verdict: the finite weighted LP bounds, the shared binary construction,
and the fractional vertex-cover asymptotic pass mathematical review.
The unrestricted-integer convex-lift extension also passes independently.
This is an internal proof review, not external peer review or a priority
assessment.

The reviewer independently derived the graph fractional-cover exponent
and shared-residual construction before learning that root had obtained
these simultaneously. This is useful independent reasoning evidence,
not evidence of publication novelty.

## Lower-bound audit

1. For binary polyhedral lifts, graph-contact sets associated with each
   assignment are compact, and two points in the same contact set have
   a feasible chord midpoint. The coordinate error is exactly
   `(a_i-b_i)(a_j-b_j)/4`.
2. The coordinate-width estimate is valid for every compact set with the
   pairwise product bound. Extreme first-coordinate witnesses have
   second-coordinate distance at most `delta/d_1`. Every other point
   lies within `2delta/d_1` vertically of one witness. Thus the full
   second-coordinate span is at most `5delta/d_1`.
3. Apply this to every edge projection. With positive widths,
   `s_i=-log2 d_i` is feasible for `L_20`. Width-zero sets have volume
   zero and do not need logarithms. Isolated vertices introduce no
   restriction and can have width one.
4. Every contact set is contained in a box of volume at most
   `2^(-L_20)`. The unit cube requires at least `2^(L_20)` such boxes.
   With at most `2^p` assignments this gives `p>=ceil L_20`.

## Unrestricted-integer convex-lift extension

The stronger result requires neither bounded integer ranges nor
polyhedral lifted constraints. Suppose a convex set `K` in
`(x,w,y,z)`-space, with `z in Z^p`, gives the relaxation. Define each
`S_a`, `a in {0,1}^p`, by existence of an exact-graph lift with integer
parity `a`. Every graph point has such a lift. Two lifts in the same
class have an integer average, and their average belongs to `K`.
Hence all edgewise midpoint inequalities hold inside `S_a`.

Although these parity classes need not be convex, closed, or a priori
measurable, their closures in the cube are compact and preserve every
pairwise product inequality by continuity. Their coordinate widths are
unchanged. Their enclosing boxes cover the cube, and all remaining
steps of the volume proof apply. Even closedness of `K` is unnecessary
for this argument. Thus the lower bound counts arbitrary integer
coordinates in any convex lift. The binary construction supplies the
upper bound for both binary dimension and unrestricted integer
dimension.

This mechanism is the published Midpoint Lemma of Lubin, Vielma, and
Zadik, with a new quantitative geometric estimate layered on it:
[[lubin2022-mixed-integer-convex-representability]] p.11-12.

## Construction audit

Let `p_i=ceil s_i`, `A_i=sum_k 2^(-k) beta_ik`, and `x_i=A_i+r_i`, where
`0<=r_i<=h_i=2^(-p_i)`. For an oriented edge, the identity

```
x_i x_j = A_i x_j + r_i A_j + r_i r_j
```

is exact and contains no double counting. The first two terms are sums
of binary-times-bounded-continuous products, so the stated four-row
linearizations are exact for integer binaries. The only approximation
is McCormick on `r_i r_j`, whose absolute vertical error is at most
`h_i h_j/4`. Since `p_i+p_j` satisfies the `L_4` requirement, every edge
meets its requested accuracy. The case `epsilon_ij>=1/4` needs zero
precision and is correctly handled by the maximum with zero.

All `x_i in [0,1]` have a binary expansion of this form, including
`x_i=1` by taking all bits one and `r_i=h_i`. With zero bits, `r_i=x_i`.
For each true graph point choosing the exact residual product gives a
feasible lift simultaneously for all edges. Shared bits do not impose
any conflicting edge-specific requirements.

The count per edge is `O(1+p_i+p_j)` auxiliary variables and rows, so
summing gives `O(n+|E|+sum_i degree(i)p_i)`. No hidden additional binary
variables are needed. This proves an actual compact lifted formulation,
not only an existence result for a potentially enormous union of cells.

## LP comparison and asymptotics

For every edge, its nonnegative logarithmic requirement rises by at
most `log2 5` when replacing constant 20 by 4. Adding `log2 5` times a
minimum fractional vertex cover to an optimum of `L_20` therefore
produces a feasible `L_4` solution. The objective increase is at most
`tau*(G) log2 5`, exactly as claimed. Ceiling each vertex precision
adds at most `n` to the objective, giving a tolerance-independent
additive gap to every admissible formulation.

For common small `epsilon`, the LP is a scalar multiple of fractional
vertex cover, yielding coefficient `tau*(G)` on `log2(1/epsilon)`.
The table values for stars, complete bipartite graphs, matchings, odd
cycles, and complete graphs are correct. Affine box scaling divides
edge accuracy by the product of endpoint widths after removing affine
terms; this preserves integer dimension.

## Scope and caveats

The whole unit-cube product graph must be included. Physical linking
equations can destroy this full-dimensional substructure. The theorem
is about every lifted product's error; scalar quadratic sums can cancel
and are a different problem. These restrictions are properly stated.
The graph is simple: square terms need separate width constraints and
are not silently covered by an ordinary loop-free fractional cover.

The LP values contain logarithms of the requested tolerances. The
mathematical formulation/count theorem is valid over real coefficients.
It should not be read as an exact rational bit-complexity result for
computing logarithmic LP optima. Rational conservative precision choices
can be investigated separately if such an algorithmic claim is needed.

No proof defect was found in the finite or asymptotic theorems.
Dedicated literature review remains necessary to judge the contribution.
