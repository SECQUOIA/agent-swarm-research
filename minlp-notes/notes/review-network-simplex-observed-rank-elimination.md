# Independent review: auxiliaries count unobserved cycles

Date: 2026-09-07. Reviewer: `review_separator`, independent of the derivation.

**Verdict: pass.** The theorem, forest-complement corollary, and minimum
individual-product completion statement in
[`network-simplex-observed-rank-elimination.md`](network-simplex-observed-rank-elimination.md)
are mathematically correct under their stated bounded equality-network and
simplex assumptions. Reviewed source SHA-256:
`edef0083976b7b8c6196a6bcefa3bd828bff7bf06f0ab38ac4a5a36e401bc3db`.
No correction is required. This review does not establish literature priority
or a measured runtime improvement.

## Exactness and the observation-sensitive dimension

Classical simplex-state disaggregation remains the starting point. Conditional
state flows differ from their state-weighted reference by circulations. The
circulation space splits over undirected blocks. Within a block, states with
no observations have identical normalized domains and can be merged; refining
them proportionally preserves every observation. Different blocks may merge
different labels because the state circulation coordinates of distinct blocks
are independent. Zero-weight states cause no difficulty with finite capacities.
These facts establish the parent compressed hull without a new general hull
method or a new reduced-RLT mechanism.

For a given block and active label, the kernel of its observed-arc map consists
exactly of circulations supported on the unobserved subgraph. Its dimension is
`|E_unobserved| - |V_B| + components`, counting isolated vertices and loops.
Degree-two suppression does not alter this kernel: observing any arc on a
suppressed path fixes the path deviation, and a circulation zero on that arc
is zero throughout the path. Thus the rank-nullity identity is valid for the
**original** unobserved arc graph, as stated, rather than just a suppressed core.

Consequently the retained auxiliary count is the sum of unobserved cycle ranks
over active block/label pairs. An entirely unobserved label is merged and must
not be charged its block rank. The forest-complement corollary is valid on
arbitrary network graphs, including K4 blocks. It does not conflict with prior
large-coefficient original-hull examples: their observation pattern must leave
unobserved cycles in some active block/label pair if their obstruction applies.

## Elimination and coefficient bounds

The fundamental-cycle matrix, including its identity chord rows, is totally
unimodular. With independent observed rows `D` and an invertible square column
pivot `B`, its determinant is `+1` or `-1`. For any core path row, each entry of
`W=c[I] B^-1` is a selected-row replacement minor divided by `det(B)`; every
entry of the Schur complement `R=c[F]-W D[:,F]` is a bordered minor divided
by that same determinant. Both matrices therefore have entries in `{0,±1}`.
The substitution is a bijective affine parametrization, not merely a necessary
condition or a numerical rank reduction.

The original-coordinate coefficient claim survives substitution:

- Each selected observation supplies a distinct product variable, and its path
  orientation only changes a sign.
- A nonselected observation contributes its own different product variable;
  selected observation equations become identities and are dropped.
- Different labels use disjoint product and retained-variable columns.
- A residual bound uses one actual original flow coordinate for its aggregate
  path deviation. Expanding that deviation in several chord coordinates is
  unnecessary and could obscure the claimed coefficient bound.

Thus flow, product, and retained-variable coefficients stay in `{0,±1}`.
Simplex coefficients can accumulate rational reference and capacity data; no
unit bound is claimed for them. The complete constraint matrix need not be
totally unimodular. The argument only uses total unimodularity of the cycle
matrix used for elimination.

## Size and completion statements

Elimination adds no rows. A cyclic suppressed core has one path at rank one
and `O(r_B)` paths otherwise. The stated row count follows. It is not a
matrix-nonzero count when rank grows: each substituted row can involve many
selected observations. Fixed maximum block rank bounds this extra factor,
giving linear sparse size in the input parameters. All rational coefficient
encoding lengths are polynomial.

Each new individual arc observation increases observed rank by at most one.
At least `rho_Bj` new scalar observations are therefore needed for ambient
linear reconstruction. Adding the nonforest edges of a spanning forest of
the unobserved subgraph attains this bound. They may be actual missing products
used as auxiliary coordinates; the completed observations have forest
complements, so the no-auxiliary theorem for the completed graph projects to
the desired formulation. This is not a lower bound for arbitrary extended
formulations or for reconstruction on special lower-dimensional feasible faces.
In particular, zero-weight strata and capacity-forced fixed flows can need fewer
coordinates than the ambient count.

An alternative proof of the unit-coefficient statement is available after this
completion: recover each remaining unobserved forest-edge state flow by summing
the balance equations on one side of its forest cut. Every known state-product
coordinate crosses that cut at most once and receives coefficient `0,+1,-1`.
The source's TU proof is already valid; this observation may help exposition.

## Independent exact checks

Added
[`verify_observed_rank.py`](../code/network_simplex_review/verify_observed_rank.py),
which uses SymPy exact arithmetic and does not import the author's compression
implementation. Run:

```sh
python code/network_simplex_review/verify_observed_rank.py
```

The script checks 204 observation patterns: all 64 patterns on K4, all 16
patterns on three parallel arcs and a loop, all four patterns on two loops,
and 120 randomly oriented connected multigraphs with random observations.
It constructs fundamental-cycle matrices directly from an incidence matrix
and an independently selected spanning tree. It checks:

1. Observation nullity against a separate spanning-forest calculation on the
   unobserved graph.
2. Full observation rank after the asserted minimum completion.
3. Pivot determinant `±1` and all entries of `W,R` in `{0,±1}`.
4. Exact reconstruction starting from arbitrary cycle coordinates and, in the
   reverse direction, independently chosen retained coordinates and observations.
5. Selected observation equations becoming identities after substitution.

Recorded result:

```text
PASS: 204 exact observation patterns; rank identity, minimum forest completion,
unit elimination coefficients, two-way reconstruction
```

These finite checks support the structural proof; they are not its substitute.
The generic rank-elimination idea and product reconstruction overlap reduced
RLT and should remain credited to the cited prior work. The explicit network
criterion and combined sparse hull bounds are suitable candidate contributions,
subject to the separate literature audit and measured computational assessment.
