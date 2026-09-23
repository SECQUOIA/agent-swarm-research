# A rational block log-determinant oracle for convex trace budgets

Date: 2026-09-05. Status: supporting extension, independently reviewed twice.

This extends the reviewed scalar
[log-product oracle](rational-log-product-convex-body-oracle.md) to
positive definite matrix blocks. The same classical weak-optimization
and exact central-ball repair argument applies. It supplies a direct
Euclidean convex solver for block trace allocation, without geodesic
optimization.

## Statement

Let `P=(P_1,...,P_B)` range over symmetric blocks of sizes `d_b`, with
`N=sum_b d_b>=1`. Let `L(P)` be any rational linear map from the block
entries to `R^m`. Let `K` be a closed convex set with a polynomial-time
rational strong separation oracle and a known rational `rho_0>0` such
that `rho_0 B_2^m subset K`. Define

```
D=max{product_b det P_b: 0<=P_b<=I, L(P) in K}.
```

For rational `0<nu<=1`, a deterministic polynomial-time algorithm
returns rational positive definite feasible blocks with

```
product_b det P_b>=exp(-nu)D.                           (1)
```

No positivity assumption on `L` or symmetry assumption on `K` is
needed by this oracle. The block trace applications impose these
properties separately for their formulation-comparison proofs.

## Rational coordinates and a known interior ball

Represent each symmetric block by its independent upper-triangular
entries, concatenated into `u in R^q`, where
`q=sum_b d_b(d_b+1)/2`. The map `P(u)` satisfies

```
||P(u)-P(v)||_F<=sqrt(2)||u-v||_2<=2||u-v||_2.
```

Write `L(P(u))=C u` with rational `C`; off-diagonal coefficients in a
trace map include their factor two. Put `c=1+sum_ji |C_ji|`. Choose
`delta=2^(-b)<=1` so that `delta N c<=rho_0/4`. The block identity
allocation scaled by `delta` is feasible, hence `D>=delta^N`.
Because all capped eigenvalues are at most one, every eigenvalue of
an optimizer is at least `delta^N`.

Set

```
a=delta^N/4,
B_0=N(Nb+2)+4,
P_0=(delta/2)I,
t_0=-N(b+1)-2,
sigma=min{delta/(32N),rho_0/(8c),1/4}.
```

Here `I` denotes the block identity and `u_0` its scaled independent
coordinates. Consider the convex body

```
Q={(u,t): aI<=P_b(u)<=I for all b,
           C u in K,
           -B_0<=t<=sum_b log det P_b(u)}.              (2)
```

Its optimum last coordinate is `log D`. It contains the Euclidean ball
of radius `sigma` centered at `(u_0,t_0)`.

To check this, a coordinate perturbation of norm at most `sigma`
changes each block in operator norm by at most `2sigma`. Thus its
spectrum remains between `delta/4` and one, and above the lower cap
`a<=delta/4`. The image of the center has norm at most `rho_0/8`,
and its perturbation has norm at most `c sigma<=rho_0/8`.

The coordinate gradient of `sum log det P_b` consists of diagonal
entries of `P_b^(-1)` and twice its upper off-diagonal entries. On the
specified ball its norm is at most `8N/delta`. Its objective change is
therefore at most `1/4`. At the center the log determinant exceeds
`t_0` by at least two, and `sigma<=1/4` controls the last-coordinate
perturbation. Finally `t_0+B_0>=3`. These facts verify the inner ball.
An outer ball of radius `2(B_0+q+1)` with the same center is immediate
from the spectral caps and `-B_0<=t<=0`.

All constants and centers are rational with polynomial encoding length.
Positive definiteness and all matrix inverse/determinant operations
below involve rational matrices whose sizes and query encodings are
polynomially bounded.

## Weak separation and exact repair

Check the linear last-coordinate bounds first. The two spectral caps
have exact rational strong separators: rational symmetric elimination
either certifies a matrix positive semidefinite or supplies a rational
negative quadratic-form vector, as in the reviewed correlation-matrix
oracle. Pull any violated inequality for `C u in K` back to `u`; a
violated pulled-back normal cannot be zero because `0 in K`.

For a point passing these tests, evaluate

```
g(P)=sum_b log det P_b
```

to an interval of radius `eta/2`, with rational midpoint `g_hat`.
Each determinant is an exact positive rational, so only scalar
logarithm evaluation is needed. If `t>g_hat+eta/2`, use the rational
tangent inequality

```
t'<=g_hat+eta/2+sum_b tr[P_b^(-1)(P_b'-P_b)].            (3)
```

It is valid by concavity of log determinant and strictly separates the
query. Otherwise lowering `t` to `min(t,g(P))` certifies distance at
most `eta` from (2). The spectral lower caps imply
`g(P)>=N log a>-B_0`, so this vertical correction stays feasible.
The tangent normal has norm at least one through its last coordinate;
other strong normals can be normalized by their infinity norm.

This gives precisely the polynomial weak-separation interface used
in the scalar oracle's checked GLS theorem. Matrix inverses and
independent-coordinate tangent coefficients are exact rationals.
Scalar logarithms have polynomial conditioning because `P_b>=aI`.

Use the scalar lemma's central-ball repair with `B_0,sigma` above:
weakly optimize the last coordinate to tolerance

```
rho=nu sigma/[4(B_0+sigma+1)],
```

then return the rational point

```
y_f=[sigma y+rho(u_0,t_0)]/(sigma+rho).
```

The same convex-combination proof places `y_f` exactly in `Q`; its
last coordinate is at least `log D-nu`. The matrix blocks specified
by its first coordinates therefore satisfy (1). The algorithm uses
only polynomially many oracle calls and rational/scalar-function
operations of polynomial bit complexity.

This is an explicit convex-optimization implementation of an established
log-determinant objective. It makes no novelty claim for MAXDET or for
the general weak optimization theorem.

Both the [first proof audit](review-block-psd-unconditional-precision.md)
and [second proof audit](review-block-psd-unconditional-precision-second.md)
passed every matrix-coordinate, radius, separation, and repair step.
The checker `code/quadratic_rank/check_block_logdet_repair.py` passed
24 rational matrix repairs with exact feasibility and objective checks
and 100-digit log-determinant checks.
