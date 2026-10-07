# Prior-art note: separable convex optimization over TU systems

Date: 2026-10-02. This focused prior-art comparison covers the reviewed
[core-only-noise theorem over TU systems](../new-direction/smoothed-core-tu-recourse.md),
including its bounded-slack TU-inequality corollary. The theorem has passed
its [independent mathematical review](../reviews/smoothed-core-tu-recourse-review.md).
This note compares its recourse certificates with established optimization
and circuit ingredients; it makes no publication-priority claim.

## Exact separable-convex recourse is already available

Hochbaum and Shanthikumar's primary paper, [“Convex Separable Optimization
Is Not Much Harder than Linear Optimization”](../../literature/papers/hochbaum1990-convex-separable-optimization-is-not/),
Theorems 1.2 and 4.3, gives exact integer optimization for a separable
convex objective over a totally unimodular system. A bounded equality system
`Az=b`, `l<=z<=u` fits by writing the equality as the two inequalities
`Az>=b`, `-Az>=-b` and adjoining signed unit rows for the bounds; these
operations preserve total unimodularity and integral right-hand sides. The
same oracle therefore applies after any coordinate interval is tightened
to integer endpoints.

The paper states a function-evaluation and LP-operation complexity. For an
explicit fixed-degree rational polynomial cost, ordinary polynomial bit
time follows by evaluating the polynomial exactly at the rational points
queried by the scaling method and using rational LP. This is the same
finite-bit specialization recorded in the
[flow-oracle audit](integer-convex-flow-recourse-prior.md), not a separate
bit-complexity theorem stated verbatim in H&S.

## Optimal labels form a box after fixing a dual multiplier

The interval representation is a standard consequence of LP
duality and TU integrality. For each discrete convex univariate cost
`f_i`, linearly interpolate its values between adjacent integer labels.
On a unit grid cell the sum of these interpolants is affine. If `Az=b`
and the bounds are integral, the intersection of a unit cell with the
feasible polytope is integral: after translating/scaling the cell, TU
integrality applies to the equality and the added coordinate bounds.
Writing any feasible point as a convex combination of the cell's integral
vertices shows that the continuous piecewise-linear relaxation has the
same minimum as the integer problem.

At an integer optimum, an optimal equality multiplier `lambda` makes each
coordinate minimize its adjusted scalar cost
`f_i(t)-(A^T lambda)_i t`. The adjacent first differences give the
minimizer interval: for an interior label `z_i`,

```text
f_i(z_i)-f_i(z_i-1) <= (A^T lambda)_i
                         <= f_i(z_i+1)-f_i(z_i),
```

with the corresponding one-sided condition at a domain endpoint. By
complementary slackness, every primal optimum is coordinatewise in these
intervals, and every feasible integer vector in the intervals is optimal.
The result is the full tied-optimum set, not just the particular witness
returned by an oracle.

For polynomial costs depending on a continuous core, the adjacent
differences are fixed-degree polynomials in that core. The theorem first
substitutes fixed native coordinates and then removes dependent equality
rows after checking consistency; the remaining intervals have positive
length. The dual polyhedron is then pointed because a line direction would
lie in the kernel of the full-row-rank matrix. Its vertices have bases from
signed TU columns, with determinant `+1` or `-1`. A base-bounded multiplier
box and these bases give the theorem's finite symbolic chart family. These
are standard piecewise-linear LP basis facts; the theorem's finite-law
composition is assessed separately below.

## The interval-violation proximity factor

The proposed generalization replaces network-cycle decomposition by a
conformal circuit decomposition of an integer kernel vector. For TU `A`,
primitive circuit directions have entries in `{−1,0,1}`. Given a feasible
integer `z` and the feasible optimum set `Y_0` represented by the dual
intervals, choose `bar_z in Y_0` minimizing `||z-bar_z||_1`. Decompose
`z-bar_z` into sign-compatible circuit steps. Each step must encounter an
interval endpoint that blocks the same step inside `Y_0`; otherwise adding
that step to `bar_z` would preserve feasibility and reduce its distance to
`z`. Charge a step to one blocking coordinate. Sign compatibility bounds
the total charge at coordinate `i` by its interval violation
`dist(z_i,I_i)`, and each circuit has at most `n` nonzero coordinates.
This yields the proposed bound

```text
||z-bar_z||_1 <= n sum_i dist(z_i,I_i).
```

The factor `n` is a direct support-size/charging bound once the conformal
decomposition and TU circuit normalization are in place. Graver, “On the
Foundations of Linear and Integer Linear Programming I,” *Mathematical
Programming* 9(1) (1975), 207–226, DOI
[10.1007/BF01681344](https://doi.org/10.1007/BF01681344), is a relevant
identified predecessor. The publisher exposes only its abstract, and the
sole ingester could not retrieve the article or PDF; the local record is
metadata-only/unread. No theorem or page locator is therefore attributed to
it. The reviewed theorem gives its own support-minimal kernel-vector
argument and proves the TU unit-entry property from determinants, so the
proximity proof is self-contained even without that source.

## Comparison boundary

The exact TU oracle, piecewise-linear interpolation, dual interval
optimality, and conformal circuit moves are established or proved directly
in the theorem. The reviewed result adds an expected exact global-search
guarantee under perturbations restricted to a small continuous core,
including its parameter dependence, one finite noise law, and same-draw
fallback. Its structured bilinear-cost corollary has a sharper bound, and
the bounded-slack reduction covers bounded TU inequalities. These claims
are not supplied by the classical recourse theorem; this scoped comparison
does not establish novelty.

Sources examined: the full H&S primary paper and its exact TU theorem
locators are recorded in the local
[source package](../../literature/papers/hochbaum1990-convex-separable-optimization-is-not/)
and [flow-oracle audit](integer-convex-flow-recourse-prior.md). Graver 1975
is identified but remains unread because the publisher route was blocked;
the theorem does not rely on it for the circuit proof. No literature-KB or
index files were edited.
