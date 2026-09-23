# Weighted-trace design with two partially observed latent drift modes

Date: 2026-09-12. The [new standalone driver](../code/research_20260912/partial_observation_trace_probe.py)
optimizes a finite-history weighted-trace surrogate by one dynamic-programming
price. On four fixed kinetic sensitivity arrays, history length eight gives
numerical true-information gaps of 0.1304–0.1311%. Its schedules improve on
greedy selection followed by single exchanges in every case. The generic dense
Liu continuous relaxation is faster on these small inputs but gives wider
0.9438–1.8741% gaps even after receiving the same feasible incumbents.

These are small deterministic probes under a specified noise model, not a
general performance comparison or an experimental validation. The
[partial-observation theorem](research-20260912-partial-observation-memory-bound.md)
has passed [fresh independent proof and numerical review](research-20260912-partial-observation-independent-review.md).
The new driver has also passed a
[fresh independent implementation review](research-20260912-partial-observation-trace-independent-review.md),
including reconstruction of all six saved DP and four dense bounds and all
5,120 final greedy exchange neighbors. Results here use floating-point
arithmetic. Separate [exact certificates](research-20260912-partial-trace-certificates.md)
give gaps below 0.0604% using the sharper normalized bound. The reviewed solver
and kinetics modules were reused without edits. The dense comparator's recorded
time excludes generation of its supplied shared incumbent.

## Model and criterion

The centered latent state has two coordinates:

```text
X_t = diag(0.4,0.2) X_(t-1) + w_t,
Y_t = (3/5,4/5) X_t + v_t,
P = sigma^2 I_2,
Q = sigma^2 diag(0.84,0.96),
r = Var(v_t) = sigma^2 = 0.00125.
```

The initial state is stationary. Process and observation errors are mutually
independent, Gaussian, known, and independent of the mean parameter. The
observed covariance is

```text
R_ts = sigma^2 [(9/25) 0.4^|t-s| + (16/25) 0.2^|t-s|]
       + sigma^2 1[t=s].
```

Both latent modes contribute to the single measured packet. This covariance
is outside the one-mode scalar AR(1)-plus-nugget family: its successive
positive-lag covariance ratios are not constant. It represents a **stylized
two-mode latent drift**, with no calibration against measured process errors.
The pointwise observation-error standard deviation is `0.05` in normalized
concentration units. Each selected time acquires the entire scalar packet;
there is no channel-selection decision.

The mean and its analytic sensitivities come from the separately reviewed
[early- and late-peak kinetic probe](research-20260912-noisy-markov-kinetics-probe.md):

```text
B(t) = A0 k1/(k2-k1) [exp(-k1 t)-exp(-k2 t)],
A0 = 1,
early peak: k1=0.7,  k2=0.2,
late peak:  k1=0.18, k2=0.045.
```

The unknown coordinates are `log(A0), log(k1), log(k2)`. The supplied
`n`-by-3 sensitivity matrix is the derivative of this mean at the stated
nominal parameters. The earlier independent sensitivity review used augmented
mass-balance and sensitivity ODEs; this driver also records the analytic
generator's complex-step check. The original local-design caveat remains:
observing `B(t)` with unknown `A0` leaves a global ambiguity under swapping the
two rates and adjusting `A0`.

There are `n=48` or `96` candidate times `12(j+1)/n` over a fixed horizon of
12 model time units. Exactly `k=n/3` are selected. Holding per-grid latent
correlations `0.4` and `0.2` fixed as `n` changes also changes both physical
correlation scales; the two resolutions do not share a fixed continuous-time
covariance model.

The criterion is weighted trace information,

```text
T(S) = tr[W (J0 + F_S^T R_SS^(-1) F_S)],
W = I_3, J0 = 0.01 I_3.
```

It is not conventional A-optimality, which minimizes a trace of inverse
information. Trace information depends on the chosen parameter coordinates
and weight; the stated log coordinates and `W=I` are fixed throughout this
probe. The positive prior contributes the constant `0.03`.

The artifact records the sensitivity, prior, and weight arrays and the full
rational latent model: `P=rI=I/800`, transition entries `2/5,1/5`, observation
row `3/5,4/5`, and innovation diagonal `21/20000,3/2500`. Saved decimal
sensitivities define the numerical input. No claim is made that these decimals
are exact real exponential sensitivities or physical measurements.

## One price and the transferred upper bound

`TwoModeDesign` supplies covariance and original information to the unchanged
`CalendarOracle`. The oracle conditions a selected observation on selected
times within its preceding `L` calendar positions. It uses the corresponding
true regression, conditional variance, and adjusted mean sensitivity. This
gives positive semidefinite local information increments `W_arc`.

Since the weight is fixed, one call `oracle.price(W)` maximizes
`sum tr(W W_arc)` over the exact-count bitmask graph. Its value excludes the
fixed prior. There is no fractional hull or logdet iteration in this driver.
The selected schedule is re-evaluated using the original two-mode covariance.
A separately evaluated evenly spaced initial schedule is retained if better.
The saved artifact distinguishes this feasible incumbent from the surrogate
optimizer and verifies recovery of the surrogate value.

For the partial-observation theorem, `Pbar=r=sigma^2`, `q=0.84 sigma^2`,
`hbar=1`, hence `gamma=sqrt(1-q/Pbar)=0.4`, `C/r=1`, and `B=1`. The reviewed
bound specialized to this model is

```text
delta_L = 2 [ gamma^(L+1)/(1-gamma)
              + gamma^(L+2)(1-gamma^L)(1-gamma^(L+1))
                / ((1-gamma)(1-gamma^2)) ].
```

It equals `0.008047072625644889` at `L=6` and
`0.0012895332172498742` at `L=8`. Full history `L>=n-1` is exact and uses
`delta=0`. The original scalar-AR(1) spectral correction is not called.

If the price finishes and `delta<1`, the prior-aware bound is

```text
max_S T(S) <= tr(W J0) + price(W)/(1-delta).
```

The driver also computes the full-selection true information bound and saves
the smaller upper bound. Every lower bound comes from a feasible size-`k`
schedule under the true covariance. The theorem is exact under its assumptions;
these evaluations of it and of the DP are floating-point calculations without
directed rounding. A cap does not produce a surrogate-optimal status or a
transferred upper bound from an unfinished price.

## Results and comparators

Greedy selection repeatedly adds the time with highest true trace score, then
takes the best improving single exchange until no such exchange remains or
its cap expires. The dense comparator uses the Liu extension with scalar
split `a=0.99 lambda_min(R)` and one visit per scalar packet. Its weighted
trace derivative is `V_i W V_i^T/a`, with
`V=(I+(R-aI)diag(z)/a)^(-1) F`.

A tangent at any evaluated visit vector gives the continuous upper bound

```text
f(z)-gradient^T z + sum of the k largest gradient entries.
```

SLSQP starts at uniform visits `z=k/n`, with objective scaling by the
full-selection score. The better DP/greedy schedule is explicitly supplied as
its discrete lower bound. Top-`k` rounding of its own fractional visits is
also evaluated, but is worse than that supplied schedule in every case. Thus
the dense method's reported feasible score should not be attributed to its
rounding rule. No MIP is run.
The recorded dense time and cap exclude the DP and greedy work that generated
its supplied discrete incumbent.

Relative gaps below are `(upper-lower)/lower`. “Greedy loss” uses
`(DP true score-greedy true score)/(DP true score)`; it is a loss against the
reported DP schedule, not against an independently known true optimum.

| n | Regime | L | DP true score | DP upper | DP relative gap | DP seconds |
|---:|---|---:|---:|---:|---:|---:|
| 48 | Early peak | 6 | 1944.380271 | 1960.418078 | 0.82483% | 0.0565 |
| 48 | Early peak | 8 | 1944.380271 | 1946.920028 | 0.13062% | 0.2243 |
| 48 | Late peak | 6 | 2568.825052 | 2589.937511 | 0.82187% | 0.0687 |
| 48 | Late peak | 8 | 2568.825052 | 2572.175547 | 0.13043% | 0.2380 |
| 96 | Early peak | 8 | 3867.260606 | 3872.328972 | 0.13106% | 0.6750 |
| 96 | Late peak | 8 | 5101.628650 | 5108.292535 | 0.13062% | 0.6845 |

| n | Regime | Greedy/exchange true score | Greedy loss | Greedy seconds | Liu upper | Liu relative gap | Liu seconds |
|---:|---|---:|---:|---:|---:|---:|---:|
| 48 | Early peak | 1942.490223 | 0.09721% | 0.2339 | 1978.472003 | 1.75335% | 0.0519 |
| 48 | Late peak | 2545.806146 | 0.89609% | 0.0765 | 2593.070902 | 0.94385% | 0.0457 |
| 96 | Early peak | 3860.405646 | 0.17726% | 1.6463 | 3939.736352 | 1.87408% | 0.1370 |
| 96 | Late peak | 5062.520467 | 0.76658% | 3.8479 | 5152.585974 | 0.99884% | 0.1752 |

All six DP calls and all four greedy/exchange runs finish. The greedy
improvement loops accept respectively 7, 1, 8, and 22 exchanges. The schedules
and their selected times are saved. At `n=48`, lengths six and eight return
the same true scores. The `L=8` selected schedules' surrogate-minus-true
discrepancies are only `0.0292,0.0336,0.0749,0.0766` information units; the
uniform correction is conservative for these particular schedules.

The dense optimizer reports convergence on the first three cases and reaches
its 200-iteration cap on `n=96`, late peak. Its remaining continuous tangent
gaps are `0.00512,0.00805,0.01064,0.02872`, respectively, or about
`2.59e-6,3.10e-6,2.70e-6,5.57e-6` relative to its best continuous value.
These residuals are small compared with the reported discrete gaps. The saved
upper bounds come from tangents and do not rely on optimizer success flags.

Both methods are inexpensive at these sizes. DP improves the upper-bound
quality and the greedy schedule here; dense continuous optimization takes less
time. Four chosen sensitivity arrays, individual local timings, and a
specified two-mode covariance do not establish broad algorithmic superiority.

## Validation, resource limits, and files

The deterministic tiny validation uses `n=10,k=3,p=3`, seeded integer-tenth
sensitivities, and all 120 schedules at `L=0,2,6,9`. An independent latent
innovation-loading construction verifies the observed covariance to
`2.71e-20`. Direct local transforms verify information and the normalized
residual spectrum. Full history reproduces original information, and each
DP result agrees with exhaustive surrogate optimization. Maximum information
or DP residual is `2.27e-13`.

The weighted Liu formula is separately checked with a non-diagonal positive
semidefinite weight. All 120 binary identities agree within `4.55e-13`;
finite differences have maximum absolute gradient error `3.22e-7` at an
information scale of roughly `10^3`. Every enumerated binary score lies below
the tested tangent. The continuous bound contains the enumerated true optimum.
Boundary tests cover one time, zero/full cardinality, full history, deadline
refusal, and memory refusal before objective allocation.

The array-workspace estimates are 0.653 MiB for `n48,L6`, 2.153 MiB for
`n48,L8`, and 6.458 MiB for `n96,L8`, below the 256-MiB limit. Their
count-layer state upper estimates are 52,224, 208,896, and 811,008.
The memory estimate includes covariance and solver workspaces but is not a
Python-process RSS cap. Widths above 30 are refused before exponential arrays
or covariance allocation. Each method has a five-second cap, checked between
numerical operations, so a single operation can overrun it. There are no
time-cap or exception records in this saved application run; the dense
iteration cap remains recorded.

The application driver shares each greedy/dense comparison across memory
lengths for the same data. It atomically checkpoints after every solve and
records exceptions without discarding completed stages. It saves all model
data, theorem status, source hashes, DP selections and arc traces, dense
fractional visits, tangent witness, optimizer history, and resource limits.

Run from the repository root with one BLAS thread:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
code/research_20260912/partial_observation_trace_probe.py validate \
--output code/research_20260912/results/partial-observation-trace-validation.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
code/research_20260912/partial_observation_trace_probe.py probe \
--output code/research_20260912/results/partial-observation-trace-probe.json
```

Artifacts: [tiny validation](../code/research_20260912/results/partial-observation-trace-validation.json)
and [application probe](../code/research_20260912/results/partial-observation-trace-probe.json).
Driver SHA-256:
`8a85b6b4f1a5e879d96a912a8375c0bf0b19b7da828883ce9c942f3d23fa44d3`.
Further implementation review, exact arithmetic certification, and empirical
residual-model validation are separate work.
