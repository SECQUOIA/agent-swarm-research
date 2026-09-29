# Near-submodular exact optimization: research screen

Date: 2026-09-28. This branch produced useful negative results and a focused
literature comparison, but no substantial positive theorem or complexity
classification. None of the results below should be promoted as a main
original contribution.

- [One-positive-edge obstructions](one-edge-obstructions.md) gives exact
  four-variable counterexamples to restoring support submodularity merely by
  fixing exceptional indicators, and to quasiconvexity or unimodality of the
  scalar Stieltjes-majorant envelope. The obstructions persist on a frustrated
  signed cycle outside the established sign-switchable class.
- [PSD-center obstruction](psd-center-obstruction.md) shows that replacing the
  stable-positive-diagonal condition by positive definiteness of the positive
  principal block does not preserve SDP–RLT exactness. A particularly simple
  counterexample follows directly from Burer–Natarajan–Willemsen's prior
  four-variable example. An independently discovered exact rational witness
  is retained as supplementary evidence.
- [Literature audit](near-stieltjes-literature-audit.md) separates the known
  sign-switchable one-positive-edge case from the unresolved frustrated case,
  and records why discrete-domain backdoors, tree-structured supermodularity,
  and stationary-point algorithms do not resolve the continuous-indicator
  question.

The exact polynomial-versus-hardness classification for a convex indicator
quadratic with one positive off-diagonal pair remains unresolved in this
investigation. A missed result under another formulation remains possible.
The most immediate next step would be a new structural idea for the
frustrated case; repeating scalar search or binary-endpoint branching would
not address the demonstrated obstructions.

Targeted verification is recorded in the individual notes. No project-wide
verification or CI inspection was performed.

An [independent adversarial review](obstruction-independent-review.md)
checked all substantive obstruction claims with separate exact calculations
and found no defect. This supports correctness of the finite counterexamples,
not novelty or a general complexity classification.
