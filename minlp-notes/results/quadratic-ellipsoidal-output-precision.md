# Correlated and grouped quadratic output error budgets

Date: 2026-09-05. Status: independently reviewed extension; audit linked below.
This extends the reviewed [finite covariance law](../results/quadratic-weighted-covariance-precision.md)
and [polynomial rational construction](../results/quadratic-weighted-precision-polynomial-construction.md)
to Euclidean, ellipsoidal, and overlapping groups of output errors.

## Statement

Let `f=(f_1,...,f_m)` be quadratic on `[0,1]^n`, with symmetric
Hessians `H_j`. Let `W_1,...,W_g` be positive semidefinite `m` by `m`
matrices and `epsilon_l>0`. Require every admitted graph error `e=w-f(x)`
to satisfy

```
e^T W_l e<=epsilon_l^2,            l=1,...,g.             (1)
```

Thus `W=I` gives a Euclidean output error budget, a positive definite
`W` gives an ellipsoidal budget, and coordinate or group projection
matrices give separate possibly overlapping groups. The matrices may
be singular; directions not measured by any budget are unrestricted.

Set

```
E_l(P)=sum_(j,k) (W_l)_jk tr(H_j P H_k P),
D=max{det P: 0<=P<=I, E_l(P)<=epsilon_l^2 for every l},
Phi=-(1/2)log2 D.
```

Use the same definitions of `p_conv,p_bin` and the same dimension-only
constants `A_n,B_n` as the finite covariance law, with accuracy now
interpreted by (1). Then

```
max{0,Phi-A_n}<=p_conv<=p_bin<=Phi+B_n.                  (2)
```

If all quadratic coefficients, all `W_l`, and all positive tolerances
are rational, the polynomial-time construction extends to produce a
rational MILP with at most `p_conv+O(n log(n+1))` binaries. No irrational
factorization of the budget matrices is needed by the algorithm.

This includes the original separate accuracy theorem by taking
`W_l=e_l e_l^T`. It also includes a single Euclidean budget without
replacing it by componentwise tolerances and paying a factor depending
on the number of outputs.

## The energy is nonnegative and has the required covariance bound

For the proof only, factor `W_l=C_l^T C_l` and form the transformed
Hessians `G_a=sum_j (C_l)_aj H_j`. Cyclic trace gives

```
E_l(P)=sum_a tr(G_a P G_a P)>=0.                         (3)
```

Consequently it is continuous, homogeneous of degree two, and monotone
under the positive semidefinite order on `P`. The determinant maximum
is positive and attained just as before.

Within a parity support, the vector quadratic midpoint identity implies

```
q(x-y)^T W_l q(x-y)<=16epsilon_l^2,
q_j(z)=(1/2)z^TH_jz.
```

For centered independent uniform points `X,Y` in a compact positive-volume
parity support, apply the scalar fourth-moment expansion to each transformed
Hessian and sum. The sum of covariance energy terms is `E_l(Sigma)`;
every other term is a squared norm or squared mean norm and is nonnegative.
Thus `E_l(Sigma)<=16epsilon_l^2`. The same cap
`Sigma<=(n/4)I`, scaling by `max(4,n/4)`, volume bound, and parity
cover prove the lower half of (2).

## The same shared grid controls each whole error ellipsoid

Take a feasible `P=U diag(lambda)U^T` and the same rotated grid with
residual widths `h_i<=sqrt(lambda_i/n)`. Let `delta_ik` denote the
error in a shared approximate residual monomial. It is symmetric and
satisfies `|delta_ik|<=h_i h_k/4` for all entries, including squares.
Set

```
Z_ik=delta_ik/sqrt(lambda_i lambda_k),
M_j=diag(sqrt(lambda)) U^T H_j U diag(sqrt(lambda)).
```

Every entry of `Z` has absolute value at most `1/(4n)`, so
`||Z||_F<=1/4`. The output error is exactly

```
e_j=(1/2)tr(M_j Z).
```

Using the conceptual factorization in (3) and Cauchy--Schwarz for
each Frobenius inner product gives

```
e^T W_l e
 = (1/4)sum_a tr[(sum_j (C_l)_aj M_j)Z]^2
 <= (1/4) E_l(P) ||Z||_F^2
 <= epsilon_l^2/64.                                    (4)
```

The binary count and row count are unchanged. In particular, this
bound is independent of the number of outputs and groups. The same
argument works for the rational orthogonal grid in the polynomial-time
construction.

## Polynomial-time computation keeps the budget matrices rational

Use the exact penalty from the algorithm result, replacing the scalar
output energy by each `E_l`:

```
h(P)=max{0,log lambda_max(P),
         max_(l:E_l(I)>0) (1/2)log(E_l(P)/epsilon_l^2)},
F(P)=-log det P+n h(P).
```

When `E_l(I)=0`, (3) implies that all transformed quadratic Hessians vanish, so
this energy is identically zero and its logarithm is simply omitted.
The corresponding measured affine terms are still represented exactly.
The factorization is used only to prove this equivalence; `E_l(I)`
is computed exactly from rational coefficients.

On any affine-invariant geodesic, (3) and the earlier diagonal-generator
argument make `E_l` a sum of exponentials with nonnegative coefficients.
Thus its logarithm is geodesically convex. In isometric tangent
coordinates its normalized half-log gradient is

```
N_l(P)/E_l(P),
N_l(P)=sum_(j,k) (W_l)_jk M_j M_k,
M_j=P^(1/2)H_jP^(1/2).
```

The matrix `N_l(P)` is symmetric positive semidefinite: by the
conceptual factorization it equals `sum_a (sum_j (C_l)_aj M_j)^2`.
Its trace is `E_l(P)`. The gradient therefore has norm at most one,
and the same global `2n` Lipschitz bound and exact scaling repair apply.
Implementation evaluates the rationally specified double sum, rather
than an irrational `C_l`.

Choose a feasible dyadic scale using rational upper bounds on `E_l(I)`:
if `delta^2 E_l(I)<=epsilon_l^2` for every group, then `delta I`
is feasible. Exact rational comparison and dyadic search find such a
`delta=2^(-b)` with `b` polynomial in the input encoding length.
The optimizer lies in the same radius `1+nb` ball.

For every nonzero group energy on that ball,

```
E_l(P)>=lambda_min(P)^2 E_l(I).
```

This follows from (3). Since `E_l(I)` is a positive rational of
polynomial bit length, it has an inverse-exponential-polynomial lower
bound, even if there is cancellation in its rational double-sum
expression. Therefore the normalized gradient and logarithm retain
the finite-precision conditioning estimates. All Jacobi, matrix-function,
inexact-subgradient, exact rational repair, and rational-grid arguments
from the construction theorem apply unchanged. The double sums have
only polynomially many terms in the input size.

## Novelty and verification boundary

Ellipsoidal and multiple-output interpolation metrics are established
in mesh adaptation. This extension does not claim those concepts as
new. Its proposed contribution is the same arbitrary-convex-lift
integer-dimension characterization and polynomial-time rational MILP
guarantee under correlated and grouped error budgets. See the existing
[novelty assessment](../notes/quadratic-weighted-precision-algorithm-novelty.md)
for the nearby metric-selection and geometric-optimization literature.

The [independent proof audit](../notes/review-quadratic-ellipsoidal-output-precision.md)
passed, including singular budgets, covariance summation, shared-error
control, the positive semidefinite normalized gradient, and rational
finite-precision bounds. The root agent separately reviewed the proof
outline. `code/quadratic_rank/check_ellipsoidal_errors.py` passed 20 exact
rational cases checking correlated-budget gradient factorizations, shared
residual bounds, and the vector fourth-moment identity. The independent
auditor also checked 16 exact rational cases.
