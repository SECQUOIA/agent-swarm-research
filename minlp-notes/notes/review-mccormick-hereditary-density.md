# Independent audit of the graph-by-graph density characterization

Date: 2026-09-04. Reviewer: independent `review_extension` agent.

Reviewed file: [Maximum induced density and the worst McCormick
gap](../results/mccormick-hereditary-density-characterization.md), including
the later Schur-multiplier appendix.

Verdict: the mathematical characterization is correct. The later literature
transfer also checks out and materially limits novelty: the square-root
density order already follows from classical Schur-multiplier theory and
Grothendieck's inequality. The elementary constant 4 and explicit McCormick
interpretation may still be useful, but their novelty is not established.

## Random-sign lower bound and localization

For an `n`-vertex, `m`-edge graph with `m>0`, the moment generating function
bound for each fixed vertex configuration is
`E exp(lambda f_sigma(s))<=exp(m lambda^2/2)`. Global reversal of vertex
signs preserves `f`, so there are at most `2^(n-1)` relevant configurations,
even when the graph is disconnected. Taking both signs of the exponent
therefore introduces a factor `2^n`, exactly as in the draft. Jensen gives

```
E ||f_sigma||_infinity <= n log(2)/lambda + m lambda/2.
```

The chosen minimizer gives `sqrt(2mn log 2)`. No independence between
different vertex configurations is used. Since the distribution of edge
signings is finite, at least one signing attains a value no larger than
the expectation.

At the point with coordinates `1/2` on `U` and zero outside, all convex
decompositions into box vertices have zero outside coordinates. The active
means can attain either extremum of the even quadratic Walsh polynomial
by mixing a sign vector and its global negative equally. The hull gap is
therefore `R_U/2`, whereas the McCormick gap is `L_U/2`. These factors
match the signed-cut normalization. The lower bound on a densest induced
subgraph consequently survives arbitrary signs on every remaining edge
of the original graph. This establishes the claimed full-support `+/-1`
lower bound without continuity or a limiting argument.

The upper direction of the induced-subgraph gap identity uses the earlier
Boland et al. result, checked in the companion density audit. Its lower
direction is proved directly here. For zero induced coefficient vectors,
the convention `0/0=0` is explicitly separated from every nonzero case.
Nonconstant orthogonal degree-two Walsh characters imply positive range
for a nonzero coefficient vector. Also `R_U<=L_U`, giving the independent
lower bound one when the graph has at least one nonzero coefficient.

## Whole-graph norm and strict support

The equality `Gamma(G)=sup_a L_V(a)/R_V(a)` is correct. Each induced ratio
can be realized as a whole-graph center ratio by zeroing all edges outside
the induced graph; the global Walsh polynomial then depends only on its
active coordinates. The reverse inequality follows by using the center
of the whole box in the definition of the gap factor.

On the finite-dimensional compact set `L_V(a)=1`, the function `R_V(a)`
is continuous and strictly positive. The center ratio therefore attains
its maximum. Approximating an optimizer by coefficient vectors with no
zero entries and using continuity of this center ratio proves equality of
the full-support supremum. The argument correctly avoids asserting
continuity of `c*(a)` across supports or attainment under strict support.

The graph-family characterization needs no hereditary closure because the
witnessing point fixes coordinates outside the dense part to zero. The
comparisons `d/2<=rho<=d` and `rho<=alpha<=d<=2rho` are valid. The labelled
acyclic orientation really partitions edges into forests: an undirected
cycle with acyclic orientation must have a vertex with two outgoing cycle
edges, which a single label class forbids.

The connected dense-core example has `2q^2` edges and `q^2+2q` vertices,
so its global density is below two while the core density is `q/2`.
The scaling counterexample correctly rules out an unnormalized weighted
density substitution. The statement remains about the vertical gap of one
bilinear function on a box, not an objective approximation ratio for a
constrained optimization model.

## Classical-theory transfer and novelty downgrade

The primary author manuscript
[Davidson and Donsig, *Norms of Schur Multipliers*](https://www.math.uwaterloo.ca/~krdavids/Preprints/DavDon_schur.pdf)
was opened independently. The upper estimate in Theorem 2.4, PDF page 8,
and the projective-norm inequality following Theorem 1.2, PDF pages 4–5,
are the stated ingredients. The matrix formulation gives the unrounded
density bound; using only the integer pattern theorem would introduce a
ceiling. The real Grothendieck constant is the appropriate one here.
For real matrices, realification of a complex Hilbert factorization preserves
its real entries and factor norms, so the real factorization interpretation
is consistent with the source's Schur norm.

For a symmetric graph adjacency pattern `P`, define the rectangle density
over sets with `|R|+|C|>0`. Partition their union into the intersection and
the two disjoint differences. An edge inside the intersection contributes
two ordered pattern entries; edges between the differences or from a
difference to the intersection contribute one. The only additional edges
on the proposed right side lie entirely inside one difference. This proves

```
|P intersect (R x C)|
 <= |E(R union C)|+|E(R intersect C)|
 <= rho(G)(|R|+|C|).
```

Taking `R=C` equal to a densest vertex set attains equality after division.
Thus the rectangular matrix density equals `rho(G)` exactly.

Let `A` be the symmetric weighted adjacency matrix and `T=sign(A)`, with
zero entries kept zero. Its matrix inner product with `A` is `2L`.
The dual of the real projective tensor norm is the real bilinear norm
`B=max_{u,v in {+/-1}^V}|u^TAv|`. For any such `u,v`, put
`p=(u+v)/2` and `q=(u-v)/2`. Symmetry gives

```
u^TAv=2[f_a(p)-f_a(q)].
```

Both points lie in the cube `[-1,1]^V`, and multilinearity bounds their
values by the extreme vertex values. Consequently `B<=4R_V(a)`.
The source bounds and dual pairing now yield

```
2L <= pi(T) B <= 2 K_G sqrt(rho(G)) B,
L <= 4 K_G sqrt(rho(G)) R_V(a).
```

This validates the author's novelty downgrade. The density order and the
qualitative boundedness characterization are existing-theory consequences
after these elementary transfers. It would be inaccurate to advertise the
order alone as a newly discovered phenomenon. No conclusion that the local
constant 4 improves every previously available constant follows from this
comparison with one specific proof.

The only requested edit was the harmless denominator convention excluding
`R=C=empty` in the definition of rectangle density. The author was notified.
