# Stage 4, round 1: root adjudication

Root read all 15 full reports in their entirety. Fourteen report no findings; reviewer04 reports one minor finding. No reviewer reports a major finding. Reviewers04 and14 also offer optional local exposition suggestions, which root accepts below because they remove avoidable ambiguity with small edits. Historical or current votes are not proof; root independently read the whole draft and checked the relevant mathematical/source claims.

## Accepted corrections

1. **m1 — validate the full flow-bound interval before deleting an unusable pool (reviewer04).** Accepted as minor. The global model permits rational interval endpoints; a negative upper endpoint gives an immediately infeasible instance. The explicit pool-throughput interval [-2,-1] counterexample shows that checking only the lower endpoint before deletion can overlook this. This is an elementary input-validation step, not a defect in the structural decomposition, complexity proof, or intended main theorem. Repair the stage-4 removal instructions to require zero in every pool and incident-arc interval. Also add the equivalent initial normalization in the foundations model: intersect every flow-bound interval with the nonnegative ray and reject an empty interval; align its unusable-pool sentence with full-interval validation. This clarifies preprocessing for the existing rational-input scope and does not narrow any theorem or change a reduction. It is a minor change to accepted stage1, preserved in the audit and included in final whole-paper review; it does not materially reopen its mathematical results.

2. **m2 — identify both fixed-input predecessors as using no bypasses (reviewer04 optional suggestion).** Accepted as a minor source-scope clarification. Both primary models have been checked. Replace the wording that singles out only the latter source with an accurate statement that both omit bypasses, while noting the latter explicitly discusses the convention. Do not add or change source metadata.

3. **m3 — distinguish arithmetic lifting from bit-time lifting in the abstract path statement (reviewer14 optional suggestion).** Accepted as minor. Arbitrary real endpoints have no finite binary encoding. The following represented-common-field sentence and proof already establish every pooling use. Say the general lift uses polynomially many arithmetic operations/comparisons, and the represented algebraic case has polynomial bit time including its input/output encoding. No change to the constructive proof is required.

No other report requests correction. No major finding was accepted, so another full stage-4 round is not required by the agreed protocol. A different agent will implement all three accepted edits. Root will inspect the exact diffs, verify the unchanged algebraic/hardness dependencies and bibliography, and rebuild before closing the stage or beginning stage5.

## Review limits

All reviewers assessed the full frozen stage with complementary emphasis, canonical proofs, relevant precursors, and primary-source/dependency checks. Their reports document limits concerning implementation of the cited general algebraic algorithms, exhaustive literature priority, and external certification. The finite support/ownership/projection checks supplement the proofs. No external acceptance or exhaustive absence of errors is inferred.

## Closure

Root inspected the separate repair diff and record, verified all three accepted changes, and checked the clean54-page build and dependency hashes. No accepted issue remains. Stage4 closes; stage5 may begin. Final stage4 SHA-256 `88b1c181cde7f72b48535054de702a2ff4688a470633eb56e528c519974189de`. The global interval normalization is a minor clarification of elementary preprocessing, not a narrower mathematical hypothesis.
