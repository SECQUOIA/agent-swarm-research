# Dense robust relaxation and exchange polishing on the same kinetic cases

Date: 2026-09-12. The [separate comparison driver](../code/research_20260912/robust_dense_comparison.py)
strengthens both the continuous competitor and the feasible schedules for the
[three-scenario kinetic probe](research-20260912-robust-kinetic-design.md).
The dense Liu relaxation solves tightly and quickly, but its upper bounds
remain wider than the shared-path bounds. Completed single exchanges improve
the hull-generated schedules. Starting exchanges from the dense method's own
rounded visits produces worse feasible designs on both saved cases.

This is a bounded comparison on the original two cases, not a new experiment
grid. All scenario data, offsets, covariance models, priors, counts, and
individual references are loaded from the saved inputs. The accepted core and
robust-design implementation were not changed by this driver. All reported
bounds are floating-point numerical results. The separate module and all
saved witnesses passed a
[fresh independent review](research-20260912-robust-dense-independent-review.md).
The reviewer also checked every final exchange neighborhood and the exact
polished certificate described below.

## Matched dense relaxation

The objective remains `min_s(logdet J_s(S)-c_s)`, with offsets equal to the
feasible individual reference scores. The dense comparator gives every
scenario the same visit vector `z`, with `0<=z<=1` and `sum(z)=k`. Each
scenario uses the accepted Liu evaluator at the fixed scalar split
`a=0.99 lambda_min(R)`. At binary visits it agrees with the original selected
covariance information. The optimizer is a continuous maxmin epigraph
problem, not a MIP.

Let `f_s(z)` denote the scenario's Liu logdet minus its offset, and let
`g_s(z)` be its gradient. For any nonnegative scenario weights summing to one,
the upper bound is

```text
sum_s lambda_s [f_s(z)-g_s(z)^T z]
 + sum of the k largest entries of sum_s lambda_s g_s(z).
```

This follows from the scenario logdet tangents and the exact support function
of the cardinality box. It is valid independently of the epigraph optimizer's
success flag. The driver retains its best completed tangent throughout.

Final tangent weights are strengthened with a small linear program. Introduce
a free threshold `nu` and nonnegative `u_i` satisfying
`u_i >= sum_s lambda_s g_(s,i)-nu`. Minimize the weighted tangent constants
plus `k nu+sum_i u_i` over simplex scenario weights. After solving, the driver
normalizes the weights and recomputes the actual top-`k` support. It does not
treat a potentially inexact LP objective as an upper bound. SLSQP multiplier
weights provide an additional candidate. Both the continuous optimizer and
the final one-thread LP retain a valid earlier witness if capped.

The continuous search starts at uniform visits `z=k/n`. A disclosed shared
feasible incumbent affects only the reported discrete lower bound. It does
not affect the fractional optimization, its rounding, or the independent
polishing of that rounded schedule.

## Stronger feasible schedules

`polish_schedule` starts directly from a supplied complete schedule. It
repeatedly examines all one-for-one exchanges, takes the best improving
exchange, and stops only after checking the final neighborhood or reaching
its cap. A completed local-optimum status refers to the returned path. At a
cap, the best feasible path is returned without a local-optimum claim.

The driver separately polishes the shared-hull incumbent and the dense
method's own top-`k` rounded visits. It also retains the previous completed
greedy result for shared-incumbent comparisons. The two polishing paths are
kept separate: the dense rounding branch does not receive a hull-generated
schedule as its start.

| n | Original hull-generated score | After hull polishing | Dense rounded score | After dense rounding and polishing |
|---:|---:|---:|---:|---:|
| 48 | -0.0942782 | **-0.0897938** | -2.3402441 | -0.1173976 |
| 96 | -0.0892262 | **-0.0840718** | -2.6497962 | -0.0896783 |

These are feasible true fixed-offset maxmin scores; larger is better. Hull
polishing accepts two and five exchanges, respectively, and checks 1,537 and
12,289 robust objective values including the initial score. Its `n=48`
schedule matches the previous greedy result. Dense rounding starts far from a
good discrete schedule, but completed polishing improves it substantially,
accepting 10 and 29 exchanges and checking 5,633 and 61,441 objectives.

Including the numerical individual-reference uncertainty, the polished
hull schedules have worst D-efficiency lower bounds of **96.9355%** and
**97.1196%**. The dense rounding/polishing schedules give 96.0512% and
96.9387%. The original central nominal schedules give 93.6938% and 96.1153%.
The conversion and uncertainty propagation are defined in the original note;
no feasible reference is treated as a proven individual optimum.

Separate exact recertification improves the 96-candidate polished schedule's
standardized interval to `[-0.086007784227,-0.074519785108]`, with exact log
gap `0.011487999119`. Its worst D-efficiency is at least
`exp(-0.086007784227/3)`, approximately 97.173780%. The saved artifact is
[robust-kinetic-n96-polished-certificate.json](../code/research_20260912/results/robust-kinetic-n96-polished-certificate.json).
The [wrapper](../code/research_20260912/certify_robust_polish.py) passes only the
new selection to the reviewed certifier; it recomputes the original-model
information and all reference certificates. This took about 8.18 seconds,
excluding numerical design and polishing. Independent dense calculations
and an exact replay passed. Earlier unpolished artifacts remain available.

## Bound comparison

| n | Dense continuous feasible value | Dense continuous upper | Continuous residual gap | Shared-path true upper |
|---:|---:|---:|---:|---:|
| 48 | 0.03203637 | 0.03204293 | 0.00000656 | -0.08152474 |
| 96 | 0.03505257 | 0.03506056 | 0.00000799 | -0.07285807 |

Both dense epigraph solves report convergence, after 118 and 134 iterations.
Their residual continuous gaps are small compared with the difference between
relaxations. Their positive values are possible because fractional Liu
information can exceed what an exact-count discrete scenario design attains.
Closing the continuous relaxation does not remove that discrete gap.

The table deliberately shows the full dense continuous upper bound requested
for this comparison. For a discrete claim, the already available individual
reference upper bounds are stronger: they imply fixed-offset robust upper
bounds of 0.00346883 and 0.00359700. For normalization by the unknown true
individual optima, the trivial upper bound is zero. Thus the dense upper can
be capped using references, but it still supplies no improvement over those
reference-only caps here. The negative shared-path upper bounds do improve
them. The shared upper bounds include the memory correction and concern the
true original-covariance objective.

With the same best feasible scores, the shared fixed-offset gaps become
0.00826906 and 0.01121369 after polishing. The full dense continuous gaps
remain 0.12183673 and 0.11913232 before applying the stronger reference-only
discrete caps. These figures compare valid bounds with matched incumbents;
they do not attribute the supplied hull schedule to dense rounding.

## Timing with incumbent generation

| n | Shared solver, from original run | Hull polishing | Dense solve | Dense rounding polishing |
|---:|---:|---:|---:|---:|
| 48 | 1.072 s | 0.162 s | 0.0645 s | 0.591 s |
| 96 | 3.655 s | 1.871 s | 0.149 s | 9.946 s |

The dense optimizer alone is fast. Its own completed discrete polishing is
substantial at `n=96`. Individual reference generation costs 2.076 and
9.980 seconds and is required to construct the shared offsets for either
method. Including references, the hull solver and its polishing take 3.311
and 15.507 seconds; the dense solver and its independent rounding/polishing
take 2.732 and 20.075 seconds.

The dense solve's recorded time and cap exclude the work that produced its
supplied shared incumbent. Including references, the original hull run, the
original greedy run, and hull polishing, that incumbent-generation cost is
3.811 and 21.313 seconds. These costs are explicitly saved. The standalone
dense pipeline totals above concern only its independent rounded/polished
schedule; the supplied shared incumbent does not affect that search.
Counting all old generation and new methods gives total accumulated work of
4.467 and 31.408 seconds. Old timings are reused transparently rather than
rerunning accepted artifacts. These are individual local timings, not a
statistically controlled runtime study.

Every dense solve and every polishing invocation has its own 30-second soft
cap. All six new application invocations complete. Each robust score includes
all three scenario covariance evaluations. BLAS and the dual LP use one
thread. Dense array-workspace checks precede dense oracle allocation; the
256-MiB estimate is not a process RSS cap. A numerical operation may overrun
the wall-clock deadline before the next check. Stages and exceptions are
atomically checkpointed.

## Validation and reproduction

The deterministic `n=10,p=2,k=3` validation enumerates 120 schedules across
three scenarios. Shared visits reproduce every binary scenario logdet within
`1.55e-15`. Finite-difference derivatives agree within `2.88e-10`. Tested
simplex tangents, including extreme finite weights, and the dual-weight LP
contain the enumerated discrete optimum. A completed polished schedule passes
all 21 exchange-neighbor checks. An analytic pair of identical scalar
scenarios reproduces the exact `log(5)` bound.

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
code/research_20260912/robust_dense_comparison.py validate \
--output code/research_20260912/results/robust-dense-validation.json

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
code/research_20260912/robust_dense_comparison.py compare \
--source code/research_20260912/results/robust-kinetic-n48.json \
--output code/research_20260912/results/robust-dense-n48.json
```

Use the `n96` source and output names for the second case. Artifacts:
[validation](../code/research_20260912/results/robust-dense-validation.json),
[48 times](../code/research_20260912/results/robust-dense-n48.json), and
[96 times](../code/research_20260912/results/robust-dense-n96.json).
They retain source-input hashes, continuous visits, dual/tangent witnesses,
optimization history, each polishing branch, evaluations under original
covariances, and all timing components.
Source SHA-256:
`b458885e5c848086e181928d3f454469222e1598e5cffc2e677c9ab961201fb3`.

This comparison establishes that the dense scalar-split relaxation remains
loose on these two fixed robust problems, even when solved tightly. It does
not rule out stronger dense formulations, multiple-start exchange search,
other rounding rules, or other robust-design algorithms.
