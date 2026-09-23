# Weighted objectives at bounded block rank: nomination-face reduction

Date: 2026-09-06. Status: passed [first independent proof review](review-potential-flow-reopened-weighted-faces.md), [second independent proof review](review-potential-flow-reopened-weighted-faces-second.md), and root review. This note closes the structural part of the weighted bounded-block direction. These are internal checks, not external peer review or a literature-priority certification. It does not by itself provide an optimization algorithm for sums of the resulting block functions.

## Claim

Fix a positive rank bound `r` and objective-support bound `p`. Consider a connected passive quadratic network with positive fixed rational edge resistances, balanced rational nomination intervals, and a rational potential objective `c^T pi` with `sum c=0` and at most `p` nonzero coefficients. Suppose every biconnected block has cycle rank at most `r`. There is a polynomially constructible family of `n^{O(rp)}` rational nomination faces, each having `O(rp)` free nomination coordinates, such that at least one face contains a global maximum. The faces are taken after the objective-preserving reductions below; feasible reduced nominations admit rational disaggregation. The result also applies to a fixed positive asymmetric quadratic law on each edge.

If `c=0`, the objective is identically zero and any feasible rational nomination suffices. A nonzero balanced vector cannot have support one. The substantive statement therefore concerns `p>=2`.

The face family depends on the graph, objective coefficients, and nomination intervals, but not on the resistance values. Consequently the structural conclusion also holds for joint optimization over independent compact allowed resistance sets. That last observation does not supply an optimizer for variable-resistance block functions.

A face here fixes some nomination coordinates at interval endpoints and leaves the others within their intervals, then imposes exact total balance. Coordinates fixed by an interval of zero width need no special treatment.

## 1. Block decomposition and objective-preserving reductions

Use the incidence tree with one node for each block and one node for every original vertex, joining a block to its vertices. The leaves include nonarticulation vertices. In the minimal subtree spanning the nonzero objective vertices, a block node represents a retained **whole block**: removing a leaf incidence of a nonsupport vertex does not remove that physical vertex or its nomination variable.

A block or a tree of blocks attached through only one retained articulation, with no objective support away from that articulation, can be pruned. Merge its nomination intervals into the articulation interval by Minkowski sum. For a prescribed aggregate nomination, rational disaggregation into the original intervals is possible. The external state depends only on that aggregate; the removed passive subnetwork admits a unique state for its local balanced effective nominations. Its objective coefficient is zero away from the attachment, so all attainable objective values are preserved.

There is a stronger contraction needed for zero adjoint currents. For any block `B`, remove its edges and let `G_v` be the component containing `v`, for each `v` in `B`. Define

```
gamma_v = sum_{u in G_v} c_u.
```

If every `gamma_v` is zero, contract the entire block to a single vertex `w`, summing the nomination intervals and objective coefficients of its vertices. Delete the block's edges. This also preserves exactly the attainable objective values.

To verify contraction, fix nominations outside `B`. The flows and relative potentials within `G_v` depend on nominations at its vertices other than `v`; its root nomination is supplied by the block. Thus changing a root potential by a constant changes that component's objective by `gamma_v` times the constant, which is zero. The original objective can be written as

```
c^T pi = sum_v sum_{u in G_v} c_u (pi_u-pi_v)
         + sum_v gamma_v pi_v.
```

The second sum vanishes. A feasible state contracts by translating each component so its root potential becomes the common potential at `w`. Conversely, disaggregate the nomination at `w` within the original root intervals. The effective injections into `B`, after accounting for the already determined exterior flows, sum to zero by conservation at `w`. Solve the passive block for these injections, and translate each exterior component to its recovered root potential. This lifts the reduced state and preserves its objective. Any admissible fixed choice of the removed resistances is sufficient. Only a balance equation and nomination boxes are used; scenario-filtering capacities or potential bounds would invalidate this argument.

Apply these operations until no removed structure remains. They preserve the block-rank bound and do not increase objective support. The zero-block test is purely combinatorial. The induced `gamma` values of every surviving block are unchanged by other zero-block contractions. If the reduced objective is zero, no optimization is needed.

## 2. Only O(p) special blocks and ordinary chains

Let `T` be the minimal block-incidence subtree spanning the remaining objective support. Every leaf of `T` is a support vertex. It has at most `p-2` nodes of degree at least three, and its total excess degree `sum(deg-2)` over these nodes is at most `p-2`.

Mark vertex nodes of `T` that belong to the objective support or have degree at least three. Call a block **special** if its block node has degree at least three in `T` or it is adjacent to a marked vertex node. There are `O(p)` special blocks. The sum of their degrees in `T` is also `O(p)`: degrees of branching nodes sum to `O(p)`, and all remaining selected block nodes have degree two. Equivalently, suppress unmarked degree-two nodes in a tree whose marked set has `O(p)` nodes.

The remaining blocks form `O(p)` disjoint ordinary chains, each joining special blocks. Every ordinary block has exactly two retained ports, no objective support, and no retained attachment except those ports. Its other physical vertices remain present, with zero objective coefficients and their own nomination intervals. All branches outside `T` have already been pruned and their nominations aggregated at their attachments.

For an ordinary block with ports `a,d`, its induced adjoint sources are `I` at `a` and `-I` at `d`, where `I` is the sum of objective coefficients on one side of the block. This `I` is constant along a chain, up to a consistent orientation. It is nonzero: otherwise every induced source of that block would be zero and the block would have been contracted in Section 1. This nonzero condition is essential; a chain with identically zero adjoint can otherwise leave arbitrarily many nominations free.

## 3. First stage: at most one active ordinary block per chain

Fix resistances and smooth each law by setting `g_e^rho(x)=g_e(x)+rho x`, for `rho>0`. This has a continuous, strictly positive derivative even when the positive and negative quadratic coefficients differ. The smoothed potential objective is differentiable in nominations. Its gradient, modulo a constant, is the electrical adjoint `h` solving `L h=c`, with strictly positive differential conductances.

In an ordinary block, its effective electrical sources are `I,-I`. The two-terminal maximum principle puts all internal adjoint potentials strictly between the port potentials. For a nonbridge biconnected block, strictness follows from two-vertex-connectivity and the strong maximum principle; a bridge has no internal vertices. The sign of the port difference is the sign of `I`, and the magnitude is nonzero. Along an ordinary chain, the port values are strictly ordered and the open ranges of consecutive blocks are disjoint.

At a maximizer over the balanced box, the normal-cone condition supplies one scalar `lambda` with

```
h_v>lambda implies b_v=u_v,
h_v<lambda implies b_v=l_v.
```

Thus on each ordinary chain, all nominations except those in at most one block are saturated in the order determined by the chain orientation and `I`. If `lambda` equals an inter-block articulation value, choose either adjacent block: leaving that whole block free includes the articulation. If `lambda` lies outside the chain's closed range, all internal chain nominations are saturated on the same side. Vertices belonging to special blocks are left free regardless of their adjoint values. In particular, an endpoint shared by a selected block and an unselected block is treated as free; there is no conflicting assignment.

Enumerate one selected ordinary block per chain or the two all-saturated alternatives. Along each chain the saturated sides are determined by its known nonzero `I`. Leave all nominations in special and selected blocks free. The number of these coarse faces is `n^{O(p)}`, independent of `rho` and resistances. At most `O(p)` blocks have free nominations.

Let `rho` tend to zero along a sequence of smoothed maximizers. Uniform state bounds and continuity of strictly convex energy minimizers give uniform convergence of the smoothed objectives on the compact balanced box. A subsequence lies on one fixed closed coarse face, and its limit is an original global maximizer on that face.

## 4. Second stage: force unimodality only inside the chosen blocks

Fix one coarse face that contains an original global maximum. The nominations outside its selected and special blocks are now frozen. In each selected or special nonbridge block `H`, mark every vertex of internal block degree at least three, every retained port (an incident vertex in `T`), and every objective-support vertex. Ports already include the support vertices, but the latter condition makes the source accounting explicit. The degree identity bounds the first set by `2r_H-2`; Section 2 bounds the total number of ports over all such blocks by `O(p)`. Hence the total number of marked vertices is `O(rp)`.

Suppress the unmarked degree-two interiors into maximal paths. For a block with `k_H` marked vertices there are `r_H+k_H-1` paths. Every such block has at least two marked ports. Bridge endpoints are marked directly. The total number of paths is `O(rp)`.

Smooth the laws again, and perturb the objective by

```
delta sum_{v in U} (pi_v-pi_ref),
```

where `U` consists only of path-interior vertices of the selected and special blocks, and the reference vertex is marked. The optimization remains restricted to the fixed coarse face. At each `v` in `U`, the electrical adjoint source is exactly `delta>0`: `c_v=0`, the vertex has no unmarked attachment to another retained block, and every removed branch has already been contracted into its nomination interval.

Along a suppressed path, the successive adjoint currents satisfy `j_i-j_(i-1)=delta`. Therefore the adjoint values increase and then decrease, with a possible maximum plateau of exactly two adjacent vertices. Every horizontal level contains at most two interior vertices. The normal-cone condition for the remaining balanced-box face again has one global `lambda`. Each path's nomination pattern is lower endpoints, an optional free pivot, upper endpoints, an optional free pivot, lower endpoints. It has at most two free internal coordinates and polynomially many choices.

Leave all marked coordinates free and enumerate these path patterns. The resulting family has `n^{O(rp)}` subfaces, each with `O(rp)` free nominations. Uniform convergence as `delta,rho` tend to zero and a fixed-face subsequence show that one subface still contains a global maximum of the original objective. This is a two-stage existence argument: the first face is fixed before adding the local objective perturbation. A single global perturbation would disturb the zero-source chain structure and is not used.

For completeness, uniformity follows from the usual passive-network flow bound `|x_e|<=B`, where `B` bounds total positive nomination. With `0<rho<=1`, normalized edge drops are bounded by `max(1,beta_max)(B^2+B)`, with `beta_max` the largest one-sided quadratic coefficient; path sums bound all normalized potentials. The perturbation is uniformly bounded by `delta |U|` times that potential bound. For joint continuity in nominations and smoothing, use a fixed spanning-tree right inverse to correct a feasible flow by a quantity tending to zero when nominations vary. Energy minimality, compact flow bounds, and strict convexity identify every subsequential limit as the unique limiting physical flow. Summing edge drops along fixed paths gives potential continuity, and compactness then gives uniform convergence for the smoothing limit.

## 5. Algorithmic consequence and remaining scope

Every retained subface is a compact rational polytope in `O(rp)` free coordinates after balance elimination. Its reduced nominations are rational affine functions of those coordinates. The reductions and face enumeration are rational and polynomial for fixed `r,p`; all rational disaggregation operations preserve polynomial encoding length.

For cacti, composing this lemma with the separately developed fixed-dimensional affine-nomination accuracy-bit optimizer in [the reopened weighted investigation](potential-flow-reopened-weighted-investigation.md) yields the desired polynomial-in-input-and-accuracy-bits weighted optimization guarantee for a fixed objective-support bound and fixed edge laws, allowing unbounded total cycle rank. The combined statement and its review status are recorded in [the weighted cactus result](../results/potential-flow-weighted-cactus-accuracy-bits.md).

For general bounded-rank blocks, the face lemma removes the structural obstruction, but controlled approximation and optimization of the resulting many local algebraic functions remains to be established. No such general algorithm follows merely from this lemma.

The argument uses familiar block-cut decomposition, maximum principles, box KKT conditions, and the repo's positive-source path perturbation. Its potential contribution is their two-stage combination, including contraction of blocks whose induced objective-source vector is zero. No literature-priority claim has yet been checked for this lemma.

## Targeted nonlinear checks

[`reopened_weighted_contraction_checks.py`](../code/potential_flow_mpd/reopened_weighted_contraction_checks.py) compares physical states before and after zero-induced-source block contraction on cactus chains with 12, 16, and 20 cycle blocks and four mixed-sign objective coefficients. Each instance has a long middle chain separating two individually balanced objective groups. Eighteen comparisons cover random balanced nominations and both original and smoothed quadratic laws; the nine contraction constructions removed 72 blocks in total. The maximum objective difference was `1.15e-12`, the maximum surviving-edge flow difference was `3.1e-12`, and the maximum physical residual was `3.97e-12`. These checks test the nonlinear objective-preservation step directly; they do not establish asymptotic complexity or replace the proof.

The independent [exact adjoint checker](../code/potential_flow_mpd/check_reopened_weighted_faces_review.py) separately passed 180 rational positive-source paths, 3,598 horizontal-level checks, and 60 subdivided rank-two theta blocks. Its author and detailed audit are recorded in the first review linked above.
