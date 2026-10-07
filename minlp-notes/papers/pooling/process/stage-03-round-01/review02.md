# Stage 3, round 1, reviewer 02

Reviewed `papers/pooling/sections/03-restricted-hardness.tex`, SHA-256 `2d8f3082b7fce0a5da15fac5a3f4d20e44bafbe6b3cf209831e25a0c4b7f44a3`. I read the reviewer protocol, the entire assigned section, the relevant accepted model and certificate dependencies in Sections 1 and 2, the coverage map, and supporting result/investigation files. I did not inspect another current-round report or edit the manuscript.

## Finding: include physical arc capacities in each weighted mode edge

**Severity: minor.** Location: `s3:weighted`, lines 254–256 and 270–274.

The proposition explicitly permits nonnegative integer arc capacities. Its proof then describes the fixed-mode flow problem using input/output vertex capacities and “the pool capacity as an edge bound.” With a restrictive physical feed or outlet bound, that description permits a throughput that cannot be restored to the physical network.

For example, take one pool and its two inputs and two outputs, all with capacity two. Give the clean intake arc capacity one and the other three arcs capacity two, and choose `alpha = 1`, `beta = 0`. The physical optimum is one: strict flow requires zero dirty intake, and clean intake is at most one. The optimal physical point retains the clean mode. The described one-edge flow problem, if bounded only by the pool and endpoint capacities, instead sends two units and cannot be reconstructed feasibly.

**Correction:** Bound the retained mode edge by the minimum of its pool capacity and the upper capacities of its two physical arcs, ignoring an arc bound when it is not imposed. This minimum is integral, so the same capacitated bipartite-flow integrality argument proves the stated result. The theorem is not contradicted; the proof needs this local specification. The unit-capacity rainbow-matching conclusion is unaffected.

## Checks of the assigned focus

- **Continuous cleanup, lines 183–190:** At a positive strict outlet, every contributing quality mass is nonnegative, so its own pool has zero dirty intake. The two replacements decrease every arc flow and preserve `s_v` and `d_v` separately. They therefore preserve profit, including the later signed linked rewards, and need no lower-bound repair because the family has zero flow lower bounds.
- **Integral replacement, lines 192–200:** Fixing one retained mode per pool makes throughput an edge variable in a bipartite capacity problem. The pool bound becomes an individual edge bound because no second mode of that pool remains. Integral node and edge bounds give an integral optimum. The argument does not assume that the original continuous solution was integral, and it does not claim that choosing the modes is easy.
- **Independent-set identity and recovery, lines 202–238:** The conflict graph has exactly the original clean-clean edges of colors 1 and 2, the dirty-dirty middle edges of color 3, and each pool's clean-dirty edge. The exchange deleting `u` and inserting `d_u` when both original endpoints are selected preserves independence and cardinality. The matching property of color 3 makes the exchanges independent. This proves both directions of `alpha(H) = n/2 + alpha(G)` and the recovery bound from any feasible profit. The greedy `alpha(G) >= n/4` estimate yields the stated factor-three loss.
- **Exactly-two degrees, lines 240–250:** Merging the lax outputs adds only a constraint already supplied by the shared dirty input after cleanup. Integral selections, optimum, and recovery remain unchanged; all four physical degrees become exactly two. The endpoint certificate applies to the full stated zero-tolerance decision class.
- **Signed rewards and multigraph scope, lines 254–281:** Cleanup preserves the two reward-bearing quantities separately, so negative rewards cause no problem. Parallel mode edges arise from distinct physical pools and retain their own capacities/colors. No parallel physical arc is required. The rainbow statement concerns the described two-edge-per-pool family, not unrestricted pooling costs. Apart from the arc-bound omission identified above, the extension is valid.
- **Positive tolerance, lines 284–343:** The two cleanup loss bounds, the sum of strict quality inequalities, and the choices `delta = eta^2`, `eta < gamma/32`, `epsilon < gamma/6` give the claimed gap contradiction. The K4 assignment has profit `3 + 2 delta` and satisfies every shared capacity for `0 < delta <= 1/2`. The text correctly avoids an integral-optimum or endpoint-certificate claim at positive tolerance.

## Checks of the rest of the stage

I checked the occurrence-splitting and private-triangle orientation reduction, its bipartite subdivision, both placements in the pooling network, the equality conditions with and without pool capacities, the PARTITION specializations, and the degree-one LP boundary.

For the positive-product route, I checked the determinant bound, cancellation above the largest fractional coordinate, extension of the strict gap by concavity, factor positivity, product expansion, and polynomial coefficient length. The two-pool reduction enforces every simplex row at some active outlet, reconstructs both filled outputs, and has the stated tree topology. Its preprocessing preserves every yes witness. The represented-family FPTAS handles the zero grid, zero optimum, rational vertices, and physical reconstruction without claiming a scheme for arbitrary pooling instances.

For the bypass route, I checked the full and half port equations, chain copying, conversion to actual intake, row signs and complements, padding and averaging, separate closed full/half cycles, coupling, and collector splitting. I checked the error-bound proof through the integral Gram determinant, its application to unscaled contract deficits, the radial outlet repair, the objective comparison, and the additional estimate for the standard economic objective. I found no unsupported use of the equality between a conversion filler and an intake after contracts are relaxed.

For constant data, I checked the least-significant-bit-first dyadic recurrence, denominator clearing and bounded partial sums, the normalization of the source factors, the two-feed quality-mass identity, and physical implementation of the affine threshold. Contract completion reaches its upper bound exactly when all deleted contracts hold, and the common economic offset cancels by conservation. The five-exception transformation uses exact slack comparisons, groups complementary ports without relying on the private supplies for copying, handles supply-four sources when splitting, and leaves exactly the two conversion fillers and anchor as variable inputs. Its exact ordinary product qualities follow from cycle tightness. The fixed quality/flow alphabets, two actual feeds/outlets, external degree bounds, and redundant pool bound survive these steps.

The stage distinguishes ordinary from strong hardness, threshold decision from contracted feasibility, and exact threshold attainment from an approximation or tolerance gap. The Section 1 endpoint certificate and Section 2 fixed-quality/fixed-outlet certificate scopes cover the NP membership claims. I found no material Stage 3 coverage omission relative to the coverage map.

## Sources and independent numerical check

After reading `literature/AGENTS.md`, I checked the local primary-source passages: Chlebík–Chlebíková author manuscript Section 5(A), pages 25–26; Matsui METR95-13, pages 2–7; Asahiro et al., Section 5; the final Haugland 2016 discussion on page 214; Haugland–Hendrix Section 4.5; and Baltean-Lugojan–Misener Remark 4.6. I also visually checked the original PDF page 26 of Chlebík–Chlebíková and pages 3 and 6 of Matsui. The first source explicitly supplies the constructed edge-three-colored cubic graph and gap; Matsui's printed estimate and positive-product factors match the version-specific discussion here. The final scope paragraph accurately separates the simultaneous restrictions from earlier broad assertions.

An independent check compared the original four-flow endpoint-disjunctive LPs with exhaustive integral pure-mode enumeration on 48 deterministic random four-pool instances. Capacities were integers in `{0,1,2}`, linked rewards were signed integers in `{-3,...,3}`, and the construction permitted repeated mode endpoint pairs and restrictive/zero arc capacities. All 48 optima agreed within `1e-8`. This is a small floating-point consistency check, not a proof of the propositions.

The exact code used in the completed inline run is saved as `/tmp/s03r02_signed_weighted_check.py`; captured output is `/tmp/s03r02_signed_weighted_check.log`. Equivalent reproduction command:

```sh
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python /tmp/s03r02_signed_weighted_check.py
```

Compilation is assigned to root and was not repeated here. I did not independently reprove the underlying PCP gap theorem, perform a comprehensive publication-priority search, or validate every historical numerical script. Historical PASS labels were not used as mathematical evidence.

**Verdict: minor findings only.** The one correction above makes the weighted proof cover its explicitly allowed physical arc capacities. I found no major defect in the reviewed stage; this is not a claim of exhaustive correctness or guaranteed external acceptance.
