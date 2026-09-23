# Near-minimal quadratic formulations depend on nonlinear input rank

Date: 2026-09-05. Status: independently reviewed structural refinement.

The dimension term in the reviewed construction can be based on the
number of input directions used by the quadratic parts. Affine input
directions need not contribute to the additive integer-count error.
The projected domain is a zonotope, so all domain restrictions still
have an exact rational linear lift.

## Theorem

Let `f_j(x)=(1/2)x^T H_j x+a_j^T x+b_j` have rational coefficients
on `[0,1]^n`. Let the symmetric output-error body `K` satisfy the
rational strong separation and known-radius assumptions of the
[general-norm theorem](../results/quadratic-general-norm-output-precision.md).
Set

```
r=rank [H_1; H_2; ...; H_m].
```

There is a deterministic polynomial-time rational MILP construction
with

```
p_out<=p_conv(f,K)+C r log2(r+1),                        (1)
```

where `C` is universal. Running time and continuous formulation size
still depend on the full input dimensions and encoding. If `r=0`, the
graph is affine and has an exact LP formulation with zero integers.
No numerical rank decision is used: all ranks and factorizations here
are exact rational operations.

The reviewed [approximation hardness theorem](../results/quadratic-integer-precision-approximation-hardness.md)
also excludes a uniform polynomial-time additive `O(r^(1-delta))`
guarantee for any fixed `0<delta<1`, unless `P=NP`. The same statement
holds for multiplicative approximation under its positive-optimum
promise. Indeed, `r<=n`, so either such guarantee would imply the
forbidden `O(n^(1-delta))` guarantee on that theorem's unit-tolerance
convex-quadratic instances. This gives the same dimension-exponent
barrier for the refined parameter; it does not exclude, for example,
an `r/log(r+1)` additive guarantee.

## Exact quotient by the common Hessian kernel

Choose a rational full-row-rank matrix `U` whose rows span all rows
of all `H_j`. Then

```
ker U=intersection_j ker H_j.
```

Let `F=U^T(UU^T)^(-1)` be a rational right inverse. The matrices
`G_j=F^T H_j F` satisfy `H_j=U^T G_j U`: `FU` is the orthogonal
projection onto the common row space, and both rows and columns of
every symmetric `H_j` lie in that space.

With `c=(1/2)1`, there is a rational affine map `a(x)` such that

```
z=U(x-c),
f(x)=a(x)+g(z),       g_j(z)=(1/2)z^T G_j z.
```

The reduced domain is the centered rational zonotope

```
Z=U[-1/2,1/2]^n subset R^r.
```

The formulation minima are exactly preserved:

```
p(f,[0,1]^n,K)=p(g,Z,K)                                 (2)
```

for both arbitrary convex lifts and binary LP lifts. To reduce a
formulation, first impose the cube inequalities if they are not already
explicit, then project it under the affine map
`(x,w)->(U(x-c),w-a(x))`. Each exact graph point of `g` is reached
because every `z in Z` has a preimage `x`; the admitted output errors
remain in `K`. In the reverse direction, impose `z=U(x-c)`, the original
cube inequalities, and `w=a(x)+v`. No integers are added in either
direction. This works even when `a(x)` varies along fibers of `U`.

## The projected cube can be rounded in polynomial time

The zonotope has a polynomial-time rational strong separation oracle:
its membership problem is the rational LP feasibility system

```
U t=z,       -1/2<=t_i<=1/2.
```

A feasible LP proves membership. If it is infeasible, solve the rational
LP feasibility system in variables `h,v`

```
v_i >= (U^T h)_i,       v_i >= -(U^T h)_i,
h^T z-(1/2)sum_i v_i >=1.
```

Strict separation of the compact zonotope, followed by positive
rescaling, makes this second system feasible exactly when `z notin Z`.
Its rational solution supplies the separator
`h^T y<=(1/2)sum_i v_i`, valid for every `y in Z` and violated by `z`.
Classical [polynomial-time rational linear programming](https://www.mathnet.ru/eng/zvmmf5239)
gives these feasibility decisions; a feasible basic solution has
polynomial encoding length by determinant bounds. This is a standard
LP ingredient, not a new oracle algorithm.

For explicit radii, choose `r` independent columns `U_J`. Let
`c_inv=1+sum_ik |(U_J^(-1))_ik|` and
`R_0=1+sum_ik |U_ik|`. Then

```
[1/(2c_inv)] B_2^r subset U_J[-1/2,1/2]^r
                          subset Z subset R_0 B_2^r.
```

The rational radii have polynomial encoding length. Apply the same
classical strong-oracle rounding and symmetry argument as in the
general-norm theorem, now to the domain `Z`. It produces a rational
positive definite matrix `A` such that

```
E(A)/beta subset Z subset E(A),
E(A)={z:z^T A z<=1},       beta=(r+1)sqrt(r).             (3)
```

## A rational coordinate normalization without irrational factors

Compute an exact rational factorization `A=L D L^T`, where `L` is
unit lower triangular and `D` has positive rational diagonal entries.
For each pivot choose a positive dyadic number `b_i` with
`sqrt(D_ii)<=b_i<=2sqrt(D_ii)`, by exact comparisons of dyadic squares.
Set `R=diag(b_i)L^T`. Then

```
A<=R^T R<=4A,
(1/beta)B_2^r subset RZ subset 2B_2^r.                  (4)
```

The first ball inclusion follows because `||y||<=1/beta` implies
`z=R^(-1)y` satisfies `z^T A z<=1/beta^2`, hence `z in Z` by (3).
The outer inclusion follows from the other quadratic-form inequality.
All factors have polynomial rational encoding; no exact irrational
square root or eigenvector is needed.

Normalize the domain to

```
Omega=(1/2)1+(1/4)RZ subset [0,1]^r.
```

It contains a centered ball of radius `1/(4beta)`, hence a cube of
side `1/[2beta sqrt(r)]=1/[2r(r+1)]`. In particular,

```
log2 vol(Omega)>=-r log2[2r(r+1)].                      (5)
```

The transformed outputs
`q(y)=g(4R^(-1)(y-(1/2)1))` are rational quadratics. Their graph on
`Omega` has the same formulation minima as `(g,Z)`. For an exact
rational lift of the domain, retain the original `x` and impose
`y=(1/2)1+(1/4)RU(x-c)`, `x in [0,1]^n`.

## The finite covariance lower bound needs only domain volume

For any full-dimensional compact convex domain `Omega subset [0,1]^r`, the
parity-support covariance proof for an ellipsoidal error budget gives

```
p_conv(q,Omega,tE_0)>=Phi(t)-A_r+log2 vol(Omega),        (6)
```

with the same covariance benchmark and constants as the reviewed
ellipsoidal theorem in dimension `r`. Indeed, each support has volume
at most `2^(A_r-Phi(t))`, while the `2^p` supports now cover volume
`vol(Omega)` rather than one. All covariance caps and midpoint
identities are unchanged. This is the only modification of that lower
bound.

For output errors, write `q(y)=b(y)+T q_bar(y)`, where `b` is rational
affine and the full-column-rank rational matrix `T` spans the image of
the quadratic coefficients, as in the general-norm theorem. The map
`q_bar` has `d<=r(r+1)/2` outputs. Define
`K_eff={e:T e in K}`; the exact affine-intersection reduction preserves
`p_conv(q,Omega,K)=p_conv(q_bar,Omega,K_eff)`. Classical rounding supplies
a rational ellipsoid `E_0` in `R^d`
with

```
E_0 subset K_eff subset alpha E_0,
alpha=(d+1)sqrt(d).
```

Here `Phi` is formed from the Hessians of `q_bar` and the rational
quadratic form defining `E_0`. The general-norm comparison, now using
(6) for `q_bar`, gives

```
Phi(1) <= p_conv(q,Omega,K)+A_r-log2 vol(Omega)
           +(r/2)log2 alpha.                            (7)
```

Construct the reviewed rational MILP for `q_bar` on the entire
containing cube `[0,1]^r`, using the ellipsoid `E_0`. Its binary count
is at most `Phi(1)+B_r+O(r)`. Restore the output via
`w_q=b(y)+T w_bar`, restrict to `Omega` by the exact linear domain lift
above, and undo the original affine input/output maps. The resulting model
is valid for the original problem. Combining (5)--(7) and (2) yields

```
p_out <= p_conv(f,K)+A_r+B_r+O(r)
           +r log2[2r(r+1)]+(r/2)log2 alpha.
```

Every term after `p_conv` is `O(r log(r+1))`, proving (1). If all
transformed quadratic outputs vanish, their image dimension is zero
and the original graph was already affine; this is the `r=0` case.

## Scope and verification boundary

The affine quotient, zonotope separation, LDL factorization and
ellipsoid rounding are classical tools. The proposed refinement is the
near-minimal integer-count guarantee based on common nonlinear input
rank, rather than on all input variables. It does not give an exact
MILP description of an arbitrary curved domain: the domain here is a
linear image of the original cube and has an explicit linear lift.
The [source and novelty audit](../notes/quadratic-nonlinear-input-rank-precision-novelty.md)
records close predecessors for ridge functions, active subspaces, and
fixed-rank box-to-zonotope reductions. None of those reductions is
claimed as new here. No matching integer-count theorem was found in
the bounded source search; this does not establish publication priority.
The [first independent proof audit](../notes/review-quadratic-nonlinear-input-rank-precision.md)
and [second independent proof audit](../notes/review-quadratic-nonlinear-input-rank-precision-second.md)
both passed. Their records are preserved in distinct files.

The parameter `r` is the rank of the stacked Hessians, not the maximum
rank of an individual Hessian or the noncommutative rank of their span.
The theorem improves the additive overhead; it does not remove the
optimum count's dependence on accuracy or make general MILP optimization
polynomial-time.

The reproducible checker `code/quadratic_rank/check_nonlinear_input_rank.py`
passed 21 exact common-kernel quotient and affine-fiber identities and
21 rational LDL normalization sandwiches and inverse maps. It verifies
the new algebraic reductions, not the classical LP or rounding algorithms.

For nonnegative diagonal Hessians in the original box axes, the
[trace-allocation refinement](diagonal-psd-quadratic-linear-dimension-precision.md)
reduces the additive overhead further to `5r+1`. It uses a different
benchmark and does not contradict the Frobenius dimension-gap example.
