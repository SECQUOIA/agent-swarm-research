# Independent review of the partial-observation trace probe

Date: 2026-09-12. Reviewer: `/root/noisy_solver_review`, separate from the
implementation author. Status: passed for the stated positive-semidefinite
weight/prior model and tested numerical scope. No core implementation change
was required. The saved results show a small improvement over greedy/exchange
selection and better upper bounds than the dense continuous comparator on
these four inputs; the dense comparator takes less time.

The reviewed source is
[partial_observation_trace_probe.py](../code/research_20260912/partial_observation_trace_probe.py),
SHA-256 `8a85b6b4f1a5e879d96a912a8375c0bf0b19b7da828883ce9c942f3d23fa44d3`.
The [independent checker](../code/research_20260912/review_partial_observation_trace_probe.py)
and [report](../code/research_20260912/results/partial-observation-trace-independent-review.json)
record source/dependency/artifact hashes, package versions, comparison errors,
saved bound reconstruction, cap checks and the improvement denominators.
The reviewer did not edit the author source or saved application results.

This audit concerns the
[numerical application probe](research-20260912-partial-observation-trace-probe.md)
using the original accepted
[partial-observation memory bound](research-20260912-partial-observation-memory-bound.md).
It does not use the normalized refinement or replace separate exact-arithmetic
certification. No new literature was identified in this implementation review.

The two-mode covariance is correct. With latent transition
`A=diag(0.4,0.2)`, observation row `H=(0.6,0.8)`, stationary latent covariance
`P=sigma^2 I`, innovation covariance
`Q=sigma^2 diag(0.84,0.96)`, and observation-noise variance `sigma^2`, its
observed covariance is

```text
R_ts = sigma^2 [0.36*0.4^|t-s|+0.64*0.2^|t-s|+1{t=s}].
```

The reviewer independently constructs loadings of every two-dimensional
process innovation into later scalar observations, then adds measurement
noise. This agrees with the implementation's covariance mixture. The two
distinct positive-lag decay modes cannot in general be represented by a
single AR(1)-plus-nugget covariance. Each selected time measures the fixed
scalar packet; it does not reveal both latent coordinates separately.

The theorem constants match this model. Here `Pbar=r=sigma^2`, the process
lower bound is `q=0.84 sigma^2`, and `||H||=1`. Consequently `gamma=0.4`,
`C/r=1` and `B=1`. The checker recomputes the near contribution by explicitly
summing the finite residual-pair majorants and the far contribution by its
geometric tail. This independently matches the driver's original
`partial_delta`, including `delta=0` at complete history. The driver does
not call the scalar AR(1) spectral bound: a mocked failure of that function
leaves the trace solves unaffected.

Reuse of `CalendarOracle` is sound. Its local regression and conditional
variance depend on the supplied covariance, rather than on an AR(1)
formula. It adjusts the sensitivity as `F_t-beta F_history` before forming
the local positive-semidefinite information matrix. The new driver uses
only those generic operations and linear pricing. The reviewer verifies
them using explicit selected-subset residual transformations, their
conditional variances, and the normalized residual spectrum. Full history
reproduces true information.

For a fixed positive-semidefinite weight `W`, weighted trace is linear in
the accumulated information matrix. One exact-count history-state price
therefore maximizes the discrete surrogate score. The fixed prior trace is
added exactly once, outside the arc price. There is no fractional hull
optimization or fractional hull gap in this stage. The reviewer's separate
dynamic program uses tuples of recent calendar indices rather than masks;
its prices agree with exhaustive tiny enumeration and all six saved
application prices.

When `delta<1`, the prior-aware inequality has the correct direction:

```text
T_true(S) <= tr(W prior)+[T_local(S)-tr(W prior)]/(1-delta).
```

The completed maximum arc price thus supplies the implemented true-design
upper bound. The true full-selection score is another valid upper bound
for a positive-semidefinite weight. The code uses their minimum, and uses
the full-selection bound alone when the spectral transfer is unavailable.
The checker reconstructs each saved arc sum, surrogate matrix, true matrix,
uniform correction and final upper bound. Every lower bound is independently
evaluated from an actual size-`k` subset of the original covariance.

The distinction between the feasible incumbent and the surrogate maximizer
is handled correctly. The driver preserves its evenly spaced seed when the
surrogate optimizer has worse true information. For example, with seven
constant scalar sensitivities, zero prior and count three, it retains
`(0,3,6)` at both `L=0` and `L=1`. The respective surrogate optimizers are
`(4,5,6)` and `(0,2,4)`, with inferior true scores. The report preserves these
two checks and verifies that the saved matrices and scores refer to the
appropriate schedule. This matters when reconstructing a certificate from
the output fields.

The weighted-trace Liu extension and gradient are correct. At
`D=diag(z/a)`, `S=R-aI`, the defining residual is
`V=(I+SD)^(-1)F`. The information is
`prior+F^T D V`, and the trace gradient is

```text
gradient_i = V_i W V_i^T/a.
```

There is no inverse information matrix in this trace gradient. The
implementation's symmetric positive-definite solve is algebraically
equivalent to the defining nonsymmetric resolvent, which the reviewer uses
as a separate reference. Tests include a nondiagonal rank-one weight, zero
weight, a singular nonnegative prior, zero/full counts and boundary visits.
The saved splits are strictly between zero and the independently computed
minimum covariance eigenvalue.

For any evaluated point, the `k` largest gradient entries give the exact
linear maximum over the count-constrained box. This proves the saved
continuous tangent upper bound independently of SLSQP's stopping status.
Objective scaling changes the optimizer's numerical objective and gradient
together; it does not change the stored unscaled tangent. The checker
reconstructs all four saved dense tangent witnesses, fractional values and
rounded true scores. No fractional score is treated as a feasible discrete
lower bound.

The sensitivities and physical-input provenance also reconstruct. The source
reuses the previously reviewed consecutive-reaction generator unchanged.
The present checker independently forms the three-species kinetic matrix and
its derivatives with respect to `log(k1)` and `log(k2)`. Matrix exponentials
give the mean `B(t)`, and their Fréchet derivatives give the two rate
sensitivities. The amplitude sensitivity is `B(t)` itself. Across the four
saved arrays, all 864 derivative entries agree within `9.44e-15`. The time
grids, selected physical times, parameter order and dependency hashes also
match the saved records.

The covariance is specified rather than fitted to data. Pointwise error
standard deviation is `0.05` in the stated normalized concentration units.
Changing `n` while keeping both per-grid correlations fixed changes the
physical correlation scales. The local mean-information criterion does not
resolve the global rate-swap ambiguity of observing only `B(t)` with unknown
`A0`. Weighted trace depends on the parameter coordinates and weight, and
is not conventional A-optimality. These caveats are correctly retained in
the source note and metadata.

The independent bounded run completed in about 7.5 seconds with one BLAS
thread, Python 3.13.11, NumPy 2.5.3 and SciPy 1.18.1. Its checks include:

| Check | Count |
| --- | ---: |
| Independent projected-covariance comparisons | 42 |
| Selected local-information matrices | 258 |
| Normalized residual spectra | 246 |
| Tiny exhaustive DP comparisons and trace solves | 42 |
| Weighted Liu binary identities | 90 |
| Weighted Liu derivative directions | 18 |
| Binary tangent comparisons | 90 |
| Tiny continuous solves | 18 |
| Reconstructed saved application DP records | 6 |
| Reconstructed saved application dense records | 4 |
| Independent greedy candidate evaluations | 6,448 |
| Final single-exchange neighbors checked | 5,120 |
| Kinetic sensitivity entries independently checked | 864 |

Maximum covariance and local-information discrepancies were `4.34e-19` and
`1.82e-12`. The maximum scaled directional derivative discrepancy was
`2.50e-10`. The saved validation artifact's four window cases and its
continuous bound were independently reconstructed; their true discrete
optima were enumerated. These numerical agreements are not rigorous rounding
error bounds.

Independent greedy construction reproduces all four saved initial greedy
schedules. Every saved final exchange schedule has no improving single
exchange within the numerical comparison tolerance. The dynamic program's
true score is higher in all four cases. Using the best saved memory bound
per case gives:

| n | Regime | DP true score | Greedy/exchange score | DP improvement over greedy | DP upper | Dense upper |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 48 | Fast | 1944.380271 | 1942.490223 | 0.097300% | 1946.920028 | 1978.472003 |
| 48 | Slow | 2568.825052 | 2545.806146 | 0.904189% | 2572.175547 | 2593.070902 |
| 96 | Fast | 3867.260606 | 3860.405646 | 0.177571% | 3872.328972 | 3939.736352 |
| 96 | Slow | 5101.628650 | 5062.520467 | 0.772504% | 5108.292535 | 5152.585974 |

Here improvement divides by the greedy score. The author's separate
“greedy loss” divides by the DP score; for the largest improvement the
corresponding loss is `0.896087%`. Neither denominator uses an independently
known true global optimum. The distinction is recorded in the report.

The dense comparator inherits its reported feasible score from the supplied
DP/greedy incumbent in every case. Its own rounding gives a lower score.
The work used to produce the supplied incumbent is excluded from the dense
comparator's recorded time and cap. Dense continuous optimization is faster
than every corresponding saved DP invocation, but its upper bounds are
wider. The 96-candidate slow case stops at its 200-iteration limit; the
retained tangent remains a numerical upper bound. No MIP is run.

Memory and deadline failure paths behave as documented. Mocked objective
evaluation verifies that initial DP memory/deadline refusal occurs before
evaluating a true objective. An injected interruption in pricing retains
the true baseline bounds and creates no transferred bound or surrogate
optimum. An interrupted dense solve similarly retains its true baseline
bounds. The application catches other exceptions and atomically checkpoints
completed stages. Memory controls are conservative array-workspace estimates,
and deadlines are soft between indivisible numerical operations.

The mathematical guarantees require actual positive-semidefinite weights and
nonnegative priors. Their numerical validator uses an eigenvalue tolerance
of `1e-12`; this does not independently certify those promises for every
nearly singular input. Ordinary matrix solves, optimizer tolerances and
floating-point DP comparisons also remain part of the numerical scope.
The fixed application weight and prior have the required signs directly.
Exact arithmetic certification is separate work, and the true application
optima were not exhaustively proved here. These four chosen arrays establish
the reported numerical comparisons, not broad algorithmic superiority or
empirical residual-model validity.

Reproduce the independent review from the repository root:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  uv run --project code/research_20260912 python \
  code/research_20260912/review_partial_observation_trace_probe.py
```
