# Forest-Laplacian quadratic graph precision with linear rank overhead

Date: 2026-09-05. Status: independently reviewed theorem.

A common forest of positive squared differences gives an additive `O(r)`
integer-count guarantee even when the Hessians have one large connected
block in the original coordinates. The key is the exact volume of the
forest incidence image of a cube. It controls the domain correlation
introduced by diagonalizing the quadratic terms.

## Statement

Let `F=(V,E)` be a forest on `n` vertices and `r=|E|`. Orient its edges
arbitrarily and write `B` for its `r` by `n` incidence matrix. Consider

```
f_j(x)=(1/2)sum_(e=uv in E) a_je (x_u-x_v)^2+l_j^T x+b_j,
x in [0,1]^n,             a_je>=0.
```

Remove every edge whose coefficient is zero in every output. The remaining
forest is the one used below; all its edges are active. The common nonlinear
input rank is exactly `r`. If `r=0`, the graph is affine and needs no integers.

Let `K subset R^m` be a compact convex unconditional body containing zero
in its interior. A valid graph approximation contains every exact graph
point and allows only errors `w-f(x) in K` on the original cube. The minima
`p_conv` and `p_bin` refer respectively to arbitrary convex mixed-integer
lifts with general integers, and mixed-binary linear lifts. No restriction
on continuous lift size is imposed in the lower bound.

For `r>=1`, let `n_c` be the vertex counts of the connected components,
including isolated vertices, and define

```
C_je=4 a_je,
D=max{product_e p_e: 0<=p_e<=1, Cp in K},
Phi=-(1/2)log2 D,
V_F=2^(-r) product_c n_c,
A_r=r+log2[omega_r(r+2)^(r/2)]<4r.
```

The following finite bounds hold:

```
max(0,Phi-A_r+log2 V_F)<=p_conv<=p_bin<=Phi+r.          (1)
```

For rational quadratic coefficients, a polynomial-time rational strong
separation oracle for `K`, and known positive rational inner and outer
radii about zero, a deterministic polynomial-time algorithm constructs a
rational MILP of polynomial size with

```
p_out<=p_conv+A_r+r-log2 V_F+1/(2ln2)
     <=p_conv+6r+1.                                    (2)
```

The first inequality can retain the actual component sizes. The running
time is polynomial in the full input and oracle encoding, not just in `r`.
No efficient solution method for the resulting general MILP is asserted.
The finite statement does not require rationality or an oracle.

## Exact quotient and the incidence-domain volume

Set `z=Bx` and `u=(z+1)/2`. Each coordinate of `z` lies in `[-1,1]`, so

```
Omega=(B[0,1]^n+1)/2 subset [0,1]^r.
```

The domain is a full-dimensional compact convex zonotope. The nonlinear
part becomes

```
g_j(u)=(1/2)sum_e a_je(2u_e-1)^2,
```

whose Hessian is the nonnegative diagonal matrix with diagonal `C_j`.
All remaining terms are affine.

The graph-precision minima for the original problem and for `g` on
`Omega` are equal. In the forward direction, first restrict the original
lift to the cube, subtract `l_j^T x+b_j` from every output, and project
through `u=(Bx+1)/2`. The exact graph maps onto the exact graph of `g`,
and errors are preserved. In the reverse direction, keep the original
continuous variable `x`, impose its box constraints and the displayed
linear equation for `u`, and restore the affine output. These operations
preserve convexity, linearity where applicable, and the integer count.
In particular, varying affine terms along an incidence fiber cause no
problem. All maps have rational coefficients when the original data do.

For completeness, the domain volume follows from an elementary tiling.
Consider one tree on `s>=2` vertices with incidence matrix `B_T`. For
any `x in [0,1]^s`, subtract `min_i x_i` from every coordinate. This does
not change `B_T x` and gives the unique representative in the cube with
minimum coordinate zero: any two representatives with equal incidence
image differ by a constant vector, and the two minima determine that
constant. Consequently `B_T[0,1]^s` is the union of the images of the
`s` faces `x_v=0`.

Each image is a parallelotope of volume `|det (B_T)_{-v}|=1`. This minor
has determinant `+1` or `-1`: delete a leaf other than the omitted vertex
and expand along its column, proceeding inductively. Two distinct face
images intersect only in the image of representatives with at least two
zero coordinates. Those intersections have dimension at most `s-2`,
and hence zero `(s-1)`-dimensional volume. Therefore

```
vol_(s-1)(B_T[0,1]^s)=s.
```

Different forest components use disjoint coordinates, so their images
form a Cartesian product. Isolated vertices contribute no image dimension
and a factor one. Rescaling all `r` coordinates by one half gives

```
vol_r(Omega)=V_F=2^(-r)product_c n_c >=2^(-r).           (3)
```

The rows of a forest incidence matrix are independent. Because every
edge is active and coefficients are nonnegative, a vector belongs to
the common kernel of all Hessians exactly when it is constant on every
component. Thus the nonlinear input rank is `r` as claimed.

## The diagonal trace lower bound on the correlated domain

The reviewed [diagonal PSD theorem](../results/diagonal-psd-quadratic-linear-dimension-precision.md)
and its [unconditional-budget extension](../results/positive-separable-unconditional-error-precision.md)
apply to supports inside `Omega` with the same support-volume bound.
Here is the specific argument showing the only domain change.

For two exact graph points in the same parity support, their graph
midpoint is admitted by convexity of the lifted relaxation. Since
`Omega` is convex, its input midpoint is in the domain, and its error
is the nonnegative Jensen vector

```
J_j(u,v)=(1/8)sum_e C_je(u_e-v_e)^2 in K.
```

Closure preserves this condition. Let `Sigma` be the covariance of
independent uniform points in a compact positive-volume support. Taking
expectations gives `EJ=(1/4)C diag(Sigma) in K`. Thus the allocation
`p_e=Sigma_ee/4` is feasible: its coordinates are at most `1/16`, and
`Cp=EJ`. Hadamard's inequality and the volume-covariance bound imply

```
vol(support)
 <=omega_r(r+2)^(r/2) sqrt(det Sigma)
 <=2^r omega_r(r+2)^(r/2) sqrt(D)
 =2^(A_r) sqrt(D).
```

The at most `2^p` parity supports cover `Omega`. The usual compact-support
approximation or closure argument from the base theorem therefore gives
`V_F<=2^(p+A_r)sqrt(D)`, which proves the lower bound in (1).
No assumption that the transformed domain is a product is made.

## A compact rational construction

For any positive feasible allocation `p`, use the reviewed shared
square-prefix construction on the whole containing `r`-cube, with

```
L_e=ceil[(1/2)log2(1/p_e)],       h_e=2^(-L_e).
```

It contains the exact graph and admits only errors satisfying
`|w_j-g_j(u)|<=(Cp)_j/8`. Unconditionality of `K` implies that these
errors belong to `K`. Restrict it to `Omega` by keeping the original
continuous `x` and imposing `u=(Bx+1)/2`. This does not add integers or
remove any exact original graph point. The upper bound in (1) follows
from `sum_e L_e<=Phi+r` at an optimal allocation.

The reviewed [rational log-product oracle](../notes/rational-log-product-convex-body-oracle.md)
returns a positive rational feasible allocation with
`product_e p_e>=exp(-1)D` in polynomial time under the stated assumptions.
All prefix gadgets and incidence equations are rational, and their size
is polynomial in the full encoding. The extra allocation loss is at most
`1/(2ln2)` binaries in the real-valued count bound. Combining this with
the lower bound and (3) proves (2).

## Scope and novelty boundary

The family includes simultaneous positive weighted Laplacian outputs
on any common forest, with arbitrary affine terms. A long path or a
large star can produce a single original Hessian adjacency block of
unbounded size. Different weighted Laplacians on the same forest need
not commute. Thus the result goes beyond the earlier fixed-block-rank
condition while retaining linear overhead in the common nonlinear rank.

The exact incidence quotient, unimodular incidence minors, and zonotope
volume are classical ingredients; no separate novelty claim is made for
them. The proposed contribution is their use in the universal finite
integer-count comparison with a compact polynomial rational construction.
The [bounded source audit](../notes/forest-laplacian-quadratic-precision-novelty.md)
found no matching whole-formulation theorem and credits the classical
zonotope-volume, parity, and compact-square predecessors. Publication
priority remains unestablished.

The forest assumption is material to the stated proof. Arbitrary cyclic
graphs need not become diagonal positive quadratics in a set of independent
edge coordinates. Likewise, replacing the incidence domain by a containing
cube without accounting for its volume is not valid for arbitrary linear
changes of variables; the [thin-domain obstruction](../notes/block-psd-domain-correlation-obstruction.md)
illustrates the failure in general.

The [first independent audit](../notes/review-forest-laplacian-quadratic-precision.md)
and [second independent audit](../notes/review-forest-laplacian-quadratic-precision-second.md)
both passed. The [exact checker](../code/quadratic_rank/check_forest_laplacian_precision.py)
passed 36 forest cases, 216 incidence minors, and 288 quotient, Jensen,
and canonical-representative checks.

The [independent integer-feature extension](independent-integer-feature-quadratic-precision.md)
replaces incidence rows by arbitrary independent integer linear forms.
A bound on their row lengths gives linear overhead even with overlapping
supports; the forest formula supplies a sharper exact domain volume.
