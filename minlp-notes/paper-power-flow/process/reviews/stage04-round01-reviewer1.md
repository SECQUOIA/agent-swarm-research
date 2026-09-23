# Stage 4, round 1 — independent reviewer 1

## Verdict

No major issue found. One minor reproducibility clarification should be fixed before stage closure. The integrated mathematical statements, literature comparisons, and analytic verification examples pass this review.

I reviewed the frozen `process/snapshots/stage04-round01` input and the stage-4 author report without reading other stage-4 reviews. All 22 manifest hashes match. This report does not substitute for the planned independent whole-manuscript review.

## Required minor repair

**M1 — Specify the minimum Python version.** Location: frozen `README.md:30`, with the requirement arising at `checks/check_resistive_exact.py:27`.

The README instructs readers to use “Python 3,” but `variable: str | None = None` is evaluated without postponed annotations. It requires Python 3.10 or newer; Python 3.9 and earlier cannot import this checker successfully. The developments checker also imports the resistive module. The standard-library-only claim is correct, but does not communicate this runtime requirement.

**Fix:** replace “with Python 3” by “with Python 3.10 or newer.” No compatibility implementation or new dependency is needed.

## Mathematical and source audit

- The abstract, introduction, and conclusion preserve the simultaneous graph restrictions, signed interval data, rational coefficient field in rational universality, and the distinction between real bus-angle lifts, principal line angles, and reference-fixed angle boxes. Size-dependent shrinking cosine bounds are distinguished from the fixed numerical alphabet in the resistive construction.
- The integrated universality discussion retains the corrected basic-closed scope over the rationals and does not restore the invalid general rational-equivalence claim from the Dynamic Toolbox. Arbitrary compact semialgebraic topology is stated through semialgebraic homeomorphism. The accepted arithmetic construction and its singleton field conclusion remain consistent with this scope.
- The quantitative discussion distinguishes a small residual from exact feasibility and distinguishes the promised certificate statement from membership of unpromised exact feasibility in NP. No exact-versus-approximate inference requiring repair was found.
- I checked the primary material for the introduction's DC and AC comparisons. Jeeninga–De Persis–van der Schaft's fixed-source model, unrestricted demand signs, convexity result, and exact/interior matrix alternatives are represented accurately. Gan–Low is credited with conditional relaxation exactness. Lehmann–Grastien–Van Hentenryck and Bienstock–Verma are not presented as proving hardness of the paper's resistive physical subclass. Bienstock–Muñoz's scaled feasibility/optimality approximation scope is preserved. Lavaei–Low is credited for the zero-reactive connection without adopting an unrestricted phase-collapse assertion. The Bienstock–Verma approximation citation now identifies the relevant preprint version.
- All eight legacy formulas were compared directly with `code/power_flow_existential_reals/dc_resistive_build_and_check.py:220–239`. The six feasible instances have the unique listed solutions; the two infeasible instances are ruled out by the stated bounds. In particular, the two irrational solutions are correct and satisfy all interval constraints. The historical AC solver statements accurately describe reported bounds on the sum of squared imaginary voltages; the paper explicitly avoids treating these floating point reports as exact certificates.
- The README, coverage map, verification appendix, and packaging are consistent with the manuscript, subject to M1. They distinguish finite computational checks from proofs and internal reviews from external peer review.

## Independent execution and layout

Artifacts are in `verification/reviewer1/stage04-round01/`.

- Manifest verification: all 22 entries match (`manifest-check.json`).
- All four frozen exact-arithmetic suites pass. Their reported counts agree with the verification appendix: 12,751 resistive profiles; 2,112 scaled AC pairs, 14,784 cosine checks and 177,168 winding cycles; the generalized gadget/subdivision/quantitative cases; and 1,681 composed arithmetic profiles plus full-circuit and simplex checks. The finite scope is stated appropriately.
- The original exact winding checker passes independently (`legacy-winding.log`): 360 scaled pairs, 4,136 closed cycles, including 256 with nonzero winding.
- An independent `latexmk` build produces a 28-page PDF. Its final log has no undefined citations or references, other warnings, overfull boxes, or underfull boxes. The final example table and bibliography were visually inspected and are legible without clipping; rendered pages and build logs are retained.

No additional required repair or optional research extension is proposed in this review.
