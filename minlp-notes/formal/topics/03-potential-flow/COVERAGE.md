Source: [`potential-flow-envelope-rational-certificates.md`](../../../results/potential-flow-envelope-rational-certificates.md).

| Claim | Lean location and scope |
|---|---|
| Asymmetric cubic energy and quadratic edge law | `Scalar.lean`: definitions, nonnegativity and monotone law |
| Rational upper roots give a scalar dual bound | `fenchel_root_bound` in `Scalar.lean` (namespace `PotentialFlow`): every real flow, both signs |
| Conservation and incidence transpose identity | `Network.lean`: actual finite directed graph, including loops, parallel edges and disconnected graphs |
| Energy lower bound from arbitrary potentials | `Network.dual_lower_bound`: every feasible flow |
| Cubic Bregman modulus with constant 1/6 | `Modulus.lean`: all real pairs, including sign changes |
| Existence and uniqueness of physical flow | `Optimization.lean`: positive coefficients and one feasible flow suffice; physical equations equivalent to minimization |
| Energy gap bounds flow error | `Certificate.lean`: each coordinate error is at most the certified radius |
| Pressure-drop interval | `certificate_pressure`: evaluate the monotone edge law at the flow-interval endpoints |
| Exact rational checks imply the real hypotheses | `RationalData.lean`, `RationalBridge.lean`: typed exact data, positivity, conservation, roots, gap, minimum coefficient and radius |
| Complete certificate soundness | `RationalNetwork.accepted_sound` in `Results.lean` |
| Saved JSON certificate | `Example.lean`: all original rational data, kernel-checked acceptance; `ExampleResults.lean`: physical flow error below 1/5000 on all six edges |

The statements use the energy and laws of the deterministic network specified
by the certificate. Coordinatewise error bounds give the stated infinity-norm
bound. The minimizing flow is unique; node potentials need not be unique.

Not formalized here:

- The uncertainty-envelope mapping, target selection, or original resistance scenario.
- The endpoint-recovery factor `C0`, refined Bregman certificates, or later original-instance pipeline.
- Numerical producer convergence, conserved rounding, integer-root algorithms, or their bit complexity.
- Correctness of the Python verifier or JSON parser as software; the generator translates data into the separately defined Lean certificate conditions.
- Empirical six-case numerical results and observed floating-point errors.
- A separate exact conjugate-equality theorem. The universal root-enclosure inequality proves the dual bound needed for soundness.

No result is inferred solely from a solver status, Python assertion, or numerical tolerance.

Follow-up: [topic 16](../16-potential-flow-certificates/COVERAGE.md) now verifies
the refined Bregman intervals, conditional endpoint-scenario recovery, support
and curvature certificates, and exact rational root constructions. The exclusions
above describe topic 03 itself; the original uncertainty-to-envelope mapping,
Python implementation and bit-complexity claims remain outside both packages.
