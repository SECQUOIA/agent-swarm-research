# Independent second review: cactus objectives with few flow measurements

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Candidate: [few-measurement convex maximization](potential-flow-cactus-few-measurement-maximization.md).
Verdict: **PASS** under the fixed-nomination quadratic cactus model stated
in the cited flow-region theorem, including its assumption that physical
operating bounds do not filter resistance scenarios.

This review verifies the complete geometric and bit-precision argument.
It does not claim publication priority for the zonotope method or an exact
algorithm for comparing independent radical sums.

## Flow-region dependency and rational endpoint recovery

The promoted [cactus flow-region theorem](../results/potential-flow-cactus-flow-region-and-optimization.md)
has the precise structure needed here. For fixed balanced rational
nominations, bridge flows are fixed and each cycle contributes one independent
circulation interval. The circulation endpoints have separate quadratic
algebraic encodings, and each is realized by a rational resistance endpoint
scenario computable by comparison with rational flow-sign breakpoints.

The interval-resistance flow region is exactly `x0+Z[l,u]`. For finite
sets, it is the convex hull of the original attainable flow region, and
every corner of the circulation box is realized by a combination of
original endpoint scenarios. Cycle blocks use disjoint resistance data
and fixed effective nominations, so the endpoint choices can be combined
independently. Bridge resistances can be any allowed values.

These statements would not automatically survive extra operating constraints
that exclude physical scenarios. The current theorem inherits the unfiltered
scenario scope from its explicit dependency. Fixed nominations and the cactus
structure are likewise substantive assumptions.

Applying the rational measurement matrix gives the affine zonotope
`Rx0+sum_C a_C[l_C,u_C]`, with `a_C=RZ_C` rational. Translation has no
effect on its exposed vertices. Algebraic segment lengths therefore cause
no algebraic coefficients in the sign-cone enumeration.

## Exact sign-cone enumeration and its complexity

For each nonzero rational generator direction, insert the hyperplane
`h^T a_C=0`. A strict sign pattern is feasible exactly when the rational
linear inequalities `sigma_C h^T a_C>=1` are feasible. One implication is
immediate. For the other, take any point satisfying all finitely many strict
inequalities and scale it by the reciprocal of their smallest positive
margin. No bound on the magnitude of that scale is assumed computationally;
ordinary rational linear feasibility yields a polynomial-bit feasible
representative directly.

Each feasible strict sign region is open in the ambient measurement space.
Incrementally extending all retained sign patterns by the two signs and
testing feasibility therefore enumerates exactly the full-dimensional
regions of the arrangement. Rational LP feasibility has polynomial bit
complexity, including for thin or unbounded cones. The number of retained
regions at every prefix is polynomial for fixed measurement dimension.
Thus the total number of tests, their row counts, and their coefficient
lengths are polynomial for fixed `k`. The asserted `N^{O(k)}` running-time
form is appropriate; this is not an FPT claim in `k`.

Repeated directions, opposite directions, and more general dependencies
only make some sign patterns infeasible. They do not increase the standard
arrangement bound. A zero direction is removed before the tests. With
no remaining directions, the empty sign pattern suffices and the
measurement region is a point.

The classical vertex-count and exposing-direction mechanism is explicitly
supported by [Onn and Rothblum, Lemmas 2.1 and 2.2, PDF page 4](https://arxiv.org/pdf/math/0309083),
which was opened directly during this review. The candidate's rational
incremental feasibility implementation supplies its own bit-level route
to the required regions. No novelty of this mechanism is inferred.

## Every actual vertex is covered despite degeneracies

For a nonzero direction `a_C` and positive length `u_C-l_C`, any generic
normal `h` uniquely maximizes the corresponding segment at `u_C` or
`l_C` according to the sign of `h^T a_C`. Segment optimization separates,
so the sum of these choices is the uniquely exposed zonotope point.

Conversely, every vertex of a polytope has an exposing normal whose
inequalities against all other vertices are strict. The set of such
normals contains an open subset of the ambient space, even if the
polytope lies in a proper affine subspace: normals orthogonal to that
subspace add lineality without destroying the strict inequalities.
This open set contains a normal avoiding all finitely many nonzero
generator hyperplanes. Its sign pattern is enumerated and selects the
given vertex.

Zero-length intervals do not invalidate this argument. Their extra
hyperplanes may split a vertex's normal cone into smaller regions, but
cannot cover an open set or remove every generic exposing normal.
Their two endpoint circulations coincide, so their endpoint choice has
no effect on the resulting measurement. A zero measurement direction
likewise has no effect even if its circulation interval has positive
length. Either precomputed endpoint scenario can be used in both cases.
The point case has the whole ambient space as its normal cone and is
also covered.

The selected circulation endpoints always have exactly realizable rational
resistance scenarios. Neither the signs of independent radical expressions
nor exact projected vertex coordinates are needed to generate this list.
Repeated candidates and duplicate projected vertices can be retained
without affecting completeness or complexity.

## Convexity and finite versus interval uncertainty

A continuous convex function on a compact polytope attains a maximum at
some vertex: express any point as a convex combination of vertices and
apply convexity. The promised convexity box contains the attainable
measurement set and, being convex, its convex hull. Thus the argument is
valid both for interval uncertainty and for the convex hull of finite
uncertainty.

For finite sets, every actual projected vertex in the enumeration is
realized by an original finite resistance scenario. All other finite
states lie in the zonotope. Consequently the maximum over the original
finite states equals the maximum over that zonotope, and the same finite
candidate list contains an optimizer. The argument concerns maximization;
it provides no analogous conclusion for convex minimization.

The polynomial need not be strictly convex or have nonnegative
coefficients. Affine or constant terms are harmless. Its convexity is
only promised on a box containing the true attainable region. The larger
box used next for a derivative bound need not satisfy that convexity
promise, since a polynomial is differentiable there regardless.

## Measurement bounds and an explicit additive guarantee

Let `B=sum_v |b_v|`. The standard passive-flow bound `|x_e|<=B` is valid
here. One direct justification is to orient nonzero physical flows in
their actual direction. Potentials strictly decrease along such arcs,
so there is no directed cycle. Decomposing the conserved flow into paths
from positive to negative nominations bounds any arc flow by the total
positive nomination `B/2`, and hence by the stated weaker bound `B`.
If nominations vanish, strict passive laws give the zero flow.

Therefore `T=B max_j sum_e |R_je|` bounds each measurement in absolute
value. On `[-T-1,T+1]^k`, every partial derivative of the polynomial has
a rational upper bound obtained from its absolute coefficients and the
radius raised to the relevant monomial powers. Taking the maximum with
1 gives `L>=1`. For fixed `k` and densely encoded degree, computing this
bound uses polynomial arithmetic and yields polynomial bit length, even
when its numerical magnitude is large.

Let `A_*=max_j sum_C |a_jC|` to distinguish this quantity from other
uses of the letter `M`. Approximating each selected circulation to absolute
error

```
delta<=min(1/(1+A_*), epsilon/[8kL(1+A_*)])
```

gives coordinatewise measurement error at most `A_* delta<=1`. The
approximate measurement and the entire segment to its true value lie
inside the enlarged derivative box. The mean-value estimate is therefore

```
|g(y_approx)-g(y_true)|
 <=L sum_j |y_approx,j-y_true,j|
 <=kL A_* delta
 <=epsilon/8.
```

This is a bound on actual polynomial value error, not a heuristic
floating-point comparison. Each quadratic endpoint can be enclosed
separately to the required absolute accuracy in polynomial bit time.
The rational approximate measurement is then evaluated exactly by dense
polynomial arithmetic. The chosen accuracy has polynomial binary length
in the original input and requested accuracy bits. Independent quadratic
fields are never assembled into one exact field.

If the algorithm chooses the candidate with greatest rational estimate,
its true value is at least the true best candidate value minus
`2*(epsilon/8)=epsilon/4`. The complete candidate list contains a global
optimizer, so this implies the stated additive `epsilon` guarantee with
slack. Ties in the rational estimates can be broken arbitrarily.

The algorithm returns the exact rational resistance vector precomputed
for the chosen endpoint combination. Approximate circulations are used
only to compare objective values, not as claimed realizable physical
flows or as substituted resistance data. Its physical flow may remain
irrational. This distinction is handled correctly by the theorem.

The cases `B=0`, all measurement directions zero, or a constant objective
can be handled immediately. Zero widths with nonzero directions can
also be left to the general enumeration. No division by a width or
by a possibly zero generator occurs.

## Fixed-rank convex quadratic specialization

For rational PSD `Q`, exact rational pivoted LDL elimination gives
`Q=L D L^T` with exactly `rank(Q)` positive diagonal pivots and rational
factors of polynomial encoding. Zero residual pivots in a PSD Schur
complement have zero residual rows and columns and can be omitted.
Equivalently the quadratic form is a sum of rational nonnegative
multiples of squares of rational linear forms, without irrational
eigenvectors or square-root factors in the measurement matrix.

Use these forms plus `d^T x` as measurements. The objective becomes a
convex quadratic with at most `rank(Q)+1` variables, whose last variable
appears only affinely. Linear dependence among the forms, a zero affine
term, and rank zero cause no difficulty; redundant or zero measurements
can be retained or omitted. Fixed rank therefore gives fixed measurement
dimension and the preceding polynomial bit algorithm. No claim is made
when rank grows with input size.

## Supporting numerical checks

Inspected and reran
`code/potential_flow_mpd/cactus_few_measurement_checks.py`. It passed
18 convex quartic projection examples in one to three measurement
dimensions, comparing 286 sign cones against 1,512 exhaustive circulation
endpoint combinations. Cases include zero directions, repeated directions,
and zero interval lengths. The objectives are sums of quartic, quadratic,
and affine terms and are convex.

These are numerical checks: cone feasibility uses floating-point linear
programming, and algebraic endpoints are evaluated at 70-digit precision.
They do not certify exact rational cone feasibility or the general
additive bound. The analytic and rational-complexity arguments above
supply those guarantees. No correction was required by this review.
