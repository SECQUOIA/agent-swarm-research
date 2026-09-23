# Stage 2 round 1 adjudication

Root read all five independent reports in full, including proof coverage and evidence limits. Four report no mandatory corrections; review 3 identifies one editorial issue. No reviewer identifies a major defect, and root's independent full proof and final-diff examination identifies none. The computations are supplementary checks, not exact certificates for numerical LP solves or proof of general correctness.

## Accepted corrections (all minor)

1. **R3 M1; R1 O1; R5 O2:** Replace the unexplained degree transition before `s3:five-thm` with an explicit forward comparison to `s5:arbitrary-exceptions`. The positive theorem bounds bypass degree by two; the hard construction permits three bypass inlets at ordinary outputs. Total physical degree and bypass degree must be distinguished. Keep exact ordinary contracts, fixed exceptions, and redundant common pool bounds visible. This is a wording repair; the preceding construction already has total output degree three.
2. **R2 optional:** Rename the positive-tolerance proposition to describe positive strict-output concentration bounds, or explicitly define that usage. Do not suggest robustness to arbitrary numerical residuals.
3. **R3 O1:** State the ordinary rational-flow bit-model convention directly for approximation recovery. If useful, use the equivalent division-free test `d_v <= eta(a_v+d_v)` with zero throughput handled separately. No broader compressed-representation algorithm is needed.
4. **R3 O3:** Identify the two matching edges associated with a pool explicitly as clean-input/strict-output and dirty-input/lax-output, with the pool as common color; keep the two-disjoint-edges-per-color restriction.
5. **R4 O1:** Cite Haugland 2016 Proposition 3 at the degree-one LP paragraph. Root checked the primary text; this is established positive-side work. Retain the short self-contained argument.
6. **R4 O2:** Add a compact final external-node contract inventory to the five-exception proof. Make exact versus variable supply/demand/quality and degree counts inspectable without redoing all port bookkeeping. Retain the exclusion of unnecessary designated reporting ports.
7. **R5 O3:** State that the circuit lemma represents rational linear equations and weak inequalities. All applications already meet this condition.
8. **R3 O2; R5 O1:** Add a compact native diagram for full and half copy gadgets and their zero-port connections. Prioritize clear physical arcs, supplies/demands, qualities, complementary port values, and distinct occurrences. The prose and inventory can carry coupling/splitting details; avoid an oversized schematic. This supports readability of the central new physical construction.
9. **Root source finding:** Add a concise comparison to Haugland, *Pooling Problems with Single-Flow Constraints*, INOC 2019, pp.95–100, DOI 10.5441/002/inoc.2019.18. Definition 2.2 and Proposition 3.1 (original PDF p.2, printed p.96) add active-flow restrictions and prove hardness. Here integral pure-mode replacement is proved for an ordinary continuous pooling family under simultaneous degree/data restrictions. Do not imply that hard selection of sparse modes itself is unprecedented. Root read and visually verified the source, already in the local literature folder; see root-stage2.md.

## Optional suggestion not adopted

R1 O2 suggests adding Haugland's MAGO 2014 announcement of scalar two-pool hardness. The current text neither claims first two-pool hardness nor claims scalar hardness for its two-output tree theorem. It identifies the precise output-count question in the later published Haugland and BKR treatments. The earlier unproved announcement has a different unrestricted-output scope and is not needed to support or qualify those claims. Adding this historical detour would not clarify the final result. No theorem or asserted priority depends on excluding it.

A separate correction agent will implement all nine accepted minor items. Because no accepted issue is major, the user's procedure does not require another five-reviewer round for this stage. Root will inspect the correction diff, validate the diagram and new citations, and require a clean isolated build before acceptance.

## Correction acceptance

Root read the complete correction report and diff, independently checked the new citation, formulas and node inventory, and inspected the rendered figure on p.39 and inventory on p.46. A tight pair of flow labels was corrected by the correction agent and the final rendering rechecked. The isolated 95-page build has no unresolved references/citations, TeX warnings, or overfull boxes; two unchanged bibliography metadata warnings belong to the later bibliography stage. `git diff --check` passes. All nine accepted minor items are resolved. Stage 2 is accepted, with sources frozen in stage2-accepted/. No major finding requires another review round.
