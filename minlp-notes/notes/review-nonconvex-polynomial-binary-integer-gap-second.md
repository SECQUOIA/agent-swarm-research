# Independent second review: nonconvex polynomial integer-count gap

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Candidate: [nonconvex polynomial binary/integer gap](nonconvex-polynomial-binary-integer-gap.md).
Verdict: **PASS** for the explicit family, finite convexity-interval bound,
and compact dense-polynomial upper bound.

The compact upper bound imports the hybrid theorem and signed-curvature
integration lemma, both independently checked in
[the hybrid audit](review-compiled-convex-polynomial-hybrid-precision-second.md).
Thus that dependency is closed from this review's perspective, irrespective
of an older pending-status sentence in the candidate. No publication
priority claim is made here.

## Explicit rational family and approximation

The triangular wave has slopes `2M` and `-2M`, is continuous at all peaks
and period boundaries, and is globally `2M`-Lipschitz. Its range is `[0,1]`.
For `N=(32M)^2`, the Bernstein weights form the binomial distribution,
so the displayed expectation identity is exact. The binomial variance
and Cauchy--Schwarz give

```
|q_M(x)-T_M(x)|
 <=2M sqrt(x(1-x)/N)
 <=M/sqrt(N)=1/32.
```

The bound is uniform, including the endpoints, and uses no convergence
claim without an explicit rate. All sample values are rational; in fact
the chosen `N` is divisible by `M`, and their denominators divide a
number of polynomial bit length in `M`.

The Bernstein representation has `N+1` terms with coefficient lengths
polynomial in `N` and `log M`. Expanding `(1-x)^(N-k)` produces at most
polynomially many binomial-coefficient products and sums. These have
polynomial bit length; the relevant binomial coefficients have `O(N)`
bits. Thus the ordinary dense rational monomial input can be constructed
in time polynomial in `N` and `log M`. There is no assertion of a
polynomial-size representation in `log M` alone, and none is needed.

## Two general integer variables

The integer period variable `z` with bounds `0<=z<=M-1`, the integer
orientation variable with bounds `0<=b<=1`, and the two linear branches
give exactly the triangular wave under `x=(z+t)/M`.
Global bounds on `t` and `y` permit finite constant deactivation bounds
for the two branches. The dependence on `M` appears only in ordinary
rational linear coefficients and the period bound.

All interior periods, shared boundaries, and `x=1` are covered. At a
shared boundary either neighboring period representation gives `y=0`.
The last point is represented by `z=M-1,t=1`.

Adding the band of radius `1/32` about this exact wave contains every
graph point of `q_M`. Every admitted output is within `1/16` of `q_M`,
which is strictly below the fixed allowed tolerance `1/4`. This is an
ordinary rational MILP and hence also a valid convex lift with two general
integer variables. The binary orientation variable is counted as one
of those two; it is not omitted from the count.

## Binary lower bound uses full assignments

At every peak the polynomial is at least `31/32`. At every trough it
is at most `1/32`. Between any two distinct peaks there is a trough.
If exact graph witnesses for two peaks had the same full binary vector,
convexity of that continuous slice would admit every convex combination
of the witnesses. In particular the graph chord at the intervening
trough input would have output at least `31/32`, producing error at
least `30/32>1/4`.

Therefore the `M` peak graph points require distinct full binary
assignments. This proves `2^p_bin>=M`, even when the binary formulation
allows nonlinear convex constraints and unlimited continuous auxiliaries.
It is not a parity argument: the needed interpolation parameter at the
trough is arbitrary, and two general integer witnesses with equal parity
would not ensure integral coordinates for that interpolation. The candidate
correctly keeps this distinction explicit.

Combining the two bounds gives
`p_bin-p_conv>=ceil(log2 M)-2`. At least `2M` distinct roots of
`q_M-1/2` occur in the alternating trough/peak intervals, while its degree
`d_M` is at most `1024M^2`. Hence the actual degrees tend to infinity
and

```
p_bin-p_conv >= (1/2)log2(d_M)-7.
```

This justifies logarithmic growth in actual degree along the family
without claiming that every dense expansion has degree exactly `N`.

The final added upper bound for this family is also valid. Replace the
period integer by `z=sum_j 2^j b_j` using `ceil(log2 M)` binary bits and
retain its bound `z<=M-1`. This represents every allowed period and
excludes unused codes. Keeping the single orientation bit gives the
same rational wave-band formulation with `ceil(log2 M)+1` binaries.
Thus the example's binary optimum lies between `ceil(log2 M)` and
`ceil(log2 M)+1`. No extra integer variable is hidden by the linear
definition of `z`.

## Finite upper bound from convexity intervals

Restricting an admissible general-integer convex lift to an input interval
adds only linear constraints and retains exact graph coverage there.
Negating the output on a concave piece is an invertible linear map and
preserves the absolute-error model and integer count.

The reviewed scalar parity argument and three-way chord refinement then
give at most `3*2^p` admissible chord intervals on each of the `s` pieces.
Their band union contains the entire graph and satisfies the prescribed
error. On a concave piece the band's vertical orientation is reversed;
the same error and containment proof applies after undoing the output
negation. All intervals are compact, so finite valid bounds exist for
the finite linear disjunction.

A union of at most `3s*2^p` bounded polyhedra can be encoded with
`p+ceil(log2(3s))` binaries. Taking `p=p_conv` is legitimate because
the feasible integer counts form a nonempty subset of the nonnegative
integers: continuity supplies a finite chord-band construction. No
attainment of an optimization over coefficients or partition lengths is
being assumed merely from taking the minimum count.

For a nonaffine polynomial, its nonzero second derivative has at most
`D-2` distinct roots. Between roots its sign is constant, giving at most
`max(1,D-1)` convex or concave pieces. Repeated roots may create unnecessary
pieces but do not invalidate the bound. Irrational boundaries are permitted
only in this finite real-coefficient upper bound, as explicitly stated.

The definition of `p_bin` in this note permits binary convex lifts. The
constructed upper bounds use the smaller class of binary linear lifts,
while the lower bound applies to the larger class, so both directions
remain consistent.

## Compact rational upper bound for arbitrary dense polynomials

Use the rational absolute derivative bound `M_1=max(1,sum k|c_k|)`.
Disjoint rational brackets of width at most
`min(1,epsilon/(32M_1))` around the distinct interior roots of `f''`
have polynomial endpoint encoding and are computable in polynomial time.
Endpoint roots need no brackets. There are at most `D-2` interior roots,
so the asserted total of at most `2D` bracket and complementary pieces
is conservative and valid. Affine polynomials are handled separately.

Every complementary piece is convex or concave. Normalize its rational
input interval, negate a concave output, and apply the reviewed hybrid
construction. Restricting a global `p`-integer lift shows that the local
optimum is at most `p`. Each local construction therefore has an actual
binary capacity at most `2^(p+11)`. The algorithm does not need to
compute `p`; this is only a comparison bound on its explicitly computed
local counts.

A narrow bracket does not require convexity. Its chord slope and function
are both bounded in Lipschitz constant by `M_1`. Comparing at an endpoint
gives absolute chord error at most `2M_1 h<=epsilon/16`. A symmetric
band of radius `epsilon/16` about that exact chord contains its graph
and admits only absolute error at most `epsilon/8`. Rational endpoints
and exact dense polynomial evaluation make this a single rational cell.

Concatenating actual local cell families yields
`K<=2D*2^(p+11)` and hence
`ceil(log2 K)<=p+12+ceil(log2 D)`. The local counts have polynomial
binary encoding even if their numerical values are large. The global
index can select a piece and a local index by comparisons and subtraction,
using the already audited cumulative-index circuit. Its construction is
polynomial because the number of pieces and every indexed local routine
are polynomially bounded. Unused index codes can be excluded.

The bands on convex pieces, concave pieces, and brackets have different
constant offsets. A global indexed circuit can output their rational
offset data as well as their endpoint data. These offset bits are forced
by the input index and enter linearly; they need no integrality declaration.
Negating a concave local output reverses the asymmetric band exactly.
Interpolation still uses a single common continuous weight within the
selected cell. Nested rational input normalizations admit a common
denominator of polynomial bit length by the same denominator-product
argument as the hybrid proof.

The final compiler clarification is correct and useful: exact bracket
endpoint output values can have nondyadic denominators. Include their
polynomially many denominators in the common output denominator, together
with the local hybrid output denominators. Their product has polynomial
bit length. A fixed integer offset then encodes signed output values as
nonnegative binary numerators. This preserves the exact bracket chords
and their `epsilon/8` admitted-error bound without assuming their values
are dyadic or spending an uncounted rounding allowance.

Thus the concatenated formulation is rational, polynomial in the dense
input and tolerance encoding, contains every exact graph point, and
satisfies the absolute-error restriction. Taking `p=p_conv` proves the
claimed bound. The explicit family supplies an `Omega(log D)` lower
overhead even for unlimited-size binary convex lifts, so logarithmic
degree dependence is the correct worst-case order. Neither direction
claims a lower bound on continuous dimension or solver running time.

No mathematical correction was required by this audit. The compact upper
bound's dependency is independently verified in the linked hybrid review;
the candidate's pending-review wording can be updated when the author
collects the other required reviews.

## Supporting exact computation

Inspected and reran `code/quadratic_rank/check_polynomial_binary_integer_gap.py`.
It passed 12 exact rational Bernstein evaluations at approximation degrees
4096 and 9216, four peak-chord incompatibility checks, and 90 checks of
the periodic MILP branches. Its integer recurrence computes the exact
binomial weights at rational inputs without expanding all monomials.
The uniform approximation theorem is supplied by the analytic variance
bound, not inferred from these finite samples.
