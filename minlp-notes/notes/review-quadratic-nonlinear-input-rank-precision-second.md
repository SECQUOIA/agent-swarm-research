# Second audit: common nonlinear input rank and integer precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed draft: `notes/quadratic-nonlinear-input-rank-precision.md`.

## Verdict

**PASS after scope clarifications.** The common-kernel quotient preserves
both formulation minima exactly. The rational zonotope normalization,
volume-adjusted covariance lower bound, effective-output reduction, and
polynomial rational construction then give the stated additive
`O(r log(r+1))` guarantee.

Two clarifications were requested and applied: impose the original cube
before projecting an arbitrary formulation, and state the modified lower
bound for compact convex domains. The actual domain is always a convex
zonotope, so neither adjustment changes the theorem. The revised note
also explicitly distinguishes the reduced output map and its covariance
benchmark, resolving a possible notation ambiguity.

This review does not establish novelty. Linear quotient maps, rational
LP separation, LDL factorization, and classical ellipsoid rounding are
established tools. The rank here is the ordinary rank of the stacked
Hessians, not their noncommutative rank or merely the rank of one scalar
combination.

## Exact quadratic quotient

Let `U` be a full-row-rank rational basis for all Hessian rows. Its
kernel is exactly their common kernel. The matrix
`F=U^T(UU^T)^(-1)` satisfies `UF=I`; `FU` is the symmetric
orthogonal projection onto the row space of `U`. Symmetry of each
Hessian puts its column space in that same subspace. Therefore

```
H_j=(FU)^T H_j(FU)=U^T(F^T H_j F)U.
```

All stated matrices are obtained by polynomial-bit rational elimination.
No numerical rank tolerance is involved.

With `z=U(x-c)`, the quadratic term
`(1/2)z^T G_j z` equals
`(1/2)(x-c)^T H_j(x-c)`. Subtracting it from `f_j(x)` leaves
exactly the affine expression

```
a_j(x)=(a_j+H_j c)^T x+b_j-(1/2)c^T H_j c,
```

where the original vector coefficient on the right is understood.
Thus affine dependence along a quotient fiber is retained rather than
discarded.

The forward formulation map keeps the original integer coordinates
and applies only the visible affine transformation
`(x,w)->(U(x-c),w-a(x))`. Restricting to the original cube first
makes every projected input belong to `Z`. Every exact graph point
over `Z` has an original cube preimage, and every admitted error
is exactly the original error vector. Affine images of convex sets
remain convex, and binary LP lifts retain a linear description by
keeping the original continuous variables.

Conversely, impose the quotient equation, the original cube, and the
affine output restoration. These are linear constraints and add no
integers. Every original exact graph point remains admitted, and every
admitted error is again unchanged. This proves equality of both integer
minima, even when the affine output varies along a fiber.

## Exact domain oracle and radii

The reduced domain is a full-dimensional compact convex centrally
symmetric zonotope because `U` has full row rank. Its LP membership
test is exact. For an outside rational query, the proposed separator LP
is feasible: strict separation of the compact zonotope provides a
positive support gap, which can be rescaled to at least one. Its
constraints imply

```
h^T y <= (1/2)sum_i |(U^T h)_i|
      <= (1/2)sum_i v_i < h^T z
```

for every `y in Z`. Thus the returned inequality is a valid strict
separator, with nonzero normal. Standard exact rational LP supplies
a polynomial-bit solution and polynomial-time decision, including
boundary membership. No zonotope vertex or facet enumeration is used.

For the inner radius, `||U_J^(-1)||_2` is bounded by the sum of its
absolute entries. An input vector of Euclidean norm at most
`1/(2c_inv)` therefore has inverse coordinates of magnitude at most
one half. It belongs to the image of the selected column cube.
For the outer radius,

```
||U t||_2 <= (1/2)sum_i ||U_:i||_2
          <= (1/2)sum_ki |U_ki| < R_0.
```

Both radii are positive rationals of polynomial bit length, as are
the inverse and chosen submatrix.

I independently checked the imported rounding statement: Dadush,
Peikert and Vempala Theorem B.5 explicitly returns a rational positive
definite ellipsoid matrix from a strong separation oracle, with either
a small outer volume or the displayed factor `(r+1)sqrt(r)` inner
inclusion. A known inner ball excludes the small-volume case using
a rational volume threshold of polynomial encoding. Symmetry removes
the translation from both inclusions by averaging each inclusion with
its negative. No center needs to be rationally represented.
[Primary rounding theorem](https://sites.cc.gatech.edu/fac/cpeikert/pubs/svp-anynorm.pdf).

## Rational normalization and volume

The positive definite matrix admits rational LDL factorization without
pivot failure. Entries and pivots are ratios of rational minors, with
polynomial encoding length. Selecting each dyadic `b_i` by exact
squared comparisons gives `D_ii<=b_i^2<=4D_ii`. Congruence by
`L` yields `A<=R^T R<=4A`.

The two ball inclusions have the stated directions. If
`||y||<=1/beta`, then `z=R^(-1)y` satisfies
`z^T A z<=||y||^2<=1/beta^2`, hence lies in `Z`.
Conversely, `z in Z` implies `z^T A z<=1`, so
`||Rz||^2<=4`. Thus scaling by one quarter and shifting to the
cube center puts the entire domain inside `[0,1]^r`.

The inner ball then has radius `1/(4beta)`. The centered axis-aligned
cube of side `1/(2beta sqrt(r))=1/(2r(r+1))` fits inside it.
Its volume proves the stated lower logarithmic bound, including
`r=1`. This bound depends only on reduced dimension, although the
normalizing coefficients may depend on the full input conditioning.

The normalized domain still has an exact polynomial-size rational
linear lift through the original cube variables. There is no need
to describe its potentially many facets or to replace it by the
containing cube in the final formulation. Inverses, shifts, and
transformed quadratic coefficients retain polynomial bit length.

## Domain-adjusted covariance lower bound

On a compact convex domain inside the reduced unit cube, parity
midpoints stay in the domain, so the quadratic contact and covariance
inequalities of the reviewed ellipsoidal theorem remain valid.
Every parity support lies inside the same containing cube, retaining
the same covariance cap. Closure causes no problem because the
domain is closed and the midpoint inequality is continuous.

The individual support-volume bound is unchanged. Summing now covers
`vol(Omega)` rather than one, giving exactly

```
p_conv >=Phi(t)-A_r+log2 vol(Omega).
```

The sign of the volume term is correct: shrinking the domain weakens
the lower bound. Convexity in this statement is needed to use the
original domain's error requirement at every admitted midpoint; the
revised note explicitly includes it.

## Output reduction and final count

After input normalization, write the output as an affine map plus
`T q_bar`, with `T` injective on its coefficient-image coordinates.
Restricting output errors to that image by affine equations preserves
the minimum integer count, as in the reviewed general-norm theorem.
The reduced output dimension is at most `r(r+1)/2`, regardless of
the original output count or affine dependence on the unreduced inputs.

The pullback body is bounded, full-dimensional, convex and symmetric.
Its rational strong oracle and inner/outer radii follow from the
rational injective map and its rational left inverse. Thus the
second classical rounding has factor
`alpha=(d+1)sqrt(d)` and a rational ellipsoid. The revised draft
correctly forms `Phi` from `q_bar` and this ellipsoid's quadratic
form, rather than mixing original and reduced output coordinates.

Containment of the pulled-back error body in `alpha E_0` makes
the larger ellipsoid's integer minimum no larger. The modified lower
bound therefore implies

```
Phi(alpha)<=p_conv(q,Omega,K)+A_r-log2 vol(Omega).
```

Rescaling a covariance by `1/alpha` changes the homogeneous energy
by `1/alpha^2` and determinant by `1/alpha^r`, while preserving
the matrix cap. Hence
`Phi(1)<=Phi(alpha)+(r/2)log2 alpha`, with the correct sign.

Constructing the reviewed ellipsoidal MILP on the full containing
cube is legitimate: a quadratic polynomial is defined there and the
construction controls its error on that entire cube. Restricting
afterwards to the exact zonotope lift only removes points. Restoring
both affine output maps and the original cube variables adds no
integer coordinates and preserves graph containment and the original
error body.

The explicit count is thus the original integer minimum plus
`A_r+B_r+O(r)`, the domain-volume penalty, and the output-rounding
penalty. Because `d<=r(r+1)/2`, every penalty is
`O(r log(r+1))` with a universal constant. There is no hidden factor
of the original input or output dimension in this additive count.
The running time and continuous description size still depend on
those dimensions and their full encoding.

If `r=0`, every Hessian is zero and the exact affine graph is an LP.
If `r>0`, invertibility of the input coordinate changes prevents
all reduced quadratic coefficients from vanishing, so the effective
output rank is positive and the rounding step is well-defined.

## Reviewed hardness corollary

The already reviewed approximation-hardness theorem also excludes a
uniform additive guarantee `O(r^(1-delta))`, or a multiplicative guarantee
of that order under the positive-optimum promise, for any fixed
`0<delta<1`, unless `P=NP`. Indeed `r<=n` and the exponent is positive,
so either input-rank guarantee would imply the corresponding forbidden
ambient-dimension guarantee. The reduction's unit componentwise error
body is included in this theorem's oracle model. The multiplicative
promise entails `r>=1`, since an affine graph needs no integers.
This corollary is a direct transfer of the existing hardness result,
not a new reduction.
