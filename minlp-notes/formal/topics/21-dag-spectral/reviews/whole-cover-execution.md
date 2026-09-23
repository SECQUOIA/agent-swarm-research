# Independent review: all-trials cover execution

Verdict: **PASS for the complete original-input cover runner and its C05
aggregate schoolbook work bound. All findings from this review are resolved.**
The reviewer did not author the cover execution or aggregate-cost modules. Earlier rational factorization and
factor-range mathematics authored by this reviewer are outside this
independent review; their separate review is required.

## Enumeration and returned paths

`CoverExecution` executes include/exclude recursion for fixed-cardinality
sublists. Its output equals `List.sublistsLen`; its length is the binomial
coefficient, including zero cardinality and cardinalities exceeding the
input length. `CoverEnumerationCost` derives a polynomial bound with a
coefficient depending only on cardinality. It does not enumerate all subsets
and filter by cardinality afterward. `candidateBasisList_toFinset` proves
that the actual produced subset list covers exactly the intended candidates.

`candidateBitRun` executes the Gram independence gate and charges rejected
candidates too. `rankBitRun_paths` identifies the union of actual returned
paths with the semantic trial union. `collectRuns` explicitly runs each
candidate and copies its path list into the output. Its length and cost
bounds concern these actual results, with path lengths obtained from path
soundness rather than an assumed output encoding size.

The zero branch executes and stores all original atom-zero tests, then uses
the zero-coordinate DP and retains at most one path. The full producer
handles source equal to sink by returning the empty path, otherwise executes
the zero branch and every positive rank through `p`. Its final deduplicator
compares actual ordered edge lists. `dedupCounted_value` proves equality with
list deduplication, and `coverBitRun_paths` identifies the resulting set with
`spectralPathSet`. Parallel edge identities are preserved; only identical
edge lists are removed.

`CoverLoopCost` combines actual branch work, path copying, concatenation,
and full-scan deduplication. Its current generic theorem assumes bounds for
the zero and rank branches. This is a valid aggregation lemma, but its
premises must be discharged from the original rational input before it
constitutes the final complexity result.

## Original-input cache bridge inspected

`coverInputRun` executes `inputRun` once on the prior and all atoms, binds the
result, and builds its `FactorData` view from that cache. The runtime owner,
weight, and vector fields of `cachedFactorData` use the executed lookup
`cache.factorAtRun`, whose value is proved equal to `cache.factorAt`.
`producedData`, dependent-length casts, and the semantic LDL label count
occur only in correctness proofs; they do not cause each runtime read to
repeat the factorization. The actual cached list length controls enumeration.

`coverInputRun_paths` identifies the returned set with `dagSpectralCover`;
`coverInputRun_isRelativeCover` applies the established cover theorem to it.
The working width is derived from original atom encodings, accuracy encoding,
dimension, and explicit graph size. `coverInputRun_work` combines the actual
LDL work with the all-trial bound. `coverInputRun_list` also preserves the exact output list under the cached
factor-data replacement. These final interfaces passed independent review
and targeted checks.

## Representation accounting inspected

The initial rank counter omitted explicit construction of `List.finRange M`.
The revised loop uses `finRangeCounted`, weights the executed sublist
recursion by `M+1` for identifier work, and uses `subsetsCounted` for actual
conversion to candidate sets. `subsetCounted` constructs a finset directly
from the list proved distinct by the executed membership tests, so no hidden
second duplicate-removal pass is introduced. The outer rank list is also
constructed by `finRangeCounted`. These charges remain present when a rank
exceeds the number of labels and produces no candidates.

Initially, a dependent candidate bypassed the trial setup charge even
though its independence gate still read basis labels and constructed Gram
matrices. The revised `candidateBitRun` executes `basisRun` before the gate
and charges both its work and `gate.copies` on either branch. A successful
trial may construct its basis again, but that second construction is charged
again. The trial itself binds its actual matrix/label cache and charges its
copy counter; it does not treat a successful gate as free cache construction.

`ProfileDPCacheExecution` extends the actual weighted comparison recurrence
with one cache-read charge for each coordinate read from each compared path.
Its exact cost decomposition is the prior DP cost plus
`labelAccessCount * R`, and it preserves the actual terminal output. This
provides the operational linkage for repeated cached-label indexing; merely
precomputing label arithmetic once would not have supplied that charge.

The source-execution reviewer separately reviews matrix/factor arithmetic,
cache storage, and their operand bounds. This aggregate review checks that
those counters are included in every relevant branch. The final producer and bound include these counters in all branches.
No mathematical or accounting issue remains from this aggregate review.

For fixed `p`, the rank sum has fixed length, all subset exponents are bounded
by `p`, and the label count is at most `p*(m+1)`. Factorization widths are
linear in input encoding width with a coefficient depending only on `p`.
The uniform profile capacity is polynomial in explicit graph size and
`ceil(1/eta)` with dimension-dependent exponent. The branch bounds, loop
aggregation, path copying, and quadratic output deduplication preserve this
fixed-dimensional polynomial regime. `coverWorkBound_mono_labels` proves the needed monotonicity in label count;
`coverInputRun_polynomial_work` substitutes `p*(m+1)` explicitly. Its final
`originalInputWorkBound` depends only on original input dimensions, encoding
widths, and accuracy. No supplied factorization, successful trial, profile
window, or branch-work bound remains as a premise. This is a schoolbook
operation-model bound, not a theorem about the Lean compiler's runtime.

## Runtime observer finding and repair

A positive-rank original-input smoke check initially overflowed the stack.
The cause was evaluation of the cost observer: an inherited schoolbook
multiplication-cost expression built a list over every position in a very
loose width budget. The producer's cost is now evaluated through
`primitiveBitCostClosed`. `primitiveBitCost_closed` proves equality of the
entire old and new functions for every operation, operand, and width, using
existing multiplication/division cost identities. Its `csimp` compiler
rewrite therefore preserves the mathematical charge exactly and does not
change paths or introduce an axiom. Independent review checked that equality;
the positive-rank test now passes with the ordinary stack setting.

## Targeted checks

From `formal/`, with Elan on `PATH` and `LEAN_NUM_THREADS=1`:

- `lake build --wfail Formal.DAGSpectral.CoverLoopCost` — passed during the initial loop review.
- `lake build --wfail Formal.DAGSpectral.CoverInputExecution` — passed for the final original-input assembly.
- `lake env lean topics/21-dag-spectral/verification/WholeCoverReview.lean` — passed.
  The client covers bounded subset enumeration, empty/oversized cardinalities,
  path comparison, duplicate removal, candidate concatenation, and the actual
  whole producer with zero input matrices: one parallel-edge representative,
  the empty source-to-source path, and no output for an unreachable sink.
  It also executes `coverInputRun` from original zero matrices and from two
  equal positive unit atoms, checking that distinct edge owners both survive
  the positive-rank trials. Runtime checks use `#eval` assertions, not native
  proof declarations. The ten printed theorem axiom sets contain only
  `propext`, `Classical.choice`, and `Quot.sound`. The final runtime log is
  `/tmp/topic21-whole-cover-review.log`.

No project-wide checks or CI inspection were performed.
