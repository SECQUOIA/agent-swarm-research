# Independent whole-manuscript review: foundations

Recommendation: accept this frozen manuscript on mathematical and scientific-content grounds. I found **0 MAJOR issues and 0 MINOR issues** requiring correction. This recommendation follows a fresh reading of the entire manuscript, not the acceptance statements in the development record.

## Scope and independence

I read `main.tex`, all 12 files in `sections/`, all five files in `appendices/`, all 23 bibliography entries, the required manuscript and supplement READMEs, and `development/COVERAGE.md`. I checked all **44 formal theorem, lemma, proposition, and corollary statements**, including the existence theorem proved across Appendix A, and the substantial unnumbered derivations. I read all six Python supplement scripts, the C++ simulator, the saved summary, and inspected the saved data through its verification script. I did not read prior review reports, author reports, coordinator assessments, or other current reviewers' reports, and did not contact other reviewers. The acceptance labels embedded in the required README and coverage map were not used as mathematical evidence.

Every file listed in `development/reviews/full-round1/snapshot.json` matched its SHA-256 hash before checking. Builds and executable checks used `/tmp/foundations-manuscript-xn_r6ftk`; no manuscript source, saved supplement data, or shared build file was modified. This report is the only review artifact written to the manuscript tree.

## Actionable findings

**MAJOR: 0.** No invalid theorem, missing argument requiring a new proof, materially unsupported scientific claim, or substantial coverage or clarity problem was found.

**MINOR: 0.** No correction is requested. There are consequently no numbered issue entries. I have kept nonissues and possible expansions out of these counts.

**Optional preferences:** none needed for this recommendation. A contents list could make a 55-page paper easier to navigate, but its absence is not a defect in the exposition or a condition of acceptance.

## Section and proof audit

The labels below identify the complete formal-result coverage. Locations are relative to the manuscript directory.

### Introduction and model

`sections/introduction.tex:1–198` and `sections/discussion.tex:1–55`: the abstract, contributions, assumptions table, and discussion match the proved results. The distinction between instantaneous sharp constants and exact long-time exponents is explicit. The three probability models—auxiliary number path, physical finite population, and independent continuum observations—remain distinct. The introduction does not claim novel compound-Poisson theory, a new classical Borel distribution, a new exponential-functional distribution, or a completed noisy nonparametric inverse method.

`sections/model.tex:14–149`, **`thm:existence`**: the measurable kernel assumptions, all-bounded-Borel weak formulation, mass-conserving solution class, variation conventions, count identity, and two sampling laws are consistent. Expected daughter count and mass are carefully distinguished from an eventwise complementary binary split. The finite-second-moment existence theorem is not silently imposed on the later results that need only an already supplied finite-count, finite-mass solution. The theorem's uniqueness claim is limited to locally bounded second moments.

### Fractional moments

`sections/fractional-moments.tex:6–263`: checked **`lem:pair`**, **`lem:moment-balance`**, **`thm:affinity`**, **`cor:critical`**, **`cor:moving`**, and **`prop:robust`**.

The pair inequality's reduction to the symmetric scalar function and its derivative sign pattern proves the stated strict equality case. For the truncated tests, the negative coagulation increment is bounded by `min(x^p,y^p)` and hence its additive-kernel integral by `2mM_p`. The fragmentation increment is nonnegative because `f_R(x)/x` decreases, and its uniform Jensen majorant is integrable. Thus the proof passes the complete weak balance, rather than only a formal differential inequality.

I recomputed the count normalization: the remaining coefficients are exactly `-a_p b-a_{1-p} sigma`. At criticality this becomes `-b kappa_p`; the half-moment normalization and the constants `kappa=3-2 sqrt(2)` are consistent across the paper. Monodisperse equal-split data supply actual initial right derivatives, so the instantaneous sharpness claim is justified. The moving-window proof correctly chooses different orders near zero and one for its two windows. The perturbed-kernel result requires a supplied solution and states a sufficient threshold only.

### Auxiliary process

`sections/auxiliary-process.tex:12–300`: checked **`thm:number-process`**, **`thm:controlled-path`**, and **`cor:controlled-size`**.

Normalization gives the claimed fragmentation rate `2 sigma` and coagulation rate `lambda N x`. The first-moment stopping argument controls overshoots through the finite partner mean; after removing the size stop, the stopped jump-count expectation remains uniformly bounded. Marginal identification uses the positive finite-jump expansion and nonexplosion, not an unproved uniqueness assertion for an unbounded forward generator. The output restriction retains incoming gain from all parent states.

The log-correction compensator is controlled by `lambda H^2/N`, and its time integral is finite under arbitrary allowed controls. The product martingale has conditional multiplier mean one half even with adaptive parent-dependent marks. Its global almost-sure supremum is finite by the maximal inequality. The resulting pathwise integrated coagulation intensity is finite without requiring its expectation to be finite; compensation after stopping at an intensity level then proves finite total count. The equality `E K_t=B_c(t)` does not contradict that pathwise conclusion. The final controlled-fragmentation dichotomy follows from these same paths and does not assume independent realized daughter fractions.

### Transport and logarithmic limits

`sections/log-limits.tex:6–448`: checked **`thm:transport`**, **`cor:constant-cost`**, **`thm:log-limits`**, **`cor:infinite-log-speed`**, **`prop:general-scale-transfer`**, **`prop:log-means`**, and **`cor:pure-coag`**.

The selfsimilarity requirement is exactly what makes the reference a standalone marked Poisson process. Clipped increasing Lipschitz tests prove the optimal transport cost without subtracting potentially infinite means. The constant-rate tail integrates to the stated `D_0` and exponent. The functional CLT reduction controls the maximum within-unit compound-Poisson fluctuation using a finite second jump moment; the nonlinear perturbation is uniformly bounded by the finite correction. Its Gaussian variance is the raw Poisson jump second moment. Ordinary Wasserstein conclusions add the initial first log moment precisely where required, and the first-moment-only speed assertion has a separate truncation proof.

The infinite negative-log-mean result follows by a common-event truncation argument. The KL identity uses the correct sampling Radon–Nikodym derivative and count-growth term. The pure-coagulation ordered limits and Borel benchmark agree with the normalization and do not assert convergence of the arithmetic mean or actual log variance.

### Last events and daughter comparisons

`sections/last-event.tex:22–220`: checked **`thm:last-controlled`**, **`cor:future-path-TV`**, and **`cor:last-moments-counts`**, together with the scalar optimal domination factor and Borel tail deduction.

The independent exponential threshold is applied to the fragmentation-only path up to its first future coagulation. Its expected accumulated hazard is exactly `q u_{t,T}`, including an infinite horizon. Jensen has the correct direction. Both infinite-activity and finite-activity controls give tail disappearance. The future-path coupling uses each process's own parent after divergence, preserving both marginals. The window-count moments and lack of uniform integrability follow from the exact compensator mean and finite last event. The Borel implicit equation yields the stated `sqrt(2) exp(-bt/2)` asymptotic.

`sections/daughter-comparison.tex:29–282`: checked **`thm:daughter-envelopes`**, **`cor:overlap-all-rates`**, and **`cor:critical-envelopes`**. Both benchmark hazards have first moment one. This suffices for their derivative bounds and killed-generator verification; no unavailable second hazard moment is used. Convex Jensen/chord comparisons give the stated supermartingale and submartingale directions. The terminal comparison error is bounded by `q exp(-bs)`. Positive epsilon daughters approach the reset benchmark with a vanishing expected residual hazard. The overlap constants use the correct chord argument, and the sharpness populations obey the positive mean-one constraint. The product normalization is `I^(1/2)/2`, not the unscaled classical exponential functional.

### Critical exact observables

`sections/critical-last-event.tex:18–279`: checked **`thm:exact-last-density`**, **`thm:general-last-density`**, **`cor:critical-moment-bracket`**, and **`prop:scalar-obstruction`**.

For equal splitting, the product recurrence cancels the direct coagulation loss. The remaining pair integrand `q Psi(q+v)` is bounded, so total-variation continuity is enough for the continuous density and initial right derivative. The Laplace PDE has the correct sign, and its derivative at zero uses only the conserved first moment.

For general measurable daughters, finite-horizon clock recursion gives a jointly measurable survival function; a limit along increasing deterministic horizons gives its infinite-horizon version. The last-event marking argument conditions at actual coagulation stopping times, projects to the post-event survival probability, and only then compensates a predictable function of time, pre-event state, and partner. This avoids differentiation of a merely measurable survival kernel and avoids conditioning at the non-stopping last event. Finite expected event count on bounded time intervals makes the integrated calculation legitimate. The density bound `j<=bh` and the lower calendar-time tail follow from the critical envelopes. The small-state two-point preparation proves instantaneous optimality of `b`.

The exponential-moment bracket includes divergence at the upper endpoint because `h(0)>0`. The scalar obstruction uses genuinely positive, finite-support populations; its dissipation bound tends to zero faster than every fixed power of its tail observable. The text correctly treats the exact critical calendar-time exponent as an unsolved further question, not a gap in these theorems.

### Finite physical populations

`sections/finite-population.tex:13–275`: checked **`prop:finite-count`** and **`thm:finite-discrepancy`**, plus the relative-moment and omitted-diagonal formulas.

The unordered-pair sum is `(L-1)nm`, giving birth and death rates `bL` and `b(L-1)`. The count mean, variance, martingale bracket, and uniform concentration constants follow from this chain. Absolute concentration does not require a positive limit for `c_n`; the relative-accuracy caveat is stated.

The discrepancy proof uses the same empirical initial measure for both models, a fixed fractional order, and the deterministic physical ceiling `nm`. It therefore proves the pathwise and expected-law CDF lower bounds without invoking propagation of chaos or numerical evidence. The threshold is sufficient, not a claimed first breakdown time. The diagonal correction is exactly `lambda(2-2^p)M_(p+1)/n`, including the count endpoint. The numerical section's descriptive claims agree with the archived summary, and its theoretical overlays are explicitly continuum references.

### Bulk-observable boundaries

`sections/observable-boundaries.tex:24–335`: checked **`thm:neutral-class`**, **`prop:observable-rigidity`**, **`prop:broadening-entropy`**, and **`thm:power-no-equilibrium`**, as well as the power-kernel positive-drift examples and the infinite-count equilibrium comparison.

The count-neutral necessity follows from monodisperse and two-atom fixed-mass preparations with variable count. The fractional and second-moment rigidity signs at monodispersity are correct. The second-moment bounds and sharp entropy production follow from the separately justified unbounded balances; expected daughter constraints suffice.

The stationary power-kernel proof is valid without negative population moments. Count balance first forces `s=m`. The total event flux is finite under count and mass, producing an invariant embedded transition kernel under `zeta=qv/(3mD)`. The singular test becomes integrable under that probability because its integral is proportional to `D M_(1-alpha)+2mN`. Testing truncated singular functions in the invariant finite-measure identity establishes finite gain and loss before subtraction. Symmetrization and concavity then bound the negative coagulation contribution by `alpha mN`, while fragmentation gives a strictly larger positive contribution. This is a stationary contradiction, not an implicit assertion of existence or nonexplosion for a time-dependent power-kernel process. The cited critical multiplicative equilibria have infinite count and do not contradict it.

### Fourier identification

`sections/fourier-identification.tex:50–346`: checked **`thm:factorization`**, **`cor:fourier-ratio`**, **`lem:one-sided`**, **`thm:fourier-identification`**, and **`prop:ratio-sampling`**.

The Fourier forcing is a paired increment; its integrable bound does not require separate log moments. The amplitude tail has exponent `delta=omega+Re psi`, and its continuity and local nonvanishing follow from uniform convergence near zero. The quotient estimate includes the correct attenuating factor. The logarithm is anchored continuously at zero.

One-sided uniqueness uses the lower half-plane with the correct sign of exponential damping. Subtracting the total signed mass at zero converts exponent equality into transform equality; reflection and restriction back to strictly negative jumps then identify the measure. The zero-selection case, separate mass/count observation for coagulation recovery, and hypothetical fraction-one atom are handled consistently. The variation-norm instability example respects both daughter constraints.

The empirical result is genuinely pointwise and uses independent continuum samples. Four real-component Hoeffding bounds produce `8 exp(-n epsilon^2/4)`. Both quotient inequalities use denominators justified by their respective signal conditions. The deterministic observation schedule balances the two displayed errors because `delta+d=omega`; it is not advertised as adaptive, minimax, or sufficient for stable full-law inversion.

### Appendix A: measurable-kernel existence and stability

`appendices/wellposedness.tex:12–284`: checked **`lem:weighted-comparison`** and the full proof of **`thm:existence`**.

Weak kernel integration is adequate on this standard Borel state space. The integrable variation bound gives norm-continuous integral curves without requiring strong measurability of moving atomic kernels. The local output-coordinate loss formula retains the full incoming measure. Its positive majorant satisfies an exact integrated gain/loss balance. Since the majorant dominates `|d|`, subtracting its loss gives the stated Gronwall inequality; the proof never differentiates a Hahn sign or a norm.

Polarization and retention of the direct loss yield

`P*w-a*w = lambda[bar m+2 bar M_2+y(bar N+2 bar m)]+sigma`.

This is bounded by the claimed integrable multiple of `1+y`. All absolute event terms have finite weighted variation under locally bounded second moments. The initial finite-third-moment cutoff construction is a valid contraction with weak kernel integrals and a positive integrating-factor map. Its count, mass, second- and third-moment estimates extend it globally. The cutoff residual is `O(1/r)` in time-integrated weighted variation using the common third-moment bound. Stability makes the approximants Cauchy in the required norm, so no measurable daughter kernel is passed through a merely narrow limit. The second initial-moment construction then uses initial truncation and only the common second-moment stability coefficient. Conservation and boundary tightness follow in the stated norm. I found no missing parent-continuity hypothesis or hidden Bochner-measurability step.

### Appendices B–E

`appendices/product.tex:11–127`: checked **`prop:product-periodic`** and **`prop:product-certificate`**. Splitting and completing the logarithmic product gives the stated sign of the periodic term and the positive remainder. The refined coefficients follow from the geometric sums of the first three alternating-log terms. The finite-product rational enclosure certifies the two 30-decimal endpoints.

`appendices/finite-count.tex:11–122`: checked **`prop:count-diffusion`**. The shifted process has independent critical branching families plus immigration. Its generating function and scaled transition transforms agree with the limiting squared-Bessel construction. The stopped bracket bound and compact containment establish path tightness, and vanishing jumps give continuity. The drift and diffusion normalization are `b` and `sqrt(2bZ)`.

`appendices/unbounded-moments.tex:11–85`: the tangent truncation, after subtracting its linear part, is an admissible bounded test. Both the truncated function and its residual are convex and vanish at zero; this gives simultaneous coagulation and fragmentation domination. The complete balance has integrable majorants using only locally bounded `M_2`. Endpoint convergence is justified as well. Continuity of `M_2` plus total-variation continuity yields the weighted continuity needed for the entropy sharpness derivative. There is no unproved use of `x^2` or `x log x` in the original bounded-test definition.

`appendices/observation-design.tex:21–204`: checked **`prop:preparation-shell`**, **`prop:dilution-gauge`**, and the unnumbered tomography and noise identities. The finite-shell converse includes the necessary skew-matrix correction to the linear term. The continuum two-constraint family is correctly only sufficient. The two-concentration unknown-source gauge and its third-concentration removal are algebraically correct, with physical nonnegativity kept separate. Reconstruction counts match the unrestricted parameter dimension; deterministic noise and finite-difference bounds include source error and curvature assumptions.

## Primary-source and attribution checks

I checked relevant primary-source passages directly rather than relying on the repository's literature notes. These were targeted attribution and normalization checks, not an exhaustive novelty search:

- Cepeda's hypotheses and Theorem 2.5 support the more restrictive, fixed-dislocation comparison and its homogeneity-moment qualification. The manuscript does not claim that theorem covers arbitrary measurable expected daughter kernels. [Primary paper](https://arxiv.org/pdf/1301.1934).
- Bertoin's equation (3) gives the stated Golovin–Borel solution with the additive-kernel normalization. The manuscript derives its last-event asymptotic separately. [Primary paper](https://www.numdam.org/item/10.1016/j.anihpc.2008.10.007.pdf).
- Bertoin–Biane–Yor's equation (1.3) and Theorem 1.1(i), equation (1.6), give the exponential sum and product with the scale conversion used here. [Primary paper](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf).
- Tran–Van's Proposition 4.3 and Remark 4.4 in the explicitly cited preprint contain the stationary-transform family and `G/(1-G)^3=Cq`. The manuscript's infinite-count deduction and conversion of kernel/selection conventions are consistent. [Primary preprint](https://arxiv.org/pdf/1910.13424v3).
- Garnier's Section 2.2 explicitly uses the two-time characteristic-function quotient and distinguished logarithm. The manuscript appropriately attributes this ingredient. [Primary preprint](https://arxiv.org/html/2405.10588v1).
- Hoang and coauthors' Sections 3.1.1–3.1.4 use an asymptotic size profile, log-transformed independent observations, Fourier reconstruction, and denominator regularization. The manuscript distinguishes their growth–fragmentation model from its nonlinear coagulation setting. [Primary paper](https://www.math.univ-paris13.fr/~phamngoc/HoangPhamRivoirardTran.pdf).
- I also accessed the original jump-representation and critical-fragmentation papers, and checked publisher/Numdam metadata for the short-time inverse paper and the Deaconu–Tanré citation. I do not count those accesses as a full independent audit of the cited papers. The latter confirms the bibliography's pages 549–579. The PMC page for Mirzaev and coauthors returned a browser challenge, so I do not claim to have independently inspected its full text in this review.

No priority claim in the manuscript depends on a failed search or the absence of a discovered predecessor. The main theorems provide their own specialized proofs; the checked citations supply historical context and classical ingredients.

## Build, supplement, and coverage checks

A clean private `make` completed successfully and produced **55 pages**. The final LaTeX log contained no warnings, undefined references/citations, multiply defined labels, or overfull/underfull boxes. I rendered and inspected the integrated figure page: all six panels, labels, legends, and the qualification in its caption are readable.

In the private copy I ran:

- `python3 supplement/verify_saved_particles.py`: passed all 90 snapshots, all nine declared runs, event-count identities, normalizations, mass ceiling, fractional-moment floor, CDF ranges, 6,588,932 total events, and archived summaries.
- `python3 supplement/count_neutral_power.py`: direct atomic drifts agreed with the formula and the rational positive lower bound was certified.
- `python3 supplement/last_coagulation_exact.py`: reproduced the overlap enclosure and illustrative positive-population values.
- A C++17 build followed by `--self-test`: passed weighted selection, resizing/removal, pair-rate and count-drift algebra, and conservation checks.

I inspected the sampler's event rate, birth decision, mass-weighted/uniform distinct-pair selection, event-clock handling across snapshots, and statistic normalizations. These agree with the described finite model in real arithmetic. The finite random resolution and floating-point limits are disclosed. I did not rerun the nine full research trajectories or the optional 2,000-seed count experiment, because those had already been reproduced and the present source/data checks raised no concern requiring that duplication. I do not treat the unarchived historical sanitizer harness as independently verified evidence.

The claim-level coverage map has a corresponding manuscript destination for each planned topic. The general-parent well-posedness, complete unbounded balances, general-parent last-event density, and rate-weighted singular stationarity argument are actually present and proved. The exact critical last-time exponent and stable noisy recovery of an entire daughter law remain explicitly stated research boundaries; neither is a promised theorem left unfinished.

Final assessment: **44 formal results reviewed; 0 MAJOR, 0 MINOR; accept the frozen manuscript.**
