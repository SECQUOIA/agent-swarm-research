This package verifies the small-grid switching-control results from
[Section 9](../../../paper-switching-control/sections/09-three-mode-floor-chambers.tex).

For three modes, the selected results are the exact worst-case errors below,
expressed in units of cell width:

| Cells | Switch budget | Error |
|---|---|---|
| 5 | 2 | 1 |
| 6 | 3 | 1 |
| 7 | 3 | 4/3 |

The final statements apply to every positive cell width, measurable relaxed
inputs, and every time throughout the horizon. The continuous three-mode,
two-switch value is also exactly `T/5` for every positive horizon.

The proof separates universal upper bounds from matching lower-bound inputs.
`Profile.lean` represents cumulative allocations at times 1 through N, with
nonnegative coordinates, conservation, and coordinate increments between zero
and the elapsed time. `History.lean` proves that every strict profile belongs
to the enumerated floor histories. `Finite.lean` defines the enumeration; `Certificates.lean` supplies actual schedules,
checked by Lean, for every ordinary history. `Geometry.lean` handles the six
exceptional seven-cell histories. `Boundary.lean` proves that the bounds extend
to all profiles with integer endpoint coordinates. `Results.lean` combines
these components. `Sharpness.lean` provides the endpoint lower bounds. `GridResults.lean`
assembles exact full-time grid values; `ContinuousResults.lean` assembles the
continuous two-switch result. `Measurable.lean`, `MeasurableWitness.lean`,
`GridRates.lean`, and `GridWitnesses.lean` connect these claims to actual
Lebesgue integrals of measurable rates.

The [generator](generate_finite.py) produces the finite proof trees. It is not
trusted as a proof checker: each generated schedule and every branch of the
coverage tree must pass Lean's kernel. The checked statements establish
coverage by schedules, rather than relying on the original Python program's
reported chamber counts or dynamic-programming cost histograms.

Proof sources are in [`Formal/SwitchingControl`](../../Formal/SwitchingControl).

This package is specific to three modes on small unit grids. The general
theory — arbitrary mode count, arbitrary grid, arbitrary horizon, with the
exact one-switch minimax formula and sharp grid transfer — is verified
separately in [topic 17](../17-grid-switching/README.md), which builds its own
model independently over Mathlib and does not import this package. The
earlier reuse plan was not carried out; topic 17's coverage record documents
that deviation from its frozen obligations.
The coverage and verification records in this folder state the final checked
scope and any paper claims left outside it. The [verification record](VERIFICATION.md) records the completed checks.
