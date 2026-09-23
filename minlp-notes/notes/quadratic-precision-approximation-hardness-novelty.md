# Novelty audit: approximating minimum integer precision dimension

Date: 2026-09-05. Independent source audit of
[the hardness draft](quadratic-integer-precision-approximation-hardness.md).
This is a bounded literature assessment, separate from its proof reviews.

The checked primary sources do not contain the draft's approximation-hardness
theorem for quadratic graph formulations. The promising contribution is the
positive-optimum gap across arbitrary convex lifts: with rational PSD quadratic
outputs on disjoint variable blocks and unit tolerances, no polynomial-time
valid-formulation constructor can guarantee additive or multiplicative
`O(N^(1-delta))` error in the minimum number of integer coordinates, for any
fixed `delta>0`, unless `P=NP`. Here `N` is the input cube dimension. This is a
qualified priority assessment, not proof that no earlier statement exists.

The broad claim that minimizing integer variables is hard would be inaccurate
as a novelty claim. Closely related formulations of that question already have
hardness results.

## Closest integer-variable antecedents

**Implied integrality.** Rolf van der Hulst and Matthias Walter,
*Implied integrality in mixed-integer optimization*, Mathematical Programming,
published 13 July 2026, Section 6.2, defines Least Integer Hull: choose a minimum
subset of original coordinates whose integrality recovers the integer hull of
a fixed rational polyhedron. Its zero case is integrality recognition and is
coNP-hard. Theorem 6.6 establishes NP-hardness using vertex deletion to a
bipartite graph and the edge relaxation of the independent-set problem.
An earlier version appeared at IPCO 2025. The inspected section contains no
approximation-gap theorem. The fixed relaxation, coordinate selection, and
integer-hull target differ from the draft's freely chosen lifted convex
relaxation of a continuous quadratic graph.
[Open journal article](https://link.springer.com/article/10.1007/s10107-026-02389-3).

**Integrality number.** Paat, Schlöter, and Weismantel define

```
i(A,b) = min { k : exists W in Z^(k x n),
  conv{x in P(A,b): Wx in Z^k} = conv(P(A,b) intersect Z^n) }.
```

Their introduction explicitly keeps the underlying polyhedral constraints
fixed; allowing integral linear combinations is broader than selecting original
coordinates, but does not permit arbitrary replacement of the relaxation.
Their paper develops constructive determinant-based bounds. This precise
definition should be used rather than the looser extended-formulation wording
in the 2026 paper's related-work paragraph.
[Original paper, Section 1](https://arxiv.org/html/1904.06874).

**Affine TU-dimension.** Bader, Hildebrand, Weismantel, and Zenklusen,
*Mixed Integer Reformulations of Integer Programs and the Affine TU-dimension
of a Matrix*, Mathematical Programming 169 (2018), 565–584, develops another
established way to reduce integer coordinates. Section 4 proves hardness of
determining affine TU-dimension using an equal-sum-subsets reduction. This
restricts the algebraic form of the reformulation and does not establish the
draft's graph-precision approximation theorem.
[Original paper, Section 4](https://arxiv.org/html/1508.02940).

## Convex covers and formulation complexity

Minimum convex cover is a substantial existing subject. Eidenbenz and Widmayer
prove APX-hardness and an `O(log n)` approximation for covering a polygon with
the fewest convex polygons. Abrahamsen subsequently proves that the exact
decision problem is complete for the existential theory of the reals.
[Eidenbenz–Widmayer, SIAM Journal on Computing 32 (2003), 654–670](https://epubs.siam.org/doi/pdf/10.1137/S0097539702405139);
[Abrahamsen, Covering Polygons is Even Harder (2021)](https://arxiv.org/abs/2106.02335).

The recent Filtser–Maimon–Yomtovyan paper retains the logarithmic approximation
guarantee while improving running time; its arXiv version was submitted in
April 2026, following SODA 2026.
[Peeling Rotten Potatoes for a Faster Approximation of Convex Cover](https://arxiv.org/abs/2604.17983).

These papers minimize the number of pieces in an explicitly described planar
polygon. The draft minimizes integer coordinates for a succinct quadratic
graph in variable dimension. Piece count and integer count are different
objectives; arbitrary integer ranges also prevent identifying integer count
with the logarithm of the number of fibers without an additional argument.
The draft obtains its lower bound through parity and pairwise forbidden
midpoints. Thus known convex-cover hardness is relevant background but does
not immediately imply this theorem.

Cevallos, Weltge, and Zenklusen prove unconditional lower bounds on integer
coordinates for mixed-integer extended formulations of several combinatorial
polytopes, including approximate formulations. Their bounds require a bound
on formulation size; for example, subexponential-size descriptions of the
matching and cut polytopes need `Omega(n/log n)` integer variables.
[Lifting Linear Extension Complexity Bounds to the Mixed-Integer Setting](https://arxiv.org/abs/1712.02176).
The draft instead proves conditional hardness of constructing a formulation
whose integer count approximates an unrestricted optimum. Its forbidden-
midpoint lower bound does not limit the number of continuous variables or
constraints in a competing convex lift. Neither statement subsumes the other.

Vavasis's exact nonnegative matrix factorization hardness is another established
representation-design precedent. His concluding discussion explicitly notes
the standard multiplicative-approximation obstruction from an optimum of zero,
while distinguishing additive approximation and approximation of nonnegative
rank itself. This is a useful precedent for explaining why the draft's
positive-optimum construction is more informative than its zero-case corollary.
[On the Complexity of Nonnegative Matrix Factorization, Section 5](https://www.cs.cornell.edu/courses/cs6241/2020sp/readings/Vavasis-2009-NMF-complexity.pdf).
This source should not be cited as automatically proving the same hardness
for extension complexity or integer precision dimension.

## Attribution and limits for the proposed result

The Max-Cut Laplacian identity and hardness are established. The same-parity
midpoint argument is established in Lubin, Vielma, and Zadik, *Mixed-integer
convex representability*, Lemma 4.1.
[Original MICP paper](https://arxiv.org/abs/1706.05135).
Direct-product gap amplification and the zero-optimum obstruction are standard
complexity arguments. The candidate contribution is their application to this
whole-formulation optimization problem, including the explicit positive-optimum
baseline and unit-tolerance PSD family.

The strongest defensible presentation keeps these distinctions explicit:

- The constructor must always return a valid graph relaxation, with its integer
  count readable from the output. The reduction does not solve that formulation.
- The low instance has optimum exactly one; the high instance requires at least
  `t+1` unrestricted integer coordinates. This removes the zero-optimum loophole.
- The approximation scale uses ambient input dimension `N`, while construction
  time uses the total binary encoding length. Do not silently replace `N` with
  encoding length in the exponent.
- The result excludes `O(N^(1-delta))` guarantees for fixed positive `delta`.
  It does not exclude every sublinear bound, such as `N/log N`, and does not
  prove an exact linear approximation threshold.
- CoNP-completeness of zero recognition is stated only for the explicitly
  encoded Laplacian family. No membership claim for the general optimization
  over arbitrary convex lifts follows.

The inspected literature supports keeping this as a potentially publishable
companion to the finite covariance benchmark and polynomial construction.
The positive-optimum approximation theorem deserves the emphasis; elementary
Max-Cut recognition alone would be a smaller consequence.

Search scope included integer-dimension minimization, implied integrality,
integrality number, affine TU-dimension, minimum convex cover, approximate
mixed-integer extended formulations, and representation-factorization hardness.
The primary sources above were checked for their actual target and constraints.
