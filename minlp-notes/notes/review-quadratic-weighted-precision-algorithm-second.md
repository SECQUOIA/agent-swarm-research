# Second audit: computing the quadratic precision benchmark

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed candidate: `notes/quadratic-weighted-covariance-algorithm.md`.

## Review status

**PASS after revision.** The geometric optimization argument, polynomial-bit
implementation, and conversion from a near-optimal covariance to a compact
rational formulation pass independent review. I read the revised main
candidate and its supporting `notes/rational-jacobi-matrix-functions.md`.
The initial draft left its polynomial-bit spectral computation as an
unproved import. The explicit rational Jacobi construction, independently
derived by the author and this reviewer, closes that issue as detailed
below. No substantive unresolved mathematical gap remains.

Two minor corrections were requested and applied: the approximation error `nu` must
bound the full objective subgradient `G`, so the chosen component
gradient must be approximated to `nu/n`; and rational formulation output
requires the affine coefficients of each quadratic to be rational too.
These do not change the algorithm or claimed asymptotic bound.

This audit concerns correctness and polynomial bit complexity, not
priority or practical running time. The iteration bound is a potentially
large polynomial, and no strongly polynomial algorithm is asserted.

## Exact penalty, radius, and geometry

For positive definite `P`, scaling it by `exp(-h(P))` makes both its
spectral cap and every quadratic energy constraint feasible. The energy
is homogeneous of degree two in `P`, while its determinant is homogeneous
of degree `n`. Thus `F(P)` is exactly the negative log determinant of
the scaled feasible covariance. Its global minimum is the desired
negative log determinant; there is no unknown penalty parameter.

The zero branch, spectral-cap branch, and energy branches of `h` are
geodesically convex. For the spectral branch, each fixed-vector Rayleigh
logarithm restricts to a log-sum-exp along a positive definite geodesic,
and taking their supremum preserves convexity. The energy log-sum-exp
identity is already established in the twice-reviewed finite result.
The negative log determinant is geodesically affine.

I independently differentiated the energy. If
`M=P^(1/2) H P^(1/2)`, the isometric gradient of `(1/2)log E(P)` is
`M^2/tr(M^2)`, with no missing factor two. It is positive semidefinite
with trace one and Frobenius norm at most one. The displayed gradient
for a fixed Rayleigh logarithm has the same properties. Consequently
`h` is globally one-Lipschitz and `F` is `(n+sqrt(n))`-Lipschitz.

The rationally chosen covariance `2^(-b)I` gives a positive determinant
lower bound. At an optimal covariance, every eigenvalue is at most one,
so the Euclidean norm of its vector of logarithms is bounded by the sum
of their absolute values, and hence by `nb log 2`. This proves the
polynomial metric-radius bound without imposing a spectral lower bound
on all feasible covariances.

The positive definite cone with the stated metric is Hadamard. Its
curvature lower bound `-1/2` is explicitly given by Proposition I.1,
printed page 71, of the linked Criscitiello--Boumal manuscript; I checked
the primary source. The weaker `-1` used in the candidate is valid.
The closed metric ball is convex, and its radial projection formula
follows by equality in the reverse-triangle lower bound along its radial
geodesic. Projection onto a closed convex subset of a Hadamard space is
nonexpansive. [Criscitiello and Boumal](https://arxiv.org/pdf/2008.02252).

I also inspected Zhang--Sra Corollary 8 and the proof of Theorem 9.
The candidate uses their one-step comparison inequality and telescoping
argument, with the stated curvature factor bounded by `1+D`. These are
established algorithmic ingredients. [Zhang and Sra](https://proceedings.mlr.press/v49/zhang16b.pdf).

## Inexact optimization and error accounting

An error-`e` subgradient at the current rational iterate is sufficient;
the oracle need not reproduce a subgradient chosen by a hypothetical
exact trajectory. The norm of the target-point logarithm in isometric
coordinates is the metric distance, at most `D`. Thus full-subgradient
error `nu` adds at most `D nu` to the subgradient inequality. A branch
whose value is below the maximum by at most `2 tau` adds at most
`2n tau`. Approximating the Rayleigh maximum with a near-maximizing
fixed rational vector adds one more controlled branch-value error,
absorbed by decreasing `tau` by a constant factor.

The sign of the displayed inexact subgradient inequality is correct for
the exponential update with tangent `-eta G`. The conceptual unrounded
update can lie outside the ball; the comparison inequality uses its
geodesic step, and subsequent metric projection cannot increase its
distance to the optimum. Rounding within metric distance `xi` changes
the squared distance by at most `2D xi+xi^2`, because both the exact
projected point and the optimum lie in the radius-`R` ball.

The resulting recurrence telescopes on the actual stored iterates.
Starting at `I`, its initial distance is at most `D`. With the displayed
choices of `eta,T,e,xi`, the initial-distance term and curvature term
are each at most `1/32`, the oracle term is at most `1/32`, and the
rounding term is below `1/64`. Selecting the least reported objective
among evaluations accurate to `1/64` adds at most `1/32`. The resulting
gap is strictly below `1/2`, as needed before the final feasibility
scaling. This proof does not multiply rounding errors across iterations.

If an entrywise approximation to a positive definite matrix of least
eigenvalue `a` has operator error at most `a u`, its relative eigenvalues
lie between `1-u` and `1+u`. For `u<=1/2`, their logarithms have absolute
value at most `2u`, proving the stated metric-error bound. This both
certifies positivity and keeps each stored iterate in the enlarged ball.

## Explicit deterministic rational spectral routine

Here is a sufficient elementary implementation, requiring no spectral
gap or selection of a distinguished eigenvector. Given rational symmetric
`A`, a positive rational bound `M>=||A||_F`, and desired positive rational
off-diagonal tolerance `delta<M`, maintain exact rational matrices

```
A=Q B Q^T,    Q^T Q=I.
```

Start with `Q=I,B=A`. The cases `n=1` and already diagonal matrices need
no rotations. Otherwise set `N=n(n-1)` and choose an off-diagonal entry
of largest magnitude. An exact Jacobi rotation would remove that entry
and its transpose. Writing `s` for the Frobenius norm of the off-diagonal
part, its new off-diagonal norm is at most

```
sqrt(1-2/N) s <= (1-1/N) s.
```

Approximate the rotation angle's half-angle tangent by a rational `t`
and use

```
c=(1-t^2)/(1+t^2),    s_rotation=2t/(1+t^2).
```

This rotation is exactly rational and orthogonal. Choose it within
operator distance `delta/(8NM)` of the ideal rotation. Conjugation by
the two orthogonal rotations then differs in Frobenius norm by at most
`delta/(4N)`. As long as the current off-diagonal norm exceeds `delta`,
the actual next norm is therefore at most

```
(1-1/N)s + delta/(4N) <= (1-3/(4N))s.
```

It follows that `O(n^2 log(M/delta))` rotations suffice. Stopping and
largest-entry selection use exact rational squared comparisons.

The ideal angle can be chosen in `[-pi/4,pi/4]`. Its tangent follows
from the standard two-by-two diagonalization using arithmetic and a
square root. While rotation is necessary, the chosen pivot has magnitude
at least `delta/sqrt(N)`, so the needed divisions have inverse bounded
by a polynomial in `n,M,1/delta`. Its half-angle tangent is bounded
in magnitude by one, and rational bisection of the square roots gives
the required precision with `poly(log M,log(1/delta),n)` bits. A zero
pivot is never used.

No matrix rounding is needed inside this spectral subroutine. Maintain
a common denominator for `B` and for `Q`. A rotation whose entries have
`k` bits adds only `O(k)` denominator bits to one exact update. Since
the number of rotations and `k` are polynomial, every intermediate
numerator and denominator has polynomial bit length. Orthogonality
preserves the matrix norm, which bounds numerator magnitudes once the
denominator is fixed. Thus exact rational matrix arithmetic has polynomial
bit cost. This avoids an unjustified unit-cost algebraic-number model.

At termination, `C=Q diag(B) Q^T` satisfies `||A-C||_F<=delta` and
`Q` is exactly rational orthogonal. Its diagonal entries are rational
Rayleigh quotients. In particular, for positive definite `A>=aI`, every
one is at least `a`. The column associated with the largest diagonal
entry has Rayleigh quotient within `delta` of `lambda_max(A)`. Repeated
or arbitrarily close eigenvalues do not affect any of these guarantees.

## Matrix functions and precision lengths

Matrix functions can now be evaluated on the exactly diagonalizable
nearby matrix `C`, with scalar functions approximated rationally. Their
errors relative to the original matrix are controlled without matching
its individual eigenvectors. For symmetric arguments, the derivative
of the matrix exponential gives Frobenius error at most `exp(K)` times
argument error when the argument norms are at most `K`. The integral
representation of the logarithm gives Lipschitz constant `1/a` on
matrices bounded below by `aI`. The square-root Sylvester equation gives
constant `1/(2sqrt(a))`; inversion has constant at most `1/a^2`.
Compositions give sufficient bounds for inverse square roots as well.

Scalar square roots are obtained by rational bisection. For logarithms,
reduce by an exact power of two to `[1,2]` and use the convergent series
in `(z-1)/(z+1)`, whose magnitude is at most `1/3`; the same series gives
`log 2`. For exponentials on `[-K,K]`, a Taylor truncation of degree
polynomial in `K` and the desired precision depth suffices. All scalar
arguments and intermediate results here have logarithmic magnitude
bounded by a polynomial in the original input length.

The radial projection may be evaluated as
`exp(t log Q)` with `t=R/max(R,||log Q||_F)`. Its scalar denominator is
at least `R>=1`, so neither a repeated eigenvalue nor `Q` close to `I`
causes an unstable division. The exact intermediate update has spectral
logarithms bounded by `R+1+3n eta`, and every nonzero energy denominator
is bounded below by `exp(-2(R+1))||H_j||_F^2`. A nonzero rational input
coefficient is at least an inverse power of two with polynomial exponent.
These estimates make all required absolute accuracies inverse powers of
two with polynomial exponents. Each outer iterate is rounded to a fresh
dyadic matrix, preventing symbolic denominators from accumulating over
all outer iterations.

## Feasibility repair and rational formulation

The exact energies of the selected rational iterate are rational. The
Jacobi residual bounds give certified upper bounds for its largest
eigenvalue, and scalar bisection gives certified upper bounds for the
square roots of its energies. They produce a rational `kappa_bar`
between `kappa` and `kappa exp(1/(4n))`. Dividing by it makes all
covariance constraints exactly feasible and loses at most `1/4` in
log determinant. No floating-point feasibility assertion is needed.

For a concrete conditioning bound, the radius and choice of `b` give
`kappa <= exp(R+1)2^b`. Together with the least eigenvalue of the stored
iterate, this yields an explicit exponential-polynomial lower bound on
the repaired covariance's least eigenvalue. Consequently the final
Jacobi tolerance required below has polynomial precision depth.

Apply the rational spectral routine to the repaired covariance with
off-diagonal tolerance at most half a known positive lower eigenvalue
bound. Set `lambda_tilde_i=B_ii/4` and
`P_tilde=Q diag(lambda_tilde) Q^T`. Then

```
P_hat/8 <= P_tilde <= P_hat/2,
Q^T Q=I,
0<lambda_tilde_i<=1/4.
```

The energy is monotone in positive semidefinite order: its directional
derivative along `A>=0` is `2tr(H P H A)>=0`, since `H P H>=0` even
when `H` is indefinite. Thus the grid covariance is feasible and loses
at most `n log 8` in log determinant.

The rational rotation has exact coordinate widths
`w_i=sum_k |Q_ki|`, between one and `sqrt(n)`. The reviewed dyadic-grid
construction uses only these rational widths, transformed rational
quadratic coefficients, and integer depths computed by squared rational
comparisons. Its binary count is bounded by

```
-(1/2)log2 det(P_tilde) + n log2 n+n.
```

Combining the constant log-determinant optimization error, the factor-eight
covariance loss, and the finite theorem's integer lower bound proves the
additive `O(n log(n+1))` comparison with arbitrary convex integer lifts.
The determinant benchmark is at most `nb log 2` in negative natural-log
scale, so all depths and their total are polynomial in the input length.
The finite theorem's compact shared-prefix construction then has
polynomially many rows, variables, and rational coefficient bits.
