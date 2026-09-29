# Publication audit of the fixed-quadratic-count prior comparison

Date: 2026-09-25. Scope: primary-source comparison for the refinement in
[the penalty upper-bound note](penalty-upper-bound.md), not a new proof review.

The current qualification is sound: the note does not claim a new general
few-quadratic value theorem or infer novelty from an unavailable proof.
One addition would make the comparison more precise: explicitly cite the
later paper's application to quadratic programming, not only its general
algebraic machinery.

This recommendation was incorporated in the main note and independently
rechecked in the companion mathematical audit.

## Sources checked

- Grigoriev and Pasechnik,
  [*Polynomial-time computing over quadratic maps I*](https://arxiv.org/pdf/cs/0403008v3),
  Theorem 1.2, printed page 3, gives component sampling with degree and
  coefficient-bit bounds of the stated polynomial form for fixed quadratic-map
  dimension. Theorem 1.5, printed page 4, states exact optimization, including
  unattained infima, but explicitly defers its proof to a continuation.
- Kamminga and Rudolph's
  [ITCS 2026 article](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/LIPIcs.ITCS.2026.83/LIPIcs.ITCS.2026.83.pdf),
  printed page 83:6, reports that the older optimization proof was unavailable
  to the authors. This supports an attributed historical caution; it does not
  establish that no subsequent proof exists.
- Their [full version, arXiv:2411.03096v2](https://arxiv.org/html/2411.03096v2),
  Sections 6.3 and 7.1, equations (98) and (101), gives reduced-variable
  feasibility and optimization formulas. Theorem 7.2 and its proof in Section
  7.2 give algebraic representations with degree and coefficient-height
  bounds. Section 8.5, Corollary 8.14 and equation (115), explicitly applies
  the framework to QCQP with a fixed total number of constraints, without
  convexity assumptions. Its bounded OptGP hypothesis remains relevant.

## Implication for positioning

The source's fixed-total-count setting differs from allowing arbitrary affine
rows. The note's convex affine-face reduction addresses that distinction.
After this reduction, squared slack variables convert the remaining
inequalities to a quadratic-map zero set. The added ball bounds the primal
variables and therefore the slack variables. Thus the general source machinery
is a direct precedent for fixed-count polynomial-height bounds after this
reduction; the comparison should not suggest that the missing older proof
creates an open fixed-count encoding problem.

This observation does not identify the source's full parameter dependence
with the note's sharper explicit exponent linear in the number of nonlinear
rows. Nor does either cited source state the mixed-integer exact-penalty
consequence. Retain the note's qualification that priority for that consequence
has not been established.

Verification consisted of reading the specified primary-source sections and
version histories. No numerical test, project-wide check, or CI inspection
was run. The parent audit owns any changes to the main note.
