# Verified results and research candidates

This is a guide to the original research developed in this repository. Mathematical verification and literature novelty are separate judgments. The listed theorems have explicit models; they are not experimental or clinical claims. Searches have found substantial prior art for the underlying methods. Where no matching transport theorem has been located, the notes state the search limits and remaining access gaps.

## Surface exchange and dispersion

A common model underlies the main results: a solute moves in a channel and reversibly adsorbs onto its wall. Adsorption and desorption vary together so their ratio stays constant. Equilibrium retention and mean speed therefore remain fixed while the exchange times change. Surface diffusion lets particles escape regions of slow exchange.

| Result | Main conclusion | Record |
|---|---|---|
| Weak surface diffusion at quadratic kinetic minima | The leading dispersion contribution scales as `D_s^(-1/4)`, with an explicit finite-rate-floor crossover. The full bulk correction approaches a finite, rate-independent limit. | [Theorem](notes/result-surface-exchange.md), [bulk review](notes/review-singular-exchange.md), [localization review](notes/review-localization.md) |
| Degenerate surface mobility | With local exchange `k≈a|s|^m` and mobility `D≈e|s|^n`, the surface contribution is finite exactly when `m<1` or `n<3`. Explicit local coefficients use established Bessel and exponential-functional identities. | [Derivation](notes/degenerate-surface-mobility.md), [review](notes/review-degenerate-mobility.md), [prior art](notes/degenerate-mobility-prior-art.md) |
| Velocity-matching cancellation | A kinetic minimum need not create divergent dispersion if its surface drift equals the mean tracer drift. For an immobile surface, the leading singular dispersion tensor has rank one. | [Corollary and review](notes/kinetic-trap-observability.md) |

The candidate advance is the coupled transport asymptotic and its conditions, rather than discovery of anomalous trapping or the special functions. [The literature audit](notes/singular-exchange-prior-art.md) distinguishes these explicitly.

## Designing surface mobility

| Result | Main conclusion | Record |
|---|---|---|
| Best uniform mobility | Flow broadening decreases convexly with surface diffusivity, while isotropic surface motion adds axial Brownian spreading. Their balance gives an exact activation criterion and a weak-flow optimum proportional to flow amplitude raised to `8/5`. | [Theorem](notes/optimal-surface-mobility.md), [review](notes/review-optimal-surface-mobility.md) |
| Best placement at a fixed budget | An explicit mobility profile gives the global optimum near a quadratic kinetic zero. On a compact wall, optimal placement changes the small-budget divergence from `M^(-1/4)` to `M^(-1/5)`. Multiple-defect allocation and general powers are included. | [Theorem](notes/optimal-mobility-placement.md), [second review](notes/review-optimal-placement-localization.md) |
| Best placement with a finite rate floor | The exact local design has three regimes: no added mobility, two active flanks, and a central active region. Activation and merging thresholds, profiles, costs, and onset powers are explicit. Compact-channel claims concern leading optimal values; they do not assert exact finite-channel support topology. | [Phase diagram](notes/placement-phase-diagram.md), [review](notes/review-placement-phase-diagram.md) |

The variational design principle overlaps established optimal-conductivity and reinforcement theory. The proposed contribution is the specific transport solution, localization, constants, and physical consequences. See the [placement prior-art audit](notes/optimal-mobility-placement-prior-art.md).

## Uncertain kinetic patterns

For the explicit bounded ensemble `k_c(s)=(c+cos s)^2`, with `c` uniform on `[-2,2]`, a moment transition occurs at order `q=4/3`. The mean surface contribution grows as `D_s^(-1/4)`, its variance as `D_s^(-2/3)`, and its squared coefficient of variation as `D_s^(-1/6)`. A logarithm appears in the critical moment. Rare near-mergers of kinetic zeros control the large moments.

The [derivation](notes/random-kinetic-barriers.md) and [independent review](notes/review-random-kinetic-barriers.md) prove the compact-ensemble statement and record a counterexample to extending it to general Gaussian disorder. A [separate review](notes/review-random-finite-bulk.md) proves uniform control of the bulk correction, transferring every positive-moment asymptotic to finite bulk diffusion at nonzero mean velocity.

Choosing mobility before the offset is known gives an optimal expected response asymptotic to `18.3861 M^(-1/4)`. Choosing it after measurement gives `22.4046 M^(-1/5)`. The constants refer to the dimensionless scalar response; physical flow dispersion multiplies them by `KV²/Z`. Both sharp bounds include arbitrary integrable designs and have independent [scalar](notes/review-robust-mobility-design.md) and [finite-bulk](notes/review-robust-finite-bulk.md) reviews. See the [design theorem](notes/robust-mobility-design.md) and [prior-art audit](notes/robust-design-prior-art.md).

These are small-budget results. The asymptotically best fixed shape can perform worse than uniform mobility at a finite budget; the numerical record includes this reversal.

Optimizing the positive moment `E[J^q]` changes the threshold from `q=4/3` under uniform mobility to `q=8/5`. The [order theorem](notes/risk-sensitive-mobility.md) and [independent review](notes/review-risk-sensitive-mobility.md) give matching bounds:

| Moment order | Best achievable growth as the budget vanishes |
|---|---|
| `0<q<8/5` | `M^(-q/4)` |
| `q=8/5` | `M^(-2/5)[log(1/M)]^(7/5)` |
| `q>8/5` | `M^((2-3q)/7)` |

The bounds cover arbitrary integrable designs. Explicit graded profiles achieve them, but the theorem does not force every design with the same order to concentrate all its mass near the folds. The [literature audit](notes/risk-sensitive-prior-art.md) identifies prior risk-aware design and resource-allocation results; no exact collision with these transport orders was found.

For the cosine ensemble, sharp coefficients are now proved for every `0<q≤8/5`. At the critical order the coefficient is `2.02233076396939`, with a [separate independent review](notes/review-critical-risk-mobility.md). Above the threshold only matching-order bounds are claimed. The same three orders hold for a [general smooth family with finitely many nondegenerate folds](notes/generic-kinetic-folds.md), under explicit geometric and probability-density assumptions; this extension also has [independent review](notes/review-generic-kinetic-folds.md).

## Measurement resolution and finite bulk transport

Suppose the offset is measured only to an equal-width bin of size `Δ`, then mobility is chosen using that observation. The optimal mean scalar response satisfies, uniformly as both parameters vanish,

`Φ(M,Δ) ≍ M^(-1/5) + M^(-1/4) Δ^(1/4)`.

The resolution scale is therefore `Δ ≍ M^(1/5)`. When `Δ/M^(1/5)→0`, the sharp coefficient is the exact-observation value `22.40462823`. When `Δ→0` and `Δ/M^(1/5)→∞`, the coefficient multiplying `M^(-1/4)Δ^(1/4)` is `25.72382739`. The [theorem](notes/finite-precision-mobility.md), [independent review](notes/review-finite-precision-mobility.md), and [prior-art audit](notes/finite-precision-mobility-prior-art.md) distinguish these proved limits from the unproved formula at a finite, positive ratio.

A [general transfer theorem](notes/scalar-to-bulk-design-transfer.md) preserves all these optimized scalar values and sharp constants in the full bulk–surface model. It adds a vanishing uniform share of mobility at the same budget and with the same observation. Under fixed positive bulk diffusivity, nonzero mean velocity, bounded rates with a uniformly positive integral, and a connected closed one-dimensional wall, the bulk remainder grows at most logarithmically. Physical `q`th moment optima are asymptotic to scalar optima multiplied by `(KV²/Z)^q`. The proof covers arbitrary observation rules, including rules changing with the budget.

## Useful results with substantial prior-art overlap

- [Traveling-channel transport](notes/exploration-soft.md): a no-drift constraint, exact diffusivity corollaries, and a constructive nonuniqueness example for inverse transport. The main spectral formula is already closely represented in Guérin and Dean (2015).
- [Periodic-removal investigation](notes/exchange-prior-art.md): the basic time-averaging inequality and frequency-response formula are established. This direction was not promoted as a new theorem.
- Initialization-dependent anomalous variance is established renewal behavior. Its coefficients were checked here because using the stationary value for an injected pulse would give a factor-of-two error.

## Reproducibility

[Numerical verification](notes/numerical-verification.md) links the programs, convergence checks, and generated data. Standalone figures are available:

- [Surface-exchange checks](results/surface-exchange-verification.pdf)
- [Mobility design and disorder](results/mobility-design-and-disorder.pdf)
- [Positive-moment design checks](results/risk-sensitive-design.pdf)

A [transport and placement draft](notes/working-paper-kinetic-defects.md) and a [companion on uncertain mobility](notes/working-paper-uncertain-mobility.md) organize the model, results, proof outlines, and literature boundaries. The [closing report](notes/final-research-report.md) identifies the strongest contributions and remaining limits.

Development was closed at the user's request after completing verification of the stated results. Unproved extensions are labeled and excluded from the theorem claims. No guarantee of publication or citation impact is made.
