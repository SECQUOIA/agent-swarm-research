# Second independent review of the globally convex polynomial point oracle

Date: 2026-10-02. Verdict: **PASS** after reading the complete actual
[globally convex polynomial theorem](globally-convex-polynomial-point-oracle.md),
including its final Section 7 clarifications. I also read the actual
[cubic completion interface](cubic-core-full-point-oracle.md) used there.
No substantive mathematical or bit-complexity gap remains. This is a
proof review, not a publication-priority assessment.

## 1. Interpolation and the global Jensen argument

The constants `C_D=(D+1)D^D` and `J_D=(D+1)D^(D+1)` are valid.
The Lagrange denominators at `j/D` have magnitude at least `D^(-D)`.
Bounding each numerator factor by `1+|t|` proves the extrapolation
bound. At zero, differentiating each basis numerator gives at most
`D` terms, with the remaining factors bounded by one. This proves
the stated derivative estimate after rescaling an interval of length
`R`. No coefficient-height or unknown-root parameter enters either
constant.

At a constrained optimum `y`, the directional first-order term lies
between zero and the feasible objective gap `E`. The translated
Bregman polynomial is nonnegative on all of Euclidean space by global
convexity. Its values on the feasible unit segment lie in `[0,E]`.
Consequently interpolation bounds its extrapolated values even at
the large distance `E^(-1/D)` used only in the analysis.

The midpoint in equation (8) is exact. Its two arguments need not
be feasible, so convexity only on the supplied polytope would not
suffice. The coefficient bounds in (9) cover both `y` and `2c-y`:
their infinity norms are at most `U` and `U+2D`, respectively. The
gradient bound and `||c-y||_infinity<=D+U` control the affine term
in the Bregman polynomial. Thus `H` is a valid uniform majorant,
including the unknown optimizer. With `R=E^(-1/D)>=1`,
`E(1+2R)^D<=3^D`, and the stated `W` safely bounds the entire
univariate polynomial on `[0,R]`.

Applying the derivative bound and adding back the first-order term
proves (10). The separate `E=0` argument is also sound: the segment
Bregman polynomial then vanishes identically, while global Jensen
bounds each translated univariate polynomial above and below on the
whole real line. Such a polynomial is constant. This directly gives
zero sampled-gradient residual, without assuming a sequence of
positive-gap feasible points.

## 2. The rational sampled rows describe precisely the optimizer slice

The integer simplex samples in (11) are unisolvent. In the falling
factorial basis, an entry vanishes unless its multi-index is
coordinatewise bounded by the sample. Ordering by total degree makes
the evaluation matrix triangular; within the same degree, a nonzero
entry requires equality of the two multi-indices. Its diagonal is
one.

The directional derivative has degree at most `D-1`. Vanishing at
all these samples is therefore equivalent to vanishing identically,
and integrating it gives global translation invariance along that
direction. The zero-gap conclusion from Section 3 puts every
difference of constrained optimizers in this kernel. Conversely,
translation invariance preserves the objective on every feasible
point in the resulting affine slice. This proves (13) with the
unknown, possibly irrational right-hand side.

Affine objectives are included: their nonzero constant gradient is
retained as a row. Constant objectives have zero row matrix and the
whole feasible polytope as their optimizer set. Neither case requires
an eigenvalue or a nonzero higher-order coefficient.

The sample count is `binom(n+D-1,D-1)`, polynomial in dimension for
fixed `D`. Sample coordinates are small integers. Evaluating the
explicit rational gradients and clearing all resulting denominators
therefore uses polynomial bit work and produces a polynomial-size
integer matrix. This is a fixed-degree statement; the proof does not
assert the same bound when the degree is an unrestricted input parameter.

## 3. Effective Hoffman and canonical-output constants

The projection-normal proof of (14) is valid for the original
polytope, including redundant rows and lower-dimensional domains.
An independent subset of original equality rows and active inequality
normals has at most `n` rows and integer Gram determinant at least
one. The resulting smallest-singular-value estimate has the stated
height bound. Since the starting point is feasible, active inequality
normals make nonpositive contributions to the projection inner product.
Only the equality residual remains. No rationality of the affine-slice
right-hand side is needed.

The bound `Q N C_* E^(1/D)` for the Euclidean residual is conservative
but correct. Equation (15) is consequently a computable rational
error constant. Its logarithm is polynomial in the rational input
length for fixed degree. The unknown optimizer, a root-separation
bound, and an unknown analytic error constant are not algorithmic
inputs.

The reviewed rational-polytope convex value solver is enough to
realize the required objective tolerance. For the minimum-norm
selector, (16) gives `tau R_x^2<=1`, so the original error bound
applies to the exact regularized minimizer. The two projection and
comparison inequalities in (17) yield

```
e <= epsilon^2/(8R_x),
||x_tau-p|| <= epsilon/2.
```

A feasible regularized objective gap `eta=tau epsilon^2/4` gives
the remaining `epsilon/2` distance by strong convexity in original
coordinates. Both new precision lengths are polynomial in `I+q`.
The penalty remains the original Euclidean norm, so the selector
does not change under the value solver's affine-hull reduction.

For a simultaneous objective certificate, the additional gradient
bound and tighter point request are valid on the convex polytope.
Pairing that point with a separately refined global value lower bound
has the stated total width. This requires only polynomially many
additional accuracy bits.

## 4. The bounded transfer in Section 7

I checked this section against the complete saved cubic-completion
source, rather than treating it as an automatic consequence of a
rational-coefficient point theorem.

The quadratic completion is exact. Because the original sampled
objective is globally bounded below on `P` by its optimum, adding
the nonnegative core penalty makes the minimizer set precisely the
optimal fiber at the selected core. The positive coefficient
`beta=alpha+1` handles tied cores. Global convexity of `G` implies
global convexity of the unknown-core tilted polynomial `T_a`.

The irrational core does not enter the rational row matrix. Uniform
majorants `beta+sigma` for its linear coefficients and `beta k/2`
for its constant term suffice for the interpolation bounds. Adding
the rational core-coordinate rows removes the unknown tilt when
describing the zero slice. For positive gap, their residual is
bounded by `sqrt(2Delta/beta)`, which is at most a known multiple
of `Delta^(1/D)` for `Delta<=1` and `D>=2`. The sampled rational
gradient residuals obey the same bound. Thus the Hoffman constant
and the resulting `Gamma` remain polynomial-bit quantities computable
without the selected exact core.

For the approximate-core solve, the uniform objective perturbation
is at most `beta sqrt(k)||b-a||`. Its contribution to the exact-core
regularized gap occurs twice. With the stated core tolerance and
`eta=tau epsilon^2/8`, the sum is at most `tau epsilon^2/4`.
The previous regularization and strong-convexity estimates then give
the full selected-point guarantee.

The final saved text handles `k=0` before dividing by `beta k`,
includes `alpha`, `sigma`, and the completion certificates in the
base encoding, and records the ordinary-polynomial specialization
when `alpha=0`. Short dyadic core output is explicitly required;
the composition does not treat an exponentially large rare-fallback
record as a short rational input. This is the already-reviewed
short-output contract from the cubic interface. The new completion
needs no extra random event or change of noise law.

## Verification scope

This was a second fresh actual-file mathematical and bit-complexity
review. The initial read identified only the zero-core clarification
in Section 7, which is now present and was reread. I did not run
duplicate optimizer diagnostics, search external literature, edit
indices, or propose further directions. Scoped local-link, syntax,
fence and whitespace checks for this review were performed separately;
no project-wide verification or CI inspection was used. Publication
priority remains a separate source-audit question.
