# Arbitrary-grid one-switch minimax and sharp grid transfer

Status: complete and independently reviewed. Verified 2026-09-20.

This is topic 17 of the [recommended-topic sequence](../../RECOMMENDED-TOPICS-PLAN.md).
It verifies the exact one-switch minimax value on an arbitrary grid
([Section 8](../../../paper-switching-control/sections/08-finite-grid-one-switch.tex)),
the sharp grid-transfer and certified-coarsening results
([Section 11](../../../paper-switching-control/sections/11-transfer-and-coarsening.tex)),
and the supporting algorithm and certificate claims of
[Section 10](../../../paper-switching-control/sections/10-instance-algorithms.tex)
on which they depend.

The package accounts for all thirty-seven frozen obligations: the thirty-six
mathematical obligations are proved by Lean theorems, and SC29 is recorded as a
scope statement with no theorem. Four independent reviewers, one per tier, found no incorrect theorem; the thirteen
findings they did raise are closed and recorded.

- [Mathematical obligations](CLAIMS.md), frozen before the proofs.
- [Claim-to-declaration coverage](COVERAGE.md).
- [Independent review](REVIEW.md).
- [Verification record](VERIFICATION.md).
- Proof sources: [`Formal/GridSwitching`](../../Formal/GridSwitching).

## Why a new model

[Topic 1](../01-switching-control/README.md) verified exact values on fixed
small unit grids with exactly three modes. Its model is hard-wired: the mode
count is the literal type `Fin 3` and every cell has width one, and most of its
27,641 lines are an exhaustive certificate for a three-mode unit-grid chamber
automaton. This topic needs an arbitrary mode count, an arbitrary strictly
increasing grid and an arbitrary horizon, so it builds a general model in
`Formal/GridSwitching`. Reuse of the earlier package was planned but **not** carried out: no module
here imports or references `SwitchingControl`, so the development is
self-contained over Mathlib. `CLAIMS.md` requires any reuse to be identified in
`COVERAGE.md`; that requirement is met vacuously. An earlier draft of this file
announced three reused assets (`SwitchingControl.Boundary`,
`SwitchingControl.Continuous.endpoint_bound` and the measurable-rates pattern of
`SwitchingControl.Measurable`); that was a plan, not a description, and is
corrected here.

## The identified risk, and how it was resolved

The rounding step inside the sharp-transfer theorem (SC24) requires an integral
assignment whose prefix counts stay within floor and ceiling of the fractional
prefix sums, supported where the cell occupation is positive. The sources obtain
it from integral network-flow feasibility, which the pinned Mathlib cannot
support: it has no max-flow, no circulation theorem, and only the definition of
total unimodularity without the Hoffman-Kruskal integrality consequence. Support
feasibility alone does not imply the prefix bounds, so the statement is global
rather than achievable cell by cell; no particular greedy algorithm is refuted.

It is proved here by **Hall's marriage theorem**. Cells are matched to tokens,
token `(i, r)` being the `r`-th unit interval of mode `i`'s mass line. A cell
is joined to that token exactly when its contribution to the mode's mass line
overlaps that unit interval in positive length. This token-specific overlap
implies the support condition and is essential to the prefix bounds.
Hall's condition is then a mass count. Padding the token count to equal the cell
count turns the injection into a bijection, and it is surjectivity that forces
the lower prefix bounds while injectivity gives the upper ones.
