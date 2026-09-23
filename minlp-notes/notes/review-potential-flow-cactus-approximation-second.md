# Second independent audit: additive approximation of cactus MPD

Date: 2026-09-05.
Reviewer: independent agent `graph_precision_second_review`.
Reviewed source: `notes/potential-flow-cactus-approximation-investigation.md`,
including its rational nomination output and real algebraic subroutine sections.

## Verdict and scope

The candidate theorem passes this second independent mathematical audit.
I found no substantive gap in the claimed polynomial bit-time additive
approximation algorithm, rational feasible nomination output, or certified
MPD interval. The smoothing and finite-face reduction are valid for arbitrary
finite load intervals with a nonempty balanced nomination polytope; zero
need not belong to each interval.

This verdict requires the stated passive model: a connected cactus,
strictly positive rational quadratic resistances, independent rational load
intervals, balance, and no additional potential or flow constraints. It is
not a novelty or publication-priority verdict. The algebraic subroutine is
a theoretical polynomial-time ingredient, not an implemented algorithm.
The review is based on a full proof read, separate derivations of the
sensitive steps, and checking the stated primary subroutine source; it does
not claim a new computational experiment.

## Aggregation and the smoothed derivative

Removing off-path blocks leaves the union of the blocks on the objective
terminals' block path. Each removed connected group attaches to that core
at exactly one vertex. Its total injection changes the core balance only
at that attachment. Independent intervals have exactly their interval sum
as attainable totals, including intervals that are not centered at zero.
Conservation and uniqueness therefore give both directions of the asserted
objective-preserving reduction. For any chosen core solution and any valid
allocation of each group total, the unique global passive flow restricts
to that same core flow. There are no physical bounds to violate elsewhere.

For smoothing parameter `rho>0`, the edge function
`beta(x|x|+rho x)` is continuously differentiable with derivative
`beta(2|x|+rho)>0`. Its inverse is continuously differentiable. The nodal
map with one potential fixed has a positive definite grounded Laplacian
as derivative, so the implicit function theorem supplies continuous
differentiability with respect to balanced nominations. Differentiating
and using Laplacian symmetry gives `dF=h^T db`, where `Lh=e_s-e_t` and
`h_t=0`, exactly as in the candidate.

At a maximum on the balanced box, differentiation along every feasible
segment gives `h^T(c-b)<=0` for all feasible `c`. Thus the maximum also
solves a linear program. Its standard polyhedral optimality conditions
yield a balance multiplier and the upper/lower saturation rules. Fixed
coordinates and lower-dimensional feasible nomination polytopes do not
require a nonlinear constraint qualification.

## Strict order and at most two free loads

The electrical derivative network has positive conductances even when
some physical flows vanish. Its sources are only `s,t`. A block attached
off the objective block path has no net electrical current and constant
`h`; this is why aggregation is performed first.

On the core, the electrical unit current traverses the objective blocks
in series. A bridge has a strictly positive potential decrease. In a
cycle, both entrance-to-exit branches are series chains of positive
resistances carrying positive current, so their potential sequences are
strictly decreasing. Interior values are strictly between the entrance
and exit values. Successive block ranges meet only at their shared
articulation value.

Consequently a multiplier can equal `h` at no more than one interior
vertex per branch of one cycle. If it equals an articulation potential,
strictness excludes every other core vertex. A terminal threshold gives
at most that terminal as pivot. All other coordinates are saturated in
the stated upper-before/lower-after order. This proves the at-most-two
claim for every smoothed maximizing nomination after aggregation.

Repeated physical potentials, repeated resistances, symmetries, and zero
physical flows do not defeat this reasoning: strictness is asserted for
the *electrical derivative potential* under positive smoothing. Equal
values across the two branches are allowed and give the two pivots.

If the multiplier exceeds the full electrical range, all coordinates are
at lower bounds; if it is below that range, all are at upper bounds. A
feasible such vector is an extreme nomination, even when it is nonzero.
The first/last block or terminal threshold includes it. No assertion that
it must be the zero vector is needed for arbitrary intervals.

For explicit enumeration, include vertex and gap thresholds on both
branches, singleton thresholds at articulations **and terminals**, and
the extreme all-lower/all-upper cases. The latter can also be retained as
endpoints of terminal-pivot faces. A cycle of length `k` has `O(k^2)`
threshold pairs. The total over a cactus is `O(n^2)` since its block
vertex counts sum to `O(n)`. Identical faces, inconsistent shared-endpoint
assignments, and empty faces can be discarded with rational comparisons.
Enumerating extra valid faces causes no correctness problem.

## Passing to the original nonsmoothed problem

The spanning-tree routing bound is uniform over the compact nomination
polytope. Comparison of each smoothed energy minimizer with that bounded
routing gives a uniform cubic-energy bound for `0<rho<=1`. Strictly
positive resistances turn this into a bound for every flow coordinate.

If nominations converge and smoothing vanishes, any limiting subsequence
of minimizing flows is feasible for the limiting nomination. Given any
competitor for that nomination, correcting its imbalance along the fixed
spanning tree gives convergent feasible competitors for the varying
nominations. Passing to the energy comparison proves optimality of the
limiting flow for the original cubic energy. That energy is strictly
convex, so the limit is unique. Tree sums of the continuous edge drops
then recover convergent normalized potentials.

This argument also proves continuity of the unsmoothed objective and,
by a compactness/subsequence contradiction, uniform convergence of the
smoothed objectives. Hence limiting smoothed maximizers are original
maximizers. There are only finitely many saturation patterns, and every
face is closed, so a subsequence uses one fixed face. At most its two
pivots can remain free in the limit. A possible loss of strictness of the
unsmoothed derivative has no effect on this argument.

## One parameter and constant-block separation

On a retained face, zero free pivots means a fixed nomination. One free
pivot is fixed by balance. With two distinct free pivots, their sum is
fixed and one load itself can be used as parameter `z`; the other is an
affine function with slope `-1`. Their interval intersection is a rational
closed interval, possibly a singleton. All represented nominations are
feasible, and every such nomination has a unique physical flow.

The two pivots lie in the same cycle and preserve that cycle's total
load. Every other block therefore sees fixed effective loads. Internal
redistribution inside the selected cycle cannot change a downstream or
upstream block's physical flow. Summing potential drops along an objective
path proves `F(z)=C+g(z)` with fixed `C`. All effective loads for fixed
blocks are rational even though their physical flows need not be.

## Fixed blocks, arrangements, and degenerate polynomial pieces

For a cycle, conservation gives affine edge flows in one circulation.
The derivative of its loop function with respect to circulation is
`sum_e 2 beta_e |x_e|`, apart from the harmless common orientation
convention. This derivative can vanish at an isolated point, but the
loop function is globally strictly increasing and has a unique root.
Rational flow-zero breakpoints divide it into pieces of degree at most
two. Linear pieces, roots at breakpoints, and zero discriminants are
legitimate algebraic cases; quadratic formulas requiring division by a
nonzero leading coefficient must not be applied blindly. The fixed-block
root has algebraic degree at most two, and its drop is in the same
quadratic field. Polynomial bit-time rational isolation suffices.

For an active cycle, each flow is `c_e+d_e z+sigma_e w` with rational
coefficients and `sigma_e` equal to `+1` or `-1`. In particular, its
zero equation is a genuine affine line, although different edges may
define the same line. An arrangement of rational lines, with coincident
lines merged geometrically if desired, has only quadratically many faces.
Keeping lower-dimensional faces or using closures of full-dimensional
cells covers every zero-flow point.

Within a sign cell, conservation already holds by construction and the
loop equation is exactly the physical compatibility condition. All edge
laws and the objective are quadratic polynomials on that cell. At a zero
flow both choices of sign give the same value zero, so shared boundaries
introduce no extraneous physical solution. A loop polynomial may reduce
in degree or vanish identically on a lower-dimensional face; general
semialgebraic decision and sampling handle these degeneracies.

## Bounds, bit complexity, and algebraic witnesses

Orienting nonzero physical flows in their actual direction gives an
acyclic directed graph because physical potential strictly decreases
along each such edge. Flow decomposition into source-to-sink paths then
bounds every edge by total positive injection, which is at most the
candidate's rational `B`. This applies also to the smoothed law. A tree
routing has the same bound, so circulation magnitude at most `2B` is a
valid compact restriction. Aggregation and the fixed-block effective
loads do not increase the needed original total-injection bound.

A path drop has absolute value at most
`M=B^2 sum_e beta_e`. Its binary encoding length is polynomial even when
its numerical magnitude is large. Tree routing, aggregation, rational
line arrangements, and quadratic polynomial assembly all involve only
polynomially many rational operations with polynomial bit growth.

Each active decision system has two real variables, degree at most two,
and polynomially many polynomial-size rational coefficients. I checked
Basu's survey: Theorem 2.18 states elimination bounds with intermediate
integer bit sizes; Theorem 3.6 and its immediate sampling consequence
supply algebraic sample points with bounded output and intermediate
integer sizes. Fixing dimension and degree gives the required polynomial
bit bounds. [Primary source](https://www.math.purdue.edu/~sbasu/raag_survey2011_final.pdf).

Clear positive denominators before calling an integer-coefficient
subroutine. Adding a rational objective threshold preserves fixed
dimension and degree. Binary search from the rational bound `[-M,M]`
requires polynomially many steps in the input length and accuracy bit
length. For witness extraction, retain a feasible lower threshold from
that search and sample the corresponding nonempty semialgebraic set.
Its point is an algebraic witness near the active optimum; the algorithm
does not need to compare the radical constant sum exactly.

The representation and isolation precision for this fixed-dimensional
algebraic sample have polynomial bit size. Refining its `z` coordinate
to a requested rational accuracy is consequently polynomial bit work.
As usual, the input-length claim includes reading the encoding of the
rational tolerance; no complexity claim should exclude that cost for
an unnecessarily long rational representation of a tolerance near one.

## Lipschitz estimate and rational nomination

At positive smoothing, derivative resistances satisfy
`r_e<=beta_e(2B+rho)`. The electrical maximum principle puts every `h_v`
between `h_t=0` and `h_s`. Unit electrical energy minimization, tested
with a unit path flow, bounds `h_s` by `sum_{e in P}r_e`. Integrating
`h^T(c-b)` on a balanced feasible segment and using the l1 bound proves
the smoothed estimate. Uniform convergence gives exactly

```
|F_0(b)-F_0(c)| <= [2B sum_{e in P} beta_e] ||b-c||_1.
```

This proof uses neither a nonzero physical flow assumption nor cactus
structure. All constants have polynomial rational encoding length.
On a two-pivot face, changing `z` by `eta` changes l1 load distance by
`2 eta`; hence `eta<=epsilon/(8C)` loses at most `epsilon/4`.

An algebraic `z` can be approximated by a rational and then clipped to
the rational feasible interval. Clipping cannot increase its distance
to the original feasible value, which gives a direct treatment of every
endpoint and collapsed-interval case. The other pivot is recomputed by
its exact rational balance equation. Greedy interval allocation within
each aggregated group produces rational original loads with precisely
the intended total and preserves global balance. No rounding of a
physical flow or potential is claimed or needed.

If `B=0` is computed on the aggregated core, every core interval is the
zero singleton, all core flows and the objective are zero, and a feasible
rational original nomination is still recovered by group allocation.
Original off-core flows can be nonzero because fixed injections and
withdrawals may cancel inside an aggregated group. If instead `B` is
computed on the original input, `B=0` forces all original loads to zero.
Since resistances are positive and `s,t` are distinct, the candidate's
`C=0` case reduces to the corresponding zero-load core situation. No
division by `C` is necessary then.

## Value intervals and a consistent error budget

For clarity, one valid implementation of the candidate's budget is:

- Approximate each fixed-block drop with absolute error at most
  `epsilon/(16n)`, so their sum has a rational interval of width at
  most `epsilon/8`.
- Compute the active optimum interval with width at most `epsilon/8`.
  Adding the intervals gives each face optimum an interval of width at
  most `epsilon/4`.
- Select the face with the greatest lower endpoint. Its true optimum is
  within `epsilon/4` of global MPD, regardless of radical-sum comparison.
- Sample a feasible active point within `epsilon/4` of its face optimum
  and round its nomination as above, losing at most `epsilon/4` more.

Thus the total nomination loss is at most `3 epsilon/4`, which is below
the requested tolerance. Taking the maximum of all lower interval
endpoints and the maximum of all upper endpoints contains global MPD;
its width is at most `epsilon/4`, hence at most `epsilon`. For this last
claim, if one face supplies the greatest upper endpoint, subtracting the
greatest lower endpoint can only reduce that face's own interval width.
Singleton nomination faces use only fixed-block intervals and require
no algebraic parameter rounding.
