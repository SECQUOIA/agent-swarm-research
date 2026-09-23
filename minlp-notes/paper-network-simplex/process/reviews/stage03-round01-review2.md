# Stage 3, round 1 — independent review 2

**Verdict: accept this stage. No major or minor defects identified.**

Reviewed the frozen `process/snapshots/stage03-round01` snapshot, principally
`sections/03-structured-oracles.tex`, its foundation and compression dependencies,
new references, and integration in the manuscript. I did not read another
current-round report, coordinate judgments, edit manuscript sources, or spawn
agents.

## Enumerated findings

1. **No major findings.** I found the stated hull characterizations,
   reconstruction algorithms, and separation arguments correct within their
   expressly restricted graph classes.
2. **No minor findings.** No required local correction identified.

## Detailed checks

### R2-S3-C1 — graph classes and orientation signs (verified)

At `sections/03-structured-oracles.tex:11–58`, orienting each theta path traversal
between the same two terminals makes the three signed circulation values sum
to zero. Assigning those values as `s,t,-s-t` and changing the third path's sign
from epsilon to minus epsilon gives the displayed `s,t,h=s+t` arc expression.
The interval construction therefore applies to circulation deviations even
when original arc directions alternate or the chosen reference flow violates
capacity bounds. A cycle uses one scalar and an independent loop is its
rank-one special case.

The later parallel-path section deliberately returns to all traversals having
the same orientation and uses `q`, not the theta-specific signed observation.
This is consistent with its zero-sum column equations. It covers any number
of parallel arcs or internally disjoint paths, not arbitrary nested
series–parallel blocks. Loops are separately handled; block articulation
vertices are covered by the already proved deviation factorization.

No hidden global label expansion occurs. Local labels use the globally shared
simplex weights, and labels absent in a block belong to that block's merged
state. The interval construction checks all observations on a path, including
incompatible repeated observations and zero-weight observations.

### R2-S3-C2 — theta feasibility and Minkowski sums (verified)

At lines 60–128, the rectangle's attainable sum interval proves all five
nonemptiness conditions, and the projection of its intersection with the sum
strip gives exactly the six stated attained supports. These formulas are
correct for segments and points as well as full-dimensional polygons.

The proof that six supports describe a planar sum does not incorrectly extend
a normal-fan statement from two dimensions to higher dimensions. Every exposed
edge of a two-dimensional sum must contain a nontrivial segment from a summand,
and all nontrivial contributing segments are parallel. For a one-dimensional
summand, at least one defining boundary contains its full affine line. This
ensures the same permitted edge directions in all cases. The separate argument
for a segment sum and point sum closes the lower-dimensional cases.

### R2-S3-C3 — affine branches and original-coordinate coefficients (verified)

At lines 137–205, every failed condition is a convex piecewise-affine expression
required to be nonpositive. A maximizing affine branch is globally bounded by
zero on the hull and agrees with the candidate violation. This is an exact
valid cut, not merely a local linearization.

In each support branch, one product appears at most once for a given state.
The local feasibility comparisons either use distinct coordinate types or
compare two observations of the same type; a repeated identical observation
cancels. Different states have different product indices. Aggregate `s,t`
coordinates use distinct original arcs, and `h` uses their sum. This supports
the unit `x,z` coefficient claim in the explicitly stated rational scaling.

The time bound includes a constant amount of work per observed block/label
pair and per block, plus observation scanning and the original domain checks.
The observation-grouping proviso and the distinction between arithmetic counts
and bit complexity are explicit. The claim does not bound the size of the
fully enumerated inequality family.

### R2-S3-C4 — compact cycle/theta reconstruction (verified)

At lines 207–255, intersecting the next state domain with the reflected suffix
sum has exactly the displayed coordinate intervals. The current aggregate is
in the remaining sum, so that intersection is nonempty. The specified choice
of `s` is within its tight bounds; the choice of `t` satisfies both its
individual interval and the sum interval. Subtraction preserves the induction.
Empty suffixes are handled by zero supports.

Normalizing only positive-weight states gives valid flow-domain coordinates.
The normalized merged coordinate can be shared as the block default for all
its constituent global states. If its weight is zero, that default is unused;
choosing the feasible aggregate coordinate is valid. An entirely unobserved
block needs only the same default. Consequently the compact storage and
arithmetic count do not falsely include writing every state-by-arc flow.

### R2-S3-C5 — transportation projection and complete subset description (verified)

At lines 278–384, the shifted transportation matrix has row sums
`r_i=delta_i-sum_j ell_ij`, column sums `c_j=-sum_i ell_ij`, and capacities
`C_ij=u_ij-ell_ij`. Local conditions imply nonnegative capacities and column
targets. Nonnegativity of row targets is not assumed without proof: it follows
from the complementary subset inequality, using zero aggregate sum. The total
row and column targets agree.

For any source-side row subset, placing each column on whichever side is less
expensive gives precisely the minimum of its incoming capacity from that row
set and its sink capacity. Shifting back converts every such cut condition
exactly into the claimed subset inequality. Thus the maximum-flow/minimum-cut
argument proves sufficiency, including zero total target. No row or column
capacity constraint is omitted. Empty and full subsets are redundant under
the local conditions as stated.

At lines 396–448, a negative shifted row yields a valid lower-bound cut.
Otherwise an insufficient maximum flow yields a subset violation because
optimizing the column-side choices cannot increase the deficient cut value.
Choosing active affine alternatives in the concave right side gives an affine
majorant, hence a globally valid upper bound that preserves the violation.
The sign of this branch argument is correct.

The node and arc counts include the merged column and both source/sink arcs.
The rational bit-complexity explanation relies on a polynomial augmenting-path
rule, not arbitrary Ford–Fulkerson choices. Reconstruction and zero weights are
consistent with the original scaled path bounds.

### R2-S3-C6 — joint theta example (verified)

At lines 257–275, each one-label decomposition has a state flow of weight
one third and complementary flow of weight two thirds, with correct aggregate
flow. Jointly, the two observed states would require two thirds on an arc whose
aggregate is only one third. The displayed residual inequality has right side
one third and left side zero. Its violation and interpretation are correct.

## Independent executable evidence

I wrote `verification/reviewer2/stage03-round01/check_oracles.py`, without importing
repository oracle code. The adjacent `result.json` records the successful run.
The check uses exact integer enumeration of state domains and their sums:

- 36 nonempty theta families, checking 839 aggregate integer targets against
  the six-support description and reconstructing every enumerated feasible
  aggregate by the displayed suffix algorithm.
- 45 nonempty parallel-path families with two through five rows, checking
  4,615 aggregate integer targets against *all* subset inequalities.
- 65 local infeasibility checks.
- Exact agreement between the shifted cut expression and its original-coordinate
  subset expression for every tested feasible target and every row subset.

Command actually run:

```sh
/home/sgusev/miniconda3/envs/minlp-notes/bin/python paper-network-simplex/verification/reviewer2/stage03-round01/check_oracles.py
```

All checks passed. These finite integer checks supplement the independent
proof review; they are not offered as a proof for arbitrary rational points.

## Review limitations

I did not independently certify bibliographic priority, retrieve every new
reference, or compile a private PDF. I inspected the source and mathematical
integration rather than final page layout. The graph sign checks were by direct
algebra and the previously reviewed path-coordinate construction; the new
executable evidence exercises the resulting coordinate domains. Later unwritten
sections and industrial performance are outside this stage's claims and review.
