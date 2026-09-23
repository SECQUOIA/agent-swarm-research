# Second independent audit: exact near-optimal follower robustness

Date: 2026-09-07. Reviewer: independent subagent `nearoptimal_review2`.
Disposition: **the main theorem and the convex fixed-normal attainment
subclass pass this proof audit**, subject to the explicitly inherited encoding
and fixed-dimension assumptions. This is a mathematical audit of the stated
composition, not an independent literature-priority determination or a practical
runtime validation.

Reviewed sources:

- [Near-optimal robustness draft](bilevel-reopened-near-optimal-robustness.md).
- [Quadratic block theorem](../results/bilevel-fixed-block-response-algorithm.md).
- [Moving normals and infimum semantics](../results/bilevel-compressed-response-infimum-semantics.md).

No theorem files were changed by this reviewer. The original draft's phrase
“shared linear inequalities/inequalities” should read “equalities/inequalities.”

## 1. Fiber compression is valid

For a fixed measurement matrix `T(x)` with at most `h` rows, the equality
`T(x)z=t` adds `h` shared equalities. The enlarged leader parameter `(x,t)` has
fixed dimension, the local quadratic blocks remain strictly convex, and the
number of aggregate rows does not increase. The added constraint normals are
polynomial and covered by the moving-normal extension. Rank deficiency of `T`
causes no failure: its equality multipliers need not be unique, and the response
engine does not require independent shared equalities.

Although the aggregate term may be nonconvex, each global fiber minimizer
satisfies polyhedral KKT conditions. The global value comparison against all
represented fiber KKT points returns precisely its global minimum. There is no
claim that all stationary fiber points are minimizers.

Every attained measurement value of a near-optimal response has a fiber
minimizer with no greater follower cost. Conversely, a fiber minimum under the
budget is a near-optimal response. This proves the projection identity even
when the original near-optimal response has nonzero gradient and satisfies no
unrestricted follower stationarity condition. It is essential that the
criterion depends only on `x` and the selected measurement `t`.

The compact box for the added measurement parameters exists with polynomial
bit length. Original coordinate bounds can be bounded on fixed-dimensional
compact `X` by real algebra; the same holds for each entry of `T`. Multiplication
and summation over the explicitly supplied coordinates preserve polynomial bit
length. No assumption that local block feasibility holds throughout the
enlarged parameter box is needed; empty fibers simply have no minimum graph.

## 2. Quantifier dimension and formula growth remain controlled

The proof uses a fixed number of compressed copies to construct the nominal
minimum graph and each measurement-fiber minimum graph. Each graph must be
eliminated before insertion into the growing collection of upper criteria.
The draft explicitly performs this necessary step.

Every `E_j(x,v,q)` and `B_j(x,v)` is computed by a separate fixed-variable
elimination. Different `T_j` can have a growing collective rank without changing
the number of real variables in any one elimination. The number of criteria is
bounded by explicit input length, so summing their polynomial output sizes is
polynomial. Conjoining these quantifier-free outputs uses the same leader and
single nominal-value variables, not a separate follower encoding per criterion.

The final worst-value and infimum formulas have only a fixed number of remaining
variables. They optimize globally over `x`; this is stronger than composing a
pointwise adversarial oracle with an unjustified polynomial-time outer solver.
The description contains no hidden high-dimensional leader search.

Degrees remain polynomial under the stated representation restriction. Products
of denominators from a growing number of blocks have polynomial degree, and the
number of monomials of polynomial degree in a fixed number of variables is
polynomial. The theorem would not follow for arbitrary binary-encoded exponents
of exponential numerical magnitude; the draft excludes those inputs.

## 3. Common-field output and attainment

At a feasible fixed leader, each near-optimal set is nonempty and compact, so
every continuous criterion maximum exists. This does not imply that the leader
infimum is attained. The proposed elimination of the bounded attainable-value
set, followed by membership of its infimum endpoint, correctly distinguishes
these cases.

When attainment holds, simultaneous algebraic sampling of the leader, nominal
value, worst measurement, and one compressed global fiber minimizer uses a fixed
total dimension. This yields one polynomial-degree real-algebraic field. All
local coordinates are rational expressions in that field with denominators
nonzero on their selected branches, so recovering a growing vector does not
multiply independent algebraic extension degrees.

This claim applies to one worst response, as stated. If witnesses for all
independent criteria are requested separately, each has polynomial encoding;
the theorem does not assert that all those unrelated witnesses can be packed
into one polynomial-degree common field. Such an assertion would require a
separate argument and can fail for independent square roots.

## 4. The fixed-normal convex subclass is sound

For a fixed constraint matrix, Hoffman's bound repairs a feasible point into a
nearby nonempty fiber with displacement tending to zero as polynomial right-hand
sides vary. Together with closed constraints and uniform bounds, this makes
`P(x)` continuous relative to the compact feasible-leader set. Neither a
constraint qualification nor a bound on the Hoffman constant polynomial in the
input is required for this qualitative continuity argument.

Positive-definite local quadratic costs plus convex aggregate cost give strict
convexity on each fiber. The nominal minimizer is unique and continuous. At a
positive budget, mixing any budget-boundary point with that minimizer makes the
cost strictly below the budget; the mixed point survives nearby fiber repair.
At a zero budget, the continuous unique nominal minimizer supplies the required
nearby choices. This establishes lower semicontinuity of the near-optimal
correspondence in both cases. Its closed graph and uniform bounds establish
upper semicontinuity. The continuous robust maxima therefore give a closed
admissible set and an attained minimum when feasible.

The proof needs convexity of the whole follower objective on each fiber. The
draft's convexity assumption on `phi(x,.)` and positive local quadratic blocks
is a sufficient condition. No hidden uniform strong-convexity constant is
required by this proof.

## 5. Additional boundary: positive budgets do not repair nonconvex attainment

The following example strengthens the zero-budget warning and is worth keeping
in the result's scope discussion. It is an elementary example, with no claim of
independent publication novelty.

Let

```
delta = 1/16,
x in [delta,1/8],  z in [0,1],
f(x,z) = z^2(1-z)^2 + x(3z^2-2z^3).
```

The nominal follower minimizer is uniquely `z=0` and its value is zero: both
terms are nonnegative on `[0,1]`, and the second is strictly positive for
`z>0` because `x>0`. This cost fits the quadratic-plus-aggregate model by taking
local quadratic cost `z^2`, one aggregate `w=z`, and absorbing the remaining
polynomial into `phi`.

Impose the robust upper constraint `z<=1/2` and minimize the leader objective
`x`. At `x=delta`, the response `z=1` has follower cost `delta`; it is included
in the near-optimal set and violates the robust constraint. At `x>delta`, every
`z>1/2` has follower cost strictly above `delta`. To verify the latter, use

```
f(delta,z)-delta = (z-1)^2 (z^2-2 delta z-delta).
```

The quadratic factor is positive on `[1/2,1]`: its value at `1/2` is `1/8`,
and its derivative is positive there. Therefore `f(delta,z)>=delta` on
`(1/2,1]`, and increasing `x` makes this inequality strict since
`3z^2-2z^3>0`. Consequently,

```
D = (1/16,1/8],
inf_(x in D) x = 1/16,
```

with no attaining leader. All constraint normals are fixed, the nominal
minimizer is unique, and the budget is a strictly positive constant. The missing
assumption from the unconditional-attainment subclass is convexity, which
prevents an isolated near-optimal component from appearing at the budget
threshold.

## 6. Independent exact checks

[The independent checker](../code/bilevel_reopened/nearoptimal_second_review.py)
uses Python rational arithmetic and does not import the repository solvers. It
checks three distinct boundaries:

- A nonconvex scalar follower with budget `9/256` whose worst response for
  `-(z-1/2)^2` occurs at the nonstationary points `1/4,3/4`. Restricting the
  adversary to unrestricted follower KKT points gives the wrong worst value.
- Exact affine-fiber minimum identities for diagonal quadratic costs, including
  collections of coordinate measurements whose combined rank grows with follower
  dimension. The symbolic witness factors show how an irrational worst response
  stays within one quadratic extension for each criterion.
- The polynomial factorization and sign conditions in the strictly positive
  budget nonattainment example above, plus rational sample exclusions.

Run command and observed output are recorded after execution below. These finite
checks support the audit's boundary analysis; the quantified dimension and
general algebraic complexity conclusions rest on the written proof.

```
python code/bilevel_reopened/nearoptimal_second_review.py
{"fiber_identity_points": 24603, "maxcut_cube_points": 5421, "maxcut_graphs": 75, "measurement_models": 35, "nonstationary_worst_response": 2, "positive_budget_polynomial_identity": 1, "positive_budget_sampled_exclusions": 2048}
```

## 7. Cross-check of the first reviewer's stronger nonattainment example

The first reviewer supplied a variation that needs no robust upper constraints.
Let `x in [0,1/16]`, `delta=1/16`, `c=delta+x`, keep `z in [0,1]`, and set

```
f(x,z) = z^2(1-z)^2 + c(3z^2-2z^3),
G(x,z) = 4x+z.
```

This reviewer independently verified that its robust objective has an
unattained infimum. At `x=0` the near-optimal set is `[0,a] union {1}`, with
`a=(1+sqrt(17))/16<1/3`, by the factorization in Section 5. At `x>0`, the
near-optimal set is exactly `[0,a_x]` for a unique `0<a_x<a`: the derivative

```
f_z = 2z(1-z)(1-2z+3c)
```

is positive up to `z=(1+3c)/2` and negative afterward, while `f(x,1)=c>delta`.
The initial root of `f(x,z)=delta` therefore gives the whole sublevel interval.
Implicit differentiation gives

```
|d a_x / dx| = a_x(3-2a_x) /
                 [2(1-a_x)(1-2a_x+3c)] < 9/4 < 4.
```

For the displayed bound, use `0<a_x<1/3` and `c>0`: the numerator is less
than one and the denominator exceeds `4/9`. The same bound holds along the
root branch through `x=0`, so `a-a_x<(9/4)x<4x`. Therefore
`W(x)=4x+a_x>a` for every positive `x`, `W(x)` tends to `a` as `x` tends
down to zero, and `W(0)=1`. Its infimum `a` is not attained. This boundary is
valid with fixed normals, strictly positive constant budget, a unique nominal
optimizer, and an affine upper objective, without upper constraints.

## 8. Optional simplification of the projection construction

The root agent proposed replacing the global fiber-minimum graph by existence
of a feasible fiber KKT point under the threshold. This simplification also
passes independent review. If any feasible point in a measurement fiber has
cost at most `v(x)+delta(x)`, then that compact fiber's global minimizer is a
fiber KKT point under the threshold. Conversely, a feasible fiber KKT point
under the threshold is itself a feasible near-optimal response. Thus the
thresholded projection needs no comparison against all other fiber KKT points.

The *nominal* value `v(x)` still must be the true global follower minimum;
the simplification applies only to the measurement-fiber existence predicate.
It also does not license restricting the adversary to KKT points of the
unrestricted follower problem. The original graph-of-fiber-minimum proof is
correct, so either formulation establishes the theorem; the thresholded KKT
formulation has fewer quantifiers.

## 9. Arbitrary quadratic upper criteria recover MaxCut

The root agent proposed the following boundary; this reviewer independently
verified the reduction. With no leader variables, resources, or aggregates, use
the follower `f(z)=sum_i z_i^2/2` on `[0,1]^N` and budget `delta=N/2`. Its
nominal value is zero and every cube point lies within the budget. Given an
unweighted graph, choose the upper criterion

```
G(z)=sum_{edges {i,j}} (z_i-z_j)^2.
```

The maximum over the cube equals the maximum cut size. Indeed, holding all
other coordinates fixed makes `G` a convex univariate quadratic, whose maximum
on `[0,1]` occurs at an endpoint. Successively replacing each coordinate by a
maximizing endpoint produces a binary vector with no smaller value. At a binary
vector, each edge contributes exactly one when it crosses the induced cut and
zero otherwise.

Therefore exact adversarial worst-value computation is NP-hard, already in this
uncoupled strictly convex quadratic follower subclass. Universal feasibility
`G(z)<=K` for all near-optimal `z` is coNP-complete on this subclass: its
complement has a binary cut certificate, and the standard MaxCut threshold
question `maximum cut >= K'` reduces to its violation with `K=K'-1`. These
complexity labels use the classical MaxCut hardness result; no new hardness of
box-constrained convex quadratic maximization is claimed.

This does not contradict arbitrarily many affine upper constraints. A single
growing-rank quadratic criterion combines information that cannot be checked
through its individual terms independently. In particular, the Hessian of a
criterion `p(Tz)` has rank at most the row count of `T`, whereas this criterion's
Hessian is twice the graph Laplacian and has rank `N-1` for a connected graph.
The fixed per-criterion measurement dimension is therefore a substantive
tractability restriction.

The independent checker enumerates every graph with up to four vertices and
checks all ternary cube points against the best binary cut. These finite checks
are supplementary; coordinatewise convexity proves the reduction for all real
cube points and arbitrary graph sizes.
