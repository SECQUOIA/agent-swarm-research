# Independent audit of the strict quartic PosSLP lower bound

Date: 2026-10-03.

## Verdict and scope

The reduction in
[unconstrained-quartic-posslp-reduction.md](../../../research-20260927/unconstrained-quartic-posslp-reduction.md)
is correct under its stated representation and promises. It gives a
polynomial many-one reduction from PosSLP to exact minimum-sign decision
for rational quartics on all of real space. The output has a supplied
rational positive definite Gram matrix for its Hessian on the full basis
`(z, X ⊗ z)`, is globally strongly convex, and has a nonzero minimum. The
minimum is negative exactly on yes instances. The rational SOS-interior
consequence is also correct, with an existence claim rather than a
polynomial-size certificate claim for the polynomial Gram.

I reconstructed the substantive arguments in the following dependencies
without relying on their earlier reviews:

- [Analytic cubic-root simulation](../../../research-20260927/posslp-certified-cubic-root-reduction.md).
- [Signed odd-root quartic realization](../../../research-20260927/signed-odd-root-circuit-quartic.md).
- [Global Hessian estimate](../../../research-20260927/general-strongly-convex-quartic-singleton.md).
- [Full Hessian Gram and rational recovery](../../../research-20260927/sos-convex-quartic-realization.md).

No substantive mathematical correction is required by this audit. Two
small clarifications below would make the proof easier to inspect. This
audit establishes neither publication priority nor any complexity upper
bound for arbitrary quartic optimization.

## 1. Analytic sign simulation

The product macro has the required exact vanishing on both coordinate
axes. Its construction uses an even analytic function with quadratic
leading coefficient one. Consequently its first nonzero bivariate term
is `xy`, and every other term contains both variables. This last property
is what makes the simulation work when input signals have unequal
orders in the small parameter; an ordinary additive approximation to
multiplication would not suffice.

The stated complex-disk bounds are valid. On the disk of radius `1/12`,
the branch of `(1+3z)^(1/3)` through one is analytic and its derivative
has modulus below two. Every intermediate argument in the product macro
stays within that disk on the closed polydisk of radius `1/100`.
Cauchy's coefficient bound and the exact axis vanishing give the
displayed relative product-error estimate. The constant `2^24` exceeds
the resulting `2 × 100^3` bound.

I checked both inductive error steps. Equal-order addition contributes
at most `34 B^2 δ^(d+1)`. Multiplication contributes at most
`(3 B^2 + 16 K B^3) δ^(a+b+1)`. Both fit the recurrence
`B_j = 64 K B_(j-1)^3`; its exact logarithm is
`log2 B_j = 16 × 3^j - 15`. Cancellation, including a zero leading
coefficient, does not invalidate the induction.

The numerator/denominator transformation aligns the addition orders
using only a constant number of macros per source gate. Orders are
annotations, not printed powers of the parameter. Their maximum is at
most `2^T`. Replacing the integer output by `2V−1` removes the zero case
before the analytic simulation, so the final signal has a certified
nonzero sign even if the original PosSLP output vanishes.

## 2. Small signals, interval promises, and encoding length

The topology fixes `T` before any small parameter is chosen. Repeated
application of `S(z) = (1+3z^2)^(1/3)−1` yields
`0 < S(z) ≤ z^2`, and the stated number of parameter gates makes
`B_T δ ≤ 2^−30`. Only the initial rational parameter has to be printed;
its bit length is linear in the raw-gate upper bound. There is no hidden
printing of a rational with doubly exponential bit length.

Direct signed interval arithmetic really satisfies the advertised input
promise, even though it loses the cancellation between a predecessor's
linear and square occurrences. Its worst deviation is at most
`13 w_(i−1)`, while each next width is `1000 w_(i−1)`.
Repeated inputs do not increase this upper estimate. The first rational
parameter gate satisfies its inclusion separately.

The extra signal used in the unconstrained reduction has `T+1` distinct
squaring gates. Rebuilding the initial parameter with the larger raw
gate count maintains every interval inclusion and strengthens the
simulation's upper bound on `δ`. The extra output and the arithmetic
output are distinct coordinates. Their normalized values satisfy
`|v0| ≤ 1/8` and `u0^2 ≤ |v0|/2` with considerable slack.

## 3. Signed odd-root realization

Sign normalization and multiplication by the common rational scale are
valid for negative boxes as well as positive boxes. Unary degree
encoding is needed: the construction retains approximately half the
degree in coordinates, and its output-size claim is not a claim for
binary encoded degrees.

The chain residuals have exactly the intended powers as their unique
real common zero. The terminal equation has odd degree and therefore a
unique real root. The Jacobian is block lower triangular and its local
determinant is `d_i α_i^(d_i−1)`, of magnitude at least one after
normalization.

One useful clarification is to state the full operator-norm bound
`||J|| ≤ ||J||_F ≤ V` explicitly before using
`ν = V^(−(N−1))`. The text explicitly mentions only individual gradient
norms at that point. The stronger bound is valid: every Jacobian entry
has magnitude at most `3 A^N`, there are `N^2` entries, and the selected
`V = 4 N A^N` dominates the resulting Frobenius bound. Thus the
singular-value product argument is sound; this is an omitted supporting
line, not a gap in the chosen constants.

The local exposing quadratic restricts to
`(t−α)(t^d−α^d)` on the power curve. Its tridiagonal matrix is positive
definite with the stated spectral margin. Substituting the affine
predecessor radicand introduces exactly the claimed centered cross
term and no residual linear term.

The identity expressing this quadratic through rational vanishing
quadratics is exact. Approximating its algebraic coefficients therefore
preserves the zero exactly. This is essential: simply approximating a
quadratic centered at the irrational point would not suffice.

The geometric weights control signed interactions with earlier gates.
After scaling coordinates by square roots of the weights, every cross
entry has magnitude at most `A sqrt(ρ)/2`, so the absolute row-sum bound
is at most `h0/4`. The stated positive quadratic margin and upper bound
follow. The coefficient approximation bounds then give a rational
vanishing quadratic with positive definite quadratic part and arbitrarily
small gradient, at polynomial requested precision.

The root-approximation recurrence also has the stated constant:
`e A^(e−1) ≤ N A^(N−1)`, and multiplying by the total absolute
radicand coefficient bound `A` gives `C = N A^N`. The supplied interval
promise keeps the radicand at least one. Outward dyadic rounding and
bisection therefore need polynomially many bits. This is a certified
approximation algorithm under supplied boxes, not an algorithm for
discovering such boxes for unrestricted signed-root circuits.

## 4. Strong convexity and a full rational Hessian Gram

The global Hessian estimate correctly retains the potentially negative
contribution from squares of indefinite quadratic residuals. The
positive quartic contribution from the exposing quadratic dominates
those terms; the quadratic residual contribution supplies curvature
near the zero. Completing the scalar square gives the stated uniform
strong-convexity bound.

The block Hessian Gram is stronger than a nonnegativity test only on
vectors of the form `(z, X ⊗ z)`. Its constant block, cross block, and
quadratic block reproduce the entire Hessian biform. The quadratic
block has a lower bound `2m^2 I`. The Schur-complement subtraction costs
at most `18 N ε^2 (L+NV)^2/m^2`. The realization uses precisely the
stronger choice of `ε` with the additional factor `N`, so the Schur
complement stays strictly positive.

Translation back to rational output coordinates gives an algebraic
positive definite Gram with an explicit rational spectral margin of
polynomial bit length. Its entries have degree at most two in the
formal center coordinates: gradient vectors depend affinely on the
center, the cross block does also, and the homogeneous block is
constant. Approximating the center to polynomial precision is enough.

The coefficient projection is exact rational linear algebra. Its
constraint matrices have disjoint supports, so the projection is
Frobenius nonexpansive and cannot consume more than the allowed spectral
error. The polynomial number of rational entries and positive margin
therefore give a polynomial-time rational certificate construction.
No dense representation of the common algebraic number field is used.

## 5. Cubic tilt and the optimum's sign

The supplied cubic Hessian Gram has the claimed entries and Frobenius
norm `sqrt(12 κ^2 + 10) < 8`. For a positive definite `h × h` rational
matrix, `det(M)/tr(M)^(h−1)` is a valid positive lower bound on its
smallest eigenvalue. Computing it and rounding `9/μ` upward requires
polynomial bit time and gives polynomial output bit length. Thus the
tilted quartic has a supplied full Hessian Gram at least the identity.

At the old zero, its objective value is `−u0^2 v0` and its squared
gradient norm is `4u0^2 v0^2 + u0^4`. Distinct coordinates are needed
for this norm identity and are present in the construction. Strong
convexity bounds the possible decrease to the new minimum by half
that squared norm. On the nonpositive PosSLP branch, the inequalities
`|v0| ≤ 1/8` and `u0^2 ≤ |v0|/2` give a strictly positive lower bound
`u0^2 |v0|/2`. On the positive branch, the old zero already has negative
objective value. Hence both branches have nonzero minima and the sign
reduction is exact.

The positive-minimum SOS consequence uses a rational center sufficiently
close to the new minimizer. The full Hessian Gram supplies every
quadratic homogeneous monomial after rational Taylor integration; the
completed norm and positive constant supply the affine span. This
proves existence of a rational positive definite polynomial Gram.
There is no justified polynomial bound on the bit length of that center
or Gram, and the source correctly makes no such claim.

## Verification performed

The following targeted commands passed:

```text
python3 research-20260927/check_posslp_cubic_root_reduction.py
python3 research-20261003-arithmetic/reviews/exact-core/lower_diagnostics.py
```

The first checks exact macro coefficients and signed interval arithmetic
for five compiled circuits, including zero and negative outputs and
cancellation. The independent diagnostic checks exposing and Jacobian
identities for odd degrees three through eleven, a translated full
Hessian Gram with mixed indefinite quadratic parts, exact rational
coefficient projection and its nonexpansive property on that instance,
and the cubic tilt identity and margin decomposition.

These finite symbolic checks supplement the universal arguments above.
They do not test a complete implemented reduction or prove its running
time. No project-wide checks or CI inspection were performed.
