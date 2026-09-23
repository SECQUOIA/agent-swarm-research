# Closing research report

2026-09-07. The user requested completion of current developments and then a stop. This record closes that work; no additional research direction is being pursued.

The strongest result package concerns how to allocate surface mobility when locations of slow chemical exchange are uncertain. It combines an unrestricted design theorem, a change in the influence of rare kinetic defects, and a quantitative measurement-resolution law. These are potentially useful transport questions for complex interfaces, adsorption, separation, and dispersion. They fit the diffusion and interfacial-transport setting identified in the initial [research-fit check](research-log.md).

Two working-paper drafts organize the results:

- [Kinetic defects, transport, and deterministic placement](working-paper-kinetic-defects.md).
- [Mobility design under uncertainty and finite observation precision](working-paper-uncertain-mobility.md).

The [results guide](../RESULTS.md) links detailed proofs, independent reviews, and literature comparisons. The drafts are research manuscripts with proof outlines and supporting notes, not claims of journal acceptance or experimental validation.

## Principal verified contributions

**Optimal design of positive disorder moments.** In the explicit ensemble `k_c(s)=(c+cos s)^2`, where `c` is uniform on `[-2,2]`, let `J` be the integrated inverse of the surface diffusion-and-exchange operator. The same mobility field must serve every realization and has integral budget `M`. The optimum of `E[J^q]` grows as

| Moment order | Optimal growth |
|---|---|
| `0<q<8/5` | `M^(-q/4)`, with an explicit sharp beta–gamma coefficient |
| `q=8/5` | `2.02233076396939 M^(-2/5)[log(1/M)]^(7/5)` |
| `q>8/5` | `M^((2-3q)/7)`, bounded above and below by positive constant multiples |

Uniform mobility instead has its moment transition at `4/3`. Design therefore changes the rate at which large disorder moments diverge. The lower bounds cover arbitrary nonnegative integrable designs, including budget-dependent fine structure. The three orders also hold for a general smooth one-parameter kinetic family with finitely many nondegenerate folds under the stated assumptions. Separate reviewers checked the general-order theorem, sharp subcritical coefficients, sharp critical coefficient, and generic extension.

**Value and precision of observing the defects.** Choosing mobility before the cosine offset is known gives a sharp mean optimum `18.3861 M^(-1/4)`. Choosing it after exact observation gives `22.4046 M^(-1/5)`. If only a bin of width `Δ` is observed, the optimum is bounded above and below by constant multiples of

`M^(-1/5) + M^(-1/4)Δ^(1/4)`.

Thus the measurement scale separating the two regimes is `Δ ≍ M^(1/5)`. Both sharp limiting coefficients are proved: `22.40462823` on the fine-resolution side and `25.72382739` multiplying the coarse-resolution term. The proof includes bins containing merging kinetic zeros; a regular-root calculation alone would not establish the joint limit.

**Validity with finite bulk diffusion.** A general comparison transfers optimized scalar values and sharp constants to the full bulk–surface transport model while preserving the budget and available observation. Adding a vanishing uniform mobility share bounds the regular bulk contribution by a logarithm, negligible against the proved divergent optima. Physical flow-dispersion moments acquire the factor `(KV²/Z)^q`. This result assumes fixed positive bulk diffusivity, nonzero mean velocity, constant affinity, a connected closed one-dimensional wall, and the stated uniform rate bounds.

**Deterministic transport and placement.** The earlier results remain useful: an explicit weak-surface-diffusion crossover at quadratic kinetic minima, a criterion for when vanishing mobility fails to regularize dispersion, an exact optimal local placement profile, and a finite-rate-floor design with explicit activation and merging thresholds. The local quadratic placement changes the small-budget divergence from `M^(-1/4)` under uniform allocation to `M^(-1/5)` under optimal allocation. The notes retain general-power and multiple-defect extensions with their review boundaries.

## Verification and practical limits

Each principal theorem has independent mathematical review. Numerical checks include mesh refinement, parameter quadrature refinement, conservation, independent transform inversions, and convex optimization with a separate lower certificate. Programs, generated JSON, and standalone figures are linked in [numerical-verification.md](numerical-verification.md).

The calculations also retain limitations. The asymptotically optimal blind mean design is worse than uniform mobility at a tested finite budget. Critical logarithmic asymptotics converge slowly. Sparse scenario quadrature can make an optimized design appear artificially favorable. These effects are documented rather than treated as evidence against the correctly stated limits or hidden by selecting favorable data.

The models impose no fixed fabrication length or pointwise mobility cap. The limits do not establish performance for a particular material or finite experimental budget. The exact scalar crossover at a finite positive ratio `Δ/M^(1/5)` and sharp supercritical moment constants remain unproved; they are explicitly excluded from the verified results.

## Novelty assessment

The strongest candidate for a further publication assessment is the uncertainty-and-measurement package. It gives a coherent transport question, sharp results, unrestricted lower bounds, a generic geometric extension, and a finite-bulk comparison. This is a judgment about the developed work, not a prediction of citations.

Targeted open-literature audits found no exact match to the main `8/5` design transition, its critical coefficient, or the joint measurement-resolution law. They did find substantial prior work on conductivity design, expected compliance, quantized decisions, rare-bifurcation moments, and optimal reinforcement. These ingredients are credited. Older chromatography full-text access gaps remain, so an absolute novelty claim is not justified.

Known-result collisions and useful negative results are preserved. The traveling-channel spectral formula overlaps published work; periodic-removal inequalities and preparation-dependent anomalous spreading are established; a Gaussian amplitude-collapse example invalidates an overly broad disorder-mean inference. None is presented as a new general mechanism.
