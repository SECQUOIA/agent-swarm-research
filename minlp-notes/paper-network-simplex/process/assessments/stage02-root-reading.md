# Stage 2: root mathematical reading

The root reread the initial compression and observation-rank proofs before the
Stage 2 author began. The author is asked to rederive them in manuscript form.

## Points independently checked

- Suppression uses degree within a block, not degree in the whole graph.
  Articulation attachments do not invalidate path circulation identities.
  A connected core of rank r at least two and minimum degree three has at most
  2r-2 vertices and 3r-3 edges. Rank-one cycles and loops need their own convention.
- In the initial formulation the local merged coordinate is the aggregate
  cycle coordinate minus the sum of explicit coordinates. There is no separate
  auxiliary vector for the merged state. An unobserved block needs none at all.
- A fundamental-cycle matrix is a TU network matrix with identity chord rows.
  Pivoting an independent observed row/column minor has determinant plus or
  minus one. Row-replacement and bordered minors control both observed-product
  and retained-coordinate coefficients after elimination.
- A selected observation is used once per state, and distinct states have
  disjoint product coordinates. Residual rows should use one representative
  original arc directly rather than a potentially repeated cycle-coordinate
  expansion. This is essential to the stated unit flow/product coefficients.
- The restriction kernel is precisely the circulations supported on unobserved
  arcs. Its dimension includes isolated vertices and loop contributions. The
  minimum number of additional individual coordinates follows by rank increase
  at most one and attainment by chords of a forest of the unobserved graph.

## Development suggested during writing

Known fixed arcs may be deleted exactly: substitute their fixed flows c and
observed products c*y, and change the balance to b minus their incidence times c.
The remaining flow polytope is affinely bijective to the original, as is its
sparse product hull. Structural parameters can then be computed on the reduced
graph. This needs no claim that all fixed arcs can be detected in linear time.

If every actually fixed arc is deleted, a relative interior flow on the remaining
arcs is strictly between its original bounds: take a convex combination of
feasible witnesses avoiding each remaining lower and upper bound. Thus no extra
affine restriction remains beyond incidence. The author may use this elementary
observation if it makes the capacity-degeneracy qualification more useful.

No Stage 2 manuscript acceptance is implied; five independent reviews follow
the completed author draft.

## Root reading of the Stage 2 draft

The fixed-arc lemma is valid: each remaining coordinate has a feasible midpoint
strictly within its original bounds, and averaging these points is interior to
all remaining bounds simultaneously. The core-size proof, TU minor argument,
reversible substitution, nonzero count, and K4 example also check out in the
root's reading. In the example the reconstructed 23 state flow is -1/10, while
all three observed values 1/5 satisfy their independent box envelopes.

Provisional minor clarification ROOT-S2-1: the paragraph explaining forest-cut
reconstruction should specify which balance system is summed. For state flows
within one block, the right-hand side is lambda_j times A_B v_B, not generally
lambda_j b restricted to V_B, because other blocks can meet at articulation
vertices. Equivalently sum A_B h=0 for deviations and restore the reference.
The formal proof already uses the correct deviation system. Adding the equation
would prevent readers from misapplying the informal implementation explanation.

Resolution before review dispatch: the author's finished Stage 2 source adds
`A_B f^{B,j}=y_j A_B v_B` to this paragraph and explains the circulation reason.
The frozen `stage02-round01` includes that clarification. ROOT-S2-1 is therefore
already resolved in the authored stage, and is not an outstanding review finding.
