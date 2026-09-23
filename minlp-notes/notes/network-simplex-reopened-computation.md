# End-to-end sparse network–simplex computations

Date: 2026-09-07. Status: initial experiments complete; independent code review
and additional validation completed. These experiments verify an implementation and compare formulations.
They do not establish computational superiority or literature priority.

## What was implemented independently

The scripts in [code/network_simplex_benchmarks](../code/network_simplex_benchmarks/)
implement three independent LP models, using SciPy HiGHS and sparse matrices:

1. The full disaggregated hull: one flow for each of the `m+1` simplex vertices,
   with scaled capacity and flow-balance constraints. Aggregate flow and observed
   products are projected from those state flows. Optimization eliminates the
   explicit aggregate-flow and product variables from this baseline, so its size
   does not include avoidable copies of these variables.
2. The McCormick relaxation in the original `x,y,z` variables, with original flow
   and simplex constraints. Valid separator cuts can be added to this model.
3. A compressed exact formulation built directly from generator metadata. It
   retains the original variables and uses `(k_B-1)*a_B` auxiliary circulation
   coordinates per parallel-path block. It eliminates the merged residual
   coordinates by subtracting the explicit state coordinates from the aggregate
   coordinates. Its construction does not use the separator's preprocessing,
   reference flow, interval computation, or coefficient generation.

The benchmark also invokes the separately implemented
[general compressed EF](../code/network_simplex_compressed/), including its own
graph preprocessing. It agrees with both independent formulations in all six
optimization cases and all three membership cases.

The third baseline matters: comparing only with the full disaggregation could
confuse the benefit of state grouping with a benefit of cutting planes.

The baseline incidence convention is outgoing-minus-incoming. The separator uses
incoming-minus-outgoing; the adapter negates balances explicitly.

## Workloads and checks

The generator creates articulation-linked parallel-path blocks, with bridges
between blocks, random capacities, heterogeneous arc orientations, and nonzero
balances induced by an interior reference flow. Each block observes three state
labels and three edges for each observed label. Independent random streams keep
graph data and observed-edge patterns unchanged when the simplex size changes.
This includes multiple
observations on the same path, an important consistency constraint.

Optimization uses fixed random linear objectives on flow and observed products.
Each of three graph sizes is solved both with free simplex weights and with all
explicit weights fixed to `0.9/m`. Fixing weights represents external conditions
that restrict a block in a larger model and forces nontrivial disaggregation.
With free weights, standalone linear optimization over the hull admits an
optimizer at a simplex vertex. Those cases test cuts and preprocessing but do
not represent a difficult application solve.
The hull remains the block hull intersected with the fixed-weight conditions; we do not
claim it becomes the hull of the original graph under arbitrary side constraints.

The six optimization cases have 8, 17, and 43 edges and 8, 32, and 128 explicit
simplex states. Fixed seeds are 31, 32, and 33. The membership cases have 51 edges,
36 observations, and 16, 128, or 1024 explicit states, with seed 41. Membership
points are exact mixtures of different feasible state flows, constructed by
opposite signed path perturbations around the interior reference flow.

For every optimization case:

- Full and compressed extended formulations must have matching optimum values.
- A cut loop starts at the McCormick optimum, adds the separator's returned cut,
  and solves the LP again until the exact separator certifies membership.
- **Every generated cut is independently audited by maximizing its violation
  over the full extended hull with free simplex weights.** Thus the audit checks
  global validity numerically to an absolute tolerance of `1e-7`, including when
  the tested candidate has fixed weights. Exact arithmetic applies to separator
  cuts and decomposition checks, not to the numerical LP support audit.
- At termination the cut-loop objective must match the full hull optimum.
- The exact decomposition is checked state by state: arc bounds, all balances,
  the aggregate flow identity, and every observed product identity.

HiGHS outputs are rationally reconstructed with denominator at most one million;
reconstruction error must be below `1e-7`, and all aggregate balance equations
must hold exactly before calling the exact separator. A failed reconstruction
raises an error instead of being counted as a hull violation. These checks are
appropriate for the small-denominator synthetic inputs here; they are not a
certified general LP-to-rational reconstruction algorithm.

Before the full pipeline, an additional 40 independent full/compressed EF
optimization comparisons passed on seeds 0–19, with both free and fixed weights.
An independent subagent then verified 120 additional support cases with new
seeds, nonzero simplex objective coefficients, paths of length 1–4, 2–6 paths,
no/full/bridge observations, and free, zero, vertex, or random fixed weights.
The maximum objective difference was `4.974e-14`; 360 recovered-point full-EF
membership checks and 360 general compressed membership checks also passed. See the [independent review script](../code/network_simplex_review/check_benchmark_baselines.py).

## Initial results

The six optimization cases all match the full hull optimum to `1e-7`. There are
85 generated cuts in total, including 23 transportation-subset cuts. Every cut
passes the independent support-optimization audit, and every terminal point has
an exactly verified decomposition.

| Edges | States | Weights | McCormick objective | Hull objective | Cuts |
|---:|---:|:---|---:|---:|---:|
| 8 | 8 | Free | -11.545392 | -10.766035 | 3 |
| 8 | 8 | Fixed | -3.182322 | -1.942398 | 16 |
| 17 | 32 | Free | -13.740528 | -13.465009 | 1 |
| 17 | 32 | Fixed | -3.275195 | -2.932457 | 18 |
| 43 | 128 | Free | -20.251810 | -17.370765 | 5 |
| 43 | 128 | Fixed | -7.287862 | -6.981917 | 42 |

For the 43-edge instance, the full extended formulation has 5,675 variables,
9,160 rows, and 34,689 matrix nonzeros. The independent compressed formulation
has 255 variables, including 48 auxiliaries, 225 rows, and 1,004 matrix nonzeros.
The final original-variable LP has 207 variables and 142 rows for free weights,
or 179 rows for fixed weights.

**Negative result:** the compressed EF is faster than the repeated cut loop in
all six cases. The initial run gives approximately 2–5 milliseconds for the
compressed EF, versus 9–319 milliseconds for preprocessing plus all separator
calls and cut-loop LP solves. On the largest fixed-weight instance, cutting also
loses to the full EF (about 319 versus 189 milliseconds). These are single-run
measurements on small synthetic models, not stable performance estimates.

The result supports using the compressed formulation as the default computational
method on these workloads. Original-variable cuts remain useful when avoiding
auxiliary variables is itself valuable, or when only selected blocks/cuts are to
be added to a much larger model. Their advantage in those settings is still
untested.


## Membership comparison with both baselines

The exact separator and the general compressed LP both accept every constructed
mixture. The separator's returned decomposition passes the exact audit. Times
below include preprocessing/model construction and the membership solve.

| Explicit states | Full EF, ms | General compressed EF, ms | Exact separator, ms |
|---:|---:|---:|---:|
| 16 | 30.28 | 6.44 | 4.29 |
| 128 | 218.13 | 7.85 | 9.76 |
| 1024 | 2876.21 | 11.49 | 16.79 |

The improvement over full disaggregation is substantial in this small study, but
there is **no consistent speed advantage over the compressed LP**. The exact
separator supplies an exact constructive certificate; the LP membership check
is numerical. The comparison cannot separate algorithmic effects from Python
implementation costs and model-construction overhead. A production benchmark
should compare repeated solves after preprocessing and use representative
application models before asserting practical speedups.

## Reproduction and measurement limits

Run:

```bash
python code/network_simplex_benchmarks/run.py --output code/network_simplex_benchmarks/results.json
```

`--quick` uses only the smallest graph's two optimization cases and the first two
membership sizes. The JSON records objectives, sizes, cut families, timings, and
Python/NumPy/SciPy versions. Reported aggregate times are sums of selected
implementation components; they are not literal total wall-clock times minus
audits, because small bookkeeping and assertion costs are also excluded.
LP timings include Python sparse-matrix construction and HiGHS solution.
Separator preprocessing is recorded separately. The reported cut-loop time
includes original LP construction, LP solves, separator calls, rational point
reconstruction, and cut conversion/addition, but excludes independent validation
of cuts and decomposition audits. Matrix-byte counts include input CSR arrays only,
not peak memory, solver factors, or process memory. The exact rational separator
runs in Python; the LP engine is compiled HiGHS. No conclusion about an optimized
native separator follows from these timings.

The networks are synthetic. As discussed in the concurrent literature audit,
the large complete-bipartite transportation experiments of Khademnia–Davarnia
lie outside the parallel-path graph class. The two-supplier, many-demand
transportation topology does belong to this class and motivates the generator,
but these instances are not taken from a published application dataset.

## Observed-rank elimination and repeated measurements

A second, materially changed formulation eliminates independently observed cycle
coordinates. The general implementation exposes `eliminate_observed=True`; the
original compressed formulation remains available with `False`. On the largest
optimization graph, it removes 33 of 48 auxiliaries, leaving 15. On the membership
graph it removes 31 of 60, leaving 29. The counts reflect observation rank, so
repeated observations on one path do not each eliminate a distinct coordinate.

The [repeated runner](../code/network_simplex_benchmarks/repeats.py) compares full
disaggregation, the initial general compressed EF, the formulation with observed
coordinates eliminated, and the exact separator. It uses the same three
membership cases and the largest fixed-weight optimization case, with **five
recorded repetitions after warming up each case**. Membership method order is
rotated across repetitions. Each repetition rebuilds every formulation. This
measures construction plus solution, not repeated callbacks against a persistent
LP model. All returned optima agree within `1e-7`; membership and final optimizer
decompositions are checked exactly. The largest case's 42 cuts receive a fresh
once-only numerical full-EF validity audit; these expensive audits are not
repeated during the timing repetitions.

The following entries are median milliseconds, with the observed minimum and
maximum in parentheses. They are descriptive measurements of these fixed
synthetic cases, not confidence intervals or asymptotic claims.

| Membership states | Full EF | Initial compressed EF | Observed coordinates eliminated | Exact separator |
|---:|---:|---:|---:|---:|
| 16 | 29.97 (24.62–42.35) | 4.40 (4.33–6.72) | 5.53 (5.33–8.18) | 4.15 (4.01–7.39) |
| 128 | 233.23 (208.25–327.42) | 5.38 (5.36–8.89) | 6.42 (5.76–10.44) | 4.97 (4.83–9.66) |
| 1024 | 3229.37 (2751.47–8398.78) | 13.45 (12.58–398.16) | 13.96 (11.48–341.20) | 13.66 (10.87–378.69) |

For the largest fixed-weight optimization case:

| Method | Variables | Rows | Median total ms (range) | Median build ms | Median solve ms |
|:---|---:|---:|---:|---:|---:|
| Full EF | 5675 | 9160 | 193.58 (181.25–300.42) | 158.40 | 41.45 |
| Initial compressed EF | 255 | 225 | 6.35 (5.41–14.97) | 3.90 | 2.74 |
| Observed coordinates eliminated | 222 | 192 | 7.62 (6.39–7.96) | 4.74 | 2.68 |
| Original-variable cutting | 207 | 179 | 278.21 (268.42–472.90) | See component data | See component data |

Build includes symbolic preprocessing, matrix construction, and bound conversion;
solve is the HiGHS call. Total also includes minor result-adapter costs. Medians
of individual components need not add to the median total. The cutting method
rebuilds and solves an LP 43 times and performs 43 separator calls; the JSON
records those components separately. It does not implement persistent-model
warm starts or batched cuts.

**The additional elimination reduces formulation size, but it does not improve
median total time in these cases.** In the optimization case the initial
compressed EF has 936 matrix nonzeros versus 839 after elimination; its CSR input
arrays shrink from 12,140 to 10,844 bytes. The eliminated formulation's added
construction work outweighs the small solve reduction. At 1,024 membership states,
original variables dominate the model, so removing 31 auxiliaries changes total
variables only from 1,171 to 1,140. These limitations are useful evidence against
claiming that fewer auxiliary variables alone guarantee faster solution.

The repeated results strengthen the initial practical conclusion: compact state
and cycle formulations are preferable to full disaggregation on this sparse
synthetic workload. The exact separator and the compressed LP have similar
membership runtimes. Original-variable cutting and extra algebraic elimination
need application-specific justification beyond these measurements.

Reproduce the five repetitions with:

```bash
python code/network_simplex_benchmarks/repeats.py
```

The complete timing components, ranges, formulation counts, and software versions
are in [repeated-results.json](../code/network_simplex_benchmarks/repeated-results.json).
The numerical optimizer still uses the previously described small-denominator
rational reconstruction adapter; these experiments do not turn general floating
point LP optimization into an exact optimization algorithm.

## Fixed-two-state flat chains: repeated comparison

The final bounded extension tests the exact circuit oracle for the
[flat-chain fixed-state theorem](../results/network-simplex-flat-chain-fixed-states.md).
This is a different graph class: a serial chain of parallel pairs, all in
parallel with one bypass arc. Each arc has unit capacity and the source-to-sink
flow is one. It is covered by the new flat-chain oracle, not by the earlier
parallel-path-block separator. There are two explicit simplex states throughout;
therefore even the full disaggregated EF has size linear in chain length.
**Full disaggregation is included as a fair comparator.**

For each length 8, 32, 128, or 512, one feasible and one outside point are tested.
Both use exact rational simplex weights `(1/2,1/2)` and observe one product per
gadget, alternating the observed state. The feasible point is an explicit
mixture of two different flows: branch profile `(1/4,1/4)`, aggregate arc flows
`(1/4,1/4)`, bypass flow `1/2`, and small opposite state allocations within each
gadget. The outside point has aggregate gadget flows `(3/10,1/5)`, bypass flow
`1/2`, and each observed product equal to `3/10`. Every individual product
satisfies McCormick. Yet the alternating observations require both state branch
flows to be at least `3/10`, while their sum is `1/2`, so their incompatibility is
joint. These are controlled verification workloads, not sampled application
instances or a diverse hard-instance collection.

The [flat-chain runner](../code/network_simplex_benchmarks/flat_repeats.py) compares
full EF, initial general compressed EF, observed-coordinate elimination, and the
exact flat-chain oracle. All methods agree on all eight cases. LP checks of
outside points require HiGHS status 2 (infeasible), so a numerical or iteration
failure cannot pass as a correct rejection. Each case has one warmup followed by five recorded repetitions, with method order rotated. Every
feasible exact decomposition is audited outside the timed components. Each of
the four outside cases also receives a once-only numerical full-EF support audit
of the returned cut, with tolerance `1e-7`.

The 41-circuit library's cold construction cost is recorded separately:
**22.32 ms**. It is cached during the repeated measurements. The first
feasible warmup also retains the lazy profile-basis setup cost in the JSON;
its first call requesting separation and decomposition took
2.27 ms. Separation without a decomposition and separation with a decomposition
are timed as two separate workloads. Their times are not subtracted to estimate
an isolated decomposition cost.

Entries below are median total milliseconds, with minimum and maximum in
parentheses. Total includes a fresh graph/model constructor for every method,
plus matrix construction and solving for LP methods; circuit-library cold time
is the separately reported one-time cost.

| Gadgets | Point | Full EF | Initial compressed | Observed coordinates eliminated | Exact flat oracle |
|---:|:---|---:|---:|---:|---:|
| 8 | Feasible | 2.51 (2.49–2.74) | 2.62 (2.58–2.73) | 3.46 (3.36–5.66) | 0.40 (0.39–0.48) |
| 8 | Outside | 3.34 (2.27–3.60) | 2.52 (2.33–3.99) | 3.71 (3.09–5.32) | 0.43 (0.39–0.71) |
| 32 | Feasible | 5.92 (5.55–6.05) | 6.35 (6.12–6.78) | 14.22 (10.34–17.89) | 1.29 (1.18–2.23) |
| 32 | Outside | 7.54 (5.52–9.49) | 9.03 (7.67–10.13) | 11.94 (9.24–16.35) | 1.62 (1.21–2.18) |
| 128 | Feasible | 19.53 (17.06–28.18) | 20.07 (19.87–24.63) | 54.87 (48.53–77.63) | 5.89 (5.02–8.48) |
| 128 | Outside | 20.98 (16.23–22.29) | 22.20 (17.55–26.61) | 61.00 (53.81–78.28) | 4.65 (4.38–7.09) |
| 512 | Feasible | 83.63 (69.73–96.01) | 108.38 (94.55–126.75) | 433.36 (410.21–463.29) | 18.83 (16.85–19.63) |
| 512 | Outside | 76.06 (70.13–92.42) | 90.80 (70.57–95.93) | 434.58 (408.11–482.81) | 20.72 (18.84–23.13) |

For the feasible 512-gadget case, asking the exact oracle for a decomposition
raises its median total from 18.83 to 22.20 ms. The returned
three-state representation is checked against every balance, capacity, observed
product, and aggregate-flow identity; the zero-weight residual state is omitted.

**The exact oracle is faster when construction and solution are timed together, but
these measurements do not show superiority over a prebuilt LP.** In the largest
feasible case, full-EF matrix construction has median 72.09 ms and the HiGHS
call has median 11.05 ms, whereas the exact oracle's online call has median
18.21 ms. The compiled LP solve itself is faster here. Reusing the fixed LP
matrix across points, persistent-model warm starts, or a native implementation
could change the comparison. No asymptotic runtime superiority follows: both
methods already have linear-size data at two explicit states.

The full membership baseline retains all three state blocks, including the
zero-weight residual block in these cases. Presolve can fix those variables,
but explicit removal before matrix construction could further reduce baseline
setup cost. That optimization was not measured. The reported comparison is
against the documented full-EF implementation, not the best possible LP adapter.

The size comparison also exposes a limit of compression. At 512 gadgets, fixed
point full-EF membership uses 3,075 flow variables and 3,076 equality rows. The
general compressed model keeps original coordinates and uses 2,565 variables
(including 1,026 auxiliaries) and 7,176 rows. Observed-coordinate elimination
reduces those counts to 2,053 variables (514 auxiliaries) and 6,664 rows, but its
extra exact algebra makes setup substantially slower: approximately
415 ms in the feasible case. With only two explicit states, state grouping
has little to merge, and the generic compressed formulation is not the strongest
implementation baseline. This negative result supports choosing a method from
the actual observation pattern and workload, rather than using auxiliary counts
alone.

The benchmark uses exact input points directly; it does not require the
small-denominator reconstruction adapter used in the earlier optimization
experiments. The LP comparisons and cut support audits remain numerical.

Reproduce with:

```bash
python code/network_simplex_benchmarks/flat_repeats.py
```

All constructor, matrix-build, LP-solve, exact-online, and exact-decomposition
workload timings are in
[flat-repeated-results.json](../code/network_simplex_benchmarks/flat-repeated-results.json).
