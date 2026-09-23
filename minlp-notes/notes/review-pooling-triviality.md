# Independent audit: polynomial pooling triviality

Date: 2026-09-04. Reviewer: independent `fbbt` agent. Target: [pooling triviality theorem](../results/pooling-triviality-polynomial.md). A separate reviewer wrote [a second audit](review-pooling-triviality-second.md).

**Verdict: Theorems 1–3, the destination decomposition, single-output LP reduction, shortest-path sign test, small-support witness, conic-hull description, and output-count approximation pass independent mathematical review under the stated assumptions.** No proof defect was found. This audit reconstructed the central argument before reading the draft. It does not certify literature priority.

**Priority update:** the destination-disaggregation machinery is already explicit in Boland–Kalinowski–Rigterink; see the final section. The verified sign and cone conclusions should be presented as explicit consequences of established formulations, not as a new decomposition method.

## Source-model check

The [Gupte–Ahmed–Dey–Cheon primary manuscript](https://www.pure.ed.ac.uk/ws/files/136877755/4883.pdf), Section 2, specifies an acyclic directed graph allowing pool-to-pool arcs. Inputs are sources and outputs are sinks. Equations (1)–(3) impose conservation, nonnegativity, and node/arc upper capacities. Equations (4a) and (5) impose linear mixing and output-quality bounds. There are no positive lower throughput requirements or prescribed intermediate quality intervals. Observation 2.3 uses zero flow to obtain `z*<=0`; Remark 2.2, physical PDF page 6, printed page 5, explicitly asks whether testing `z*=0` is polynomial. The candidate addresses that formal model. Introductory references to meeting demand do not override the upper-bound-only equations.

## Destination decomposition

Fix a feasible physical flow `y` and its pool qualities. Write `F_v` for pool throughput and `h_j(v)` for the backward destination fractions in the draft.

1. The recursion is well-defined on the DAG. At an inactive pool, nonnegativity and conservation make every incident flow zero. Its destination fractions therefore cannot affect a nonzero term.
2. Every active pool has an active successor. Following successors must terminate at an output. Reverse induction gives `sum_j h_j(v)=1` at every active pool. The draft includes this induction rather than relying only on reachability.
3. The component `y^j_uv=y_uv h_j(v)` uses the fraction at the **head**. Consequently all incoming arcs at a given pool are multiplied by one common factor. Tail weighting would generally fail to preserve the mixture.
4. Incoming component throughput is `h_j(v)F_v`, and the recursion makes outgoing component throughput equal to it. Both vanish at inactive pools.
5. Incoming specification mass is multiplied by the same factor. Retaining the original pool quality therefore satisfies every tracking equation, including when `h_j(v)=0`. Outgoing arcs still share one quality vector.
6. Output `j` retains its entire original incoming arc vector; other outputs receive zero. Hence quality feasibility is preserved without assuming an arbitrary submixture satisfies the original quality limits.
7. Coordinatewise domination `0<=y^j<=y` preserves every arc and node upper capacity. No sign assumption on costs is used.
8. The components sum to `y`, so linear costs add and a negative total cost has a negative component.

The checks cover arbitrarily many pool layers, reconvergence, direct input-output arcs, signed qualities, and signed costs. Starting from a physical flow matters: an arbitrary commodity relaxation may permit demixing and need not preserve original pool qualities.

## Exact single-output LP

For any physical flow serving only `j`, sum all pool specification balances. Every internal quality-flow term cancels. The remaining terms equate the specification mass reaching `j` with `sum_i lambda_ik s_i`, including direct deliveries. This algebra does not require nonnegative specifications.

Conversely, take an LP-feasible ordinary flow. Topological weighted averaging defines each active pool quality; any finite vector works at inactive pools. This constructs a physical flow with the same arc vector and cost. Summing the constructed balances again proves that the LP's aggregate specification inequalities enforce the output's actual qualities. Therefore this LP is exactly the flow projection of the single-output physical restriction.

If `t_j=0`, positive flow anywhere could be followed to an output with positive inflow, a contradiction. Acyclicity excludes isolated circulations. This verifies the zero-throughput case without dividing by zero.

## Objective signs and rational complexity

Single-output feasible sets are subsets of the original feasible set and contain zero; hence `z*<=z_j<=0`. A negative feasible total flow yields a negative destination component and therefore a negative LP optimum. Conversely, a negative LP flow reconstructs a physical flow. This proves the zero-optimality equivalence.

For `m=|J|>=1`, decomposition of an optimum and `z_j<=c^T y^j` give `min_j z_j<=z*/m`. Thus `z*<=z_best<=z*/m<=0` has the correct minimization signs. After negation, the method is an `m`-approximation for nonnegative profit. Empty output sets force zero flow and are correctly separated.

The later strengthened bound using the coupled commodity LP also passes: `z_rel<=z*<=z_best<=z_rel/m<=0`. An optimal relaxation solution consists of `m` single-output component flows whose sum satisfies all original capacities. Each component is dominated by the sum, hence satisfies those upper capacities individually, and is physically realizable by the single-output lemma. Some component costs at most the average `z_rel/m`, and its single-output LP can only improve that cost. This is a bound from the particular stated commodity relaxation, not an automatic assertion about an arbitrary weaker pooling LP. It also proves that this relaxation detects zero-optimality exactly.

The LPs are rational, bounded in arc flows, and polynomial in size. Exact LP sign comparison is polynomial; a floating-point tolerance does not certify zero. The output qualities also have polynomial encoding length. Clear a common flow denominator; path expansions of concentrations have denominators dividing a common input-quality denominator times the product of positive integer pool throughputs over ancestors. A DAG path visits each pool at most once, so this product has polynomial bit length.

Finite capacities and convex-combination bounds on active qualities justify attainment. Inactive qualities can be assigned within a fixed bounded box, giving an equivalent compact feasible representation.

## Shortest-path test and sparse witness

After deleting zero-capacity arcs and nodes, positive capacity magnitudes do not affect the existence of a negative direction. Decomposing a single-output conserved flow into source-output paths shows that its normalized cost is at least the mixture of shortest-path costs for its source proportions. Its aggregate specification constraints give a feasible blending simplex point.

Conversely, a negative blending mixture can be routed along one shortest path per used input. Common positive scaling makes every arc and node capacity feasible; single-output reconstruction produces valid mixing, even when the chosen paths merge and later split. Quality ratios and objective sign are unchanged. Negative arc costs are harmless on a DAG. Infeasible simplices and unreachable outputs correctly have no profitable witness.

An optimal blending vertex uses at most `K+1` inputs. On support size `s`, normalization and active quality rows have rank at most `K+1`; if `s>K+1`, a nonzero supported null direction preserves active rows. Sufficiently small perturbations in both directions preserve inactive inequalities and positivity, contradicting extremality. Two simultaneously active sides of an equality quality interval count as the same row direction. The claim also works for `K=0`. Selected shortest paths may pass through arbitrarily many pools; the draft correctly does not confuse support size with network size.

## Polyhedral conic hull

Each `C_j` in Theorem 3 is a polyhedral convex cone and an exact single-output physical set. The destination decomposition places every uncapacitated physical flow in `sum_j C_j`; conversely every `C_j` lies in the physical set `S`. Since the sum is a convex cone, these inclusions establish `cone(S)=sum_j C_j`. The draft explicitly defines `cone` using finite nonnegative combinations, avoiding ambiguity with mere positive scaling. Because `S` itself is closed under scaling, `conv(S)=cone(S)`.

On the positive-capacity support, every finite physical flow can be scaled into the original capacity region. Thus `cone(P)=cone(S)`, and a polynomial-size linear projection describes every homogeneous valid linear inequality. The cost-vector dual-cone sign convention `c^T y>=0` is correct for minimization and zero-optimality. Polyhedrality implies closedness here; it is not assumed for an arbitrary conic hull.

The warning about the capacitated convex hull has a concrete witness. Use two inputs with qualities 0 and 1, one pool, and two outputs requiring exactly 0 and exactly 1. Include only the four input-pool/pool-output arcs. Give each input, output, and arc capacity 1, and the pool capacity 2. Any physical nonzero flow can serve only one output, so every point of `conv(P)` has total output at most 1. The uncapacitated conic hull contains the sum of the two unit single-output flows. That sum satisfies all original capacities and has total output 2. Therefore intersecting the conic hull with capacities is strictly weaker than `conv(P)`, already on five nodes.

## Independent exact-arithmetic check

A Python/Fraction experiment independently checked 250 random feasible DAG flows. Each graph had three inputs, five ordered pools, three outputs, and all allowed forward arcs. Zero random weights produced inactive arcs and pools; input and inactive-pool qualities included negative values. Exact checks covered component summation, conservation, unchanged-quality tracking, designated-output inflow preservation, zero other-output inflow, capacity domination, and signed-cost additivity. All 250 cases passed. This supports the algebra and does not replace it.

## Prior-art boundary

[Dey–Gupte's open manuscript](https://optimization-online.org/wp-content/uploads/2013/04/3849.pdf), Section 1.1, explicitly permits only input-pool, input-output, and pool-output arcs. Theorem 2 gives an output-count approximation using single-output restrictions; Section 6 explicitly identifies the single-output polynomial case. Standard-pooling triviality therefore already follows from that work.

The author subsequently identified closer generalized-network prior art, which this reviewer then inspected independently: Boland, Kalinowski, and Rigterink, [*New multi-commodity flow formulations for the pooling problem*](https://optimization-online.org/wp-content/uploads/2015/06/4959.pdf), Section 4.2.1. Equations (18)–(21) explicitly give output-commodity conservation, aggregate output quality, head-fraction bilinear consistency, and summation to physical arc flow. The manuscript's Section 3 permits pool-to-pool arcs. Thus generalized destination disaggregation and aggregate source-quality equations are established. Correctness of the new notes is unaffected, but the novelty interpretation must be weaker: they make sign, small-witness, and conic-hull consequences explicit. This audit did not establish whether those consequences were stated previously elsewhere, and did not exhaust later citations.
