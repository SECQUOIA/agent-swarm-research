# Second independent audit: one-resource follower optimization in accuracy bits

Date: 2026-09-05. Reviewer: quadratic_weighted_precision.
Status: **PASS** for the complete theorem in its stated scope. No correction
is required. This review addresses mathematical correctness and bit
complexity, not novelty or practical running time.

Reviewed the full [candidate](bilevel-one-resource-accuracy-bit-algorithm.md),
the [inverse approximation lemma](certified-positive-polynomial-inverse-approximation.md),
and the [bounded-power algorithm](bilevel-bounded-power-accuracy-bit-algorithm.md).
I previously completed a separate full
[second audit of the inverse lemma](review-certified-positive-polynomial-inverse-approximation-second.md).

## Feasibility, multiplier bounds, and endpoint cases

The linear image of the follower box is exactly `[b_min,b_max]`, including
signed and zero resource coefficients. Hence intersecting the leader
polytope with the two affine resource bounds gives exactly the feasible
leader set. Empty and lower-dimensional sets are covered by rational LP.
When every weight is zero, the equality reduces to `b(x)=0` and the
reviewed diagonal construction applies on that exact rational slice.

Each marginal is strictly increasing on `[0,1]`; its integral is strictly
convex even if its second derivative vanishes at zero. Thus every feasible
resource face has a unique minimizer. For a fixed multiplier, coordinatewise
clipped inversion minimizes the box Lagrangian uniquely.

The four threshold values per nonzero weight correctly handle the sign of
that weight. At the global lower multiplier, a positive-weight coordinate
is saturated at one and a negative-weight coordinate at zero. At the upper
multiplier these states reverse. Their extrema hold uniformly for every
leader in the cube. Since each nonzero coordinate contributes thresholds
separated by `G_i/|w_i|>0`, the resulting bounds satisfy `L<U`.
All thresholds have polynomial rational height, including when a resource
weight is very small or has a negative sign.

The continuous resource response decreases from `b_max` to `b_min` on
this common bounded interval. A balancing multiplier therefore exists at
every feasible leader, including endpoint resources. Lagrangian
minimization proves optimality directly once balance holds; no constraint
qualification or interior resource point is needed. Flat multiplier
intervals cause no problem: all balancing multipliers give the same unique
primal optimum.

The compact-multiplier subsequence proof of continuity is also valid.
Every convergent subsequence of responses has a balancing limit at the
limiting leader, which must be its unique optimum. The true upper objective
is therefore continuous on the compact feasible leader set and attains
its optimum.

## Exact residual control

For `lambda>=lambda*`, positive-weight coordinates decrease and
negative-weight coordinates increase. In both cases
`w_i(q_i(lambda)-q_i(lambda*))<=0`; the inequalities reverse when the
multiplier order reverses. Zero-weight coordinates do not change.
Consequently

```
sum_i |w_i| |q_i(lambda)-q_i(lambda*)|
 = |sum_i w_i q_i(lambda)-b(x)|
```

is an exact identity. It remains valid under saturation, at endpoint
resources, and on flat portions of the resource response. In particular,
a zero residual forces every nonzero-weight response difference to vanish;
zero-weight differences already vanish. The arbitrary signed upper
objective satisfies the claimed bound by `c_max/w_min` times this residual.
No lower derivative bound, inverse sensitivity estimate, or numerical
strong-convexity constant is being assumed.

## Polynomial approximation and exact algebraic optimization

The tolerance `eta=epsilon/[32(1+A+C)]`, with
`C=c_max W/w_min`, has polynomial encoding and logarithmic precision
requirement. The inverse lemma permits growing numerical degree `P` and
arbitrary nonnegative rational coefficient conditioning. Normalizing
`lambda=L+(U-L)theta` keeps the approximation variables in a unit cube of
fixed dimension `r+1`. Large multiplier bounds affect rational coefficient
heights, not the dimension or an iteration count proportional to their
numerical magnitude.

There are polynomially many pulled-back affine thresholds and therefore
polynomially many arrangement cells in fixed dimension. Taking the closures
of nonempty relative cells preserves the selected approximation branches.
Boundary-only and lower-dimensional cells remain included. Polynomial
substitution has polynomial output size because the number of variables
is fixed; it does not introduce one algebraic variable per follower.

The approximate balance constraint in each cell defines a compact
semialgebraic set. A true balancing point lies in at least one such set,
because its polynomial balance error is at most `W eta`. Thus a winning
cell exists and its algebraic minimum satisfies equation (12).

The explicit minimizer formula has `2(r+1)` variables, independent of the
number of followers. I checked the fixed-variable elimination interface
against [Basu's primary-author survey, Theorem 2.18](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf),
including its intermediate and output coefficient bit bounds. Together
with the algebraic sampling interface already checked in the linked
diagonal proof, this gives polynomial degree and height for a sampled
minimizer. Comparing two candidate values needs only a polynomial-degree
pairwise representation; retaining the winner avoids constructing a field
containing every candidate, much less all true follower roots.

## Rational recovery and the full error ledger

The proof correctly does not assume that the approximate balance set has
a rational point. Instead, it rounds within the underlying rational
polytope `Q`. In fixed dimension, its vertices have polynomial rational
height and can be enumerated in polynomial time. Caratheodory's theorem
gives an affinely independent simplex with at most `r+2` vertices containing
the algebraic point. Solving for its barycentric coordinates stays in the
sampled field. Rounding all but one weight down and assigning the remaining
mass to the last vertex preserves membership in this simplex exactly.
This also preserves every equality defining a lower-dimensional cell.

The selected `delta` controls both the polynomial objective and polynomial
balance change by their explicit coefficient-based derivative bounds on
the unit cube. These bounds and `log(1/delta)` have polynomial encoding.
Thus the rational recovered leader belongs to `X'` exactly, while the
auxiliary polynomial balance error is allowed to increase from `W eta`
to `2W eta`. The true Lagrangian response at the recovered parameter has
residual at most `3W eta`.

Combining the exact residual identity with the uniform response
approximation yields

```
|H(xhat)-H_Q(vhat)| <= A eta + 3C eta.
H(xhat)-OPT <= epsilon/8 + (2A+3C)eta <= 7epsilon/32.
```

Both inequalities have the correct signs. The rational polynomial value
itself satisfies

```
-(A+3C)eta <= H_Q(vhat)-OPT <= A eta+epsilon/8,
```

so its absolute error is at most `5epsilon/32`. It can be evaluated exactly
as a rational number of polynomial height. No final exact balancing
multiplier, common algebraic field of follower coordinates, or exact
sum-of-roots comparison is needed. Feasibility refers to the returned
leader and its true follower, not to the unbalanced auxiliary approximate
response, as the candidate explicitly states.

## Diagnostics and scope

Inspected and reran
[the exact signed-balance checker](../code/bilevel_one_resource/check_signed_balance.py).
All 7,200 identity and upper-objective error certificates across 160
instances passed. The cases include signed, zero, and tiny weights,
global multiplier bounds, saturation, and endpoint balances. These use
rational linear marginals and check the new balance mechanism exactly;
they do not implement the semialgebraic optimizer or replace the separately
audited polynomial inverse lemma.

The fixed leader dimension, fixed resource coefficients, single equality,
affine upper objective, and absence of additional response-dependent upper
constraints are material assumptions. Running time is polynomial in the
numerical degree and requested accuracy count, not merely their binary
encoding lengths. The existing sparse-power rational-output obstruction
embeds by a zero resource row, or by adding a separate resource-fixed
coordinate. The proof does not claim an extension to multiple resource
rows, where its exact no-cancellation identity is unavailable.
