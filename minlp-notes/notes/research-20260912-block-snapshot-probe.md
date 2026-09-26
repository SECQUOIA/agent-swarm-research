# Full-vector snapshot selection: bounded numerical prototype

Date: 2026-09-12. The new [standalone implementation](../code/research_20260912/block_snapshot_design.py)
maximizes scalar surrogate information by one exact-count dynamic program.
In two small stylized reaction-spectrum cases, it obtains a numerical true
information gap below 0.73%, but greedy selection finds the same schedule and
the dense Liu continuous relaxation gives tighter upper bounds. These results
show that the block dimension can increase without increasing the mask state
count. They do not establish an application or general performance advantage.

The code uses the separately reviewed
[full-block memory bound](research-20260912-noisy-markov-memory.md#full-observed-blocks-after-noise-whitening).
Its floating-point calculations are not an exact rational certificate or a
proof that either application schedule is globally optimal. The theoretical
scope and ongoing prior-work assessment are recorded separately in the
[full-block approximation-scheme note](research-20260912-full-block-design-fptas.md).
No existing reviewed solver was edited.

The [fresh implementation review](research-20260912-block-snapshot-independent-review.md)
passed without code changes. It independently reconstructs covariance blocks,
local conditionals, tiny discrete optima, dense relaxation bounds, kinetic
sensitivities, saved schedules and resource-limit behavior.

## Fixed model and acquisition unit

Selecting one time acquires every coordinate of a `d`-vector observation.
There are `n=24` candidate times `t_j=12(j+1)/24`, exactly `k=8` acquisitions,
and `d=4` or `16` channels. No coordinate within an acquired vector can be
selected separately. The single unknown mean parameter is `log(k1)`.

The mean uses consecutive first-order kinetics with known `A0=1`, known
`k2=0.2`, and nominal `k1=0.7`:

```text
A(t) = A0 exp(-k1 t)
B(t) = A0 k1/(k2-k1) [exp(-k1 t)-exp(-k2 t)]
C(t) = A0-A(t)-B(t).
```

At channel coordinates evenly spaced over `[0,1]`, the three fixed positive
profiles are `exp(-(lambda-center)^2/(2 width^2))`, with centers
`(0.15,0.50,0.85)` and widths `(0.16,0.19,0.16)`. The mean spectrum is the
linear combination of these profiles weighted by the three concentrations,
with path length one. Differentiating this formula gives the channel vector
`F_t = partial m_t / partial log(k1)`. An independent complex-step evaluation
of the mean agrees to below `1e-15` in these cases. The saved files include
times, profiles, concentrations, spectra, and sensitivities.

This is a **stylized Beer-Lambert spectrum and noise model**. It does not use
measured spectra, estimated residual covariances, calibrated channel units, or
published chemical sensitivity data. Time, channel coordinate, and signal
units are normalized model units. Increasing `d` adds observations at the same
per-channel noise level; information values across dimensions therefore do
not have a common normalization.

The zero-mean latent error is a stationary vector recursion with covariance
`P=I`, observation noise covariance `V=I`, and

```text
A = (0.4/2) (cyclic_shift + diagonal(1,-1,1,-1,...))
Q = I-AA^T.
```

Here `A` denotes the transition matrix, separately from species `A(t)` above.
The transition has rational entries before floating conversion, and the
triangle inequality gives `||A||_2 <= 0.4`. In both application dimensions,
the numerical operator norm is `0.4`, the minimum eigenvalue of `Q` is `0.84`,
and `||AA^T-A^TA||_2` is `0.16`. Thus the transition is coupled and nonnormal.
The observed covariance has diagonal blocks `2I`, lower blocks `A^(t-s)`,
and their transposes above the diagonal. Covariance is known and independent
of the mean parameter. A fixed scalar prior `J0=0.01` is included.

Saved decimal matrices specify the numerical inputs. No exact-real claim is
made for the exponential sensitivities or binary floating representation.

## Oracle, dynamic program, and numerical bounds

`SnapshotDesign` owns covariance and true scalar information. The true score is

```text
J(S) = J0 + F_S^T R_SS^(-1) F_S.
```

`BlockCalendarOracle` uses selected observations within the previous `L=6`
calendar positions. For history `H`, it computes and caches

```text
B_H = R_tH R_HH^(-1),   D_H = R_tt-B_H R_Ht,
w_tH = (F_t-B_H F_H)^T D_H^(-1) (F_t-B_H F_H).
```

Stationarity makes the regression and conditional covariance depend only on
the history ages. Each distinct mask therefore requires one block regression
and conditional factorization. The adjusted sensitivity still depends on the
current time. The cache and Cholesky solves preserve the order of history
blocks even though transitions do not commute with their transposes.

`maximize()` uses its own arrays for time, count, and the last `L` selection
bits. It maximizes `J_L(S)=J0+sum w_tH` over exactly `k` selected times and
recovers the maximizing schedule. This is discrete surrogate optimization;
there is no fractional mixture or hull optimization in this prototype.

For `Pbar=rmin=1`, the reviewed finite-series block bound is `0.0090873091`.
The reviewed gain refinement with `kappa=1/2` gives

```text
delta = 2 rho^(L+1)/(1-rho)
        [1 + (1/2) rho (1-rho^L)/(1-rho)]
      = 0.007274321237333336.
```

Neither expression contains `d`. The implementation uses the smaller bound
and sets it to zero at full history `L>=n-1`. When `delta<1`, the surrogate
maximum supplies the prior-aware true upper bound

```text
max_S J(S) <= J0 + [max_S J_L(S)-J0]/(1-delta).
```

The full-selection true information supplies another upper bound by data
processing. The smaller upper bound is saved. The lower bound is the original
covariance score of the recovered feasible schedule. Floating-point matrix
solves and comparisons qualify all reported bounds; no outward rounding or
exact arithmetic is used. If the surrogate dynamic program hits its cap, it
does not report a surrogate optimum or transferred upper bound.

## Comparators and results

The first comparator greedily adds the time with greatest true information,
then repeatedly takes the best improving single exchange. The second
maximizes the shared-block Liu continuous extension, using scalar split
`a=0.99 lambda_min(R)` and repeating each block visit variable over all its
channels. It starts from uniform visits `z=k/n`; the better discrete schedule
from the other methods is disclosed as its feasible lower bound, not as a
fractional optimizer start. Rounding its best fractional visits also yields
a true-evaluated schedule.

For the continuous comparator, a tangent at any evaluated box point gives

```text
upper_log_information = f(z) - gradient^T z
                        + sum of the k largest block gradient entries.
```

This bounds the entire cardinality relaxation and therefore the original
discrete objective. The bound does not rely on the optimizer's success flag.
The best tangent point, gradient, linear price, visits, and evaluation history
are saved for reconstruction. Fractional objective values never serve as
feasible discrete lower bounds.

All three methods select times `0.5,1.0,...,4.0` in both cases. Greedy takes
293 true objective evaluations including its initial feasible schedule and
finds no improving exchange. The application problems were not exhaustively
enumerated. Relative gaps in this table mean `(upper-lower)/lower`.

| Channels | Common feasible true information | DP transferred upper | DP relative gap | Liu continuous upper | Liu relative gap |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.2610185886 | 0.2628579575 | 0.70469% | 0.2616529007 | 0.24301% |
| 16 | 1.5457055982 | 1.5569587178 | 0.72802% | 1.5488857342 | 0.20574% |

| Channels | DP total / pricing seconds | Greedy and exchange seconds | Liu continuous seconds | Estimated workspace |
|---:|---:|---:|---:|---:|
| 4 | 0.0222 / 0.00454 | 0.00898 | 0.00606 | 1.05 MiB |
| 16 | 0.0261 / 0.00440 | 0.0317 | 0.0609 | 14.88 MiB |

These are individual local timings, not statistically controlled runtime
comparisons. Both dimensions have 64 cached masks, a 13,824 count-layer state
upper estimate, and 5,279 visited DP states. Local block algebra and dense
covariance storage increase with channel dimension. The selected schedule's
surrogate-versus-true discrepancies are only `-1.09e-9` and `4.49e-8`, much
smaller than the uniform transfer bound.

The continuous optimizer converges in 21 and 23 evaluations. Its remaining
continuous tangent gaps in log information are `2.50e-7` and `2.78e-8`, so the
reported discrete gaps mainly reflect the fractional relaxation in these
cases. Its fractional variables concentrate at the edge of the selected
window. No MIP is run.

## Validation, limits, and reproduction

The deterministic tiny test uses `n=10,d=3,k=3` and seeded sensitivities from
integer tenths. It enumerates all 120 schedules for each of `L=0,2,6,9`.
Separate dense calculations check local information and the relative
precision spectrum; full history reproduces true information. An independent
innovation-loading covariance construction agrees within `2.78e-17`.
Maximum information and DP residuals are `1.33e-15` and `4.44e-16`.
All 120 Liu binary identities agree within `8.88e-16`; ten finite-difference
gradient checks have maximum error `1.51e-10`. The continuous upper bound
contains the enumerated true optimum. Boundary cases cover one time,
empty/full cardinality, full history, and preflight memory refusal.

Each method has a 30-second cap and a 256-MiB conservative array-workspace
limit. All reported runs finish without exceptions or caps. Checks occur
between operations, so a dense solve or optimizer operation can overrun the
wall-clock deadline. Workspace estimates cover the covariance, local caches,
DP arrays, and dense comparator workspaces; Python, BLAS, and interpreter
overhead are not a process RSS cap. Oversized histories are refused before
covariance allocation; widths above 30 are refused explicitly. Completed
stages and exceptions are checkpointed by atomic JSON replacement.

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
code/research_20260912/block_snapshot_design.py validate \
--output code/research_20260912/results/block-snapshot-validation.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
code/research_20260912/block_snapshot_design.py probe --d 4 --time-limit 30 \
--output code/research_20260912/results/block-snapshot-d4-probe.json
```

Use `--d 16` and the corresponding output name for the second case. The saved
artifacts are [validation](../code/research_20260912/results/block-snapshot-validation.json),
[four channels](../code/research_20260912/results/block-snapshot-d4-probe.json), and
[sixteen channels](../code/research_20260912/results/block-snapshot-d16-probe.json).
Implementation SHA-256:
`85c328d8cab52989a308c90e54008ecc211ecb0ad1bd5b3db39b90f6ea6193ba`.

The [fresh implementation review](research-20260912-block-snapshot-independent-review.md)
of this implementation SHA passed (see the start of this note). No claim of novelty or empirical process-model validity follows
from these small deterministic probes.
