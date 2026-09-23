# September 12 research implementations

This locked environment contains measurement-selection and dynamic-relaxation
prototypes. The [closeout record](../../notes/research-20260912-closeout.md)
collects the results, independent reviews, reproduction instructions and limits.
The [research log](../../notes/research-20260912-log.md) preserves the investigation.

## Noisy correlated measurement design

The current noisy-AR-plus-nugget implementation is documented in
[noisy-markov-design-README.md](noisy-markov-design-README.md). It uses a
finite-calendar information approximation and a uniform correction to bound
the original selected-covariance design objective.

The separately reviewed `covariance_dense_oracle.py` implements the dense
relaxation through classical innovation and adjoint recursions. Its
[numerical review](../../notes/research-20260912-covariance-dense-oracle-independent-review.md)
preserves the failures found in two earlier implementations and the scope of
the repairs. It does not replace exact cut certification.

`block_snapshot_design.py` implements scalar-information optimization for
complete vector snapshots. Its
[independent review](../../notes/research-20260912-block-snapshot-independent-review.md)
reconstructs the tiny exhaustive checks and both saved chemistry probes.
Those probes show fast computation but no improvement over greedy selections;
the dense relaxation supplies tighter numerical bounds.

`partial_observation_trace_probe.py` selects scalar observations of two latent
drift modes. Its [implementation review](../../notes/research-20260912-partial-observation-trace-independent-review.md)
confirms small improvements over greedy/exchange on four chemical cases.
`certify_partial_trace.py` supplies separately reviewed
[exact certificates](../../notes/research-20260912-partial-trace-certificates.md)
with relative gaps below 0.0604%. These use stipulated noise and local kinetic
sensitivities; they are not validations of an experimental noise model.

`robust_kinetic_design.py` uses one schedule across three reaction-rate
scenarios. `certify_robust_design.py` and `compare_robust_nominal.py` have
separate [exact-certificate review](../../notes/research-20260912-robust-certificate-independent-review.md).
The [certificate note](../../notes/research-20260912-robust-design-certificates.md)
records rigorous standardization despite unknown individual optima, the two
saved gaps, and improvements over the saved central-scenario schedules.
`robust_dense_comparison.py` and `certify_robust_polish.py` supply the
[reviewed dense comparison and polished certificate](../../notes/research-20260912-robust-dense-independent-review.md).

`fixed_physical_grid_benchmark.py` holds the horizon, physical covariance and
observation budget fixed while refining the candidate grid. Its
[reviewed results](../../notes/research-20260912-fixed-physical-grid-independent-review.md)
expose the calendar implementation's finer-grid cost. The separate
`fixed_physical_grid_refined_transfer.py` tightens completed saved bounds using
the reviewed pair estimate and preserves the original artifacts.

`latent_separator_design.py` implements the
[latent-separator block-pattern relaxation](../../notes/research-20260912-latent-separator-implementation.md).
`certify_latent_separator.py` independently recomputes its
[rational global certificates](../../notes/research-20260912-latent-separator-certificates.md).
Larger blocks strengthen the tested upper bounds but require exponentially
many local patterns; the best 192-candidate certificate still misses a 0.01
log-gap target. Generation and certificate costs are reported separately.

- `certify_noisy_markov.py` recomputes bounds with exact rational arithmetic;
  see the [certificate note](../../notes/research-20260912-noisy-markov-certificates.md).
- `certify_dense_design.py` and `certify_all_splits.py` provide independent
  continuous-relaxation comparisons; see the
  [all-splits result](../../notes/research-20260912-all-splits-separation.md).
- `noisy_markov_kinetics_probe.py` supplies smooth reaction sensitivities;
  its [application review](../../notes/research-20260912-noisy-markov-kinetics-independent-review.md)
  checks them against independent mass-balance ODE calculations.
- `noisy_markov_spacing_design.py` and `certify_spacing_design.py` impose a
  minimum sampling gap; the
  [spacing certificate note](../../notes/research-20260912-spacing-certificates.md)
  records the achieved bound and exact-arithmetic cost.

The earlier noiseless Markov code below remains a separate implementation.
Its exact path hull is established prior work, as the research log explains.

## Certified polynomial ODE supports

`extended_rpd.py` compiles exact rational affine supports of fixed-interval
polynomial extended-RPD fields, including inconsistent endpoint inputs and
finite affine-invariant refinements. `rational_affine_flow.py` certifies
propagation of held affine supports. The nonlinear numerical reference only
chooses supports; its accuracy is not an assumption of the certificate.
Model constants must be integers, rational strings or `Fraction` values.

`ode_support_experiment.py` records all rational slab coefficients and final
cuts for two explicitly stylized reaction systems. See
[the prototype note](../../notes/research-20260912-ode-prototype.md) for the
commands, physical tube proofs, review corrections and limitations. Fixed broad
state boxes do not by themselves give a convergent parameter-branching solver.

## Correlated measurement selection

`markov_design.py` compares two exact mixed-integer convex formulations for
selecting exactly `k` scalar measurements. Independent chains may share the same
unknown parameter vector. Within each chain, candidate indices are consecutive
and the fixed error covariance is `R[i,j] = sigma**2 * rho**abs(i-j)`.
Sensitivities and a positive-definite prior information matrix are supplied as
data. Covariance parameters are fixed, not estimated design parameters.

Run from the repository root:

```bash
uv run --project code/research_20260912 python code/research_20260912/markov_design.py validate
uv run --project code/research_20260912 python code/research_20260912/markov_design.py solve --family reaction --n 16 --k 5 --rho 0.8 --time-limit 5
uv run --project code/research_20260912 python code/research_20260912/markov_design.py solve --family generic --n 12 --p 3 --k 4 --seed 0 --relaxation
```

The environment requires an available Gurobi license. Every Gurobi model uses
one thread, seed zero, and a quiet environment. Each solve accepts a wall-time
budget of at most 30 seconds, measured from before oracle/model construction.
Small overruns can occur during construction, solver return, or final evaluation.
`--formulation path|dense|both` defaults to `both`; each formulation gets its own
time budget. Solve commands emit one JSON object per formulation.

The `reaction` family observes the intermediate concentration B in A → B → C,
with nominal rates 0.7 and 0.2, initial A concentration one, and times uniformly
spaced on [0.1, 12]. Its three parameters are the logarithms of the two rates and
initial concentration. Analytic local sensitivities are used, with `sigma=0.05`
and prior `0.01 I`. `--p` applies only to the seeded Gaussian `generic` family.
In both families, `rho` is the correlation per candidate-grid interval; changing
`n` in the reaction family changes the physical interval represented by `rho`.

## Formulations and solve method

Both maximize the natural logarithm of the determinant of

```text
J(S) = prior + sum_g F[g,S].T @ inverse(R[g,S,S]) @ F[g,S].
```

`path` has binary visit variables and continuous nonnegative flows on each
ordered complete DAG. Source-to-observation arcs contribute the first-observation
information. An arc from selected index i to the next selected index j contributes
the innovation information based on `rho**(j-i)`. Sink arcs contribute zero. An
empty path is allowed. Binary visits uniquely determine each chain's path, so
the affine arc information is the exact information of the selected subset.

`dense` uses the concave binary-exact extension with
`a = split_fraction * lambda_min(R)`, `S = R-a I`, `D = diag(z)/a`,
`V = solve(I+S D, F)`, and information contribution `F.T @ D @ V`.
Its log-determinant gradient is `V[i] @ inverse(J) @ V[i].T / a`.
Each chain uses its own `a` and covariance block. The default split fraction
is 0.5; the Python APIs allow any fixed fraction strictly between zero and one.
Fractions near one give stronger scalar-split relaxations.

The outer-approximation loop solves a linear master globally, evaluates the
selected subset by independently solving its original dense covariance system,
and adds a global log-determinant tangent. It starts with a tangent at full
selection and at a deterministic feasible seed. Full-selection information also
supplies a valid objective upper bound. Optional `root_rounds` in `solve_oa`
first generates continuous-root cuts, charging that work to the same time budget.
Rounding its visits to a size-k subset provides an independently evaluated
incumbent. The default remains zero root rounds; there are no callbacks.
Each master is solved with zero relative MIP gap,
absolute MIP gap at most `1e-9`, and feasibility/integrality/optimality tolerances
`1e-9`. The default outer stopping gap is `1e-6` in absolute log-determinant units.

`solve_relaxation` changes visits to continuous variables and runs LP outer
approximation. Its feasible value is a lower bound on the continuous optimum,
and can exceed every integer objective. Accordingly, its JSON `lower_bound` and
`selected` fields are null. Its initial point has uniform fractional visits; the
path version represents this by mixing the full and empty paths. The path
relaxation permits mixtures of paths of different sizes subject to the total
visit constraint.

## Python API and result fields

With this directory on the Python import path:

```python
import numpy as np
from markov_design import Chain, Design, solve_oa, solve_relaxation

F = np.array([[1., 0.], [1., 1.], [0., 1.]])
design = Design((Chain(F, rho=0.8),), prior=0.1*np.eye(2), k=2)
result = solve_oa(design, "path", time_limit=5)
root = solve_relaxation(design, "dense", time_limit=5)
```

`selected` uses zero-based indices flattened in chain order. Integer
`lower_bound` is always the objective of an actual size-`k` subset.
`upper_bound` is the smallest full-selection or master bound seen;
`objective_residual` is the absolute difference between the returned subset's
formulation objective and its original dense-covariance objective. Results also
record elapsed wall time, outer rounds, total master nodes, cut count, and the
last Gurobi status. `fractional_visits` accompanies the best continuous value.

Only `status="optimal_tolerance"` reports the requested outer gap as closed.
`time_limit` and `iteration_limit` preserve available bounds and a feasible
integer subset without claiming completion. These are solver-numerical bounds,
not exact-arithmetic or interval certificates. Roundoff can make the upper bound
slightly smaller than the lower bound; the reported gap clips this difference
at zero, while a material inconsistency receives a separate failure status.

`validate()` exhaustively compares all subset information matrices on tiny
single-chain and independent-chain cases, checks directional derivatives and
tangent inequalities, compares integer results with enumeration, tests cardinality
edges and an iteration cap, and checks the reaction sensitivities by finite
differences. `validation-implementation.json` records the initial validation run.

The path information hull is a linear image of the selected-principal-inverse
hull of Lee, Gómez, and Atamtürk, arXiv:2412.17178. This implementation does not
claim a new path-hull theorem. The research notes record the priority correction.

`path_oracle.py` implements a separate single-chain branch-and-bound method.
Its exact-count dynamic program supplies support maxima for logdet tangent
upper bounds, using a fully corrective mixture of path information matrices.
Run it directly for the exhaustive small-instance checks. Its `pricing_calls`
field counts certificate pricing calls, excluding initialization calls. Its
time limit is soft because construction and one valid bound calculation finish
before returning.

For a matched comparison with a stronger dense split and root initialization:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 \
  python code/research_20260912/compare_solvers.py \
  --output code/research_20260912/results/strengthened_comparison.json \
  --sizes 12 24 --seconds 5 --root-rounds 200 --split-fraction .99
```

Each result includes all failures/limits and the source hashes. This is a
comparison of specific implementations, not a general solver ranking.
