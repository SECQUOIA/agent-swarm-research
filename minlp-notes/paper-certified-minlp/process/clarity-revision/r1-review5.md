# R1 independent review 5

## Verdict

**No major issue found.** The revision states the scientific problem and value more clearly while retaining the exact-model and trust qualifications. One minor wording change would keep the conclusion's experiment statistic as precise as the abstract and introduction.

Read the revision plan, R1 author report, current abstract, introduction and discussion, and the corresponding frozen experiment summary. No other R1 report was read; no manuscript, numerical evidence or code was changed. Pending R2 experiment organization and archive refresh are expected later-stage work, not R1 defects.

## Minor correction

1. **Minor — attach the 203 count specifically to accepted replay artifacts in the conclusion.** At `sections/07-discussion.tex:11`, “demonstrates practical certificate production and replay for 203 of 289 attempted models” can be read as 203 successful producer returns. The frozen experiment has 198 completed accepted productions and 203 accepted artifacts in separate replay, including four timeout survivors and one worker-error survivor. The next sentence helps, so this is a clarity issue rather than a false numerical result. Use, for example: “The uniform experiment yields accepted artifacts for 203 of 289 attempted models in separate replay. This demonstrates practical capability under the stated protocol.” Retain the following sentence about unsuccessful producer returns. This also makes the abstract, introduction and conclusion use the same operational meaning of 203.

## Scientific assessment

The first paragraph identifies the actual research problem: nonlinear cut validity for the interpreted model and binding of that relaxation to the exact discrete proof. The next paragraphs explain the objective-preserving feasible-set connection and why numerical subproblem accuracy is not a soundness premise. This provides a concrete significance statement without inventing a new optimization principle.

The four contribution categories distinguish method, findings, validation and artifacts. The 161 tests are presented as executable validation rather than 161 separate mathematical discoveries; Lean's support/enclosure premises and unmechanized software boundary are explicit. The 222-model catalogue remains a descriptive cross-protocol collection. Neither its coverage nor the 203/289 replay statistic is presented as a general performance or completeness result.

The three completed externally accepted proofs in the abstract are supported by the existing three-proof audit: two mixed-direction linear combinations and one gapped integer disjunction. The wording identifies invalid supplied steps, not false final objective bounds. The introduction and conclusion maintain the separate category of conservative curvature/domain/cut-enclosure rejections. They do not infer solver defects merely from reference discrepancies.

Exact optimality in the two witness cases is kept distinct from feasibility in the MILP relaxation or proximity to a library reference. The discussion's source/loaded-model distinction prevents an unqualified claim of certification of earlier decimal source semantics. The phrase “original-model” is supported by the explicit same-model condition and model-section reference.

The shorter literature discussion still places Halbig et al. prominently, retains their continuous plane-check and discrete integer-freeness procedures, and preserves the finite-point-count versus bit-length distinction. Established safe bounding, support minimization, VIPR checking and formal verification remain attributed. No first-system claim, unsupported absence assertion, or novelty inflation was introduced by shortening the earlier qualifications.

Apart from the single count-label clarification above, the R1 revision improves the framing without changing the supported scientific scope.
