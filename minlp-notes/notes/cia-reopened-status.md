# Switching-control research continuation

Date: 2026-09-07. Status: complete. The [paper-readiness record](cia-reopened-paper-readiness.md) is the final coverage map for this continuation. It supersedes earlier active or stopped-task labels for the CIA topic only.

The objective is to develop practically useful, correct results and prepare the current switching-control material for a paper. New claims must receive independent mathematical review, appropriate exact or numerical checks, and a qualified comparison with openly accessible primary literature before promotion. Internal agent review is not external peer review; numerical experiments do not establish universal statements.

## Completed work

| Direction | Final disposition |
| --- | --- |
| Finite-grid minimax | [Explicit exact one-switch formula](../results/cia-finite-grid-one-switch-minimax.md) on every rational nonuniform grid; constructive extremizers and independent mathematical/code reviews. |
| Practical rounding | [Exact one-switch and fixed-budget algorithms](../results/cia-fixed-switch-budget-algorithm.md), repeated modes, minimum dwell times, public-profile benchmark, and independent exact enumeration. |
| Grid transfer | [Sharp switch-preserving transfer](../results/cia-sharp-grid-transfer.md), binary nonuniform refinement, and a counterexample to the source's half-grid argument. |
| General switching budgets | [Stronger seeded bound](../results/cia-seeded-arbitrary-switch-bound.md) and one new plateau case; the exact higher-budget formula remains open, with the failed event relaxation retained. |
| Small-grid boundary | [Exact five-cell result](../results/cia-five-interval-two-switch-minimax.md) contradicts a published lower-bound corollary; independent integer enumeration and source audit passed. |
| Sources | [Completed primary-source audit](cia-reopened-literature.md), including the full dissertation and final published article; known ingredients credited and priority qualified. |

No retained claim is awaiting review. The remaining questions are explicitly unresolved, rather than prerequisites for the retained results. Internal agent review is not external peer review, and numerical experiments do not establish universal statements.

## Scope discipline

The established continuous exact formulas concern one switch with at least three modes, two switches with at least four modes, and three switches with at least five modes. General bounds use fewer activation blocks than modes. Finite-grid formulas, freely placed continuous switches, repeated-mode schedules, and schedules requiring distinct modes must be distinguished. Application constraints such as dwell times or restricted transitions are not silently added to a theorem.
