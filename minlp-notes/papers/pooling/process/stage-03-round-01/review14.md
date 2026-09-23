# Stage 3, round 1 — review 14

Reviewed `papers/pooling/sections/03-restricted-hardness.tex`, lines 1–1286, under `papers/pooling/process/reviewer-protocol.md`. The assigned focus was preservation of the canonical results and distinct Stage 3 restrictions recorded in `process/coverage.md`, together with proof correctness and available dependencies. I did not edit the manuscript, inspect other reviewers' reports, or delegate this review.

## Finding

### R14.1 — Include the physical arc bounds in the weighted replacement network

**Severity: minor.** Location: Proposition `s3:weighted`, lines 255–256 and its proof at lines 270–274.

The proposition expressly allows separate nonnegative integer arc capacities. The proof then describes the retained-mode flow problem using input/output capacities and “the pool capacity as an edge bound.” A retained mode uses two physical arcs, whose capacities must also bound this edge. As written, the replacement optimization can return a throughput that violates a physical arc capacity, so the assertion that it restores a feasible pooling point needs this additional bound.

For a concrete example, take one pool, its clean and dirty inputs, and its strict and lax outputs, with every node capacity equal to two. Give every physical arc capacity two except the clean intake arc, whose capacity is one. Set the linked mode rewards to `alpha = 1`, `beta = 0`. A clean-only throughput of one is feasible and optimal. After retaining the clean mode, the flow problem described using only node capacities and pool edge capacity two returns throughput two, which violates the clean intake bound.

**Repair:** explicitly bound the retained mode edge by the minimum of the pool capacity and its intake and outlet arc capacities, omitting an arc term when that capacity is not imposed. This minimum is integral, so the same capacitated bipartite flow integrality argument proves the proposition without changing its statement. The signed-reward and rainbow-matching claims do not need to be weakened.

This is a local omission in the proof of the optional arc-capacity extension; it does not refute the integral-mode theorem or affect the unit-capacity hardness constructions.

## Coverage and proof checks

The coverage comparison found no material missing Stage 3 result. In particular:

- **Local degree restrictions, lines 19–150:** checked occurrence splitting, the private triangle, subdivision in both directions, the two layer placements, threshold equality, both pool-capacity omissions, the PARTITION/private-layer specializations, and the degree-one LP boundary. The ordinary/strong distinction for the two-node specializations is retained.
- **All four degrees two, lines 152–282:** checked cleanup preserving `s` and `d`, fixed-mode integral replacement, the subdivided independent-set identity and constructive recovery, the factor-three approximation transfer, merged lax outputs, and exactly-two physical degrees. The weighted/rainbow extension is retained, including multigraph scope and the restriction to four linked costs. Allowing signed rewards is justified because cleanup preserves the two rewarded flows separately; it does not depend on reward positivity. The arc-bound omission above is the only finding in this extension.
- **Positive tolerance, lines 284–340:** checked the two cleanup losses, the aggregate strict-quality bound, the fixed rational tolerance and approximation constants, the affine shift, and the exact `K_4` feasible example. The manuscript correctly avoids claiming an endpoint NP certificate or integral optimality at positive tolerance.
- **Positive-product and two-pool family, lines 342–548:** checked the vertex denominator estimate, largest fractional index argument, corrected large-`p` separation, product expansion and positivity, polynomial coefficient length, LP preprocessing, simplex rows at both primary outputs, radial reconstruction, threshold direction, tree and single-bypass forms, economics, capacity omissions, and exact output-demand variant. The FPTAS retains its supplied-representation hypothesis, zero grid point, zero optimum case, LP count, rational bit bounds, and physical reconstruction. It is not promoted to arbitrary two-pool pooling.
- **Copy and degree refinements, lines 550–790:** checked full-port identities and conversion, signed homogeneous rows, source-specific coefficient/generator bounds, full-only four-port averages and padded trees, half-port formulas and mixed chains, signed children, dyadic root bounds, separate full/half closed cycles, positive conversion qualities, explicit cycle coupling, and collector splitting. The degree-four, degree-three, and input-degree-two milestones and their contract/quality distinctions remain available.
- **Exact penalty, lines 792–958:** checked the independent active-normal argument and singular-value bound, residual scaling with integral contract rows left unchanged, nonemptiness of the exact copy polytope, primary feasibility inequality, radial repair and its loss estimate, polynomial penalty encoding, exact optimum shift, and the separate production-cost objective repair. The theorem does not infer strong hardness from the large penalty.
- **Constant data, lines 961–1163:** checked least-significant-bit multiplier order, signed rational row normalization and bounded partial sums, addition-source splitting, the LP projection statement, dyadic source normalization, two actual feed qualities and quality mass, physical threshold circuit, final palette, completion threshold, bounded economics, and strong NP membership. The earlier incomplete general binary route has been replaced by a complete representation proof. No unsupported approximation gap is claimed.
- **Five exceptions, lines 1165–1264:** checked slack comparisons, requested-port/complement grouping without circular use of private supplies, supply-two and supply-four splitting, exact ordinary output qualities, the two conversion fillers plus anchor, the two primary output exceptions, removal of unnecessary designated signal ports, redundant pool bound, and retention of positive contracts. The source threshold is implemented physically and is not left as an external side constraint.

I compared these scopes with the seven canonical restricted-hardness result files and the distinct weighted, positive-tolerance, FPTAS, degree-four, degree-three, single-upper-quality-cycle, and linear-universality notes identified in `coverage.md`. Promoted duplicate histories were not treated as additional independent theorems or as evidence of correctness.

## Dependencies and limits

The invoked endpoint certificate is present in Stage 1 at `s1:endpoint-or`, with the required input-quality box, endpoint upper specifications, and integral-flow certificate. Stage 2's `s2:pooling-np` explicitly covers bounded pool-times-quality and pool-times-output counts, arbitrary bypasses and contracts, and finite flow upper bounds. Its basis-index verifier and determinant bit-complexity argument are available. These hypotheses cover the Stage 3 NP-membership uses, including the unbounded-attribute two-pool case.

I read `literature/AGENTS.md` before source inspection. I checked the local Matsui report's relevant source proof and compared its printed Theorem 2.1 and proof directly with original PDF pages 3–4; the manuscript's counterexample and restriction to the repaired large-`p` argument are consistent. I checked the Chlebík–Chlebíková author manuscript's explicit edge-three-colored cubic construction in Section 5(A), including original PDF page 26. The bibliography distinguishes those accessible versions from journal pagination.

I did not independently reprove the source PCP approximation-gap theorem, repeat an external novelty search, audit every historical-source comparison at lines 1266–1286 against original publications, or rerun the repository's numerical network compilers. Those are limits of this review, not additional findings. Finite numerical tests and prior PASS labels were not used to establish any theorem.

**Verdict: minor findings only.** One explicit capacity bound should be added to the weighted replacement proof. No major mathematical or coverage defect was identified within the checked scope.
