# Stage 1, round 1 — independent review 2

**Verdict: accept this stage. No major or minor defects identified.**

Reviewed the frozen files in `process/snapshots/stage01-round01`, including the
introduction, complete foundation section, bibliography, and README. My emphasis
was circulation factorization and constructive sparse-state gluing. I did not
read another current-round report, coordinate judgments, edit manuscript sources,
or spawn agents.

## Findings list

1. **No major findings.** I found no false statement, essential proof gap, or
   unsupported central claim in the written stage.
2. **No minor findings.** I have no required local corrections. This is not an
   assessment of the unwritten sections or the eventual completeness of the paper.

## Mathematical checks

### R2-S1-C1 — disaggregation, including the empty case (verified)

At `sections/01-foundations.tex:107–142`, finite capacities are exactly the
hypothesis needed to force a zero state flow at zero weight. The explicit scaled
system avoids an invalid interpretation of the empty polytope at zero weight.
At least one weight is positive, so feasibility of the extended system implies
that the underlying flow polytope is nonempty. The proof accounts for absent
products and for an observed label of zero weight. When `m=0`, the only state flow
is `x`, and the claimed reduction to the flow polytope follows directly.

The constructive direction really uses at most `m+1` graph points: each normalized
positive state flow supplies one point with the corresponding simplex vertex.
The linearity argument in the other direction establishes containment of the
whole convex hull, rather than only containment of graph points.

### R2-S1-C2 — reference offsets and block factorization (verified)

At `sections/01-foundations.tex:159–231`, the decomposition is into circulation
*deviations*. The reference vector need only satisfy the balance equations.
Accordingly, the block domains need not contain zero. This resolves the important
nonzero-balance issue at articulation vertices: the reference vector carries the
balance, while every deviation has zero incidence within each block separately.

For arbitrary arc orientations, a fundamental undirected cycle gives a signed
circulation; it need not be a directed cycle. The stated forest argument proves
that these vectors span the full kernel. A fundamental cycle is confined to one
cyclic biconnected block, including a two-edge parallel cycle. A loop gives its
own unit-coordinate kernel vector. The direct sum statement therefore remains
valid for multigraphs and self-loops. The bridge coordinates of every circulation
are zero by the same basis argument, and the bounds on those coordinates are
correctly checked on the reference vector.

I also checked the cases of no cyclic blocks, disconnected components, isolated
vertices with nonzero balance, zero capacities, and a zero-dimensional feasible
polytope. The assumptions and empty-family convention give the correct outcomes.
Zero capacities can lower feasible dimension but do not invalidate the ambient
cycle coordinates or the linear decomposition.

### R2-S1-C3 — locally different mergers and global reconstruction (verified)

At `sections/01-foundations.tex:233–328`, local mergers do not introduce an
inconsistent correlation across blocks. Given a global state `k`, the proof
chooses a feasible scaled deviation independently in each Cartesian block and
then combines them using the block kernel decomposition. This is permissible
because all capacity constraints are edgewise and there are no additional side
constraints. The original common global weight is retained in every block.

For a positive merged weight, proportional refinement belongs to the correct
scaled block domain even when that domain excludes zero. For a zero merged
weight, all missing global weights are zero; finite bounds force the merged
vector to zero. Thus the piecewise definition preserves both the local sum and
all original observed coordinates. Unobserved blocks and observed labels with
zero weight are correctly distinguished. The proof also establishes all bridge
state bounds after reconstruction.

The final paragraph at lines 345–349 correctly limits the exactness claim after
additional linear constraints are imposed. The common-matrix example at lines
330–342 is arithmetically correct and isolates why homothetic merging, rather
than shared row normals alone, is essential.

## Executable evidence

I wrote an independent exact-arithmetic check in
`verification/reviewer2/stage01-round01/check_factorization.py`; it does not import
any repository hull implementation. Its result is recorded in the adjacent
`result.json`.

The check derives local and global kernels using exact SymPy rational arithmetic
on a graph consisting of two triangles meeting at an articulation, a parallel
pair, a bridge, a loop, a disconnected edge, and an isolated vertex. It varies
arc orientations across 36 independently selected assignments, constructs a
reference flow deliberately outside its capacity bounds, and verifies 324 exact
state refinements. Cases include zero residual weight, zero explicit weight,
zero merged weight, different observed-label sets in different blocks, and
entirely unobserved blocks. Every case passed checks of local circulation,
scaled bounds, observation preservation, global balance, and reconstruction of
the original flow.

Command actually run:

```sh
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python paper-network-simplex/verification/reviewer2/stage01-round01/check_factorization.py
```

The computations supplement the proof review; they do not substitute for the
arguments for arbitrary graphs or prove the entire hull theorem by sampling.

## Attribution and readability

The stage clearly credits disaggregation and shared-simplex Cartesian gluing as
known foundations. I inspected the local dissertation text stored under the
Davarnia 2017 archive entry and confirmed that Proposition 2.6 is indeed a
*dissertation* locator, as the manuscript says. I also checked the local
Kis–Horváth discussion of the common-matrix reaggregation boundary and its
Section 5.7 heading. The published [Almoghrabi–Skutella–Warode article](https://link.springer.com/article/10.1007/s10107-026-02392-8)
confirms the cited Remark 1 and the distinction between total-flow integrality
and individual commodity coordinates; the unnumbered remark in the local
preprint is a version difference, not a manuscript error.

The definitions precede their use, the global residual state is distinguished
from a local merged state, and the proofs are readable without the research
notes. The paper does not suggest that generic polynomial-time separation is a
new contribution.

## Review limitations

I did not independently verify every bibliography entry or every historical
locator, run a private TeX build, or certify novelty of future results. I reviewed
the source rather than PDF page layout. The exact experiment uses a deliberately
mixed but finite family of graphs; the universal statements were assessed by
reading and reconstructing their proofs. The stage contains no benchmark claims
requiring numerical replication.
