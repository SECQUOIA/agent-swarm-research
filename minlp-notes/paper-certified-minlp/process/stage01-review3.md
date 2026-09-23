# Stage 1 independent review 3

Reviewed 2026-09-13. Scope: introduction, model/checking contract, bibliography, evidence maps, and current author report; emphasis on empirical claim-to-evidence integrity and relevant-topic scope. No manuscript or checker edits were made. This is an independent read and targeted evidence audit, not a rerun of all large proofs.

## Verdict

**No major Stage 1 issues found.** One concrete minor evidence-label error should be corrected before advancing. The current prose properly limits the contribution to the implemented integration and reliability study, distinguishes historical acceptance from current replay, and does not infer original-model optimality from a master incumbent or a library reference. The remaining sections, public artifact packaging, and prospective experiments are later-stage obligations, not defects in these two initial sections.

## Required minor correction

**R3-1 — Timing population and measurement are mislabeled in the evidence map.** `evidence/repository-inventory.md:30` calls 7,987.954 seconds “summed worker times” for the final campaign. Recomputing from the 289 raw JSONL records shows that this is the sum of `checker_seconds` for only the 188 verified records. It excludes rejected records and per-record hashing. `certify/summarize.py:78` explicitly constructs its timing list from `verified`.

The distinct raw aggregates are:

| Measurement | Seconds |
|---|---:|
| Campaign wall time from the timing JSON | 1,465.3805854320526 |
| Sum of checker time over 188 verified records | 7,987.953598855151 |
| Sum of checker time over all 289 records | 8,234.349308964098 |
| Sum of per-record elapsed time over all records | 8,337.713025806152 |

Proposed fix: replace “summed worker times 7,987.954 seconds” with “summed checker time for the 188 verified records was 7,987.954 seconds.” If the intended statistic is total campaign work, use the appropriate all-record aggregate and state what it includes. Preserve the distinction in later experiment tables. This does not change the acceptance evidence or the stated absence of performance-superiority claims.

## Evidence checks and accepted claims

- Independently parsed all 289 replay JSONL records: 289 distinct instance names, 188 `verified`, 92 `rejected`, nine `missing_artifacts`. The historical `historical_checker` labels are 269 `OK`, six `FAIL`, and 14 absent. The introduction correctly identifies 269 as a previous acceptance label, not the repaired verified total.
- Independently summed verified proof-file sizes from raw artifact entries: 38,826,726,525 bytes, matching the evidence map. The audit JSON's 67 domain/curvature, 13 cut-check, and 12 proof-inference rejections agrees with the map. The proof-failure record explicitly limits its independent arithmetic reconstruction to rejected rows and shared parsing; neither initial section overstates this as a second complete verifier.
- Inspected `solver_discrepancy_audit/audit.json`, the joined `clay0204m_optimality.json`, and the primal/source evaluator. The `clay0204m` record joins an exact feasible objective of 6545 with a complete lower check of 6545. Its pinned certification-source hashes still match current files. The saved-point residual evidence contains affine violations 9/2 and 3 for `clay0204m`, and upper-bound violations of 1 for `b4` and `b5` in `risk2bpb`.
- The source-equivalence evaluator documents exact binary64 source literals and does not verify the GAMS compiler or historical execution. The model section's distinction among source file, loaded tree, and checked expression is therefore necessary and correctly stated. Later discrepancy writing must retain this limitation and ignore insignificant residuals attributable to listing precision; the current map and introduction already avoid a universal solver-bug diagnosis.
- Inspected `prepare_model`, rational propagation, full/partial checking, VIPR/master comparison, and given-cut checking in `driver.py`. The declared domain-before-propagation convention, exact master constants, variable correspondence, full proof requirement, and absence of a certified bound from partial success agree with the initial contract. The distinction between a sufficient underestimator on the box and a merely valid row cut is mathematically correct.
- The support-point discussion correctly avoids assuming a finite gradient at every boundary point and correctly treats general subgradients as mathematical permission rather than an implemented oracle. The primal-gap statement follows from a feasible witness and the verified lower bound; it does not assume attainment for lower-bound certification alone.
- The topic inventory covers the relevant existing developments: exact semantics, safe cuts including unbounded coordinates, rational propagation, proof replay and discovered defects, proof/master identity, historical repair outcomes, fresh regressions, source/primal discrepancies, exact optimality examples, and trust/reproducibility limits. Adjacent unrelated optimization work need not be incorporated merely because its notes also use “certified” or “convex.” Formal work is accurately identified as a future scoped obligation rather than an already completed theorem.

## Writing and literature boundary

The introduction gives the closest convex-MINLP certificate work a prominent comparison and explicitly disclaims novelty for classical outer approximation, safe rounding, finite certificates, and discrete proof replay. The literature map records source locations and distinguishes full-text inspection from abstract-level inspection. No unsupported priority claim appears in the present introduction. This review did not independently reverify every bibliographic field or every prior-work theorem; those are covered by the dedicated literature review rather than inferred from this empirical audit.

“Restricted complete VIPR language” is understandable in the context of the complete/partial distinction, but later kernel exposition should state the accepted syntax precisely so that “complete” is read as complete proof artifacts rather than support for every VIPR extension. This is a later exposition obligation, not an additional required Stage 1 correction.
