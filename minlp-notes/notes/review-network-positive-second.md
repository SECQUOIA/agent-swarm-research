# Second independent audit of cycle/theta network–simplex hulls

Date: 2026-09-04. Reviewer: `review_extension`. Status: passed, including the constructive decomposition corollary added after the first review. No literature-priority claim is certified.

Reviewed [the positive-network note](common-factor-network-positive.md). The exact original-space membership conditions, linear inequality separation bound, unit flow/product coefficient corollary, and compact rational decomposition are mathematically sound within the stated graph and equality-balance scope.

## Block coordinates and global state consistency

For an equality-constrained flow polytope, differences from a reference solution lie in the circulation kernel. Its cycle space splits as a direct sum over the undirected biconnected blocks: every undirected cycle lies in one block, and cycle vectors span the kernel. Bridges therefore have fixed flow. At articulation vertices each block's circulation separately has zero divergence. This proves independence of the block coordinates even when other blocks attach to internal nodes of a theta path.

A cycle contributes one signed scalar circulation coordinate. In a theta block, orient its three paths conceptually between their common endpoints. Their signed circulation deviations sum to zero, so they can be written `s,t,-s-t`. Absorbing the last minus sign and actual arc orientations gives the three coordinate types and signs used in the note. Arc bounds consequently give exactly an interval or the six-inequality polygon in equation (2). Parallel paths and arbitrary arc directions do not alter this argument. Self-loops can be removed and treated as independent scalar factors. A spanning-forest balance solution suffices for the reference; it need not satisfy capacities.

The simplex disaggregation and transformation to scaled block coordinates are exact. In particular, an observation satisfies

```
epsilon_e (z_ej-y_j v_e)=h_e(theta_j),
```

including observations with negative arc sign. Intersecting all repeated observations of one type correctly requires them to agree, rather than allowing independent choices.

Each block may merge a different set of unobserved simplex states. This causes no global inconsistency: normalize that block's residual coordinate by its total merged weight, then assign this same normalized block coordinate to every original state merged there. The contribution of each such state is its own global weight times that coordinate. After doing this separately in all blocks, each original state has one feasible full flow because the block domains form a Cartesian product. The state weights remain the common values `y_j` and `1-sum y_j` throughout. There is no need to merge the same states in all blocks.

If a state weight is zero, its initialized scaled coordinate intervals are zero singletons. Feasibility therefore forces every associated observation to be zero and the block coordinate to vanish. A zero residual weight also forces a zero residual coordinate; its unused normalized default can be any feasible base-block coordinate. No division by zero is required.

## State feasibility and Minkowski sums

For a cycle, state nonemptiness must be checked separately from aggregate lower and upper sums. The note now includes this necessary condition.

For a theta state, the three interval nonemptiness checks and the two sum-interval overlap checks in (7) are necessary and sufficient. Eliminating the other coordinate gives exactly the six tight bounds in (8). For example, the least feasible `s` is `max(ell_s,ell_d-u_t)`, and its largest feasible value is `min(u_s,u_d-ell_t)`. The corresponding formulas for `t` and `s+t` follow by the same direct interval argument. All six bounds are attained when the state is nonempty.

A two-dimensional Minkowski sum of these polygons has only the same three possible edge directions: an exposed edge is the sum of exposed faces of the summands, and any positive-dimensional summand face in a one-dimensional sum must have that direction. The support values in the six associated normals add. A degenerate state segment must lie along one of these directions, because its affine hull is forced by a tight defining inequality. Segments and points therefore cause no extra missing normal. This proves the six aggregate conditions exactly, including degenerate cases.

## Separation and coefficient scope

All lower expressions are convex piecewise affine and all upper expressions are concave piecewise affine. For instance, `ell_d-u_t` is convex and `u_d-ell_t` is concave. Each failed condition can be written as a convex piecewise-affine function bounded above by zero. Choosing its active affine branch gives a globally valid affine inequality with the same violation at the tested point. This remains valid when the candidate itself violates a local state condition; validity is needed only on true hull points.

The finite branch expansion does have coefficients in `{-1,0,1}` on flows and observed products. A state support branch contains either one observation or observations of distinct coordinate types. The local sum-feasibility conditions likewise use distinct types. In a same-type lower-versus-upper check, selecting the same observation causes cancellation. Across states the product indices are distinct. Thus no observed product receives coefficient two. Aggregate `s` and `t` can each be read from one reference arc, and their sum uses two different arcs. Simplex coefficients may contain network data and are not subject to the unit-coefficient assertion.

This assertion concerns a chosen rational linear description in the original coordinates. Clearing denominators or choosing a different representative modulo flow equalities can change coefficient magnitudes. It does not establish unit primitive-integer coefficients or unit EC&R multipliers.

There is one residual state per block, and the number of explicit block/state pairs is at most the number of observations. Scanning the arcs, observations, and simplex coordinates therefore gives the stated linear rational-arithmetic operation bound once indices are grouped. Computing the reference, block coordinates, and original linear feasibility checks fits the same bound. Sorting ungrouped indices is correctly listed separately. All arithmetic uses rational input combinations of polynomial bit length; the theorem is not a constant-bit-cost claim.

## Constructive decomposition

The new suffix procedure is valid. Sums of tight state supports describe each remaining Minkowski sum exactly. Reflecting it about the remaining aggregate `r` changes each lower bound to `r_h-suffix_upper_h` and each upper bound to `r_h-suffix_lower_h`. Intersecting with the current state therefore gives precisely the six bounds displayed in the note. This intersection is nonempty whenever the remaining aggregate belongs to the remaining sum.

The proposed point selection is correct for any nonempty resulting polygon. Set

```
s=max(ell_s,ell_d-u_t),
t=max(ell_t,ell_d-s).
```

The first coordinate is its attained lower support and is at most `u_s` and `u_d-ell_t`. Since `s>=ell_d-u_t`, both arguments defining `t` are at most `u_t`. The sum is at least `ell_d`; if `t=ell_t`, it is at most `u_d` by the upper bound on `s`, and if `t=ell_d-s`, the sum is exactly `ell_d<=u_d`. Thus all original inequalities hold. Subtracting this point leaves a feasible suffix aggregate. A zero-state suffix is the singleton zero and is correctly represented by six zero supports. Intervals have the analogous elementary construction.

After sequential decomposition, division by each positive explicit state weight yields its normalized feasible block coordinate. One normalized residual coordinate per block supplies the common default for every unobserved original state; only observed block/state pairs need exceptions. Hence the full decomposition has at most `m+1` positive-weight graph points, stored through a reference flow, block data, defaults, exceptions, and the global weights. Its compact output size is linear in the graph, state list, and observations. Writing all full flow vectors can require `Theta(m|E|)` entries, as the note correctly states.

I implemented an independent exact constructive check in [audit-network-positive-decomposition.py](../code/audit-network-positive-decomposition.py). It generates feasible sums from independently selected witness points, then decomposes those sums using the suffix rule. All 400 rational instances, containing 1,860 state polygons, passed direct checks against every original state inequality and the exact sum. Cases include negative coordinate values, zero singletons, and degenerate coordinate or sum intervals. This specifically checks the new decomposition; it does not duplicate the author's 400 LP membership comparisons or test graph-block extraction.

## Scope and example

The equality-balance assumption and the restriction on individual biconnected blocks are essential to the proof. Arbitrarily many allowable blocks may meet at articulations, but a general series–parallel block with more than two cycles is not covered. Adding slack arcs for inequality balances may violate this class. Extra linking inequalities and nonlinear flow physics cannot be imposed before convexification merely by intersecting this hull afterward.

The final single-theta example is correct: each of two observed states separately can use the third path with weight `1/3`, but they cannot both do so when the aggregate third-path flow is `1/3`. The displayed joint inequality follows from the residual state's upper support on `s+t`, and its violation is exactly `1/3`.

The result is a correct structural specialization of classical disaggregation and planar Minkowski sums. This review establishes correctness of the stated formulas and construction, not that the specialization is absent from the literature.
