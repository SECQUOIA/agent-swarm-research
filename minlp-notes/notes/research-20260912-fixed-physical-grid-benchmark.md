# Fixed physical covariance and fixed measurement budget under grid refinement

**The current memory implementation met a numerical logdet-gap target of 0.01 on the 48-point grid, but did not retain that performance on the 96- or 192-point grids.** A smaller-window diagnostic at 96 points, followed by the already reviewed tighter error transfer, obtained a gap of 0.03710 in about 28.05 seconds. This is tighter than the tested dense OA implementation, while remaining above the target. These results identify a practical scaling limitation of the current representation and implementation; they do not prove that this problem requires exponentially large memory or that better algorithms cannot certify it.

Status: author run complete; the benchmark and refined transfer passed [fresh independent review](research-20260912-fixed-physical-grid-independent-review.md). The [driver](../code/research_20260912/fixed_physical_grid_benchmark.py) and [complete checkpointed artifact](../code/research_20260912/results/fixed-physical-grid-benchmark.json) preserve every run, input, status, bound, timing, and source hash. No reviewed solver core was changed. This investigation directly addresses the fixed-physical-grid test proposed in the [impact assessment](research-20260912-impact-assessment.md).

## One physical model and one budget

The nominal mean is the same stipulated fast consecutive-reaction model used in the existing kinetic probes:

\[
B(t)=\frac{A_0k_1}{k_2-k_1}(e^{-k_1t}-e^{-k_2t}),
\qquad A_0=1,\quad k_1=0.7,\quad k_2=0.2.
\]

The three mean parameters are \(\log A_0,\log k_1,\log k_2\), with prior information \(0.01I\). The existing analytic sensitivity generator includes its complex-step check. Candidate times are \(t_j=12(j+1)/n\), and **every grid selects exactly 16 distinct observations**. There is no additional sampling-gap, installation, or packet restriction.

All grids share the same stipulated observation covariance in physical time:

\[
R(t,u)=\frac1{800}e^{-\lambda|t-u|}+\frac1{800}\mathbf1_{t=u},
\qquad \lambda=-16\log(4/5).
\]

The resulting adjacent latent correlations are

\[
\rho_{48}=256/625=0.4096,\qquad
\rho_{96}=16/25=0.64,\qquad
\rho_{192}=4/5=0.8.
\]

These rational values are stored as exact strings. Each coarser grid is a subset of the finer grid under `fine_index=(fine_n/coarse_n)*(coarse_index+1)-1`. The driver verifies the exact rational covariance nesting and bit-identical saved sensitivity rows at shared times. Increasing \(n\) therefore changes the available observation times, while holding the physical mean, covariance, horizon, prior, and measurement budget fixed.

The covariance is synthetic and known in this benchmark. It is not an estimated experimental covariance. This remains local mean-information design at nominal parameters, with the previously documented global rate-swap ambiguity outside the criterion's scope.

## Budget and comparator design

For each grid, a shared greedy construction followed by best single-exchange search receives at most five seconds. It completed on all three grids. Each memory or dense pipeline is charged the measured data construction, preflight calculation, and shared heuristic generation. It then receives the remaining portion of a nominal 30-second pipeline budget.

The memory method calls the unchanged `solve_hull`, including oracle construction, seed evaluation, and pricing within its timer. It uses the core's existing scalar bound, not the newer refined bound. The common heuristic supplies an additional feasible lower bound after the solve; the memory core has no warm-start interface and is not modified to accept one.

The dense comparator calls the unchanged `solve_dense_oa` with split fraction 0.99, at most 200 root OA rounds, and Gurobi branching. It starts from the shared heuristic incumbent, whose generation is charged to its pipeline. The true objective of every returned schedule is reevaluated. BLAS/OpenMP and Gurobi each use one thread. The upper bounds in this benchmark are numerical; no new exact certificate is claimed here.

The 30-second limit is implemented by the existing cooperative timers and solver limit. Measured pipeline overruns were at most 0.049 seconds and are saved explicitly. Shared work is charged to each alternative pipeline for comparison, although it was executed only once per grid in the experiment.

## Preflight: sufficient bounds and estimated workspace

For a spectral error bound \(\delta\), the preflight separately records:

- the one-sided logdet upper-bound correction \(-3\log(1-\delta)\);
- the two-sided surrogate-optimizer loss bound \(3\log[(1+\delta)/(1-\delta)]\).

The first window making either component at most 0.01 is a **sufficient approximation-bound estimate**. It is not a lower bound on necessary memory and does not by itself ensure a 0.01 discrete optimization gap. Prior-aware bounds, instance-specific information, or a different representation may improve the result.

The newer reviewed stationary pair bound is included in this preflight to avoid treating the core's older constant as the only available analysis. It uses gap one, which adds no restriction to distinct calendar selections.

| Candidates | First refined window for one-sided component \(\le0.01\) | Estimated workspace at that window | First refined window for two-sided component \(\le0.01\) | Largest window within 256 MiB estimate |
|---:|---:|---:|---:|---:|
| 48 | 7 | 2.07 MiB | 7 | 14 |
| 96 | 15 | 505.28 MiB | 17 | 14 |
| 192 | 35 | \(1.047\times10^9\) MiB | 38 | 13 |

The old core bound first meets the one-sided component at windows 8, 18, and 40, respectively. The scheduled primary windows were 8, 14, and 13, with estimated workspaces 3.07, 253.53, and 253.69 MiB. The coarse-grid window was chosen to meet its target without unnecessary history. The finer-grid windows use the largest allowed by the estimate.

No scheduled solve returned `memory_limit`: all selected primary windows passed the estimate cap. Larger-window figures are preflight estimates, not attempted allocations or observed memory failures. The cap is not a hard process-memory bound. Cumulative process RSS reached 418.4 MiB during the 96-point primary run. This includes interpreter and retained earlier-solver memory; the process high-water marks cannot be used as isolated per-method peaks.

## Measured results

The table uses each method's global numerical upper bound and the better of its own feasible incumbent and the charged shared heuristic. Every objective is the same true selected-covariance logdet criterion.

| Candidates | Method | Pipeline time | True feasible objective | Numerical upper bound | Gap | Outcome |
|---:|---|---:|---:|---:|---:|---|
| 48 | Memory, \(L=8\) | 0.771 s | 14.929653 | 14.938132 | 0.008478 | Target reached |
| 48 | Dense OA and branching | 30.048 s | 14.919244 | 15.080463 | 0.161219 | Time limit |
| 96 | Memory, \(L=14\) | 30.002 s | 14.945663 | 17.313745 | 2.368082 | No completed price |
| 96 | Dense OA and branching | 30.028 s | 14.945663 | 15.361136 | 0.415473 | Time limit |
| 96 | Memory, \(L=12\), separate diagnostic | 28.046 s | 14.952767 | 15.049939 | 0.097172 | Surrogate hull closed; target missed |
| 192 | Memory, \(L=13\) | 30.002 s | 14.953047 | 17.641733 | 2.688686 | No completed price |
| 192 | Dense OA and branching | 30.024 s | 14.953047 | 15.625546 | 0.672499 | Time limit |

Both finer-grid primary memory runs have `generated_paths=1` and `pricing_rounds=0`. Thus their calendar-oracle construction and initial path evaluation completed, but no first pricing step completed before the deadline. They are **first-pricing timeouts**, not demonstrated construction timeouts. Their returned upper bounds are the full-selection bounds, and their useful lower bounds come from the shared heuristic.

The 96-point \(L=12\) run was performed after the primary \(L=14\) run produced no completed price. It has its own 30-second pipeline budget and remains an explicitly separate diagnostic. It completed eight pricing rounds, with a surrogate hull gap about \(3.22\times10^{-9}\), and found a better incumbent. Its true-design gap remained 0.09717 under the core's error transfer. It therefore separates a tractable smaller history graph from the still inadequate true-design bound; it does not replace the failed primary run or establish the requested target.

The shared heuristic results were:

| Candidates | Setup plus heuristic time | True objective | Objective evaluations | Accepted exchanges | Status |
|---:|---:|---:|---:|---:|---|
| 48 | 0.170 s | 14.919244 | 3,209 | 4 | Single-exchange local optimum |
| 96 | 1.193 s | 14.945663 | 27,017 | 19 | Single-exchange local optimum |
| 192 | 3.027 s | 14.953047 | 70,537 | 23 | Single-exchange local optimum |

These local-optimum statuses concern the returned schedules under the implementation's stated exchange tolerance. They do not supply global upper bounds. The memory method improved the coarse-grid and diagnostic incumbents beyond the completed shared exchange searches.

## Tighter reviewed transfer without another solve

A separate [reanalysis driver](../code/research_20260912/fixed_physical_grid_refined_transfer.py) applies the already reviewed stationary refined delta to each completed saved surrogate upper bound:

\[
U_{\mathrm{true}}\le U_{\mathrm{surrogate}}-3\log(1-\delta_{\mathrm{refined}}).
\]

This requires no new optimization or pricing, leaves the original artifact intact, and uses gap one, so it adds no sampling restriction. The [separate reanalysis artifact](../code/research_20260912/results/fixed-physical-grid-refined-transfer.json) records the exact rational delta, numerical transformation, source hashes, and added postprocessing cost.

| Run | Refined delta | Numerical upper bound after transfer | Numerical gap | Pipeline plus reanalysis |
|---|---:|---:|---:|---:|
| 48 points, \(L=8\) | 0.0006455323 | 14.935625 | 0.005971 | 0.772 s |
| 96 points, \(L=12\), diagnostic | 0.0120482180 | 14.989863 | 0.037097 | 28.047 s |

The reanalysis takes less than one millisecond per available bound in this run. The 96-point \(L=14\) and 192-point \(L=13\) runs have no completed surrogate upper bound to transfer. They remain unchanged. Because the input surrogate bounds are numerical, using an exact analytical delta does not turn this reanalysis into an exact certificate. The finer grids still miss the 0.01 target after this improvement.

## What the comparison establishes

The fixed physical correlation test exposes a real limitation that fixed-step-correlation comparisons conceal. With twice or four times as many candidate times but the same 16-observation budget, the affordable primary memory graphs did not complete a price within the chosen limit. The smaller 96-point graph could be optimized and outperformed the tested dense implementation's bound, but it did not reach the target. This supports investigating a cheaper physical-history representation or a sharper useful certificate before expanding this nominal benchmark family further.

The dense result is also limited. All three runs exhausted their 200 root OA rounds with unresolved root gaps of about 0.06846, 0.24890, and 0.46468, respectively. They then spent the remaining time on one integer master solve, visiting 102,543, 56,009, and 32,464 nodes. These are results for the specified reviewed prototype and stopping rules, not an optimized treatment of every Liu relaxation or a general solver ranking. The existing structured covariance evaluator could remove dense linear-algebra overhead, but it does not by itself resolve these master-relaxation gaps.

No failure here proves a necessary exponential memory requirement. Nor do the sufficient preflight windows prove that a better prior-aware or schedule-specific certificate could not meet the target at a smaller window. The numerical evidence is narrower and useful: the current pipeline has a decisive fine-grid scaling problem under these matched budgets, while the completed heuristic still provides good feasible schedules cheaply.

The complete experiment took about 173.37 seconds. It used Python 3.13.11, NumPy 2.5.3, SciPy 1.18.1, and Gurobi 13.0.3 in the isolated project environment. Gurobi executed all three comparisons successfully. The driver recorded and verified unchanged core hashes throughout the run. The independent review reconstructs the saved memory prices, transfer bounds, and accounting. The historical dense MIP bounds remain numerical and were not independently certified; their complete cut histories were not retained.

Reproduction:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --project code/research_20260912 python \
  code/research_20260912/fixed_physical_grid_benchmark.py
```

Use `--preflight-only` with a separate `--output` path to inspect the model and resource estimates without running the solvers.
