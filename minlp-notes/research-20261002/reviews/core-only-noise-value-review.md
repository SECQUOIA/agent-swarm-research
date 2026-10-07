# Independent review of the fixed-law core value oracle

Date: 2026-10-02. Verdict: **pass**. This is a fresh actual-file review
of [core-only-noise-value-oracle.md](../new-direction/core-only-noise-value-oracle.md).
It also reads the value-only convex recourse interface, the projected
finite-tail specialization, and the existing exact fallback interface.
A separate mathematical agent independently checked the cap,
truncated-moment and bit-cost arguments. No substantive gap was found
under the stated verified curvature and residual-convexity premises.

The result gives a value Cauchy oracle and feasible objective
approximations for one fixed sampled instance. It does not give
distance to an optimizer or a coordinate evaluator for an optimizer.
This distinction is essential to its compatibility with the reviewed
point-output reductions.

## 1. Convex recourse needs value precision only

For a fixed rational core point, the residual feasible set is the same
unit box and the restricted polynomial is convex. The objective-interval
part of the
[convex evaluation proof](../new-direction/convex-patch-evaluation.md)
uses no positive Hessian modulus. Its capped epigraph has explicit
rational inner and outer radii, and polynomial value and gradient
evaluation supplies a rational separation oracle. The GLS Turing
interface and its homothety/clipping repair return a feasible rational
point and certified objective bounds in polynomial query bit time.
Strong convexity enters only the separate conversion from value error
to point error, which is not used here.

The [recourse predecessor](../new-direction/smoothed-polynomial-box-recourse.md)
also proves the compact tangent certificate. At a sufficiently accurate
feasible rational point `z`, minimize the affine tangent over the
residual box coordinatewise. Convexity makes that minimum a global
lower bound. Its gap is at most the desired tolerance after a value
solve to `min(eta/2,eta²/(8K))`, with a rational coefficient-based
smoothness bound `K`. This increases requested accuracy by only a
polynomial number of bits. A verifier checks the tangent directly;
it need not trust the internal convex solver stopping decision.

Consequently residual ties, flat directions, boundary minimizers and
zero residual curvature cause no failure. Recognizing arbitrary
polynomial convexity is not being provided for free: the main theorem
explicitly charges its supplied verifier and curvature certificates.

## 2. Projected growth has the required finite-law format

The good-event formula in (7) is equivalent to point growth of the
conditional value function in core distance. Setting the tested core
equal to the proposed optimum first forces the proposed residual point
to be conditionally optimal. The remaining inequalities then assert
the value-function growth bound at every core point. Conversely, any
such value-function growth bound and an optimal residual completion
satisfy the formula.

Residual coordinates appear in its objective and quantifiers, but not
in the squared growth distance. Multiple residual optima at the same
core therefore remain allowed. Positive projected growth excludes
distinct optimal core points, as required by the later localization
argument.

The formula has two quantified blocks of original dimension and fixed
polynomial degree. Taking a scalar noise section preserves this format.
The reviewed fixed-block quantifier-elimination bound therefore gives
a component bound exponential only in base input data, independent of
threshold height and sampled coefficient height. Applying the continuous
proximal tail to the continuous conditional value function, then the
same marginal discrepancy transfer, yields the stated bound
`P(g<t)<=kt/sigma+C_0/M`. It is uniform over every threshold for one
fixed grid. Its atom term includes `g=0` draws; no residual-noise or
residual-uniqueness premise is needed.

## 3. Approximate corners certify every draw

Holding a residual optimizer fixed while independently rounding core
coordinates proves the lower correction `e=kLh²/8`. Fixed product
feasibility is used here. The oracle intervals of width `e` then give
sound cell lower bounds `min ell-e`.

The final incumbent must be used in the pruning pass. The actual
algorithm makes two linear passes, so every retained cell has a
minimizing lower-corner value at most `U+e`. Its true corner value is
at most `U+2e`, and the cell containing an optimum gives `U-f*<=2e`.
Every retained cell therefore has a true witness of gap at most `4e`.
Keeping cells against an obsolete larger incumbent would not justify
this bound; the draft explicitly avoids that error.

For every current corner, `ell>=u-e>=U-e`. Thus all current lower bounds
are at least `U-2e`. Previously removed cells had bounds larger than
their then-current incumbents, which are at least the new incumbent.
Together these observations prove the global interval `[U-2e,U]`
without any growth assumption. All optimal cores survive. The finite
level satisfying `2e<=2^-q` is `O(I+q)`, so a query terminates at that
level or invokes the independently correct fallback.

## 4. Generated states, not retained states alone, are capped

On a positive-growth draw, a retained cell has a corner within
`h sqrt(kL/(2g))` of the unique optimal core. Coordinate lattice counts,
corner incidence and child generation give

```
generated cells <= 4^k(3+sqrt(2kL/g))^k
                <= 512 max(1,L/g)^(k/2).
```

For `k=2` the first expression is at most `400 max(1,L/g)`, already
below the displayed common constant. The bound covers the initial
single cell as well.

The saved algorithm compares `2^k` times the retained parent count to
`T=512B` before constructing the next level. It therefore bounds
generated candidates and their oracle calls, including candidates that
would later be pruned. A cap imposed only after pruning would not
suffice. The cap is per level; a fixed total-work cap independent of
`q` would incorrectly force fallback on ordinary draws at large
requested precision.

The cells have disjoint dyadic interiors and are generated uniquely
from their parents. A shared corner occurs in at most `2^k` cells.
Repeated corner queries thus cost only a fixed factor, and no expensive
deduplication or pairwise cell comparison is required. Linear generation,
two linear passes, and polynomial work per row preserve the exponent
`k/2`. An unspecified quadratic cost in list length would destroy the
two-dimensional moment argument; the actual algorithm excludes it.

## 5. One growth event pays for all levels and accuracies

Write `Z=max(1,L/g)`, `W=Z^(k/2)`, `r=kL/sigma`, and
`beta=C_0/M`. Every attempted cap at every precision implies `W>B`.
This implication is pathwise for the fixed objective, so no union
over levels, oracle calls or requested precisions is taken.

For `s>=1`, the threshold-uniform growth tail gives
`P(W>s)<=r s^(-2/k)+beta`. Integrating up to `B` proves

```
E min(B,W) <= 1+r+beta B          for k=1,
E min(B,W) <= 1+r log B+beta B    for k=2.
```

Likewise `B P(any cap)<=r B^(1-2/k)+beta B<=r+1` when
`beta B<=1`. Choosing `B>=B_0` and the base-only law
`M>=C_0B` pays for the exact fallback's exponential base factor.
There is no mesh-spacing requirement on `M`. Fine queries for which
`M h` is very small use the same growth-tail law and the same cap.

The fallback bit bound separates its base-only exponential factor
from a fixed polynomial in sampled coefficient height and requested
precision. Since `log M=poly(I)`, choosing this law creates no
circular dependence on its own sampling precision.

At level `j`, dyadic coordinate and query-tolerance lengths are
polynomial in `I+j`. Substituting a rational core in a fixed-degree
polynomial has the same bound. The certified convex value interface
has a fixed polynomial bit exponent, independent of the growth
constant or list length. These facts give the single random work
factor in (19), valid simultaneously for all `q`. Its expectation is
`(1+L/sigma)poly(I)` after absorbing `log B` into the base polynomial.
Record and output sizes obey the same bound. Exceptional individual
draws can still have exponential cost and output, as stated.

The source exact fallback handles ties and positive-dimensional optimal
sets and returns feasible rational approximations with global lower
bounds. It changes neither the objective nor the sampled law. Repeating
a query from scratch is already enough for the theorem; caching is
optional and not needed in this cost argument.

## 6. Degenerate cases and scope

For `k=0`, one ordinary convex value solve suffices. For `L=0`, core
endpoint rounding does not increase expected objective, so some core
vertex attains the global value. Taking the minimum lower endpoint
and minimum feasible upper endpoint across the at most four corner
solves preserves their requested interval width. This includes ties
and core-linear objectives without a growth argument.

For larger `k`, the stated integral and fallback payment acquire the
factor `B^(1-2/k)`. The note correctly identifies this as a limitation
of the present proof rather than a general impossibility result.
The returned feasible points need not approach any fixed optimizer
or have a controlled distance to the optimal set. The intervals
instead evaluate one fixed optimal value to arbitrary accuracy.

## 7. Distinct targeted verification

The reviewer diagnostic
[check_core_value_cap_review.py](check_core_value_cap_review.py)
checks probability and cap arithmetic, separate from the author's
cell-refinement diagnostic. Its fixture has conditional value
`sum_i(gamma_i-1)v_i` and may be realized with an independent residual
`z^4`, which has no positive uniform Hessian modulus. Endpoint atoms
produce flat core directions and zero projected growth. This fixture
is deliberately used to test the abstract cap/tail calculation; the
actual theorem's `L=0` special branch would solve it directly.

The [saved results](core-value-cap-review-results.json) report 18 finite
laws, 7,154 exact rational draw checks, and 108 threshold-tail checks.
They verify capped ceiling moments and expected fallback payment for
both `k=1` and `k=2`, with genuine tied endpoint atoms in every law.
The diagnostic does not implement the core grid, the convex solver or
the algebraic fallback.

Command actually run:

```
python research-20261002/reviews/check_core_value_cap_review.py
```

The review, checker and result file also passed scoped local-link,
fence, whitespace, Python-syntax and JSON checks and `git diff --check`.
No project-wide verification, CI check or index edit was used. The
author's separate grid diagnostic was not rerun by this reviewer.
