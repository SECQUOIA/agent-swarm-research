# Independent review of mixed bag-cell pruning and exact closure

Date: 2026-10-02. Reviewed the complete
[mixed author draft](sparse-bag-cell-smoothed-miqp.md). This review focuses on
the deterministic extension of the
[reviewed continuous algorithm](sparse-bag-cell-review.md), including its
integer-grid transition and exact closure. No external search or additional
agents were used. Probability bounds and the finite noise law require their
own analysis; the finite checks here make no expectation claim.

**Verdict.** The proposed deterministic extension is sound. The two essential
changes are to replace integer unit cells by singleton cells when the mesh
first drops below one, and to fix integer coordinates only when their
retained projection hull is a singleton. Derivative signs are used only
for continuous coordinates. Convex closure requires every integer coordinate
to have been fixed.

## 1. Integer cells and common refinement

Round original integer bounds inward first, reject empty domains, and
remove fixed coordinates. Choose an initial mesh that is an integral power
of two and is at least one and every original interval width. Until the
mesh reaches one, integer grids have integral step, integral initial anchor,
and integral clipped upper endpoint. Their cells contain the integer points
in the displayed intervals, not every real point in those intervals.

While `h>=1`, ordinary refinement at the next common dyadic partition gives
at most two interval children per integer coordinate. At `h=1`, every
nondegenerate integer interval has length exactly one. For the next level,
replace it by its two singleton endpoint cells. A singleton remains a
singleton at all later levels. Thus at every level with `h<1`, every integer
factor of every bag cell is a point. The child count remains at most
`2^|B|` per bag cell, including this transition.

This change preserves the physical mixed feasible set: the only feasible
integer points in a unit interval are its endpoints. Splitting a unit
interval into two real half-intervals would be a different construction and
would not supply the later zero-width localization argument.

## 2. Rounding, sparse rows, and pruning

A feasible integer strictly inside a coarse interval can be rounded to its
two integral endpoints with its mean preserved. The rounding outcomes are
valid original integer values. In a unit interval an integer is already an
endpoint, so its variance is zero. At fine levels, singleton integer cells
also make rounding deterministic.

The common-partition argument from the continuous review still applies to
every bag simultaneously. Nongrid coordinates have a unique containing
interval; grid-boundary coordinates stay fixed. Every rounded outcome
therefore satisfies all bag whitelists, including any specified containing
bag cell. Singleton coordinates cause no exception. The corner-row test
continues to describe exactly the allowed full mixed-grid assignments.

With `n` counting both coordinate types, independent rounding gives the
same conservative bound

```
E[F(Y)]<=F(x)+E_j,       E_j=nLh_j^2/8.
```

At fine levels only continuous coordinates contribute variance; retaining
`n` in the bound is harmless. The curvature assumption is on the continuous
quadratic extension, including between coarse integer grid nodes.

Sparse separator-key DP, conditional bag-cell lower bounds, and the monotone
incumbent are unchanged. Retaining ties preserves every original mixed
optimizer. Every retained cell has a genuine full mixed-grid witness with

```
F(y)-f*<=2E_j=nLh_j^2/4.
```

The pruning history proves bounds on the original mixed domain. It need
not prove them on fractional integer-coordinate points, which are outside
that domain. No dense enumeration of all integer labels is required by the
search: it generates only children and corners of retained cells.

## 3. Sound exact closure

Intersect the coordinate projection hulls over containing bags, as in the
continuous algorithm. Every original optimizer remains in this product.
If an integer coordinate's resulting interval is a singleton, its value is
integral and is shared by every original optimizer. Recording that integer
value is sound even when it is strictly inside the original integer range.

Do not infer an integer value from a gradient sign. An interior integer
optimizer can have strictly positive or strictly negative derivative. There
is no feasible infinitesimal integer move, so continuous box KKT reasoning
does not apply to that coordinate.

For continuous coordinates, strict gradient interval signs remain valid.
At any original optimizer, holding its integer values fixed still permits
a small continuous move unless that continuous coordinate is at the
appropriate original endpoint. Thus a positive sign forces the original
continuous lower bound and a negative sign forces its upper bound. This
test can also be used before all integers have been fixed. Intersecting the
closure hull with already justified equations preserves its optimizer
containment invariant.

For the proposed convex closure, first require all integer coordinates to
be fixed. If the principal Hessian on the remaining continuous coordinates
is PSD, solve the resulting convex continuous box QP at those integer
values and the recorded continuous endpoints. That original integer slice
and continuous face contain every original optimizer. The convex solution
is therefore globally optimal for the original mixed problem.

A PSD continuous block with unfixed integer coordinates is not sufficient
for this closure rule. Integer optimization would still remain. If no
continuous coordinates remain, fixing every integer gives the immediate
zero-dimensional closure.

## 4. Sufficient localization on a good draw

Suppose the original mixed problem has a unique optimizer `x*` and full
point growth at least `g0>0`. At a level below one, any retained integer
cell is a singleton. Its retained-cell witness therefore has that exact
integer coordinate value, and

```
|y_i-x_i*| <= ||y-x*|| <= h_j sqrt(nL/(4g0)).
```

If this radius is less than one half, every retained integer value equals
`x_i*`. Hence all integer projection hulls are singletons. There is no
extra cell-width term for these integer coordinates after the transition.

For continuous coordinates the previous radius remains valid:

```
r_j=h_j[1+sqrt(nL/g0)/2].
```

Let `A=2+nL/g0`. The proposed conditions `h_j<=1/2` and `A h_j<=1/4`
guarantee the singleton transition and an integer radius strictly below one
half. They are conservative sufficient conditions. The final draft uses
`h_j<=1/(4A)`, which implies both because `A>=2`.

Assume in addition that every active continuous coordinate has a strictly
complementary signed gradient of magnitude at least `tau`. If `M` bounds
the maximum absolute Hessian row sum, `A h_j<=tau/(2M)` makes every such
continuous gradient sign detectable on the closure hull. All active
continuous coordinates are then fixed to their original endpoints.

The remaining coordinates are continuous and interior at `x*`; the integers
are already fixed. Perturbing these free coordinates within that same mixed
slice and applying point growth gives

```
H_free,free >= 2g0 I.
```

The PSD closure must therefore succeed. No strict-complementarity condition
is required on integer coordinates, and none is used. As before, the growth
and margin conditions only bound the stopping level; the actual closure
tests do not trust them.

## Targeted exact verification

The commands actually run were

```
python3 -B research-20261002/new-direction/check_sparse_mixed_bag_cells.py
python3 -B research-20261002/new-direction/check_sparse_bag_cells.py
```

The [mixed checker](check_sparse_mixed_bag_cells.py) reuses the genuine
sparse tree DP and adds integral cell refinement, mixed feasible rounding,
integer-slice enumeration for the verification oracle, singleton integer
fixing, and the all-integers-fixed closure requirement. The second command
checks that the shared implementation still passes the continuous cases.

The [mixed results](sparse-mixed-bag-cell-check-results.json) passed four
instances and 19 stages. They include an interior integer optimum with a
positive derivative, two tied integer labels with a continuum of continuous
optima, two integer coordinates combined with nonconvex continuous boundary
closure, and a purely integer problem with interior optimal labels.

All 444 finite bag min-marginals matched exhaustive allowed assignments;
1,171 rounded atoms remained feasible; 151 retained witnesses met the
`2E_j` bound; and 115 removed cells preserved the tested optimal points.
Six integer values were fixed from singleton hulls. Three cases reached
exact closure, including one with no remaining continuous coordinates. The
PSD case with two tied integer labels correctly did not close.

The continuous regression retained its previous results: five instances,
16 stages, 2,295 checked min-marginals, and three exact closures. Its
boundary-only intersection fixture also passed. Exhaustive small-instance
oracles are used only for verification, not claimed as the sparse algorithm
or an efficient mixed solver. No project-wide verification, CI inspection,
or external search was performed.
