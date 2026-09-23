# Independent review: weighted nomination-face reduction

Date: 2026-09-06. Reviewer: independent subagent `review_weighted_faces`.

## Verdict and scope

I independently checked the proof in [the nomination-face note](potential-flow-reopened-weighted-face-reduction.md). I found no mathematical blocker in the structural claim: with fixed positive edge laws, objective support at most `p`, and block cycle rank at most `r`, a global optimum is contained in a constructible `n^{O(rp)}` family of reduced nomination faces with `O(rp)` free coordinates.

The statement concerns a balanced nomination box without scenario-filtering operating constraints. Its faces belong to the reduced problem, whose nomination aggregation must be retained when reconstructing a solution. It does not assert that a corresponding original-box face has only `O(rp)` free original coordinates. The pointwise family is independent of resistances, so its existence conclusion also applies to compact independent positive resistance uncertainty. It supplies no algorithm for optimizing the resulting variable-resistance functions.

This review establishes neither literature priority nor a general bounded-block-rank accuracy-bit algorithm. Composition with the separate affine-parameter optimizer is valid on cacti with fixed positive quadratic or asymmetric quadratic laws, conditional on that optimizer's independent validation. In particular, the face proof does not resolve sums of general block algebraic functions.

## Structural proof checks

### Objective-preserving reductions

For a pendant support-free subnetwork, its external influence is exactly its aggregate nomination at the attachment. Every aggregate in the summed interval can be split into original intervals, and the internal passive problem has a unique flow state for the resulting effective injections. Only the attachment contributes to the objective. Thus pruning preserves both attainable objective values and feasibility.

For zero-source block contraction, deleting block edges separates components `G_v` rooted at the block vertices. The block-cut tree guarantees that these components are disjoint. When every `sum_(u in G_v) c_u` vanishes, the contribution of each component is invariant under a constant shift of its potential. Consequently the relative root potentials supplied by the removed block have no effect on the objective.

Contraction is valid in both directions. Starting from an original state, shift each component to a common root potential and sum its root nominations. Starting from a reduced state, split the merged root nomination into the original root intervals. The external edge flows are already determined. The required block injections then sum to zero by conservation at the merged vertex; solve the block for those injections and translate each external component to the recovered root potential. This preserves all original box constraints and exactly preserves the objective. The deleted block imposes no restriction on which balanced root injections can be realized, since all positive quadratic laws are unbounded and strictly increasing.

Deleting or contracting one block changes no surviving block's induced objective-source sums: the objective coefficients on each side are simply aggregated. It also does not raise any surviving block's cycle rank. Each contraction reduces graph size, so the iterative reduction terminates in polynomial time. Summing rational intervals and splitting them greedily preserve polynomial encoding length. Mixed signs and cancellation in `c` are allowed throughout this argument.

### Support skeleton and coarse faces

The incidence graph using all vertex nodes and block nodes is a tree. Its minimal support-spanning subtree has support vertices as leaves, so its branching degree sum is `O(p)`. Support vertices of degree two contribute at most `2p` additional incidences. Therefore the number of special blocks and the total number of their retained ports are `O(p)`, even if the original graph has many blocks or vertices in a block.

After removing the special block nodes, each remaining component is an ordinary chain with two-terminal blocks. The effective adjoint source across one chain is constant, because its intervening vertices and pruned branches have no objective coefficients. It is nonzero after the zero-source contractions. This is the exact hypothesis needed to prevent a long chain of constant adjoint values.

With positive smoothing, the derivative of every law is positive, and the potential objective has electrical adjoint gradient. In a biconnected block, every internal vertex has electrical potential strictly between two distinct prescribed terminal values: equality at an extremum would propagate by the weighted maximum principle and contradict two-vertex-connectivity. Bridges have no interiors. Thus chain port values are strictly ordered, and successive blocks' open adjoint ranges are disjoint.

The balanced-box KKT rule uses one scalar threshold. It holds even if the balanced box has no relative interior beyond its forced coordinates, because the feasible set is polyhedral. Equality at a shared articulation causes no issue: choose an adjacent block and treat vertices in the union of selected and special blocks as free. Outside this union, the threshold determines the interval endpoint on each side of the selected block. Endpoints also belonging to special blocks remain free. A threshold outside the chain range gives one of the two constant endpoint patterns.

Selecting at most one block on each of `O(p)` chains gives `n^{O(p)}` coarse faces. This enumeration only needs graph structure, objective side sums, and interval endpoints; it does not need the actual adjoint values or resistances.

### Second perturbation and coordinate count

In each chosen nonbridge block, internal degree at least three marks at most `2r_H-2` vertices. Retained ports contribute `O(p)` marks in total. Suppressing the other degree-two vertices leaves `r_H+k_H-1` paths when the block has `k_H` marked vertices. Every retained block has at least two retained ports; bridge endpoints are handled separately. There are therefore `O(rp)` marked vertices and paths.

Every unmarked path-interior vertex belongs to only that retained block and has original objective coefficient zero. Thus perturbing exactly those coordinates by positive `delta`, compensated at a marked reference vertex, gives adjoint source exactly `delta` at each interior vertex. The reference term preserves zero total objective coefficient. The coarse face must be fixed before this perturbation; otherwise the first-stage zero-source chain argument would no longer apply.

For a consistently oriented path, currents obey `j_i-j_(i-1)=delta>0`. Positive edge conductances imply that the adjoint values first increase and then decrease, with at most one zero increment. A horizontal level therefore contains at most two interior vertices; when adjacent, they form the maximum plateau. The KKT pattern is lower endpoints, up to one equality pivot, upper endpoints, up to one equality pivot, lower endpoints. This includes empty sections, entirely upper or lower paths, and a two-vertex maximum plateau.

Enumerating the path breakpoints has polynomial cost per path. Marked coordinates and at most two equality coordinates per path remain free. Combining `O(rp)` paths with the coarse enumeration gives the claimed `n^{O(rp)}` family and `O(rp)` free-coordinate bound. Empty faces can be removed by rational linear feasibility checks; overlap between faces is harmless.

### Limits and reconstruction

The existence proof correctly uses two limits. First take smoothed global maximizers and extract a subsequence in one fixed coarse face. Then maximize the perturbed smoothed objective on that face and extract a subsequence in one fixed fine face. Both families are finite and their faces are closed.

For completeness, joint continuity of the normalized passive state in nominations and smoothing can be proved by taking a fixed spanning-tree right inverse of the incidence matrix. Small nomination changes admit small feasible tree-flow corrections. These corrections, compact flow bounds, and strict convexity show that every limit of minimizing flows is the unique minimizer for the limiting nominations and law. Potential continuity follows by summing edge drops along fixed paths. Compactness then gives the uniform convergence used in both stages. The potential perturbation is uniformly bounded by its coefficient times the number of perturbed vertices and a uniform normalized-potential bound.

Each resulting nonempty face has a fixed number of free coordinates and only rational affine balance constraints. Eliminating one free coordinate, when needed, gives a compact rational polytope of fixed dimension. Solving each face and taking the best value is polynomial for fixed `r,p` whenever the local-function optimizer has the asserted fixed-dimensional complexity. The rational disaggregation map then restores feasible original nominations without changing the achieved objective.

The degenerate objective is harmless: with `sum c=0`, support size one implies `c=0`; a nonzero objective has at least two support vertices.

## Independent exact checks

I wrote and ran [the independent adjoint check](../code/potential_flow_mpd/check_reopened_weighted_faces_review.py). It uses Python rational arithmetic throughout and passed:

- 180 paths with positive interior adjoint sources, unequal positive conductances, and arbitrary rational terminal potentials;
- 3,598 horizontal-level checks of the two-equality-coordinate and contiguous upper-region properties;
- 60 subdivided theta blocks of cycle rank two, checking strict interior terminal bounds and positive terminal conductance.

These finite checks exercise the two electrical mechanisms independently of the author's nonlinear experiments. They do not replace the proof, test every graph, or implement global face enumeration and optimization.

## Required boundaries for a paper statement

Retain the distinctions between reduced and original nomination faces, fixed and variable resistance algorithms, and cactus and general bounded-rank blocks. Do not import exact capacity constraints into this face lemma: both objective-preserving contraction and the box-only KKT rule can fail under those additional constraints. The affine-parameter cactus theorem may separately admit local exact capacity constraints, but that extension does not compose with this unrestricted-box face reduction without new arguments.
