# Independent integer features give dimension bounds without disjoint blocks

Date: 2026-09-05. Status: independently reviewed theorem.

Positive sums of squares of independent integer linear forms admit an
integer-count bound governed by the row lengths of the feature matrix.
In particular, bounded integer row lengths give additive `O(r)` overhead,
even when the features overlap in the original variables and the Hessians
do not commute.

## Statement

Let `T in Z^(r by n)` have full row rank, with `r>=1`, and consider

```
f_j(x)=(1/2)sum_(i=1)^r a_ji(T_i x)^2+l_j^T x+b_j,
x in [0,1]^n,                a_ji>=0.
```

Each feature is active: for each `i`, some `a_ji>0`. Define

```
w_i=sum_k |T_ik| >=1,
ell_i=sum_(k:T_ik<0) T_ik,
C_ji=a_ji w_i^2.
```

Let `K subset R^m` be a compact convex unconditional error body with zero
in its interior, and use the whole-graph approximation and integer-count
minima from the [forest theorem](forest-laplacian-quadratic-precision.md).
Set

```
D=max{product_i p_i: 0<=p_i<=1, Cp in K},
Phi=-(1/2)log2 D,
A_r=r+log2[omega_r(r+2)^(r/2)]<4r,
Omega={diag(w)^(-1)(Tx-ell): x in [0,1]^n},
V=vol_r(Omega).
```

Then

```
max(0,Phi-A_r+log2 V)<=p_conv<=p_bin<=Phi+r.             (1)
```

If all coefficients are rational and `K` has a polynomial-time rational
strong separation oracle and known positive rational inner and outer
radii about zero, a deterministic polynomial-time algorithm constructs a
rational MILP of polynomial size satisfying

```
p_out<=p_conv+A_r+r-log2 V+1/(2ln2)
     <=p_conv+5r+sum_i log2 w_i+1.                      (2)
```

The nonlinear input rank is `r`. A uniform bound `w_i<=s` gives overhead
at most `(5+log2 s)r+1`. The matrix `T` need not be totally unimodular,
and its rows need not have disjoint supports. The feature representation
is part of the input; no algorithm for discovering a favorable positive
square decomposition is claimed.

## A minor controls the normalized domain volume

The coordinates `u_i=(T_i x-ell_i)/w_i` lie in `[0,1]`, and `Omega` is a
full-dimensional compact convex image of the cube. Choose any set `I`
of `r` columns for which `T_I` is nonsingular. Fix all other input
coordinates at zero. The corresponding image is a parallelotope contained
in `Omega`, of volume

```
|det T_I|/product_i w_i >=1/product_i w_i.               (3)
```

The inequality uses only that the nonzero determinant is an integer.
This volume argument requires no calculation of the volume of the whole
zonotope. More generally, any explicit nonzero minor gives the sharper
bound `V>=|det T_I|/product_i w_i`; it can be computed by rational Gaussian
elimination in polynomial time. Since `Omega` lies in the unit cube,
these quantities never exceed one.

In the new coordinates the nonlinear outputs are

```
g_j(u)=(1/2)sum_i a_ji(w_i u_i+ell_i)^2,
```

with diagonal nonnegative Hessians `diag(C_j)`. The common kernel of the
original Hessians is exactly `ker T`, because all features are active
and all coefficients are nonnegative. Thus the common nonlinear input
rank is `r`.

## Precision comparison and rational construction

The exact affine quotient argument from the forest theorem applies
verbatim: subtract the original affine output before projecting through
`u=diag(w)^(-1)(Tx-ell)`, and reverse the projection by retaining the
original continuous `x`, its box constraints, and that rational linear
equation. It preserves both formulation minima even when the original
affine output varies within a fiber of `T`.

The diagonal trace covariance proof on any convex subdomain of the
unit cube bounds every parity-support volume by
`2^(A_r)sqrt(D)`. The supports cover volume `V`, so the lower bound in
(1) follows. The coordinate square-prefix model on the containing cube
uses at most `Phi+r` binaries and has coordinatewise errors bounded by
`Cp/8`, hence errors in `K`. Restricting it with the original continuous
input variables gives the upper bound in (1).

Use the reviewed [rational log-product oracle](../notes/rational-log-product-convex-body-oracle.md)
to find an exactly feasible positive rational allocation with product
at least `exp(-1)D`. The prefix formulation then adds at most
`1/(2ln2)` to its ideal count. Every equation and gadget is rational and
has polynomial encoding length; `w_i`, `ell_i`, and their squares also
have polynomial encoding length. Combining this with (3) proves (2).
The algorithm does not need to know or approximate `V`.

## Interpretation and limitations

A common forest incidence matrix has `w_i=2`, so (2) gives the forest
bound `p_out<=p_conv+6r+1`. The forest theorem additionally computes the
exact normalized domain volume, which can sharpen that estimate.
More generally, independent integer forms involving a bounded number
of variables with bounded integer coefficients give the same linear-rank
order. Overlap of those supports is allowed, including a single large
connected Hessian adjacency block.

The dependence on the row lengths is intentional. A rational feature
matrix may be converted to integer rows by clearing denominators and
absorbing each row scaling into its coefficients `a_ji`; primitive rows
can then be obtained by dividing by their greatest common divisors.
These operations preserve rational polynomial input length, but the
resulting integer row lengths may be large. This theorem therefore does
not infer linear overhead for arbitrary ill-conditioned real or rational
linear feature changes.

For the [thin-domain obstruction](../notes/block-psd-domain-correlation-obstruction.md),
features `x_1` and `x_1+delta x_2` with `delta=1/M` become the primitive
integer rows `(1,0)` and `(M,1)`. The row-length term is `log2(M+1)`,
so the present statement does not contradict that obstruction.

Integer minor bounds, box images under linear maps, and separable square
formulations are established ingredients. The proposed contribution is
this explicit formulation-wide near-minimum integer-count guarantee for
a given positive integer-feature representation. The [bounded source audit](../notes/independent-integer-feature-precision-novelty.md)
found no matching guarantee, while identifying separable convex functions
of overlapping affine forms as established formulation practice.
Publication priority remains unestablished.

The [first independent audit](../notes/review-independent-integer-feature-precision.md)
and [second independent audit](../notes/review-independent-integer-feature-precision-second.md)
both passed. The [exact checker](../code/quadratic_rank/check_integer_feature_precision.py)
passed 30 minor-volume, normalized-range, common-rank, quotient, and
rational-rescaling cases.
