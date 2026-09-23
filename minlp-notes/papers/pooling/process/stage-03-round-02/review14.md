# Stage 3, round 2 — independent review 14

Reviewed the entire `papers/pooling/sections/03-restricted-hardness.tex`, lines 1–1294, with SHA-256 `b8201a4bc6a61d4304f888649afe97bfc4aeefd9234d314a8cae3b805b3fad40`. I followed the round instructions and reviewer protocol. I did not consult other current-round reports or edit the manuscript.

No major or minor finding identified. In particular, I found no material omission among the 19 Stage 3 entries in the coverage inventory and no unsupported strengthening of their mathematical guarantees.

## Coverage comparison

I compared the relevant arguments in all seven canonical results and twelve notes. For promoted duplicates, I compared their text with the canonical result, including differences, rather than treating the promotion label as evidence.

| Original entry | Manuscript location and retained content |
|---|---|
| `results/pooling-one-quality-degree-two-hardness.md` | `s3:co`, `s3:local-degrees`, and the following paragraphs: occurrence splitting, private triangles, subdivision, both layer placements, omitted pool bounds, PARTITION specializations, and the degree-one LP boundary. |
| `results/pooling-all-degrees-two.md` | `s3:all-two-thm`: cleanup, constructive integral replacement, independent-set identity and recovery, factor-three approximation transfer, merged lax outputs, and exactly two degrees. |
| `results/pooling-two-pools-two-outputs-hardness.md` | `s3:matsui` through `s3:two-pools`: source separation, preprocessing, simplex embedding, objective identity, tree topology, single bypass, economics, normalization, capacity omission, exact demands, and the outlet-fraction NP certificate. |
| `results/pooling-one-pool-bypass-np-completeness.md` | `s3:copy-lemma`, `s3:row-copy`, `s3:base-bypass`: physical copying and conversion, port allocation, bounded-coefficient cone representation, source bounds, zero-intake case, objective identity, and fixed-quality NP membership. |
| `results/pooling-one-pool-upper-bounds-np-completeness.md` | `s3:cycles`, `s3:hoffman`, `s3:upper-only`: one upper quality, degree-two inputs, explicit error bound, radial repair, exact optimum shift, economic-objective repair, and polynomial coefficient encoding. |
| `results/pooling-constant-data-two-feed-np-completeness.md` | `s3:linear-circuits`, `s3:constant-thm`: rational-row representation, dyadic source normalization, two actual feeds, threshold circuit, fixed physical data, completion economics, and strong NP-completeness. |
| `results/pooling-five-exception-feasibility-hardness.md` | `s3:five-thm`: slack comparisons, grouping unused mates, supply-two and supply-four splitting, exact ordinary output qualities, five exceptions, redundant pool capacity, and feasibility NP membership. |
| `notes/pooling-positive-tolerance-extension.md` | `s3:tolerance`: cleanup loss, fixed rational gap constants, shifted positive qualities, and strong exact-optimization hardness without an integral-optimum or NP-membership claim. |
| `notes/pooling-positive-product-subfamily-approximation.md` | `s3:fptas`: the `ceil(1/epsilon)+1` LP bound, zero grid point, zero optimum, rational encoding, physical reconstruction, and supplied-representation requirement. |
| `notes/pooling-bypass-degree-four-hardness.md` | `s3:half`: four-full-port averaging, padded trees, signed leaves, root bounds, exact projection, and bounded flow capacities remain explicit. |
| `notes/pooling-bypass-degree-three-hardness.md` | `s3:half`: half-port formulas, mixed exact-quality chains, three-port averaging, complementary children, degrees, and dyadic root capacities remain explicit. |
| `notes/pooling-bypass-linear-universality.md` | `s3:linear-circuits`: the incomplete investigation is replaced by a complete binary-coefficient construction for rational rows on bounded signals. The manuscript does not assert the earlier unchecked scope. |
| `notes/pooling-single-upper-quality-cycles.md` | `s3:cycles`: separate full and half cycles, summed residuals, different positive conversion qualities, explicit coupling, and collector substitution. |
| `notes/pooling-upper-flow-only-penalty-hardness.md` | `s3:hoffman`, `s3:upper-only`: the distinct value-preserving penalty guarantee survives the later constant-data decision construction. |
| `notes/pooling-constant-data-two-feed-hardness.md` | Promoted argument retained in `s3:linear-circuits` and `s3:constant-thm`. |
| `notes/pooling-one-pool-bypass-copy-hardness.md` | Promoted argument retained in `s3:copy-lemma`, `s3:row-copy`, and `s3:base-bypass`. |
| `notes/pooling-two-pools-two-outputs-investigation.md` | Promoted argument retained in `s3:matsui` and `s3:two-pools`, with an independently justified large-parameter source estimate. |
| `notes/pooling-all-degrees-two-investigation.md` | `s3:weighted` retains the distinct integer-capacity and rainbow-matching extension. Allowing signed linked rewards is justified because cleanup preserves the two rewarded quantities separately. Optional physical arc capacities enter the retained mode bounds. The unused exploratory MAX-2-SAT route need not be reproduced. |
| `notes/pooling-fixed-exception-hardness-refinement.md` | Promotion pointer; its full result is retained at `s3:five-thm`. |

## Mathematical checks

I checked both directions of the orientation and pooling reductions, including equality at the threshold and the weaker recovery argument when pool capacities are omitted. The all-degree-two proof retains an algorithmic recovery from arbitrary feasible flows; integrality is proved only after fixing allowed modes. The weighted extension does not claim an integral feasible set or allow arbitrary independent arc costs. The positive-tolerance estimate and the K4 counterexample are consistent with the distinction between zero-tolerance integrality and positive-tolerance approximation hardness.

For the positive-product source, the largest fractional index isolates the positive diagonal contribution, and all other surviving terms have exponent at most `2k-1`. The stated determinant bound supplies the required separation at vertices; concavity extends it to the polytope. I checked the product identity, positivity, polynomial bit length, and the generator bounds used by both later normalizations. The two-pool reduction uses signs only on feasible mixtures, whereas the bypass and penalty constructions establish positive individual coefficients before using them.

The copy and circuit proofs allocate distinct physical port occurrences, preserve the signal ranges, and justify both projection directions. Full and half gadgets share a chain only in the exact-quality construction; the upper-only construction separates their cycles and explicitly couples them. In the penalty proof, the error bound is applied after cycle construction and source splitting, leaves integral contract rows unscaled, and repairs primary outlet feasibility separately. Rebuilding preserves homogeneous cone rows even though complementary and auxiliary flows need not scale. The separate argument for private-input rewards avoids assuming that their flows equal actual intakes before contracts are restored.

The signed-row circuit bound keeps every partial sum below two, including constants and negative coefficients. Contract completion removes positive lower bounds only after encoding the source threshold physically. Its bounded costs establish strong threshold hardness without implying an approximation gap. In the five-exception proof, copying is independent of private fillers, so grouping complementary ports is not circular; the final two conversion fillers and anchor account for all three exceptional inputs.

I checked the invoked certificate hypotheses against `s1:endpoint-or` and `s2:pooling-np`. The full many-pool NP-membership claims now explicitly impose upper output quality specifications only, with endpoint bounds in `{0,1}`. The fixed-pool claims use bounded flow fibers and a fixed number of quality or outlet-fraction parameters; they do not require rational physical witnesses or imply polynomial optimization.

## Source checks and verification limits

I read `literature/AGENTS.md` before consulting literature. I checked the local primary-source text for Chlebík–Chlebíková, Section 5(A), pages 25–26, and visually checked original PDF page 26, including the explicitly colored regular graph and preserved gap. I read the Matsui report's source construction and inspected original PDF page 3 to verify the scope and formula of its printed Theorem 2.1. The manuscript's small-parameter counterexample and repaired large-parameter proof agree with that source. I also checked the final Haugland discussion on printed page 214, the Haugland–Hendrix bypass question on printed page 607, and Baltean-Lugojan–Misener Remark 4.6 against their local primary texts.

This was a proof and coverage review. I did not rerun numerical network experiments or compilation; the round assigns compilation to root. I did not independently reconstruct the full external approximation-hardness proof, audit every bibliography field, or conduct an exhaustive novelty search. Historical PASS labels and finite experiments were not used as theorem evidence. No new finite mathematical check was needed to resolve a concrete concern.

**Verdict: no findings**, within the verification limits stated above.
