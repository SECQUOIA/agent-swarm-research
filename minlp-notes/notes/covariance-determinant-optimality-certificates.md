# Finite certificates for the covariance determinant benchmark

Date: 2026-09-05. Status: independently reviewed useful certificate;
see [the root audit](review-covariance-optimality-certificate-root.md).
This note may help practical implementations of the reviewed
[quadratic precision construction](../results/quadratic-weighted-precision-polynomial-construction.md).
It does not propose a new general optimality-certificate method.

Consider the determinant problem with energies
`E_j(P)=tr(H_jPH_jP)` and positive bounds `epsilon_j^2`. Let `P` be
any exactly feasible positive definite covariance, so `0<P<=I` and
all stated energy budgets hold. Choose arbitrary
nonnegative multipliers `mu_j` and a positive semidefinite matrix `S`.
Define

```
c=sum_j mu_j(epsilon_j^2-E_j(P))+tr[S(I-P)]>=0,
R=-P^(-1)+2sum_j mu_j H_jPH_j+S,
G=P^(1/2) R P^(1/2),
L=-log det P>=0.
```

If `D_star` is the optimal determinant, then

```
0<=log D_star-log det P <= c+sqrt(n)L ||G||_F.            (1)
```

In particular, complementarity `c=0` and stationarity `R=0` certify
that `P` is globally optimal. No claim of necessity is needed here.

**Proof.** The Lagrangian

```
J(X)=-log det X+sum_j mu_j(E_j(X)-epsilon_j^2)
                    +tr[S(X-I)]
```

is geodesically convex on positive definite matrices. The energy terms
are geodesically convex, `-log det` is geodesically affine, and
`tr(SX)` is geodesically convex because `S` is positive semidefinite.
Its gradient in isometric coordinates at `P` is `G`.

Let `P_star` be an optimal feasible covariance. Since all eigenvalues
of both matrices are at most one and `det P_star>=det P`, both
minimum eigenvalues are at least `det P`. Therefore every eigenvalue
of `P^(-1/2)P_starP^(-1/2)` lies in
`[det P,1/det P]`, and its logarithm `A` satisfies
`||A||_F<=sqrt(n)L`. Geodesic convexity gives

```
-log D_star >= J(P_star)
             >= J(P)+tr(GA)
             >= -log det P-c-sqrt(n)L||G||_F.
```

Rearrange to obtain (1). ∎

For rational `P,mu,S`, the squared residual norm can be evaluated
without a matrix square root:

```
||G||_F^2=tr(PRPR).
```

It is a nonnegative rational number. Certified scalar log and square-root
bounds turn (1) into a fully rigorous numerical interval for the
determinant benchmark. An arbitrary feasible covariance already gives
a binary upper construction; (1) can additionally bound its distance
from the best covariance and therefore from the best integer count.

With `P` fixed, minimizing the right side of (1) over `mu>=0,S>=0`
is a convex conic problem: `c` is linear and `G` is affine in the
multipliers. Thus candidate multipliers from a local nonlinear solver
can be improved or verified separately. This observation does not assert
that a numerical solver returns exact feasible multipliers automatically.

For the [correlated budget extension](../results/quadratic-ellipsoidal-output-precision.md),
replace each `H_jPH_j` by its positive semidefinite budget sum
`sum_(a,b) W_(j,ab) H_a P H_b`; the same proof applies.
