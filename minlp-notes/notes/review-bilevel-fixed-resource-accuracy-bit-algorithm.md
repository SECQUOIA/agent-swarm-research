# Independent audit of the fixed-resource accuracy-bit algorithm

Date: 2026-09-05. Reviewer: fixed_resource_audit, independent of the proof author.

**Verdict: PASS for the stated nonnegative polynomial-marginal theorem and
the signed-marginal extension in Section 8.** The signed extension and the
one-resource transfer are covered explicitly in the addendum below.
I independently checked the complete [candidate proof](bilevel-fixed-resource-accuracy-bit-algorithm.md),
including its rational input and output claims. I found no substantive mathematical
defect and no missing polynomial-bit conditioning assumption. The proof handles
inequalities, equality pairs, degenerate feasible follower faces, signed resource
columns, and signed upper objective coefficients. This audit establishes neither
publication priority nor a practical implementation bound.

The reviewed scope fixes the leader dimension and the number of resource rows;
the resource matrix is independent of the leader. The original proof assumes
nonnegative marginal coefficients with positive sums; the addendum replaces
this with strict increase for arbitrary signed coefficients. Numerical degree
may grow.

## Exact feasible-leader projection

The separation characterization is correct: `C[0,1]^N+R_+^k` is a closed
polyhedron, and a separating linear functional with finite lower support has
nonnegative coefficients. Its support value is the sum of the coordinatewise
minima in equation (1).

On each cone cut out by the column and coordinate hyperplanes, this support
value is linear. The cone lies in the nonnegative orthant and is therefore
pointed. Checking its extreme rays suffices. Every ray has `k-1` independent
active hyperplanes; including coordinate hyperplanes deals with rank deficiency
and zero columns. Enumerating extra nonnegative nullspace directions is harmless:
the original inequality is valid for all such directions. Directions and the
resulting leader inequalities have polynomial rational encoding. The count is
polynomial when `k` is fixed, including the separate `k=0,1` conventions.

Thus the final rounding preserves exact follower-feasible leader membership in
an explicit rational polytope. It does not require a strictly feasible follower.

## Uniform constants and approximate duality

The scaling by a common denominator `D` is consistent throughout. For an
independent collection of integer rows, the Gram determinant is a positive
integer and each Gram cofactor is bounded by the displayed `V`. More explicitly,
each entry of `A_J v` is at most `sqrt(N) M ||v||_2`, and multiplication by at
most `N` inverse entries gives the claimed individual coefficient bound. Summing
at most `N` coefficients gives the coarser `N^3 M V ||v||_2` bound. For a gradient
bounded in infinity norm, the individual coefficients are at most
`N^3 M V Gbar`. Multiplying them by `D` gives multipliers for the original,
unscaled constraints, as required by `Lambda=K Gbar`.

Polyhedral normal-cone representations hold on lower-dimensional faces and do
not require Slater's condition. Nonnegative representations can be reduced to
independent rows by conic Caratheodory reduction. This proves bounded *existence*
of a suitable resource multiplier, which is all the algorithm uses.

For feasibility repair, projection stationarity supplies the analogous normal
representation of `q-y`. At active resource rows the scaled violation is at most
`D delta`; active box rows contribute a nonpositive quantity because `q` is
already in the box. The scalar-product identity therefore proves the uniform
Hoffman estimate with the displayed `K`. Division by the norm is unnecessary
when the projection displacement is zero; that case satisfies the bound directly.

The weak-duality inequality has the correct sign for `Cz<=b` and `lambda>=0`:
the box-Lagrangian minimum is a lower bound for the feasible follower optimum.
Repair and Lipschitz continuity then give equation (7). Neither the approximate
response nor the repaired response is incorrectly treated as the exact optimizer.

The power-Bregman inequality is valid in both directions. For the reverse
direction, `v^j-(v-t)^j>=t^j` follows by applying the binomial theorem to
`v=(v-t)+t`, with both summands nonnegative. The replacement of every exponent
by `P+1` is valid because all distances lie in `[0,1]`. Summing nonnegative
coefficients yields the stated `mu`, and first-order optimality at the feasible
follower optimum supplies the needed sign of the linear term. Equation (8)
follows without a uniform positive Hessian lower bound.

The continuity and attainment argument is also sound: choose optimal multipliers
in the common compact box, pass to subsequences, and use continuity of the clipped
inverse and the feasibility/complementarity conditions. Uniqueness identifies
every limiting response. This avoids invoking an unjustified continuity theorem
for a potentially degenerating feasible correspondence.

## Surrogate optimization and rational recovery

I read the [positive-polynomial inverse lemma](certified-positive-polynomial-inverse-approximation.md)
and checked the interface used here: rational branches and breakpoints,
uniform error on the *closed* branch intervals, and polynomial encoding in
`P`, coefficient bits, and `log(1/eta)`. Approximation branches may exceed the
unit box slightly; the present proof uses their errors and does not assume their
exact feasibility. Endpoint branch overlap causes no problem.

There are only `r+k` geometric variables after substituting `lambda=Lambda theta`.
In that fixed dimension, the affine arrangement, its lower-dimensional cells,
their vertices, and the dense expansion of all substituted polynomials have
polynomial size. The min-point formula introduces a second copy of these
variables, not one variable for each follower coordinate. Exact real algebraic
optimization and sampling consequently retain polynomial degree and bit bounds.
Pairwise algebraic value comparisons are sufficient; a joint field containing
all original follower roots is unnecessary.

The rational recovery deliberately stays inside the rational cell and exact
leader-feasibility polytope, while allowing a controlled change in the nonlinear
surrogate inequalities. This is essential. Every point of the bounded rational
cell belongs to a simplex of at most `r+k+1` of its vertices, including when the
cell is lower dimensional. Enumeration in fixed dimension and exact algebraic
tests find such a simplex. Rounding its barycentric weights down and placing
the remaining mass on one vertex preserves membership exactly. Rational grid
precision depends on coefficient bit lengths, not on an unasserted interior
radius. Algebraic floor comparisons for the weights are also polynomial-bit
operations.

The displayed polynomial coefficient sum is a valid Lipschitz bound on the
unit cube. After rounding, the true response has violation at most `3S eta`
and complementarity error at most `3k Lambda S eta`. Substituting (9) into
(8) bounds each contribution by `tau/2`. Finally,
`A_c(eta+tau)<=epsilon/8` and `A_c eta<=epsilon/16`, so the claimed
`5epsilon/16` leader error and the asymmetric bounds for the rational value
estimate both hold. All powers in the tolerance have polynomial bit length
for *numerical* degree `P`.

If zero follower coordinates are allowed as an input convention, that empty
case should simply be dispatched to the leader LP. The proof explicitly begins
its nontrivial constant construction at `N>=1`; this is a harmless preprocessing
clarification, not a restriction on any nonempty instance.

## Independent exact diagnostics

I wrote and ran the separate standard-library
[Fraction checker](../code/bilevel_bounded_power/check_fixed_resource_first_review.py).
It does not call an optimization solver or use the candidate's implementation.
It compares primal vertex enumeration with the resource-ray inequalities and
solves small quadratic follower/projection problems by independent active-KKT
enumeration.

Results:

- 512 exact primal-feasibility versus ray-projection comparisons.
- 288 exact approximate-dual, feasibility-repair, and response-growth checks.
- 5,408 directed power-Bregman inequalities through marginal degree 32.

The deterministic cases include zero columns, dependent and opposite rows,
rational signed coefficients, boundary feasibility, and clipped responses.
These tests supplement the general proofs and do not replace them.

## Checked primary references and limits of the audit

Hoffman's original 1952 paper states the matrix-dependent distance-to-feasibility
bound for consistent linear inequalities. The candidate supplies its own coarse
integer-Gram estimate rather than requiring computation of an optimal Hoffman
constant. The original paper is available as a
[scan of the National Bureau of Standards publication](https://upload.wikimedia.org/wikipedia/commons/0/07/On_approximate_solutions_of_systems_of_linear_inequalities_%28IA_jresv49n4p263%29.pdf).

Basu's [author-hosted survey](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf),
Theorem 2.18, gives quantifier-elimination complexity and integer intermediate
bit-size bounds with explicit dependence on block dimensions. Theorem 2.15 and
the accompanying discussion give algebraic sampling. Fixing the total dimension
as done here makes the required operations polynomial in degree, polynomial
count, and coefficient encoding. These are established tools; the audit does
not ascribe novelty to them.

No claim has been reviewed for additional response-dependent upper constraints,
a leader-dependent resource matrix, unbounded resource-row count, or sparse
binary-encoded degrees with running time polynomial only in their encodings.

## Addendum: arbitrary signed polynomial marginals

**Section 8 verdict: PASS.** I independently checked its new interpolation and
Bregman calculations and its transfer through the complete fixed-resource proof.
I read the interface and completed review verdicts for the
[general inverse lemma](certified-monotone-polynomial-inverse-approximation.md).
Its full complex-analytic construction has separate
[first](review-certified-monotone-polynomial-inverse-approximation.md) and
[second](review-certified-monotone-polynomial-inverse-approximation-second.md)
PASS audits. I do not count this transfer audit as a third independent audit of
that full analytic construction.

Subtracting the initial marginal value and absorbing it into the affine target
preserves the follower objective. The shifted strictly increasing marginal lies
between zero and `G_i`; therefore the gradient and multiplier bounds remain
valid despite signed coefficients.

For a normalized marginal of degree `d`, all shifted interpolation values on
`[a,a+s]` lie between zero and its increment. The sum of absolute Lagrange basis
bounds is `(d/s)^d 2^d/d!`. Bounding the values at zero and one separately and
using their difference one gives (14), with room in the stated constant.
This argument needs monotonicity, not coefficient positivity.

For either displacement direction, the last half of the Bregman integration
interval has a marginal difference at least the increment over an interval
of length `s/2`. Applying (14) there and multiplying by the integration length
`s/2` gives exactly `G_i s^(d+1)/[4(4d)^d]`. Since `d<=P` and `s<=1`, the
replacement by `G_i s^(P+1)/[4(4P)^P]` weakens the bound correctly. The resulting
`mu` has polynomial encoding in numerical `P`. It supplies precisely the
response-growth estimate used by the existing error ledger.

The new inverse approximation can have larger polynomial degree and branch
count than the positive-coefficient construction. The fixed-dimensional
arrangement, dense expansion, optimization, and rounding arguments require
only polynomial bounds in the input and requested precision, so they still
apply. The constructed rational tolerance has polynomial encoding; the general
lemma's explicit rational-tolerance input convention is therefore respected.

The independent exact checker now also passes **3,380 signed-polynomial
modulus and Bregman cases** for normalized translated odd powers through degree
17. The tested stationary points include `1/3` and `1/2`, so these cases include
strictly increasing marginals with an interior zero derivative, as well as
stationary endpoints. Both displacement directions are checked.

**One-resource Section 9 verdict: PASS.** I read the full
[one-resource theorem](../results/bilevel-one-resource-accuracy-bit-algorithm.md)
and checked this transfer specifically. Its endpoint multiplier bounds and
weighted no-cancellation identity use strict monotonicity and continuity of
the clipped inverses. They do not use marginal coefficient signs. Exact leader
feasibility is determined entirely by the fixed resource weights. Polynomial
branches with uniform error on their closed domains provide the same fixed
`r+1` arrangement and polynomial surrogate; the original rational recovery and
error ledger remain valid. No replacement Bregman bound is needed in that
single-equality proof. The diagonal zero-row branch also uses only the general
inverse interface and the already reviewed fixed-dimensional recovery argument.
