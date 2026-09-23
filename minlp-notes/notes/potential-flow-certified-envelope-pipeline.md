# Original-instance certificates for uncertain network arc extrema

Date: 2026-09-06. Status: implementation, exact mechanism checks, and independent pipeline and goal-integration reviews passed. This integrates reviewed results rather than claiming an independently novel envelope theorem.

## What is now certified

[`certified_envelope.py`](../code/potential_flow_mpd/certified_envelope.py) accepts the original oriented graph, fixed balanced rational nominations, independent positive resistance intervals or finite rational sets, a target edge, and maximum/minimum direction. It constructs the deterministic envelope, solves a numerical SOCP, and emits one JSON containing the original instance, an envelope energy certificate, and a recovered endpoint scenario with its own energy certificate.

A separate invocation using Python's standard library verifies the original-instance interpretation as well as numerical error. It does not trust stored envelope coefficients, floating-point adjoint signs, solver status, or a claimed scenario objective. Its output contains:

- a rational interval containing the exact original uncertainty extremum;
- a rational interval containing the selected original scenario's physical target flow;
- a rigorous upper bound on the scenario's target-flow loss;
- when all necessary signs are certified, a proof that the selected rational endpoint scenario is **exactly optimal**, despite the physical state being represented only by an interval.

The implementation supports connected simple loopless graphs with no `K4` minor. The result's multigraph scope is wider than this implementation. Resistance scenarios have no side constraints, and nominations are fixed. The strict schema rejects additional fields such as capacities; silently dropping physical constraints would change the meaning of the certificate.

## Exact construction and graph scope

The checker validates vertex indices, simplicity, connectivity, positivity, dimensions, and exact nomination balance. It repeatedly removes a degree-at-most-two vertex, joining its two neighbors when needed. Acceptance supplies a reverse construction by adding vertices adjacent to cliques of at most two vertices, hence a partial 2-tree and therefore a graph with no `K4` minor. The standard reduction is complete for this graph class. An input outside the implemented scope is rejected.

A grounded all-unit-resistance Laplacian is solved using rational Gaussian elimination. The sign of each rational potential difference gives the unit adjoint current's exact sign. In particular, dangling blocks yield **exact zeros**, not signs inferred from a floating-point tolerance. The already reviewed [adjacent-terminal sign theorem](../results/potential-flow-series-parallel-arc-validation.md) then justifies using these signs for all positive secant resistances. The checker recomputes the maximum/minimum envelope profile, including the target edge's reversed rule, directly from the original allowed endpoints.

The checker next applies the reviewed [rational energy certificate](../results/potential-flow-envelope-rational-certificates.md) and [Bregman interval certificate](../results/potential-flow-envelope-bregman-certificates.md). It invokes the base checker before sharpening intervals. Optional `goal_bounds` data supply full conservation-aware target witnesses for the envelope and selected scenario, using [`goal_flow_certificate.py`](../code/potential_flow_mpd/goal_flow_certificate.py). Each witness includes its validated edge intervals, rational potentials, factor, and radius. The verifier reconstructs the target selector, verifies the witness against the corresponding recomputed law and energy certificate, and intersects the resulting centered target interval with the Bregman target interval. It rejects malformed witnesses and empty intersections. If the producer finds the documented zero-curvature-cycle obstruction, it omits that witness; existing Bregman bounds remain valid. The checker has no numerical dependencies and does not use `assert` for certificate acceptance. Duplicate JSON keys, nonstring rational fields, unknown fields, and Boolean indices are rejected.

## Certified scenario loss and exact endpoint identification

Let `I*=[l*,u*]` contain the envelope target flow, and let `Iβ=[lβ,uβ]` contain the physical target flow for the selected allowed endpoint scenario. Both come from independently checked deterministic energy certificates. For maximization,

```
0 <= optimum - x_a(beta) <= u* - lβ.
```

For minimization,

```
0 <= x_a(beta) - optimum <= uβ - l*.
```

This direct posterior bound avoids the potentially large global factor in approximate-sign recovery. It is valid even when envelope signs remain unresolved. The producer selects the endpoint coefficient agreeing with the rational approximate envelope flow. It reuses that feasible flow and recomputes potentials and the certificate under the original selected law; a second numerical optimization is unnecessary for validity. A poor reused point merely gives a wider certified interval.

There is a stronger termination condition. Suppose each edge's certified envelope-flow interval `[l_e,u_e]` satisfies at least one of:

1. its two envelope coefficients coincide with the selected resistance;
2. `l_e>=0`, and the selected resistance is the positive-side coefficient;
3. `u_e<=0`, and the selected resistance is the negative-side coefficient;
4. `l_e=u_e=0`.

Then the selected original law agrees with the envelope law at the **true** envelope flow on every edge. The full envelope state consequently satisfies the selected original scenario's physical equations. Uniqueness of passive physical flow and the envelope theorem prove that this rational scenario attains the exact original target extremum. Non-strict interval signs are enough because either coefficient yields zero pressure drop at zero flow. There is no exact algebraic sign test or claim to compute the exact physical state. The reported zero loss refers to the selected scenario, not to an exact numerical target-flow value.

This is an elementary posterior corollary of the existing endpoint-attainment argument and certified intervals. Its implementation closes a practical gap; no separate literature-priority claim is made for sign identification or interval subtraction.

## Scale-consistent numerical production

Let `B` be total positive nomination and `C` the largest envelope coefficient. For `B>0`, the producer solves and certifies the normalized problem with `b/B` and coefficients `c/C`. A normalized certificate lifts exactly by

```
flow         -> B flow,
potentials   -> C B^2 potentials,
conjugate roots and energy gap -> C B^3 times their normalized values,
flow radius  -> B radius.
```

These identities follow directly from quadratic laws and cubic energy/conjugate expressions. Exact rational rescaling preserves every checked inequality. The goal witness is also constructed in normalized units: its edge intervals and radius scale by `B`, its potentials stay unchanged, and its factor scales by `1/(CB)`, because its certified curvature scales by `CB`. This preserves exact covariance of final target intervals under common rational changes of flow and resistance units. Normalizing only the numerical solve would leave absolute rational root-rounding error in the original units; that substantially harmed a small-supply experiment. Certifying in normalized units before exact lifting removed this avoidable unit dependence.

The numerical producer uses the existing explicit cubic SOCP lift with CVXPY/Clarabel and rational conservation repair. These are practical solver heuristics, not an implementation of the theorem's polynomial-bit ellipsoid algorithm. It does not accept an accuracy target or promise that a chosen width will be achieved. Extreme coefficient ratios can still give wide bounds or numerical solver failure. Exact verification remains valid whenever it succeeds.

## Reproduction and observed results

From the repository root:

```sh
/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/certified_envelope_benchmarks.py
python -S -O code/potential_flow_mpd/certified_envelope.py verify code/potential_flow_mpd/certified_envelope_example.json
/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/potential_flow_mpd/certified_envelope.py solve code/potential_flow_mpd/certified_envelope_water_topology_instance.json /tmp/water-topology-certificate.json
python -S -O code/potential_flow_mpd/certified_envelope.py verify /tmp/water-topology-certificate.json
```

The benchmark includes maximum and minimum directions, mixed interval/finite resistance sets, reversed orientations, block rank 39 with 80 edges, a million-to-one base coefficient ratio, supply `10^-8`, a dangling cyclic block with zero adjoint currents, zero nominations, and a deliberately ambiguous active-sign case. The two small cases are compared against all 128 endpoint scenarios combined, using a separate circulation-equation numerical solver. Sixteen malformed document classes are rejected in subprocesses with both `-S` and `-O`; the valid example also verifies in that mode. These are mechanism and integration checks, not evidence of large-network scalability.

All ten benchmark cases produced valid certificates; nine certified an exactly optimal endpoint scenario. The raw per-case measurements are retained in [`certified_envelope_benchmark_results.json`](../code/potential_flow_mpd/certified_envelope_benchmark_results.json). With integrated goal witnesses, representative certified target widths are about `1.52e-5` for the 80-edge case and `1.22e-5` for the million-to-one case, versus Bregman-only widths `2.10e-5` and `1.54e-5`. The normalized small-supply case has width `2.16e-15`; certifying directly in original units before the scaling fix gave about `9.71e-10`. The strongest observed improvement is the ambiguous-sign case: its target width decreases from `4.99e-4` to `4.37e-6` (about 114-fold), and its safe scenario-loss bound decreases from `6.92e-4` to `5.28e-6` (about 131-fold), while exact endpoint optimality remains unclaimed. This improvement uses conservation through the curvature-weighted target certificate even though some individual edge intervals contain zero. There is still no second numerical flow solve. Exact goal witness production raises the 80-edge runtime from about 0.9 seconds to 4.6 seconds; verification remains about 0.4 seconds in these runs. Several solves report `optimal_inaccurate`; the rational certificates remain the basis for reported guarantees. Timing includes Python/CVXPY import overhead on the first case and is descriptive only.

## Open external topology adaptation

The benchmark additionally uses the topology and pipe lengths/diameters in [Vrachimis's open EPANET dataset](https://zenodo.org/records/1185136), accompanying [Vrachimis, Eliades and Polycarpou (2018), *Real-Time Hydraulic Interval State Estimation for Water Transport Networks: a Case Study*](https://doi.org/10.5194/dwes-11-19-2018). The downloaded `Vrachimis2018NetDWES.inp` contains 11 nodes and 13 pipes, including a `leak` node subdividing one pipe. Its pipe topology passes the exact graph-scope check. The original node IDs `1,...,10,leak` map to `0,...,10`; pipe order is preserved, and the benchmark target index 7 is original pipe `11`, from node `4` to node `9`.

Only the topology and geometric data are used. The stored adaptation assigns synthetic demands of one unit at original nodes `2,...,10`, zero at `leak`, and supply nine at reservoir node `1`. It assigns the rational quadratic proxy coefficient

```
r_e = (length_e / 1000) (300 / diameter_e)^5,
allowed resistance interval = [0.9 r_e, 1.1 r_e].
```

This is a geometry-inspired quadratic test model. It does not reproduce the paper's demand patterns, measurements, leakage inference, pressure conditions, or Hazen–Williams exponent. Accordingly the result is an external-topology test of the certified optimization pipeline, **not a certified hydraulic prediction for that water system**. The adapted target interval has width about `2.39e-6` (`3.13e-6` before the goal witness), and the selected scenario is certified exactly optimal for this quadratic adaptation. The dataset identifies the University of Cyprus KIOS group as copyright holder and uses EUPL 1.1; its full file is not copied into the repository. The benchmark's transformed factual instance is retained for reproduction with source attribution here.

## Independent review

The [independent pipeline review](review-potential-flow-certified-envelope-pipeline.md) checks graph acceptance against an explicit `K4`-minor definition on all 771 connected labeled graphs with two through five vertices, exact rational states and analytic target values, malformed inputs in ordinary and optimized Python, and scale changes far beyond floating-point range. The [goal-certificate review](review-potential-flow-goal-oriented-certificates.md) separately audits the mathematics and checker for the target witnesses. Integration review also exercises the zero-nomination, positive-gap circulation obstruction; the producer helper was corrected to handle that fallback uniformly.

## Remaining work and limits

The bridge from original uncertainty data to a checked scenario is now implemented. The next practical scale question is whether numerical solving and rational verification remain fast on a broad collection of substantially larger applicable networks. The exact dense Laplacian solve has cubic arithmetic operation count, and per-edge rational interval sharpening can dominate small solves; neither is optimized for large networks. Side-constrained uncertainty, correlated resistance choices, variable nominations, graph classes beyond the theorem, and hydraulic model calibration are outside this implementation. Further work should be driven by a concrete application and required error tolerance rather than a claim that this bounded benchmark establishes deployment readiness.
