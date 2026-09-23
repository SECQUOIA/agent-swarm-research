# Block PSD quadratic precision under unconditional error budgets

Date: 2026-09-05. Status: independently reviewed extension.

The block PSD precision theorem also holds for a whole unconditional
convex error budget. A direct Euclidean log-determinant allocation
oracle provides the polynomial rational construction. No output
ellipsoid approximation or geodesic solver is needed for this extension.

## Statement

Use the common original-coordinate block partition and positive
semidefinite Hessian blocks of the reviewed
[block PSD theorem](../results/block-psd-quadratic-precision.md):

```
H_j=diag(H_j1,...,H_jB),       H_jb>=0,
```

with block sizes `d_b` and `N=sum_b d_b`. Affine terms are arbitrary.
Let `K subset R^m` be a compact convex body invariant under every
coordinate sign change, with a polynomial-time rational strong
separation oracle and known positive rational inner and outer radii.
Require `w-f(x) in K` for every admitted approximation point, and
contain the exact graph on `[0,1]^N`.

Set

```
E(P)_j=sum_b tr(H_jb P_b),
D_K=max{product_b det P_b: 0<=P_b<=I, E(P) in K},
Phi_K=-(1/2)log2 D_K.
```

With exactly the constants `A,B_grid` of the block PSD theorem,

```
max(0,Phi_K-A)<=p_conv<=p_bin<=Phi_K+B_grid.              (1)
```

For rational input a deterministic polynomial-time algorithm constructs
a rational MILP within additive

```
O(sum_b d_b log(d_b+1))
```

of `p_conv`. After eliminating the common kernel separately inside
each original block, the stronger bound is

```
p_out<=p_conv+O(sum_(b:r_b>0) r_b log(r_b+1)),
r_b=rank[H_1b;...;H_mb].                               (2)
```

The constant is universal and does not depend on output dimension,
coefficients, tolerances encoded by `K`, or original block sizes beyond
the displayed ranks. Full input dimensions, oracle complexity, and
radius encodings still enter runtime and the continuous model size.

## The covariance trace vector is dominated by an expected Jensen vector

For two exact graph points in one parity support, their admitted graph
midpoint has nonnegative Jensen error vector

```
J_j(x,y)=(1/8)sum_b (x_b-y_b)^T H_jb(x_b-y_b),
J(x,y) in K.
```

For independent uniform points in a positive-volume compact support,
with full covariance `Sigma`, convexity gives

```
EJ in K,       (EJ)_j=(1/4)sum_b tr(H_jb Sigma_bb).
```

Put `c_b=max{4,d_b/4}` and `P_b=Sigma_bb/c_b`, as in the block
covariance proof. Then the caps hold and, by positive semidefiniteness,

```
0<=E(P)<=EJ
```

coordinatewise. An unconditional convex body contains every vector
whose coordinate magnitudes are dominated by one of its members.
Consequently `E(P) in K`. The block determinant and volume arguments
are unchanged, proving the lower half of (1).

For the upper half, the reviewed within-block grid gives the simultaneous
componentwise estimate

```
|w-f(x)|<=E(P)/8.
```

Thus every admitted error belongs to `K`. Exact graph containment and
all binary counts are unchanged. The final linear formulation uses
shared residual monomial variables; it does not encode the possibly
curved set `K` itself by linear inequalities.

## A direct rational convex allocation oracle

The map `E` is rational and linear in the independent block entries,
and the objective `sum_b log det P_b` is concave. The supporting
[block log-determinant oracle](../notes/rational-block-logdet-convex-body-oracle.md)
therefore applies directly. It returns exactly feasible positive
definite rational blocks with

```
product_b det P_b>=exp(-1)D_K.
```

The proof supplies spectral lower caps excluding no optimizer, a known
rational inner ball in a log-determinant hypograph, exact rational
matrix-inverse tangents, and the classical GLS weak optimization
interface. An explicit rational central-ball repair ensures exact
feasibility. Only scalar logarithms of rational determinants are
approximated; no matrix geodesic computation is used.

For the final grid use the already reviewed rational orthogonal Jacobi
construction separately in each block. Its rational grid covariance
satisfies `P_b/8<=P_tilde_b<=P_b/2`. Because the Hessians are positive
semidefinite,

```
0<=E(P_tilde)<=E(P).
```

Unconditionality therefore preserves budget feasibility. The determinant
loss is at most `N log 8`, so the construction costs only `O(N)` extra
binaries beyond the finite benchmark bound.

Finally repeat the base theorem's blockwise common-kernel quotient and
product-zonotope normalization. The Hessians remain PSD in their blocks,
while the output body `K` is unchanged. The domain-volume penalty is
`O(sum_b r_b log(r_b+1))`. This proves (2) with the exact rational
linear lift of the original product domain.

## Scope and novelty boundary

This extension includes boxes, weighted absolute-sum budgets, and
Euclidean error balls under their oracle assumptions. An arbitrary
correlated ellipsoid need not be unconditional. The original disjoint
coordinate-block and product-domain condition remains in force; it
cannot be obtained for free through copy variables.

The matrix allocation is established convex log-determinant optimization.
The proposed extension is the Jensen-vector lower comparison and the
whole-body error guarantee with the same individual-block-rank overhead.
The [source and novelty assessment](../notes/block-psd-unconditional-error-novelty.md)
distinguishes classical MAXDET from the GLS oracle implementation for
error bodies without finite LMI descriptions. It found no matching
whole-formulation theorem in the bounded search; publication priority
remains unestablished.

The [first proof audit](../notes/review-block-psd-unconditional-precision.md)
and [second proof audit](../notes/review-block-psd-unconditional-precision-second.md)
both passed for this extension and its direct matrix oracle. The checker
`code/quadratic_rank/check_block_logdet_repair.py` passed 24 rational
matrix repairs with exact spectral, budget, and objective bounds and
100-digit log-determinant checks. The second reviewer reran it.
