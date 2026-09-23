# Independent review: compressed network–simplex extended hull

Date: 2026-09-07. Reviewer: independent subagent `review_compression`.
Scope: [candidate proof](network-simplex-reopened-compressed-hull.md), read
independently of the author's implementation, followed by the implementation
review below. Verdict: **PASS for the theorem and reviewed implementation,
subject to the presentation qualifications below.** This is a correctness
review, not a priority determination.

## Proof audit

The circulation decomposition and proportional state refinement are correct.
The reference flow need only solve the balance equations; it need not satisfy
capacity bounds. Every homogeneous circulation has zero net contribution at
each vertex separately within every undirected biconnected block. Consequently,
independent block circulations can be combined while preserving all original
balances, including at articulation vertices. This remains true if a vertex
has nonzero external supply or demand: that imbalance is already in the
reference vector.

Maximal paths use degree within a block, not degree in the full graph. At an
internal degree-two vertex the homogeneous block circulation is constant up to
the arc orientation signs. Intersecting the original signed deviation bounds
therefore gives exactly the stated path interval. For a connected suppressed
core of rank at least two and minimum degree three, `2k >= 3n` and
`r=k-n+1` give `n<=2r-2` and `k<=3r-3`. Rank-one blocks require the separate
loop representation in the statement.

The fundamental-cycle matrix has full column rank and can be oriented to have
an identity on chord rows. Thus `t_B(x)` is obtained from distinct chosen
original arcs, with an orientation sign and reference shift. There is no
assumption that the entire original flow polytope has positive dimension.
Zero capacities or forced block coordinates remain admissible.

For positive weights the explicit block bounds are precisely the perspective
of the bounded core-coordinate domain. At zero weight all core path values
are zero; chord identity then forces all auxiliary coordinates to zero.
This handles zero explicit labels and a zero residual weight without closure
or recession problems. For a positive residual weight, its normalized block
coordinate can be shared by every globally unobserved simplex state in that
block. Different blocks may have different unobserved state sets, because
their domains are independent Cartesian factors. Refining every block and
combining matching global labels yields a valid full state flow.

Bridges are fixed at their reference values. A disconnected component requires
its own total-balance check; isolated vertices are included. A self-loop has a
zero incidence column and is an independent interval/rank-one block. Parallel
arcs must remain distinct edges: a pair can form a rank-one block even though
the simple graph on the same vertices would have a bridge. These are
implementation requirements, not exceptions to the proof.

## Presentation corrections and limits

1. The reviewed draft's final paragraph said “Every variable coefficient” is
   in `{0,-1,1}`. This should say **every extension-variable coefficient**,
   as the theorem already does. The simplex-variable coefficients contain
   path bounds and reference values. No total-unimodularity assertion about
   the full extended matrix follows.
2. The displayed complexity counts variables and rows. With unrestricted
   rank it does not count sparse matrix entries. Writing `N=|V|+|E|+m+|O|`,
   one explicit nonzero bound is
   `O(N + sum_B [r_B^2(a_B+1) + r_B |O_B|])`, with the sum over active
   blocks. It follows by expanding core bounds and product observation
   rows. Fixed maximum block rank still gives linear sparse matrix size.
3. Constructing rational references by a spanning-forest solve and taking
   signed interval intersections gives polynomial coefficient bit lengths.
   This is not a bound on runtime for a general LP solver.
4. This is an exact hull for the stated graph/domain. Intersecting it with
   arbitrary extra restrictions is generally only a relaxation of the
   restricted nonlinear graph.

## Independent exact computational check

The independent verifier is
[review_compression.py](../code/network_simplex_exploration/review_compression.py).
It constructs both the candidate compressed EF and the classical EF with one
flow per original arc and simplex state without using production formulation
code. It then also imports the production model to compare its formulations,
both before and after observed-rank elimination, against those independent
assemblies. SciPy finds primal and dual optima, then Python
`Fraction` arithmetic checks all primal constraints, dual signs, exact
stationarity, and equal primal/dual objectives. Comparisons therefore use
exact rational optimality certificates, not floating objective tolerances.

Result: **270 matching support optima across four formulations, with 1080
exact rational primal/dual certificates**. Cases include a K4 block, a nested series–parallel block,
four parallel paths, a self-loop, subdivided paths with reversed orientations,
articulation gluing, a disconnected cyclic component, a bridge, and an isolated
vertex. Capacities may be zero. Reference flows can violate capacity bounds.
Observations produce different local label sets. In addition to optimizing
over the entire hull, the verifier fixes fractional simplex weights and
aggregate flows, including zero explicit weights and zero residual weights.

The independent formula assembly starts from hand-specified core/path data.
The production assembly receives only the original graph, balances,
capacities, and observations. Its block partition is checked against the
hand-specified blocks. Every produced fundamental cycle is checked against
the exact original incidence matrix, and the reference balances are checked
exactly. The number of retained variables after observed elimination is
compared with an independent union-find cycle count on each unobserved
multigraph. All flow, product, and auxiliary coefficients are checked to be
unit or zero. These finite cases do not exhaust all graphs; they do not test
empty input polytopes or claim a runtime benchmark.

## Production implementation audit

The audited [model.py](../code/network_simplex_compressed/model.py) correctly
uses edge IDs in iterative Tarjan traversal, preserving parallel arcs,
and handles loops independently. Its spanning-tree reference sign agrees
with incoming-minus-outgoing incidence. Normalizing and grouping identical
fundamental-cycle rows is exact and can merge more than literal degree-two
paths; this remains valid because it merges equal linear functions on the
entire circulation space. The rational state bounds, residual bounds, and
observation equations match the proof.

The observed-coordinate elimination uses only free auxiliary pivots from
observation equations, fully reduces previously selected pivot expressions,
and substitutes them into all model rows before renumbering the retained
coordinates. This is a reversible rational elimination. Production LP solves
are numerical and are correctly described as such; the independent verifier
adds exact certificates for the tested instances.

A practical issue identified during review is repeated global observation
scanning in per-block and per-block/state loops. This does not affect
correctness, but can make assembly superlinear even at fixed block rank.
The author repaired both scans. The final inspected code constructs
`observed_by_edge` once, collects a block's observations by traversing its
own edges, and reads `Block.observations[state]` during elimination. I checked
these changes directly. The repeated global-scan concern is resolved;
this does not by itself establish a complete assembly-time bound or a
measured speedup.

## Literature boundary

The general simplex-disaggregated hull is already given in the appendix of
[Khademnia and Davarnia, arXiv version 2](https://arxiv.org/html/2302.14151v2),
and the proof uses this classical fact. The candidate's potential contribution
is its explicit combination of local observation sparsity, independent flow
blocks, and cycle/path coordinates with the resulting size bound. This audit
does not establish that those reductions or their combination are new.

## Possible further compression

The review led to [observed-rank elimination](network-simplex-observed-rank-elimination.md):
only `r_B-d_Bj` state coordinates need remain, equal to the cycle rank of
the label's unobserved subgraph. The separate note proves the refinement,
the unit coefficient assertion, and the forest-complement original-space
corollary. Since this reviewer co-developed that proof, its independent
theorem review belongs to a different reviewer.
[That independent review](review-network-simplex-observed-rank-elimination.md),
by `review_separator`, passed the proof and 204 exact observation-pattern
checks. The production elimination is included in the 1080 exact certificates
above.
