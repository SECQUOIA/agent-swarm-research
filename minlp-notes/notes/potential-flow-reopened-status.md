# Potential-flow continuation and paper-readiness work

Started: 2026-09-07 (UTC). Status: complete. The [paper-readiness record](potential-flow-paper-readiness.md) gives the final results, evidence, and scope.

The user reopened the potential-flow topic to develop practically important results, thoroughly verify them through independent reviews, and prepare the existing directions for a paper. This record supersedes the earlier closure only for this topic. Other repository research programs and paper work are outside this continuation.

## Work undertaken

1. Reassess the envelope theorem against newly available circuit literature and try to resolve the remaining Hasler–Wang source gap.
2. Build an original-instance envelope certificate pipeline. The verifier must check the graph, original uncertainty data, envelope mapping, numerical energy certificate, and recovered scenario, rather than trusting a preconstructed energy instance.
3. Investigate weighted objectives with bounded cycle rank per block. In particular, examine certified rational approximation of sums of local algebraic pressure-drop functions; the old Wronskian outline is not a proved algorithm.
4. Determine useful extensions and obstructions for operating constraints. Distinguish universal validation from filtering the allowed uncertainty scenarios, and exact feasibility from additive optimization.
5. Develop conservation-aware certificates for linear flow measurements, using the convex energy sublevel containing the exact physical state.

Each promoted development received independent mathematical and, where applicable, implementation review. Source comparison, written proofs, exact arithmetic checks, and numerical experiments provide different evidence. None is described as external peer review or formal certification of a universal theorem.

## Initial observations

- The literature archive has gained directly relevant circuit sources since the earlier source audit; its older missing-source statements need reassessment.
- The existing saved energy certificates do not encode the original graph/target/uncertainty mapping. Closing this interface is useful even if the underlying convexity and certificate mechanisms are established.
- Existing paper directories contain unrelated pre-existing modifications. This continuation will preserve them.

The final dispositions follow; detailed proof and implementation records are linked from the paper-readiness record.

## Completed review gates

- The fixed-factor weighted cactus approximation proof passed independent review after corrections to bridge sign partitions, accuracy normalization, and closed capacity-domain hypotheses.
- The weighted nomination-face reduction passed two independent reviews. It bounds free **reduced** nominations; disaggregation need not produce a sparse face in the original coordinates.
- The joint interval-resistance extension passed two independent full reviews, including exact local capacities with algebraic output. Rational capacity recovery is compared with the tightened problem's optimum unless an optimum-margin assumption is supplied.
- A fixed-nomination corollary strengthens additive recovery to an exact optimal rational resistance profile, including rational local arc capacities. Its proof passed both reviewers. The [exact block solver](potential-flow-exact-weighted-cactus-solver.md) also passed independent optimization and arithmetic/schema reviews; it requires supplied cycle/bridge blocks.
- The original-instance envelope pipeline and its conservation-aware goal witnesses passed independent mathematical and implementation reviews. A zero-load fallback regression found during integration was corrected.
- The ordinary-capacity irrational-witness example and uniform resistance Lipschitz bound passed independent checks. The latter improves the original square-root rounding estimate to a linear estimate.
- The final consolidated replay passed all 19 selected commands; outputs and test-source hashes are in [reopened_validation.json](../code/potential_flow_mpd/reopened_validation.json). Proof checks that use assertions run without optimization; certificate verifiers also run with `-S -O`. The ten bounded envelope benchmarks passed, with exact endpoint optimality certified in nine.

The source follow-up retrieved the relevant Gotzes et al. 2016 paper and credited its affine-ray radical formulas. Vigneron's approximate-summation architecture and the earlier interval-resistance models are also explicitly credited. No inspected source supplies the combined weighted cactus accuracy-bit theorem. Hasler–Wang 1993 remains a documented access gap for the older envelope identity.

## Final disposition

The weighted cactus summation gap is resolved, including joint continuous resistance uncertainty and an exact fixed-nomination specialization. The original-instance certificate interface and conservation-aware bounds are implemented and reviewed. Capacity feasibility and rational-output limitations are proved with exact counterexamples, and the resistance Lipschitz bound supplies explicit rounding budgets.

General higher-rank weighted block optimization, discrete or correlated resistance choices, and broader operating filters remain outside the proved statements. The full varying-load algebraic optimizer is not implemented. These boundaries, the source qualifications, and the supplied-block solver contract are preserved in the [paper-readiness record](potential-flow-paper-readiness.md). Current results are ready to be written into a paper; no further development is active in this continuation.
