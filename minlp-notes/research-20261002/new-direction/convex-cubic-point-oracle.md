# Polynomial-time point approximation for convex cubics on boxes

Date: 2026-10-02. Status: passed a
[fresh full actual-file review](../reviews/convex-cubic-point-oracle-review.md)
and a [focused independent error-bound review](convex-cubic-point-hoffman-review.md).
This concerns convexity on the supplied box, not convexity on all of
Euclidean space. The [completed focused source comparison](../prior-art/convex-cubic-point-oracle-prior.md)
does not establish publication priority.
The separately reviewed [polytope addendum](convex-cubic-polytope-point-oracle.md)
extends both point-output conclusions to every bounded rational polytope.

## 1. Statement

Let `f` be an explicit rational polynomial of degree at most three,
convex on a nonempty bounded closed rational box `B`. Let `I` be its binary
input length, including the box. Convexity is a promise; this is not a
polynomial-time recognition claim. Write

```
S = argmin_(x in B) f(x).
```

There is a deterministic algorithm which, for every integer `q>=0`,
returns a feasible rational point `x_q` with

```
dist_2(x_q,S) <= 2^(-q)
```

in bit time polynomial in `I+q`, with an absolute polynomial exponent.
It can also return an arbitrary requested certified objective gap in
polynomial time. No strong-convexity modulus, unique optimizer, optimal
face, or selected optimizer is supplied or needed.

The proof gives a computable global bound on the unit box:

```
dist_2(x,S) <= Gamma [f(x)-min f]^(1/4)
       whenever 0 <= f(x)-min f <= 1,                    (1)
```

where `Gamma>=1` is rational with polynomial binary length and is
computed in polynomial time. The exponent `1/4` is sufficient for the
algorithm; no optimality claim is made for it.

Fixed coordinates are substituted first. An empty box is detected
directly. Positive-width coordinates are transformed affinely to
`[0,1]^n`; the transformed cubic has polynomial input length. If all
coordinates are fixed, return that point and take `Gamma=1`.
Sections 2--6 concern `n>=1`
and the unit box. Section 7 translates distances back to the original
box.

## 2. The Hessian has a fixed kernel

Set `c=(1/2,...,1/2)` and write `H(x)=nabla^2 f(x)`. The Hessian is
affine because `f` is cubic. Convexity gives `H(x)>=0` throughout the
box, including its boundary by continuity. Affinity gives

```
H(x)+H(1-x)=2H(c),
0 <= H(x) <= 2H(c).                                     (2)
```

Consequently `K=ker H(c)` equals `intersection_(x in box) ker H(x)`.
In one direction, (2) implies `H(x)u=0` for `u in K`; the reverse
direction follows by evaluating at `c`. Individual boundary Hessians
may have larger kernels, as for `f(t)=t^3` at `t=0`.

Let `g_c=nabla f(c)` and define `h(x)=f(x)-g_c'x`. Integrating the
Hessian on the segment from `c` to `x` shows

```
nabla h(x) in K^perp.                                   (3)
```

Thus `h` is constant on each feasible segment parallel to `K`, and
`f` is affine on such segments with slope `g_c`. All data defining
`K` and this slope are rational and have polynomial binary length.

If `H(c)=0`, equation (2) gives `H(x)=0` everywhere on the box and
`f` is affine there. Choosing each coordinate endpoint according to
its linear coefficient gives an exact rational optimizer. An error
constant in (1) is also explicit: if `g_c=0`, take `Gamma=1`;
otherwise clear its denominators with `D`, set `A=Dg_c'`, and apply
(10). With `C=max(1,max_i|D(g_c)_i|)`, the constant
`Gamma=(nC)^(n-1)D` works because the equality residual is `D E`
and `E<=E^(1/4)` for `E<=1`. Henceforth assume `H(c)` has positive
rank.

## 3. Cubic symmetry gives a quantitative gap transverse to the kernel

Choose a rational bound

```
M=max(1, max_i sum_j |H(c)_ij|).
```

Then `||H(c)||_2<=M` and `||H(x)||_2<=2M` by (2). Let `y` be any
optimizer, `x` any feasible point, `d=x-y`, and `E=f(x)-f(y)`. Put

```
a=d'H(y)d,    b=d'H(x)d,    u=a+b.
```

Both endpoint quadratic forms are nonnegative. Exact cubic Taylor
expansion and box first-order optimality at `y` give

```
E = nabla f(y)'d + (2a+b)/6 >= u/6.                     (4)
```

Let `T` denote the constant, fully symmetric third derivative tensor.
Since `H(x)-H(y)=T[d]`, symmetry yields the identity

```
d'H(c)d = a + (c-y)'(H(x)-H(y))d.                       (5)
```

This is the step that uses a cubic objective, not merely an arbitrary
matrix-valued affine function.

For a positive semidefinite matrix `Q`,
`||Qd||_2<=sqrt(||Q||_2 d'Qd)`. Applying this to both endpoints and
using `||c-y||_2<=sqrt n` gives

```
d'H(c)d <= u + 2 sqrt(n M u).                           (6)
```

Also `u<=4M||d||_2^2<=4Mn`, so `u<=2sqrt(nMu)`. Hence

```
d'H(c)d <= 4 sqrt(n M u).
```

Let `P` be orthogonal projection onto `K^perp`, and let `lambda` be
the smallest positive eigenvalue of `H(c)`. Combining the last inequality
with (4) gives

```
E >= [d'H(c)d]^2/(96 M n)
  >= lambda^2 ||Pd||_2^4/(96 M n).                       (7)
```

Neither `y` nor the projection `P` is computed by the algorithm. They
are used only in the proof of the effective error bound.

## 4. The optimizer set is one affine slice of the box

For any fixed optimizer `y`,

```
S = {u in [0,1]^n:
        H(c)(u-y)=0,  g_c'(u-y)=0}.                     (8)
```

Indeed, if `u` is also optimal, (7) gives `u-y in K`. Equation (3)
then gives `f(u)-f(y)=g_c'(u-y)=0`. Conversely those two equalities
make `h(u)=h(y)` and the affine part equal, hence make `u` optimal.
The right-hand side in (8) can be irrational; its coefficient matrix
is rational and known.

To control both equalities quantitatively, (2)--(3) give

```
||nabla h(w)||_2 <= 2M sqrt n
```

on the box. Integrating along `[y,x]` therefore yields

```
|g_c'd| <= E + 2M sqrt n ||Pd||_2.                       (9)
```

This accounts for possible nonconstant affine behavior along the common
Hessian kernel. Merely bounding `Pd` would not suffice for (1).

## 5. An explicit rational Hoffman bound

Here is the required special case, with its height bound included.
Let `A` be any integer matrix with `n` columns, put
`C=max(1,max_ij |A_ij|)`, and suppose

```
Z={w in [0,1]^n: Aw=b}
```

is nonempty. The vector `b` may be real or irrational. For every
`x in [0,1]^n`,

```
dist_2(x,Z) <= (nC)^(n-1) ||Ax-b||_2.                  (10)
```

For completeness, let `w` be the Euclidean projection of `x` onto `Z`.
Projection optimality represents `x-w` as a linear combination of an
independent subset of rows of `A` spanning its row space, plus a
nonnegative combination of active
outward box normals. Conic elimination modulo the row space of `A`
leaves a set of box normals independent modulo that row space. Let
`R` stack the resulting independent rows. It has at most `n` rows,
integer entries bounded by `C`, and

```
sigma_min(R) >= (nC)^(-(n-1)).
```

To see this bound, `RR'` is positive definite with integer determinant
at least one, and every eigenvalue is at most `(nC)^2`. Taking the
product of eigenvalues bounds the smallest one; taking its square root
gives the displayed estimate, also when there is only one row.

Writing `x-w=R't`, the independent representation satisfies
`||t||_2<=(nC)^(n-1)||x-w||_2`. In its inner product with `x-w`,
the active outward box normals contribute nonpositive terms because
`x` is in the box. The remaining equality-row contribution is bounded
by `||t||_2 ||Ax-b||_2`. Thus

```
||x-w||_2^2
 <= (nC)^(n-1)||x-w||_2 ||Ax-b||_2,
```

which proves (10). The zero-distance case is immediate. Redundant
rows and lower-dimensional slices cause no problem; a row basis is
used only in the proof. This is a quantitative instance of the classical
Hoffman error bound, not a new general error-bound theorem.

## 6. Fully computable polynomial-bit constants

Choose a positive integer `D` clearing all denominators of both `H(c)`
and `g_c`. The product of their positive denominators is one valid
polynomial-bit choice. Form the integer matrix

```
A=D [ H(c) ; g_c' ],    C=max(1,max_ij |A_ij|).
```

Its number of entries and every binary length are polynomial in the
input. If the rank of `H(c)` is `r>=1`, a positive principal minor of
order `r` is at least `D^(-r)`. Equivalently the product of its nonzero
eigenvalues, the sum of those principal minors, is at least `D^(-r)`.
All these eigenvalues are at most `M`. Thus the following rational
number is a valid lower bound for `lambda`:

```
lambda_0 = D^(-n) M^(-(n-1)).                           (11)
```

No algebraic eigenvalue approximation is needed. Define the deliberately
coarse rational quantities

```
R_0 = 96 M n / lambda_0^2,
Gamma = (nC)^(n-1) D [1+M(1+2n) R_0].                  (12)
```

They are at least one, have polynomial binary length, and can be computed
in polynomial time. From (7),

```
||Pd||_2 <= R_0 E^(1/4).
```

For `0<=E<=1`, equations (9) and `||H(c)d||_2<=M||Pd||_2` imply

```
||Ad||_2
 <= D [E+M(1+2n)||Pd||_2]
 <= D [1+M(1+2n)R_0] E^(1/4).
```

Applying (10) to the optimizer slice (8) proves (1) with precisely
the constant (12). This estimate is uniform over the unknown optimizer
and its possibly irrational affine-slice right-hand side.

## 7. Algorithm and output interpretation

For a unit-box distance request `epsilon=2^(-q)`, invoke certified
convex value optimization with target gap

```
eta=(epsilon/Gamma)^4 <= 1.                             (13)
```

The [reviewed arbitrary-dimensional convex value-oracle interface](core-only-noise-value-oracle.md#2-two-established-bit-interfaces)
returns a rational point in the box and a certified objective gap at
most `eta`, in polynomial bit work in the input and `log(1/eta)`.
It uses rational convex weak optimization and feasible repair; it does
not assume point-distance access. Its tangent lower certificates are
independently checkable given the convexity premise. Here

```
log(1/eta)=4q+4log Gamma=poly(I)+4q.
```

Equation (1) proves the requested point distance. To translate from a
normalized box back to the original one, put
`W=max(1,max_i (upper_i-lower_i))` and use normalized accuracy
`2^(-q)/W` in (13). The diagonal affine map increases Euclidean
distance by at most `W`, and `log W` has polynomial input length.
Rational coordinate output and the associated certificates therefore
have polynomial bit size as well.

This first algorithm returns distance to the optimizer set. It does not
by itself produce exact active-set labels or a polynomial-size expanded
algebraic optimum. Section 8 obtains a particular canonical point by a
separate regularization argument. The [cubic radical active-set construction](convex-active-set-radical-comparison.md)
already shows why accurate points should not be equated with exact
boundary labels.

The result contrasts with the reviewed
[degree-four PosSLP point-extraction implication](posslp-convex-point-extraction.md),
which concerns constant distance to some optimizer, not just a canonical
choice. The present proof uses two special cubic facts: Hessian affinity
gives the common center kernel, and symmetry of the constant third
derivative links endpoint Hessian actions to center curvature. These
steps do not extend to a general quartic Hessian. No complexity-class
separation or first-in-literature claim follows from this comparison.

## 8. A fixed minimum-norm optimizer is also polynomial-time computable

Let `p` be the unique minimum-Euclidean-norm point of the nonempty
compact convex optimizer set `S`, using the original coordinates of
the supplied box. The same input admits a deterministic Cauchy oracle
for `p`: a feasible rational point within `2^(-q)` of `p` is computable
in polynomial bit time in `I+q`.

The affine branch is immediate. Its optimal set fixes coordinates whose
linear coefficients are nonzero and leaves the others in their original
intervals. Project zero onto that box face to obtain `p` exactly.
For the nonaffine branch, let `Gamma_B>=1` be `W Gamma` from Section 7,
so (1) holds in original coordinates with `Gamma_B`. Choose a rational
`R>=1` bounding `||x||_2` on the original box, for instance
`R=max(1,sum_i max(|lower_i|,|upper_i|))`.

For `epsilon=2^(-q)`, put

```
tau = epsilon^6/(1024 R^4 Gamma_B^4),
eta = tau epsilon^2/4.                                  (14)
```

Let `x_tau` minimize `f(x)+tau||x||_2^2` on the original box. It is
unique. Comparison with `p` gives

```
f(x_tau)-f* <= tau (||p||_2^2-||x_tau||_2^2),
||x_tau||_2 <= ||p||_2 <= R.
```

In particular the unregularized objective gap is at most `tau R^2<=1`,
so the original error bound applies. If `s` is a nearest point of `S`
and `e=||s-x_tau||_2`, then

```
e^4/Gamma_B^4
 <= f(x_tau)-f*
 <= tau (||s||_2^2-||x_tau||_2^2)
 <= 2R tau e.
```

Thus `e<=(2R tau Gamma_B^4)^(1/3)`. Projection optimality of `p`
onto `S`, together with `||x_tau||<=||p||`, also gives

```
||x_tau-p||_2^2
 <= 2 p'(p-x_tau)
 <= 2 p'(s-x_tau)
 <= 2R e.
```

With (14), `e<=epsilon^2/(8R)`, hence
`||x_tau-p||_2<=epsilon/2`. This is the fixed-fiber regularization
argument from the [earlier conditional rate](canonical-convex-fiber-regularization.md#2-tikhonov-convergence-at-a-fixed-core),
now with an effective polynomial-bit error constant.

Use the same convex value oracle to find a feasible rational point
`x_hat` with regularized objective gap at most `eta`. The objective
is strongly convex with modulus `2tau`, so constrained first-order
optimality implies

```
||x_hat-x_tau||_2 <= sqrt(eta/tau)=epsilon/2.
```

The triangle inequality proves `||x_hat-p||_2<=epsilon`. Both
`log(1/tau)` and `log(1/eta)` are `poly(I)+O(q)`. The regularized
objective is still an explicit rational cubic, and the value solver
has polynomial cost in these bit lengths. No eigenvalue lower bound
of the regularized Hessian is used to define the original error
constant.

On a nonunit box the penalty here is deliberately the original norm
`||x||^2`; replacing it by the norm of normalized coordinates would
select a different canonical optimizer. This stronger Cauchy output
still does not decide exact active labels or provide small expanded
algebraic coordinates.

## Verification status

The base derivation was independently reached by the parent researcher.
The focused review passed the actual optimizer-set statement, rational
Hoffman bound, and explicit height constants. The fresh full review
passed the complete saved proof, including a separate actual-file check
of the minimum-norm corollary. Neither reviewer duplicated the diagnostic
below.

The author-side diagnostic owner ran
`python3 -B research-20261002/new-direction/check_convex_cubic_point_oracle.py`.
The [exact checker](check_convex_cubic_point_oracle.py) passed eight
fixtures: 1,050 cubic-symmetry and endpoint-gap checks, 465 actual
fourth-root distance bounds, 546 optimizer-slice equivalences, 24
precision-scale checks, 162 irrational-right-hand-side Hoffman bounds
(including 20 boundary projections), and 216 nonunit/fixed-coordinate
normalization checks. Its small affine-kernel slope has 101 coefficient
bits; the resulting explicit constants have 1,220 and 960 bits in two
fixtures. The checks include counterexamples to omitting the gradient
equality, treating a nonintegrable affine matrix field as a cubic
Hessian, and minimizing the normalized-coordinate norm instead of the
original norm. The optimizer sets are explicit fixture data; this is not an
implementation of generic convex optimization or a convexity recognizer.
The note author inspected the checker rather than rerunning that same
diagnostic. The focused source comparison distinguishes this effective
constant from qualitative convex-polynomial error bounds and keeps
convexity recognition separate. Yang 2009 remains abstract-only in that
audit, and equivalent prior results have not been excluded. No index
edits or project-wide checks are made.
