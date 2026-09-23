# Research record

Developed 2026-09-06–07. The current investigations are concluded at the user's request. This directory records original investigations, independent reviews, and failed novelty tests. A correct proof and a search that finds no match do not establish publication priority.

Start with [the consolidated results and verification report](RESULTS.md). It presents the main theorems, their relationship, prior-art distinctions, numerical evidence, and limits.

The completed [LaTeX paper and PDF](../paper-additive-coagulation/README.md) consolidate the additive topic in 55 pages. Five writing stages each completed five independent reviews and all required corrections. Five fresh reviewers then checked the whole manuscript, with zero major and zero minor findings. The [final report](../paper-additive-coagulation/development/FINAL-REPORT.md) records developments beyond the original notes and the verification scope.

The initial repository inspection found a literature knowledge base and no original theorem manuscripts outside it. The existing knowledge base is ignored by Git; new research records live here so they can be versioned. No literature artifacts are being redistributed.

## Current strongest direction

The main direction is quantitative separation of number-weighted and mass-weighted sampling in additive coagulation–fragmentation. The critical model conserves both count and mass, yet its size distribution continues to separate. More generally, an auxiliary process representing the number distribution has only finitely many coagulations almost surely, with quantitative last-event tails, although its expected cumulative coagulation count may diverge.

| Result | Proof status | Novelty assessment |
|---|---|---|
| [Sharp fractional-moment decay and separation of number from mass](results/invisible-kinetics-extension.md) | Independent review complete; weak-test justification included | No exact match found in bounded search; broader asymptotic literature comparison remains necessary |
| [Finite log-size correction at arbitrary constant fragmentation rate](results/general-additive-log-coupling.md) | Independent full proof review complete; no logarithmic moments needed for the finite-cost statement | Pure fragmentation limits and tagged-process methods are established; no matching nonlinear transport bound found in the audited sources |
| [Controlled rates and parent-dependent daughters](results/controlled-additive-trajectories.md) | Independent actual-file review complete | Finite accumulated log correction and finite last auxiliary coagulation are the candidates; the process representation uses known methods |
| [Last-event tails, future-path approximation, and sampling overlap](results/last-coagulation-tail.md) | Independent actual-file review complete; sharp critical overlap factor also checked | Standard first-event killing combined with nonlinear moment decay; no matching full theorem found in focused open-source audit |
| [Sharp daughter-law bounds](results/sharp-daughter-extremality.md) and [exact critical observables](results/last-coagulation-exact-equal-split.md) | Independent actual-file reviews complete, including limiting sharpness and negative scalar-closure result | Exponential functionals and convex comparison are established; the specific auxiliary-event bounds and optimal sampling-overlap comparison are the candidates |
| [Identification from late-time Fourier ratios](results/fourier-identification.md) | Independent full proof review complete | Fourier and Mellin inversion have close precedents; the candidate is the explicit vanishing error from nonlinear additive coagulation |
| [Finite-population failure of mass predictions at logarithmic times](results/finite-population-breakdown.md) | Independent review complete | Logarithmic finite-size effects are known; simultaneous accurate count and nearly maximal mass-CDF discrepancy is the narrower candidate |

These results use explicit model assumptions and do not claim that real processes follow the model. The auxiliary number process is not a physical mass-tagged particle. The original [existence note](results/additive-model-wellposedness.md) covers selfsimilar time-dependent daughters. The completed paper now supplies global mass-conserving existence for measurable parent- and time-dependent daughters with finite initial second moment, and uniqueness in the locally bounded second-moment class. Its estimates under only finite count and mass remain conditional on a supplied solution when that construction does not apply.

The [finite-particle experiment](results/critical-additive-particle-experiment.md) has also passed independent code and statistical review. Nine runs illustrate number–mass separation. They do not numerically establish the continuum discrepancy without a deterministic-solution comparison. The new theory remains a set of research candidates, not a publication-priority certification.

## Other retained findings

- [Coarse graining](ideas/coarse-graining.md): exact dimension formulas, a fragmentation-induced increase in dimension, and quantitative approximation bounds. A deeper audit found that a 1988 semigroup theorem supplies much of the core structure. Treat the dimension results as applications of established theory, with useful self-contained proofs, rather than an independent general theorem.
- [Inverse experimental design](ideas/inverse-design.md): a complete class of mechanisms invisible to count measurements at fixed material loading, plus concentration-based reconstruction. Elementary mixture gauges are classical. The stronger distributional consequences appear in the active direction above.
- [Extinction with unknown daughter dependence](results/extinction-coupling.md): the basic bounds are known-method corollaries. [Uniform near-critical bounds](results/extinction-near-critical.md) and [a rule for tied reproductive values](results/extinction-perron-ties.md) give narrower explicit results, independently checked, with uncertain standalone impact.
- [Power-kernel nonstationarity](results/count-neutral-power-kernels.md): independently verified exclusion of finite-count equilibria beyond the additive case, and an explicit failure of the earlier fractional-moment monotonicity. Known infinite-count equilibria are distinguished.
- [Fourier sampling certificate](results/fourier-sampling-tradeoff.md): independently checked finite-time error and observation-time balance under an explicit independent-sampling model. This is a supporting application of established concentration tools, not a full statistical inversion method.

## Verification and continuity

The [reviews directory](reviews) contains independent proof and literature reports. The [verification directory](verification) contains reproducible numerical and exact-arithmetic checks; these supplement proofs. Each result records its own assumptions and review status.

All current theorem developments and their independent reviews are complete within their stated scope. Unresolved mathematical questions and limits are recorded in the result files. No further research directions are active. Findings traced to prior theory are retained with corrected attribution.
