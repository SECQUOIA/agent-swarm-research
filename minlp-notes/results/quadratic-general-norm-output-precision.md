# Quadratic graph precision for general symmetric error bodies

Date: 2026-09-05. Status: independently reviewed theorem; proof and
source audits linked below.

The reviewed polynomial construction extends to any bounded symmetric
convex output-error body with a polynomial-time separation oracle and
known inner and outer radii. The number of outputs does not enter the
additive integer-count error. The key is to round the error body only
on the image of the quadratic coefficients, whose dimension is at most
`n(n+1)/2`. Ellipsoid rounding is a classical ingredient.

## Statement and oracle assumptions

Let `f:R^n -> R^m` have rational quadratic coefficients, with domain
`[0,1]^n`. Let `K` be a compact convex body in `R^m`, symmetric about
zero, with rational known radii

```
0<r_0<=R_0,       r_0 B_2^m subset K subset R_0 B_2^m.
```

Suppose a rational strong separation oracle for `K` runs in time
polynomial in its query encoding length and the encoding of `K`. Here
strong separation returns membership or a rational separating linear
inequality. Its output encoding length is included in that polynomial
bound. A valid approximation contains every point of the exact graph
and permits only errors `w-f(x) in K`.

There is a deterministic polynomial-time algorithm producing a rational
MILP with

```
p_out <= p_conv(f,K)+C n log2(n+1),                      (1)
```

for a universal constant `C`. As before, `p_conv` permits arbitrary
convex lifts, any number of continuous variables and constraints, and
unbounded general integer variables. Running time is polynomial in
the quadratic input, the oracle encoding, `n,m`, and the binary lengths
of `r_0,R_0`. This is an existence and encoding result, without a claim
of practical running time.

More generally, the proof needs only a well-bounded strong separation
oracle directly for the effective error body defined below. The
strong ambient oracle is one sufficient input model with a simple
exact pullback.

## Restricting the outputs to their nonlinear image costs no integers

Write

```
f(x)=a(x)+C u(x),
```

where `a` is rational affine, `u` lists the `s=n(n+1)/2` quadratic
monomials, and `C` is their rational `m` by `s` coefficient matrix.
Let `d=rank C`. If `d=0`, the graph is affine and has an exact LP
formulation, so (1) holds with zero integers.

For `d>=1`, choose a rational full-column-rank basis `T` for the image
of `C`, and solve `C=T B` rationally. Then

```
g(x)=B u(x),       f(x)=a(x)+T g(x),
K_eff={z in R^d: Tz in K}.
```

All matrices have polynomial encoding length by rational elimination.
For both the arbitrary-convex-lift and binary-LP minima,

```
p(f,K)=p(g,K_eff).                                      (2)
```

One direction follows by adjoining the affine equation
`w=a(x)+Tz` to a formulation for `(g,K_eff)`. For the other, start
with any formulation for `(f,K)`, introduce `z`, and impose that same
affine equation. This retains every exact graph point, and any admitted
point has `T(z-g(x)) in K`, hence `z-g(x) in K_eff`. No integer variables
are added. This argument also covers original formulations whose
admitted errors did not lie in the image of `T`.

The body `K_eff` is bounded, full-dimensional, convex and symmetric.
Take rational positive bounds `c_T>=||T||_2` and
`c_L>=||(T^T T)^(-1)T^T||_2`, for example one plus the sums of absolute
entries. Then

```
(r_0/c_T) B_2^d subset K_eff subset (R_0 c_L) B_2^d.       (3)
```

The rational strong separation oracle pulls back exactly: query `Tz`
and replace a violated inequality `h^T e<=b` by `h^T Tz<=b`.
Because `Tz` violates it and `0 in K`, the pulled-back normal is
nonzero. The new radii and oracle have polynomial encoding complexity.

## Classical rounding gives a rational ellipsoid in dimension d

Use the established polynomial oracle rounding theorem of Grötschel,
Lovász and Schrijver, *Geometric Algorithms and Combinatorial
Optimization*, Theorem 4.6.1. A directly accessible primary research
statement is Dadush, Peikert and Vempala,
[*Enumerative Lattice Algorithms in Any Norm via M-Ellipsoid Coverings*](https://sites.cc.gatech.edu/fac/cpeikert/pubs/svp-anynorm.pdf),
Theorem B.5, which explicitly outputs a rational positive definite
matrix `A` and an ellipsoid

```
E={z:z^T A z<=1}
```

with `K_eff subset t+E`. For a chosen positive volume threshold `eta`,
it gives either `vol(E)<=eta` or `t+E/beta subset K_eff`, where
`beta=(d+1)sqrt(d)`. The theorem is deterministic and polynomial in
the input encoding and logarithmic accuracy. It is a variant of the
classical GLS rounding algorithm, not a new rounding result here.

Put `r=r_0/c_T` and choose the rational threshold
`eta=min{1/2,(r/d)^d/2}`. Since `[-r/d,r/d]^d subset r B_2^d`,

```
vol(K_eff)>eta.
```

Thus the small-volume alternative is impossible. Symmetry removes
the translation from both inclusions. The inner inclusion and its
negative imply `E/beta subset K_eff` by taking averages. If
`x in K_eff`, the outer inclusion applied to `x` and `-x` gives
`x-t in E` and `x+t in E`; their average gives `x in E`. Therefore

```
E_0 subset K_eff subset beta E_0,
E_0={z:z^T W z<=1},       W=d(d+1)^2 A.                 (4)
```

The matrix `W` is rational with polynomial encoding length. Neither
the possibly real center `t` nor an irrational square root of `A`
appears in the output or subsequent computation. When `d=1`, the
one-dimensional rounding can equivalently be obtained by rational
bisection with a constant factor; the stated rounding theorem also
covers this case.

## Transfer of integer complexity through a norm approximation

The following argument applies whenever a rational ellipsoid satisfies
`E_0 subset K_eff subset alpha E_0` with `alpha>=1`. Let `G_j` be the
Hessians of `g_j`, and define

```
E_W(P)=sum_jk W_jk tr(G_j P G_k P),
D(t)=max{det P: 0<=P<=I, E_W(P)<=t^2},
Phi(t)=-(1/2)log2 D(t).
```

The reviewed [ellipsoidal covariance law](../results/quadratic-ellipsoidal-output-precision.md)
gives

```
Phi(alpha)-A_n <= p_conv(g,alpha E_0)
                <= p_conv(g,K_eff)=p_conv(f,K).          (5)
```

For every covariance feasible for `D(alpha)`, its rescaling `P/alpha`
is feasible for `D(1)`. Therefore

```
D(1)>=D(alpha)/alpha^n,
Phi(1)<=Phi(alpha)+(n/2)log2 alpha.                      (6)
```

Run the reviewed [polynomial rational construction](../results/quadratic-weighted-precision-polynomial-construction.md)
with the single positive definite output budget `W` and tolerance one.
Its explicit construction bound is `p_out<=Phi(1)+B_n+O(n)`. Every
admitted error lies in `E_0 subset K_eff`, so the affine embedding
produces a valid rational MILP for `(f,K)`. Combining (5)--(6) gives

```
p_out <= p_conv(f,K)+A_n+B_n+O(n)+(n/2)log2 alpha.       (7)
```

With `alpha=beta=(d+1)sqrt(d)` and `d<=n(n+1)/2`, all terms after
`p_conv` are `O(n log(n+1))`, proving (1). No factor depending on `m`
remains in the additive guarantee. The input size and running time
still depend on `m` and on the description of the error oracle.

This proof separates the only loss from classical norm rounding:
a factor `alpha` in output error costs at most `(n/2)log2 alpha`
in the covariance benchmark. The smaller effective dimension is what
makes a general oracle norm compatible with the original additive
integer-count guarantee.

## Scope and novelty boundary

The result covers arbitrary well-described norm balls, including
polyhedral norms given by separation, with anisotropy represented in
the radius encoding rather than the integer-count overhead. It can
also use an oracle directly for a bounded section in the nonlinear
image, even if some other output directions are unrestricted.

It does not assert a new ellipsoid-rounding algorithm, a practical
implementation, or a guarantee for arbitrary error sets without known
inner and outer radii. Convexity and symmetry are explicit assumptions.
The proposed new conclusion is the dimension-only additive guarantee
against all convex mixed-integer lifts for quadratic graph approximation.
Two independent proof audits passed: the [first audit](../notes/review-quadratic-general-norm-output-precision.md)
and [second audit](../notes/review-quadratic-general-norm-output-precision-second.md).
The [source and novelty assessment](../notes/quadratic-general-norm-precision-novelty.md)
checked the exact rational strong-oracle rounding import and found no
matching formulation theorem in its bounded search. This does not
establish priority beyond the checked literature.

The reproducible checker `code/quadratic_rank/check_effective_output_image.py`
passed 28 exact rational cases covering image decompositions, Hessian
reconstruction, covariance-energy preservation, and shared-error budgets.
This checks the new algebraic reduction; it does not implement the
classical ellipsoid-rounding oracle.

For the `l1` output norm, a [specialized semidefinite covariance law](quadratic-l1-output-precision.md)
uses the classical PSD Grothendieck bound to retain a constant-factor
surrogate and explicit finite constants.

The [nonlinear input-rank refinement](quadratic-nonlinear-input-rank-precision.md)
replaces the additive dimension term by `O(r log(r+1))`, where `r` is
the exact rank of the stacked Hessians. Affine input directions remain
in the continuous lift and do not contribute to this overhead.
