# Numerical verification records

These computations check specific mathematical predictions. They do not establish literature novelty or experimental validity. All parameters below are dimensionless, chosen for verification rather than fitted to a material.

## Constant surface diffusivity

Run `python scripts/check_surface_exchange.py` from the repository root. Results are in [surface-exchange-checks.json](../results/surface-exchange-checks.json).

The periodic rate is `k(s)=2(1−cos s)+δ` on a wall of length `2π`, giving a quadratic minimum with `a=1`. Sparse finite differences verify the integrated surface resolvent against the oscillator crossover. At `D_s=10⁻⁸`, refining the wall grid from 8,192 to 65,536 cells changes the scaled zero-floor integral from 4.64815875 to 4.64749790. The limiting asymptotic constant is 4.64747601. This refinement distinguishes grid error from the small-diffusion asymptotic error.

A separate finite-volume bulk calculation uses a strip of height 1, periodic transverse length `2π`, bulk diffusivity 1, affinity 0.7, and plug velocity 1. One wall adsorbs reversibly. The calculation uses detailed-balance conductances and a half-cell correction for the Robin exchange boundary. Grids of `(512,8)`, `(1024,16)`, and `(2048,32)` bulk cells test both wall and bulk resolution.

At the finest grid, the difference between full flow dispersion and the exact reduced surface term is 0.0351023, 0.0334468, and 0.0332828 at surface diffusivities `10⁻²`, `10⁻⁴`, and `10⁻⁶`. The predicted limiting bulk contribution is `0.7²/(3×1.7³)=0.0332451`. Conservation residuals are below `10⁻¹²`. The bulk correction is nonnegative in every run, as required by the variational proof.

## Independent time-domain check

Run `python scripts/check_exchange_transients.py`. Results are in [exchange-transient-checks.json](../results/exchange-transient-checks.json).

For the same periodic rate at zero surface diffusivity, the integrated resolvent is exactly `I(z)=2π/[sqrt(z)sqrt(z+4)]`. Inverting exact moment transforms avoids a wall mesh. Separate principal square roots preserve the analytic branch needed for complex inversion.

De Hoog and Talbot inversion agree to well below `10⁻¹⁵` relative difference. At time `10⁶`, stationary and bulk-injected variances divided by their respective predicted leading `t^(3/2)` laws are 1.0002563 and 1.0006991. Their ratio is 1.9991152, approaching two. This preparation effect is established renewal theory; the check verifies its correct use here.

The result assumes no independent axial Brownian motion in this test. Such motion adds its own variance and does not change the leading anomalous term.

## Vanishing surface mobility

Run `python scripts/check_degenerate_mobility.py`. Results are in [degenerate-mobility-checks.json](../results/degenerate-mobility-checks.json).

The mobility is `D(s)=ε[2(1−cos s)]^(n/2)`, and symmetry reduces the computation to `[0,π]`. A geometric finite-volume grid resolves the degenerate endpoint. The first cell is an explicit regularization and must be refined: a finite result on one mesh cannot establish a finite continuum dispersion coefficient.

For `n=2` and `ε=10⁻⁶`, the scaled zero-floor integral is 4.93480341, versus the predicted `π²/2=4.93480220`. Doubling the grid from 12,000 to 24,000 cells gives 4.93480296. Nonzero scaled rate floors agree with the separate inverse-square-operator gamma formula to about `10⁻⁶` relative error.

Endpoint refinement distinguishes the threshold: `n=2` and `n=2.5` converge, `n=3` increases by approximately 92.1034 for every factor 100 decrease in endpoint cutoff, and `n=3.5` and `n=4` grow as powers. For `n=3`, the predicted increment at `ε=0.1` is `(2/ε)log(100)=92.1034`. The independent variational proof, rather than these finite meshes, establishes the finiteness threshold.

## Figures

Run `python scripts/plot_exchange_results.py` after the first two checks. It creates the [verification figure](../results/surface-exchange-verification.png) and a [PDF for export](../results/surface-exchange-verification.pdf).

The figure separates the candidate surface-diffusion crossover, finite-bulk verification, and the established initialization effect. It does not present all three as novel discoveries.

## Optimal mobility placement

Run `python scripts/check_optimal_placement.py`. Results are in [optimal-placement-checks.json](../results/optimal-placement-checks.json).

A discrete convex dual on a finite interval independently checks the exact whole-line mobility profile. For `a=R=1`, truncation at `±4` gives the exact optimal value 11.5. The 120- and 240-cell dual optima are 11.494021 and 11.498517, with optimal slope bounds 8.002856 and 8.000734, approaching the predicted value 8.

For the periodic rate `2(1−cos s)`, an admissible localized design and a uniform design receive the same integral of diffusivity. Their dispersion-resolvent ratio is 0.5992, 0.4757, 0.3778, and 0.3001 at budgets `10⁻³`, `10⁻⁵`, `10⁻⁷`, and `10⁻⁹`. The localized value multiplied by `M^(1/5)` approaches 6.222824, versus the proven asymptotic constant 6.222824. The agreement of the last digits is partly cancellation between discretization and asymptotic errors and should not be interpreted as that many digits of continuum accuracy.

## Finite-floor placement phases

Run `python scripts/check_placement_phases.py`. Results are in [placement-phase-checks.json](../results/placement-phase-checks.json). The independent reviewer also supplied [a separate primal optimization program](../scripts/check-placement-phase-review.py).

Quadrature verifies equality of primal and dual costs for the explicit profiles. A separate constrained quadratic optimization checks the dual field. Starting from zero rather than the analytic candidate, the 240-cell calculations at dimensionless velocities 1.8 and 3 converge in 34 and 18 iterations; their costs differ from the continuum predictions by approximately `8×10⁻⁷` and `−2.1×10⁻⁶` relative. This avoids using an analytic starting point as the only optimization check.

Near activation, the computed mass exactly matches `q⁵/60` within floating-point error. The performance gain divided by `q⁷/560` approaches 0.9999978 as the velocity excess decreases to `10⁻⁵`. These checks support the independently proved `5/2` and `7/2` onset laws.

## Coalescing zeros and disorder

Run `python scripts/check_coalescing_zeros.py`. Results are in [coalescing-zero-checks.json](../results/coalescing-zero-checks.json). The moment theorem now has separate scalar and finite-bulk reviews.

For the local pair potential `(y²−μ)²`, the integrated inverse at `μ=0` is 2.949174 numerically, consistent with the quartic constant 2.949172. A periodic profile `k_c(s)=(c+cos s)²` approaches this local pair curve when `c` is scaled near ±1. The local curve is not monotone in separation: it increases above its value at exact coalescence before decreasing for widely separated zeros.

For `c` uniform on `[-2,2]`, quadrature of the full periodic boundary problem gives `D^(2/3) E[J²]` equal to 63.3922, 62.9067, 62.8144, and 62.7952 at diffusivities `10⁻³`, `10⁻⁵`, `10⁻⁷`, and `10⁻⁹`. An independent local-pair integral predicts approximately 62.78994. The mean converges much more slowly: `D^(1/4) E[J]` is 11.5268 at `10⁻⁹`, versus the candidate limit 12.18595. Finite-diffusivity agreement must not be claimed for that mean asymptotic.

The squared coefficient of variation increases from 1.0552 to 13.9456 over the same range. The [independent review](review-random-kinetic-barriers.md) supplies the uniform estimates required to justify disorder averaging; fixed-realization asymptotics alone would not justify these moment claims. A Gaussian amplitude-collapse counterexample is preserved in the associated research note.

## Designing before and after measurement

Run `python scripts/check_robust_design.py`. Results are in [robust-design-checks.json](../results/robust-design-checks.json). The fixed blind shape is asymptotically optimal; the adaptive values are from an explicit admissible trial and do not certify finite-budget optimality.

| Budget | Blind / uniform response | Adaptive trial / blind response |
|---:|---:|---:|
| 1e-3 | 1.03364 | 0.82648 |
| 1e-6 | 0.99844 | 0.59387 |
| 1e-9 | 0.97908 | 0.42951 |

The limiting fixed-shape improvement over uniform mobility is about 4.70%, but only 2.09% is realized at the smallest budget in this table. At the largest budget, the asymptotic shape is worse. The scaled blind response approaches 18.3861 slowly; the scaled adaptive trial approaches the sharp adaptive coefficient 22.4046. Doubling the smallest-budget wall grid and increasing quadrature from 40 to 60 nodes per interval changes the last displayed ratios by less than `2e-5` absolute.

The [finite-bulk review](review-robust-finite-bulk.md) adds an independent Neumann-patch calculation, supporting its analytically proved uniform exchange-flux bound. The response fields and optimal values in these numerical tables remain scalar quantities.

## Positive disorder moments and graded mobility

Run `python scripts/check_risk_sensitive_design.py`, followed by `python scripts/plot_risk_sensitive_design.py`. The [data](../results/risk-sensitive-design-checks.json), [figure](../results/risk-sensitive-design.png), and [exportable PDF](../results/risk-sensitive-design.pdf) test explicit graded trials from the [independently reviewed order theorem](review-risk-sensitive-mobility.md). These computations do not optimize a discretized design or determine sharp optimal constants.

For the third moment, the graded-trial to uniform-design ratio decreases from 0.9142 at `M=1e-3` to 0.03490 at `M=1e-12`. The graded third moment multiplied by `M` takes values 7243.6, 7571.1, 7824.6, and 7945.0 at budgets `1e-3, 1e-6, 1e-9, 1e-12`. This supports the constructed `M^(-1)` upper order, compared with `M^(-7/6)` under uniform mobility. It does not identify the infimum's leading constant.

At the critical moment `q=8/5`, the trial moment divided by `M^(-2/5)[log(1/M)]^(7/5)` decreases from 9.495 to 3.703 over this range. A later independently verified proof gives the sharp limit 2.02233; the figure displays the substantial remaining drift. The tested distance-based critical shape has the same logarithmic normalization and local leading coefficient as the sine-based construction. At the smallest budget, doubling the wall grid and increasing parameter quadrature changes the critical trial moment by about 0.026% and the third moment by 0.0058%. The much larger finite-budget changes therefore cannot be attributed solely to the tested mesh error.

## Canonical uncertain-center optimization

Run `OPENBLAS_NUM_THREADS=1 python scripts/check_uncertain_center_design.py`. The [data](../results/uncertain-center-design-checks.json) solve the local uncertain-center functional defined in [the finite-precision note](finite-precision-mobility.md). The optimization starts from uniform mobility. A supporting-plane bound independently bounds the global minimum of each discretized convex problem; it is not a continuum certificate.

At 400 spatial cells, the objective is 6.22265 for a known center, 6.63310 for uncertainty width 2, and 11.13858 for width 32. The known-center continuum value is 6.22282. The discrete primal-to-lower-bound gaps are respectively 0.00168, 0.00163, and 0.00014. These figures warrant only modest numerical precision.

For width 32, simultaneous spatial and parameter refinement changes the value from 11.19649 (200 cells, 96 quadrature nodes) to 11.13858 (400 cells, 192 nodes), about 0.52%. Reevaluating the latter design with 384 parameter nodes changes its objective by less than `1e-13` relative, so spatial error remains the more material tested limitation. The mobility is restricted to a finite padded interval, with the exterior reciprocal-potential response integrated exactly; no theorem that the continuum optimum has this support is inferred from the computation.

A preliminary 24-node calculation at width 32 gave 10.84053 on the 200-cell grid, substantially below the 96-node result. Sparse scenario sampling can make an optimized design look artificially favorable. This exploratory failure motivated the parameter refinement and is retained as a warning about this numerical boundary. The computation does not prove the conjectured finite-ratio crossover for the full cosine ensemble.
