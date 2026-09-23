# Independent review: local DP bit charges

Reviewed `ProfileBitCost`, `AlgorithmBitCost`, `SpectralAlgorithmCost`, and
`ProfileDPBitExecution`. The reviewer did not author these modules.

Verdict: **PASS for the reviewed local schoolbook charge, output equivalence,
operand widths, and the derived polynomial bound. Both implementation-
accounting issues identified in the initial review are resolved below.** This review does not cover the all-trials
source-operation bound or certify the Lean compiler's runtime.

## Proved local contracts

`compareAllBitCounted` performs a full comparison scan and sums its
operand-dependent charges. `representativesBitCounted_spec` proves both the
selected-list equality and exact equality with `representativeBitWork`.
The weighted vertex recurrence uses the same candidate lists as the original
DP, without enumerating all feasible paths. `runBitCounted_table` and
`outputBitCounted_paths` establish exact returned-path equality.
`outputBitCounted_work` bounds the actual accumulated charge by `dpBitWork`;
it does not define the producer's returned charge to be that upper bound.

Key charges include recomputing both integer profiles on each comparison,
comparing their integer coordinates, and a quadratic owner-mask budget.
Sequential integer addition charges use the actual operand sizes. Their
bounds grow with the actual path length, subsequently bounded by the DAG's
vertex count. No unit-cost rational arithmetic or dictionary lookup is
used in these expressions. Copying generated paths is charged by their
length and edge-identifier size; the exact generated-extension theorem
connects the aggregate to the actual candidate lists.

Rational floor labels have a derived width `F+E+r+N+3`, using the exact
rational mesh. Negative floors are covered. The profile-window theorem is
applied to allowed paths with the retained-entry bound and `N >= v-1`;
it is not a supplied finite-window certificate. The state capacity uses
the actual owner bound and the source coordinate count, followed by the
polynomial upper bound in `ceil(1/eta)`. The theorem requires positive rank,
mesh tolerance, and `N`; the separate rank-zero branch is outside this review.

The algorithm definitions are computable for supplied finite integer labels.
Real casts and real floors appear in proof bridges, while the spectral
instance uses rational division and integer floor. The local theorem still
requires the retained-entry magnitude and source rational bit bounds;
the global normalization assembly must derive them for its actual input.

## Accounting fixes verified

The initial terminal predicate constructed `es.toFinset` while charging a
linear scan of required owners. The producer now calls `terminalOwnerCheck`,
which directly tests each required owner for membership in the original
path. `terminalOwnerCheck_eq` proves equivalence to the former mask test,
and `outputBitCounted_paths` preserves the original output theorem.
The `Finset` decidable bounded universal instance scans the required set;
it does not enumerate every ambient edge or construct a path finset.
The charge `(required.card+1)*(path.length+1)*(m+1)` covers that scan,
including empty owner requirements and empty paths.

The table uses nested `Function.update` closures, so a predecessor lookup
can traverse up to `v` updates and compare vertex identifiers at each step.
The control charge now includes an additional graph-size factor:
`(m+1+v)*(v+m+1)^2` per vertex. The aggregate in `dpBitWork` and
`dpWorkPolynomial` is `(v*(m+1)+v*v)*(v+m+1)^2`. This conservative allowance
covers both the chain traversal and the identifier comparisons, as well as
the edge scan and update control. The change is propagated through the
counted producer and its polynomial bounds; it does not assume a unit-cost
random-access array. It preserves the fixed-dimensional polynomial regime.

The full-scan key comparison already budgets profile recomputation and
quadratic list-based mask operations. Candidate copying is accounted for
separately. These inspected local operations have no remaining accounting
issue from this review.

The cost instrumentation itself is an analysis device. Arithmetic needed
only to compute a reported cost counter is not counted as work of the
uninstrumented producer. The results are about the stated schoolbook
operation model, not a proved bound on the compiler's binary.

The global implementation must also specify whether rational labels and
trial acceptance are cached. `labelPreprocessingBitWork` is appropriate for
materialized labels; an arbitrary function argument does not establish that
materialization. `labelAccessCount` and `uncachedDPBitWork` explicitly offer
a charge for repeated source-label calls. The global review must choose and
justify its actual evaluation strategy, including repeated edge filters.

## Targeted checks

From `formal/`, with Elan on `PATH` and `LEAN_NUM_THREADS=1`:

- `lake build --wfail Formal.DAGSpectral.ProfileDPBitExecution` — passed.
- `lake env lean topics/21-dag-spectral/verification/DPBitCostReview.lean` — passed.

The independent executable client checks parallel paths, owner preservation,
an impossible required-owner set, weighted full scans after an early false
comparison, signed negative floor, the returned-work inequality, and empty/full/missing
terminal-owner checks.
The four principal printed axiom sets contain only `propext`,
`Classical.choice`, and `Quot.sound`. No project-wide checks or CI inspection
were performed.
