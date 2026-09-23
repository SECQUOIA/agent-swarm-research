# Sum-of-absolute-errors quadratic precision via the PSD Grothendieck bound

Date: 2026-09-05. Status: independently reviewed extension.
This note develops the `l1` output-error counterpart of the reviewed
[covariance characterization](../results/quadratic-weighted-covariance-precision.md)
and [polynomial rational construction](../results/quadratic-weighted-precision-polynomial-construction.md).
The semidefinite approximation ingredient is classical.

## Theorem

Let `f=(f_1,...,f_m)` be quadratic on `[0,1]^n`, with real symmetric
Hessians `H_j`, and require

```
sum_j |w_j-f_j(x)|<=epsilon,       epsilon>0.
```

For `P>=0`, form the positive semidefinite Gram matrix

```
Gamma(P)_jk=tr(H_j P H_k P).
```

It is the Gram matrix of `P^(1/2)H_jP^(1/2)` in Frobenius inner
product. Define its correlation-matrix semidefinite bound

```
S(P)=max{tr(Gamma(P) X): X>=0, diag(X)=1},
D_1=max{det P: 0<=P<=I, S(P)<=epsilon^2},
Phi_1=-(1/2)log2 D_1.
```

Put `c_n=max{6,n/4}` and
`A_n'=log2[omega_n(n+2)^(n/2)]+(n/2)log2 c_n`.
Then the same arbitrary-convex-lift and binary-LP minima satisfy

```
max{0,Phi_1-A_n'}<=p_conv<=p_bin<=Phi_1+n log2 n+n.      (1)
```

For rational quadratic coefficients and rational positive `epsilon`,
a deterministic polynomial-time algorithm produces a rational MILP
within additive `O(n log(n+1))` of `p_conv`. The additional correlation
matrix oracle is implemented below using classical weak optimization
and an explicit rational feasibility repair. The proof and source audit are linked below.

## Established semidefinite bound

For every positive semidefinite real `Gamma`, the classical positive
semidefinite Grothendieck inequality gives

```
max_(s in {-1,1}^m) s^T Gamma s
 <= max_(X>=0,diag(X)=1) tr(Gamma X)
 <= (pi/2) max_(s in {-1,1}^m) s^T Gamma s.               (2)
```

The upper ratio is Nesterov's established semidefinite relaxation bound;
it is not a new contribution. A primary source explaining this bound
and its improvements is Briët, de Oliveira Filho, and Vallentin,
[*The positive semidefinite Grothendieck problem with rank constraint*](https://arxiv.org/abs/0910.5765),
which credits the earlier Rietz and Nesterov results.

## Lower and upper precision bounds

The vector midpoint discrepancy within a parity support has `l1` norm
at most `4epsilon` when expressed using
`q_j(x-y)=(1/2)(x-y)^TH_j(x-y)`. For each sign vector `s`, its scalar
combination therefore has absolute value at most `4epsilon`. The
reviewed fourth-moment calculation gives, for the uniform covariance
`Sigma` of a compact positive-volume support,

```
s^T Gamma(Sigma)s<=16epsilon^2    for every sign vector s.
```

By (2), `S(Sigma)<=8pi epsilon^2<36epsilon^2`. Also
`Sigma<=(n/4)I`. Thus `Sigma/c_n` is feasible for `D_1`. The same
volume-covariance inequality and parity cover prove the lower bound
in (1). No enumeration of the sign vectors is used by the proof's
algorithmic part.

For the upper bound take a feasible `P` and the reviewed rotated grid.
Its shared residual error matrix `Z` has Frobenius norm at most `1/4`,
and each output error is `e_j=(1/2)tr(M_jZ)`, with
`M_j=P`-scaled transformed Hessian. For every sign vector,

```
|sum_j s_j e_j|
 <= (1/2)||sum_j s_j M_j||_F ||Z||_F
 <= (1/8)sqrt(s^T Gamma(P)s)
 <= epsilon/8.
```

Taking the maximum over sign vectors gives `||e||_1<=epsilon/8`.
The binary count and rational-grid arguments are otherwise unchanged.
The semidefinite surrogate costs only a dimension-independent factor
in covariance scaling, and hence only `O(n)` in integer dimension.

## Geodesic convexity and the SDP oracle

For any fixed correlation matrix `X`, the energy
`E_X(P)=tr(Gamma(P)X)` is an energy with a positive semidefinite output
budget. If `E_X` is identically zero, omit its logarithmic branch.
Otherwise it is positive for every positive definite `P`, and its half
logarithm is geodesically convex with normalized gradient

```
sum_(j,k) X_jk M_jM_k/E_X(P),
```

which is positive semidefinite, has trace one, and has norm at most one.
Consequently `(1/2)log S(P)` is the maximum of such geodesically convex
functions and is globally one-Lipschitz whenever some Hessian is nonzero.
Its maximum is attained because the correlation matrices form a compact
set. If all Hessians vanish, this branch is omitted.

The exact penalty

```
h(P)=max{0,log lambda_max(P),(1/2)log(S(P)/epsilon^2)},
F(P)=-log det P+n h(P)
```

has the same `2n` Lipschitz bound and equals the negative log determinant
after scaling `P` by `exp(-h(P))`. An SDP optimizer `X` supplies a
subgradient; a rational feasible `X` whose objective is within a small
relative factor of the optimum supplies a near-active component, which
is sufficient for the inexact subgradient recurrence.

For rational `P`, `Gamma(P)` is exactly rational. If it is nonzero,

```
tr Gamma(P)<=S(P)<=m tr Gamma(P).
```

The lower inequality uses `X=I`; the upper uses `X<=mI`. Normalize
`Gamma` by its positive trace before calling the SDP oracle. Its
entries then have magnitude at most one and the optimum lies in `[1,m]`.

### A rational oracle from weak optimization

Here is an explicit reduction to ordinary convex-body weak optimization;
it does not assume a black-box exact SDP optimizer. Work with normalized
`Gamma` of trace one. For `m>=3`, parameterize the correlation matrices
by their `d=m(m-1)/2` upper off-diagonal entries `v`, with
`X(v)=I+off(v)`. Their feasible body `K` contains the Euclidean ball of
radius `1/4` centered at zero: `||off(v)||_F=sqrt(2)||v||_2<1` there.
Also `K` is contained in the ball of radius `m`, because every correlation
entry has magnitude at most one. For `m=1,2` the scalar or interval
optimization is exact and elementary.

There is a polynomial-bit rational strong separation oracle. Exact
rational symmetric elimination either certifies `X(v)>=0` or produces
a rational vector `a` with `a^T X(v)a<0`; the inequality
`a^T X(u)a>=0` separates every `u in K` from `v`. The elimination uses
rational congruences and one- or two-dimensional pivots. A negative
pivot gives the vector directly; a zero diagonal with a nonzero
remaining off-diagonal entry gives an indefinite two-dimensional
principal block and a rational negative vector. Fraction-free
elimination bounds the intermediate encoding lengths polynomially.
Dividing the separating normal by its nonzero infinity norm makes
its Euclidean norm at least one, with polynomial encoding length.
The strict separation then satisfies the weak separation convention
in the cited 1981 paper for every positive oracle tolerance.

Grötschel, Lovász, and Schrijver's [1981 paper](https://ir.cwi.nl/pub/10046/10046D.pdf),
Definition (5) on printed page 172 and Theorem (3.1) on page 177,
therefore gives the following polynomial-bit operation. For any rational
`rho>0`, it returns rational `v` with distance at most `rho` from `K`
and with linear objective at most `rho` below its optimum. This uses
the explicit inner and outer radii above. Their definition and running
time include polynomial dependence on `log(1/rho)`.

Use the objective `sum_(j<k) 2Gamma_jk v_jk`. Write `s=S(P)/tr Gamma(P)`
for its optimum plus the constant one, so `1<=s<=m`, and set
`a=tr(Gamma X(v))`. Then

```
a>=s-rho,       lambda_min(X(v))>=-sqrt(2)rho>=-2rho.
```

The rational repair

```
X_f=(X(v)+2rho I)/(1+2rho)
```

has exact unit diagonal and is positive semidefinite. Its objective
`a_f=(a+2rho)/(1+2rho)` satisfies

```
0<=s-a_f
 <= [rho+2rho(s-1)]/(1+2rho)
 <=(2m+1)rho.
```

Thus, given rational `0<nu<=1/2`, choose
`rho=nu/[4(m+1)]`. The rational pair

```
L=tr(Gamma(P) X_f),       U=L+nu tr Gamma(P)
```

satisfies `L<=S(P)<=U`, `L>=tr Gamma(P)/2`, and `U/L<=1+2nu`.
The upper value is certified by the weak optimization guarantee; no
explicit dual SDP point is needed. All matrices and bounds have
polynomial encoding length.

The feasible `X_f` supplies a near-active budget and its normalized
gradient. Since `S(P)/L<=1+2nu`, the half-log discrepancy is at most
`nu`. The value `U` supplies the upper bound for final scaling repair.
Taking inverse-polynomial `nu` within the existing branch-evaluation
budget therefore gives precisely the inexact oracle used by the
reviewed polynomial construction. Approximating the resulting full
penalty subgradient, including its factor `n`, uses the error allocation
already stated in that construction.

For conditioning, `tr Gamma(P)>=lambda_min(P)^2 tr Gamma(I)`, and
the last trace is a positive rational of polynomial bit length. A
feasible dyadic covariance can be chosen from
`delta^2 m tr Gamma(I)<=epsilon^2`. Therefore the previous polynomial
radius and finite-precision matrix bounds remain valid. Every numerator
in the normalized gradient is computed directly from rational `X` and
the matrix-function approximations; no factorization of `X` is needed.

## Scope and current status

A rational linear transformation of the outputs permits weighted `l1`
budgets `||A(w-f(x))||_1<=epsilon`. Finitely many such budgets can be
combined with the already reviewed positive semidefinite quadratic
budgets by taking the maximum of their penalty components. The number
of groups affects running time but not the dimension-only additive
bound.

This does not transfer the separate componentwise-error hardness theorem
to a single `l1` budget: its low-case product construction has a different
total-error budget. No such hardness claim is made here.

The [independent proof and source audit](../notes/review-quadratic-l1-output-precision.md)
passed. The proposed connection is the integer-dimension guarantee, not
the Grothendieck inequality, correlation SDP, or its optimization algorithms.
The [general symmetric-body theorem](quadratic-general-norm-output-precision.md)
also covers this norm at the `O(n log(n+1))` level; the present result
retains a specific constant-factor semidefinite covariance surrogate
and explicit finite constants. The [related novelty assessment](../notes/quadratic-general-norm-precision-novelty.md)
records this overlap and does not establish publication priority.

The reproducible checker `code/quadratic_rank/check_l1_errors.py` passed
24 exact shared-residual `l1` bounds and 30 exact rational elliptope
feasibility and certified-upper-bound repairs. It checks the new algebraic
steps, not an implementation of classical weak optimization.
