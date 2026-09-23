# Stage 1, round 2, reviewer 04

Assigned manuscript: `papers/pooling/sections/01-foundations.tex`, read in full (lines 1–685). Emphasis: shortest paths, sparse witnesses, signed costs, scaling, and polynomial encoding bounds. I followed `papers/pooling/process/reviewer-protocol.md`, did not inspect other reviewers' reports, and did not edit the manuscript.

## Findings

No major or minor findings identified. No correction is requested.

## Mathematical checks

- **Model and certificates (lines 1–179).** The homogeneous product inequalities handle zero deliveries correctly, including exact quality contracts. The acyclic quality-box argument bounds a representative lift without asserting that every assignment to an inactive pool is bounded. Affine-rank substitution preserves all original product inequalities and uses polynomial-size rational elimination. The distinction between a real feasibility formulation and an NP certificate is maintained.

- **Physical rank-one block (lines 181–205).** The margin factorization and the zero-throughput convention are valid. The objective restriction to coefficients of the form `a_i+b_j` correctly prevents transferring arbitrary matrix-objective hardness to physical feed/outlet costs.

- **Destination decomposition and single-product LP (lines 207–293).** Multiplication by the destination fraction at the head of each arc preserves both incoming quality proportions and conservation at pools. Coordinatewise domination preserves all the permitted upper capacities because the subsection excludes positive lower bounds. Topological reconstruction proves physical feasibility for the complete LP arc flow, rather than merely constructing a flow with the same aggregate cost. The signs in the approximation and relaxation inequalities are correct for cost minimization.

- **Shortest-path equivalence (lines 295–322).** A negative acyclic single-product flow has positive delivery. Ordinary path decomposition therefore gives normalized input weights, and replacing each route cost by its input–product shortest-path cost can only decrease the objective, including with signed arc costs. Conversely, routing the input mixture on selected shortest paths gives the required aggregate quality mass. Mixing at shared pools is supplied by the single-product projection lemma; the paths do not have to preserve separate input identities physically. Zero-capacity deletion is essential and is explicitly present.

- **Sparse witness and bit size (lines 324–343).** On a support of size greater than `K+1`, normalization and the active quality rows admit a nonzero two-sided feasible perturbation. Lower and upper bounds on the same attribute do not double the rank. A compact rational mixture LP has a rational optimal vertex with determinant bounds polynomial in input length. Each selected acyclic path is simple and has polynomial rational cost length. Summing its weighted arc contributions gives polynomial-size rational loads for every arc and node capacity. The displayed minimum of positive capacity-to-load ratios is strictly positive and polynomially encoded. It preserves quality ratios and negative cost. Reconstruction can be treated as one triangular rational system, so it does not rely on a potentially misleading sequence of independent denominator-size estimates.

- **Conic hull (lines 345–389).** Nonnegative scaling and destination decomposition justify the equality with the Minkowski sum without assuming closure of a conic hull. The linear projection supplies polyhedrality and closure. Scaling back into the capacitated set uses only positive retained capacities. The two-pure-product example correctly separates the capacitated convex hull from reimposition of capacities on the uncapacitated convex hull.

- **Cycles (lines 391–526).** In the positive support, a component without external inflow also has no external outflow by conservation. All other component systems are invertible substochastic systems; the backward orientation used for quality reconstruction is consistent with incoming quality balances. Solving the complete rational system gives a polynomial encoding bound even near singularity. Negative cycles supply feasible isolated circulations under the stated algebraic semantics. In their absence, removing cycles cannot increase a single-product flow's cost, and preserves source withdrawals and product delivery. The union of selected simple shortest paths may contain cycles, but the cyclic reconstruction lemma covers this. Merging isolated circulation into one product component also establishes the claimed product-count approximation. The quality box containing zero supplies attainment, including when there are no inputs.

- **Facial and endpoint specifications (lines 528–685).** The support-compatibility characterization yields network branches with integral vertices for integer bounds. The nonfacial converse uses a strictly negative mixture while every integral unit-capacity flow has cost zero. Recognition by forbidden-input weight is an equivalence. The face enumeration bound follows from fixed affine dimension and bases of active facet normals; it need not be tight. The stated check for omitted arcs with positive lower bounds preserves contracts. Endpoint disjunctions, finite-throughput big-M rows, and the rational branch-vertex threshold certificate are consistent with these arguments.

## Source cross-check and limits

I checked the local primary text `/tmp/pooling-paper-sources/dey-gupte-article.txt`, Section 4 and Theorem 2: it expressly derives the output-count approximation through a solution serving one output, supporting the manuscript's attribution. I also read the foundation source inventory to identify the intended source versions. The mathematical proofs above were checked independently; I did not treat the inventory as proof evidence.

I did not compare every cited claim against the published versions of the Boland, Gupte, or rank-one papers, perform a publication-priority search, inspect later manuscript stages, or run numerical experiments. Those are limits of this review, not identified defects. This review does not establish exhaustive correctness or predict external acceptance.

**Verdict: no findings.**
