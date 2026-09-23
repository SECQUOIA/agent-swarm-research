# Independent review: executed cover preprocessing

Verdict: **PASS for the four stable normalization, independence, label, and
cache modules and their arithmetic-cost claims, their actual storage
counters, and original-input factor execution and copy/bit-work bounds.**
Basis initialization is covered by the separate
[basis-input review](basis-input-execution.md). The complete global
representation/control composition remains outside these local results.

Reviewed modules are `CoverNormalizationExecution`,
`CoverIndependenceExecution`, `CoverLabelCost`, and `CoverCacheCost`.
The appended eager dyadic runners in `DyadicScaleBits` and the actual
cache-to-DP integration in `CoverBitCost.trialBitRun` were also inspected.

## Actual arithmetic data flow

`runMatrix` executes each entry's `ArithmeticExpr.run` and stores its result
and events in a finite vector. Returned matrix entries and the flattened
event transcript are projections of those same stored runs. Subsequent
matrix indexing does not reevaluate expressions. `mulRun` and `inverseRun`
therefore materialize actual computed matrices, including totalized inverse
behavior on singular inputs.

`normalizeRun` sequentially stores the Gram matrix, its rational inverse,
the left inverse, range projector, normalizer, reconstruction matrix, first
matrix product, and final congruence. Each stage consumes stored preceding
results. The reconstruction matrix uses the returned scalar inverse runs.
The value lemmas identify these matrices with the original producers, while
`normalizeRun_events` identifies the complete concatenated arithmetic trace.
No supplied basis inverse, projector, or transformed atom is an input.

`independenceRun` computes the stored Gram determinant and uses both ordered
comparisons against zero to reject exactly the zero determinant. It handles
empty rank, dependent candidates, and non-square basis matrices without an
assumed independence premise. The exact event count includes Gram formation,
determinant evaluation, and both comparisons.

`atomRun` normalizes the actual atom, multiplies the cached projector by the
original atom, and tests range equality using two comparisons per matrix
entry. It also tests every normalized diagonal against `4*p`, including
equality at the boundary. Its accepted-code theorem matches the original
range and magnitude filter. Tests operate on returned arithmetic values;
there is no supplied acceptance flag.

`scalesRun` materializes the actual dyadic searches. `powerTwoRun`,
`dyadicSearchRun`, and `dyadicScaleRun` return the values their arithmetic
produced together with its events; the tested value drives the search branch.
`dyadicNormalizeRun` and the actual trial runner use those returned scales.

`labelRun` first stores every rational quotient, then floors those stored
quotients and retains the integer matrix. The upper-triangle labels project
that stored matrix. All `r^2` entries are evaluated and charged, including
the lower triangle that the DP does not need. Negative values use actual
mathematical floor, not truncation toward zero. The mesh is totalized at zero
at this low-level API; the cover's approximation proof supplies its strictly
positive mesh separately.

`trialRun` stores the prior and each edge's `AtomRun`, then computes labels
from the stored normalized edge atoms. It deliberately repeats normalization
once per atom; the cost includes all these calls. `CoverBitCost.trialBitRun`
passes these stored acceptance flags and labels into `outputCachedBitCounted`.
Thus the reviewed integration computes the DP inputs from the actual
preprocessing results, rather than evaluating a specification in parallel
with an unrelated transcript.

## Cost boundary

The local event-width lemmas cover intermediate rational products, inverses,
projector tests, normalized entries, and magnitude constants. At fixed
dimension the atom budget is linear in the original entry/weight width and
the arithmetic bound is cubic. The separate dyadic normalization bound is
degree four. `labelRunWork` charges quotient arithmetic plus an explicit
schoolbook signed-floor cost, and is bounded cubically in the combined
entry and mesh widths. `cacheWork_bound` sums the prior and all edge atoms,
then all edge labels. Scale construction and mesh formation are deliberately
charged by the caller, not this cache theorem.

These arithmetic theorems alone concern the declared rational primitive and
floor cost model. The final implementation composes them with explicit
storage, access and control charges, reviewed below and in the
[whole-cover review](whole-cover-execution.md). This boundary was reported
to the aggregate reviewers and cost author. In
particular, building a power transcript by repeated append copies a
quadratic number of list cells; a model that copies each rational payload
needs an additional width factor. The final local storage counters reviewed
below instead record actual cached scalar payloads and container operations.
Diagnostic arithmetic-trace allocation is explicitly outside that model.
The aggregate polynomial proof and its complete input integration passed the
separate whole-cover review. No claim about Lean VM timings follows from these bounds.

This implementation resolves the normalization execution concern recorded
in the earlier [bit-foundations review](bit-foundations.md): cached values
now drive subsequent operations. The separate global cost-model boundary
remains explicit.

## Targeted verification

- `lake build --wfail Formal.DAGSpectral.CoverNormalizationExecution
  Formal.DAGSpectral.CoverIndependenceExecution
  Formal.DAGSpectral.CoverLabelCost Formal.DAGSpectral.CoverCacheCost` passed.
- `topics/21-dag-spectral/verification/CoverPreprocessingReview.lean`, run with
  `lake env lean -DwarningAsError=true`, passed fifteen preprocessing
  assertions: nontrivial rectangular normalization and reconstruction,
  full trace equality, independent/dependent/empty-rank determinants,
  range rejection, closed magnitude cutoff, negative and exact floors,
  all-entry label charges, an actual dyadic scale, and cached-atom labels.
- Axiom inspection of `normalizeRun_events`, `atomRun_accepted_iff`,
  `trialRun_labels`, and `independenceRun_value` returned only `propext`,
  `Classical.choice`, and `Quot.sound`. No new axioms or admitted proofs
  were found in the reviewed four modules. No project-wide or CI checks
  were run.

Reviewed SHA-256 values:

| Module | SHA-256 |
| --- | --- |
| `CoverNormalizationExecution` | `330d4dc3ffc3292351754e9a9c60f99933878adcabe9653c1da56ef0caccb686` |
| `CoverIndependenceExecution` | `96339b1528bb032401af5a7406c114ffc3b7fb70a3e2a29d618317c601fe7e54` |
| `CoverLabelCost` | `8c21a9c5dc2d2133ddc77477a664a027c52676e88f9ea3a3202067ba5abb8fc0` |
| `CoverCacheCost` | `396b4fa89e2cb8b5ca8d4cbdfa901002dacc9fe21b3c0a2be3c5c83cec001e16` |

## Original-input factor execution

`FactorInputExecution` materializes every Schur matrix and every leading
factor column before recursive use. `StoredFactor` keeps rational vector
coordinates in a `Vector`; extending a recursive factor creates and charges
the new leading zero coordinate. `ldlRun_factors` and `ldlRun_events` identify
both the actual returned factors and their arithmetic charge list with the
earlier LDL specification, for arbitrary rational matrices. PSD is required
for the separate positive-factor/reconstruction theorem, not for this
execution identity. Empty dimension and zero pivots are handled explicitly.

The pivot branch tests exact equality with zero. Its extra `.compare` event
is a conservative cost charge, not an assertion that the ordered comparison
result decides equality on negative inputs. Following the review, the author
documented this distinction and charged the actual canonical-rational
equality digit scan separately in `copies`. This resolves the negative-pivot
execution concern without inserting an unnecessary PSD premise into the
value identity.

`inputRun` executes LDL once per owner, stores all results, tags the stored
factors, and flattens them in owner/local-factor order. `inputRun_indexed`
proves exact agreement with the original public integer labels. Zero owners
contribute no factors, and multiple factors from the same owner retain their
repeated owner label. There is no deduplication that could lose a forced
owner or factor. The raw prior is handled through the caller's owner-zero
convention.

`InputRun.factorAt` and `cachedLookup` accept an existing cache/list. Their
use does not run LDL again; the latter has an explicit linear scan counter.
The convenience identity `inputRunAt A k` itself calls `inputRun A` and must
not be used as an uncached runtime accessor. This integration concern was
reported to the author and root. The separate `FactorInputData` bridge was
inspected: its runtime fields use the supplied cache and its actual length,
while the original `producedData` appears only in erased proof fields.
The final bridge strengthens this to `InputRun.factorAtRun`, which returns
the record and visited-cell count from one actual `cachedLookup`. A proof of
membership extracts its result without a fallback. Its record equals
`factorAt`, and its counter is bounded by the actual cache length plus one.
The runtime owner, weight, and vector fields now use this counted accessor.
The [basis-input review](basis-input-execution.md) covers the corresponding
per-field access charges. Final whole-producer integration remains the
aggregate review's scope.

The final `FactorInputData` module also passed independent review. Its
`cachedFactorData_eq` identifies all runtime fields with the original
producer after a proof-only dependent-length cast. `cachedFactorData_bits`
derives weight and vector widths directly from original prior/edge bounds
and the cached-factor membership theorem. It does not assume supplied
factor widths or an input rank. `lake build --wfail
Formal.DAGSpectral.FactorInputData` passed, as did the independent
`topics/21-dag-spectral/verification/FactorDataReview.lean` runtime client checking cache length,
prior versus repeated edge owners, weights, and coordinates. Both bridge
theorems have only the three standard axioms. The reviewed module hash is
`0bdadcbbf9d0cb84e44b51a03b3aa7189bca326428fe57cde7e40bea91433737`.
The final accessor client additionally verified the actual four-cell
traversal to the last factor and its returned cached coordinate.
`InputRun.factorAtRun_steps` also has only the three standard axioms.

The copy charge uses actual signed numerator/denominator digit sizes for
stored scalars, vectors, matrices, factors, and owner tags. Induction bounds
recursive matrix scans, factor extension, tagging, and control. Original
matrix entry bounds imply factor and event widths `factorBits n B`, with
dimension-only factor `4^n`; no prebounded supplied factorization is assumed.
`InputRun.bitWork` charges an already materialized cache. The final bound
`inputBitWork_polynomial` is
`inputCoefficient n * (m+1)^2 * (B+1)^3` from original atom bounds.
This is the specified arithmetic-plus-copy model; it does not include a
claim that every diagnostic transcript allocation is a measured host-runtime
step.

The targeted command
`lake build --wfail Formal.DAGSpectral.FactorInputExecution` passed.
Its final reviewed SHA-256 is
`7e2f2e76361e0e031f5af2ff61314d16cefc6851e8351f7f1eb846a56b6d3001`.

The independent `topics/21-dag-spectral/verification/FactorInputExecutionReview.lean` client passed
fourteen runtime checks covering fractional Schur factors, actual trace
equality, zero and negative pivots, zero matrices, empty dimensions/owners,
repeated owners, exact flatten order, and cached lookup boundaries.
`inputRun_indexed`, `ldlRun_eq_instrumented`, and `inputBitWork_polynomial`
use only `propext`, `Classical.choice`, and `Quot.sound`.

The storage integration issue found during review is resolved. LDL now
composes the actual returned `S.copies` for the Schur/tail matrix and charges
both leading-column materializations plus their vector control. The
dimension-only `copySteps` recurrence was enlarged to
`copySteps n + 20*(n+2)^3`, and the original-input polynomial bound was
reproved. Exact runtime checks now include the full 33-unit storage count
for a one-dimensional negative pivot and the 9-unit zero-pivot case.
The final targeted build of `FactorInputData` and
`CoverIndependenceExecution` passed, rebuilding the corrected dependency.

## Actual cache storage counters

The final `RationalStorage`, updated `CoverNormalizationExecution`,
`CacheStorageExecution`, and updated `CoverIndependenceExecution` passed
independent review. Rational payload size is the actual absolute-numerator
digit count plus denominator digit count and one sign/tag unit. The basic
bound `2*B+1` applies to signed and zero values.

`runMatrix.copies` charges both stored result cells and projected matrix rows,
using the actual returned rational payloads, plus vector container control.
The normalization counter sums the counters for every computed intermediate
matrix and the actual inverse-scale vector. The atom counter adds the actual
projector-product cache and comparison flags. The label counter includes its
returned quotient cache, the actual signed integer floor payloads, and their
vector control. The trial counter sums its actual prior, edge, and label
counters, including all repeated normalizations.

`CacheStorageExecution` derives bounds for these returned counters from the
original entry/scale/mesh widths. Signed-floor storage uses the additional
integer digit allowed by the floor theorem. The final scaling lemmas are
linear in a common multiplier of all rational widths, for fixed dimensions
and atom count. The independence counter separately includes the cached
Gram matrix, returned determinant payload, and comparison/control flags.
Its bounds have no acceptance premise, so rejected candidates incur the
same gate-storage accounting before branching.

These counters cover stored output payloads and the declared container
operations. Arithmetic atom reads belong to the rational primitive model;
diagnostic event-list allocation is excluded as instrumentation. Concrete
factor-field access and basis initialization need their own scan accounting
and are not implied by these matrix-storage lemmas.

Targeted `lake build --wfail Formal.DAGSpectral.CacheStorageExecution`
passed. `topics/21-dag-spectral/verification/CacheStorageReview.lean` passed six runtime assertions
for nontrivial rational sizes, empty-row control, a negative floor, atom
storage composition, and inclusion of all child trial counters. Axiom
inspection of `trialRun_copies_le` and `trialStorageBudget_scale` returned
only the three standard axioms.

Final storage-module SHA-256 values:

| Module | SHA-256 |
| --- | --- |
| `RationalStorage` | `83fd93ad08b9b6a6d6ad58c2a70c17a5fc9391b16e0d03df0e749a04cafe732f` |
| `CoverNormalizationExecution` | `865277e07ffda4c1ec573a5722a9d91969e57885176a0683f4fe600fb5b1c6fc` |
| `CacheStorageExecution` | `977b42382b80de664577811881d3080a5024732176357c532593a5be3d4a5c75` |
| `CoverIndependenceExecution` | `11bdfbd6de59db1c05b6e114174566ca872fd115f91a63ea614e5477e9f4f306` |
