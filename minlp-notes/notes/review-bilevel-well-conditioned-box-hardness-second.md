# Second independent review: conditioned unit-box follower hardness

Date: 2026-09-05. Verdict: **PASS** for
[the complete candidate proof](bilevel-well-conditioned-box-exact-hardness.md).
The exact decision problem is NP-complete under its stated restrictions,
and the accuracy-bit barrier follows. This review does not establish
independent literature priority for the complete construction.

## Network and Boolean-score reduction

The recursion `t_next=3t-2 clip(3t-1)` maps each of its three pieces
inside `[0,1]`. Consequently the two ReLU outputs have ranges `[0,2]`
and `[0,1]`, and their difference is the required clipped digit.
Substituting the expanded earlier digits produces a strictly lower
triangular network in the stated ordering; the two ReLUs of a digit
need not depend on each other. The coefficient bound `C=2*3^n`
dominates every ternary coefficient and every readout coefficient.

The network residual `h-Ah-b0-x*b1` is the negative part of each
preactivation. The explicit digit and readout ranges bound it between
zero and two. This bound holds uniformly over all leaders, not only
at Boolean witnesses. It is essential to the later error argument.

The displayed Boolean leaders have polynomial rational bit length and
lie strictly inside `[0,1]`. Their ternary remainder bounds force every
digit exactly to its desired endpoint. The score identity follows from
`y-ReLU(2y-1)=min(y,1-y)`. For an unsatisfiable formula, a clause false
under nearest-bit rounding has each continuous literal equal to its
variable's minority amount. Distinct clause variables prevent repeated
counting, so that clause's sum is at most `D(y)`. The resulting uniform
score lower bound is two. The cited preprocessing of ordinary 3SAT
into distinct-variable clauses is polynomial and preserves its decision.

## Scaling, conditioning, and coefficient length

With `s_i=s_0*theta^(i-1)`, strict lower triangularity gives
`|B_ij|<=C*theta^(i-j)`. Both row and column sums are bounded by
the geometric series `C*theta/(1-theta)<=2C*theta<=1/50`.
Hence the spectral norm is at most `1/50`, and for every vector `v`,

```
(49/50)||v||_2 <= ||(I-B)v||_2 <= (51/50)||v||_2.
```

Squaring proves both asserted absolute eigenvalue bounds for the Gram
matrix. Their ratio is `(51/49)^2<2`. The upper bound also bounds the
magnitude of every matrix entry by less than two.

For each of `b0,b1`, the scaled infinity norm is at most `1/4`.
The transpose multiplier has infinity norm at most `51/50`, since
the column norm of `B` has the same bound. Thus each normalized
linear follower coefficient has magnitude at most `51/200<1`.
The upper coefficients have magnitude `2*delta/s_i<=2`. The fixed
unit bounds and the scalar leader bound use zero and one only.

Although `M` is large, its logarithm is polynomial. Taking powers of
`theta` through depth `N-1` gives polynomial bit length for every
`s_i`, its reciprocal, the scaled matrix, and its rational Gram matrix.
In particular `log(1/delta)=O(N^2 log(NC))`. Matrix expansion uses
polynomially many arithmetic operations on those explicitly bounded
rationals. No exponentially large number of network nodes or entries
is introduced.

Keeping the square's leader-only term gives joint convexity in leader
and follower variables. Dropping that term preserves all follower
responses but does not itself assert joint convexity of the normalized
model. The draft distinguishes these two statements correctly.

## Relative-coordinate error: the critical step

The scaled network point lies in the unit box and satisfies its stated
clipped fixed-point identity, because upper clipping does not affect
the scaled ReLU output. Separately, box KKT conditions are exactly
the projected-gradient identity with step one at the QP optimizer;
using that identity requires no convergence claim about an iterative
algorithm.

Subtracting the two identities and using coordinatewise clip
nonexpansiveness gives
`e<=P e+S^(-1)|B|^T S |S^(-1)r|`. The scaling algebra is

```
U=S^(-1)|B|^T S=S^(-2)P^T S^2.
```

Thus its nonzero entry in row `i`, column `k>i`, is bounded by
`C*theta^(2(k-i))`; the squared scale ratio is correct. The residual
identity after dividing by `S` yields
`|S^(-1)r|<=(I+P)e+2*1`, including when some approximate coordinates
or active sets differ substantially from the exact network's.

Nilpotence gives the nonnegative inverse `T=(I-P)^(-1)` and
`||T||_infinity<=M`. Multiplying the componentwise inequality by this
nonnegative inverse is valid even though `(I-P)e` itself need not
be coordinatewise nonnegative. Taking norms only after that step gives

```
||e||_infinity <= a ||e||_infinity + 4MC theta^2,
a<=2MC(1+NC)theta^2<1/2.
```

Moving the first term to the left therefore proves the displayed
`8MC theta^2=1/(1250 N^2 C M)<=1/(16N)` bound. There is no circular
small-error assumption and no reliance on an absolute Euclidean error
being small relative to the tiniest coordinate scale.

The score vector has exactly `N` entries of magnitude two, so its
one-norm is `2N`. Multiplying the relative error bound by that norm
and by `delta` proves the uniform upper-value error `delta/8`.
This validates the transfer of the exact network's SAT score gap to
the actual QP responses.

## Decision complexity, certificates, and limits

The yes upper minimum is at most `delta/8`; the no minimum is at
least `15delta/8`. No nonnegativity of the approximate QP upper
objective is needed. The threshold `delta` separates them. Continuity
of the unique response on the compact leader interval gives attainment.

I independently checked the referenced active-face NP argument.
Guess lower/free/upper statuses. A positive-definite principal matrix
solves free-coordinate stationarity as an affine rational function
of the scalar leader. Bound feasibility, lower/upper gradient signs,
and the upper threshold are then weak rational affine inequalities
in that scalar. A nonempty feasible interval has a polynomial-size
rational point. Degenerate free coordinates touching a bound are safe,
because a zero gradient satisfies the bound's KKT condition. Rational
linear algebra bounds the follower certificate length polynomially.
Thus NP membership applies to the stated rational SPD box model,
not only to the special Boolean witness leaders.

An additive-value guarantee with error `delta/4` gives yes reported
values at most `3delta/8` and no values at least `13delta/8`.
The threshold `delta` still separates them, and the requested number
of accuracy bits is polynomial in the source input. This proves the
claimed precision dependence barrier. It does not contradict an
algorithm polynomial in inverse tolerance, since `1/delta` can be
exponentially large. Uniform spectral conditioning and coefficient
magnitude bounds do not bound denominators or the required precision.
No constant-gap, strong-hardness, or fixed-alphabet conclusion follows.

## Independent exact validation

[check_conditioned_hardness_second.py](../code/bilevel_response/check_conditioned_hardness_second.py)
assembles the rational network and the actual scaled matrices rather
than testing only their upper bounds. It passed five families,
including the eight-clause unsatisfiable formula on three variables:
all matrix, residual, coefficient, contraction, and error constants
passed exact Fraction comparisons. It also passed 490 exact network
score samples and 30 exact Boolean leader witnesses. The largest
checked Gram-matrix entry had 5,883 bits. These checks use no numerical
QP tolerance and do not stand in for actual follower KKT verification.
The completed
[first independent audit](review-bilevel-well-conditioned-box-exact-hardness.md)
reports 42 actual rational QP response checks, using 390 rational active
systems through dimension 17, including the eight-clause unsatisfiable
formula, ReLU breakpoints, endpoints, and Boolean leaders. Its
[separate exact checker](../code/bilevel_dense_box/check_conditioned_hardness_first_review.py)
checks full box KKT conditions, relative-coordinate errors, and score
gaps without floating-point solves.

The draft credits the earlier ternary scalar-leader construction and
regularization-path antecedents. Exponential response complexity alone
would not prove this upper-optimization result. The present audit
verifies the explicit bounded network and its quantitative QP
approximation; it does not claim that arbitrary ReLU networks are
represented exactly by the constructed QPs.
