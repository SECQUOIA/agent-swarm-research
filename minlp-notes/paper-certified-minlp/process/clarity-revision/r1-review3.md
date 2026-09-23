# R1 independent review 3: scientific framing and prior work

Verdict: **No major or minor issue identified.** The revision makes the research problem and scientific contribution easier to identify while preserving the supported scope. No correction is requested.

## Scope

I read `PLAN.md`, `r1-author.md`, and all of the current abstract, introduction, and discussion. I checked their revised claims against the accepted soundness, formal-coverage, and experimental sections and result tables. The earlier primary-source inspections recorded in my Stage 5 and Stage 6 reviews remain evidence for the unchanged source facts; this review does not claim a new full literature search or new experimental execution. No other R1 review report was read, no work was delegated, and no manuscript file was edited.

## Assessment

1. **The scientific problem now precedes the implementation inventory.** The opening identifies the gap between a rational discrete proof and a bound for the stated nonlinear model: validity of the cuts and identity of the justified master. The next paragraphs give the desired mathematical assertion and the proposed chain of evidence. This is a concrete research problem with an explicit result, rather than an implicit claim that assembling software components alone supplies novelty.

2. **The four contribution categories accurately separate evidence types.** The method is the implemented certificate interface and its conditional soundness. The experiments establish observed capability and specific reliability failures. Tests and the selected Lean theorems provide validation within their respective boundaries. The catalogue and replay materials are reusable artifacts. The 161 tests are not recast as 161 independent mathematical facts, and the 222-model union is expressly not a uniform success rate.

3. **Attribution survives the shorter presentation.** Halbig et al. remain the closest computational comparison, and the comparison specifies the difference in checking procedures rather than implying that prior convex-MINLP certificates lack independent verification. Baes's point bound is still distinguished from bit complexity. Jansson, Messine–Trombettoni, and Elloumi receive clear credit for rigorous bounding; the finite-box residual correction is explicitly called an application of an established calculation. The description of QIBEX-R continues to be a claim about what Elloumi et al. describe, not an independent validation or an assertion that their software cannot export evidence.

4. **No unsupported priority claim is introduced.** The rewritten abstract's phrase “closes these gaps” is tied to the implemented contract, followed by conditional soundness and the unmechanized executable boundary. The introduction explicitly credits established support and proof principles. Its Slater/attainment discussion remains a conditional validity result, with no inferred completeness advantage. Wood, CakeML, CvxLean, and earlier formal nonlinear work retain their distinct credited contributions.

5. **The prominent empirical claims preserve their evidence.** The 203/289 figure is accepted artifacts in separate replay, not 203 completed successful producer returns. The three completed proofs with external acceptance are the existing exact local audits in Section 6. The text describes invalid supplied combination/disjunction steps, not necessarily false final bounds. Original-model witnesses remain essential to the two exact-optimality conclusions. Omitting historical bookkeeping and example objective values from the abstract does not remove those results from the paper or distort their interpretation.

6. **The discussion synthesizes consequences without overstating them.** It explains consistent model semantics, distinct failure categories, original-model primal feasibility, and representation costs. The exact loaded model remains distinct from source-formula equivalence. An invalid local justification, a failed sufficient test, and a reference discrepancy are kept separate. The conclusions acknowledge incomplete admission, large proofs, shared-machine timing, and unverified executable components. These limits are consistent with the scientific contribution rather than retreating from an earlier broader assertion.

The pending experimental reorganization and archive/documentation update belong to R2 under the approved plan. Their absence at this intermediate gate is not an R1 defect.
