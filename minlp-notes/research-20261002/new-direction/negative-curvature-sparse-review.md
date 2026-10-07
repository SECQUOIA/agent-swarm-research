# Review of the negative-curvature structural bounds

Date: 2026-10-02. Scope: an independent algebraic review of Sections 1--3
of [negative-curvature-sparse.md](negative-curvature-sparse.md).
No new agents, executable tests, or external searches were used.

**Verdict.** The metric inequality, proximal contraction and threshold
example are correct with the stated continuous convex-domain scope.
The envelope identities also check directly. They do not establish the
open sparse algorithm or a growth-independent certificate.

## 1. Growth in the shifted Hessian metric

Write `F(x)=x^T H x/2+b^T x+c`, with symmetric `H`, and
`nu=max(0,-lambda_min(H))`. Let `s` be a global optimizer, `d=x-s`,
and `Delta=F(x)-f*`. First-order optimality on a convex feasible set
gives `grad F(s)^T d>=0`, so exact expansion implies

```
Delta >= d^T H d/2.
```

If also `Delta>=g||d||^2`, take a convex combination with weights
`g/(g+nu)` and `nu/(g+nu)`. This gives exactly

```
Delta >= [g/(2g+2nu)] d^T(H+2nu I)d.                              (1)
```

With growth toward a general optimal set `S`, choose `s` nearest to
`x` in Euclidean distance. An arbitrary optimizer need not satisfy the
second premise. Since minimizing the shifted quadratic distance over
`S` can only decrease its value, (1) also implies growth toward `S`
in that metric.

For `nu>0`, `H+2nu I` is positive definite. At `nu=0`, it is merely
positive semidefinite and can be singular. The main note correctly
restricts its positive-definite metric interpretation to `nu>0`.

## 2. The convex proximal baseline

Use the exact proximal objective

```
F(x)+(lambda/2)||x-c||^2,                lambda>nu,
```

on the original bounded convex domain, with feasible `c`. It is
strongly convex. Let `y` be its minimizer, choose a nearest optimizer
`s` to `y`, and set

```
Delta_y=F(y)-f*,      r=||y-s||,      d=||c-y||.
```

Weak convexity and constrained proximal optimality give, respectively,

```
Delta_y <= grad F(y)^T(y-s)+(nu/2)r^2,
grad F(y)^T(y-s) <= lambda(c-y)^T(y-s).
```

Therefore `Delta_y<=lambda d r+(nu/2)r^2`. Under growth
`Delta_y>=g r^2` and `a=1-nu/(2g)>0`, this yields

```
a Delta_y <= lambda d sqrt(Delta_y/g),
Delta_y <= lambda^2 d^2/(g a^2).                                (2)
```

The zero-gap case is immediate; otherwise division by the positive
square root is valid. Comparing the proximal objective at `y` and
`c` gives

```
Delta_c-Delta_y >= (lambda/2)d^2.
```

Combining this with (2) proves the claimed contraction

```
Delta_y <= [C/(1+C)] Delta_c,
C=2lambda/[g(1-nu/(2g))^2].                                     (3)
```

These arguments hold at box or convex-polytope boundaries. The
variational inequalities, rather than zero-gradient equations, are
what is required. No constraint qualification is needed. They do not
extend directly across distinct integer assignments.

The threshold example is also correct. For `nu>0`, the function
`F(x)=nu x-(nu/2)x^2` on `[0,1]` has unique minimizer zero and global
growth `g=nu/2`. From center one, the proximal objective has derivative
`(lambda-nu)(x-1)` and is minimized at one for every `lambda>nu`.
Thus the proximal iteration can stall at a nonoptimal point when
`nu=2g`.

## 3. Envelope identities and the remaining scope

For `E_lambda(c)=min_x[F(x)+lambda||x-c||^2/2]`, subtracting
`lambda||c||^2/2` leaves an infimum of affine functions of `c`.
This proves the stated upper coordinate curvature `lambda`.

Growth and relaxation of the domain of the inner quadratic give

```
E_lambda(c)-f*
 >= min_(x in R^n, s in S) [g||x-s||^2+(lambda/2)||x-c||^2]
 = [g lambda/(2g+lambda)] dist(c,S)^2.
```

The displayed envelope growth constant and ratio are therefore correct.
Choosing `lambda` comparable to `nu` concerns `nu>0`; the case `nu=0`
is already a convex optimization problem. On an unconstrained branch,
differentiating the exact quadratic minimizer gives the claimed Hessian
`lambda H(H+lambda I)^(-1)`, which can be dense.

The contraction uses a quantitative growth promise and deteriorates as
`nu/g` approaches two. A proximal subproblem certificate does not verify
that global growth promise. The reviewed identities thus support the
stated baseline and the proposed metric, while leaving sparse state
representation and independent global certification unresolved.
