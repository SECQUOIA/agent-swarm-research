# Stage 2, round 1 — independent review 3

Reviewed `process/snapshots/stage02-round01`, especially the complete new
`sections/02-compression.tex`, together with the foundation dependencies and
the changes to their source positioning. No other current-round reports were
read, and no manuscript source was edited.

## Verdict and enumerated findings

**Accept: no major or minor issues identified.**

1. **S02-R1-R3-01 — Verification finding, no correction required:** the
   observation-rank elimination, including its unit coefficient claim, follows
   from the stated minor identities. The minimum-completion claim is properly
   restricted to individual-coordinate reconstruction on the ambient linear
   space. It is not presented as an extension-complexity lower bound.

This is not approval of results planned for later stages. The absence of a
matching prior theorem is not independently established by this review.

## Mathematical examination

### Fixed coordinates

Lemma `lem:fixed-arcs` is correct under the section's nonemptiness assumption.
That assumption gives `0 <= c <= u_F`, so extension and restriction really are
inverse feasible-set maps. The added product coordinates are affine in the
retained simplex variables, and hence commute with convexification.

The affine-hull assertion does not silently assume that the original flow
polytope has an interior point. After all constant coordinates are removed,
each remaining coordinate has a feasible midpoint strictly between its bounds.
A finite average supplies one point strict in every remaining bound. Its
relative neighborhood in the balance space establishes the claimed affine
hull. The empty-coordinate case is explicitly handled. Detecting fixed arcs is
not incorrectly included in an unproved preprocessing time claim.

### Path and cycle compression

The signed path deviations and both orientation cases in the path bounds are
consistent with incoming-minus-outgoing balance. Degree-two suppression is
performed within a cyclic block, so articulation attachments do not invalidate
the argument. A non-cycle core has minimum degree three; the rank and degree
identities imply the stated core-size bounds. The separate loop/rank-one case
avoids applying that bound where it would fail.

The cycle-coordinate formulation is exactly the accepted block-state
formulation with one merged state removed. In particular, the aggregate core
deviation is a circulation because `x` remains in the original flow domain.
Every zero-weight state is forced to zero by finite path bounds and identity
chord rows, even if the unscaled translated domain does not contain zero.

### TU lemma and bordered minors

I checked both steps of Lemma `lem:cycle-tu` rather than taking the coefficient
claim as a general property of Gaussian elimination. Replacing tree columns
by chord columns and expanding the unchanged identity columns proves that each
minor of the network matrix is an incidence determinant divided by the tree
determinant. Appending chord identity rows preserves total unimodularity.

For the second step, an entry of `c_I B^{-1}` is the determinant obtained by
replacing the corresponding row of `B` with `c_I`, divided by `det(B)`.
The residual free-column entry is exactly the displayed bordered determinant
quotient. The numerator either uses distinct rows and columns of `C`, or has
a repeated row and vanishes. Thus both coefficient arrays are unit-valued.
The empty-pivot case is covered and creates no exceptional division.

### Observation-sensitive formulation and encoding

Pivot reconstruction is reversible. Nonselected observation equations remain,
including observations of multiple original arcs along the same path. A
selected equation becomes an identity and may be removed. The selected product
coordinates are distinct, while different labels have disjoint product columns.
Consequently assembling a residual row does not combine several occurrences of
one product into a coefficient of magnitude two. The single representative
flow coordinate similarly preserves unit flow coefficients.

The kernel of observation restriction consists precisely of circulations on
unobserved arcs; isolated vertices must be counted, as the manuscript does.
This proves the nullity formula and the forest-complement corollary even with
loops and parallel edges. Polynomial coefficient encoding follows from finite
sums of rational input data, while the manuscript correctly warns that clearing
simplex-coefficient denominators changes the integer normalization.

The explicit nonzero bound is sufficient. Each state path expression has at
most `r_B` product/auxiliary terms and one collected simplex coefficient;
each block has `O(r_B)` paths. Residual rows add these across `a_B` labels,
and a remaining observation equation uses `O(r_B)` entries. This yields the
displayed `r_B^2(a_B+1) + r_B |O_B|` bound, in addition to the original sparse
domain. Thus the fixed-maximum-rank input-linear matrix-size consequence is
justified. No general TU claim for the completed formulation is made.

### Coordinate completion and example

Each added scalar coordinate can remove at most one dimension of the
restriction kernel. Adding the nonforest edges of the unobserved subgraph
removes all its cycles and attains that lower bound. Treating the added
observations as auxiliary variables commutes with convexification; the added
row count is absorbed because the number of added coordinates is at most
`sum_B r_B a_B`. The direct forest-cut explanation also correctly retains
component-consistency equations.

I recomputed the K4 balance identities and the separating example using exact
fractions. The four-path average has the stated arc flows. All three selected
products satisfy McCormick, while their sum is `3/5 > 1/2`. This is a valid
strict-strength example and is not incorrectly presented as a complete hull
description by itself.

## Independent executable checks

`verification/reviewer3/stage02-round01/check_elimination.py` constructs
incidence and cycle matrices independently, without importing repository hull
implementations. It checks all observation patterns and all square pivot
choices for a loop, four oppositely oriented parallel arcs, and a K4 network.
All **121 square minors, 72 nonsingular pivots, 382 reconstructed rows, and
82 observation patterns** passed exact SymPy checks. These finite checks
supplement the proof examination; they do not replace it.

A private `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
build succeeded. The final 13-page log has no warnings or overfull/underfull
boxes. The build copy, log, check script, and JSON counts are retained in the
same verification directory.

## Source audit and limitations

I verified the RRLT comparison directly against the author-hosted manuscript
linked as `[LP06]` on [Liberti's publication list](https://www.lix.polytechnique.fr/~liberti/publications.html):
[the open author copy](https://www.lix.polytechnique.fr/~liberti/red10.pdf).
Theorem 3.1 on printed pp.7–8 replaces a complementary set of product equations
using full-row-rank multiplied balances; Section 2 discusses introducing and
eliminating absent products. The paragraph following the theorem also warns
that removing exact product equations does not automatically make their
relaxations redundant. The manuscript's attribution and insistence on keeping
reconstructed state/residual bounds are consistent with this source. The
author copy is dated November 28, 2005, with a January 29, 2006 build stamp;
its theorem number agrees with the cited locator.

The CiteSeer mirror timed out, and the browser tool could not open the author
PDF, but ordinary HTTPS retrieval of the author's linked copy succeeded.
The latter was read with `pdftotext`; no access restriction was bypassed.
The fixed-graph observation criterion is described as the additional
specialization, while the underlying linear-elimination principle is credited.
I found no unsupported absolute priority assertion in this stage.

The earlier source-locator correction now identifies the published electronic
companion explicitly. I checked the foundation changes against the previous
snapshot and found no new mathematical dependency problem. This bounded source
audit did not attempt an exhaustive literature search for every graph-theoretic
specialization or re-run the repository's numerical implementations.
