This topic verifies simplex disaggregation and exact sparse-product hull tests
for flat chains from the [foundations](../../../paper-network-simplex/sections/01-foundations.tex)
and [fixed-state chain section](../../../paper-network-simplex/sections/07-fixed-state-chains.tex).

The general theorem proves that convex-hull membership is equivalent to a sum
of scaled feasible flows, one for each simplex vertex. It includes an explicit
convex decomposition, zero state weights, and empty flow systems. The original
simplex convention, nonnegative coordinates with sum at most one, is connected
to full weights by adding the residual state.

For a chain of arbitrary length, the proofs connect the actual network incidence
equations and observed products to a common state profile. After eliminating the
unobserved residual state and grouping repeated inequalities, membership is
equivalent to the original-domain checks, the zero-row check, and:

| Explicit labels | Exact remaining criterion | Main theorem |
|---|---|---|
| 2 | Five interval inequalities | `mem_hull_iff_five_tests` |
| 3 | Sixteen inequalities | `mem_hull_iff_sixteen_tests` |
| 3 | Equivalent sixteen positive-circuit combinations | `mem_hull_iff_circuit_tests` |

The theorems are in [`Results.lean`](../../Formal/NetworkSimplex/Results.lean),
under `NetworkSimplex.Chain.ReductionData`. The b-arc flow is represented as
`1 - xh - xa`, using its original flow balance. Observation patterns are arbitrary;
the residual state is unobserved. Recovery is proved through profile feasibility,
state flows, and a convex combination of graph points.

The [coverage table](COVERAGE.md) maps claims to proofs and records exclusions.
The [verification record](VERIFICATION.md) contains the checks. All sources are
in [`Formal/NetworkSimplex`](../../Formal/NetworkSimplex). Run
`bash scripts/verify.sh` from `formal/` for the complete project check.
