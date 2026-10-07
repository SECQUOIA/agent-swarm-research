# Independent review of the selected-core Cauchy oracle

Date: 2026-10-02. Verdict: passed the actual
[core-coordinate addendum](../new-direction/core-only-noise-core-oracle.md).
I also read the complete generic polynomial fallback and checked the
transition from the reviewed all-dimensional count theorem. This is a
correctness review, not a novelty assessment.

## The selected core is fixed and has the required fallback interface

The [generic fallback](../new-direction/polynomial-exact-fallback.md)
explicitly selects one lexicographic global optimizer, including ties and
positive-dimensional optimizer sets. Its scalar singleton formulas use
two quantified blocks; reordering variables to put the core first does
not add blocks or change the bit-bound structure. All coordinate formulas
refer to that same point. The base exponential budget is independent of
sampled coefficient length and refinement precision, which enter with
an absolute polynomial exponent. Thus the addendum does not silently
replace an arbitrary-root output guarantee by a lexicographic guarantee.

Both ordinary output and fallback approximate this one fixed core. No
consistency of residual witnesses is required or promised. A nonunique
residual fiber therefore creates no selector problem for ordinary queries.

## Both containment invariants are sound

The retained cells cover every globally optimal core because each cell
containing one has a valid lower bound no greater than the optimum and
hence no greater than the incumbent. This reasoning includes boundary
cores and retained ties.

The feasible incumbent's core also survives. Its conditional true value
is at most its reported feasible objective. Therefore every generated
cell containing that core has lower bound at most the final incumbent
when it is the winning point. An old winning incumbent lies in a child
of a previously retained containing cell. A new one is a queried corner
of a current cell. Neither can be lost in the final filtering pass.
Equivalently, a historically pruned cell had lower bound strictly above
its then incumbent, which was at least the current incumbent; it cannot
contain the current winning core.

Consequently the coordinate hull contains both the returned incumbent
and every optimal core. Its squared diagonal length is the sum of squared
coordinate widths. The exact rational test in equation (4) certifies
the requested Euclidean core error to the selected optimizer, without
using uniqueness or an unverified growth premise. The objective interval
remains the independently valid interval from the cell algorithm.

## The cutoff and enlarged law pay for the extra output promise

Replacing `L` by `L_+=L+sigma` is a valid supplied upper bound and handles
the zero-curvature case uniformly. It enlarges the final numerical
factor by at most a factor depending on `k`.

On projected growth at least `g_0`, each retained cell's true near-optimal
corner is within `h sqrt(k L_+/(2g_0))` of the unique optimal core. Adding
one cell width and taking the coordinate hull gives equation (9).
The rational bound `D=4k+k^2 L_+/g_0` follows from
`sqrt(k)<=k` and `sqrt(x)<=1+x`. Its binary length is polynomial in the
base data. The prescribed terminal level consequently has depth
`poly_d(I)+O(q)` and ensures both requested tests on every good-growth
draw.

Failure of the actual hull test at any precision therefore implies the
single event `g<g_0`. The event is fixed before all queries; there is no
union over their terminal levels. The projected-growth formula and tail
apply in every core dimension, even though the predecessor's earlier
growth-based count integral was restricted to dimensions one and two.

With `g_0=sigma/(2kB)` and the stated enlarged grid size, the continuous
tail term and finite-grid discrepancy each contribute at most `1/(2B)`.
Hence the added fallback probability is at most `1/B`. Combining it
with the existing all-scale cap event by a union bound is sufficient;
the events need not be independent. The all-dimensional count moment
and its finite-law discrepancy are unchanged. Hull construction is one
linear pass through retained cells, and the larger terminal depth changes
only the fixed polynomial factor. Equation (14) is therefore one valid
random work factor simultaneously for all queries.

## Refinement and scope

On fallback, coordinatewise box clipping preserves feasibility and does
not increase distance to the selected exact point. Core coordinate error
at most `2^(-q)/(k+1)` implies the Euclidean core bound. Error at most
`2^(-q)/(2G)` in every coordinate gives objective error at most
`2^(-q)/2` by the stated one-norm gradient bound. Combining this with
an exact-value enclosure of width at most `2^(-q)/2` gives the requested
global interval. The logarithm of `G` has polynomial sampled input
length, so these refinements respect the fallback contract.

The one- and two-core-coordinate specialization correctly reuses the
earlier sharper truncated moment and retains its linear dependence on
`1+L/sigma`. The general statement uses the all-scale theorem's parameter
factor. Neither branch gives distance to any chosen residual optimizer,
nor does the noise theorem solve the unperturbed instance.

## Verification record

This review independently checked the actual statements, containment
induction, rational diameter bound, selector source, combined law budget,
and fallback error allocation. No new numerical diagnostic was needed:
the addendum changes output and stopping conditions, and its guarantees
follow from the exact inequalities above and already checked grid/fallback
interfaces. A targeted check of this review's local links, whitespace and
fences passed. No project-wide checks, CI inspection, external search,
or index edits were performed.
