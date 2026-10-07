# Convex cubic point approximation on bounded rational polytopes

Date: 2026-10-02. Status: passed a
[fresh full actual-file review](../reviews/convex-cubic-polytope-point-review.md)
and a [focused preprocessing review](convex-cubic-polytope-preprocessing-review.md).
It extends the reviewed [box theorem](convex-cubic-point-oracle.md)
to arbitrary bounded rational polytopes, including lower-dimensional
ones. The [completed focused source comparison](../prior-art/convex-cubic-point-oracle-prior.md)
leaves publication priority unresolved.

## 1. Statement

Let

```
P={x in R^n: Cx<=b}
```

be a nonempty bounded rational polytope, and let `f` be an explicit
rational polynomial of degree at most three, promised convex on `P`.
The binary input length `I` includes the polynomial and the linear
description. For every `q>=0`, a deterministic algorithm returns a
feasible rational point within Euclidean distance `2^(-q)` of the
optimizer set in bit time polynomial in `I+q`.

It can instead approximate the unique minimum-Euclidean-norm optimizer
to that accuracy, also in polynomial bit time. The norm and distance
refer to the original coordinates. No unique optimizer, active face,
relative-interiority of the optimizer, or strong-convexity modulus is
assumed. Convexity recognition is not included.

The proof constructs a rational constant `Gamma_P>=1`, of polynomial
binary length, such that

```
dist_2(x,S) <= Gamma_P [f(x)-f*]^(1/4)
   for x in P with 0<=f(x)-f*<=1,                       (1)
S=argmin_P f.
```

Only classical rational linear programming and convex weak value
optimization are used algorithmically. The unknown optimizer and its
possibly irrational affine-slice right-hand side occur only in the
analysis.

## 2. Actual affine-hull reduction and a rational interior ball

Use rational linear programming to test feasibility. If boundedness is
not accepted as a promise, first solve both coordinate extrema for every
original coordinate and reject an unbounded one. For each input row
`C_i x<=b_i`, maximize its slack `b_i-C_i x` over `P`. The row is
universally tight precisely when this maximum is zero. This is not the
test that the row merely attains equality somewhere.

Let `Ex=e` be an independent subset of these universally tight rows.
Its affine solution space is exactly `aff(P)`. Indeed, for every
non-universally-tight row choose a feasible point with positive slack.
Averaging these finitely
many points gives one point strictly satisfying every non-universal row.
It has a relative neighborhood in `{Ex=e}` satisfying all such rows;
the universal rows remain equalities. Thus that affine space cannot
exceed `aff(P)`. The case with no remaining rows is immediate.

Rational elimination gives

```
x=x_0+V u,
```

where the columns of `V` are a rational basis of `ker E`. Choose the
free original coordinates as `u`, so `V` contains an identity submatrix.
The entries of `x_0,V` have polynomial binary length. Let `s` be the
number of columns. If `s=0`, return the sole feasible point and take
`Gamma_P=1`. Otherwise
the transformed polytope

```
P'={u in R^s: a_i'u<=d_i for all i}
```

is bounded and full-dimensional. Its description, and the pulled-back
cubic `phi(u)=f(x_0+Vu)`, have polynomial encoding length. This uses the
fixed degree three; explicit affine substitution creates at most
polynomially many monomials. Only after this reduction do we use a
positive semidefinite Hessian: convexity on the original lower-dimensional
set need not imply ambient positive semidefiniteness there.

Remove transformed zero rows, rejecting a negative right-hand side.
For the nonzero rows put `w_i=||a_i||_1` and solve the rational LP

```
maximize rho
subject to a_i'c+rho w_i<=d_i for all i,
           0<=rho<=1.                                   (2)
```

Full dimension gives a strictly positive optimum. Boundedness of `P'`
makes the feasible set in `(c,rho)` compact, so a rational optimal
solution of polynomial binary length exists and can be computed. Since
`||a_i||_2<=w_i`, its Euclidean ball satisfies

```
B_2(c,rho) subset P',    rho>0.                         (3)
```

Coordinate LPs compute `l_j=min_(P') u_j` and `r_j=max_(P') u_j`.
Set

```
R=max(1, sum_j max(|l_j-c_j|,|r_j-c_j|)).                (4)
```

Then `||u-c||_2<=R` on `P'`, and its diameter is at most `2R`.
All these rational data have polynomial binary length. The LPs can
also reject infeasibility or unboundedness if those input promises are
not assumed. No numerical interior-point tolerance is used to decide
an exact affine hull or positive radius.

## 3. Reflection replaces the box midpoint identity

Let `H(u)=nabla^2 phi(u)` and `H_c=H(c)`. It is an affine matrix
function, positive semidefinite on `P'`. For every `u in P'`, the point

```
u'=c-(rho/R)(u-c)
```

belongs to the interior ball (3). Affinity expresses `H_c` as a positive
convex combination of `H(u)` and `H(u')`. Consequently

```
0<=H(u)<=beta H_c,    beta=1+R/rho.                     (5)
```

In particular

```
K=ker H_c=intersection_(u in P') ker H(u).
```

Individual boundary Hessians may have larger kernels. If `H_c=0`,
the pulled-back objective is affine on `P'`. Linear programming returns
an exact rational optimizer. Its minimum-norm optimal point in original
coordinates is the solution of a rational convex quadratic program on
the resulting optimal face; this is also polynomial-time solvable.
The promised error constant is available in this branch as well. If
`g_c=nabla phi(c)=0`, every feasible point is optimal and take
`Gamma_P=1`. Otherwise clear denominators of `g_c` and the polytope
rows with `D`, and use `A=Dg_c'` in (10). Since the equality residual
is exactly `D E`, that estimate gives

```
Gamma_P=max(1,W(sC_*)^(s-1)D),
```

where `W` is the norm bound for `V` in (12) and `C_*` includes the
cleared polytope rows. For `E<=1`, use `E<=E^(1/4)`. These constants
have polynomial bit length. We henceforth assume positive rank.

Define the rational upper bound

```
M=max(1, beta max_i sum_j |(H_c)_ij|).
```

Thus `||H(u)||_2<=M` on `P'`, and `log M` is polynomially bounded
in the input. The third-derivative symmetry identity and exact cubic
Taylor expansion from the box proof require only a feasible segment,
not a product domain. For an optimizer `v` and any `u in P'`, put
`d=u-v`, `E=phi(u)-phi(v)`, and

```
a=d'H(v)d,    b=d'H(u)d.
```

Then

```
E>= (a+b)/6,
d'H_c d=a+(c-v)'(H(u)-H(v))d.                           (6)
```

Use `||d||<=2R`, `||c-v||<=2R`, and the weaker uniform bound
`||H||<=2M` to apply the box estimate with diameter `2R` in place
of `sqrt n`. If `Pi` projects onto `K^perp` and `lambda` is the
smallest positive eigenvalue of `H_c`, it gives

```
E >= [d'H_c d]^2/(96 M (2R)^2)
  >= lambda^2 ||Pi d||_2^4/(384 M R^2).                 (7)
```

No center-to-optimizer margin is assumed. The interior ball is used
only to control all feasible Hessians by the known rational center
Hessian.

## 4. The affine slice and the general-polytope Hoffman constant

Put `g_c=nabla phi(c)`. As in the box proof, the polynomial
`phi(u)-g_c'u` has gradient in `K^perp`. Equations (6)--(7) imply

```
argmin_(P') phi
 = {w in P': H_c(w-v)=0, g_c'(w-v)=0}.                 (8)
```

The bound `||H||<=M` and (4) also imply

```
|g_c'd| <= E + M R ||Pi d||_2.                         (9)
```

We need the following integer-matrix Hoffman estimate. Let
`Q={w:Bw<=h}` be any polyhedron and let
`Z={w in Q:Aw=t}` be nonempty. Both `A,B` are integer matrices with
`s>=1` columns; their right-hand sides may be real. If

```
C_*=max(1,max|A_ij|,max|B_ij|),
```

then for every `u in Q`,

```
dist_2(u,Z) <= (s C_*)^(s-1) ||Au-t||_2.               (10)
```

The proof is the projection argument in the box theorem with active
rows of `B` replacing active coordinate normals. Select an independent
subset of original equality rows, then conically eliminate dependent
active inequality normals modulo that row space. At most `s` independent
integer rows remain. Their Gram determinant is a positive integer and
their largest singular value is at most `s C_*`; hence their smallest
singular value is at least `(s C_*)^(-(s-1))`.

In the projection inner product, each active inequality normal has a
nonpositive contribution because `u` is feasible for `Q`. Removing
those contributions bounds the squared distance by the coefficient norm
times `||Au-t||`. This proves (10), including redundant rows and
lower-dimensional slices. In particular its constant is independent
of the possibly irrational right-hand side in (8). Boundedness is not
needed for this projection lemma.

Choose a positive integer `D` clearing denominators of `H_c`, `g_c`,
and the transformed inequalities. Form

```
A=D[H_c;g_c'],    B=D[a_i']_i,
C_*=max(1,max|A_ij|,max|B_ij|),
lambda_0=D^(-s) M^(-(s-1)),
R_0=384 M R^2/lambda_0^2,
Gamma_u=(s C_*)^(s-1) D [1+M(1+R)R_0].                (11)
```

All numbers are rational, computable in polynomial time, and have
polynomial binary length. As in the box proof, a positive maximal-order
principal minor of `H_c` proves `lambda>=lambda_0`. For `0<=E<=1`,
(7), (9), and `E<=E^(1/4)` give

```
||Pi d||<=R_0 E^(1/4),
||Ad||<=D[1+M(1+R)R_0]E^(1/4).
```

Using (10) proves the distance bound in reduced coordinates. Set

```
W=max(1,sum_ij |V_ij|),    Gamma_P=W Gamma_u.            (12)
```

Since `||V||_2<=W`, mapping back to original coordinates proves (1).
The affine-hull parametrization need not be orthonormal.

## 5. Certified value optimization and exact feasible repair

The reduced problem is convex on a full-dimensional bounded rational
polytope with the known inner ball (3) and outer bound (4). The
[capped-epigraph weak-optimization construction](convex-patch-evaluation.md)
applies with these radii. Rational LP rows separate a query outside
`P'`; at a query inside `P'`, the polynomial tangent separates a
violated epigraph inequality. Both are exact rational operations.

For clarity, a monomial bound on the coordinate bounding box gives a
rational `F_max>=max(1,max_(P') |phi|)`. Cap the epigraph at `F_max+2`.
It contains a Euclidean ball of radius
`min(rho/2,1/2)` around `(c,F_max+1)` and has a polynomial-bit outer
radius. The usual inner-set comparison in weak optimization is
therefore controlled by polynomial-bit constants, just as in the
linked construction. Objective accuracy and distance to this epigraph
can be made arbitrarily small with polynomial dependence on their
requested bit lengths.

Coordinate clipping would not preserve the polytope. Instead suppose
the rational near-feasible output `u` is within `delta>0` of `P'`.
Apply the rational homothety

```
u_hat=(rho u+delta c)/(rho+delta).                       (13)
```

For every input normal,

```
a_i'u<=d_i+delta||a_i||_2,
d_i-a_i'c>=rho||a_i||_2,
```

so `u_hat` satisfies every inequality exactly. If `bar u in P'` is
within `delta` of `u`, then

```
||u_hat-bar u||_2 <= delta(1+R/rho).                     (14)
```

A rational coefficient bound on `||nabla phi||` over the coordinate
bounding box controls the objective loss between these two feasible
points. If `(u,t)` is within `delta` of the capped epigraph, take its
nearby feasible epigraph point `(bar u,bar t)`; then additionally
`phi(bar u)<=bar t<=t+delta`.

One explicit tolerance and certificate are useful. Let `G>=1` be the
gradient norm bound just described and put

```
r_K=min(rho/2,1/2),
A_0=1+(2F_max+1)/r_K,
C_0=A_0+1+G(1+R/rho),
delta=min(r_K/2,eta/C_0).
```

The weak-optimization interface returns `(u,t)` within `delta` of the
capped epigraph, with `t` at most `delta` above the minimum over its
`delta`-inner set. Moving an exact epigraph minimizer toward
`(c,F_max+1)` by fraction `delta/r_K` produces a point in that inner
set. Therefore `t<=f*+A_0 delta`. Equations (13)--(14) now make

```
[t-A_0 delta, phi(u_hat)]
```

a valid global value interval with feasible upper endpoint and width
at most `C_0 delta<=eta`. All constants have polynomial binary length.
This supplies the required value interface without assuming exact-feasible
output from weak optimization.

If a compact tangent lower certificate is required, use a finer convex
value solve as in the box interface and minimize its rational affine
tangent by LP over `P'`. Polynomial Hessian and diameter bounds give
the same polynomial-bit tangent-gap conversion. The feasibility and
point-distance theorem itself only needs the certified value interval.

Consequently a target value accuracy
`eta=(2^(-q)/Gamma_P)^4` gives the set-distance conclusion with
`poly(I)+O(q)` accuracy bits. No search over affine faces, optimizers,
or integer points is performed.

## 6. Minimum norm remains in the original coordinates

Let `p` be the minimum-norm point of `S` in the original coordinates,
and choose a rational `R_x>=1` bounding `||x||` on `P`, using coordinate
LP bounds. With `epsilon=2^(-q)`, take

```
tau=epsilon^6/(1024 R_x^4 Gamma_P^4),
eta=tau epsilon^2/4.                                    (15)
```

Minimize the reduced polynomial

```
phi(u)+tau||x_0+Vu||_2^2
```

to feasible objective gap `eta` by Section 5. Its exact minimizer
corresponds to the unique minimizer `x_tau` of `f+tau||x||^2` on
`P`. The already reviewed minimum-norm argument uses only convexity,
compactness, the original-coordinate bound (1), and the radius `R_x`.
It gives `||x_tau-p||<=epsilon/2` with (15).

For any feasible original point `x`, convexity and constrained
first-order optimality give

```
[f(x)+tau||x||^2]-[f(x_tau)+tau||x_tau||^2]
  >= tau||x-x_tau||^2.
```

This inequality is valid even when `P` is lower-dimensional. The
returned feasible value approximation is therefore within the other
`epsilon/2` of `x_tau` in original Euclidean distance. No lower bound
on a singular value of `V` is needed for this conversion, and no
normalized-coordinate norm is substituted for the original norm.
All parameters in (15) have `poly(I)+O(q)` bits. This proves the
canonical Cauchy-output conclusion.

## Verification status

The focused review passed the actual affine-hull preprocessing, rational
inball, generalized Hoffman argument, affine error-constant branch, and
polynomial-bit metric conversion. The full review passed the complete
saved addendum, including the explicit weak-output repair, certified
interval, and original-coordinate minimum norm. These were analytic
reviews; no duplicate diagnostic runs are attributed to them.
The author-side diagnostic owner ran
`python3 -B research-20261002/new-direction/check_convex_cubic_polytope.py`.
The [polytope-specific checker](check_convex_cubic_polytope.py) passed six
affine-hull fixtures and 24 universal-row classifications, four inball
LP vertices, 45 reflection/Hessian-domination points, 810 exact feasible
repair and objective-loss checks, 1,080 general-row Hoffman bounds on
12 rational slices, and 91 original-norm comparisons under a nonorthogonal
affine embedding. It includes a cubic convex on an oblique triangle but
not its coordinate bounding box, a clipping failure, implied equalities,
and a wrong-parameter-norm guard. The note author inspected the checker;
the diagnostic uses small enumerated LP bases and explicit optimizer
sets, not a general solver. It does not duplicate the box theorem's
cubic-identity checks.
The focused primary-source comparison is complete; it does not rule out
equivalent prior results, and Yang 2009 remains abstract-only in the
audit. This addendum makes no claim to cover nonlinear feasible sets
or general convexity recognition.
No index edits or project-wide checks are made.
