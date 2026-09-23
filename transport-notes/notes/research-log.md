# Research log

## 2026-09-06: Initial inventory and direction selection

The repository has a local literature library describing 167 read packages, organized into seven topics and a ranked research agenda. There were no separately tracked original-result notes or programs at the start. Existing topic pages synthesize published work and propose investigations; these are not original results.

Research fit was checked against the [Purdue faculty profile](https://engineering.purdue.edu/ChE/people/ptProfile?resource_id=169352), [group research description](https://viveknarsimhan.wixsite.com/website/research), and [group publications](https://viveknarsimhan.wixsite.com/website/publications). Relevant areas include particulate transport in complex fluids, complex interfaces, membrane dynamics, and diffusion and heat/mass transfer. These pages were accessed 2026-09-06.

Three investigations are active:

1. **Traveling compliant channels.** An exact invariant-measure constraint may forbid asymptotic passive-tracer drift at zero mean fluid flux. A reduced traveling-channel model may admit nonperturbative diffusivity bounds and monotonicity in traveling speed. Independent derivation and literature comparison pending.
2. **Degenerate surface exchange.** Rates of adsorption and desorption can vanish together at isolated surface locations while preserving finite equilibrium affinity. This may create divergent dispersion and nonanalytic regularization by weak surface diffusion. Derivation, comparison with trap models, and independent review pending.
3. **Periodic removal as a transport probe.** Fixed-mean periodic killing cannot improve the asymptotic removal rate in a fixed cooperative exchange system. This is established mathematics, not a new result. Frequency-response measurements may probe the survival-conditioned exchange process, but reversible spectral monotonicity and Stieltjes structure are also established. Any proposed advance must go beyond rephrasing these facts.

Independent agents develop the first two directions and audit prior art for the third. Separate reviewers will assess concrete derivations. Exploratory numerical success will not substitute for a proof, and a proof within a reduced model will not establish validity of that reduction outside its stated regime.

## Known-result collisions retained as constraints

- Time averaging for cooperative periodic matrices already yields the basic constant-removal inequality without detailed balance; see the forthcoming exchange prior-art note for exact sources.
- Generic adsorption/desorption contributions to Taylor dispersion are established, including Levesque et al. (2012). The proposed singular-rate limit requires a separate comparison.
- A 2026 preprint already addresses compliant-channel Taylor dispersion (arXiv:2604.05592). Generic addition of pulsation or wall compliance is therefore insufficient novelty.

## Status terminology

- **Candidate:** a proposed result with open correctness or scope questions.
- **Verified within model:** derivation and independent review agree under explicit assumptions, with appropriate numerical checks.
- **Possible novelty:** targeted literature search has not found the exact result; overlap and search limits remain stated.
- **Publishable:** reserved for a coherent, thoroughly checked advance with a defensible comparison to prior work. None assigned yet.

## First verified theorem and subsequent investigations

The static surface-exchange crossover is now independently verified within its model. Separate reviewers checked the reduced resolvent, full-bulk variational separation, uniform flux estimate, limiting bulk correction, and scalar localization at multiple quadratic minima. The main result is in [result-surface-exchange.md](result-surface-exchange.md); reviews are in [review-singular-exchange.md](review-singular-exchange.md) and [review-localization.md](review-localization.md). Numerical checks and a standalone figure are recorded in [numerical-verification.md](numerical-verification.md).

The strongest novelty claim is the coupled transport theorem and its geometric surface-diffusion cutoff. The [independent literature audit](singular-exchange-prior-art.md) found that multirate trapping, the anomalous variance exponent, preparation-dependent factor two, and oscillator kernel are established. Older chromatography full-text access gaps remain. No claim of an entirely new anomalous-transport mechanism is justified.

The traveling-channel dispersion formula has direct prior-art overlap with Guérin and Dean (2015). It is retained as a physical corollary. A constructive inverse result uses classical homometric sets to give different smooth channels with the same all-speed dispersion and global hydraulic measurements; this is a possible application of known phase-retrieval nonuniqueness, not a new general inverse-theory principle.

Subsequent work:

1. **Vanishing mobility.** A variational threshold and an inverse-square-operator crossover have independent review. For a quadratic exchange zero and mobility vanishing as `|s|^n`, finite dispersion requires `n<3`. Generic quadratic mobility zeros still regularize dispersion, but with a different fractional power. Domain and initial-law qualifications are explicit.
2. **Observable cancellation.** If local surface drift equals the mean tracer drift at a kinetic minimum, that minimum need not create a dispersion divergence. This is recorded as a corollary, with a tensor extension.
3. **Optimal uniform mobility.** Isotropic surface diffusion both releases trapped particles and adds axial Brownian spreading. Convexity and a finite-floor threshold may give an explicit optimal-mobility design law. Review is ongoing.
4. **Optimal placement of mobility.** A candidate whole-line solution allocates a fixed integral of diffusivity near the kinetic zero and changes the small-budget exponent from `−1/4` to `−1/5`. Independent verification and a comparison with optimal-conductivity theory are ongoing. The generic variational dual already appears in optimal-reinforcement literature, so novelty must be more specific.

## 2026-09-07: Design and uncertainty extensions

The fixed-budget placement theorem now has two mathematical reviews, including compact-wall localization, multiple defects, and finite bulk transport. The joint isotropic-mobility optimum has a weak-flow `|V|^(5/3)` cost. The finite-floor placement problem has an explicit three-regime solution, independently checked through a global variational certificate and separate primal and dual numerical optimizations. See [the results guide](../RESULTS.md) for navigation.

The random-offset kinetic family `k_c=(c+cos s)^2` now has an independently verified moment theorem. Fixed-realization asymptotics were insufficient: uniform estimates around coalescing zeros were required to prove the disorder averages and critical logarithm. A Gaussian single-mode counterexample shows that even the mean can be infinite at every positive surface diffusivity when rare samples lose almost all killing. That negative result is retained to prevent an unsupported general-disorder claim.

The finite-bulk random-offset extension is being checked using an exact identity for `k_c''` and a uniform flux estimate. Robust mobility design is also active: choosing the design before the offset is known appears to retain the `M^(-1/4)` divergence, whereas adapting to the measured offset permits `M^(-1/5)`. A sharp lower bound must cover arbitrary microscopic placement patterns, not only a chosen smooth family.

The numerical records now include mesh refinement, finite-bulk conservation checks, independent Laplace inversions, convex optimization from zero initial designs, coalescing-zero matching, and disorder quadrature. Finite-parameter errors and slowly converging means are stated rather than hidden by reporting only fitted exponents.

The finite-bulk disorder and before/after-measurement design reviews are now complete. Uniform exchange-flux estimates close both transfers for fixed positive bulk diffusivity and nonzero mean velocity. The exact design exponents and constants survive this physical extension. A working-paper draft now brings these results together; it has its own independent scope and formula audit.

The next investigation optimizes positive disorder moments. Preliminary upper and lower bounds give a new design threshold at moment order `8/5`, compared with `4/3` under uniform mobility. The critical order appears to require a logarithmic allocation across many spatial scales. This result is undergoing independent mathematical and literature review; exact constants beyond the mean case remain separate questions.

Independent review now verifies every regime of the positive-moment order theorem, including unrestricted lower bounds and the critical logarithm. The separate literature audit found established risk-aware design and resource-allocation precedents, but no exact theorem matching these orders. Numerical trials support the high-moment improvement and show slow convergence at the critical order. Work continues on sharp subcritical constants, finite-bulk transfer, general smooth landscapes, and finite-precision measurement.

## Closure requested by the user

The user subsequently requested completion of current developments, no new ideas, and a final report. The existing proof and review tasks were completed. Sharp subcritical and critical moment constants now have independent reviews; the generic fold theorem, the finite-precision order law and sharp endpoints, and the same-budget scalar-to-bulk transfer are also verified. The final manuscript audit made the connected-wall assumption explicit for the general transfer lemma. The surface relative asymptotic now explicitly requires a nonempty set of kinetic zeros.

Two working-paper drafts, detailed independent reviews, reproducible numerical records, and a [closing report](final-research-report.md) are retained. Remaining conjectures—the supercritical sharp constants and the exact intermediate measurement crossover—are clearly excluded from verified claims. All current development and documentation work is closed; no further research direction is active.
