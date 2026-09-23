# Diagonal positive semidefinite quadratics admit O(r) precision overhead

Date: 2026-09-05. Status: independently reviewed theorem.

For nonnegative diagonal Hessians in the original box coordinates, a
trace allocation benchmark gives an additive `O(r)` characterization
and polynomial rational formulation construction. Here `r` counts the
coordinates occurring quadratically. This improves the general
`O(r log(r+1))` overhead on this structured family. It uses a different
benchmark, consistent with the existing Frobenius-benchmark obstruction.

## Finite statement

Consider rational or real quadratics on `[0,1]^n` of the form

```
f_j(x)=(1/2)sum_i h_ji x_i^2+a_j^T x+b_j,
h_ji>=0,       j=1,...,m,
```

with separate positive tolerances `epsilon_j`. Let `r` be the number
of indices `i` with some `h_ji>0`. All other coordinates enter only
through an affine map and can be kept as continuous variables. If
`r=0`, the exact graph is a linear formulation. For `r>=1`, index only
the active coordinates and define

```
D_tr=max{product_i p_i:
          0<=p_i<=1, sum_i h_ji p_i<=epsilon_j for all j},
Phi_tr=-(1/2)log2 D_tr,
A_r^tr=r+log2[omega_r(r+2)^(r/2)].
```

The determinant maximum is attained with all `p_i>0`, since a small
positive common value is feasible. The arbitrary-convex-lift and
binary-LP minima satisfy

```
max(0,Phi_tr-A_r^tr)<=p_conv<=p_bin<=Phi_tr+r.            (1)
```

The constant obeys `A_r^tr<4r`. For rational coefficients and
positive rational tolerances, a deterministic polynomial-time
algorithm constructs a rational MILP with

```
p_out<=p_conv+5r+1.                                     (2)
```

The output has polynomially many rows and variables in the full input
encoding. This is a complexity guarantee, not a practical runtime
claim. The active rank is explicit here; no domain rounding is needed.

## Positivity gives a trace covariance bound

Affine terms can be subtracted in the lifted output, as in the reviewed
input-quotient argument. The graph approximation problem therefore
reduces exactly, without extra integers, to the active `r`-cube.

For any parity support from an arbitrary convex lift, the quadratic
midpoint identity implies

```
0<=q_j(x-y)=(1/2)sum_i h_ji(x_i-y_i)^2<=4epsilon_j.
```

Let `Sigma` be the covariance of independent uniform points `X,Y` in
a positive-volume compact support. Taking expectations yields

```
sum_i h_ji Sigma_ii=E q_j(X-Y)<=4epsilon_j.
```

Also `Sigma_ii<=1/4`. Thus `p_i=Sigma_ii/4` is feasible for `D_tr`.
Hadamard's determinant inequality and the reviewed volume-covariance
bound give

```
vol(support)
 <=omega_r(r+2)^(r/2) sqrt(det Sigma)
 <=omega_r(r+2)^(r/2) product_i sqrt(Sigma_ii)
 <=2^r omega_r(r+2)^(r/2) sqrt(D_tr).
```

Covering the unit-volume cube by at most `2^p` parity supports proves
the lower bound in (1). No estimate of `lambda_max(Sigma)` is needed;
the diagonal covariance entries suffice because the Hessians are
nonnegative diagonal matrices.

The Gaussian bound `omega_r<=(2pi e/r)^(r/2)` gives

```
A_r^tr<=r+(r/2)log2[2pi e(1+2/r)]<4r.
```

## The original coordinate grid controls all outputs together

For any feasible positive allocation `p`, choose

```
L_i=ceil[(1/2)log2(1/p_i)],       h_i=2^(-L_i)<=sqrt(p_i).
```

Use `L_i` prefix binaries for coordinate `i`, leaving a continuous
residual in `[0,h_i]`. Represent the prefix square and prefix-residual
products exactly, and use the usual triangle for the residual square.
Its error is at most `h_i^2/4`. Since there are no quadratic cross
terms, every admitted output error satisfies

```
|w_j-f_j(x)| <= (1/8)sum_i h_ji h_i^2
              <=epsilon_j/8.
```

The same shared square variables represent every output. The model
contains every exact graph point. Its binary count is

```
sum_i L_i <=-(1/2)log2 product_i p_i+r.
```

At an optimal allocation this proves the upper bound in (1). The exact
prefix products can use the already reviewed recursive prefix gadget;
its size and all output equations are polynomial in the encoded input
and in the constructed binary count.

## Polynomial rational allocation: an elementary convex algorithm

The allocation problem maximizes `sum_i log p_i` under rational linear
constraints. For completeness, the following log-coordinate argument
keeps its bit-complexity conditioning explicit and needs no matrix
optimization.

Choose a feasible dyadic common allocation `delta=2^(-b)`, with `b>=0`
of polynomial encoding magnitude, by requiring
`delta sum_i h_ji<=epsilon_j` for every nonzero row. At an optimum,
`product_i p_i>=delta^r` and every `p_i<=1`, so `p_i>=delta^r`.
Let `R=rb+1`. The logarithms of an optimizer lie in `[-R,0]^r`.

For `u in R^r`, define

```
h(u)=max{0,max_i u_i,
         max_(j:sum h_ji>0) log[(sum_i h_ji exp(u_i))/epsilon_j]},
F(u)=-sum_i u_i+r h(u).
```

The maximum is convex: its row branches are log-sum-exp functions.
The map `p_i=exp(u_i-h(u))` is feasible and has negative log product
`F(u)`. Therefore the minimum of `F` on `[-R,0]^r` is exactly
`-log D_tr`. Its subgradients have norm at most `sqrt(r)+r<=2r`.
Each row-branch gradient is a nonnegative vector summing to one.

Here is one explicit polynomial inexact scheme. Set `D_bar=rR`,
`G_bar=3r`, `eta=1/(16G_bar^2)`, and
`T=ceil(16D_bar^2/eta)`. Start at `u_0=0`. At each step evaluate the
branches with absolute error at most `tau=1/(128r)`, choose a maximizing
estimated branch, and approximate the resulting full `F` subgradient
with Euclidean error at most `nu=1/(64D_bar)`. Update by

```
u_next=clip_[-R,0]^r(u-eta g).
```

Choose the approximate gradients on a common dyadic grid with a
sufficient polynomial number of bits. All stored iterates are rational;
clipping is exact rational arithmetic. The chosen vector has norm at most
`G_bar`, and its approximate subgradient error on this box is at most

```
e=2r tau+D_bar nu<=1/32.
```

The elementary projected-subgradient recurrence, summed over the `T`
steps, bounds the mean objective gap by

```
D_bar^2/(2eta T)+eta G_bar^2/2+e<=3/32.
```

Evaluating each objective to accuracy `1/64` and retaining the best
estimated value therefore returns `u` with gap at most `1/8`.
On the box, every nonzero row sum is at least
`exp(-R)sum_i h_ji`, so all logarithms and normalized gradients have
inverse-exponential-polynomial conditioning. Scalar exponential and
logarithm evaluation to the requested accuracy has polynomial bit
complexity, as in the reviewed construction's scalar-function bounds.
The step count and rational encoding lengths are polynomial as well.

Choose positive rational `q_i` approximating `exp(u_i)` with
`|log q_i-u_i|<=1/(32r^2)`. Define the exactly rational upper repair

```
kappa=max{1,max_i q_i,max_j [(sum_i h_ji q_i)/epsilon_j]},
p_i=q_i/kappa.
```

The allocation `p` is exactly feasible. Since `F` is `2r`-Lipschitz,
its negative log product is at most

```
F(log q)<=F(u)+2r sqrt(r)/(32r^2)
        <=-log D_tr+1.
```

Thus `product_i p_i>=exp(-1)D_tr`. The rational grid has at most
`Phi_tr+r+1/(2ln2)` binaries. Combined with (1) and `A_r^tr<4r`, this
proves (2). Dyadic grid depths are computed by exact rational square
comparisons, and all grid coefficients have polynomial encoding length.

## Scope and open boundary

The diagonal condition is in the original box coordinates (or in a
signed permutation of them). Pairwise commuting PSD Hessians in an
arbitrary rotated eigenbasis do not automatically satisfy this condition:
the rotated domain can create an additional covering problem. Similarly,
positivity is essential to the trace lower bound and to controlling all
square errors by nonnegative sums.

The [Frobenius dimension-gap example](../notes/covariance-benchmark-dimension-gap.md)
is already a diagonal PSD example. It does not contradict (1): for
`H=I`, `epsilon=1`, the new trace benchmark is
`Phi_tr=(r/2)log2 r`, whereas the old squared-energy benchmark was
`(r/4)log2 r`.

The ordinary scalar allocation problem and coordinate interpolation are
established tools. Existing logarithmic square approximations and shared
SOS2 formulations for multiple univariate outputs are particularly close
upper-construction antecedents. The proposed refinement is the simultaneous
trace covariance lower bound giving an `O(r)` finite characterization
against arbitrary convex lifts, with a rational compact construction.
The [source and novelty assessment](../notes/diagonal-psd-quadratic-precision-novelty.md)
credits those predecessors and found no matching whole-formulation theorem
in its bounded search; publication priority remains unestablished.

The [first proof audit](../notes/review-diagonal-psd-quadratic-precision.md)
and [second proof audit](../notes/review-diagonal-psd-quadratic-precision-second.md)
both passed, including the finite constants, the scalar inexact algorithm,
and the exact rational feasibility repair.

The [positive separable polynomial extension](positive-separable-polynomial-integer-precision.md)
retains `O(r)` overhead for fixed degree and gives
`O(r+sum_i log(D_i))` for growing dense degrees, using a power-coordinate
lower bound and shared rational prefix powers.

The [unconditional-error-body extension](positive-separable-unconditional-error-precision.md)
retains these dimension bounds for whole monotone norm budgets, using
`Cp in K` directly in the allocation and rational output rectangles.

The [block PSD extension](block-psd-quadratic-precision.md) allows
noncommuting Hessians within original coordinate blocks. Its overhead
is `O(sum_b r_b log(r_b+1))`, so uniformly bounded block ranks also
give a linear total-rank overhead.
