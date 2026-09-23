# Second independent audit: varying-normal bilevel responses and infimum semantics

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS.** I independently checked
[the compressed-response infimum theorem](../results/bilevel-compressed-response-infimum-semantics.md)
and its complete proposed extension to
[polynomial local constraint normals](bilevel-moving-local-normal-extension.md).
The latter may be integrated into the result. The review covers rational
branch completeness at changing ranks, the optimistic and pessimistic
formulas, and exact infimum and optimizer output. The previously audited
fixed-dimensional real-algebraic algorithms and positive-definite local
quadratic block theorem are imports, not new claims in this review.

## Varying local ranks

For each fixed leader, local constraints still define a polyhedron. A
strictly convex positive-definite quadratic has a unique minimizer on
every nonempty bounded local fiber. Its KKT conditions are necessary and
sufficient without Slater or independence of the original constraint rows.

Enumerating all pairs of equality-row and inequality-row subsets `(I,J)`
with `|I|+|J|<=d_b` is polynomial for fixed block dimension. This includes
the empty pair. The construction does not choose an equality basis once
for all leader values.

For each pair, let `V` be its selected normals and use the saddle matrix
`M=[Q,V^T;V,0]`. At a leader where `Q` is positive definite, `M` is
nonsingular exactly when `V` has independent rows. If `V` is dependent,
a nonzero vector in the kernel of `V^T` gives a null vector of `M`.
Conversely, a null vector satisfies `Vy=0` and
`y^T Qy=0`, implying `y=0`, then its multiplier component is zero by row
independence. The explicit branch guard `det(M)^2>0` is essential.

After this guard, Cramer's rule and the squared determinant give genuine
rational coordinates with positive denominator. Testing all original
primal rows and the signs of selected inequality multipliers is sufficient
for branch soundness: omitted multipliers can be set to zero, so the
candidate satisfies full local KKT conditions. No additional equality-span
test is needed.

For completeness, at any particular feasible leader choose an actual basis
`I` of its equality row space. Project active inequality normals and the
normal-cone representation of the minimizer's negative gradient into the
quotient by that space. A nonnegative conic representation can have its
positive support reduced until the projected generators are independent:
move coefficients along a dependence until one vanishes, preserving
nonnegativity. There are at most `d_b-rank(E_b(x))` selected inequalities.
Lifting back gives independent rows together with `I`, so this enumerated
branch has nonzero determinant and represents the minimizer. The argument
is pointwise and covers all equality-rank changes.

Every valid branch at the same compressed point returns the same local
minimizer. Thus sign-condition enumeration followed by choosing the first
valid branch loses no responses. Determinant nonvanishing and every branch
test must be among those sign conditions, as the extension specifies.
The product of the selected squared determinants is positive on its own
regime; no assertion of positivity away from that regime is used.

## Diagnostics for the rank argument

I checked the following examples symbolically with exact SymPy arithmetic:

- For scalar local cost `y^2/2-y` and equality `xy=0`, the nonempty equality
  branch has saddle determinant `-x^2` and solution `(y,lambda)=(0,1/x)`
  when `x>0`. At `x=0`, the empty equality branch correctly returns `y=1`.
  Clearing the singular branch without its guard would be invalid.
- In two dimensions with cost `(y_1^2+y_2^2)/2-y_1-y_2` and local matrix
  `diag(x,x)`, the full saddle determinant is `x^4`. The optimum changes
  from `(0,0)` for positive `x` to `(1,1)` at zero. This checks a rank drop
  of two and the necessity of including the empty pair.
- With equality `y_1=0` and cost `(y_1^2+y_2^2)/2-y_2`, the unconstrained
  minimizer `(0,1)` is feasible. The empty equality subset is therefore a
  valid response branch even though it does not span the equality space.

These checks passed. They supplement the general proof rather than replace
it; no full quantifier-elimination implementation is claimed.

## Compression and bit complexity

The block saddle matrices have size at most `2d`. Polynomially varying
local and shared normals therefore preserve polynomial-degree determinant,
adjugate, numerator, and feasibility-test encodings. The number of branch
tests is polynomial for fixed `d`, even with unbounded local row counts.
Their sign conditions live in the fixed-dimensional leader, aggregate,
and shared-multiplier space. Local multipliers are solved rationally;
they are not added as quantified variables for every block.

Common-denominator products and upper-polynomial substitution occur only
after this dimension reduction. Their expanded degrees and coefficient
heights are polynomial in the input length and actual input degree.
Consequently the growing-degree encoding condition from
[the separate degree audit](review-bilevel-fixed-aggregate-response-degree-complexity.md)
continues to suffice. Singular branch boundaries are included through
other valid branches, never through division by zero.

Pointwise KKT necessity for the complete follower polyhedron gives every
global minimizer a compressed representation. Every represented KKT point
is primal feasible. Comparing all represented KKT values therefore still
enforces global follower optimality even when the aggregate objective is
nonconvex and all constraint normals vary.

## Optimistic and pessimistic quantifiers

Under optimistic semantics, impose the upper constraints on the selected
global follower optimum. The resulting attainable upper-value set has the
same fixed-variable description as before. No reaction-graph closedness
is needed to describe this set or decide its emptiness.

Under the stated pessimistic convention, `Bad(x)` is true if any global
follower optimum violates any upper constraint. The strict violation
`g_j>0` correctly complements the weak admissibility condition. The
separate nonempty-response clause excludes infeasible followers instead
of admitting their leaders by vacuity. The objective predicate `T` includes
all global follower optima without first filtering by upper constraints.
`Worst` requires a realized upper value that dominates every such value,
so it represents exactly the stated pessimistic objective.

For each fixed feasible leader, the follower feasible fiber is closed and
bounded and its polynomial objective is continuous. Its argmin set is
therefore compact, and the worst upper value is attained there. This
pointwise fact does not imply leader-level attainment.

The formulas use a fixed number of copies of the response predicate.
Regime alternatives and the unbounded list of upper constraints are
quantifier-free disjunctions sharing the same compressed variables.
Eliminating the internal response quantifiers once is also valid. Either
route avoids introducing a separate quantified block for each regime,
constraint, local row, or follower block. Duplicated response multipliers
or overlapping valid branches do not alter the visible response sets.

## Infima, attainment, and algebraic output

Compact `C` and finite continuous polynomial coordinate bounds provide a
uniformly bounded enclosing set for every follower response. The upper
polynomial is bounded on this enclosure, even when the actual reaction
graph or admissible leader set is not closed. Thus each feasible
optimistic or pessimistic problem has a finite infimum.

Quantifier elimination yields the corresponding nonempty bounded
univariate semialgebraic value set `V`. Its infimum is a real-algebraic
endpoint, and membership of that endpoint in `V` decides attainment. The
displayed lower-bound and arbitrarily-close-value formula also
characterizes this endpoint exactly; its quantified variable count is
fixed. Empty problems must be reported as infeasible rather than assigned
a finite infimum, as the result's conditional statement requires.

When attainment holds, simultaneously sampling the infimum formula and an
encoded attaining response yields all compressed coordinates and the
value in one polynomial-degree algebraic extension. In the pessimistic
case the appended response equation returns a global follower optimum
realizing the worst upper value. Positive-denominator rational evaluation
recovers all follower coordinates in the same extension. There is no
unbounded product of independent coordinate fields.

The fixed-dimensional degree, intermediate-bit, and sampling guarantees
are the standard ones stated in
[Basu's survey, Theorems 2.15, 2.18, and 3.6](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf).
These algorithms do not require a bounded set of multiplier witnesses.

## Scope and counterexamples

The example `xz=0` with follower cost `(z-1)^2` correctly gives optimistic
infimum zero without attainment for upper objective `x+z`. It applies
equally when this equality is regarded as a moving local row.

For the fixed-normal example
`f(x,z)=z^2(1-z)^2+xz` on the unit square, the response is uniquely zero
at positive leaders and is `{0,1}` at zero. Consequently `F=x+z` gives
pessimistic values `W(x)=x` for positive `x` and `W(0)=1`. Adding robust
upper constraint `z<=1/2` excludes exactly the zero leader. Both
nonattainment and nonclosed robust admissibility claims are correct.

The broader theorem must retain uniform coordinate bounds, positive-definite
local quadratic blocks, fixed structural dimensions, and the polynomial
degree encoding. It computes an infimum and decides attainment; it does
not restore the narrower fixed-normal optimistic attainment guarantee.
No substantive defect remains under these conditions.

## Integrated result reread

I reread the integrated result after Section 1 incorporated all varying
local normals and both corollaries adopted the broader scope. The
determinant guards, rank argument, assumptions, and semantic formulas match
the reviewed extension. This integrated version also passes. I requested
one prose correction: the vector represented by outward active inequality
normals is the local objective's **negative** gradient. The KKT systems
and multiplier signs in the construction were already correct.
