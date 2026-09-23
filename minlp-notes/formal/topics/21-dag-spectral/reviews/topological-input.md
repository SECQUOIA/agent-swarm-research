# Independent review: raw DAG input and topological ordering

Verdict: **PASS for computed ordering, preservation of the original paths and
matrix data, the raw-input cover conclusions, and the stated incoming-edge
scan count.** These modules do not prove a total bit-operation bound for raw
DAG preprocessing. The C05 cover-cost theorem uses an explicitly ordered DAG;
`checkDAG` can verify that representation by checking every edge.

Reviewed sources: `TopologicalSort`, `TopologicalSortCost`, `TopologicalPath`,
and `RawHeadline` in `formal/Formal/DAGSpectral/`. This reviewer did not author
or edit those sources.

## Actual computation and input assumptions

`RawAcyclic` excludes a nonempty directed cycle in the actual endpoint relation.
It is the correctness theorem's input-domain assumption. The executed Kahn
algorithm does not query that proposition or receive a topological-order
oracle. It computes the ready vertices by finite edge tests, selects the least
ready vertex, erases it, and continues for at most `v` rounds.

The finite well-foundedness argument appears only in the proof that an
acyclic nonempty remainder has a ready vertex. `kahnOrder_spec` proves no
repetitions, exact vertex coverage, and strictly increasing position along
every edge. `topologicalOrder` constructs the permutation using `idxOf` and
list lookup; there is no chosen inverse or supplied permutation. Its forward
property is then checked through the existing finite `checkDAGWithOrder`
interface. Isolated vertices and the empty graph are covered. The modules do
not state a complete Boolean cycle-recognition theorem; this is not needed
for their acyclic-input correctness statements.

## Edge identities and the original-input cover

`RawPath` and `ExplicitDAG.Path` use the same snoc construction on
`List (Fin m)`. `rawPath_iff_ordered` changes only vertex labels. The edge list
is unchanged in both directions, so parallel edges remain distinct and the
same path-information sum is evaluated. The length and no-repeated-edge
results follow from the computed ordered graph.

`rawFeasiblePaths` is a finite semantic domain, not an enumeration performed
by the cover algorithm. `mem_rawFeasiblePaths` identifies it exactly with
`RawPath`. `rawDagSpectralCover` supplies the computed permutation and original
`Q0` and `Q` to the established cover algorithm. Its relative-cover, empty
output, kernel-preservation, and cardinality theorems are valid direct
instantiations; their tolerance and PSD hypotheses match the underlying
headlines. The kernel theorem retains `0 < eta < 1`, and the other cover
conclusions retain `eta > 0`.

## What the counter proves

`incomingScan_spec` relates the executed scan to the conjunction over its
actual edge list and proves its count equals that list's length.
`readyVerticesCounted_spec` proves the returned ready set and exactly `v*m`
incoming-edge tests per full scan. `kahnOrderCounted_order` identifies the
counted output with the actual Kahn output. Therefore
`topologicalSort_scan_bound` gives at most `v^2*m` incoming-edge tests, even
when the graph is cyclic or empty.

An incoming-edge test contains an endpoint equality and a finite-set
membership test. The count does not additionally count comparisons inside
membership, filtering, minimum selection, erasure, permutation lookup, or
endpoint-table construction. In particular, the original permutation's
function body refers to `topologicalList`; an additive one-time preprocessing
bit-cost claim requires explicit caching/materialization or accounting for
repeated evaluation. This boundary was reported to the root and author.
A separate `TopologicalMaterializeCost` helper was added by this reviewer;
it is not part of this independent review and does not turn the scan count
into a complete raw-preprocessing bit theorem.

## Targeted checks actually run

From `formal/`, with `PATH="$HOME/.elan/bin:$PATH" LEAN_NUM_THREADS=1`:

- `lake build --wfail Formal.DAGSpectral.TopologicalSort Formal.DAGSpectral.TopologicalSortCost Formal.DAGSpectral.TopologicalPath`: passed.
- `lake build --wfail Formal.DAGSpectral.RawHeadline`: passed.
- `lake env lean topics/21-dag-spectral/reviews/artifacts/topological-input.lean`: passed; the retained log records the axiom checks and runtime output.

The artifact checks an arbitrarily numbered three-vertex path: the computed
order is `[2, 0, 1]`, its forward and inverse positions compute correctly, the
same edge list `[0, 1]` transports to the ordered graph, and the counted run
performs 18 edge tests. It also checks a self-loop, isolated vertices, and the
empty graph. Audited declarations use only `propext`, `Classical.choice`, and
`Quot.sound`. No project-wide verification or CI inspection was performed.
