# Block positive semidefinite quadratics have block-size precision overhead

Date: 2026-09-05. Status: independently reviewed structural extension.

A common partition into small positive semidefinite quadratic blocks
reduces the additive integer-count overhead to the block dimensions.
The Hessians may fail to commute within each block. Fixed block size
therefore retains a linear, rather than dimension-times-log-dimension,
additive guarantee.

## A finite block covariance law

Let rational or real quadratics on `[0,1]^N` have a common coordinate
partition into blocks of sizes `d_1,...,d_B`, with

```
H_j=diag(H_j1,...,H_jB),       H_jb>=0,
```

and arbitrary affine terms. Require separate errors
`|w_j-f_j(x)|<=epsilon_j`, where all tolerances are positive. Blocks
with no quadratic term at all may be removed after affine output
subtraction. Define

```
D=max{product_b det P_b:
       0<=P_b<=I_(d_b),
       sum_b tr(H_jb P_b)<=epsilon_j for every j},
Phi=-(1/2)log2 D,
c_b=max{4,d_b/4},
A=log2[omega_N(N+2)^(N/2)]+(1/2)sum_b d_b log2 c_b,
B_grid=N+sum_b d_b log2 d_b.
```

Then

```
max(0,Phi-A)<=p_conv<=p_bin<=Phi+B_grid.                 (1)
```

For rational input, a deterministic polynomial-time algorithm gives a
rational MILP with

```
p_out<=p_conv+O(sum_b d_b log(d_b+1)).                  (2)
```

The implicit constant is universal, independent of the number of
outputs, coefficients, and tolerances. All size and time bounds are
polynomial in the full encoded input. This does not claim a practical
running time.

## Lower bound by block covariance and positivity

For a positive-volume compact parity support, let `Sigma` be its full
`N` by `N` covariance. Positivity of every quadratic output and the
midpoint identity give

```
sum_b tr(H_jb Sigma_bb)<=4epsilon_j.
```

Also `Sigma_bb<=(d_b/4)I`: every unit-direction variance is bounded
by one quarter of its squared range on the `d_b`-cube, at most `d_b/4`.
Thus `P_b=Sigma_bb/c_b` is feasible. Indeed, the caps hold and
`c_b>=4` yields the trace constraints.

The block determinant inequality gives
`det Sigma<=product_b det Sigma_bb`. It follows either by iterating
Schur complements of a positive definite covariance matrix, or by
continuity for a singular one. Combining it with the usual
volume-covariance inequality bounds every support's volume by

```
omega_N(N+2)^(N/2) [product_b c_b^(d_b/2)] sqrt(D).
```

The parity cover proves the lower half of (1). The global factor
`omega_N(N+2)^(N/2)` is `exp(O(N))`; only the block caps introduce
logarithms of block dimensions.

## The grid rotates and shrinks only within blocks

Diagonalize each feasible covariance block as
`P_b=U_b diag(lambda_b) U_b^T`. Every rotated coordinate of the
`d_b`-cube has width `w_i<=sqrt(d_b)`. Choose its residual grid width
at most `sqrt(lambda_i/d_b)`. The resulting number of prefix binaries
is at most

```
-(1/2)log2 product_b det P_b +sum_b d_b log2 d_b+N.
```

For each block the shared symmetric residual error matrix `Z_b`, in
the normalized coordinates, has entries bounded by `1/(4d_b)`.
Hence `||Z_b||_2<=1/4`. The transformed Hessian

```
M_jb=diag(sqrt(lambda_b)) U_b^T H_jb U_b
       diag(sqrt(lambda_b))
```

is positive semidefinite, with trace `tr(H_jb P_b)`. The output error
from this block is `(1/2)tr(M_jb Z_b)`, so

```
|w_j-f_j(x)|
 <=(1/8)sum_b tr(H_jb P_b)<=epsilon_j/8.
```

This uses the elementary inequality `|tr(MZ)|<=tr(M)||Z||_2` for
`M>=0`, obtained by diagonalizing `Z` or by its two semidefinite bounds.
No common eigenbasis for the Hessians is required. The exact prefix
and shared residual product construction is the reviewed quadratic
grid applied separately within each block. It proves the upper half
of (1), with polynomially many rows relative to the constructed count.

## Polynomial covariance construction reuses the reviewed bit proof

The displayed determinant problem is already a convex optimization
problem: its objective is a concave log determinant and its constraints
are linear traces and semidefinite caps. The following explicit
reduction also reuses the reviewed polynomial rational covariance
algorithm without importing an unspecified exact optimizer.

Work on the product of the positive definite block cones and set

```
E_j(P)=sum_b tr(H_jb P_b),
h(P)=max{0,max_b log lambda_max(P_b),
         max_(j:E_j(I)>0) log(E_j(P)/epsilon_j)},
F(P)=-sum_b log det P_b+N h(P).
```

The repair `P_b ->exp(-h(P))P_b` is exactly feasible and has negative
log determinant `F(P)`. On a block geodesic, every nonzero trace energy
is a sum of exponentials with nonnegative coefficients, since each
`H_jb` is positive semidefinite. Thus its logarithm is geodesically
convex. Its normalized tangent-gradient blocks are

```
P_b^(1/2) H_jb P_b^(1/2)/E_j(P).
```

They are positive semidefinite and their total trace is one, so their
joint Frobenius norm is at most one. Cap branches have the same bound.
Consequently `F` has the same global `2N` Lipschitz bound as the
reviewed construction, with `N` replacing its input dimension.

A feasible common dyadic covariance satisfies
`delta E_j(I)<=epsilon_j`. It has polynomial-bit exponent, and the
optimizer determinant is at least `delta^N`. Every eigenvalue of an
optimizer is therefore at least `delta^N`, giving the same polynomial
radius bound. The block diagonal cone is a totally geodesic subspace
of the full positive definite cone: geodesics, logarithms, exponentials,
and identity-centered radial projections all preserve its blocks.
The earlier curvature and inexact iteration bounds thus apply directly.
Numerical routines operate on the blocks separately and preserve every
off-block zero exactly.

The only changed scalar energy is linear in `P` rather than quadratic.
On the bounded iterate region,

```
E_j(P)>=lambda_min(P) E_j(I).
```

Nonzero `E_j(I)` is a positive rational of polynomial encoding length,
so the log and normalized-gradient conditioning is at least as simple
as before. Zero energies are omitted. The existing rational matrix
function approximations and oracle error allocations therefore produce
an exactly feasible rational block covariance with determinant at least
`exp(-1)D` after upper-bound scaling repair.

Apply the exact rational Jacobi residual construction to each block.
The resulting rational grid covariance satisfies
`P_b/8<=P_tilde_b<=P_b/2`. It preserves trace feasibility and loses at
most `N log 8` in log determinant. The exactly orthogonal rational
basis in each block retains rotated widths at most `sqrt(d_b)`. Thus
the additional count is `O(N)`, proving (2). This reuses the full
[polynomial covariance proof](../results/quadratic-weighted-precision-polynomial-construction.md)
and its separately audited spectral appendix; it is not a claim that
real-arithmetic matrix operations alone establish bit complexity.

## Removing common kernels within blocks

For block `b`, let

```
r_b=rank [H_1b; H_2b; ...; H_mb].
```

Then a stronger intrinsic guarantee is

```
p_out<=p_conv+O(sum_(b:r_b>0) r_b log(r_b+1)).           (3)
```

Use the exact common-kernel quotient from the
[input-rank theorem](../results/quadratic-nonlinear-input-rank-precision.md)
separately on each original block. Positive semidefiniteness is preserved
under its rational congruences. The projected original cube is a product
of centered zonotopes of dimensions `r_b`, because the original blocks
have disjoint input coordinates.

Round and rationally normalize each nontrivial zonotope separately as
in that theorem. The normalized domain is a product
`Omega=product_b Omega_b subset [0,1]^r`, where `r=sum_b r_b`, and

```
vol(Omega_b)>=[2r_b(r_b+1)]^(-r_b).
```

The output Hessians remain block diagonal PSD after these blockwise
affine coordinate changes. Run the construction for the containing
cube. In the lower bound the parity supports cover `vol(Omega)` rather
than one, adding the loss

```
-log2 vol(Omega)<=sum_b r_b log2[2r_b(r_b+1)].
```

Every other term is given by (1)--(2) with block sizes `r_b`. Restoring
the original cube variables supplies an exact rational linear lift of
the product domain and preserves the formulation minimum, including
arbitrary affine fiber terms. This proves (3). If every nonzero block
rank is at most `s`, the overhead is `O(r log(s+1))`; it is `O(r)` for
fixed `s`, even when original block sizes and ambient dimension grow.

## Scope and novelty boundary

Blocks refer to disjoint original input coordinates. There may be many
outputs, and their matrices need not commute inside a block. Positivity
and the common block structure are used explicitly in the trace lower
bound and the residual-error bound. A single block recovers an
`O(r log(r+1))` guarantee; rank-one blocks give linear overhead.

The ingredients are block determinant inequalities, matrix trace
allocation, and the already reviewed rational quadratic construction.
The proposed structural conclusion is the dependence of near-minimal
integer dimension on the individual common block ranks. The
[source and novelty assessment](../notes/block-psd-quadratic-precision-novelty.md)
credits classical MAXDET, Fischer determinant inequalities, and existing
Hessian-connected-component decompositions. Arbitrary blocks created by
copy variables do not meet this theorem's original independent-domain
assumption. No matching whole-formulation theorem was found in the
bounded search; publication priority remains unestablished.

The [first proof audit](../notes/review-block-psd-quadratic-precision.md)
and [second proof audit](../notes/review-block-psd-quadratic-precision-second.md)
both passed, including the full rational bit-proof adaptation and the
blockwise quotient/domain comparison. The checker
`code/quadratic_rank/check_block_psd_precision.py` passed 36 exact block
determinant, covariance cap, trace allocation, and noncommuting PSD
residual-error cases. The second reviewer independently reran it.

The [unconditional-budget extension](block-psd-unconditional-error-precision.md)
retains the same individual-block-rank bound under whole monotone error
bodies and supplies a direct Euclidean log-determinant solver.

The [forest-Laplacian refinement](forest-laplacian-quadratic-precision.md)
gives linear overhead for positive squared differences on a common forest,
even with a single large connected original-coordinate block. Its exact
incidence-domain volume controls the correlation introduced by the quotient.
