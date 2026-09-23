# Independent audit of fixed interaction-rank optimization

Date: 2026-09-04. Reviewer: independent `review_extension` agent.

Reviewed file: [Exact optimization for rank-one flow blocks with low-rank
costs](../results/rank-one-low-rank-costs.md).

Verdict: the fixed-interaction-rank algorithm is correct, including exact
reconstruction and polynomial bit complexity. The pure rank-one greedy
special case is also correct. One output-size correction was required and
has been applied: its near-linear bound returns margins or a factored matrix;
writing all entries of the dense optimal matrix additionally costs `O(mn)`.

## Cost decomposition

The minimum interaction rank is correctly computed by the displayed double
centering. With

```
P=I_m-1_m e_1^T,  Q=I_n-e_1 1_n^T,
```

one has `D=PCQ=P(C-a1^T-1b^T)Q` for every `a,b`, so its rank cannot exceed
any residual rank. Choosing the specified first-column and first-row costs
makes the residual exactly `D`, attaining the bound. Rational rank
factorization has polynomial bit complexity. This proof includes rank zero
and matrices with only one row or column. Coordinatewise consistency of
the lower and upper bounds is now explicitly assumed or checked.

The margin objective contains exactly the separately needed information:
`S`, the `k` interaction coordinates, and one additive-cost coordinate on
each side. Its projected dimension is therefore at most `k+2`, regardless
of the two original margin dimensions.

## Enumeration and feasibility

The zonotope vertex bound is the standard central-hyperplane arrangement
bound, with dimension zero and zero generators handled separately. The
incremental enumeration by convex-hull membership LPs is valid even without
general position. Every vertex of a Minkowski sum of a polytope and a segment
is a sum of a vertex and an endpoint, so retaining only current vertices
does not lose a future vertex. Duplicated candidates must be merged before
testing membership in the convex hull of the others, as the draft specifies.

Each projected vertex has a box-corner witness. Every stored candidate is
a sum of rational generators, and LP culling does not replace it by a new
point. Thus projected coordinates have polynomial bit length, and witnesses
can be recorded by their endpoint choices.

A vertex of a hyperplane section lies in the relative interior of a minimal
face of dimension at most one. If that face had dimension at least two,
its direction space intersected with the hyperplane direction would have a
nonzero vector, allowing movement in both signs within the section. This
argument applies to lower-dimensional polytopes and tangential sections.

At a fixed positive total the objective is affine in either projected
margin separately. Starting with a global fixed-total minimizer, minimizing
one side at a vertex and then the other side at a vertex cannot raise its
value. Hence there is a pair of slice vertices attaining the optimum.

All pairs of projected vertices include endpoints of all actual edges.
The extra chords remain feasible because they are inside the zonotope,
and their interpolated corner witnesses remain inside the original box.
Consequently these extra candidates cannot create a spurious objective
value below the true optimum. Horizontal chords may be discarded: an
interior point of a horizontal original edge is not a slice vertex because
the entire edge lies in the section. Original vertices are retained as
singletons, including the sole vertex of a dimension-zero projected box.

Synchronizing the first coordinates of a row chord and a column chord
therefore produces feasible margins with a common total. All fixed-total
vertex optima occur in some such synchronized pair.

## Univariate optimization and bit complexity

On a nonhorizontal chord both the projected margin and its original box
witness are rational affine functions of `S`. Pairing two such functions
in the displayed objective gives `alpha S+beta+gamma/S`. The only possible
strict interior minimum on positive totals occurs when `alpha,gamma>0`,
at `sqrt(gamma/alpha)`. When both are negative the stationary point is a
maximum; zero coefficient cases are monotone or constant. The draft correctly
distinguishes these cases and does not use the positive-root minimum value
for a negative-coefficient stationary maximum.

Zero total is feasible exactly when all lower bounds on both sides vanish.
For feasible nonnegative margins, `|<C,W>|<=||C||_max S`. Thus zero supplies
the correct limit without an artificial pole. More specifically, any
candidate chord reaching zero has a zero original margin at that endpoint;
the interpolated margin is proportional to `S` there. Its paired objective
therefore extends continuously to zero. Singleton zero intersections and
the feasible interval `{0}` are dealt with separately.

There are polynomially many candidates when `k` is fixed. Forming rational
differences, slopes and endpoints uses quantities of polynomial bit length.
Interior objective values have the form `beta+2sqrt(alpha gamma)` with a
nonnegative radicand. Comparisons between two such values require only a
constant number of rational sign tests and sign-aware squarings, so their
bit cost remains polynomial. Membership of a positive square root in an
interval with nonnegative rational endpoints is also a rational comparison
after squaring.

Once one candidate is selected, all coordinates of the margins lie in the
same quadratic field. Multiplication and division by the positive selected
total preserve that field and polynomial encoding length. Therefore an
exact optimal matrix can be written with at most one shared square root.
The running time is polynomial for every fixed rank, with an exponent
depending on the rank; the claim is XP and does not establish FPT.

## Quality-constraint Lagrangian corollary

The later PSE corollary was checked separately. Dualizing the terminal-quality
constraints with supplied rational multipliers `lambda_jk>=0` adds the matrix
`Q Lambda^T-1 b^T`, where `b_j=sum_k lambda_jk H_jk`, to the operating cost.
If that original cost is additive in source and terminal indices, the
resulting interaction rank is at most the number of qualities. Thus fixed
quality count gives an exact polynomial per-block Lagrangian minimization
oracle over the remaining row/column bounds and rank-one constraint. The
qualification on rational multipliers matches the bit-model theorem. This
does not imply global pooling tractability or exact Lagrangian duality.

## Rank-one cost specialization

For a supplied factorization `C=pq^T`, each scalar margin image at fixed
total is a closed interval. The minimum product of two scalar intervals
is attained at one of their four endpoint pairs, regardless of signs or
whether either interval straddles zero. The scalar extrema are ordinary
continuous-knapsack values, obtained in coefficient order or its reverse.

Zero capacities and coefficient ties do not invalidate the value functions:
they merely merge breakpoints or produce adjacent equal slopes. Prefix sums
give the affine pieces, and a sweep of the union of the four breakpoint
sets evaluates only linearly many intervals after sorting. The same radical
comparisons and zero-total handling apply. One reconstructs only the winning
greedy margins, so the claimed near-linear arithmetic bound is valid for
the factored output. Dense output necessarily takes additional `O(mn)` work.

The irrational example checks directly: with margins `(1,S-1)` on each
side, the factors give `(S+2)(S+1)/S=S+3+2/S`, whose minimum on `[1,2]`
is `3+2sqrt(2)` at `S=sqrt(2)`.

The author reports completed exact-arithmetic comparisons against a solver
that enumerates both margin bound patterns: 160 seeded signed rational
instances, including 111 feasible and 49 infeasible cases, plus dedicated
irrational, zero-only, and singleton-total examples. The implementation is
[verify-rank-one-costs.py](../code/verify-rank-one-costs.py). This review
focuses on the general proof and complexity details rather than duplicating
those checks.

## Prior work and interpretation

The primary manuscript of
[Punnen, Sripratak and Karapetyan](https://repository.essex.ac.uk/22056/1/1212.3736v3.pdf)
was opened independently. It explicitly treats the equivalent continuous
problem over two independent boxes, establishes fixed-rank polynomial
solvability, and gives a fast rank-one case. Its objective is bilinear plus
additive terms; it does not have the common varying total and division by
that total used here. The cited
[Hladík, Černý and Rada work](https://kam.mff.cuni.cz/~hladik/publ/b2hd-HlaCer2021c.html)
is an additional established zonotope precedent.

Thus low-dimensional box projection and fixed-rank optimization are known
methods. The audited result supplies an explicit adaptation to this isolated
rank-one flow block, including moving slices and exact quadratic-field
solutions. This audit does not establish independent publication novelty or
extend tractability to other pool constraints.
