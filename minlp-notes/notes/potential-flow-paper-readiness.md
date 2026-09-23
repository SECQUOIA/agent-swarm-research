# Potential-flow results and paper-readiness record

Date: 2026-09-06. Status: continuation complete; mathematical and implementation reviews passed, and all 19 consolidated checks passed. Ready for manuscript preparation within the scope below.

The continuation developed the weighted cactus direction, completed an original-instance numerical certificate pipeline, and resolved important distinctions between exact and rational feasible output. It did not start a separate research topic or modify the existing paper manuscripts.

## Main new theorem family

The [joint weighted cactus result](../results/potential-flow-joint-weighted-cactus-accuracy-bits.md) is the principal candidate paper contribution. All statements below allow arbitrarily many cactus cycles. A weighted potential objective has rational coefficients summing to zero, so its value is independent of the potential reference.

| Input model | Reviewed guarantee | Important restriction |
| --- | --- | --- |
| Fixed rational nominations; arbitrary weighted objective; independent continuous resistance intervals | Exact optimal rational resistance profile, computable in polynomial bit time | The global value can be retained as a sum of local quadratic algebraic values; exact comparison of that sum with a threshold is not claimed |
| The preceding model with rational signed arc capacities | The same exact rational optimizing-profile guarantee, or exact infeasibility | This is a cactus theorem; the rank-two series-parallel obstruction below lies outside that class |
| A fixed number of affine load factors; arbitrary objective support; independent resistance intervals | Additive optimization polynomial in input and accuracy bits, with a rational feasible original scenario | No operating filters in the rational-output main theorem |
| Full balanced nomination boxes; fixed objective support; independent resistance intervals | The same accuracy-bit guarantee and rational original-scenario recovery | The face reduction fixes support rather than the number of load factors |
| Fixed load-factor dimension with rational arc capacities | Exact feasibility and additive optimization with algebraic feasible parameters | Tight capacities can exclude every rational parameter |
| Supplied positive capacity slack | Rational recovery feasible for the original capacities | The objective comparison is with the tightened optimum unless an additional optimum-margin assumption is supplied |

The fixed asymmetric-law predecessor remains useful in its own scope: [weighted cactus approximation](../results/potential-flow-weighted-cactus-accuracy-bits.md) and the [affine-family proof](potential-flow-reopened-weighted-investigation.md).

The proof has three distinct parts. The [nomination-face reduction](potential-flow-reopened-weighted-face-reduction.md) contracts blocks whose induced objective coefficients vanish, selects a bounded number of active blocks, and then applies a local perturbation. The [approximation argument](potential-flow-reopened-weighted-investigation.md) replaces local radicals by uniformly accurate rational polynomial pieces before summing. The joint theorem eliminates resistance intervals through a one-equality LP and enumerates local circulation candidates. The fixed-nomination specialization needs only rational arithmetic and quadratic comparisons, rather than the parameter-space real-algebraic optimizer.

Both [first](review-potential-flow-reopened-joint-weighted.md) and [second](review-potential-flow-reopened-joint-weighted-second.md) independent full reviews passed, including the exact rational-profile corollary. The face argument has [two](review-potential-flow-reopened-weighted-faces.md) [separate](review-potential-flow-reopened-weighted-faces-second.md) reviews. The fixed-law compiler has its [own full review](review-potential-flow-reopened-weighted.md). These are internal research-agent reviews, not external peer review or proof-assistant certification.

## Practical computation

The [original-instance envelope pipeline](potential-flow-certified-envelope-pipeline.md) now verifies the graph, original resistance uncertainty, exact envelope construction, energy certificate, and recovered endpoint scenario. The verifier uses only Python's standard library. Its numerical producer uses SOCPs and reports the accuracy actually certified. It has [independent pipeline review](review-potential-flow-certified-envelope-pipeline.md) and [independent goal-certificate review](review-potential-flow-goal-oriented-certificates.md).

The [conservation-aware goal bounds](potential-flow-goal-oriented-certificates.md) reuse an existing energy witness and solve a rational weighted-Laplacian problem. On the deliberately ambiguous-sign benchmark, they reduced the target interval width about 114-fold and the scenario-loss upper bound about 131-fold, without another physical-flow solve. Nine of ten bounded benchmarks certify an exactly optimal endpoint scenario. The cases include 80 edges, a million-to-one coefficient ratio, near-zero flows, and an openly sourced water-network topology under an explicitly documented quadratic adaptation. This is not a calibrated prediction for the source water system or a large-network scalability claim.

The [exact weighted block solver](potential-flow-exact-weighted-cactus-solver.md) implements the fixed-nomination corollary using rational arithmetic and exact quadratic numbers. Its input is a supplied decomposition into independent cycle and bridge blocks; graph-to-block mapping is outside this implementation. This scope must be explicit when presenting its timings or output. The general varying-nomination real-algebraic optimizer remains a theorem rather than an implemented production algorithm.

The solver passed separate [optimization](review-potential-flow-reopened-joint-weighted.md#implementation-audit-exact-fixed-nomination-block-solver) and [arithmetic/input-contract](review-potential-flow-exact-weighted-cactus-arithmetic.md) audits. Checks include 280 exact comparisons with independent LP vertex enumeration, 1,531 high-precision physical profiles, severe radical cancellation, orientation invariance, and malformed input rejection. The root agent also read the complete implementation and the final proof and review records.

## Useful obstructions and safeguards

The [rational-witness boundary](../results/potential-flow-capacity-rational-witness-boundary.md) gives a five-vertex series-parallel example with ordinary positive-width upper capacities and only one variable resistance, where every feasible resistance is irrational. This prevents extending cactus rational-witness claims to all series-parallel graphs. A separate fixed-law cactus example forces an irrational load parameter under capacity filters.

The joint theorem's four-cycle example has a unique exact optimizer with an interior resistance. It proves that checking resistance-box corners does not solve arbitrary weighted potential optimization. Its upper bound and attaining state are verified by exact rational arithmetic.

The same rational-witness result proves the all-graph estimate

```
||x(beta')-x(beta)||_infinity <= 2m M ||beta'-beta||_infinity / beta_lower,
```

where M bounds total positive nomination and both resistance profiles have the stated positive lower bound. This controls rational scenario rounding even at zero and reversing flows. Upper terminal-pressure filters can already be nonconvex on a triangle; they cannot be silently included in a convex capacity formulation.

## Source comparison and contribution wording

The [reopened circuit audit](potential-flow-reopened-literature-audit.md) and [weighted/joint audit](potential-flow-reopened-weighted-literature.md) retrieved and compared additional open primary sources. In particular:

- Gotzes et al. (2016) already give affine-ray quadratic-radical/rational cycle formulas and discuss node-disjoint cycles.
- Aßmann et al. (2018) establish interval-resistance models and single-cycle capacity linearization. Joint load/friction uncertainty also has earlier literature.
- Vigneron supplies an important arrangement and approximate-algebraic-summation predecessor, with inverse-error rather than accuracy-bit complexity in the inspected theorem.
- Classical circuit theory, convex duality, and electrical projections underpin the envelope and certificate components.

No inspected source states the combined weighted cactus guarantees above. This supports a qualified contribution claim, not an assertion of exhaustive priority. Hasler–Wang's 1993 nonlinear tolerance paper remains unread; the EPFL record is metadata-only. Consequently the older single-envelope identity should not be advertised as unprecedented. The new weighted computational theorem, exact optimizing-profile result, and independently checked implementation should carry the paper's contribution statement.

## Reproducibility and remaining boundaries

Run the consolidated checks from the repository root:

```sh
/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/run_reopened_checks.py
```

The runner records commands, outputs, exit codes, timings, and test-source hashes in [reopened_validation.json](../code/potential_flow_mpd/reopened_validation.json). Proof-check scripts retain assertions; acceptance verifiers are also exercised with site packages and assertions disabled. Numerical comparisons, exact finite arithmetic, and universal proof reviews remain distinct evidence.

The final replay passed all 19 commands, including the ten envelope benchmarks and the exact solver example at 80-bit interval precision. The [repository hygiene record](../code/potential_flow_mpd/reopened_hygiene.json) records Python parsing, local Markdown link checks, and a clean whitespace check for the continuation's tracked changes.

The cactus case of the earlier weighted summation problem is resolved. The [general higher-rank block boundary](potential-flow-bounded-block-weighted-obstruction.md) remains open: the face reduction is available, but a corresponding approximation theorem for more general local algebraic value functions is not established. Discrete resistance choices, arbitrary global parameter correlations, cross-cycle operating restrictions, and a scalable numerical implementation of the varying-load optimizer are not claimed. These require additional assumptions or methods; they are not unfinished steps in the proved statements.

The current package is ready for manuscript preparation with those boundaries and source qualifications preserved. No unresolved correctness issue remains from the recorded reviews. I am stopping this continuation because its current proof and certificate directions have reached complete, reviewed statements; the remaining extensions require distinct new methods or application evidence. Further implementation work should be driven by a concrete network, error requirement, and measured bottleneck.
