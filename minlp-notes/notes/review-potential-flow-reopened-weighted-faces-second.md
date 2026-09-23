# Independent second audit of the weighted nomination-face reduction

Date: 2026-09-06. Reviewer: `flow_weighted`, independently assigned by the root agent after the structural proof was drafted. Verdict: PASS for the fixed-law structural statement, including fixed asymmetric quadratic laws. The claimed structural extension to compact resistance uncertainty also passes as an existence statement; it is not an optimization algorithm for resistance uncertainty.

Reviewed source: [weighted face reduction](potential-flow-reopened-weighted-face-reduction.md). This review is independent of that note's author. The reviewer authored the separate affine-load approximation ingredient, so this is not an independent audit of that approximation theorem.

## Contraction and reconstruction

The zero-block contraction is valid. Removing a block's edges in a block-cut decomposition separates its different vertices into distinct components. Each component's internal flows and relative potentials are determined by its nominations away from its root. The objective contribution that changes under a root-potential translation is exactly the component's induced coefficient sum `gamma_v`; it vanishes by hypothesis. Aggregating the block vertices' nomination intervals therefore preserves the reduced external state and objective. Conversely, splitting the aggregate nomination within those intervals yields balanced effective block injections, and the passive block state supplies the translations needed to lift the reduced state. There is no hidden capacity constraint or potential bound in this operation.

The contraction does not merge two vertices of another surviving block: that would create a cycle in the block-incidence tree. Thus it preserves surviving block topology and their rank bounds. It cannot increase objective support. Objective-free pendant pruning is the corresponding one-attachment special case. Rational interval-sum disaggregation has polynomial encoding length.

## Skeleton and first-stage faces

The minimal support-spanning incidence tree has only support leaves, at most `p-2` branching nodes, and total branching degree `O(p)`. Consequently the marked-node incidences, special blocks, their port counts, and remaining ordinary chains are all `O(p)`. Physical nonsupport vertices inside a retained block must remain; the note explicitly preserves them and their nomination intervals.

The induced adjoint current across an ordinary chain is the fixed sum of objective coefficients on one side. It is nonzero because every zero-induced-source block has already been contracted. With positive differential resistances, the two-terminal maximum principle gives strictly nested terminal order and disjoint open interior ranges along the chain. A single box-and-balance KKT multiplier can therefore intersect only one block's open range, or one shared articulation level. Leaving that block and its shared endpoints free covers both cases. Known current signs determine the endpoint pattern outside the selected block. Vertices shared with a special block remain free, avoiding incompatible endpoint assignments.

Enumeration of one selected block per ordinary chain, or all-upper/all-lower alternatives, has polynomial size for fixed `p`; the family is independent of smoothing and resistance. Compactness and uniform convergence permit a fixed closed face subsequence, so no limiting zero flow invalidates the conclusion.

## Second-stage faces and perturbation

Fixing the coarse face before adding the positive-source perturbation is essential and is done correctly. Perturbation on all vertices from the start would destroy the zero-source ordinary-chain argument. On the fixed coarse face, marking retained ports, objective support, and block-degree-at-least-three vertices leaves only degree-two paths without off-block adjoint sources. Their number and the total marked count are `O(rp)`, by the standard block rank degree identity.

Each perturbed interior adjoint source is exactly positive `delta`, so path currents strictly increase and potential values first increase then decrease. A level intersects at most two interior vertices, including the possible two-vertex plateau. Applying the balanced-box normal cone inside the coarse face gives at most two free nominations per path. Shared vertices belong to the marked set and are counted once. The graph-only family of subfaces is closed and has `n^{O(rp)}` choices. A second compactness limit preserves an original maximizer on one subface.

The smoothing bounds hold uniformly over the whole compact balanced nomination box: passive flows are bounded by total possible positive injection, and normalized potentials by path sums of bounded edge laws. Asymmetric coefficients preserve strict monotonicity and the smoothed positive differential resistance. The perturbation is uniformly small on the bounded state set.

## Composition and limits

After reduction, each final face is a compact rational polytope in `O(rp)` free coordinates. This is exactly the input form required by the separately reviewed affine-load cactus optimizer. For fixed objective support on a cactus with fixed positive rational asymmetric quadratic laws, the two ingredients therefore yield polynomial additive optimization in input and accuracy bits, rational feasible nomination output, and unbounded total cycle rank.

Neither proof gives joint weighted resistance optimization. The structural face family remains valid after selecting the resistance vector of a joint maximizer, but evaluating the objective over those faces with variable resistances needs another algorithm. General fixed-rank-per-block networks have the same unresolved local-function approximation step. Operating constraints invalidate pruning and zero-block contraction, so they are outside the unrestricted-box composition even though the affine-load optimizer has a separate local-capacity corollary.

No blocking error or missing hypothesis was found in this structural audit. This is internal independent review, not a literature novelty certification or external peer review.
