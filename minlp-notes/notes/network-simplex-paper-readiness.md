# Sparse network–simplex hulls: paper-readiness record

**Historical closeout, superseded by the manuscript.** The current account is
[the paper](../paper-network-simplex/main.pdf), with
[source and evidence entry points](../paper-network-simplex/README.md).
Manuscript development sharpened the flat-chain result to unit flow/product
coefficients through three observed labels (failure at four), with five tests
at two labels and 16 circuits at three, and reduced the sharp K4 example to
five products. Stronger fixed-weight and positive-state LP baselines also
changed the practical conclusions: global state merging is often fastest,
and earlier long-chain boundary speedups do not survive these controls.
The original numbers and assessments below are preserved as historical
evidence; they are not the current manuscript's claims.

Date: 2026-09-07. Status: continuation complete. All retained mathematical results,
implementations and computational studies passed independent internal review;
root integration checks passed. This is a research closeout, not a manuscript
submission or journal peer-review claim.

## Assessment

The continuation now supports a coherent paper about how observation patterns
and network structure control exact sparse hull representations. It contains
constructive algorithms, sharp structural boundaries, complete implementations,
and honest computational comparisons. General simplex disaggregation and
polynomial hull separation were already known and are not claimed as discoveries.

The most practical default emerging from the tests is a compressed exact extended
formulation. Exact original-variable separators serve two additional purposes:
they provide rational certificates, and the fixed-state flat-chain specialization
can avoid constructing a large state-flow LP. Neither fewer variables nor an
exact cut oracle automatically implies faster optimization.

## Retained results and evidence

| Development | What is established | Proof and review |
|---|---|---|
| Sparse general-graph extended hull | Blockwise state merging and cycle/path compression use `sum r_B a_B` additional variables. The observation-sensitive refinement uses only `sum rho_Bj`, where `rho_Bj` is the cycle rank of the arcs unobserved by label `j` in block `B`. | [Base proof](network-simplex-reopened-compressed-hull.md), [refined proof](network-simplex-observed-rank-elimination.md), [base review](review-network-simplex-reopened-compressed-hull.md), [refinement review](review-network-simplex-observed-rank-elimination.md). |
| Forest-complement original hull | If every active label's unobserved subgraph is a forest, no additional variables are needed, on arbitrary graphs. Flow/product/auxiliary coefficients in the compressed construction are unit. Missing-product completion is minimal only among individual-coordinate additions for ambient linear reconstruction. | Same refined proof and independent review; reduced RLT reconstruction is explicitly credited. |
| Bounded block cycle rank | Explicit original-variable separation with `2^{O(r^2)}` parameter work and input-linear rational arithmetic at fixed maximum block rank. Integer flow/product coefficients are bounded by rank alone. The rank-three bound two is sharp on a unit-capacity K4 with seven observations. | [Result](../results/network-simplex-bounded-rank-hull.md), [independent review](review-network-simplex-reopened-bounded-rank.md). |
| Sparse series–parallel obstruction | With `O(q)` arcs, states and observations, a necessary product-facet coefficient ratio is Fibonacci `F_q`. Capacities and total flow are one. The graph can be simple, planar, treewidth two and maximum degree three. Coefficient magnitudes exceed every polynomial in sparse model encoding size. | [Result](../results/network-simplex-series-parallel-coefficient-growth.md), [independent review](review-network-simplex-reopened-series-parallel.md). |
| Fixed-state flat-chain oracle | An arbitrarily long chain of parallel pairs inside a bypass has exact original-variable separation and state-count-only coefficient bounds at fixed simplex dimension. Two explicit simplex variables use 41 positive-circuit tests after row grouping. Arbitrary observations on both pair arcs and the bypass are permitted. | [Result](../results/network-simplex-flat-chain-fixed-states.md), same independent series–parallel review. |

The original [cycle/theta](../results/network-simplex-cycle-theta-hull.md),
[parallel-path](../results/network-simplex-parallel-path-hull.md), and
[general universality](../results/network-simplex-universality.md) results remain
part of the paper. Their historical scope notes now link the completed extensions
instead of describing solved directions as open.

## Implementations and verification

- [Specialized exact separator](../code/network_simplex/README.md): graph
  preprocessing, sparse state grouping, cycle/theta supports, parallel-path
  max-flow cuts, and compact exact decompositions. Unsupported general topology
  is rejected. [Independent review](review-network-simplex-reopened-separator.md)
  includes 906 in-domain comparisons, 550 exact decompositions and exact global
  cut checks on independently enumerated vertices.
- [General compressed formulation and certificates](../code/network_simplex_compressed/README.md):
  exact rational assembly on arbitrary graphs, optional observed-coordinate
  elimination, numerical LP optimization, and verified rational Farkas cuts.
  [Independent implementation review](review-network-simplex-compressed-implementation.md)
  passed. Author checks include 600 objective comparisons, 758 memberships and
  476 verified cuts. A separate reviewer checked 270 objectives across four
  formulations with 1,080 exact rational primal/dual certificates.
- The general certificate pipeline recovers the required coefficient ratios
  `2`, `5`, and `21` on the K4 and Fibonacci examples in both formulation
  variants. [Integration record](../code/network_simplex_compressed/integration-output.json).
- The [fixed-state flat-chain implementation](../code/network_simplex/FLAT_CHAIN.md)
  passed its [independent implementation review](review-network-simplex-flat-chain-implementation.md),
  including 900 independently exactly certified decisions: 192 decompositions
  and 708 globally valid violated cuts. Its library is exponential in state
  count; the practical tests use at most two explicit simplex variables.
- [Computation record](network-simplex-reopened-computation.md) and
  [independent measurement review](review-network-simplex-reopened-computation.md)
  give exact instance definitions, model-equivalence checks, timing components,
  repetitions, source attribution, and negative findings.

Finite computations supplement proofs. Exact arithmetic is used for the stated
certificates and witness identities. Numerical LP comparisons are labelled as
such. In the general certificate API, `numerically_feasible` is not an exact
membership certificate, and failed rational cut recovery is reported explicitly.
The small-denominator numerical-to-rational adapter used by optimization
benchmarks is not a general certified LP reconstruction algorithm.

## Practical conclusions and limits

On the largest original sparse optimization case, full disaggregation has 5,675
variables and 9,160 rows. Initial compression reduces this to 255 variables and
225 rows; observed-coordinate elimination reduces it further to 222 variables
and 192 rows. Five-run median construction-plus-solution times are approximately
194 ms, 6.35 ms and 7.62 ms, respectively. Repeated cutting takes approximately
278 ms. These are small synthetic models, and construction is included.

Thus additional elimination saves size but does not improve total runtime here;
construction offsets its modest solve-time saving. The exact separator and
compressed LP also have similar membership times on the original sparse-state
workload. Larger benchmarks and outer-model applications are not inferred from
these measurements.

The separate long-chain study compares the new flat oracle against full
disaggregation as well as both compressed formulations. Full disaggregation is
an essential baseline there because the number of states is fixed. Cold library
construction, cached membership, decomposition, model construction and engine
time are distinguished. A build-and-solve improvement does not establish an
advantage over a persistent or prebuilt LP model.

At 512 gadgets, five-run median feasible membership times were 83.63 ms for
full disaggregation and 18.83 ms for the exact flat oracle, or 22.20 ms when an
exact decomposition was requested. The LP engine alone took 11.05 ms versus
18.21 ms for the exact online call. Thus the measured gain includes construction;
it is not a faster-callback claim. The full membership baseline also retains
the zero-weight residual-state block, so explicit removal of known zero states
is another untested baseline optimization. The cold circuit library cost was
22.32 ms and was excluded from cached repetitions, with that distinction explicit.

## Literature positioning

The [primary-source audit](network-simplex-reopened-literature.md) covers
Khademnia–Davarnia, Davarnia–Richard–Tawarmalani, Kis–Horváth's network Cayley
hulls, classical edge-direction/zonotope refinement, Liberti–Pantelides reduced
RLT reconstruction, large-coefficient 0/1 polytopes, and recent series–parallel
multiflow results. It found no exact matching restricted coefficient theorem or
combined observation-sensitive graph-hull statement in the inspected open
sources. This is a qualified literature assessment, not proof of priority.

The paper should emphasize the restrictive graph realizations, precise
coefficient/observation bounds, and the implemented structural specializations.
Generic convexification, rank-based product elimination, Farkas certificates,
and min-cut separation are established mechanisms and must be credited.

The [reaggregation source-boundary note](network-simplex-reaggregation-source-boundary.md)
and its [independent review](review-network-simplex-reaggregation-source-boundary.md)
preserve a useful correction: a common constraint matrix alone does not make
RHS aggregation exact. This is a known limitation, not a new main result. The
current proof merges only homothetic unobserved-state copies and is unaffected.

## Paper scope and remaining boundaries

A natural manuscript sequence is: model and known disaggregation; observation
compression and forest complements; explicit block and flat-chain oracles;
rank bounds and sharp examples; series–parallel coefficient growth; computational
comparisons and certificate semantics. The retained proof and code records are
sufficient to write those sections without assuming unresolved claims.

The current constructive directions have been completed and extended through
their useful immediate consequences. The failed scalar-profile composition is
retained in the [series–parallel investigation](network-simplex-reopened-series-parallel.md).
The following remain open boundaries, not gaps in the accepted results:

- Fixed simplex dimension on arbitrary nested series–parallel networks. The
  flat-chain proof has only one shared state-throughput profile; general nesting
  retains several interacting profiles. The Fibonacci family lets state count
  grow and therefore does not answer this question.
- Sharp coefficient constants above rank three, or a complete classification of
  graphs and observation patterns admitting unit coefficients. The sufficient
  forest-complement condition is not necessary.
- Speedups in production solvers, persistent LP callbacks, and industrial outer
  models. The current experiments neither establish these nor require them for
  the mathematical paper.

The root's [adjudication](network-simplex-reopened-root-review.md) records proof
readings, corrections, evidence distinctions, and final integration decisions.
The [final validation and artifact hashes](../code/network_simplex_review/final-validation.json)
identify the final checked source and link the repeatable root integration commands.
