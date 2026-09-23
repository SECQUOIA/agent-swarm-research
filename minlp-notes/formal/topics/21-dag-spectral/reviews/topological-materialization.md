# Independent review: cached topological endpoints

Verdict: **PASS for `TopologicalMaterializeCost.lean` and its stated scan-work
boundary.** The earlier topological sorting and raw-input headline review is
separate. This module does not claim full raw-graph bit complexity.

`topologicalIndexScan` returns the first occurrence, or the list length if
absent. Its counter includes the final empty-list test, so the uniform bound
is `length+1`. `topologicalEndpointScan` executes both endpoint scans for each
edge and charges one additional step per endpoint pair plus the final empty
case. Substitution of the proved topological-list length gives the advertised
`m * (2*(v+1)+1) + 1` bound.

`materializedTopologicalGraph` computes one topological list and stores the
two reordered endpoints of every original edge in a vector. The local rank
function is a scan over the cached list, not a precomputed vector of all
vertex ranks. Subsequent graph endpoint access reads the stored endpoint
vector and does not rerun sorting. Edge identity is preserved, including
parallel edges. The proof of `materializedTopologicalGraph_eq` establishes
equality of the complete `ExplicitDAG` with the earlier graph definition,
using equality of both endpoint functions and proof irrelevance.

The scan counter executes the same endpoint-indexing procedure on a list of
edge indices. It is not a cost-returning version of the entire graph
constructor: sorting, allocation, copying bit strings, and comparison/index
bit costs remain outside this counter. This matches the module's explicit
documentation. No inference of a full bit-work theorem from this scan count
is justified or needed for the stated lemma.

Targeted verification:

- `lake build --wfail Formal.DAGSpectral.CriterionSelectWeighted
  Formal.DAGSpectral.TopologicalMaterializeCost` passed.
- `topics/21-dag-spectral/verification/TopologicalMaterializationReview.lean`, run with
  `lake env lean -DwarningAsError=true`, passed seven runtime assertions:
  a reverse-numbered three-vertex DAG, exact reordered edges, the scan bound,
  stored endpoint access, an absent index, duplicate-list first occurrence,
  and empty edge input. The acyclicity proof was checked by ordinary Lean
  tactics, not supplied as an unchecked runtime assertion.
- Axiom inspection of `materializedTopologicalGraph_eq` and
  `topological_materialization_scan_bound` returned only `propext`,
  `Classical.choice`, and `Quot.sound`. No project-wide or CI checks were run.

Reviewed SHA-256:
`d40a1e2397b3196efead9678d5b2c8e7042ddf8319986752fa4604c7aeb38a2e`.
