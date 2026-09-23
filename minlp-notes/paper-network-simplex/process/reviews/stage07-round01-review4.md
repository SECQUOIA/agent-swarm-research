# Stage 7, round 1 — independent review 4

**Verdict: no major or minor issues identified in this stage.** The new framing matches the accepted results and qualified computational evidence. The integral-flow corollary is correct, appropriately attributed as classical, and does not overstate the size of an integral decomposition.

## Scope and independence

I read the complete Stage 7 source diff and the frozen abstract, introduction, structural scope table, new corollary and proof, literature additions, graph figure, conclusion, computational prose changes, README and coverage map. I compared the changed computation section with the accepted Stage 6 snapshot and checked the summarized results against their actual theorem statements and evidence. I read the stage author and validation records, but no other current-round review. I edited only my report and private verification directory, and used no subagents.

## Findings

1. **No actionable findings.** This is acceptance of the assigned integration stage, not a substitute for the required subsequent whole-manuscript review.

## Assessment

The integral-flow proof correctly uses the fractional-arc subgraph. A loop permits a one-coordinate perturbation. Otherwise a vertex cannot be incident to exactly one fractional arc when its balance and the other arc values are integral. A cycle therefore exists; its signed circulation admits perturbations in both directions because its arcs are strictly inside their integral bounds. This excludes every nonintegral vertex. Boundedness permits integral-vertex refinement of each positive-weight normalized state flow. At a fixed simplex vertex the retained products are linear, which proves the stated hull equality. Empty domains, parallel arcs, loops, zero weights and the case `m=0` do not invalidate the argument. The following paragraph correctly distinguishes this equality from an integral `m+1` decomposition bound or integrality of fractional coordinate sections.

The abstract, contributions and scope table retain the necessary boundaries: the residual-coordinate count belongs to the supplied formulation, the minimum completion claim concerns individual products on the ambient circulation space, unit coefficients concern the specified flow/product row scaling, and bounded-rank recovery has a larger parameter factor than separation. The three-observed-label flat-chain threshold is not extended to arbitrary nested series–parallel networks. The coefficient obstructions are not misrepresented as separation hardness or large extension complexity. The diagram correctly depicts the directed unit-flow topology and common statewise branch profile.

The new numerical summary matches the accepted all-labels-observed control: 7,215 full/global state-flow variables, 495 initial-compression variables and 367 after observed elimination, with about 30 versus 10 ms median totals for full versus initial compression. The new conclusion and README retain negative findings, synthetic/shared-host scope and exact-versus-numerical certificate distinctions. The updated provenance describes the separate measurement sets without changing their inputs or values.

The added literature comparisons are supported by primary sources. [Fiorini's manuscript](https://samuel.fiorini.web.ulb.be/papers/howto_rev.pdf) supports the stated general facet transfer, and its [publisher record](https://www.sciencedirect.com/science/article/pii/S1572528606000168) agrees with the new bibliography. The [Hoffman–Kruskal reprint](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/kruskalhoffman.pdf) confirms the TU integrality implication and original publication metadata. I also read KD Section 4.2 in the repository's primary full text; the service-transportation motivation and the stated common-simplex specialization are accurately distinguished.

## Checks actually performed

Private evidence is in `verification/stage07-review4/`.

- Wrote a new exact refinement check using fractional-support null directions and recursive two-sided rounding, independently of the author's vertex-enumeration checker and production oracles. Across **24 multigraphs**, it exactly refined **240 normalized flows into 2,462 integral terms** and verified **96 complete sparse hull mixtures** with zero through three explicit labels. Each term satisfies the original balances and capacities; all mixture weights and original flow/simplex/product coordinates reconstruct exactly. The graphs include loops, parallel/reverse arcs, zero capacity and isolated vertices. All checks passed. This is finite evidence; the general corollary rests on the proof assessed above.
- Independently verified **all 88 Stage 7 manifest hashes** and frozen/current manuscript source agreement. Recomputed **all 483 timing summaries** from the retained raw records and separately checked the new introductory model counts and rounded timings.
- Read the completed source coverage map and historical supersession pointers. Checked that the accepted computation formulas and measurements are unchanged; the changed prose adds attribution and clarifies provenance.
- Built the frozen manuscript in a private source tree: **48 pages**, with no final warning, undefined reference/citation, or overfull/underfull diagnostic. Visually inspected the private title/abstract page, scope table page and graph-diagram page. The diagram and table are legible and their locators resolve.

## Limits

I did not rerun the official timing study or infer performance beyond its reported synthetic cases. Production algorithms are unchanged in this stage, so I relied on the accepted code audits and current hash verification rather than duplicating their full experiments. I checked the new citations and their claims, not an exhaustive new priority search. The accepted theorem proofs were consulted at the interfaces used by the new framing; the forthcoming whole-manuscript round must still assess all sections together.
