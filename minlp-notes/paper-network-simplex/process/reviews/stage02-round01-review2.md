# Stage 2, round 1 — independent review 2

**Verdict: accept this stage. No major or minor defects identified.**

I reviewed `sections/02-compression.tex` in the frozen
`process/snapshots/stage02-round01` snapshot, together with the foundation
statements on which it depends and the changes to those foundations since my
Stage 1 review. I did not read other current-round reports, coordinate with
reviewers, edit the manuscript, or spawn agents.

## Enumerated findings

1. **No major findings.** The fixed-arc reduction, path compression,
   observation-sensitive elimination, forest-complement corollary, and
   individual-coordinate completion statement have valid proofs under the
   stated assumptions.
2. **No minor findings.** I have no required local correction to this stage.

## Detailed mathematical assessment

### R2-S2-C1 — fixed-coordinate reduction (verified)

At `sections/02-compression.tex:12–49`, adjoining the fixed coordinates is indeed
an affine bijection of the flow domains and of the bilinear graph sets: a deleted
product is the affine coordinate `c_e y_j`. The affine-hull conclusion after
removing *all* fixed coordinates is valid. For each nonconstant remaining
coordinate, the midpoint of two differing feasible values is strictly between
its finite bounds. Averaging those midpoints produces a point strict in every
remaining coordinate, because other midpoint values still satisfy their bounds.
A relative neighborhood in the balance affine space is then feasible. The empty
remaining-arc case is treated separately and correctly.

This preprocessing is not claimed to run in linear time or to follow from
zero-capacity detection alone. Removing fixed arcs may change blocks, and the
text correctly asks that ranks be computed on the resulting graph. It also
retains the distinction between full-domain affine dimension and a conditional
state slice.

### R2-S2-C2 — suppression, orientations, and core size (verified)

At lines 51–105, the signed path deviation follows from the *block circulation*
balance, even if an internal path vertex is an articulation of the full graph
or original arc orientations alternate along the path. The deviation, rather
than the original flow, is constant after applying the signs. Both formulas for
the path interval follow by solving the original arc bounds for that signed
deviation.

A cyclic biconnected block of rank at least two has at least one vertex of
block degree at least three; suppressing all internal degree-two vertices leaves
minimum degree at least three. The handshaking and cycle-rank identities therefore
give both stated core bounds. The single-cycle convention correctly covers
rank-one parallel pairs and self-loops. The formula for cycle rank includes
isolated vertices when it is later applied to an unobserved subgraph.

The identity chord rows imply boundedness and injective parametrization even
when capacities force a lower-dimensional domain. Repeated observations of
arcs on a single suppressed path are not discarded; their consistency equations
are retained.

### R2-S2-C3 — exact extended hull and coefficient accounting (verified)

At lines 107–154, eliminating the merged cycle coordinates by their sum does
not lose circulation balance, since the aggregate deviation and each retained
state deviation are already core circulations. At zero weight, finite lower
and upper path bounds collapse to zero regardless of whether the unscaled
interval contains zero. Hence the proof covers infeasible reference bounds,
zero state weights, and zero merged weights.

I independently reconstructed the row and variable counts. The residual
inequalities use one original flow coordinate per path, preventing unintended
coefficient aggregation in `x`. Each selected product belongs to one state,
so different state contributions in the residual cannot accumulate on the same
product coordinate. The nonzero bound at lines 278–292 properly accounts for
dense cycle rows, and the manuscript distinguishes rational row scaling from
primitive integer normalization. None of these statements asserts total
unimodularity of the whole extended formulation.

### R2-S2-C4 — elimination and unobserved cycle rank (verified)

At lines 169–261, the proof that the fundamental-cycle matrix is totally
unimodular is valid: after fixing tree columns, every square submatrix of the
network matrix is a tree-column replacement determinant divided by a unit
tree determinant. Appending chord identity rows preserves the property.

For the pivot substitution, an entry of `W` is a row-replacement minor, and an
entry of `R` is a bordered minor divided by the pivot determinant. Selected-row
repetition yields zero rather than invalidating the determinant argument. Empty
pivot and free sets are explicitly covered. Consequently substitution preserves
the claimed unit coefficients.

The key dimension calculation is the kernel of restriction to observed arcs.
It consists exactly of circulations supported on unobserved arcs, with dimension
`|U|-|V|+c`. Observing any one original arc on a suppressed path fixes the signed
path value, so selecting independent observed core rows has the same rank as
restriction on the original graph. This proves the claimed auxiliary count,
including disconnected unobserved graphs, parallel cycles, and loops.

### R2-S2-C5 — forest recovery and minimum completion (verified)

At lines 294–375, a forest complement eliminates every unknown circulation
direction. For completion, every scalar coordinate can reduce kernel dimension
by at most one, while selecting the nonforest edges of the unobserved graph
removes exactly that many directions. The stated minimum is appropriately
restricted to individual-coordinate reconstruction on the ambient linear space;
it is not presented as an extension-complexity lower bound or as a statement
about zero-weight slices.

Applying the forest corollary to the enlarged observation set gives the claimed
alternative extended formulation. New observations are only added for locally
active labels, so they do not enlarge the label counts. Their additional rows
are absorbed by the existing rank-label term. Forest-cut reconstruction uses
one unknown crossing forest edge, known state products on the other crossing
arcs, and known weighted block balance; disconnected forest components impose
the necessary consistency equations.

### R2-S2-C6 — the worked K4 example (verified)

At lines 377–400, the three formulas for missing state deviations satisfy all
four incoming-minus-outgoing balance equations. In particular the expression
for the 23 deviation gives exactly the displayed inequality. The proposed flow
has values `x12=x34=1/2` and all other arcs `1/4`. At weight `1/2`, each observed
product `1/5` satisfies all four independent McCormick inequalities, whereas
the sum `3/5` violates the reconstructed state bound. The example correctly
presents this as one necessary cut, not the complete hull description.

## Independent executable checks

I wrote and ran
`verification/reviewer2/stage02-round01/check_elimination.py`, using only exact
SymPy arithmetic and no repository hull implementation. Results are in the
adjacent `result.json`.

It checks 810 observation patterns on 30 independently oriented, subdivided
multigraphs arising from a loop, parallel pair, theta core, K4, and K3,3. Checks
include:

- Exact incidence kernels and signed equality of all original rows along each
  suppressed path.
- Preservation of cycle rank and the applicable minimum-degree core bounds.
- Empty, full, and varied sparse observation sets.
- All entries of each independently formed elimination `W` and `R` belonging
  to `{0,1,-1}` and exact reconstruction after substitution.
- Equality between elimination nullity and the unobserved multigraph cycle rank.
- Exact number and sufficiency of added nonforest coordinates.
- Symbolic K4 balance identities and rational checks of its McCormick gap.

All checks passed. Command actually run:

```sh
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python paper-network-simplex/verification/reviewer2/stage02-round01/check_elimination.py
```

The finite computations support the independent proof assessment; they do not
replace the proofs for arbitrary graphs or establish all claims by sampling.

## Scope and limitations

I examined all mathematical statements in the new section and their foundation
dependencies. I did not independently establish bibliographic priority, retrieve
the complete Liberti–Pantelides paper, compile a private PDF, or assess later
unwritten sections. The existing attribution describes the classical elimination
mechanism as prior work and confines the additional claim to the graph criterion
and exact sparse hull consequence; I found no overstated general novelty in this
stage. No computational performance claims are made here.
