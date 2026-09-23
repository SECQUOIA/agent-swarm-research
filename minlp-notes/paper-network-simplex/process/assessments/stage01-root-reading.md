# Stage 1: root source reading

The root read the accepted cycle/theta, parallel-path, universality, compression,
and observation-rank source proofs, and the paper-readiness and literature audit.
This is preparation for adjudication, not an acceptance of unwritten material.

## Foundational checks

1. With finite capacities, a zero-weight disaggregated state is identically zero.
   Division is needed only for positive weights. At least one weight is positive,
   so the disaggregated system cannot falsely represent an empty flow domain.
2. A reference solution to the balances need not satisfy capacities. The state
   expression is its scaled reference plus a circulation, so the offset cancels
   when state weights sum to one.
3. Undirected simple cycles generate the circulation space, including oriented
   signed cycles. Each belongs to one block. Edge-disjoint block supports give
   a direct sum even at articulation vertices; loops are separate coordinates
   and bridges have zero circulation deviation.
4. Block bounds therefore give a Cartesian product. For a nonempty convex set
   P, nonnegative homothetic copies sum to their total weight times P. Different
   block-local merged label sets can be refined using the same global weights;
   they do not require independent copies of the simplex variable.
5. A hull intersection with additional model constraints is generally only a
   relaxation of the corresponding constrained graph hull. The paper needs this
   scope distinction when discussing applications.

## Source checks and later-stage dependencies

- The open Khademnia–Davarnia abstract confirms that its multivariate forest
  procedure produces an important class, whereas the univariate procedure is
  complete. General extended-hull exactness is already known.
- Kis–Horváth's open article identifies the transportation/subset projection
  precedent in Section 5.7; the cut mechanism should not be claimed as new.
- The root checked De Loera–Onn's open published PDF, Section 3.3, printed p.816:
  the coordinate injection maps every input cell into the third index 1. This
  supplies the first-layer property needed by the later two-state universality
  transfer. The manuscript must explicitly identify this source property.
- The local Davarnia–Richard–Tawarmalani package is a dissertation under a
  journal-style slug. Proposition 2.6 must be attributed to the dissertation.
- The chance-simplex preprint has a locally available v2 dated August 2026;
  an old note's v1 comparison is not sufficient if the final paper cites it.

Primary links inspected:

- https://arxiv.org/abs/2302.14151
- https://link.springer.com/article/10.1007/s10107-021-01652-z
- https://www.math.ucdavis.edu/~deloera/researchsummary/universalitytransportation.pdf

No manuscript finding is adjudicated until the author finishes and the five
independent reports arrive.

## Root reading of the finished Stage 1 snapshot

The root read the complete `sections/01-foundations.tex`, main file, bibliography,
and author record before the independent reports. The proofs correctly retain
the domain and degeneracy distinctions above. No major mathematical defect was
found in this reading.

Provisional minor finding ROOT-1: the final explanation of Example 2.3 should
distinguish a set-level homothetic Minkowski identity from adding arbitrary
right-hand-side representations. In the example the two sets are actually
identical, hence homothetic, but their different redundant-row representations
still aggregate incorrectly. The implemented merger uses one fixed block
representation scaled by each weight. State that explicitly; the current final
sentence could otherwise suggest that equality of the represented domains
alone makes arbitrary RHS aggregation safe. This is an explanatory refinement,
not a defect in the merger theorem or the counterexample.
