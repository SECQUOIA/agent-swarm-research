# Second audit: diagonal PSD quadratic precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed candidate:
`notes/diagonal-psd-quadratic-linear-dimension-precision.md`.

## Verdict

**PASS.** The trace-allocation finite characterization and deterministic
rational construction are correct. The explicit constants
`A_r^tr<4r` and `p_out<=p_conv+5r+1` follow from the written
proof. No substantive correction was needed.

The diagonal condition is in the original cube coordinates, and all
diagonal quadratic coefficients are nonnegative. This audit does not
extend the theorem to an arbitrary rotated domain, indefinite diagonal
coefficients, or general output-error bodies. It also does not establish
literature priority.

## Removing affine coordinates

An inactive coordinate has zero quadratic coefficient in every output
and appears only through the affine terms. Subtract the full affine output
map, restrict the original formulation to its cube, and project to the
active coordinates. Every active cube point has an original cube preimage,
and the output errors are unchanged. Conversely, retain the inactive
coordinates continuously and restore the affine map by linear equations.

Thus the two formulation minima equal those of the active `r`-cube
without integer overhead. Unlike a rotated common-kernel quotient,
this domain is still exactly a cube and needs no volume normalization.
For `r=0`, the exact original affine graph is an LP.

## Trace covariance lower bound

The homogeneous quadratic part satisfies, within a parity support,

```
q_j(x-y)=(1/2)sum_i h_ji(x_i-y_i)^2<=4epsilon_j.
```

This is the correct factor: the vertical error at the midpoint of
two exact graph points is `q_j(x-y)/4`. Nonnegative diagonal
coefficients make this quantity nonnegative. Taking closures within the
compact cube preserves the inequality and covering property without
assuming the original convex lift is closed.

For independent uniform points on a compact positive-volume support,
`E[(X_i-Y_i)^2]=2Sigma_ii`. Therefore

```
E q_j(X-Y)=sum_i h_ji Sigma_ii<=4epsilon_j.
```

Every coordinate variance is at most one quarter. Hence
`p_i=Sigma_ii/4` is a feasible trace allocation, with cap in fact
at most one sixteenth. Positive support volume makes the covariance
positive definite, so its diagonal entries are positive.

The volume-covariance inequality followed by Hadamard gives

```
vol(S)<=omega_r(r+2)^(r/2) sqrt(det Sigma)
      <=omega_r(r+2)^(r/2) product_i sqrt(Sigma_ii)
      <=2^r omega_r(r+2)^(r/2) sqrt(D_tr).
```

The factor `2^r` is correct because each variance is four times
its allocation. Covering a unit-volume cube with at most `2^p`
parity supports proves the displayed finite lower bound. Zero-volume
supports need no covariance division and contribute nothing to the
volume sum. Unbounded general integer ranges do not affect the parity
argument.

The Gaussian ball bound gives

```
A_r^tr<=r+(r/2)log2[2pi e(1+2/r)].
```

For every integer `r>=1`, the bracket is at most `6pi e<64`.
Consequently this is strictly below `4r`, including the smallest
dimension. There is no hidden asymptotic qualification in that constant.

## Shared coordinate grid

For any positive feasible allocation, its cap ensures
`L_i=ceil((1/2)log2(1/p_i))>=0`. The residual width satisfies
`h_i^2<=p_i`. Binary prefixes represent every input coordinate,
including its upper endpoint.

The residual-square triangle contains the square graph and has absolute
error at most `h_i^2/4). Prefix squares and prefix-residual products
can be represented exactly using bounded products of the existing
binaries; no additional integer variables are needed. Sharing the
approximate square variables across outputs gives

```
|w_j-f_j(x)| <=(1/8)sum_i h_ji h_i^2
             <=epsilon_j/8.
```

There are no cross-coordinate quadratic terms, and positivity justifies
using the same linear budget to bound every absolute output error.
Setting all residual squares to their true values retains every exact
graph point.

The rounded-depth inequality
`sum_i L_i<=-(1/2)log2(product_i p_i)+r` is valid, including empty
prefixes. At an optimal allocation it proves the claimed finite
binary upper bound. Arbitrary real data are permitted for this finite
existence statement; the algorithmic statement separately requires
rational data.

## Convex allocation and global conditioning

Choose the feasible common dyadic allocation `delta=2^(-b)`.
Its exponent can be found with rational comparisons of the row sums,
and its magnitude is polynomial in input encoding length. At an
optimal allocation, `product_i p_i>=delta^r` and every `p_i<=1`.
Thus each `p_i>=delta^r`; in natural logarithms every optimum
coordinate lies in `[-rb log 2,0] subset [-R,0]`.

Each nonzero row branch of `h(u)` is a log-sum-exp with nonnegative
weights, and its gradient is a probability vector. Coordinate branches
have unit gradients; the zero branch has zero gradient. Hence `h`
is globally one-Lipschitz and convex, and
`F=-sum_i u_i+r h` is globally convex and at most
`sqrt(r)+r<=2r`-Lipschitz.

Its scaling repair makes every allocation feasible and gives exactly
`F(u)=-log(product_i exp(u_i-h(u)))`. Thus it never underestimates
the true optimal negative log product. At an optimal feasible allocation,
all penalty branches are nonpositive and `h=0`, so the minimum
over the chosen box is exactly `-log D_tr`.

The lower bound on a nonzero row sum,
`exp(-R)sum_i h_ji`, is valid uniformly on the box. Nonzero rational
row sums and positive tolerances have inverse-exponential-polynomial
size bounds. Scalar logarithms, exponentials, and normalized row gradients
therefore require only polynomial precision depth. Zero rows are correctly
omitted from logarithmic branches.

## Inexact iteration constants and rational arithmetic

The Euclidean box diameter is `sqrt(r)R<=D_bar=rR`. A reported
maximizing branch whose values have error at most `tau` is within
`2tau` of the true maximum. Multiplication by `r` gives
branch-value subgradient error `2r tau`. The prescribed approximation
error `nu` is for the full objective subgradient, so its inner-product
error against any feasible displacement is at most `D_bar nu`.

With the displayed constants, each contribution is `1/64`, making
the total at most `1/32`. The exact subgradient norm is at most
`2r`, and the small approximation error keeps it below `G_bar=3r`.

Euclidean projection onto the box is coordinate clipping and is
nonexpansive. The usual squared-distance recurrence with an
error-`e` subgradient telescopes over the actual iterates. Its initial
distance and step-norm contributions are each at most `1/32`;
the oracle contributes at most `1/32`. The average gap is therefore
at most `3/32`. Selecting the best objective reported to accuracy
`1/64` adds at most `1/32`, giving the claimed `1/8`.

No unstable trajectory comparison is needed. Approximate gradients can
be chosen on one fixed polynomial-bit dyadic grid. Since `eta` is
rational with a fixed integer denominator, all unprojected updates then
have a common denominator of polynomial bit length; clipping to the
integer endpoints `-R,0` preserves this property. Numerator magnitudes
are bounded by the box and one bounded step. More general choices with
polynomial bit precision per iteration also give polynomial total
encoding because the number of iterations is polynomial.

The scalar elementary-function routines and exact clipping therefore
implement the claimed iteration in polynomial bit time. There is no
implicit exact transcendental-arithmetic assumption.

## Exact rational repair and the final constant

Positive rational `q_i` can approximate `exp(u_i)` with the stated
logarithmic error because those exponentials are uniformly bounded
below by `exp(-R)`. The required absolute precision has polynomial
depth and can be chosen to preserve positivity.

The rational maximum `kappa` is exactly
`exp(h(log q))`; its definition uses only rational sums, ratios, and
comparisons. Thus `p=q/kappa` is exactly feasible, including its cap,
and has negative log product exactly `F(log q)`.

The Euclidean perturbation is at most `sqrt(r)/(32r^2)`. The global
Lipschitz bound loses at most `1/(16sqrt(r))<=1/16`. Together with
the iteration gap `1/8`, the total loss is at most `3/16`, which
is stronger than the safe bound one used in the note.

The resulting grid has binary count at most
`Phi_tr+r+1/(2 ln 2)`. Since
`Phi_tr<=p_conv+A_r^tr`, `A_r^tr<4r`, and
`1/(2 ln 2)<1`, this proves
`p_out<=p_conv+5r+1`. All depth decisions use exact squared rational
comparisons. The feasible common allocation bounds the benchmark by
`O(rb)`, making the total depth polynomial; the shared-prefix
construction and rational output equations consequently have polynomial
size and coefficient encoding.

