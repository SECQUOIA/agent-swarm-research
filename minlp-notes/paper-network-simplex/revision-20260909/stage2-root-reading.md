# Stage 2 root mathematical reading

The root's preliminary reading covers the 33 formal results and their proof
contracts; see root-preliminary-reading.md. This stage adds checks of the exact
source injection, local-neighborhood sufficiency, and circuit classification.
Earlier acceptance records are provenance, not substitutes for this reading.

## Checks of sensitive arguments

- De Loera--Onn define representation by a coordinate-erasing bijection, and
  their printed page 816 injects (i,j,k) as ((i,j),(1,k),1). The retained
  variables are actual first-layer entries. Clearing rational equations does
  not rescale the original variables; the manuscript's final uniform network
  normalization scales the free coordinates and preserves their ratio.
- In the balanced-incidence lemma, -delta+tau has entries -delta_r and
  R delta_r. The displayed epsilon bounds the infinity norm of the recovered
  profile change and the single slack adjustment by a/16. Every free observed
  value remains positive below a/2; every branch profile remains above 15a/16.
  Reducing an unobserved entry in the selected row preserves all bounds and
  every aggregate and state balance. This establishes a neighborhood with
  two-dimensional section interior, needed to exclude affine-equation changes
  of the two coefficients.
- Splitting serial joins and subdividing unobserved b-arcs produces 3N vertices
  and 4N arcs with maximum degree three and no parallel pairs. Connectors and
  subdivided arcs have unique state-flow lifts and redundant unit bounds;
  fixing their aggregate values preserves the same two free product coordinates.
- The bounded-rank multiplier bound follows from a unimodular transformation of
  the primitive support ray, not an entrywise inverse triangle estimate. The
  inverse-basis recovery polytope includes every suffix support. Its vertex has
  full-rank active normals even when the polytope is lower-dimensional.
  Sequential rational denominators acquire at most one parameter-bounded
  determinant per chosen state; this is additive growth of bit length.
- The expanded three-label classification checks the actual small-support
  cases. With a negative singleton, both positive proper subsets must cover its
  coordinate, giving the two overlapping pairs. With no negative singleton,
  presence of a positive singleton excludes overlapping pairs by positivity
  and minimality, leaving partitions; pair-only covers require all three pairs.
  The unique weight two belongs to the negative full normal, which contains no
  product. Original-flow coefficient repair still needs the separate gadget
  balance argument; circuit weight bounds alone would not prove it.

## Independent exact finite computation

root-circuit-check.py uses SymPy rational nullspaces, with no production or
candidate-library imports, to enumerate minimally supported positive dependencies
of the reduced signed-subset universe. Its output is root-circuit-check.json and
root-circuit-check.log. Counts (labels, normals, circuits, maximum primitive weight):
(1,2,1,1), (2,6,5,1), (3,11,16,2), (4,20,95,3).
The first three reproduce the stated small-library counts. The fourth is extra
finite evidence and is not proposed as a new manuscript result. Enumeration
supplements the complete symbolic case proof; it does not establish a general
coefficient theorem or the original-coordinate occurrence and repair arguments.

No definite mathematical defect has emerged in these checks. Stage 2 remains
subject to completion of the author audit, five independent reviewers, root
adjudication, and correction of any accepted findings.
