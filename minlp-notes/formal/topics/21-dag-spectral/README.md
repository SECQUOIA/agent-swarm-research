# DAG spectral approximation sets

Status: complete. All 33 frozen claims are proved in 124 Lean modules,
independently reviewed, and verified by the targeted checks recorded below.
Topic 21 verifies a deterministic rational construction
of finitely many feasible paths that approximate every PSD information sum
on an explicit DAG in both relative PSD directions. Singular ranges must be
preserved exactly. The scope includes the actual algorithm, cardinality and
Turing bit bounds, criterion consequences, and conditional sandwich transfer.

- [Frozen claims](CLAIMS.md).
- [Independent source inventory](SOURCE-REVIEW.md).
- [Coverage](COVERAGE.md).
- [Review record](REVIEW.md).
- [Targeted verification](VERIFICATION.md).

Proofs are in [Formal/DAGSpectral](../../Formal/DAGSpectral/).

The original-matrix interface is
[`dagSpectralCover`](../../Formal/DAGSpectral/Headline.lean). Its input graph
has verified topological vertex indices; the rational PSD matrices may be
singular. The returned set covers every feasible path in both relative PSD
directions, preserves kernels for `0 < eta < 1`, and satisfies the exact
rank-by-rank cardinality bound. It returns the empty set exactly when no path
exists. The [`rawDagSpectralCover`](../../Formal/DAGSpectral/RawHeadline.lean)
wrapper computes a topological ordering for arbitrary vertex numbering while
preserving the original edge identifiers.

[`CoverWholeExecution`](../../Formal/DAGSpectral/CoverWholeExecution.lean)
connects a counted list implementation to this same returned set.
[`coverInputRun`](../../Formal/DAGSpectral/CoverInputExecution.lean) executes
and stores the original LDL factors once, then returns that same list with
its measured work. `coverInputRun_polynomial_work` bounds the work using
only the original matrix and accuracy encodings and explicit graph size.
[`CriterionSelectHeadline`](../../Formal/DAGSpectral/CriterionSelectHeadline.lean)
applies the criterion selectors to the produced paths. Exact E comparisons
use a computed characteristic-polynomial separation bound, including equal
and repeated eigenvalues. Contrast calculations use an executable rational
Moore–Penrose inverse and exact estimability tests.

The cost model charges schoolbook rational and integer arithmetic, finite
scans, dictionaries and witness copying. It does not claim a wall-clock bound
for Lean's compiler or runtime. Dimension-dependent constants and exponents
can be large; this is a fixed-dimension complexity result, not a practical
solver or a dimension-independent FPT bound. The costed cover core takes the
verified ordered graph. The additional raw topological wrapper has separate
ordering and endpoint-scan counts, not a claimed full bit-cost theorem for
Lean's topological-sort implementation.

The conditional transfer assumes a separately supplied uniform finite-memory
PSD sandwich. Stochastic locality estimates and construction of that upstream
graph are excluded. The represented-matroid extension belongs to topic 22.

The primary
[source note](../../../notes/research-20260912-dag-psd-approximation-set.md)
and [correlated-measurements paper](../../../paper-correlated-measurements/README.md)
were updated to match the verified scope. Topic 22 and later topics remain
queued. No project-wide verification or CI inspection is run locally.
