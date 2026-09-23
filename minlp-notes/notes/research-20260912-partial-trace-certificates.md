# Exact trace-information certificates for two-mode sensor drift

Date: 2026-09-12. Status: the mathematical bound and the
[certificate implementation](research-20260912-partial-trace-certificate-independent-review.md)
passed separate fresh reviews. Four saved cases have exact relative gaps below
0.0604%. Independent dense covariance inversions and a tuple-history dynamic
program reproduced every saved exact lower bound, upper bound and price.

The [numerical experiment](research-20260912-partial-observation-trace-probe.md)
selects observations of a local consecutive-reaction model under a two-mode
latent drift error. Its covariance is

```text
R_ij = v[(9/25)(2/5)^abs(i-j)+(16/25)(1/5)^abs(i-j)+1{i=j}],
v = 0.00125.
```

This is a fixed scalar observation `(3/5,4/5)` of two independent latent modes,
each with stationary variance `v`, plus independent measurement variance `v`.
The two modes have different transition rates, so this covariance is outside
the original scalar AR(1)-plus-nugget family. The covariance is stipulated,
not fitted to physical measurement data.

The mean sensitivities concern `log(A0),log(k1),log(k2)` at a specified nominal
reaction model. The criterion is the trace of information with identity weight
and prior `0.01 I`. This criterion depends on parameter scaling and differs from
D-optimality. The problem has 48 or 96 candidate times and selects respectively
16 or 32 scalar observations. The early- and late-peak parameter regimes are
defined in the numerical experiment. These remain local-information designs,
with the previously documented global parameter-identifiability limitation.

The new [certifier](../code/research_20260912/certify_partial_trace.py) uses exact
rational two-state Kalman calculations for the local regression coefficients,
innovation variances, and selected information. It recomputes every path price
using the [reviewed outward integer scorer](research-20260912-integer-interval-scores.md).
The cardinality-constrained dynamic program is exact on those integer upper
scores. The fixed prior trace is added once without scaling.

The [normalized partial-observation bound](research-20260912-partial-observation-memory-bound.md)
applies with `gamma=2/5`, signal-to-noise bound `s=1`, and `kappa=1/2`.
For a window of eight, its square-root coefficient is rounded upward exactly:

```text
sqrt(1/2) <= 707106781187/1000000000000,
delta <= 0.0005838858411624957   (display value of the saved rational bound).
```

All information and certificate comparisons use the stored fractions; displayed
decimals are only summaries. In particular, decimal sensitivity data define the
exact certified model, without an implicit exact-ODE sensitivity claim.

| Case | Exact feasible information, displayed | Exact upper bound | Relative gap, rounded upward | Certificate time |
|---|---:|---:|---:|---:|
| 48, early peak | 1944.38027090 | 1945.54540833 | 0.059924% | 0.617 s |
| 48, late peak | 2568.82505160 | 2570.35945882 | 0.059732% | 0.777 s |
| 96, early peak | 3867.26060554 | 3869.59489863 | 0.060361% | 1.314 s |
| 96, late peak | 5101.62865000 | 5104.68579710 | 0.059925% | 1.262 s |

The relative gap is `(upper-lower)/lower`. Hence each selected design has at
least `1/(1+relative_gap)` of optimum trace information for the declared model.
The first certificate ran alone; the remaining three ran concurrently with
BLAS and OpenMP threads limited to one each. These times exclude numerical
design generation. Each certificate uses 256 history patterns. The 48-candidate
cases price 10,495 arcs and visit 96,255 states; the 96-candidate cases price
22,783 arcs and visit 452,607 states.

The numerical comparison reports higher true information than completed
greedy/exchange search on every case and tighter bounds than the tested dense
relaxation. Those comparator values remain floating-point results in a separately
reviewed scope. The exact certificates here concern the selected design and
the full discrete optimum; they do not certify a competing continuous optimum
or establish a general solver-performance advantage.

Inputs and outputs are in `code/research_20260912/results/`:

- `partial-observation-trace-probe.json` supplies all four models and proposals.
- `partial-observation-trace-certificate-0.json` through `-3.json` contain
  self-contained model data, exact bounds, prices, selections, grids and hashes.

For example, reproduce the first certificate from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python code/research_20260912/certify_partial_trace.py code/research_20260912/results/partial-observation-trace-probe.json code/research_20260912/results/partial-observation-trace-certificate-0.json --case 0
```

Use `--case 1`, `2` or `3` for the other cases. The default selects the final
saved dynamic-programming proposal. `--original-bound` retains the earlier,
weaker reviewed partial-observation formula for comparison.
