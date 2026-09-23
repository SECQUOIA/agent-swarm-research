# Operating-constraint investigation closeout

Date: 2026-09-06.

The complete reviewed statements, proofs, source comparison, and reproduction commands are now in [Rational resistance witnesses under arc capacities and uniform perturbation bounds](../results/potential-flow-capacity-rational-witness-boundary.md).

The investigation began with the distinction between robust testing of all uncertainty scenarios and optimization over scenarios filtered by operating constraints. The existing cactus result already linearizes arc capacities even with globally correlated resistance parameters; this should not be claimed as a new extension.

The coordinating agent proposed a rank-two series-parallel example where an exact target-flow equality forces the only uncertain resistance to be irrational. The investigating agent independently checked it and strengthened it to ordinary positive-width upper capacities by adding a connector and saturating a two-edge cut. This is the main preserved representation boundary.

An initial energy estimate gave a square-root resistance perturbation bound. The independent reviewer sharpened it to a uniform linear bound by identifying a directed cycle of sufficiently large flow differences. The investigating agent separately verified that proof. Strict capacity margins therefore permit rational box-preserving rounding with an explicit linear precision budget; no feasibility algorithm is inferred merely from this witness-size statement.

The exact triangle pressure-filter example is retained as a modest useful negative result. It shows why a general upper-pressure filter cannot simply be appended to the cactus LP. Conductance reparameterization was considered but not pursued as a novelty claim: Klimm et al. (2026), Corollary 4, already proves relevant convex continuous conductance design. Raber (2022), Theorem 3.12, already proves continuity of physical flows in resistances; the quantitative estimate is distinguished from that qualitative antecedent.

Independent review: [full audit](review-potential-flow-reopened-operating-constraints.md). Exact scripts: [construction and scalar checks](../code/potential_flow_mpd/reopened_constraints_exact_checks.py) and [independent review checks](../code/potential_flow_mpd/check_reopened_constraints_review.py).
