# Final independent review

Date: 2026-09-22. The final integration reviewer authored no production
Lean module in this package.

The 37 obligations in [CLAIMS.md](CLAIMS.md) are covered by the declarations
mapped in [COVERAGE.md](COVERAGE.md). No unresolved mathematical,
statement-fidelity, or whole-execution cost finding remains. This review
approves the represented-matroid package within its stated input and cost
model. Build, axiom-audit, kernel-replay, and manuscript evidence are separate
checks recorded in the verification directory and topic README.

## Original-input conclusion

`representedSpectralCover_complete` applies to the supplied arbitrary
rectangular rational representation, PSD element information, PSD prior,
and rational `0 < eta < 1`. For every original column base it produces one
actual returned original base satisfying both relative PSD inequalities,
with exactly the same kernel and range. Redundant representation rows,
singular information, repeated factor owners, prior-owned factors, and the
three distinct rank-zero cases are covered.

The counted implementation is `representedInputRun`.
`representedInputRun_value` identifies its returned list's underlying set
with that same headline cover. `representedInputRun_polynomial_work`
supplies the original-input cost bound with no assumed feasibility oracle
or good-normalization certificate. Only information dimension is fixed;
representation dimensions and matroid rank remain variable.

## Claim closure

| Claims | Review conclusion |
|---|---|
| M01–M04 | Row selection preserves all column dependencies and original bases. Restriction and deletion retain the original row count. The owner marker is equivalent to containment of the deduplicated forced-owner set. The selected variant uses owner counting, not a claimed contraction implementation. Nonzero scalar clearing also preserves bases. |
| N01–N07 | The original matrices feed the actual rational PSD factor cache. Existing generic normalization theorems apply to finite sets without graph assumptions. Maximum volume supplies a proof-only good trial; the executed enumeration, exact dyadic scales, filters, forced owners, identity floor, reconstruction, and exact ranges are connected to it. No supplied normalization witness remains. |
| P01–P06 | Signed floors include negative entries. Equal base cardinality cancels the shift. The actual rational determinant polynomial has precisely the attained profiles as positive coefficients. Explicit interpolation evaluates that polynomial and one-pass deletion recovers actual original bases. Ground-truth enumeration appears only in specifications and proofs. |
| S01–S03 | Common forced and prior contributions cancel. The sharp optional-entry bound requires positive optional rank, while zero optional rank gives equality. The explicit spectral factor is `r q h = eta`; rectangular reconstruction gives both PSD directions and exact kernels/ranges without a conditioning assumption. |
| C01–C04 | The optional-profile injection preserves the source output count despite the owner coordinate. Variable-rank determinant and interpolation operands have polynomial encoding bounds. Cached execution includes preprocessing, all trials, support and deletion queries, storage, deduplication, and witness production. Its final polynomial envelope depends on fixed `p`, not fixed matroid rank. |
| O01–O06 | Generic homogeneous criteria retain their explicit comparison requirement. Concrete D, E, A, contrast, and weighted-contrast selectors have exact comparison implementations and stated bit-work bounds. Singular conventional A-cost is infinite, estimability and zero variance are preserved, and common-prior or rectangular-congruence transfer keeps the same cover. |
| U01–U03 | Explicit uniform and partition representations satisfy the supplied-matrix contract with polynomial encoding. Oriented incidence covers arbitrary finite labelled graphs, including loops, parallel edges, and disconnected spanning forests; connectedness gives spanning trees. |
| B01–B04 | Exact witnesses establish the stated cancellation, finite-field, unattained-profile, interior-optimum, dominance-deletion, and singular-range limitations. Rank preservation, characteristic-zero positivity, and zero optional rank remain explicit safeguards. These witnesses are not broader hardness claims. |

The independent component evidence is in
[REVIEW-ALGEBRA.md](REVIEW-ALGEBRA.md),
[REVIEW-REPRESENTATION.md](REVIEW-REPRESENTATION.md),
[REVIEW-INTERPOLATION.md](REVIEW-INTERPOLATION.md),
[REVIEW-CARDINALITY.md](REVIEW-CARDINALITY.md), and
[REVIEW-CONSEQUENCES.md](REVIEW-CONSEQUENCES.md).
The final reviewer additionally read the complete new execution composition,
the original-input interfaces, the normalization reuse boundary, the sharp
optional remainder, and the polynomial cardinality and cost definitions.
[REVIEW-COMPLEXITY.md](REVIEW-COMPLEXITY.md) records the final cost closure.
This closes the scope exclusions of the earlier bounded component reviews;
no review is used to approve its author's own implementation.

## Final execution and source checks

The assembled `InputExecution` module passed its targeted build with warnings
as errors. The final review snapshot is recorded in
[REVIEW-FINAL-SOURCES.json](REVIEW-FINAL-SOURCES.json).
All 17 earlier representation-review hashes and all 12 earlier
consequence-review hashes were rechecked after the interruption and matched
the current source. The final execution edits changed proof elaboration,
coordinate-order instance coherence, and cost assembly; their interfaces
were reread after the successful build.

The preserved [execution client](verification/ExecutionExamples.lean) passed
all three exact returned-base checks: matroid rank zero with nonzero prior,
positive matroid rank with zero information, and positive scalar information.
It ran with warnings as errors; the last case executes normalization, shifted
labels, the owner marker, determinant interpolation, and recovery. This result
is separate from the universal proofs and the independent kernel replay.
Finite examples cannot establish the spectral or complexity theorems.

The cost model counts exact integer/rational arithmetic and conservative
finite scans, storage, and witness copies. It does not measure the time or
memory used by Lean to construct the cost observer's transcripts. The output
list may repeat the same base across trials; its underlying set is the proved
cover. No dominance pruning or Pareto-maximality assertion is introduced.

The scope remains explicit rational representations and additive PSD
information. Arbitrary independence-oracle or finite-field inputs,
simultaneous path and matroid constraints, matroid intersection, arbitrary
correlated histories, priority claims, and practical performance claims are
excluded as in [SOURCE-REVIEW.md](SOURCE-REVIEW.md). No project-wide local
verification or CI inspection was performed for this review.
