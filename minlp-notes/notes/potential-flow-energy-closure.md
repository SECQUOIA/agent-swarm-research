# Closure of the global energy direction

Later update: [potential-flow work reopened on 2026-09-06](potential-flow-reopened-status.md).
The weighted cactus summation and nomination-face gaps recorded below now have
separately reviewed resolutions. General higher-rank block approximation remains
outside the new algorithm. This file retains the earlier energy closeout history.

Date: 2026-09-05. This records completion of an existing direction, not a new research proposal.

The [maximum-dissipation result](../results/potential-flow-global-energy-maximization.md) is complete as a verified supporting result. Both mathematical audits, the primary-source assessment, the cactus capacity-filter addenda, and the exact certificate-code audit passed. Its positive conclusion comes from classical resistance-energy concavity and conic duality; the detailed polynomial-bit output and original-instance certificate are retained without a broad new-convexity claim. The opposite [minimum-energy direction](../results/potential-flow-global-correlation-energy-design-hardness.md) remains strongly hard under its stated bounded-data global correlations. These statements concern different optimization directions and are consistent.

The closure check reran the exact cone/state checker: 180 cone cases, 1,080 necessity controls, 84 complete-graph physical states, 1,008 edge witnesses, and five interior constructions passed. The saved triangle certificate again gave exact lower and upper dissipation `3/4`, with zero global suboptimality. The independent certificate audit checker again accepted 99 exact certificates and 99 gauge shifts, rejected 151 malformed direct inputs, and rejected 294 corrupt CLI inputs under normal and optimized Python. No code or mathematical correction was needed.

## Existing flow investigations reconciled

- The [cross-cycle example](potential-flow-cross-cycle-correlation-obstruction.md) already had a complete independent review. Its stale status was corrected. It proves nonconvexity and failure of shared-parameter endpoint selection, without a hardness conclusion.
- The [cactus uncertainty-hull characterization](potential-flow-cactus-uncertainty-hulls.md) already had an independent review covering both the qualitative proof and the explicit polynomial-size restoration. Its stale status was corrected. The missing older nonlinear-tolerance source remains a priority limitation, not an unverified proof step.
- The [power-law region extension](potential-flow-power-law-region-convexity-extension.md) already had two independent audits and a source assessment. Its stale status was corrected. It is qualitative for each fixed real exponent `p>0`, `p!=1`; no quantitative restoration claim was added.
- The [early block/law extensions](potential-flow-block-law-extensions.md) are covered by the stronger twice-reviewed continuous polynomial-law theorem. Their derivation is archived as superseded.
- The [early joint-resistance sign-pattern route](potential-flow-joint-resistance-sign-patterns.md) is archived as superseded by the independently proved joint theorem. The latter does not depend on establishing every claim of that older route.
- The [weighted bounded-block obstruction](potential-flow-bounded-block-weighted-obstruction.md) remains a documented limitation: varying algebraic block functions prevent the existing one-active-block summation argument from extending directly. Its Wronskian outline is not a proved optimization algorithm. No result from that outline is claimed here.

The [weighted sign-path corollary](potential-flow-weighted-sign-path-decomposition.md) now has a completed [root audit](review-potential-flow-weighted-sign-path-decomposition.md). Its exact checker passed 192 signed paths, including 32 returning paths and 3,394 threshold checks. This inventory makes no claim that all possible flow generalizations or all historical priority questions have been resolved.
