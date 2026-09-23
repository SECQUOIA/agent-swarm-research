The smooth-sensitivity probe gives small certified true-objective gaps for two
explicit consecutive-reaction mean models at n=48 and n=96. With k=n/3,
latent correlation ρ=0.4, and calendar memory L=8, the numerical true gaps range
from `0.00346883` to `0.00360830`. Hull runs take 0.63–3.22 seconds. The ordinary
strengthened dense comparator retains gaps of 0.12–0.24 at its ten-second caps.
This is a small stylized application probe,
not a measured-noise benchmark, a priority claim, or a discrete-optimality claim.

The mean follows mass balances for consecutive first-order A → B → C, with
initial concentrations A(0)=A0 and B(0)=C(0)=0:

\[
\dot A=-k_1A,\quad \dot B=k_1A-k_2B,\quad
B(t)=\frac{A_0k_1}{k_2-k_1}(e^{-k_1t}-e^{-k_2t}).
\]

Only B is observed. The parameters are `log(A0), log(k1), log(k2)`, in that
order. Set d=k2−k1 and u=exp(−k1 t)−exp(−k2 t). The sensitivity row is

```text
[B,
 A0*k1*(k2*u/d² − k1*t*exp(−k1*t)/d),
 A0*k2*(−k1*u/d² + k1*t*exp(−k2*t)/d)].
```

The two nominal regimes are A0=1 with rates `(0.7,0.2)` and `(0.18,0.045)`.
Their B peaks occur at approximately 2.5055 and 10.2688 model time units,
respectively, within the fixed horizon 12. Rates are per model time unit and
concentrations are normalized by the nominal initial concentration. The two
regimes capture an early peak and a peak near the horizon. Both have separated
rates; this driver does not evaluate a near-equal-rate limit.

The local criterion does not establish global parameter identifiability.
Indeed, swapping k1 and k2 while replacing A0 by A0*k1/k2 leaves this B mean
unchanged if both rate orderings are admissible. The probe evaluates local
Fisher information at the specified nominal parameters, without claiming
global recovery from B alone.

Candidate times are `t_j=12*(j+1)/n`, j=0,…,n−1. Thus n=48 has spacing 0.25,
and time zero is excluded. Exactly one third of the candidates are selected;
there is no additional minimum sampling gap. The independently specified
observation error model is

```text
R[i,j] = P * rho**abs(i-j) + r * (i==j),
P = r = 0.00125.
```

This is a **stylized known covariance**, with stationary latent AR(1) error
and independent nugget noise. It is not derived from the reaction equations,
estimated from experimental data, or attributed to the earlier published
kinetics example. Total pointwise error standard deviation is 0.05 normalized
concentration units. At ρ=0.4 the observed first-lag correlation is 0.2, because
the nugget contributes half the marginal variance. The objective adds `0.01 I`
in the specified log-parameter coordinates. Covariance parameters are fixed
and have no parameter-sensitivity contribution.

Holding ρ fixed while changing n on this fixed horizon changes the physical
correlation scale: ρ is the latent correlation per candidate-grid interval.
Consequently the n=48 and n=96 runs are explicitly specified statistical
instances, not identical continuous-time error processes sampled at two rates.

The isolated [driver](../code/research_20260912/noisy_markov_kinetics_probe.py)
does not edit the independently reviewed solver core. It computes analytic
sensitivities and checks them against independent complex-step differentiation
of the mean formula. The maximum absolute discrepancies are `1.67e-16` and
`2.22e-16`. The saved
[n=48 results](../code/research_20260912/results/noisy-markov-kinetics-probe.json)
and [n=96 results](../code/research_20260912/results/noisy-markov-kinetics-n96-probe.json)
contain the complete time grids, mean values, sensitivity matrices, prior and
covariance parameters, mixtures, pricing witnesses, selected times, and solver
records. Their schema is compatible with the independent exact certifier.
The exact certificates below concern the saved decimal input values, rather
than asserting exact real values for the exponential sensitivities.

Every run uses one thread and ten seconds per solver invocation. The
dense baseline is the ordinary dense Liu evaluator with split fraction 0.99
and up to 200 root LP outer-approximation cuts. It receives the hull's
true-evaluated incumbent as a disclosed MIP start, with hull time reported
separately. Both its root and integer phases share its ten-second budget.

| n | Regime | Method | True lower bound | True upper bound | True gap | Seconds |
|---:|---|---|---:|---:|---:|---:|
| 48 | Early peak | Memory L=8 | 14.948664846 | 14.952244509 | 0.003579663 | 0.657 |
| 48 | Early peak | Dense strengthened | 14.948664846 | 15.098062269 | 0.149397423 | 10.011, capped |
| 48 | Late peak | Memory L=8 | 9.957780910 | 9.961249736 | 0.003468825 | 0.633 |
| 48 | Late peak | Dense strengthened | 9.957780910 | 10.075405637 | 0.117624727 | 10.015, capped |
| 96 | Early peak | Memory L=8 | 16.973742738 | 16.977351038 | 0.003608300 | 2.524 |
| 96 | Early peak | Dense strengthened | 16.973742738 | 17.212989876 | 0.239247138 | 10.014, capped |
| 96 | Late peak | Memory L=8 | 11.893877158 | 11.897474154 | 0.003596996 | 3.221 |
| 96 | Late peak | Dense strengthened | 11.893877158 | 12.096655107 | 0.202777949 | 10.015, capped |

All four hulls closed their surrogate gap below `1e−6`. The n=48 hull points
are mixtures of two paths, so the calculation retains the discrete-relaxation
distinction. None of the true gaps closes. All dense lower bounds remain those
supplied by the hull runs. After 200 cuts, the dense root LP outer approximation
still has gaps of 0.0631 and 0.0499 at n=48, and 0.2227 and 0.1688 at n=96.
Consequently the dense bounds reflect both limited outer-approximation progress
and the underlying relaxation; this experiment does not measure only the
continuous relaxation's strength.
The certified approximation constant is `0.0011648935570090673`; it accounts
for most of the reported true-objective gap. The small experiment does not
establish that any selected schedule is globally optimal.

Reproduce the initial probe from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/noisy_markov_kinetics_probe.py
```

The bounded n=96 extension changes only the grid size and selected count:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/noisy_markov_kinetics_probe.py \
  --n 96 --rho 0.4 --L 8 --time-limit 10 \
  --output code/research_20260912/results/noisy-markov-kinetics-n96-probe.json
```

The driver accepts `--n`, `--rho`, `--L`, `--regime`, `--time-limit`, and
`--output`. It atomically checkpoints after every solve and records exceptions
without discarding earlier results. Still larger n, stronger correlation, additional
sampling constraints, and the new structured dense evaluator are separate
followups; the original small probe does not establish their behavior.

## Exact certificates

The independently reviewed rational certifier recomputes each true incumbent
and a uniform upper bound over all size-`k` selections. It uses the stronger
innovation floor and retains the unscaled prior in its tangent. The resulting
gaps are smaller than the floating-point table's original approximation bound.

| n | Regime | Certified logdet gap, rounded upward | Certificate time |
|---:|---|---:|---:|
| 48 | Early peak | 0.00190758 | 0.952 s |
| 48 | Late peak | 0.00182972 | 0.958 s |
| 96 | Early peak | 0.00193602 | 2.299 s |
| 96 | Late peak | 0.00194271 | 2.314 s |

For each three-parameter case, D-efficiency is
`(det(J_selected)/det(J_optimum))^(1/3)`. A certified logdet gap `g` gives
D-efficiency at least `exp(-g/3)>=1-g/3`. All four cases therefore guarantee
at least **99.935% D-efficiency** under their stated local-design models.

Times exclude the numerical solve. The four certificates ran concurrently,
with one BLAS thread per process. Their filenames are
`noisy-markov-kinetics-certificate-n48-fast.json`,
`noisy-markov-kinetics-certificate-n48-slow.json`,
`noisy-markov-kinetics-certificate-n96-fast.json`, and
`noisy-markov-kinetics-certificate-n96-slow.json` in
`code/research_20260912/results/`. Each retains the exact decimal problem,
reference matrix, integer price and rational objective bounds.

The [fresh application review](research-20260912-noisy-markov-kinetics-independent-review.md)
passed 864 sensitivity entries against an independently assembled mass-balance
and sensitivity ODE, 16 rows against 70-digit matrix exponentials, 27 saved
path-information reconstructions, and replay of all four exact certificates. These certificates concern local design under a specified error
model; they do not settle the global rate-swap ambiguity or validate that
model against experimental observations.
