The separate prototype
[`noisy_markov_design.py`](../code/research_20260912/noisy_markov_design.py)
implements the calendar-memory information model, exact-count linear pricing,
surrogate hull optimization, and a transferred upper bound for the **true**
discrete log-determinant objective. Tiny exhaustive checks pass. The bounded
synthetic comparison below shows usable certificates at moderate correlation,
while also showing why the stronger dense baseline must be retained. No priority
or general performance claim is established.

The implementation assumes fixed scalar sensitivities, stationary covariance
`R[i,j] = P rho^|i-j| + r 1[i=j]`, `P>=0`, `r>0`, and a positive-definite fixed
prior. It selects exactly k of n candidate indices. The theory supports other
constraints, but they are not implemented in this prototype. The older
`markov_design.py` and path-oracle code were not edited. The adjacent
[README](../code/research_20260912/noisy-markov-design-README.md) documents the
APIs and reproduction commands.

For each calendar index and preceding-L-bit mask, the choose-arc matrix uses
the exact local conditional variance and the adjusted sensitivity
`F[t] - b @ F[history]`. The skipped history is marginalized when forming those
local conditionals. Skip arcs contribute zero. An additional count state makes
the linear-pricing problem exactly the size-k path problem. The code uses a
longest-path dynamic program with predecessor recovery.

At a feasible mixture matrix M, with H=M⁻¹, the completed dynamic program gives

```text
U = logdet(M) - p + trace(H J0) + max_path sum_arc trace(H W_arc).
```

This is an upper bound on the surrogate hull optimum. SLSQP refines the convex
weights on the generated paths. Its numerical completion is not used as a
global certificate: the tangent and completed dynamic program supply that
bound. Every priced path considered as an incumbent is reevaluated using the
original selected covariance. `hull_optimal_tolerance` closes only the surrogate
hull gap; `true_optimal_tolerance` requires the true upper and lower bounds to
meet the requested tolerance. The saved result distinguishes both gaps.

The implementation uses the accepted sharper bound from the
[memory theorem](research-20260912-noisy-markov-memory.md). With η=P/(P+r),

```text
δ = (2P/r) ρ^(L+1)/(1−ρ) [1 + η ρ(1−ρ^L)/(1−ρ)],
```

where ρ is the absolute transition coefficient. Full history `L>=n−1`, zero
latent variance, and zero correlation have δ=0. If δ<1, the first true upper
bound is `U − p log(1−δ)`. A final additional pricing step retains the prior:
at `N=J0+(M−J0)/(1−δ)`, price with arc gradient `N⁻¹/(1−δ)` and form
`logdet(N)−p+trace(N⁻¹J0)+price`. The returned true upper bound is the minimum
of these two bounds and the exact full-selection objective. If δ>=1, the
implementation retains only the full-selection bound. All arithmetic remains
floating point, with the associated numerical qualification.

The same-data dense comparator uses Liu's binary-exact concave extension with
the full noisy covariance. The baseline takes `a=0.5 λmin(R)` and no root cuts.
The strengthened run takes `a=0.99 λmin(R)` and up to 200 LP outer-approximation
rounds before the integer phase. LP feasible values never update the integer
lower bound. Both phases share the same per-run time budget. The strengthened
run receives the best true-evaluated path from the two hull runs as a disclosed
MIP start; its reported time excludes those earlier hull runs. This makes the
incumbent input explicit rather than crediting its discovery to the dense solver.

The saved [validation report](../code/research_20260912/results/noisy-markov-design-validation.json)
passes these checks:

- All 4,095 nonempty subsets of each of five n=12 cases satisfy the spectral
  bound, including signed correlation, L=0, and full history: 20,475 checks.
- Exact-count pricing matches enumeration; surrogate and transferred true
  upper bounds enclose the corresponding enumerated discrete optima.
- The dense binary extension matches original covariance objectives on every
  size-four subset of those cases. Both dense configurations solve a separate
  eight-candidate case to its enumerated optimum.
- Cardinalities zero, one, and n, iteration and time caps, oversized-memory
  refusal, and invalid subset inputs have the intended behavior.

The [independent solver review](research-20260912-noisy-solver-independent-review.md)
also reconstructed saved pricing witnesses and checked the implementation with
another state representation. Its final sweep passed 40 hull solves, 32 dense
solves, 160 linear prices, and 80 root-fractional comparisons, among its other
checks. These numerical checks support the finite implementation, not a proof
about floating-point rounding errors.

The fixed benchmark uses seeded Gaussian sensitivities, p=3, `P=r=1`,
`J0=0.1 I`, ρ=0.4, k=n/3, and one thread. Every individual invocation has a
five-second limit. The
[complete benchmark JSON](../code/research_20260912/results/noisy-markov-design-benchmark.json)
includes the sensitivity matrices, input parameters, final mixture weights and
path matrices, both bound witnesses, all solver statistics, and source hash.
The main results from that run are:

| n, k | Method | True lower bound | True upper bound | True gap | Seconds |
|---|---|---:|---:|---:|---:|
| 12, 4 | Memory L=4 | 1.526184 | 1.685203 | 0.159020 | 0.010 |
| 12, 4 | Memory L=6 | 1.526184 | 1.576864 | 0.050681 | 0.013 |
| 12, 4 | Dense baseline | 1.526184 | 1.526184 | <1e−6 | 0.841 |
| 12, 4 | Dense strengthened | 1.526184 | 1.526184 | <1e−6 | 0.022 |
| 24, 8 | Memory L=4 | 5.730882 | 5.868659 | 0.137776 | 0.011 |
| 24, 8 | Memory L=6 | 5.730882 | 5.752434 | 0.021552 | 0.032 |
| 24, 8 | Dense baseline | 5.730882 | 6.171873 | 0.440991 | 5.008, capped |
| 24, 8 | Dense strengthened | 5.730882 | 5.730882 | <1e−6 | 0.032 |
| 48, 16 | Memory L=4 | 7.696650 | 7.836860 | 0.140210 | 0.061 |
| 48, 16 | Memory L=6 | 7.696650 | 7.719338 | 0.022688 | 0.183 |
| 48, 16 | Dense baseline | 7.643142 | 8.804426 | 1.161284 | 5.009, capped |
| 48, 16 | Dense strengthened | 7.696650 | 7.721273 | 0.024624 | 5.008, capped |

All six surrogate hull gaps closed below `1e−6`. The memory runs did not close
their true discrete gaps. Enumeration independently establishes the n=12
optimum; the strengthened dense run also closes the n=24 gap. No discrete
optimality is claimed for n=48. The stronger split and root phase remove the
large apparent advantage against the initial dense baseline on the smaller
examples. At n=48 the memory certificate is slightly tighter within this capped
run. This single synthetic seed is insufficient for a performance conclusion.

For these inputs, δ is `0.04521984` at L=4 and `0.007274321237333336` at L=6.
The prior-aware step improves the n=48 L=6 upper bound by only
`0.0001746334`; most of the certificate comes from the uniform theorem and
surrogate tangent. The threshold table below uses n=48, k=16, p=3 and the
default allowance for up to 101 stored paths. Its memory figures include a
conservative dense-covariance workspace estimate, not just mask states.

| ρ | Target δ | First L | Actual δ | Masks per stage | Estimated workspace, MiB |
|---:|---:|---:|---:|---:|---:|
| 0.4 | 0.05 | 4 | 0.045220 | 16 | 1.19 |
| 0.4 | 0.01 | 6 | 0.007274 | 64 | 1.57 |
| 0.6 | 0.10 | 8 | 0.087545 | 256 | 3.07 |
| 0.6 | 0.05 | 10 | 0.031662 | 1,024 | 9.07 |
| 0.6 | 0.01 | 13 | 0.006853 | 8,192 | 65.07 |

The preflight memory guard runs before covariance allocation. Its default
workspace limit is 256 MiB; an initial refusal returns null bounds rather than
inventing an unevaluated incumbent. Python/BLAS runtime memory and already
supplied inputs are outside this estimate, so it is not a hard RSS limit. Time
caps are soft around indivisible linear algebra, preprocessing, and return
operations. Stronger correlation or a denser physical time grid may require
prohibitive memory. Sensitivity generation, covariance-parameter estimation,
multivariate partial observation, and larger-design scaling are outside this
prototype's validated scope.

A bounded extension uses n=48 and 96, seeds 0, 1, and 2, L=6 and 8, and the
same p=3, k=n/3, ρ=0.4, `P=r=1`, and `J0=0.1 I`. Its
[driver](../code/research_20260912/noisy_markov_extended_benchmark.py) atomically
checkpoints the [extended results](../code/research_20260912/results/noisy-markov-extended-benchmark.json)
after every solve, including an exception record if a solve fails. Each new
invocation has a five-second cap. The n=48, seed-zero L=6 and strengthened-dense
records were reused after exact input, source-hash, cap, and initial-selection
matches; this reuse is recorded in the JSON. No exceptions occurred.

| n | Seed | L=6 true gap | L=6 seconds | L=8 true gap | L=8 seconds | Strong dense true gap at 5 s |
|---:|---:|---:|---:|---:|---:|---:|
| 48 | 0 | 0.022688 | 0.183 | 0.004360 | 0.617 | 0.024624 |
| 48 | 1 | 0.021774 | 0.189 | 0.003532 | 0.687 | 0.018007 |
| 48 | 2 | 0.024188 | 0.203 | 0.005535 | 0.701 | 0.025648 |
| 96 | 0 | 0.021803 | 0.846 | 0.003502 | 2.639 | 0.034121 |
| 96 | 1 | 0.021816 | 0.784 | 0.003529 | 2.439 | 0.018460 |
| 96 | 2 | 0.022091 | 0.472 | 0.003449 | 1.721 | 0.023567 |

All twelve surrogate hull runs closed their hull gap below `1e−6`; none closed
the true gap. All six dense runs reached their time cap, with the same true
lower bound as the best hull incumbent supplied to them. Thus the table
compares upper-bound strength at a common feasible value, with the cost of
finding that value reported separately. L=8 gives a tighter true upper bound
than the capped dense solver in all six cases. The strengthened dense solver's
fast exact closures at n=12 and n=24 remain part of the record. This extension
adds three seeds within one deliberately narrow model family; it does not
establish broad scalability, novelty, or discrete optimality at n=48 or n=96.

Run the extension with:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/noisy_markov_extended_benchmark.py
```
