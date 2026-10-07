# Independent review: the conditioned fan preordering obstruction

Date: 2026-10-02. Verdict: **PASS** for the actual normalized construction.
The reviewer read the complete
[fan note](../new-direction/fan-preordering-growth-obstruction.md), its
[origin-jet predecessor](../new-direction/box-preordering-growth-obstruction.md),
and the local SPN-graph audit. This review establishes the finite algebra
and mathematical implications; primary-source provenance and corrigendum
scope remain with the literature reader. No originality claim is inferred
from the calculation. The later minimum-width argument is reviewed in
the addendum below.

## Exact matrix, support, and conditioning

The current file uses the normalized nonnegative matrix

\[
 V=[e_1,e_2,e_3,(e_2+e_4)/2,(e_3+e_5)/2],\qquad C=V^THV.
\]

These are the actual constants audited here, rather than the earlier
unnormalized candidate. Nonnegative congruence preserves copositivity,
and the predecessor supplies an elementary proof that the displayed Horn
matrix is copositive. Direct exact multiplication gives the stated `C`.

All seven nonzero off-diagonal pairs form precisely the fan with hub 3
and outer path `1-2-4-5`. This counts positive and negative entries alike.
The three stated bags cover every pair and satisfy running intersection.
A triangle gives the lower bound on treewidth, so the graph has treewidth
exactly two. The quadratic can be represented by its unary and pairwise
monomial factors in these bags; no five-variable factor scope is needed.

For `Q=C+I/100`, copositivity gives growth at least `1/100` on the whole
nonnegative orthant and hence on the box. The feasible vector `e1+e2`
has zero `C` energy, proving that this growth constant is exact. Positive
growth makes the origin the unique box minimizer. Every diagonal of `C`
equals one, so the exact coordinate upper curvature is `101/50` and
the ratio is `202`. The absolute row sum bound of five gives the stated
full-Hessian norm bound `501/50` as well.

## Positive definite dual separator

The displayed `W` is symmetric and entrywise nonnegative. The reviewer
independently constructed an exact rational LDL factorization, checked
all five pivots positive, and reconstructed `W` from the factors. This
proves positive definiteness without relying on floating-point feasibility
or only checking entrywise signs.

The exact identities are

\[
 \langle C,W\rangle=-163,\qquad
 \operatorname{tr}W=12013,\qquad
 \langle Q,W\rangle=-4287/100.
\]

If `Q=P+N` with `P` positive semidefinite and `N` entrywise nonnegative,
then both inner products with `W` are nonnegative. The negative displayed
value excludes SPN decompositions even over arbitrary real coefficients.
It also excludes positive semidefiniteness of `Q`, so the quadratic is
nonconvex despite its positive orthant growth.

## Why the obstruction holds at every degree

The referenced origin-jet lemma applies to precisely the advertised full
preordering, including overlapping lower- and upper-slack sets and
arbitrarily high polynomial degrees. Its necessity argument is sound:

1. At the origin, all terms without lower slacks have nonnegative SOS
   constants. Their sum is zero, so each multiplier vanishes there.
   Every polynomial being squared therefore has zero constant, leaving
   a PSD quadratic jet and no linear jet.
2. The resulting linear part comes only from terms with one lower slack.
   Their constants are nonnegative and cannot cancel. They too vanish,
   making those terms start at degree at least three.
3. Terms with exactly two distinct lower slacks contribute only a
   nonnegative multiple of `x_i x_j` at degree two. More lower slacks
   contribute nothing to that jet.

Upper slacks have positive constant at the origin. Their negative linear
terms do not change this reasoning because all potentially problematic
lower-degree multiplier terms have already vanished. An overlap such as
`x_i(1-x_i)` is therefore handled. Repeated powers can be absorbed into
SOS multipliers. The quadratic jet must be PSD plus entrywise nonnegative,
contradicting the separator. Higher-degree cancellation cannot repair it.

The finite rectangular-cover consequence is also valid. Some closed cell
contains infinitely many positive diagonal points tending to the origin.
It therefore has all lower endpoints zero and strictly positive upper
endpoints. The same local argument applies to its own slacks. This does
not address nonrectangular partitions, extra generators, vanishing
multipliers, or strictly approximate lower bounds.

## Connected chains

For any number of fan blocks, adding the stated nonnegative bridge squares
preserves the lower growth bound. Making every block equal to `e1+e2`
annuls every bridge and attains the same ratio, so growth remains exactly
`1/100`. At most two bridge terms meet a coordinate; hence the coordinate
curvature/growth ratio is at most `206`.

Attach each bridge bag to the first bag of its two blocks. This produces
a tree decomposition, preserves connected occurrences of every variable,
and has maximum bag size three. Existing triangles retain the exact
treewidth lower bound.

Restricting all variables outside one block to zero preserves every SOS
and converts box slacks into original slacks, zero, or one. The restricted
quadratic is `Q+(d/100)e1 e1'`, where `d<=2` is the bridge degree. Its
trace against `W` is at most

\[
 -4287/100+(2/100)1773=-741/100<0.
\]

Thus the restriction cannot have a full-preordering identity; neither
can the whole chain. The same negative trace proves that a principal
quadratic restriction is nonconvex. These arguments hold for arbitrary
chain length, not only the finite instances in the checker.

## Significance and verification performed

The mathematical addition is a conditioned, connected width-two example
for the specified exact unmultiplied certificate obstruction. The
non-SPN fan itself is established prior work according to the source audit.
This review does not establish that the displayed congruence or witness is
new, and it does not rely on an unresolved graph classification. It also
does not claim this easy explicit family is difficult to optimize or to
certify by a different method.

The reviewer ran

```sh
python research-20261002/reviews/check_fan_preordering_review.py
```

The [persistent diagnostic](check_fan_preordering_review.py) passed exact
Horn congruence, five positive LDL pivots and matrix reconstruction, the
trace identities, complete fan support, and exact growth/curvature checks.
It also checked five explicit chain decompositions, totaling 119 bags,
including tree connectedness, edge coverage, and running intersection;
all 31 one-block restrictions had the asserted negative separator bound.
No randomized or floating-point diagnostic was used in this reviewer run.
The author's separately reported determinant and sampled-growth checks
were not rerun or attributed to this reviewer.

The finite diagnostic supplements the universal cone, growth, and jet
arguments. It neither enumerates all preorderings nor proves the
arbitrary-degree conclusion computationally. No project-wide checks,
CI inspection, external source search, or index edits were performed.

## Addendum: the classical forest case and minimum width

The reviewer reread the actual file's added forest-SPN proof. It is valid.
For a leaf with nonnegative incident coefficient, the leaf diagonal and
cross term are entrywise nonnegative, and the remaining principal matrix
is copositive. If the incident coefficient `b` is negative, copositivity
forces its diagonal `a` to be strictly positive. Subtracting the rational
PSD form `(a*x_i+b*x_j)^2/a` leaves a zero leaf row and column and changes
only its neighbor's diagonal. The remainder is copositive because its
value at every nonnegative remaining vector equals the original form
at the feasible minimizing leaf value `x_i=-b*x_j/a`. Isolated diagonals
are nonnegative. Leaf induction therefore supplies the claimed SPN
decomposition for every forest.

Since graphs of treewidth at most one are forests, the jet equivalence
now proves a precise minimum-width statement: two is the minimum
interaction treewidth of a homogeneous copositive quadratic without
the specified unmultiplied box-preordering identity. This conclusion
uses the self-contained leaf proof, not an unverified broad SPN-graph
classification. It is not a minimum-width claim about other polynomial
objectives, certificate families, or optimization hardness. The argument
is a classical positive baseline, as the author explicitly states.
