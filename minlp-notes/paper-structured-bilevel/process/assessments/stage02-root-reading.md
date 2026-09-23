# Root investigation during stage 2

Status: proposed development for author verification, not yet a reviewed result.

Root rechecked the canonical exact scalar/block/moving-normal proofs and the
fixed-core support-function appendix dependency. The main response proof must
retain global comparison and recover each follower by its rational local response
formula. Convexity of aggregate fibers helps explain compression but does not
make global follower stationarity sufficient.

## Direct fixed-core witness recovery proposal

The old fixed-core source uses Adler--Beling algebraic LP recovery. Root inspected
the actual primary text, Section 5 Remark 1, which states the rational bit-model
extension and its dependence on common field degree while outlining the details.
That source is consistent with the original argument, but the fixed aggregate
dimension permits a simpler constructive recovery that avoids the LP dependency.

Let `h=k+1` include shared constraints and the local linear objective. At the
sampled optimum `(x*,eta*)`, all coordinates lie in one polynomial-degree field K.
The polynomial support-sign-regime enumeration has already selected a tuple of
local vertices for each retained regime in `(x,lambda)`. Evaluate each tuple at
`x*`; retain it if every selected local vertex is defined and feasible. It need
not have a realizable original direction regime at this particular `x*`.

Every retained tuple's aggregate sum belongs to the Minkowski sum T of the local
linear images. Conversely, for every direction lambda, the actual sign regime
at `(x*,lambda)` selects a retained tuple attaining the support of T. Therefore
the finite hull of all retained sums and T have identical support functions and
are equal. The required shared/objective target belongs to that hull.

Caratheodory gives a representation with at most `h+1=k+2` sums. Enumerate subsets
of at most that size. An affinely independent successful subset has uniquely
determined barycentric weights; choose independent rows of its augmented matrix,
solve a constant-size system in K, then check every equality and nonnegativity.
Reconstruct every original local block with those same weights and the retained
vertex tuples. Local convexity and linear shared outputs guarantee feasibility
and the target objective. All coefficients remain in K. Fixed-size determinants,
polynomial input formulas and polynomially many sums bound their encoding.

The zero-dimensional/lower-dimensional case uses subsets of size at most h+1,
not an assumed full-dimensional simplex. Actual support regimes ensure at least
one feasible tuple whenever the original target is feasible.

This construction is only for the fixed-core appendix's linear local objective
and outputs. It must not be applied to the nonconvex follower reaction graph:
mixing true follower optima can create false follower choices. The main bilevel
recovery continues to use its rational response functions.

## Degree scope

The old fixed-core statement fixes input degree. Its proof appears to yield
polynomial time in actual degree and rational input length for fixed core, local
block, and aggregate dimensions. The author is asked to verify this extension
explicitly, including the support polynomials, products, sampling, and recovery.
No novelty claim is made for standard support functions or Caratheodory's theorem.

## Constant-Hessian degree refinement

Root proposed and independently checked the constant-local-Hessian refinement:
with fixed rational local normals and Q matrices independent of the leader,
all KKT inverses have rational constant denominators. Local responses, aggregate
candidate equations, and upper substitutions therefore have degree bounded by
a function of input degree and fixed dimensions, independent of block or row
count. Repeated fixed-dimensional quantifier elimination and joint sampling
preserve such a degree bound. Rational response evaluation adds no field.

Primary verification: Basu--Pollack--Roy (1996), Theorem 1.3.1 and Section 3.1.3
(the latter PDF pp. 27--28), explicitly give elimination and sampling degrees
independent of polynomial count. Coefficient lengths and total output length
still grow polynomially with input length. This refinement does not apply to
leader-dependent local Hessians or moving local normals without a separate
argument. It is a corollary of established degree bounds, not a priority claim.

## Independent draft proof reading

Root read the full stage 2 section and fixed-core appendix before external
review. Checked local KKT completeness after equality-row reduction and
conic support reduction; signed-determinant clearing; sign-condition selection
in fixed dimension instead of Cartesian branch enumeration; polynomial growth
of denominator products in fixed ambient dimension; and global comparison
against every feasible stationary candidate. Feasible candidates can include
nonglobal stationary points, but each global minimum is among them, which is
exactly the completeness/soundness argument used.

Checked that fixed-normal attainment uses the same global row matrix in
Hoffman's bound, allowing comparison points from the limiting feasible fiber
to be approximated in every nonempty approaching fiber. Moving normals retain
pointwise polyhedral KKT necessity but lose this argument, as the explicit
nonattainment example records. Pessimistic feasibility separately requires a
nonempty follower set, excludes any response violating any upper row, and
maximizes upper value over all global responses before optimizing the leader.
Infimum and attainment predicates are distinct.

The new support-tuple recovery uses common weights and checks all redundant
equations after a fixed-size independent-row solve; it covers lower-dimensional
images. The author's exact diagnostic checks hull coverage for all Cartesian
endpoint images of small interval sums and common-field reconstruction over
Q(sqrt(2)); this tests reconstruction, not general quantifier elimination.

One expository request was sent during authorship: distinguish absence of a
linear-independence assumption on local constraints from the required block
structure, and explain unique strictly convex minimization on each fixed
aggregate/resource fiber. Both are present in the current draft.
