# Second review: block PSD quadratic precision

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed note: `notes/block-psd-quadratic-precision.md`.
Verdict: **PASS** for the finite bounds, polynomial rational construction,
and refinement by individual common block ranks.

This is an independent correctness review, including the transfer of the
previously reviewed bit-complexity proof. It does not establish publication
priority or practical running time.

## Finite lower bound

For `f_j(x)=(1/2)x^T H_j x+affine`, the midpoint error is
`(1/8)(x-y)^T H_j(x-y)`. Each `H_j` is PSD, so this is nonnegative.
Two independent uniform points in a compact parity support therefore give

```
sum_b tr(H_jb Sigma_bb)<=4 epsilon_j.
```

The block-direction variance bound is
`Sigma_bb<=(d_b/4)I`, because a unit direction has range at most
`sqrt(d_b)` on that block's cube. For
`c_b=max(4,d_b/4)` and `P_b=Sigma_bb/c_b`, the spectral caps hold.
Since every trace summand is nonnegative and each `c_b>=4`,

```
sum_b tr(H_jb P_b)
 <=(1/4)sum_b tr(H_jb Sigma_bb)<=epsilon_j.
```

The block determinant inequality is applicable to any PSD covariance;
positive-volume supports have positive definite covariance, and singular
cases follow by continuity. It gives

```
det Sigma <= product_b det Sigma_bb
           <= product_b c_b^(d_b) D.
```

Combining this with the established volume-covariance estimate proves the
displayed support-volume bound and the parity-cover lower bound. Compact
closures of the parity supports preserve the midpoint inequality, as in
the base result, so measurability or closure of the initial lift is not
required. The global volume constant has logarithm `O(N)`; the logarithmic
block-size terms arise only from the `c_b` factors.

## Block grids and trace error control

For an orthogonal basis within block `b`, the exact coordinate width on
the rotated cube is its column's absolute-coordinate sum. This lies in
`[1,sqrt(d_b)]`. The dyadic depth can thus be chosen as

```
L_i=ceil(log2(w_i sqrt(d_b/lambda_i)))>=0,
h_i=w_i 2^(-L_i)<=sqrt(lambda_i/d_b).
```

The standard shared square and residual-product LPs give a symmetric
matrix of monomial errors whose `(i,k)` entry has magnitude at most
`h_i h_k/4`. After division by `sqrt(lambda_i lambda_k)`, each entry
of `Z_b` has magnitude at most `1/(4d_b)`, and its operator norm is
at most its maximum absolute row sum, hence at most `1/4`.

For the transformed PSD Hessian `M_jb`, the semidefinite inequalities
`-(1/4)I<=Z_b<=(1/4)I` imply
`|tr(M_jb Z_b)|<=tr(M_jb)/4`. Including the quadratic factor `1/2`
gives the claimed total error at most `epsilon_j/8`. The same residual
monomials are shared among the outputs; commutation of their Hessians is
never used. Original cube inequalities remain in the formulation through
the blockwise coordinate identities.

Summing the depths gives exactly the stated upper constant
`N+sum_b d_b log2 d_b` above the determinant benchmark. Blockwise
binary-continuous products and residual envelopes have polynomially many
rows and coefficients relative to the input and the constructed count.

## The full rational optimization proof transfers

I compared the proposed substitutions with the complete reviewed
`results/quadratic-weighted-precision-polynomial-construction.md` and its
rational Jacobi appendix, rather than treating matrix functions as
unit-cost exact operations.

On a block geodesic `P_b(t)=P_b^(1/2) exp(tA_b) P_b^(1/2)`, each trace
energy is a sum of exponentials with nonnegative coefficients: diagonalize
each `A_b` and use the nonnegative diagonal entries of the congruence of
`H_jb`. Every nonzero energy is positive. Its logarithm is therefore
geodesically convex. Its tangent-coordinate gradient blocks are precisely

```
M_jb/E_j(P),       M_jb=P_b^(1/2) H_jb P_b^(1/2).
```

There is no factor `1/2` in this gradient. These blocks are PSD and the
sum of their traces is one. Their joint Frobenius norm is at most one.
The spectral-cap branches have the same bound. Consequently the exact
penalty has global Lipschitz constant at most `N+sqrt(N)<=2N`.

Uniform scaling by `exp(-h(P))` multiplies trace energies by that factor
and the product determinant by its `N`th power. Thus `F` is exactly the
negative log determinant of a feasible repair, and its global minimum
equals the desired negative log determinant. This verifies both the
changed homogeneity and the absence of an unknown penalty parameter.

A dyadic feasible `delta I` yields `det P_star>=delta^N`. The spectral
caps imply every optimizer eigenvalue is at least `delta^N` and the sum
of its negative log eigenvalues is at most `-N log delta`. Hence the same
polynomial metric-radius bound applies. The product of block cones is
totally geodesic in the full SPD cone: inverse square roots, exponentials,
logarithms, and geodesics preserve the blocks. The identity-centered radial
projection also remains in this product. The curvature, projection, and
one-step comparison estimates used in the earlier proof consequently
restrict to this setting without a changed dimension factor.

More explicitly, one may use the earlier `R,D,Z,eta,T,xi` and oracle
accuracy choices with `n=N`. For a selected branch, approximate its whole
product-space gradient to `nu/N`, so the resulting objective subgradient
has error at most `nu`. Its inexact inequality has error at most
`2N tau+D nu`, with the same constant-factor allowance for an approximate
largest-eigenvalue Rayleigh branch. Rounding each block symmetrically to
dyadic entries at the earlier full-matrix accuracy keeps the stored matrix
block diagonal, positive definite, and within the enlarged metric ball.

The necessary conditioning estimate is

```
E_j(P)>=exp(-(R+1)) E_j(I).
```

For a nonzero rational PSD input, `E_j(I)>0` is a rational number of
polynomial encoding length. All normalized trace gradients and energy logs
therefore have the required inverse-exponential-polynomial denominator
bounds. Matrix-function approximation and rational near-Rayleigh vectors
use exactly the earlier residual Jacobi routine; neither a spectral gap
nor commuting input Hessians is required.

For clarity, the final repair uses the changed exact expression

```
kappa=max(1,max_b lambda_max(P_b),max_j E_j(P)/epsilon_j).
```

The trace ratios are rational and exactly evaluable. Certified rational
upper eigenvalue estimates produce a rational upper bound on `kappa`
within relative factor `exp(1/(4N))`. Dividing all blocks by that bound
is exactly feasible and loses at most `1/4` in log determinant. Combined
with the earlier inexact iteration margin, this gives determinant at least
`exp(-1)D`. The magnitude and minimum-eigenvalue bounds needed for the
subsequent spectral routine remain exponential-polynomial.

Applying rational Jacobi separately to the blocks gives exactly rational
orthogonal bases and rational grid covariances satisfying
`P_b/8<=P_tilde_b<=P_b/2`. Trace feasibility is monotone under PSD order,
and the total determinant loss is at most `N log 8`. The extra binary
count is thus `O(N)`. Exact rational comparisons determine all depths;
the original input, trace computations, transformed coefficients, and
binary product bounds all retain polynomial bit length. This establishes
the claimed reuse of the full bit proof.

## Block common-kernel quotients preserve the relevant minima

For each original block, choose rational full-row-rank `U_b` spanning the
rows of its Hessians and the rational right inverse
`F_b=U_b^T(U_b U_b^T)^(-1)`. Then

```
H_jb=U_b^T G_jb U_b,       G_jb=F_b^T H_jb F_b>=0.
```

The reduced coordinates `z_b=U_b(x_b-(1/2)1)` have domain the product
of the centered block zonotopes. The product property follows from the
disjoint original input coordinates. Subtracting the original affine
output map before projection preserves every admitted error, even when
that map varies along a quotient fiber. Imposing the original cube before
projection, and reinstating it in the reverse lift, proves equality of
both arbitrary-convex and binary-LP formulation minima. No integer is added
in either direction.

Apply the already reviewed rational zonotope rounding separately to each
nonzero block. Its rational coordinate normalization preserves PSD by
congruence and preserves block structure. The resulting product domain is
compact and convex, lies in the reduced cube, and has volume at least

```
product_(b:r_b>0) [2r_b(r_b+1)]^(-r_b).
```

The finite covariance lower bound still applies on this domain with the
same cube-based caps. Its parity supports cover `vol(Omega)`, so the sole
change is the additive term `log2 vol(Omega)` in that lower bound. The
upper construction runs on the containing cube and is then restricted by
the exact rational original-variable domain lift. These operations compare
the same transformed Hessian benchmark, so no equality between optima on
different domains is presumed.

After summing the volume loss, finite constants, and rational-construction
loss, the overhead is `O(sum_(b:r_b>0) r_b log(r_b+1))`, with a universal
constant. Blocks of rank zero are affine and require no integers; if all
ranks vanish, the entire graph has an exact LP. Original block sizes and
output counts remain in runtime and continuous size, but not in the
asserted additive integer-count term. No unresolved mathematical or
encoding issue was found.

I also inspected and reran `code/quadratic_rank/check_block_psd_precision.py`.
All 36 exact rational cases passed the block determinant, covariance cap,
trace allocation, and shared PSD residual bounds. The checker uses exact
principal-minor tests for its matrix inequalities. These checks supplement
the proof; they do not implement the imported matrix optimizer or the
classical domain-rounding algorithm.
