# Independent review: profile dynamic program

Reviewed `Graph`, `Profiles`, `ProfileDP`, `ProfileDPBounds`,
`ProfileSpectralDP`, `ProfileDPCost`, and `ProfileDPExecution`. The reviewer did not author these
modules. Also inspected the coordinate-window arguments in `ProfileCount`
and the actual Batteries implementation of `List.pwFilter`.

Verdict: **PASS** for the graph and profile algorithm, feasibility,
completeness, retained-state and generated-extension counts, and spectral
coordinate-error bridge. The comparison-budget inequality and its linkage to the concrete counted
producer are also proved. This review does not certify the final all-trials
producer or the full rational bit-work assembly.

## Executed algorithm and path semantics

`ExplicitDAG` retains edge identities, including parallel edges, and requires
every edge to advance the given vertex order. The reviewed module assumes
that order as input; construction or validation of it for an unindexed DAG
is a separate part of G01. The path predicate stores the actual ordered edge
list. Its length is at most `v-1`, and its edge list has no duplicates.

`run` processes vertices in topological order. A vertex's candidates are the
empty source path, when appropriate, and extensions of representatives
already stored at predecessor vertices. The algorithm does not generate the
family of all feasible paths before merging. The edge predicate is tested
before extension and preserves original edge identities.

`representatives` is a list filter that retains original objects. Its mapped
keys are exactly the deduplicated input keys. Thus no witness is invented,
no reachable key is lost, and every stored key has one representative.
The mask records the intersection of required edge owners with the actual
path's edge set. Prior-only owners must be handled by the caller, rather
than inserted as fictitious graph edges.

`stateKey_extension` proves that equal masks and signed profile sums remain
equal after a common next edge. `candidates_complete` and `run_complete`
apply this fact to each actual path's last edge. The replacing prefix ends
at the required predecessor, and the extension uses that edge's actual
source. This supplies continuation one edge at a time; it does not assume
an arbitrary concatenation of simple paths is feasible. Strictly increasing
vertex indices and the proved path edge bounds preclude a repeated-edge or
repeated-vertex conflict with the remaining suffix. No path-length field is
needed in the state.

The final owner filter is exact. `output_sound` returns an allowed path with
all required owners. `output_complete` covers every allowed path satisfying
that requirement. `output_nil_iff` detects precisely the absence of such a
path. `output_self` returns `[[]]` for empty owner requirements and `[]`
otherwise. A topologically indexed zero-vertex graph has no source or sink
inhabitant; the two-vertex no-edge case is covered by the boundary client.

## Counts and rounding bridge

The state encoding consists of a subset of the required owners and one
integer from the common coordinate window per profile coordinate. Its
cardinality is exactly `2^required.card * window.card^card(kappa)`.
Injectivity follows from the actual list's unique keys. Bounds apply to
every intermediate table, not only to a supplied terminal certificate.

`edgeExtensions_eq_generated` equates the extension counter with the sum
of actual candidate-extension list lengths at their destination steps.
Each allowed edge is counted with the number of representatives stored at
its source when its destination is processed. Thus `m*B` bounds generated
edge extensions rather than all paths or an unrelated counting model.

The spectral wrapper uses signed floors, permits negative coordinates and
different path lengths, and derives the precise coordinate count
`ceil(8*p*r*N^2/eta+N)+2`. It requires positive rank, positive mesh tolerance,
positive `N`, and `N>=v-1`. Zero-rank handling belongs to the separate branch.
`output_coordinate_close` combines actual output completeness and soundness
with the residual bound to give strict entrywise error below `N*h`.
The common prior remains outside the rounded edge-label sum.

The retained table has at most `v*B` paths, but this is not the total memory
of the list implementation. The candidate list can have `1+m*B` paths.
`DP-IMPLEMENTATION.md` correctly accounts for this additional buffer, whole
path storage/copying, scans of the explicit edge list, and key recomputation.
It does not mislabel the extension count as total Turing work.

## Comparison execution linkage

The initial review found that the comparison budget was defined separately
from execution. `ProfileDPExecution` now closes that gap. Its concrete
`compareAllCounted` scans every retained-tail element and returns both the
Boolean result and the exact number of key comparisons. The proof equates
this result to the membership-based predicate and the tail length.

`representativesCounted_spec` proves both output equality with the original
`pwFilter` representatives and exact equality of its count to
`representativeComparisonBudget`. `runCounted_table` carries that equality
through the actual vertex recurrence; `runCounted_final_cost` identifies the
returned count with `comparisonBudget`. `outputCounted_spec` preserves the
actual final path list and count. The proved quadratic bound therefore
bounds an explicitly defined producer's dictionary comparisons, not just a
separate accounting expression. Terminal mask tests and key evaluation
costs remain separate, as the code and implementation notes state.

The counted implementation deliberately performs a full scan even when an
early comparison already fails. This is a valid implementation choice; the
claim is about that producer and does not assert an exact short-circuit
comparison count for another backend. The independent client checks a
repeated-key case with five comparisons and the complete path producer's
one-comparison and zero-comparison boundary cases.

## Independent targeted checks

From `formal/`, with Elan on `PATH` and `LEAN_NUM_THREADS=1`:

- `lake build --wfail Formal.DAGSpectral.ProfileSpectralDP Formal.DAGSpectral.ProfileDPCost` — passed.
- `lake build --wfail Formal.DAGSpectral.ProfileDPExecution Formal.DAGSpectral.NormalizationComplete Formal.DAGSpectral.GraphInput Formal.DAGSpectral.RangeObstruction` — passed (the latter three also support the separate normalization review).
- `lake env lean topics/21-dag-spectral/verification/ProfileDPReview.lean` — passed.

The client is preserved as
[`verification/ProfileDPReview.lean`](../verification/ProfileDPReview.lean).
Its kernel-checked `decide` examples cover parallel edges with identical
profiles, required-owner distinctions, impossible owner combinations,
disallowed edges, backwards-unreachable sinks, signed cancellation across
different path lengths, exact extension and comparison counter values,
unprocessed future vertices, and no-edge source-equals-sink behavior.

The client also printed axioms for completeness, exact generated-extension
count, returned-coordinate closeness, and the comparison-budget bound.
Only `propext`, `Classical.choice`, and `Quot.sound` were reported. No
project-wide checks or CI inspection were performed.
