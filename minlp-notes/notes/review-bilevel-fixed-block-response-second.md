# Second independent audit of the fixed-block bilevel algorithm

Date: 2026-09-05. Reviewer: `binary_formulation_review`.

**Verdict: PASS.** I independently checked
[the promoted fixed-block theorem](../results/bilevel-fixed-block-response-algorithm.md),
including growing local row counts, degenerate local polyhedra, rational branch
enumeration, polynomial bit complexity, common-field recovery, and attainment.
No required correction was found. I also reviewed the current scalar theorem on
which its global comparison and real algebraic steps depend.

## Equality quotient and independent conic support

The full follower feasible set is a polyhedron for each fixed leader. Thus every
global follower minimizer has the necessary polyhedral normal-cone multipliers,
without any Slater, independence, or interior assumption. After fixing the
aggregate and shared multipliers, each block satisfies the KKT conditions of
the displayed local quadratic program. Its positive definite Hessian makes these
conditions sufficient and its feasible optimizer unique. This auxiliary local
convexity does not assert convexity of the global follower objective.

Let `L` be the row space of the original local equality matrix, and project the
active inequality normals into the quotient by `L`. A normal-cone contribution
is a nonnegative combination of these projected vectors. Suppose its current
positive-support projected vectors have a linear dependence
`sum_j alpha_j gbar_j=0`. Choose its sign so at least one `alpha_j>0` and set

```
t = min_{alpha_j>0} lambda_j/alpha_j.
```

Replacing the positive coefficients by `lambda_j-t alpha_j` keeps all
coefficients nonnegative, preserves the represented quotient vector, and removes
at least one positive coefficient. Repeating leaves linearly independent
projected vectors. Zero projected vectors are removed in the same way. The
discarded contribution is in `L` and is absorbed into the unrestricted equality
multipliers.

Consequently, at most `d_b-rank(E_b)` inequality normals are needed, independent
together with an equality row basis. This proof works for cones with lineality,
opposite active inequalities, and zero normals. It does not require a pointed
normal cone or a nondegenerate vertex. All selected inequalities remain active,
so the reduced coefficients still satisfy complementarity.

A diagnostic case is the singleton defined in two dimensions by `y_1=0` and
the two inequalities `(1,1)y<=0` and `(-1,-1)y<=0`. The quotient normal cone is
the whole one-dimensional space. Either sign of an arbitrary required quotient
normal is represented using just one of the two inequalities, independent
together with the equality. The method does not need to retain both opposite
rows in the saddle-point matrix.

Retaining every original equality as a feasibility test is necessary and is
done in the theorem. For example, selecting a basis from the two rows
`y_1=e_1(x)` and `2y_1=e_2(x)` must not erase the consistency condition
`e_2(x)=2e_1(x)`.

## Rational branches and sign tests

For an enumerated independent set of rows `V`, the homogeneous saddle-point
system gives `Vy=0` and `Q_b y+V^T theta=0`. Multiplication by `y^T`, followed by
positive definiteness, gives `y=0`; row independence then gives `theta=0`.
The matrix is therefore nonsingular everywhere on `C`, including when its
active subset does not describe a feasible branch.

Each primal and multiplier coordinate has a Cramer representation `n/Delta`.
Replacing it by `n Delta/Delta^2` is exact and gives a positive denominator
on `C`. All original primal equalities and inequalities and all selected
inequality-multiplier signs can be checked after multiplication by that same
positive denominator. The selected active equalities and stationarity already
hold by the solved system. Nonselected inequality multipliers are zero.

A branch passing these tests is therefore the unique local optimizer. Conversely,
the conic-support argument proves that every local optimizer passes some branch.
Several passing branches may return different multipliers, but they return the
same primal block. This is the precise uniqueness property needed to select the
first passing branch. Uniqueness of multipliers is unnecessary.

There are at most `sum_{j=0}^{d_b-t_b} binomial(m_b,j)` subsets per block.
Testing row independence and selecting an equality basis use rational linear
algebra. Because `d` is fixed, the total number of subsets and the total number
of original-row feasibility tests across all branches are polynomial in input
length, even when local row counts grow.

All branch tests are polynomials in the same fixed-dimensional vector
`(x,w,lambda,mu)`. Joint realizable sign conditions determine every branch's
validity. Enumerating these conditions, including zero signs, has polynomial
cost and count under the degree assumptions. On a condition intersecting `C`,
choosing one passing branch per block loses no response by local uniqueness.
This avoids the potentially exponential Cartesian product of branch lists.
The formulas are used together with `x in C`; no invertibility or positive
definiteness outside `C` is needed.

## Degree, bit complexity, and recovery

Let `delta` bound actual input degree. The effective linear costs have degree
`O(delta)`, including polynomial `U(x)` and the aggregate derivative. Each
saddle-point matrix has size at most `2d`, so its determinant, Cramer
numerators, squared denominator, and all cleared tests have degree
`O(d delta)` and polynomial coefficient bit length.

The total number of these polynomials is polynomial in the original input.
On each retained sign condition, multiplying one denominator from every block
gives degree `O(B d delta)`. Coordinate numerators have a comparable bound.
The common denominator is positive on `C`. Shared constraints, complementarity,
and follower values can therefore be cleared exactly, including the quadratic
cross terms inside each block. The aggregate term is evaluated at `w`.
Substitution of upper polynomials of degree at most `delta` gives polynomial
degree, for example `O(B d delta^2)` suffices after increasing constants.

Every expansion uses a fixed number of compressed variables. The number of
possible monomials of polynomial degree is therefore polynomial, and coefficient
bit lengths remain polynomial under the required products and sums. These are
bit bounds, not merely arithmetic operation bounds. The degree-controlled
explicit input representation is material; succinct binary exponents encoding
exponentially large degree are excluded as stated in the scalar theorem.

The real algebraic imports were checked directly in my
[scalar audit](review-bilevel-fixed-aggregate-response-third.md):
[Basu–Pollack–Roy](https://www.math.purdue.edu/~sbasu/jacm95.ps), Section 1.3 and
Theorem 1.3.1, control formula length and intermediate/output bit sizes, while
Section 3.1.3 constructs sample points as common univariate representations.
Both competing follower copies and, for optimization, a competing upper tuple
have fixed total dimension. Thus quantifier elimination and simultaneous
sampling have polynomial bit complexity here.

Every recovered follower coordinate is a rational function of one selected
compressed algebraic sample. Evaluating these functions in its common field
does not introduce a fresh algebraic extension per block. All denominators are
nonzero at the selected leader. Returning the entire growing follower vector
therefore has polynomial total encoding length and recovery cost.

## Global optimality and attainment

The assembled compressed formula represents exactly feasible follower KKT
points. Every global follower minimizer appears, and every represented point
is feasible. Comparison against all represented values consequently enforces
global follower optimality even when the aggregate objective is nonconvex.
The comparison includes no upper-level restrictions on competing responses.

For each instance, the full matrix of all local, shared, and coordinate-bound
normals is independent of the leader. Its size may grow across instances, which
does not affect the needed uniformity of Hoffman's constant within one instance.
Only continuous right-hand sides vary. Along a convergent sequence of global
response pairs, every feasible comparison at the limiting leader has nearby
feasible comparisons by Hoffman's bound. Passing the objective comparisons to
the limit proves that the response graph is closed.

Continuous coordinate bounds over compact `C` give uniform boundedness. The
upper weak inequalities are closed. Thus the optimistic feasible graph is
compact and its upper polynomial objective attains a minimum whenever feasible.
Auxiliary multipliers may be unbounded; they are not part of this compactness
argument and do not obstruct algebraic sampling.

## Attribution and scope

I read Section 4 of
[Megiddo–Tamir (1993)](https://theory.stanford.edu/~megiddo/pdf/qtranrev.pdf).
Their general model separates small convex quadratic blocks after introducing
shared resource multipliers and describes the resulting local responses through
complementarity. Their linear-time model fixes local row counts as well as local
dimensions. The present theorem allows growing row counts at polynomial cost;
the independent-support enumeration above justifies that distinction. The local
technique remains an established antecedent and is correctly credited.

This audit establishes correctness of the stated extension, not universal
novelty. Positive definiteness, fixed block dimension, fixed compressed global
dimensions, fixed feasible-set normals, and the explicit degree condition are
the assumptions used by this proof.
