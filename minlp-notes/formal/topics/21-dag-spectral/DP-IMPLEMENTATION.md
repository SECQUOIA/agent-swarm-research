# Concrete profile dynamic program

The formal construction uses an explicitly indexed directed acyclic multigraph:
vertices are `Fin v`, edges are `Fin m`, and every edge satisfies
`src e < dst e`. Parallel edges retain distinct identities. An actual path is
a list of edge identities satisfying the inductive connectivity predicate.
The graph proofs give length at most `v-1`, no repeated edge, and the empty
path as the only path from a vertex to itself. An `allowed` Boolean predicate
implements a trial's edge filters without changing edge identities.

Raw vertex numbers need not already be topological. `kahnOrder` in `TopologicalSort.lean`
computes a topological list by repeatedly scanning for vertices with no
incoming edge from the remaining set and choosing the least numbered one.
For the usual acyclicity premise—no nonempty directed walk from a vertex
back to itself—the proof establishes that a ready vertex always exists.
The actual producer uses finite scans and finite minima, not the
well-founded minimum used in that existence proof. `topologicalOrder`
constructs a permutation from the computed list, with explicit list lookup
as its inverse. `checkDAGWithTopologicalOrder` connects it to input validation.

`rawPath_iff_ordered` in `TopologicalPath.lean` proves that reindexing the two endpoints
preserves exactly the raw path lists. Original edge identities, edge labels,
and owner requirements remain unchanged. The counted full-scan variant in
`TopologicalSortCost` returns the same order and performs at most `v²*m`
incoming-edge tests. Finite-set membership, numeric minimum selection, and
erasure add polynomial work on indices of bounded bit length; the test
count is not asserted to be the complete bit-operation count.

`ProfileDP.run` processes the vertices once in their given topological order.
At a vertex it forms only the extensions of representatives already stored
at predecessor vertices. It also includes the empty path at the source.
`representatives` keeps one actual path per owner-mask and signed integer
profile, using a finite list filter. It does not enumerate all feasible
paths and then select representatives from that enumeration.

The profile index is an arbitrary finite type, so a trial can use the actual
upper-triangular coordinate type directly. A mask is the intersection of the
required edge set with the path's edge set. `stateKey_extension` proves that
equal masks and profiles remain equal after the same extension. Every stored
object is a filtered feasible path; every feasible path has a representative
with the same state once its endpoint has been processed. The terminal
filter keeps exactly representatives with the complete required-edge mask.

The principal contracts are:

- `run_sound`, `run_complete`, and `run_unique` for the actual table.
- `output_sound` and `output_complete` for actual returned paths.
- `output_nil_iff` for exact detection of no eligible path.
- `output_self` for the source-equals-sink case, including required owners.
- `edgeExtensions_eq_generated` equating the extension counter with the
  lengths of the candidate extension lists actually formed by vertex steps.

For a coordinate window with `C` integer values, `d` coordinates, and `r`
required owners, put `B=2^r C^d`. The implementation proves at most `B`
retained states per vertex, `vB` retained table states, `mB` edge extensions,
and `B` terminal representatives. `ProfileSpectralDP.spectral_dp_bounds`
instantiates this with the exact source value
`C=ceil(8*p*r*N^2/eta+N)+2`, provided the retained arc entries have magnitude
at most `4p` and `N>=v-1`, `N>0`. The label producer rounds negative entries
with the ordinary integer floor. `output_coordinate_close` connects an
actual returned representative to the coordinate-sum error `N*h`.

These state counts are not a tight memory bound for the simple list
implementation. It materializes one vertex's candidate list before merging,
whose length is at most `1+mB`. Its retained table has at most `vB` entries;
the transient candidate buffer adds polynomial working storage. Storing
whole paths adds their length, at most `N`, to the storage and copying cost.

`ProfileDPExecution` supplies a concrete full-scan counted implementation.
`compareAllCounted` evaluates each key comparison and counts it;
`representativesCounted_spec` proves that its selected list is exactly the
original representative filter and its count is the comparison budget.
`runCounted_table` and `runCounted_final_cost` lift these identities to the
entire table producer. `outputCounted_spec` identifies its returned terminal
paths and comparison count with the existing output and budget. Thus the
budget has an operational connection to a proved equivalent producer, rather
than being only a formula on candidate-list lengths. Terminal owner tests
and arithmetic inside key evaluation remain separate charges.

The implementation also scans the explicit edge list to form incoming lists
at each vertex. Its representative filter uses list comparisons rather than
an optimized dictionary. `ProfileDPCost.comparisonBudget_bound` bounds the
charged key comparisons by `v*(1+mB)^2`; the budget charges every element of
a representative-list test even if Boolean evaluation could stop early.
A key evaluation recomputes the mask and integer profile from the stored
edge list. These are additional polynomial operations; the formal statement
does not equate edge extensions with total bit operations or claim an
optimized dictionary implementation.

The graph and integer-profile algorithm definitions are computable. Real
floor labels in the analysis wrapper are connected to exact rational floors
by the separate rounding lemmas. The finite-state counting proof uses
classical finite-type instances only in its proof, not as an instruction
for producing representative paths.

`BasisInputExecution` constructs each trial's actual input cache. It scans
identifiers in increasing order, tests membership by a full scan of the
candidate, and copies the selected columns, weights, and owners. The owner
set comes from an already distinct output list, so its construction needs no
second duplicate-removal pass. Every finite identifier range is produced by
`finRangeCounted`. Empty candidates still pay the identifier and branch scans.

Scalar copies use their actual numerator and denominator bit lengths. Each
column coordinate also pays `(M+p+2)^2` for source lookup and binary index
control; the weight and owner each pay a source lookup. The original cached
factor input implements those accesses through `factorAtRun`, whose actual
list traversal has at most `M+1` steps. The computed field value is bound
once before its payload is copied. `basisRun_columns`, `basisRun_weights`,
and `basisRun_required` identify these caches with the original trial
semantics; `basisRun_work` bounds the accumulated work by an explicit
polynomial.

`trialBitRun` consumes that cache and accumulates the scale and mesh traces,
normalization and label-cache storage, and the DP counter. The cached DP
charges each label access in the comparison that performs it.
`trialDP_labelAccessCount` bounds those accesses, while `trialLabel_readWork`
proves that the per-read charge covers the computed signed integer digits
and the three cache indices. Its bound uses
explicit input bit widths. `trialBitRun_length` bounds the actual returned
list, including the prior-rejection branch. No synthetic trial setup charge
is used in the producer.

Targeted implementation checks, run from `formal/` with the Elan toolchain
on `PATH` and `LEAN_NUM_THREADS=1`:

```text
lake build --wfail Formal.DAGSpectral.ProfileSpectralDP Formal.DAGSpectral.ProfileDPCost
lake build --wfail Formal.DAGSpectral.ProfileDPExecution
lake build --wfail Formal.DAGSpectral.TopologicalPath
lake build --wfail Formal.DAGSpectral.BasisInputExecution
lake build --wfail Formal.DAGSpectral.TrialBitCostBound
lake env lean /tmp/Topic21DPSmoke.lean
lake env lean /tmp/Topic21TopologicalSmoke.lean
lake env lean /tmp/Topic21BasisSmoke.lean
lake env lean /tmp/Topic21TrialCostAxioms.lean
```

All final checks passed. The DP smoke client used kernel-checked `decide` examples on a
four-edge diamond to check signed cancellation, owner-mask preservation,
unreachable output, the empty source-to-source path, and rejection of an
impossible owner requirement. Selected soundness, completeness, count, and
cost declarations used only `propext`, `Classical.choice`, and `Quot.sound`.
The topological client checked a graph whose numeric labels run backwards,
its computed permutation and explicit inverse, the counted scan total,
isolated vertices, the empty graph, termination on a cyclic input, and a
raw path witness. These are implementation checks; independent review is
recorded separately.

The basis smoke client checked sorted label output from an unordered subset,
empty-candidate scan work, duplicate owners, and complete scans after an
owner match. Its semantic and work declarations passed the standard-axiom
audit. The source reviewer separately checked the actual cached factor input.
