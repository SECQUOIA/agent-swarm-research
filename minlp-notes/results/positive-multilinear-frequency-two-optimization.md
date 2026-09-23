# Exact envelope evaluation for frequency-two positive polynomials

Date: 2026-09-04.

Status: algorithmic corollary independently reviewed; see [the audit](../notes/review-multilinear-frequency-two-optimization.md). The matching and edge-cover machinery is classical. No novelty claim is made for this reduction or its envelope consequence.

Consider the unit-cube positive polynomial and dual graph from [the frequency-two gap theorem](positive-multilinear-frequency-two-gap.md). Assume rational coefficients and a rational point `x`.

Discarded affine terms can be added back to the final envelope and absorbed into `lambda` in the binary oracle. Variables appearing in no nonlinear term optimize separately in that oracle.

**Corollary.** Its convex-envelope value at `x` can be computed exactly in polynomial bit time. A supporting affine minorant can also be obtained. The concave envelope is already explicit, so the full scalar graph hull admits polynomial-time separation. This claim does not provide a polynomial-size explicit formulation of the full lifted multilinear polytope.

## Binary optimization reduces to edge cover

For arbitrary rational `lambda`, the needed binary optimization problem is

```
min_{X in {0,1}^n} f(X)-lambda^T X.
```

Let `Z=1-X` be the selected failure edges of the dual graph. The objective becomes

```
-sum_i lambda_i
 + sum_i lambda_i Z_i
 + sum_v a_v 1{v is uncovered by Z}.                  (1)
```

Dummy vertices for single-incidence variables have zero penalties. A negative-cost edge can always be included: adding it strictly decreases its edge cost and cannot increase any uncovered-vertex penalty. Include all such edges, add their costs to the objective constant, remove them from the remaining decision set, and set the penalties of their endpoints to zero. All remaining edge costs and vertex penalties are nonnegative.

This is prize-collecting edge cover. The following explicit reduction suffices. Add two new vertices `h,k` with a zero-cost edge between them. For every existing vertex `v`, add an edge `vh` with cost equal to its uncovered-vertex penalty. Keep all remaining original edges with their original nonnegative costs. Find a minimum-cost edge cover of the augmented graph.

Every original selected edge set can be extended to an augmented edge cover by adding the penalty edge for each uncovered vertex and the zero-cost edge `hk`; its added cost is exactly the uncovered penalties. Conversely, take an augmented edge cover and keep its original edges. Each original vertex they leave uncovered must have its penalty edge in the augmented cover. Thus the original edge costs plus uncovered penalties are no greater than the augmented cover's cost. These two directions prove equality of the optimal values. They also recover an optimal binary vector for (1).

Minimum-cost edge cover has a polynomial-time reduction to weighted matching. Therefore (1) is an exact polynomial-time binary oracle, including arbitrary signs of `lambda`.

## Envelope computation

The convex envelope at `x` is the finite-distribution LP

```
min sum_{v in {0,1}^n} pi_v f(v)
subject to sum_v pi_v=1, sum_v pi_v v=x, pi_v>=0.
```

Its dual is

```
max eta+lambda^T x
subject to eta+lambda^T v<=f(v) for every binary v.
```

Separation of the dual constraints is exactly the binary minimization oracle above. Standard rational LP optimization with a polynomial-time separation oracle therefore computes the exact value and an optimal dual affine minorant in polynomial bit time.

Here is an explicit encoding bound. Let `A=sum_v a_v`, after affine terms have been removed. The dual feasible polyhedron contains no line because the vectors `(1,v)` over the binary cube span `R^(n+1)`. Its attained optimal face therefore contains a vertex. That vertex solves `n+1` independent tight equations with a nonsingular zero-one coefficient matrix and right-hand sides in `[0,A]`. Its determinant has magnitude at least one, and Cramer's rule bounds every coordinate by `(n+1)! A`. Consequently restricting every dual coordinate to `[-B,B]`, where `B=max{1,(n+1)! A}`, preserves an optimum and supplies a polynomial-bit bounding box for rational separation-to-optimization. Boundary points cause no exception: the finite vertex LP remains feasible and bounded, with an attained dual optimum.

The concave envelope `sum_v a_v min_{i in S_v} x_i` is explicit. At a point outside the scalar graph hull, the lower supporting minorant or an upper supporting affine piece separates it; cube violations are separated by their coordinate bounds.

## Literature and limits

The underlying prize-collecting edge-cover problem is established. A primary modern source explicitly describes the classical weighted-edge-cover reduction to weighted matching: *On Constrained Minimum Weight Edge Covers With Applications to Emergency Planning* (Networks, 2025), [published article](https://onlinelibrary.wiley.com/doi/full/10.1002/net.22261). A source review should still determine whether this exact multilinear-envelope corollary has already been stated.

The unit-cube and zero-lower-box scope is the same as in the sharp gap theorem. An affine rescaling from arbitrary positive lower bounds does not preserve the simple uncovered-vertex objective in (1).

The independent audit also checked 150 small exhaustive instances of the reduction, including negative edge costs, parallel edges, zero penalties, and isolated vertices. Its record links the exact verification script.
