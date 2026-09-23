# Polynomial-time construction of nearly minimal quadratic precision formulations

Date: 2026-09-05. Status: independently reviewed twice. Publication priority
is unestablished. The theorem builds on the reviewed
[finite covariance precision law](quadratic-weighted-covariance-precision.md).
The proof audits and novelty assessment are linked below.

## Theorem and scope

For quadratic outputs with all coefficients rational, symmetric Hessians
`H_j`, rational positive tolerances
`epsilon_j`, and the unit input cube, a deterministic polynomial-time
algorithm constructs a rational MILP graph relaxation using at most

```
p_conv + O(n log(n+1))
```

binaries, where `p_conv` permits arbitrary convex lifts and unrestricted
general integer coordinates. Polynomial time here means polynomial in
the total rational input encoding length, including the binary encoding
of all tolerances. The additive constant is uniform over the Hessians
and tolerances. The proof computes a covariance with log determinant within a constant
of optimum, then constructs a rational version of the reviewed rotated grid.

This is a polynomial-time existence theorem; the conservative iteration
bounds are not a practical runtime claim. The algorithm is an application of established geodesic subgradient methods;
no novelty claim is made for those methods or for the geometry of
positive definite matrices.

The reviewed [approximation hardness theorem](quadratic-integer-precision-approximation-hardness.md)
rules out additive `O(n^(1-delta))` for every fixed `delta>0`, unless
`P=NP`. This remains true with unit tolerances and a positive minimum
integer dimension. Thus the construction has the best possible dimension
exponent up to subpolynomial factors, without claiming a sharp logarithm.

The [correlated-budget extension](quadratic-ellipsoidal-output-precision.md)
preserves the construction for Euclidean, ellipsoidal, and overlapping
groups of output error budgets.

## Established geometric algorithm used

The positive definite cone has affine-invariant metric

```
<A,B>_P=tr(P^(-1) A P^(-1) B),
d(P,Q)=||log(P^(-1/2) Q P^(-1/2))||_F.
```

It is a Hadamard manifold with sectional curvature between `-1/2` and
zero. A weaker lower bound `-1` is sufficient here. See Criscitiello and
Boumal, Proposition I.1, Appendix I,
[primary paper](https://arxiv.org/abs/2008.02252).

Zhang and Sra's projected subgradient analysis gives, on a geodesically
convex set of diameter `D`, a bound of order
`DL sqrt(zeta(-1,D)/T)` for a geodesically convex `L`-Lipschitz objective.
Here `zeta(-1,D)=D/tanh(D)<=1+D`. The proof's summed one-step inequality
also bounds the best iterate. We use Corollary 8 and the proof of
Theorem 9 in their
[open primary paper](https://proceedings.mlr.press/v49/zhang16b.pdf).
The constrained domain below is a metric ball, so projection has an
explicit spectral formula.

## An exact penalty that also repairs feasibility

Write `E_j(P)=tr(H_jPH_jP)` and omit zero Hessians from the formulas
involving their logarithms. For every positive definite `P`, define

```
h(P)=max{0, log lambda_max(P),
         max_(j:H_j!=0) (1/2)log(E_j(P)/epsilon_j^2)},
F(P)=-log det P+n h(P).
```

All logarithms in this note are natural. The repaired covariance

```
P_hat=exp(-h(P))P
```

satisfies `P_hat<=I` and all `E_j(P_hat)<=epsilon_j^2`. In fact,

```
F(P)=-log det P_hat.                                    (1)
```

If `D_star` denotes the maximum determinant in the finite theorem,
then `F(P)>=-log D_star` for every positive definite `P`, with equality
at every determinant maximizer. Thus there is no unknown penalty
parameter or feasibility-versus-objective tradeoff.

Each component of `h` is geodesically convex. The energy statement
was proved in the finite result. The eigenvalue statement follows from
`log lambda_max(P)=sup_(v!=0) log[(v^T P v)/(v^T v)]`:
on a geodesic, each logarithm is a scalar log-sum-exp after diagonalizing
the generator. The zero component is constant.

In the isometric coordinates that represent a tangent vector by
`P^(-1/2) A P^(-1/2)`, the gradient of `(1/2)log E_j(P)` is

```
M_j^2/tr(M_j^2),        M_j=P^(1/2) H_j P^(1/2).
```

It is positive semidefinite with trace one, hence has Frobenius norm
at most one. The gradient of `log(v^TPv)` is likewise the trace-one
matrix

```
P^(1/2) v v^T P^(1/2)/(v^T P v).
```

These formulas show that `h` is globally one-Lipschitz. Since the
gradient of `-log det P` is represented by `-I`, `F` is globally
`L=n+sqrt(n)<=2n` Lipschitz and geodesically convex.

## A ball of polynomial radius contains an optimizer

Choose a nonnegative integer `b` such that

```
delta=2^(-b)<=1,
delta ||H_j||_F<=epsilon_j  for every j.
```

One can choose `b` in polynomial time without irrational comparisons
by replacing `||H_j||_F` by `sum_(a,c)|H_(j,ac)|` and rounding the
resulting rational logarithmic bound upward. Its magnitude is polynomial
in the input encoding length. The covariance `delta I` is feasible.

For an optimum `P_star`, all its eigenvalues are at most one and
`det P_star>=delta^n`. Hence

```
d(I,P_star)=sqrt(sum_i (log lambda_i(P_star))^2)
           <=sum_i -log lambda_i(P_star)
           <=nb log 2.
```

Set `R=1+nb`. The closed metric ball `B_R={P:d(I,P)<=R}` contains an
optimizer. It is geodesically convex. Projection of a positive definite
matrix onto this ball is

```
Proj_R(P)=exp(t log P),
t=min{1,R/||log P||_F},
```

with the natural identity convention when `P=I`. The formula is exact:
the reverse triangle inequality gives the lower bound `d(I,P)-R`
for distance to the ball, and the radial geodesic attains it.

With exact arithmetic, the imported subgradient bound gives polynomially
many iterations to obtain `F(P)<=-log D_star+1/4`, because the domain
diameter, curvature factor, and Lipschitz constant are all polynomial
in `n,b`. The remaining subsections explain how to avoid assuming exact
transcendental arithmetic.

## Inexact one-step estimate

The following proof makes rounding errors local; it does not attempt to
track a single exact trajectory through all iterations.

Initialize the outer iteration at `P_0=I`. Suppose every stored iterate is rational positive definite and lies
within `B_(R+1)`. Let `P_star` be an optimal covariance in `B_R` and set
`D=2R+2`, `Z=1+D`. At the current iterate `P`, obtain a symmetric
matrix `G` in isometric tangent coordinates satisfying

```
||G||_F<=3n,
F(P)-F(P_star)
 <= -tr[G log(P^(-1/2)P_star P^(-1/2))]+e.               (2)
```

The sign in (2) is consistent with descent: the exact subgradient
inequality is `F(P_star)>=F(P)+<grad F(P),Log_P(P_star)>`.

Form the conceptual exact update and exact projection

```
Q=P^(1/2) exp(-eta G) P^(1/2),
Q_bar=Proj_R(Q),
```

then store a rational symmetric `P_next` with `d(P_next,Q_bar)<=xi`.
For `xi<=1`, the next iterate lies in `B_(R+1)`. The Zhang--Sra
comparison inequality and the nonexpansiveness of projection give

```
F(P)-F(P_star)
 <= [d(P,P_star)^2-d(P_next,P_star)^2]/(2eta)
    + Z eta(3n)^2/2 + e +(2D xi+xi^2)/(2eta).            (3)
```

For the rounding term, use
`d(P_next,P_star)<=d(Q_bar,P_star)+xi` and
`d(Q_bar,P_star)<=2R<D`. No error from earlier iterations is amplified
outside the telescoping distance term.

For example, take

```
eta=1/[16 Z(3n)^2],
T=ceil(16D^2/eta),
e<=1/32,
xi<=eta/[128(D+1)].
```

Sum (3) for `T` iterations. The average objective gap is at most

```
1/32+1/32+1/32+1/64 < 1/4.
```

Thus some stored iterate has gap below `1/4`. Evaluating objective
values within `1/64` and selecting the smallest reported value gives
a stored iterate with gap below `1/4+1/32<1/2`.

## Obtaining the inexact oracle and rounded steps in polynomial bit complexity

All stored matrices have eigenvalues in
`[exp(-(R+1)),exp(R+1)]`. Taking absolute entrywise accuracy
`2^(-poly(input length,n,b))` therefore suffices for all fixed inverse
polynomial metric accuracies required above. More explicitly, if a
symmetric approximation differs from a positive definite matrix of
minimum eigenvalue `a` by operator norm at most `a u`, `u<=1/2`,
then its relative eigenvalues lie in `[1-u,1+u]` and its metric
distance is at most `2sqrt(n)u`.

For nonzero rational `H_j`, on this ball

```
E_j(P)>=exp(-2(R+1)) ||H_j||_F^2.
```

This follows by viewing `E_j(P)` as the squared Frobenius norm of
`P^(1/2)H_jP^(1/2)` and using the minimum singular value of the
two-sided multiplication. A nonzero rational input entry has magnitude
at least `2^(-s)` for input encoding length `s`. Thus every denominator
in the normalized energy gradient has inverse of at most exponential
polynomial magnitude. Logs, inverses, square roots, and normalized
gradients consequently need only polynomially many precision bits.

Approximate each component of `h` to additive `tau`, choose a maximizing
reported component, and approximate its gradient in isometric
coordinates to error `nu/n`. The chosen component is within `2tau`
of the maximum. Its exact gradient is then a `2tau`-subgradient for
`h`. The resulting `G=-I+n grad h` has approximation error at most
`nu` and satisfies
(2) with

```
e<=2n tau+D nu.
```

Choose `tau<=1/(128n)` and `nu<=1/[64(D+1)]`. The displayed `e<=1/32`
then holds.

There is no need to choose a distinguished eigenvector at a repeated
largest eigenvalue. The [rational Jacobi lemma](../notes/rational-jacobi-matrix-functions.md)
returns an exactly orthogonal rational `V` with
`||P-V diag(V^TPV)V^T||<=sigma`. Choose the column `v` corresponding
to the largest diagonal entry. Its exact Rayleigh quotient differs from
`lambda_max(P)` by at most `sigma`; taking
`sigma<=tau lambda_min(P)/2` bounds its logarithmic error by `tau`.
Use the smooth geodesically convex branch
`log[(v^T P v)/(v^T v)]` and its displayed gradient. This adds at most
`tau` to the branch error; using `tau<=1/(256n)` absorbs it in the
stated `e<=1/32` budget.

The same self-contained lemma evaluates matrix logarithms, exponentials,
inverse square roots, and radial projection with polynomial bit complexity
on the stated spectral ranges. It uses rational exactly orthogonal
rotations, a proved geometric off-norm contraction, and explicit
matrix-function perturbation estimates. It needs no eigenvalue gap or
real-arithmetic eigensolver import. The exact intermediate update `Q`
has logarithmic spectral bounds at most `R+1+eta(3n)`, so it satisfies
the same conditioning bounds. Round the final projected matrix
symmetrically to dyadic entries with sufficiently many bits to ensure
metric error `xi`. The relative-error inequality above proves that it
stays positive definite and in `B_(R+1)`.

After selecting the best stored rational `P`, estimate from above

```
kappa=max{1,lambda_max(P),max_j sqrt(E_j(P))/epsilon_j}
```

by a positive rational `kappa_bar` within relative factor
`exp(1/(4n))`. The matrix `P_hat=P/kappa_bar` is rational and exactly
feasible; verify its matrix cap and rational energy inequalities if
desired. Its negative log determinant exceeds `F(P)` by at most `1/4`.
Thus the rational covariance output has

```
log det P_hat>=log D_star-1.                             (4)
```

## A rational grid with only an additional linear number of binaries

It remains to turn rational `P_hat` into rational formulation coefficients.
Apply the rational Jacobi routine with `sigma<=lambda_min(P_hat)/2`,
using a certified positive rational lower bound on that eigenvalue from
the earlier spectral estimates. It returns exactly orthogonal rational
`Q` with `B=Q^T P_hat Q` and off-norm at most `sigma`. Set
`lambda_tilde_i=B_ii/4`. Then

```
P_hat/8 <= P_tilde=Q diag(lambda_tilde)Q^T <= P_hat/2,
Q^TQ=I,        0<lambda_tilde_i<=1.
```

Indeed, `P_tilde` differs from `P_hat/4` in operator norm by at most
`lambda_min(P_hat)/8`. Its scales are positive because every diagonal
entry of `B` lies between the extreme eigenvalues of `P_hat`. The
minimum eigenvalue has an exponential-polynomial lower bound, so the
construction takes polynomial time.

The energies are monotone in the positive semidefinite order: the
directional derivative of `E_j(P)` in a positive semidefinite direction
`A` is `2tr(H_jPH_jA)>=0`, since `H_jPH_j` is positive semidefinite.
Therefore `P_tilde` remains feasible and

```
det P_tilde>=8^(-n) det P_hat.                           (5)
```

Use rational coordinates `x=Qy`. Each coordinate of `Q^T x` has
width at most `sqrt(n)` on the unit cube. Translate its bounding box,
and use residual widths at most `sqrt(lambda_tilde_i/n)` as in the
reviewed grid proof. Orthogonality is not needed for the identity

```
tr(H_j P_tilde H_j P_tilde)
 = ||diag(sqrt(lambda_tilde)) Q^T H_j Q
                diag(sqrt(lambda_tilde))||_F^2.
```

All coordinate identities, widths, prefixes, and transformed Hessian
coefficients are rational. Bit depths can be chosen without irrational
comparisons by squaring the target width inequality. With
`L_i=ceil(log2(w_i sqrt(n/lambda_tilde_i)))`,

```
sum_i L_i <= -(1/2)sum_i log2 lambda_tilde_i
             +n log2 n+n.
```

The relation `det P_tilde=product_i lambda_tilde_i` is exact because
`Q` is orthogonal. Equations (4), (5), and the finite
integer lower bound therefore give the count
`p_conv+O(n log(n+1))`.

The total formulation encoding length is polynomial. The determinant
benchmark is itself at most `O(nb)` in log scale, so the number of
binary digits and all depths are polynomial. The exact rational inverse
of the polynomial-bit matrix `Q` also has polynomial bit length by
the adjugate and determinant formulas.

## Verification and novelty boundary

The [first proof audit](../notes/review-quadratic-weighted-precision-algorithm.md)
and [second proof audit](../notes/review-quadratic-weighted-precision-algorithm-second.md)
both passed. They reviewed the exact penalty, known geometric convergence
inequality, all finite-precision budgets, rational Jacobi implementation,
feasibility repair, and final rational MILP encoding. Review corrected the
component-gradient accuracy to `nu/n`, made rational affine coefficients
explicit, and requested explicit initialization at `P_0=I`.

`code/quadratic_rank/check_covariance_algorithm.py` passed 26 exact rational
Jacobi contractions across six positive definite matrices and 40 checks
of penalty derivatives and feasibility repair. The finite precision
formulation itself has its separate residual LP and rotated-domain checks.
These calculations supplement the proof.

The [independent novelty assessment](../notes/quadratic-weighted-precision-algorithm-novelty.md)
identifies established ellipsoid and Hessian metric selection, simultaneous
output tolerances in mesh adaptation, geodesic metric optimization, and
projected subgradient algorithms. The candidate contribution is the
polynomial-time construction of a rational MILP whose binary count is
within `O(n log(n+1))` of the integer dimension achievable by arbitrary
convex lifts with unrestricted general integer coordinates. The bounded
search did not locate this guarantee; it does not establish priority.

The [general symmetric-error-body extension](quadratic-general-norm-output-precision.md)
uses classical oracle ellipsoid rounding on the effective quadratic output
image to retain this additive guarantee for arbitrary well-bounded norm
balls with polynomial rational strong separation.

The supporting rational Jacobi guarantee also appears in
[Del Pia (2026), Theorem 2](https://arxiv.org/html/2607.29386).
That established spectral ingredient is distinct from the whole-graph
integer-count guarantee proved here. The self-contained audited
implementation remains in the linked matrix-function appendix.

The [nonlinear input-rank refinement](quadratic-nonlinear-input-rank-precision.md)
replaces the additive dimension term by `O(r log(r+1))`, where `r` is
the exact rank of the stacked Hessians. Affine input directions remain
in the continuous lift and do not contribute to this overhead.
