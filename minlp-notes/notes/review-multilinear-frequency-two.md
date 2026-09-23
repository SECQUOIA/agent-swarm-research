# Independent audit of frequency-two multilinear gaps

Date: 2026-09-04. Reviewer: independent `review_extension` agent.

Reviewed draft: [Positive multilinear gaps when every variable appears
in at most two terms](../results/positive-multilinear-frequency-two-gap.md).

Verdict: the theorem is correct on the unit cube, and by scaling on boxes
with zero lower bounds. The odd-girth factor `g/(g-1)`, bipartite exactness
for the scalar positive polynomial, and sharp universal factor `3/2` all
pass. The draft correctly declines to claim an arbitrary-positive-lower-bound
extension. Only two minor row-indexing and zero-degree wording clarifications
were requested, and the author applied them.

## Dual multigraph and gap normalization

Every active variable becomes one edge. A variable in two distinct monomials
joins their two factor vertices; a variable in one monomial joins it to a
fresh zero-weight dummy vertex. Multilinearity prevents loops. Parallel
edges are permissible and correspond to different variables shared by the
same pair of monomials. Fresh degree-one dummies add no cycles or odd cycles.
Variables in no nonlinear term have no effect on either gap and can be
sampled independently later.

For failure marginals `p=1-x`, a term has upper value `1-max p_i` and lower
value `1-min(1,sum p_i)`. Its gap is therefore `c_v(p)-b_v(p)` with the
definitions in the draft. The expected term product is the probability
that its dual vertex receives no selected failure edge. This proves the
coverage representation, including the subtracted baseline `b_v(p)`.
All positive term upper values are simultaneously attainable by a common
threshold, justifying the scalar hull-gap identity. Dummy weights are zero,
so their added coverage contributes no objective term.

## Degree-slab vertices

On fractional coordinates of a polytope vertex, the vertex-indexed tight
degree rows must have full column rank. If they did not, perturbing in a
nonzero null vector by a sufficiently small amount would keep all tight
degree rows fixed, preserve all slack degree inequalities, and keep every
fractional coordinate strictly between its box bounds. This would contradict
extremality. The row at a vertex is counted once even if its lower and upper
degree bounds coincide.

Each such row contains at least two fractional coordinates: its right-hand
side is an integer, and every nonfractional incident edge contributes an
integer, so exactly one strictly fractional contribution is impossible.
Every fractional edge has two endpoints. Combining these facts with full
column rank forces equality in both incidence counts. Thus every fractional
edge has both endpoints among the tight rows, and each of these vertices has
fractional degree exactly two.

Consequently the fractional components are cycles, including a possible
parallel-edge two-cycle before the rank test. Every even cycle admits the
usual alternating nonzero null vector, so no even cycle occurs at a vertex.
The remaining components are disjoint odd cycles. At each of their vertices,
the two strictly fractional coordinates sum to an integer between zero and
two, hence sum to one. An odd cycle forces every one of them to equal `1/2`.
Degree-one dummy vertices therefore cannot belong to a fractional component.

The prescribed vector `p` lies in the compact degree-slab polytope and hence
has a finite decomposition into its vertices. On this polytope the coverage
target `c_v(z)=min(1,sum z_i)` is affine on each vertex's permitted degree
slab: if the original sum is below one, the whole slab is contained in
`[0,1]`, including the singleton slab at zero; otherwise its lower bound is
at least one. This proves `E c_v(Z)=c_v(p)`. Convexity of coordinate maximum
gives `E b_v(Z)>=b_v(p)` in the required direction.

## Cycle rounding and the baseline

An odd cycle of length `L` has exactly `L` maximum matchings, indexed by
their unique uncovered vertex. Each edge belongs to `(L-1)/2` of them.
Mixing a uniformly selected such matching with its edge complement with
equal probability therefore gives every cycle edge marginal `1/2`.

The complement covers every vertex: a matched vertex has one incident edge
outside the matching, and the unmatched vertex has two. Thus each cycle
vertex has coverage probability `1-1/(2L)` after the mixture. Integral
edges remain fixed, so a vertex incident to an integral selected edge is
covered with probability one. Different fractional cycles share no vertices
and can be rounded independently.

For a cycle vertex lacking another selected edge, `c_v(z)=1` and
`b_v(z)=1/2`. With `alpha=1-1/g` and `L>=g`, its coverage is at least
`alpha c_v(z)+(1-alpha)b_v(z)`. All remaining vertices satisfy this
inequality exactly. Averaging and then using convexity of the baseline gives

```
E I_v-b_v(p)
 >= alpha c_v(p)+(1-alpha)E b_v(Z)-b_v(p)
 >= alpha[c_v(p)-b_v(p)].
```

This step is sound and is the essential distinction from an ordinary
unshifted coverage approximation. Nonnegative term weights allow these
vertexwise inequalities to be summed. A bipartite dual graph admits no
fractional cycle, so the degree-slab decomposition itself achieves every
term's lower-envelope target simultaneously.

## Sharpness and scope

On a unit-weight odd cycle with half failure marginals, the total local
gap is `L/2`. For every selected edge set, coverage is bounded by
`|F|+(L-1)/2`: use `2|F|` when at most `(L-1)/2` edges are selected and
the total vertex count otherwise. Taking expectations gives maximum
coverage at most `L-1/2`. The matching/complement mixture attains it.
Subtracting the baseline `L/2` leaves hull gap `(L-1)/2` and the claimed
ratio `L/(L-1)`. The triangle supplies `3/2` with strictly interior means.

Bipartite exactness concerns the envelope of the scalar positive polynomial.
It is not a claim of full lifted-polytope exactness. Parallel variables can
create incidence cycles even when the dual multigraph is bipartite, and the
draft correctly preserves this distinction.

Scaling a box with zero lower bounds preserves every monomial scope and
positive coefficient. Expanding after a positive lower-bound shift can
create many submonomials sharing the same variable; the frequency-two
argument does not apply to that expanded graph. No such extension follows
from the current proof.

## Checks and established ingredients

The primary paper
[Barrus, *On fractional realizations of graph degree sequences*](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i2p18/pdf/)
was read independently. Its Theorem 2.1 gives the relevant bounded
fixed-degree half-integral odd-cycle structure and attributes the matching
foundations to earlier work. The present proof independently covers degree
slabs, parallel edges, and non-graphic degree data; the extra parity statement
in Barrus's graphic-degree setting is not needed or imported.

[audit-frequency-two-cycle-rounding.py](../code/audit-frequency-two-cycle-rounding.py)
checks the rounding with exact rational arithmetic for odd lengths
`3,5,7,9,11`. Every edge marginal and every vertex coverage matched its
formula exactly. It also verifies the sharpness inequality on all
`2,728` selected-edge subsets across these five cycles.

The author separately reports 200 seeded weighted, unequal-marginal
multigraph checks against the full probability-distribution LP, including
single-incidence variables. All passed; 94 bipartite cases attained exactness.
Those numerical checks complement the independent arithmetic rounding check.

The gap application and odd-girth refinement retain provisional novelty.
This review establishes correctness, not priority over matching-based
coverage or multilinear-polytope literature.
