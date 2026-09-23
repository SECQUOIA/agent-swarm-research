# Whole-paper round 1 adjudication

All five independent full-paper reports were received and inspected. They reviewed the complete manuscript, including all proofs and appendices, source-dependent inputs, numerical material, and cross-section scope. Each reviewer reports no major scientific correction under the intended assumptions. The coordinator nevertheless classifies one formal statement omission as **major**, for the reason below. A separate agent will correct every accepted issue, followed by another five-reader whole-paper round.

## Accepted findings

| Finding | Reports | Coordinator assessment and action |
|---|---|---|
| Missing explicit nonnegative curvature scale in `prop:smooth-necessity` | R5.1 | **Major formal statement correction.** Add `kappa_N >= 0` in the proposition. The physical positive-capacity interpretation communicates the intended sign, and the earlier sufficient theorem entails it in that theorem's own hypotheses. However, the standalone necessity proposition does not explicitly import those hypotheses. With an equal mixture of Normal(-N,N) and Normal(N,N), h=0, Q=P, and kappa=-1, its written lower-curvature condition holds while its conclusion fails. The coordinator therefore treats the missing sign as material to the literal theorem, despite the reviewer's minor classification. The proof and physical applications require no substantive change once the sign is stated. |
| Repeat nonnegative curvature in the vector Gaussian model | R1.1 | Valid minor clarification. The scalar model already defines the parameter as nonnegative; repeat the condition in the independently readable vector model rather than relying on its inheritance. |
| “Positive smooth cap” beside the minimum truncation | R1.2, R2.M1 | Valid minor ambiguity. The exponential cap is smooth but the minimum-truncated activity need not be. Use “positive exponential cap”; the existing proof already differentiates only after removing cutoffs. |
| Explain the subsystem's coexistence heat-capacity scale | R5.2 | Valid minor explanatory improvement for the intended reader. Add a concise paragraph restricted to the verified microscopic examples or explicitly controlled second moments. State the leading result `C_S,can/k_B / N^2 -> beta^2 w_- w_+ ell^2`, by total variance and controlled phase moments; within-phase variances are order N (or degenerate). **Do not use an O(N) remainder with fixed limiting weights or nominal centers:** that stronger remainder is not needed and does not follow from the general weak-limit formulation. Explain how secant calibration permits a bath smaller than the full canonical coexistence heat capacity. |
| Restore primary capillarity motivation citations | R5.3 | Valid minor attribution improvement. Verify and cite Biskup–Chayes–Kotecky on fluctuation/droplet competition and Kim–Keyes–Straub on toroidal droplet/strip configurations. Credit only the physical motivation, retaining the explicit fact that neither supplies this manuscript's assumed full density envelope or square-torus microscopic rate. |

R3 and R4 request no corrections. No substantive criticism is rejected. The stronger O(N) remainder suggested as an example in R5.2 is not adopted; the leading asymptotic statement is the warranted and useful form.

## Independent assessment

The coordinator agrees with the reports' checks of the exact physical likelihood, arbitrary-calibration support and two-phase necessity, positive phase-tail sufficiency, short-range contour argument, full microscopic entropy limits, and both global optimization proofs. Numerical checks include distinct direct-density and shared-bath integrations as well as archive verification. The isolated-source LaTeX build also passed.

The required repeat round is triggered by the literal smooth-necessity statement, not by a newly discovered failure of the physical reservoir theorem. No additional research direction is opened. The correction, explanatory addition, and narrow source attribution will all be present before reviewers are dispatched again.
