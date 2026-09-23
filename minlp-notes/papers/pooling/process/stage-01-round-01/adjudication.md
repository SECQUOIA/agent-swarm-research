# Root adjudication: stage 1, round 1

All 15 assigned reviewers delivered reports. Root assessed the counterexamples and proof arguments, rather than counting agreement as mathematical evidence.

## Accepted major finding

M1: The endpoint disjunction and MILP omit the essential upper-quality-only restriction. Accepted. All 15 reviewers identified this defect. With source qualities 0 and 1 and a product requiring quality exactly 1, the proposed disjunction permits a unit flow from the quality-0 source because the upper bound is 1. That flow violates the lower quality constraint. Even faciality does not repair the stated equivalence. Restrict this specialization explicitly to coordinate upper quality bounds in `{0,1}`, with no additional nonredundant quality restrictions. Lower flow bounds remain permitted. The intended theorem and proof then apply. This is major despite its short textual repair because the stated equivalence is false without the hypothesis.

## Accepted minor findings

1. Effective finite flow bounds: reviews 01, 02, 03, 08, 13, 15. State that finite rational upper bounds bound every arc flow in all capacitated models, either directly or through finite node capacities. Put this condition before boundedness/attainment assertions. The uncapacitated cone is explicitly exempt. If source upper bounds are not explicitly supplied, bound the return arc by the sum of effective arc upper bounds. This clarifies the intended model rather than proving an unbounded optimization claim.
2. Scaling before reconstruction: review 04. Route the shortest-path mixture, scale it to satisfy capacities, and then invoke the capacitated single-product lemma. Explicitly ignore zero-load capacity rows when defining the scale.
3. Absorption conventions: review 06. Define `h_j=0` on removed circulation classes and inactive pools, and the Kronecker values on products, before the component formula on the whole arc set.
4. Conflicting notation: reviews 08 and 12. Use a scalar demand symbol distinct from the polyhedral right-hand-side vector `b_j`.
5. Dual cone answer direction: review 14. Say that no profitable flow exists exactly when the cost belongs to the dual cone; profitable flow corresponds to nonmembership.
6. Bibliography author names: review 11. Correct Gupte to Akshay and Cheon to Myun-Seok, verified against the actual source. Also normalize volume/number/pages into proper fields for the four current entries, using verified metadata; this is a publication-format improvement.

No reported finding was rejected. Duplicate findings are consolidated above. No additional result is inferred from the reviewers' lack of objections. The coverage audit found no material stage-1 omissions. The cyclic approximation completion received direct proof checks, including its compactness and circulation-merging arguments.

## Required next action

A separate repair agent will implement these corrections and record the changes and compilation check. Because M1 is major, stage 1 must then receive another complete 15-agent review. Stage 2 remains pending.
