# Independent review: basis initialization and source access

Verdict: **PASS for `BasisInputExecution.lean` and its explicit scan/copy
model.** Complete cover execution and its global polynomial bound are
reviewed separately.

The producer scans the actual candidate finset for every integer label in
the increasing identifier list. The pair-valued commutative sum records both
matches and comparisons; its value is independent of the finset's internal
ordering. The resulting label vector is proved equal to the original sorted
label enumeration. Empty candidates still incur identifier initialization
and failed membership-scan charges.

For each selected label, `cellsRun` materializes its rational column, weight,
and owner. It binds each copied scalar, weight, and owner once before using
that value in both the result and its payload-size charge. `basisRun_columns`
and `basisRun_weights` identify the actual cache with the earlier producers.
There is no independence premise: dependent candidates produce the same
well-defined input cache and can be rejected by the next gate.

The owner procedure scans all stored owners for every possible edge,
including entries after a match. It constructs its finset directly from the
already distinct filtered identifier list. This avoids a hidden duplicate
removal algorithm. Prior owner `none` is excluded, while repeated edge owners
are represented once. `basisRun_required` proves exact equality with
`forcedOwners`, preserving its intended mask meaning.

The scan/copy counter includes counted identifier initialization, every label
and owner scan, list/array copies of actual rational payloads, copied owner
and label identifiers, and source-field access charges. The final scalar
copy loop binds its source value once. Every column coordinate pays
`(M+p+2)^2` for source access; weight and owner each pay that charge too.
The review identified and the author corrected an earlier undercount caused
by multiple uncached source-field reads. The final per-field accounting does
not rely on compiler hoisting of a function-valued column.

For the concrete input representation, `InputRun.factorAtRun` executes a
counted lookup on the stored factor list. It returns the same record as
`factorAt` and visits at most `M+1` cells. `cachedFactorData` uses that executed
accessor in its runtime fields. The squared access budget conservatively
covers this linear list traversal and coordinate/index control. A generic
`FactorData` value may contain arbitrary functions, so `basisRun_work` is a
bound in this declared finite-data access model, not a runtime theorem for
every possible Lean implementation of those functions.

The inspected integration invokes `basisRun` before the independence gate
and includes both the returned basis cost and `gate.copies` in the rejected
branch. Successful candidates deliberately initialize the basis again inside
`trialBitRun`; this second run is also charged. The trial then uses the stored
columns, weights, and deduplicated owner set in normalization and the actual
profile DP. This source inspection checks data and charge flow; the final
aggregate bound is a separate obligation.

Targeted verification:

- `lake build --wfail Formal.DAGSpectral.BasisInputExecution` passed.
- The independent `topics/21-dag-spectral/verification/FactorDataReview.lean` client was extended
  with seven basis assertions using actual raw-input factor caches: increasing
  labels, both column rows, repeated-owner deduplication and prior omission,
  empty-candidate work, a full owner scan after a match, and exact rational
  payload plus access charge. These and the four preceding factor-data checks
  passed with `lake env lean -DwarningAsError=true`. Two final checks of the
  counted source accessor verified its last-factor traversal and returned
  coordinate, bringing this client to thirteen assertions.
- `basisRun_work` and `basisRun_required` have only `propext`,
  `Classical.choice`, and `Quot.sound` as axioms. No project-wide or CI checks
  were run.

Reviewed SHA-256:
`6ed210104376e8f0d5ce7016ee193ad46c366bb655c639488520108b39dde228`.
