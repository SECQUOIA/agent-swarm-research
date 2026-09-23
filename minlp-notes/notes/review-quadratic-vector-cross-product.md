# Independent audit: quadratic-vector covariance certificate

Date: 2026-09-05.
Reviewer: independent agent `graph_precision_second_review`.
Source: `results/quadratic-system-covariance-lower-bounds.md`.

## Verdict

The sum-of-squares certificate, finite lower constant, arbitrary convex
integer-lift extension, general compact binary upper construction, and
cross-product counterexample all pass independent mathematical review.
No substantive correction was found. The full draft was read, including
the residual-square upper formulation and explicit cross-product signs.
This is a proof audit, not a publication-priority assessment.

The exact condition `sum_j H_j^2=cI`, with `c>0`, is important. Positive
definiteness of that sum alone would not imply the result; an explicit
counterexample to that possible weakening is recorded below.

## Moment identity and constants

Let a positive-volume compact contact set be translated to its centroid,
and let `X,Y` be independent uniform vectors on that translated set.
Their covariance `Sigma` is positive definite: zero variance in a
nonzero direction would concentrate a positive-volume uniform law on
a hyperplane. Compactness supplies all required fourth moments.

For one symmetric Hessian, write `A=X^T H X`, `B=Y^T H Y`, and
`C=X^T H Y`. Since `q(X-Y)=(A+B-2C)/2`, direct expansion gives

```
E[q(X-Y)^2]
 = (1/2) E[A^2] + (1/2)(E[A])^2 + E[C^2].
```

The terms `E[AC]` and `E[BC]` vanish by independence and centering,
and `E[AB]=(E[A])^2`. Finally,
`E[C^2]=tr(H Sigma H Sigma)`. Thus the factor in the draft is correct
for `q(v)=v^T H v/2`; no hidden factor two or four is lost.

The midpoint deviation of a quadratic coordinate is `q(s-t)/4`, so
componentwise error `epsilon` gives pairwise bound `delta_j=4 epsilon`.
Consequently summing the moment inequalities gives exactly

```
sum_j tr(H_j Sigma H_j Sigma) <= 16m epsilon^2.
```

Affine terms in the quadratic outputs cancel from every midpoint
identity and have no effect on this calculation.

## Determinant inequality

In an orthonormal eigenbasis of `Sigma`, define
`W_ab=sum_j (U^T H_j U)_ab^2`. Symmetry of every Hessian makes `W`
symmetric and nonnegative. The certificate survives orthogonal
conjugation, so each row sum and each column sum of `W` is exactly `c`.
Its total sum is `cn`, which is positive.

Apply weighted arithmetic-geometric mean to the positive numbers
`lambda_a lambda_b` with weights `W_ab/(cn)`, omitting zero weights.
The total exponent of each `lambda_a` is its row contribution plus its
column contribution, namely `2/n`. This proves

```
sum_j tr(H_j Sigma H_j Sigma)
 >= cn (det Sigma)^(2/n).
```

Diagonal weights are handled correctly: the associated number is
`lambda_a^2`, so that coordinate contributes twice, just as in the
row-plus-column count. Off-diagonal weights occur in both ordered
positions and are already included in total weight `cn`.

Combining with the moment bound gives
`det Sigma <= [16m epsilon^2/(cn)]^(n/2)`. Taking its square root
therefore introduces exponent `n/4`, which produces the required
`epsilon^(n/2)` volume rate.

## Volume bound and arbitrary lifted formulations

The volume-covariance inequality used in the draft is correct and has
the displayed constant `omega_n(n+2)^(n/2)`. After whitening the centered
set, covariance is identity and the integral of squared norm is its
volume times `n`. The centered ball of equal volume minimizes that
integral, giving radius at most `sqrt(n+2)`. Undoing the whitening
transformation multiplies volume by `sqrt(det Sigma)`.

Same-parity integer lifts have an integral midpoint in the original
convex lifting set. Its input stays in the box, so the error hypothesis
applies. Taking each parity support's closure in the compact box
preserves every pairwise quadratic inequality by continuity. Those
closures still cover the box, regardless of whether the lifting set,
projection, or original support is closed or measurable.

Zero-volume classes contribute nothing. Applying the covariance bound
to the remaining classes and summing over at most `2^p` classes gives

```
V <= 2^p omega_n(n+2)^(n/2)
     [16m epsilon^2/(cn)]^(n/4).
```

Raising to `2/n` and rearranging gives exactly

```
epsilon >= sqrt(cn/m) V^(2/n)
           / [4(n+2) omega_n^(2/n)] * 2^(-2p/n).
```

The proof permits arbitrary finite-dimensional continuous convex lifts
and unrestricted integer ranges. It needs graph containment over a
full-dimensional box and error on every admitted point in that box;
a lower-dimensional zero set or only selected feasible points would
not suffice.

## Compact upper construction

After affine box normalization, each output is a finite linear
combination of monomials and an affine term. Choose a positive `C`
bounding the sum of absolute quadratic coefficients separately for
every output. Shared depth-`L` coordinate expansions cover all of
`[0,1]^n`, including 1 by the all-ones prefix plus the full residual.

For a distinct-index product, the identity
`x_i x_l=A_i x_l+r_i A_l+r_i r_l` is exact. Each prefix term is a sum
of binary-times-bounded-continuous products and therefore has an exact
linear description at integral binary values. Residual McCormick
error is at most `h^2/4`.

The square identity is also correct:
`x_i^2=A_i x_i+r_i A_i+r_i^2` expands to
`A_i^2+2A_i r_i+r_i^2`. The residual-square triangle

```
max(0,2h r_i-h^2) <= t <= h r_i
```

contains `r_i^2` for `0<=r_i<=h`. With `u=r_i/h`, its lower error is
`u^2` when `u<=1/2` and `(1-u)^2` when `u>=1/2`, both at most `1/4`.
Its upper error is `u-u^2<=1/4`. Thus its two-sided bound is exactly
what the proof needs. It need not be the tighter sawtooth lower envelope.

Assembling signed coefficient sums loses at most `C h^2/4` per output.
The chosen ceiling for `L` makes this no larger than epsilon, with the
`L=0` case covering `epsilon>=C/4`. All exact output graph points lift
simultaneously using the same input expansions and exact residual
monomials. There are exactly `nL` binary variables. Counting at most
quadratically many monomials gives the stated linear-in-`L` formulation
size for a fixed system and box.

This upper bound applies even without the certificate. The certificate
proves the matching `n/2` leading lower coefficient when it holds.

## Cross-product matrices and scalar rank

The draft uses

```
A(a) = [[0,a_3,-a_2],[-a_3,0,a_1],[a_2,-a_1,0]],
H(a) = [[0,A(a)],[-A(a),0]].
```

These signs are consistent with
`x^T A(a)y=a dot (x cross y)`. The Hessian block matrix is symmetric
because `A(a)` is skew-symmetric. The identity
`A(a)^T A(a)=||a||^2 I-aa^T` proves rank exactly two whenever `a!=0`.
The kernel of `H(a)` consists of the two independent copies of the
one-dimensional kernel of `A(a)`, so its rank is exactly four.
There is therefore no nonsingular scalar Hessian in the pencil.

For the three coordinate Hessians, direct multiplication gives
`sum_j H_j^2=2 I_6`. Substituting `n=6,m=3,c=2,V=1` into the finite
bound gives

```
epsilon >= 2^(-p/3)/(16 omega_6^(1/3)),
p >= 3log2(1/epsilon)-log2(4096 omega_6),
omega_6=pi^3/6.
```

Both constants in the draft are correct. Six shared half-precision
input expansions give the matching upper coefficient three. A fixed
scalar output has rank four and coefficient two, so scalar rank alone
cannot characterize simultaneous approximation.

As an independent exact check, I constructed the Hessians directly from
the three polynomial coordinates in symbolic arithmetic. The sum of
squares was exactly `2I_6`; the symbolic pencil determinant was zero,
and its generic rank was four. Coordinate pencils and the mixed pencil
with coefficients `(1,-2,3)` also had exact rank four. These checks are
independent of the author's verification script, but the analytic rank
identity above proves the statement for every nonzero coefficient vector.

## Useful limitations and an immediate extension

Do not weaken the certificate to positive definiteness of
`sum_j H_j^2`. The map

```
G(x_1,x_2,x_3)=(x_1 x_2, x_2 x_3)
```

has Hessian-square sum `diag(1,2,1)`, which is positive definite.
Nevertheless, discretizing only the shared coordinate `x_2` gives
integer precision coefficient one, and its scalar bilinear restriction
gives a matching lower coefficient. The putative full-dimension
coefficient `3/2` would be false. Exact equal marginals, not merely
positive marginal lower bounds, are what make the weighted determinant
inequality work.

For `k` independent cross-product blocks, every output Hessian is
supported on one six-coordinate block. The full family still satisfies
`sum_j H_j^2=2I_(6k)`. The theorem gives coefficient `3k`. Every scalar
Hessian is block diagonal with each nonzero block of rank four, so its
maximum rank is `4k` and the best scalar-rank coefficient is `2k`.
Thus the additive deficit of the scalar-rank prediction is unbounded
as `k` grows, while the factor `3/2` persists. This is an immediate
corollary of the reviewed argument, not a separate unverified mechanism.
