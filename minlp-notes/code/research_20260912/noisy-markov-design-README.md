`noisy_markov_design.py` is a separate prototype for fixed scalar sensitivities
with stationary covariance `R[i,j] = P*rho**abs(i-j) + r*(i==j)`, where `P>=0`,
`r>0`, and `abs(rho)<1`. It selects exactly `k` calendar indices and adds the
supplied positive-definite prior information matrix. It does not change the
noiseless Markov implementation.

The calendar-memory approximation conditions a selected observation on the
selected observations in its preceding `L` calendar positions. Each mask uses
the true local covariance regression, its conditional variance, and the adjusted
sensitivity `F[t] - b @ F[history]`. The resulting rank-one PSD information is
stored on a choose arc; skip arcs have zero information. This is a Vecchia
working-model approximation of the true marginal likelihood.

`solve_hull(design, L)` optimizes log determinant over a convex combination of
size-`k` paths. At each matrix `M`, a count-layer dynamic program finds the path
maximizing `sum trace(inv(M) @ W_arc)`. The tangent upper bound is

```text
U = logdet(M) - p + trace(inv(M) @ prior) + best_path_price.
```

Weights on the generated paths are refined by SLSQP over the simplex. The
upper bound uses the completed dynamic program and remains valid if that
refinement stops early. The graph hull preserves the exact count, but maximizing
a concave function over it can exceed the best discrete path objective.
`hull_optimal_tolerance` reports only the surrogate hull gap. The separate
`true_gap` reports the remaining certified true-objective gap.

With `eta=P/(P+r)`, the reviewed uniform bound used here is

```text
delta = (2P/r) * abs(rho)**(L+1)/(1-abs(rho))
        * (1 + eta*abs(rho)*(1-abs(rho)**L)/(1-abs(rho))).
```

Independent noise and complete history `L>=n-1` have `delta=0`. For `delta<1`,
`U - p*log(1-delta)` bounds the true discrete optimum. A final additional pricing
step can tighten this while retaining the unscaled prior. It uses
`N = prior + (M-prior)/(1-delta)` and arc gradient `inv(N)/(1-delta)`. The
implementation takes the minimum of both transferred bounds and the true
full-selection objective. Every incumbent is reevaluated with the original
selected covariance. When `delta>=1`, only the full-selection upper bound is
used. The [theorem note](../../notes/research-20260912-noisy-markov-memory.md)
gives the assumptions and statistical meaning.

The main APIs are:

```python
design = NoisyDesign(F, rho, latent_variance, nugget_variance, prior, k)
result = solve_hull(design, L=6, time_limit=5)
baseline = solve_dense_oa(design, time_limit=5)
stronger = solve_dense_oa(design, time_limit=5, split_fraction=0.99, root_rounds=200)
```

`CalendarOracle` exposes local information, normalized residual covariance,
and exact-count linear pricing. `DenseLiuOracle` and `solve_dense_oa` implement
the same-data binary-exact Liu extension, independently of the older AR(1)-only
code. The default dense split is `a=0.5*lambda_min(R)` with no root cuts.
`split_fraction=0.99, root_rounds=200` uses a stronger split and up to 200 LP
outer-approximation cuts before the integer phase, under the same total time
budget. Root feasible values are kept separate from true integer lower bounds.
An optional `initial_selected` supplies a size-`k` true-evaluated MIP start.

All returned hull paths, their information matrices, and their final weights
are saved. The best surrogate upper-bound witness records its matrix, gradient,
priced path, linear value, and tangent bound. The prior-aware true-bound witness
is saved separately. These permit independent reconstruction; they are
floating-point certificates, not rational or interval proofs.

Memory is estimated before covariance and mask allocation, including dense
covariance workspaces, arc matrices, count-state predecessors, and corrective
workspaces. The default estimate limit is 256 MiB. An initial refusal returns
`memory_limit` with null objective and bound fields. This is a workspace
estimate, not an operating-system RSS limit; the Python/BLAS runtime and
already supplied input data also occupy memory. `time_limit`, `iteration_limit`,
and `correction_stalled` retain completed bounds and true-evaluated incumbents.
Time limits are soft around indivisible numerical operations and final output.
Each solver invocation accepts at most 30 seconds.

Run from the repository root with one BLAS thread; Gurobi always uses one thread:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/noisy_markov_design.py validate
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/noisy_markov_design.py benchmark --time-limit 5
```

`solve --n 48 --k 16 --rho .4 --L 6` runs one hull instance;
`solve --dense --split-fraction .99 --root-rounds 200` selects the stronger dense
configuration. `thresholds --n 48 --k 16 --rho .6` prints memory and delta tables.
The fixed benchmark preserves both dense configurations. Its strengthened run
receives the best hull incumbent as an explicitly recorded MIP start; hull
construction time is reported separately and is not charged to that MIP's cap.
No priority or general performance claim follows from these small examples.
The [independent review](../../notes/research-20260912-noisy-solver-independent-review.md)
checks the final source and reconstructs the saved pricing certificates.

`noisy_markov_extended_benchmark.py` runs the n=48/96, seeds 0/1/2, L=6/8
extension with the strengthened dense comparator. It atomically saves
`results/noisy-markov-extended-benchmark.json` after every solve. Exact matching
records reused from the first benchmark and all time caps are identified in
that output. Use the same one-thread environment variables as above.
