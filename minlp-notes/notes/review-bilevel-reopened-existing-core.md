# Reopened independent audit of the existing bilevel core

Date: 2026-09-06. Reviewer: independent `existing_proof_audit` agent.

**Verdict: PASS for the stated fixed-resource and one-resource accuracy-bit
theorems and their general monotone-polynomial inverse dependency.** I found
no substantive correction to make in these results. This is a fresh proof
audit, not an inference from their previous PASS labels. It does not establish
novelty or practical running time.

Reviewed in full:

- [Fixed-resource theorem](../results/bilevel-fixed-resource-accuracy-bit-algorithm.md).
- [One-resource theorem](../results/bilevel-one-resource-accuracy-bit-algorithm.md).
- [General monotone inverse lemma](certified-monotone-polynomial-inverse-approximation.md).

I also checked the compression and attainment arguments of the
[exact aggregate theorem](../results/bilevel-fixed-aggregate-response-algorithm.md)
and the [fixed-rank quadratic corollary](bilevel-fixed-rank-quadratic-corollary.md).
No defect was found in these arguments. This auxiliary check is not a full
audit of every extension in the broader bilevel package.

## Fixed-resource model and exact feasibility

The separation inequality has the correct direction: for
`b in C[0,1]^N + R_+^k`, every nonnegative functional is bounded below by
`sum_i min(0,lambda^T C_i)`. Conversely those functionals separate every
point outside this closed polyhedron. On each orthant-restricted arrangement
cone, the right side is linear, so testing extreme rays suffices. Coordinate
hyperplanes are essential and are included. In a pointed cone, each extreme
ray has `k-1` independent active homogeneous constraints, even when the cone
is lower dimensional. Thus the enumerated rational inequalities describe
the feasible leader set exactly, including degenerate resource faces.

The integer scaling in Section 3 is consistent. If `A=D[C;I;-I]`, the
representation coefficients for rows of `A` must be multiplied by `D` to
obtain multipliers for the original constraints. The stated `K` and
`Lambda` include that factor. An independent set of at most `N` integer
rows has a positive integer Gram determinant; its inverse cofactor bound
controls individual coefficients as well as their sum. The generous
`N^3 M V` factor dominates the needed powers of `N`. No dependence on the
number of active rows is omitted after conic reduction.

At the Euclidean projection of a box point onto the feasible polytope,
the displacement is a conic combination of active normals. Each active
resource row contributes at most `D delta` to its scalar product with
the displacement, and active box rows contribute nonpositively. This
proves the repair bound without requiring a Slater point or identifying
an active set computationally.

## Response error and attained upper optimum

For the true box-Lagrangian minimizer `q`, weak duality yields
`F(q)+lambda^T(Cq-b)<=F(z*)`. After feasibility repair, Lipschitz
continuity gives the claimed primal gap. The proof correctly distinguishes
`q`, the repaired feasible point, and the exact follower optimizer.

The signed-polynomial extension has a valid coefficient-independent
modulus. Interpolation on a response interval of length `s` bounds both
normalized endpoint values by `v(2d/s)^d`, where `v` is the marginal
increment there. Subtracting those endpoint values gives
`v >= (s/(2d))^d/2`. Integrating on the half of a displacement interval
farther from the Bregman base point gives
`G s^(d+1)/[4(4d)^d]`. This applies in both directions; for a leftward
displacement the integrand is `g(base)-g(base-t)`. Replacing `d` by the
maximum numerical degree weakens the lower bound. Interior stationary
points do not invalidate it.

Shifting a signed marginal by its constant term and shifting the affine
load by the same amount preserves the cost exactly. A normalized strictly
increasing marginal lies between its two endpoint values, so the original
gradient and multiplier bounds remain valid despite cancellation among
polynomial coefficients.

Uniformly bounded multipliers give a correct compact-subsequence proof
of response continuity along feasible leaders. Feasibility and
complementarity pass to limits, and strict convexity identifies the
limiting response. Thus compactness of the feasible leader polytope
really does imply upper-objective attainment.

## Surrogate optimization, bit complexity, and rational recovery

The inverse interface needs polynomial bounds on branch count, degree,
coefficient encoding, and closed-interval error. It does not need the
sharper positive-coefficient branch estimate. Substitution of affine
arguments into these polynomials has polynomial expanded size because
the total geometric dimension `r+k` is fixed. Introducing a second copy
of these variables to define the minimizing set keeps the dimension
fixed; no variable for each true inverse value is introduced.

The required algebraic import is appropriate. The quantifier-elimination
theorem and its coefficient-size bounds in
[Basu's author-hosted survey, Theorem 2.18](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf)
give polynomial degree and bit bounds after fixing all variable-block
dimensions. This supports the complexity claim; it does not make the
resulting general-purpose algorithm computationally practical.

The rational rounding step preserves the rational cell, not the nonlinear
surrogate feasible set. This distinction is necessary and explicit. In
fixed dimension one can enumerate cell vertices and simplices containing
the sampled algebraic optimizer. Rounding nonnegative barycentric weights
down and assigning the remainder to one vertex preserves every rational
equality of a lower-dimensional cell. Exact algebraic sign comparisons
make rounding valid even near a grid boundary. The enlarged residual and
complementarity allowances account for loss of nonlinear feasibility.

I recomputed the final ledger: the true box response has resource
violation at most `3S eta` and complementarity error at most
`3k Lambda S eta`; each term in the response bound is at most `tau/2`.
The upper error from replacing the true response by the branch value is
at most `A_c(eta+tau)<=epsilon/8`. The claimed leader and value errors
therefore hold with room. Every required precision has polynomial bit
length in the numerical degree and accuracy count. Neither an exact
follower vector nor a feasible approximate follower vector is promised.

## The inverse lemma's analytic step

The dangerous target set includes real parts of **all complex critical
values**, not just critical values from real stationary points. The
three-real-variable formula describes exactly those real parts; its
projection is finite. Polynomial expansion and fixed-dimensional
elimination keep its encoding polynomial.

Padding their rational enclosures controls inverse oscillation on every
merged bad component through the interpolation modulus. In the remaining
gaps, every critical real part lies at least `rho` behind a boundary, or
is more than one unit away from `[0,1]`. This proves the stated clearance.
The geometric panels, their rational midpoint approximations, and the
analytic radius leave the displayed strict margin to all complex critical
values. The rational center cannot itself be critical.

Absence of critical values alone is not used as an unjustified assertion
of a global inverse: properness of the polynomial gives a finite
unramified covering of a slightly enlarged disk. Every connected sheet
over this simply connected disk gives a single holomorphic inverse. The
sheet through the rational response center agrees with the increasing
real inverse on the panel. The root bound controls this branch on the
whole Cauchy disk.

Formal reversion produces rational Taylor coefficients. A product of
`h` coefficients with indices summing to `n` has a denominator dividing
`A_1^(2n-h)` after factoring out `Q^n`; the additional division by `A_1`
preserves the claimed denominator `A_1^(2n-1)` for `h>=2`. Cauchy's
coefficient bound then bounds the numerator encoding. It is important
that intermediate products also have polynomial bit size; at most
exponentially many compositions are summed, so their logarithmic count
is polynomial in the truncation degree. This resolves that potential
arithmetic vulnerability.

## One resource and exact aggregate attainment

The scalar multiplier endpoints are valid for signed and zero weights.
Each nonzero weighted response difference has the same weak sign, so the
weighted absolute-difference identity is exact. Zero weights have no
response change with the multiplier. The rational-recovery residual
allowance and the resulting upper-objective error follow without any
strong-convexity bound. The signed-marginal transfer needs only the
general inverse interface; it does not reuse the positive-coefficient
degree estimate as an unproved bound.

For the exact aggregate theorem, comparing a feasible KKT point with every
KKT point is sufficient for global optimality: every global minimum is
represented and all represented points are feasible. This is not an
assumption that nonconvex KKT conditions suffice. Positive local quadratic
coefficients make clipping single-valued even though the aggregate term
may be nonconvex.

Its optimistic-attainment proof correctly uses **fixed constraint normals**.
Given convergent optimal pairs, Hoffman repair approximates any feasible
limit competitor by competitors at the sequence leaders. Continuous
right-hand sides and box endpoints make the repair displacement vanish.
This closes the response graph. Leader-dependent aggregate coefficients
do not affect this argument because they occur in the objective. The
argument must not be transferred automatically to leader-dependent
resource normals; that is a separate semantics question.

## New independent exact diagnostic

[The reopened checker](../code/bilevel_reopened/existing_core_review.py)
uses only `fractions.Fraction` and standard-library arithmetic. Its
normalized quintic marginals have derivatives proportional to
`(z-a)^2 ((z-b)^2+c^2)`. They therefore combine a real stationary point
with a nonreal conjugate critical pair, and have signed coefficients.
The cases include stationary endpoints, stationary interior points, and
`c=1/1024`, which brings the nonreal critical points close to the real axis.

It checks the inverse modulus and directed Bregman estimate independently
by exact integration, and evaluates the full critical values with exact
Gaussian-rational arithmetic. For the generated analytic panels it checks
the distance to every actual complex critical value, including both
extreme allowed errors in the rational Taylor center. The completed run
passed all 16 models, 1,152 directed Bregman inequalities, 1,152 inverse
modulus inequalities, 48 exact critical-point evaluations, 56 bad-component
width checks, and 79,456 analytic-panel checks. Run it with
`python code/bilevel_reopened/existing_core_review.py` from the repository
root. These finite checks supplement the universal proof and do not
implement quantifier elimination or the complete bilevel optimizer.
