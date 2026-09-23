# Second review: weighted tree cut-direction parameter

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed note: `notes/potential-flow-weighted-tree-sign-pattern.md`.
Dependency read: `notes/potential-flow-fixed-support-weighted-tree.md`.
Verdict: **PASS** for the structural strengthening and inherited exact
`N^{O(k)}` rational optimization guarantee.

This audit checks correctness and parameter scope. It does not establish
publication priority or a fixed-parameter tractable running time.

## Contraction and orientation preserve the problem

With incidence columns positive at the tail, tree cut summation gives the
unique `Aw=c`. The identity

```
c^T pi=sum_e w_e beta_e x_e|x_e|
```

is independent of the potential reference because `sum c=0`. An edge with
zero objective cut flow contributes nothing. Contracting all such edges
and replacing each cluster's nomination interval by the sum of its
original intervals preserves the projected nomination domain exactly.
Every balanced aggregate nomination has an original box-feasible
disaggregation, and retained flows agree by cut summation. Internal
potential drops may change under disaggregation, but the displayed
identity proves they have no missing objective contribution.

After contraction the remaining graph is still a tree, and each retained
cut weight is nonzero. Reversing an edge reverses both `w_e` and the
physical flow, leaving the objective contribution unchanged. Thus all
retained weights may be made positive by edge orientation. If none remain,
the objective is zero and is handled separately; the nontrivial parameter
and counting arguments below concern a tree with at least one edge.

## Degree-two objective coefficients do not obstruct path ordering

A vertex is unmarked exactly when it has one incoming and one outgoing
edge. In particular it has undirected degree two. Suppressing all such
vertices therefore produces a tree on the `k` marked vertices, with
`k-1` paths. Every path is consistently directed: at each internal vertex
the entering path edge must be the incoming edge and the next edge the
outgoing edge, or the same argument applies in reverse.

An internal coefficient need not vanish. If the incoming and outgoing
positive cut magnitudes are different, its coefficient is their signed
difference. This affects their magnitudes but does not reverse either
arrow. For fixed positive resistances and the smoothed quadratic law,
tree flows are linear in nominations and differentiation gives

```
h_tail-h_head=beta_e(2|x_e|+rho)w_e>0.
```

This identity has the correct orientation sign. It follows directly from
the objective identity and the linear tree flow map, with `h` defined
modulo a common constant on the balanced nomination space. It requires
neither equal successive `w_e` nor zero internal objective coefficients.
Strict gradient decrease consequently holds along every suppressed path,
including when some physical edge flows are zero.

## The nomination faces remain complete

At a maximum of the differentiable smoothed objective on the box with
one balance equation, its gradient lies in that polytope's normal cone.
A common scalar balance multiplier therefore puts upper nominations where
`h` is larger, lower nominations where it is smaller, and any interior
nomination at equality. This holds for degenerate boxes and nomination
polytopes as well; fixed coordinates can be regarded as either endpoint.

Strict path ordering allows at most one internal vertex at the multiplier
value. Along a directed path, all vertices before the threshold can be
fixed to their upper bounds and those after it to their lower bounds.
Enumerating every cut and every possible free pivot covers the optimum's
internal nominations. Leaving all marked nominations free is sufficient:
there is no need to enumerate three statuses at marked vertices. The
larger free face still consists of valid original nominations after its
box bounds and balance are imposed.

Each path has only linearly many choices in its number of internal
vertices, including the two extreme cuts and the empty-path case. There
are `k-1` paths, so the family size is `N^{O(k)}`. Every face has at most
`k+(k-1)=2k-1` free nomination coordinates before balance or other affine
degeneracy is eliminated.

The family depends only on the cut-current orientations. It is independent
of resistance values, nomination values, and the smoothing parameter.
The smoothed objectives converge uniformly to the original objective on
the compact nomination polytope at each fixed resistance vector. A
subsequence of maximizers lies in one fixed closed face, and its limit is
an original maximizer on that face. Fixing the resistance vector of a
joint optimum therefore transfers a joint optimum to the same enumerated
family. This argument does not require a discrete optimizer to vary
continuously with resistance.

## The support and path counts are correct

For a nontrivial contracted tree, every leaf has a nonzero aggregate
objective coefficient. A degree-two marked vertex has both arrows entering
or both leaving, so its coefficient is respectively minus or plus the
sum of two strictly positive cut magnitudes, and is also nonzero. Thus
every marked nonbranching vertex is in the aggregate objective support.
Contraction does not increase its support size above the original `p`.

If the tree has `L` leaves, its branching count is at most `L-2`, from
the tree degree identity. Since `L<=p`, the marked count obeys

```
k <= p+(L-2) <= 2p-2.
```

Zero objective is already handled separately; a nonzero zero-sum objective
has `p>=2`. No bound with a negative right-hand side is being used in
the trivial case.

For a path initially oriented left to right, each cut weight is exactly
the cumulative objective sum on its left. Contracting zero-weight edges
removes zeros from this sequence without changing retained cut weights.
At an internal retained vertex, adjacent weights of the same sign give
one entering and one leaving arrow; opposite signs give two entering
or two leaving arrows. There are consequently exactly `t` internal marks
for `t` sign changes, plus the two endpoints. Hence `k=t+2`, and equal
sign of every nonzero cumulative sum gives `k=2` even with growing
objective support. Replacing `c` by `-c` reverses all arrows and preserves
the marked set, so the same parameter applies to minimization.

## Inherited rational optimization and verification

For fixed nominations on a tree, each resistance appears linearly in the
objective. The endpoint rule based on `w_e x_e|x_e|` therefore remains
exact, and its endpoints belong to either the allowed finite set or the
allowed closed interval. Zero-flow boundaries cause no discrepancy.

On a nomination face of dimension `O(k)`, tree flows are rational affine
functions. Their sign hyperplanes split it into `N^{O(k)}` rational
quadratic cells. The inherited active-face stationarity method is valid:
an independent basis of active normals at a global quadratic maximizer
appears in the enumeration; the corresponding rational linear stationary
system is feasible; and all feasible solutions of that same system have
the same quadratic value. A rational LP point thus attains the value,
even for singular quadratics or degenerate nomination faces. Comparing
these candidates is exact rational arithmetic.

Rational cut sums, endpoint choices, cluster disaggregation, and tree
potential integration then recover an optimal original physical state.
The new face dimension changes only the inherited exponent to `O(k)`.
Positive resistances and the absence of extra pressure or flow feasibility
constraints remain essential assumptions. No cycle extension or runtime
of the form `f(k)N^C` is implied.

I inspected and reran
`code/potential_flow_mpd/weighted_tree_sign_pattern_checks.py`.
It passed 148 exact cut-direction counts and compared the proposed face
family against 2,818 stationary candidates in two five-support path cases
with respectively two and three marks. The stationary optimization checks
use floating-point linear algebra and LP, as documented in the dependency;
they are supplementary evidence, not a certified implementation of the
rational algorithm. No unresolved structural or mathematical defect was
found.
