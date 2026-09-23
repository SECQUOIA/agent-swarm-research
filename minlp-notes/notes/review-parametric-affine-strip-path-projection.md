# Independent review: affine-strip path projection

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Candidate: [parametric affine-strip projection](parametric-affine-strip-path-projection.md).
Verdict: **PASS** for the stated finite-bound, scalar-state path model with
a fixed number of parameters. No novelty is attributed to difference
constraints or fixed-dimensional real algebraic algorithms.

## Normalization and signs

On a cell where every gain is nonzero, `A_i=product_(h<=i) a_h` is
nonzero and has a fixed sign. Since `A_i=a_i A_(i-1)`, dividing the
transition by `A_i` gives coefficient exactly one on `y_(i-1)`.
If `A_i>0`, the increment interval is `[b_i/A_i,c_i/A_i]`; if
`A_i<0`, its endpoints are reversed. The same sign rule applies to
the coordinate bounds. Thus negative gains and alternating prefix-product
signs are handled correctly, without an absolute-value or orientation
assumption on the original states.

The imposed conditions `alpha_i<=beta_i` and `L_i<=U_i` are necessary.
They reject transitions or node intervals whose original lower bound
exceeds its upper bound. No extra partition according to the relative
order of those bounds is required: their inequalities can simply be
retained in the projected formula.

## Directed distances and all-pairs feasibility

The upper increment bound is an arc from `i-1` to `i` of length `beta_i`;
the lower bound is the reverse arc of length `-alpha_i`. Their sum is
nonnegative. Any closed walk in a bidirected path crosses each edge
equally often in both directions, so it has nonnegative length. Removing
such excursions leaves the unique simple directed path. The displayed
sums are therefore the exact shortest-path distances, even when some
individual arc lengths are negative.

For any feasible state, `y_i<=y_j+d(j,i)<=U_j+d(j,i)` and `y_i>=L_i`.
This proves every required pair inequality. Conversely, define

```
y_i=min_j [U_j+d(j,i)].
```

All quantities are finite because the node bounds are finite and the
path is finite. The pair inequalities give `y_i>=L_i`; the term `j=i`
gives `y_i<=U_i`. If `j` realizes the minimum defining `y_h`, the
triangle inequality gives

```
y_i<=U_j+d(j,i)<=U_j+d(j,h)+d(h,i)=y_h+d(h,i).
```

Applying this in both adjacent directions recovers both increment bounds.
Multiplying by each `A_i`, with its correct sign, gives every original
transition and coordinate bound. This proves sufficiency and exact
recovery; it does not rely on a relaxation or a necessary-condition test.

## Endpoint projection

For a prospective retained endpoint, use its fixed normalized value as
both the lower and upper bound. The recovered state is then forced to
equal that endpoint. Keeping the original endpoint restrictions separately
prevents the replacement from discarding a required bound. Both endpoints
can be fixed simultaneously because the all-pairs conditions include
their mutual compatibility as well as compatibility with internal bounds.

There are only `O(n²)` pair conditions. They are inequalities in the
parameter vector and the two retained endpoint coordinates; all other
states have been eliminated. For a zero-edge path, the two endpoint
names denote the same state, so their equality must of course be retained
if they are written as separate output coordinates. A one-vertex component
within a longer split path is handled directly by its node bounds.

## Polynomial degree and coefficient encoding

Let `S` be the ordinary dense rational input length and let the parameter
dimension be fixed. The degree of a prefix product is the sum of the
input gain degrees, hence polynomial in `S`. The number of monomials
of such a degree in fixed dimension is polynomial. Multiplying dense
polynomials adds coefficient bit lengths, with an additional logarithm
of the number of convolution summands; over polynomially many products
and sums this remains polynomial in `S`.

One can see the denominator control without multiplying a separate
denominator for every summand. Within a nonzero-gain component ending
at index `r`, every prefix product `A_i` divides `A_r` as a polynomial.
Thus each term `b_i/A_i`, `c_i/A_i`, or normalized node bound can be
written with common denominator `A_r`, using the appropriate suffix
gain product in its numerator. Retained endpoint variables enter these
numerators at most linearly. Constant rational coefficient denominators
can also be cleared with polynomial total bit length.

The sign of `A_r` is known on the current cell, so multiplying each pair
inequality by that denominator is exact with the appropriate orientation.
Alternatively multiplying by a squared common denominator is possible
while retaining its nonvanishing condition. Either method yields polynomial
degrees and coefficient heights, rather than nested rational expressions
whose expanded size is uncontrolled. Cells on which a gain vanishes
are not passed through this division step.

After solving the fixed-dimensional retained-coordinate problem, all
recovery expressions use rational functions and a finite minimum evaluated
at the same point. If the retained point is algebraic, selecting a minimum
only selects one of these values and introduces no field extension.
Exact comparisons and arithmetic have polynomial bit cost in its standard
algebraic representation. The retained dimension is fixed, and the
real-algebraic solver supplies polynomial-degree, polynomial-height
representations. No tower of one new algebraic root per eliminated state
is introduced. At rational retained points, the recovered states are
rational as well.

## Zero gains and multiple bounds

If `a_i=0` on the selected sign cell, the transition becomes
`b_i<=x_i<=c_i` and has no dependence on the preceding state. Deleting
that edge separates the feasibility problem into independent subpaths.
The new bounds belong to the first node of the right component and
are kept along with its original bounds.

Prefix products must be restarted at one for each new component; then
every remaining transition gain inside that component is nonzero.
Components with no retained endpoint require only their parameter
feasibility inequalities. Components containing one or both retained
endpoints use the corresponding fixed-value normalization. At most two
of these components can contain global endpoints, unless both lie in
the same component.

At a fixed coordinate, several lower and upper bounds can be retained
without choosing an active bound. Require each lower candidate to be
at most every propagated upper candidate. In the recovery formula take
the minimum over all upper candidates. Negative prefix products swap
the entire lower and upper families. This is equivalent to intersecting
the intervals and avoids additional parameter case splits.

The number of extra bounds created by zero transitions is linear in
path length. Summing the squared component sizes is at most the square
of the total size, so the projection still has polynomially many
inequalities. Consecutive zero gains, isolated vertices, and cells of
lower parameter dimension require no special arithmetic beyond this rule.

## Fixed-dimensional sign enumeration and exact algorithms

Only realizable sign patterns of the input gains are needed; their
connected components need not be distinguished for this normalization,
because it depends on signs alone. A sign-invariant decomposition is
also valid. Zero signs and lower-dimensional realizations must be retained.

The primary book [Basu, Pollack, and Roy, *Algorithms in Real Algebraic Geometry*](https://www.math.purdue.edu/~sbasu/bpr-posted1.pdf)
was checked directly in the repository PDF, with visual inspection of
pages 525–526 because its text encoding is irregular. Theorems 13.11–13.12
provide sign-condition sampling/enumeration with polynomial arithmetic
complexity for fixed dimension and polynomial degree/bit bounds for the
algebraic representatives. Theorem 13.13 gives the corresponding
fixed-dimensional existential decision bound. These are the classical
operations needed after the explicit elimination here.

There are polynomially many realizable sign patterns for fixed parameter
dimension. On each, the projection formula has polynomial size, degree,
and coefficient encoding. Taking their union therefore preserves those
bounds. Combining with additional polynomial constraints on the retained
variables yields a fixed-dimensional semialgebraic feasibility problem,
because the parameter vector and the two endpoints have fixed total
dimension. Exact feasibility and witness recovery consequently have
polynomial bit complexity under the stated dense encoding.

This conclusion does not apply to an objective or constraint involving
all eliminated states merely because its original description was dense
and short. Such a quantity need not be determined by the retained
endpoints, and adding an accumulated state would leave the scalar
normalization theorem. The candidate excludes that case. Likewise the
common gain in the two transition bounds is essential: different upper
and lower gains do not yield the same difference-constraint system.

For rational-function input gains or bounds, the same argument would
extend on a domain where all original denominators are nonzero, after
including their signs in the case decomposition. That is a useful
optional extension for applications but is not silently needed for the
formal polynomial-input statement audited here.

## Exact independent checks

Created and ran
`code/parametric_path_lp/check_affine_strip_projection_review.py`.
It compares the normalized all-pairs conditions and minimum-formula
recovery against an independent forward reachable-interval propagation
in the original affine coordinates. All 1,200 rational cases agree:
635 feasible and 565 infeasible, including 707 cases with zero gains
and 983 with negative gains. The tests use no retained endpoint, either
endpoint separately, or both endpoints, and include inconsistent node
and transition bounds.

Every recovered feasible witness was separately checked against every
original coordinate bound, affine transition, and fixed endpoint value.
The checker uses exact rational arithmetic throughout. It supports the
fixed-parameter algebraic identities and zero-gain handling; the symbolic
degree bounds and fixed-dimensional sign enumeration rest on the proof
and primary-source check above. No mathematical correction was required.
