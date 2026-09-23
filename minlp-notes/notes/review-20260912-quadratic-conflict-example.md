The revised quadratic-conflict construction passes this correctness review.
Its certificate is valid for globally active inequality rows represented by
symmetric quadratic matrices. This fresh
independent review checked the certificate contract, repair LP, exact example,
and stated limits in
[the research note](research-20260912-algorithm-opportunities.md). It did not
assess novelty or solver performance.

The nonnegative aggregation argument is sound: original feasibility implies
`G_lambda <= 0`, and valid local underestimators imply `G_lambda >= L_lambda`
throughout the node box. A strictly positive minimum of `L_lambda` therefore
proves node infeasibility. When the aggregate matrix is PSD, its tangent is
an underestimator everywhere, so imposing that tangent as an inequality is
globally valid and separates its expansion point in the infeasible box.
An arbitrary tangent need not exclude the whole box. A tangent at a minimizer
of the convex aggregate over the box does exclude it, by the first-order
optimality condition and the positive margin.

The displayed inequality-only repair LP is correct. Its auxiliary variables
satisfy `v_j <= min(0,a_j)`, and nonnegative box widths make the lifted
expression a lower bound on the exact affine box minimum. Choosing
`v_j = min(0,a_j)` attains that minimum. Thus any feasible positive `delta`
already certifies the proof; optimality is not required for validity. The
absolute-value constraints enforce diagonal dominance with nonnegative
diagonal. For symmetric matrices, the displayed sum-of-squares identity
proves PSD exactly.

The review identified and the note corrected one normalization issue:
unrestricted multipliers for linear equalities require normalization as well.
Normalizing only inequality
weights can leave the margin objective unbounded. For example, take the
globally valid inequality `g(x) = -1 <= 0`, equality `h(x) = x = 0`, and node
`B = [1,2]`. With inequality weight one, the affine certificate
`L(x) = -1 + mu*x` has margin `mu - 1` for `mu >= 0`. Its margin is unbounded
although every individual certificate is sound. The note now scopes the
displayed LP to inequality rows. For an equality extension, it specifies
`mu = mu_plus - mu_minus` with
nonnegative parts and normalize the sum of all inequality weights and both
equality parts to one. This also permits equality-only certificates.

The exact example passes independent coefficient checks:

- Both estimator differences expand to the displayed polynomials. Their
  factorizations are nonnegative on `[1/5,1]^2`.
- The root witness satisfies both lifted rows, both complete square
  envelopes, and all four McCormick inequalities.
- `2*ell_1 + ell_2` has positive affine coefficients and exact box minimum
  `7/100`. The first estimator alone has minimum `3/50`.
- `2*g_1 + g_2 = 2*x^2 + 3*x*y + 2*y^2 - 21/100`. Its symmetric matrix has
  determinant `7/4` and the stated positive DD certificate.
- At `(1/5,1/5)`, the aggregate value is `7/100` and its gradient is
  `(7/5,7/5)`. Its tangent is exactly `x+y <= 7/20`. This excludes both the
  root witness and the entire indicated node box.
- The origin and the two stated individual-activation points satisfy both
  original rows. Joint activation is infeasible.

The added exact repair calculation is also correct. With normalized weights
`(a,1-a)`, the matrix is
`[[a,(3*a-1)/2],[(3*a-1)/2,2*(1-a)]]`. Diagonal dominance holds exactly for
`1/5 <= a <= 5/7`. The affine box margin is `(31*a-17)/20` when
`a <= 5/9`, and `(11*a-5)/100` otherwise. Both pieces are increasing and
agree at the breakpoint, so the optimum is `(5/7,2/7)` with margin `1/35`.
The illustrative weights `(2,1)` have normalized margin `7/300`; their
unnormalized margin `7/100` should not be compared directly with the optimum.

The pure-bilinear and Shor limits are correct. A symmetric PSD matrix with
zero diagonal is zero, since each two-by-two principal minor forces the
corresponding off-diagonal entry to vanish. Signed multipliers on purely
bilinear equalities cannot change this fact; those equalities alone still
provide no diagonal curvature. Cancellation can nevertheless produce useful
affine aggregates. In a common Shor lift, summing the lifted rows gives
`trace(Q_lambda*X) + a_lambda^T*x + b_lambda <= 0`, while PSD of both
`Q_lambda` and `X-x*x^T` implies `G_lambda(x)` is no larger than that lifted
quantity. Consequently all these PSD aggregate inequalities are implied by
the full Shor relaxation.

Conditional GDP rows require the conjunction of all supporting activation
conditions. The note's revised wording correctly states this restriction.
It also explicitly requires symmetric quadratic matrices, replacing them by
their symmetric parts when necessary. These corrections resolve all findings
from this review.

Validation on 2026-09-12: the updated
[exact arithmetic script](../code/research_20260912/verify_quadratic_conflict_example.py)
ran successfully. Separate rational coefficient calculations checked the
polynomial expansions and the repair-margin formulas; the universal
validity claims above were checked algebraically. No benchmark or novelty
claim follows from these checks.
