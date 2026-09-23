# Stage 1 independent review 1

Reviewed 2026-09-13. Scope: the introduction, mathematical model and checking contract, bibliography, evidence inventory/literature review, and current author report. Particular attention was given to exact expression identity, declared domains, support points, and correspondence with the repaired implementation. No manuscript or checker files were edited.

## Verdict

**No major issues found in Stage 1.** The stated lower-bound contract is mathematically coherent, the implementation restrictions are represented conservatively, and the prior-work discussion avoids a broad priority claim. One minor terminology correction is recommended before closing this stage.

## Finding

### R1-1 — Minor: distinguish complete proofs from completeness of the admitted language

Location: `sections/01-introduction.tex:33`, sentence beginning “Our Python replay kernel”.

“A restricted complete VIPR language” is ambiguous: a reader may understand “complete” as a proof-system completeness assertion or as full VIPR language support. Neither interpretation is established or intended. The implemented interface checks complete proof artifacts in an admitted subset of VIPR. This agrees with `certify/vipr.py`, the inventory's explicit unsupported-case rejection, and the later statement that no general completeness theorem is claimed.

Proposed correction: “Our Python replay kernel is a separate, unmechanized implementation that checks complete proofs in a restricted subset of VIPR.” The later implementation section can enumerate that subset and explain full suffix consumption.

## Independent checks and reasoning

- Read `exact_model.py`, the domain/curvature implementation in `convexity.py`, `SafeCutter` and its interval evaluator, and the model preparation, rational propagation, and supplied-cut checking in `driver.py`. The shared exact extractor really uses rational arithmetic; the misleading legacy local name `generate_standard_repn` in the curvature module is an alias of the exact extractor, not evidence of floating aggregation.
- Confirmed that domain validation traverses original expression subtrees before symbolic simplification. Negative powers and division require a base/denominator away from zero; logarithms require positive arguments. The declared-box domain rule precedes affine propagation. The model section accurately distinguishes this sufficient restriction from feasible-domain definedness.
- Checked that supplied support points must lie in the propagated box and that every row variable participates in the residual-slope correction. Half-lines require the appropriate residual sign; a free coordinate requires an exactly zero interval residual. The text's stronger support inequality is the appropriate mathematical premise.
- The differentiability condition in Section 2 is sufficient, without incorrectly asserting finite boundary gradients. The example `-sqrt(x)` at zero is correct: a finite slope would have to satisfy `s <= -1/sqrt(x)` for every positive `x`, which is impossible. More general accepted boundary derivatives and curvature recognizers remain later proof/implementation obligations.
- Verified the binary-coefficient example by exact `Fraction` arithmetic: the sum is `-1/36028797018963968 = -2^-55`. Its curvature distinction is correct.
- Checked epigraph extension, affine constants, minimization/maximization sign conversion, the empty-feasible-set convention, and the final primal-witness inequality. With finite checked lower bound and a feasible witness, `beta <= p* <= f(w) <= U`; thus the stated gap follows, and `U=beta` does imply attainment.
- Ran the narrow existing independent semantic regressions: `test_exact_semantics.py`, `test_independent_semantics.py`, and `test_driver_independent_review.py`; **28 tests passed**. This supports the inspected executable boundaries, not a software soundness theorem.
- Independently counted `cert_replay_20260913_complete.jsonl`: 289 rows, 188 `verified`, 92 `rejected`, and 9 `missing_artifacts`. I did not rerun the full large-proof campaign.
- Read the inventory and current author report against the inspected code and soundness note. Their claims about current versus historical status, the loaded-tree interpretation, restricted derivative support, and unmechanized checker trust are consistent.
- Independently opened [Wood et al., open manuscript v4](https://arxiv.org/html/2312.10420v4), including its explicit separation between logical transformation verification and executable implementation. The introduction's restraint about that scope is supported. This review did not independently refresh every bibliography record; failed DOI resolutions for Coey and Szeider during this pass supply no contrary evidence.

## Obligations for later stages, not current defects

1. Prove the rational intercept formulas and their half-line/free-coordinate cases, including the relation between the symbolic-gradient route and the general support-vector contract.
2. State the admitted expression and proof rules precisely. “Supported” is appropriately qualified here but must become reproducible in the implementation section.
3. Give the incumbent-cutoff argument: such rows are conditional on improving a checked master solution and are not unconditional inequalities for all feasible master points.
4. Provide accessible artifacts or checked acquisition instructions before retaining “reproducible” in a final submission. The inventory already identifies this packaging obligation.
5. Keep the broader significance proportional to an integration/reliability contribution; this Stage 1 text does not establish first-of-kind priority, polynomial certificate size, or solver superiority.

No result-invalidating error was identified, and no major-issue review cycle is required by this review alone after the minor terminology correction.
