# Network–simplex continuation

**Historical continuation record.** Subsequent manuscript development and
stronger baseline comparisons are documented in
[the paper folder](../paper-network-simplex/README.md). Its sharper results
and current computational conclusions supersede the closeout statements below;
the original investigation record is retained.

Started and completed 2026-09-07 at the user's request. Status: complete.
The [paper-readiness record](network-simplex-paper-readiness.md) is the final
closeout and supersedes the active-work labels below, which preserve the plan.

## Objective and scope

Make the sparse network–simplex hull results ready for a paper, prioritizing
practical value and correctness. The underlying model has a bounded
equality-constrained network-flow polytope, a simplex variable, and selected
bilinear product coordinates. It is distinct from passive potential flow and
physical pooling. Existing paper folders are outside the editing scope.

The prior completed results are `results/network-simplex-cycle-theta-hull.md`,
`results/network-simplex-parallel-path-hull.md`, and
`results/network-simplex-universality.md`. General polynomial-size disaggregated
extended hulls and polynomial separation are already known.

## Completed work allocation

- Complete graph-to-cut separator, exact rational certificates and constructive
  recovery: `code/network_simplex/`.
- Independent extended-formulation baseline and computational experiments:
  `code/network_simplex_benchmarks/` and
  `notes/network-simplex-reopened-computation.md`.
- Bounded block cycle rank, explicit coefficient bounds and a finite support
  library: `notes/network-simplex-reopened-bounded-rank.md`.
- General series–parallel networks and possible coefficient obstructions:
  `notes/network-simplex-reopened-series-parallel.md`.
- Sparse blockwise extended formulation with suppressed degree-two paths:
  `notes/network-simplex-reopened-compressed-hull.md`.
- Open-primary literature comparison:
  `notes/network-simplex-reopened-literature.md`.

Candidate results were not accepted merely because an author reported a proof.
Each retained theorem and substantial implementation received independent
subagent review, corrections, and relevant exact/numerical verification.
Computational comparisons must distinguish the exact extended hull from weaker
relaxations and must not claim stronger bounds than the same exact hull.

The final closeout distinguishes proved results, measured performance,
qualified priority assessments, useful negative findings, and remaining open
questions. No external messages or manuscript submissions are authorized.
