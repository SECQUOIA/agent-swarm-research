# Independent full-manuscript review: integration and PBE readership

Review date: 2026-09-07. Recommendation: **accept within the stated scope**.

**Findings: 0 MAJOR, 0 MINOR.** I found no mathematical gap, invalid claim, material ambiguity, or relevant-result omission requiring correction. I checked all **44 theorem, lemma, proposition, and corollary statements and their proofs**, rather than restricting the review to exposition. Two optional presentation preferences appear separately below and are not acceptance conditions.

## Independence, snapshot, and scope

I read `main.tex`, all twelve main-section files, all five appendices, all 23 bibliography entries, `README.md`, `development/COVERAGE.md`, the supplement README, and every supplement source script and the C++ simulator. I inspected the saved-data checks and numerical summaries, the manuscript's rendered pages, and the relevant research-result inventory and substantive source statements. I did not read manuscript author reports, earlier manuscript review reports, other current whole-manuscript reports, or coordinator assessments. I did not contact other reviewers. References to earlier acceptance in the required README and coverage map were treated as development metadata, not mathematical evidence.

All files listed in `development/reviews/full-round1/snapshot.json` matched their recorded SHA-256 digests when checked. The snapshot file's own SHA-256 is `148ebf6bff3d74ac6e25f87330199b0fe4b42e5c30b4ac702cead00bb9683413`.

The review build was isolated in `/tmp/full-r5-d794y5pi`. I copied the mathematical source, bibliography, Makefile, and supplement there and ran `make -B`; I did not run a shared manuscript build or change mathematical source, figures, or saved research data. The resulting PDF has 55 pages. Its final LaTeX log has no warnings, undefined references, overfull boxes, or underfull boxes. Its SHA-256 is `3025af2a41b389ad9afc1f4db98d7e820f7cefc1740356d719c0da3bd4161610`; build-time PDF metadata can change this digest without changing the content.

## Formal proof coverage

Each row records an independently checked statement and the main mathematical boundary I examined. “Pass” means that the argument supports the statement under its written assumptions; it does not certify novelty or an unstated stronger conclusion. Locations below are relative to the manuscript directory and refer to the reviewed snapshot.

| No. | Statement and source location | Independent check | Result |
|---|---|---|---|
| 1 | Theorem 2.3, `sections/model.tex:78`; Appendix A | Weighted comparison retains the direct loss cancellation. Bounded-kernel construction uses weak measure integrals; third-moment cutoff errors are integrable and vanish. Initial truncation then needs only a common second-moment bound. Count, mass, Borel daughters, and uniqueness pass in weighted variation. | Pass |
| 2 | Lemma 3.1, `sections/fractional-moments.tex:6` | Recomputed the normalized scalar inequality. The ratio controlling the second derivative strictly decreases; the endpoint and derivative argument proves strictness away from equal sizes. | Pass |
| 3 | Lemma 3.2, `sections/fractional-moments.tex:42` | Checked both coagulation and daughter bounds for `min(x^p,R)`. Their dominating integrals require count and mass, not an additional size moment. | Pass |
| 4 | Theorem 3.3, `sections/fractional-moments.tex:83` | Recomputed raw coefficients and the count normalization, obtaining `-a_p b-a_(1-p) sigma`. Checked the squared half-moment factor and separate-rate instantaneous sharpness. | Pass |
| 5 | Corollary 3.5, `sections/fractional-moments.tex:151` | Critical coefficients, their unique maximum, both window estimates, weak boundary limits, and stationary contradiction follow with finite-time mass conservation retained. | Pass |
| 6 | Corollary 3.6, `sections/fractional-moments.tex:198` | Both endpoint ratios of `kappa_p` have limit `log 2`; separate fixed exponents give the two moving-window estimates under the strict velocity inequality. | Pass |
| 7 | Proposition 3.7, `sections/fractional-moments.tex:224` | Kernel upper bounds justify testing; lower bounds determine dissipation. Recomputed the factorized coefficient and the sufficient `s_*<2am` threshold. | Pass |
| 8 | Theorem 4.1, `sections/auxiliary-process.tex:12` | Re-derived normalization and both jump rates. Checked first-moment stopped nonexplosion and the finite flux `2 sigma+b`. Full incoming gain remains in restricted-output equations; minimal positive expansion plus nonexplosion identifies the marginal probability. | Pass |
| 9 | Theorem 4.3, `sections/auxiliary-process.tex:174` | Checked the logarithmic increment bound, compensator, controlled-clock integration, true finite-horizon product martingale, pathwise bounded maximum, and finite total hazard. The expected count identity is compatible with almost-sure finite count. | Pass |
| 10 | Corollary 4.4, `sections/auxiliary-process.tex:283` | Infinite fragmentation activity forces the size product to zero; finite activity gives finitely many fragmentation events in addition to the finite coagulation count. | Pass |
| 11 | Theorem 5.1, `sections/log-limits.tex:48` | Independent marked reference is justified only for selfsimilar daughters. Clipped increasing Lipschitz tests establish optimality of the ordered coupling without subtracting infinite logarithmic means. | Pass |
| 12 | Corollary 5.3, `sections/log-limits.tex:129` | Integrated the exponential forcing bound and checked `omega`, `D_0`, and their critical factors. | Pass |
| 13 | Theorem 5.4, `sections/log-limits.tex:165` | Checked the compound-Poisson raw second-moment variance, unit-interval oscillation bound for the functional limit, almost-sure uniform perturbation, ordinary transport CLT, and truncated first-moment LLN. Initial log integrability is imposed only where used. | Pass |
| 14 | Corollary 5.5, `sections/log-limits.tex:287` | Bounded jump truncations and a common probability-one event justify the infinite-mean limit. Jensen is applied to the truncated positive fraction before its cutoff is removed. | Pass |
| 15 | Proposition 5.6, `sections/log-limits.tex:316` | The path difference is uniformly bounded by `A_infinity`; its scaled bound directly transfers weak and J1 limits. No unsupported stable domain of attraction is asserted. | Pass |
| 16 | Proposition 5.7, `sections/log-limits.tex:348` | Recomputed mean-log, geometric prefactor, and KL count term; all needed logarithms are integrable under the stated assumptions, including the zero-fragmentation convention. | Pass |
| 17 | Corollary 5.8, `sections/log-limits.tex:403` | Ordered endpoint couplings yield the exact cost and remaining tail; eventual constancy gives a proper positive-size limit without logarithmic moments. | Pass |
| 18 | Theorem 6.1, `sections/last-event.tex:22` | First-event hazard uses the fragmentation-only future, not the full future compensator. Its conditional expectation equals `q u_(t,T)` by count cancellation. Checked both possible total coagulation-activity cases in the proof of finiteness. | Pass |
| 19 | Corollary 6.2, `sections/last-event.tex:115` | Common clocks and uniforms preserve both marginal daughter kernels even after states differ. Probability of first disagreement bounds total variation of the complete future path, including infinite horizon. | Pass |
| 20 | Corollary 6.3, `sections/last-event.tex:148` | Recomputed exponential-moment integral, constant window count mean, conditional-mean lower bound, and higher-power bound. Event-bearing probability is positive because the mean is positive. | Pass |
| 21 | Theorem 7.1, `sections/daughter-comparison.tex:29` | Both benchmark hazards have mean one at all stated rates. Recomputed killed generator signs from convexity. Bounded expectation passage is sufficient; positive epsilon-daughters approximate the reset hazard in L1, including the residual after the first small mark. | Pass |
| 22 | Corollary 7.2, `sections/daughter-comparison.tex:160` | Concave chord gives the lower overlap coefficient, the first-event bound gives the upper coefficient, and monodisperse admissible populations show lower sharpness. | Pass |
| 23 | Corollary 7.3, `sections/daughter-comparison.tex:235` | Critical exponential and equal-split hazards give the rational/product envelopes. Recomputed all overlap constants and the positive mean-one two-point construction attaining the upper constant in the limit. | Pass |
| 24 | Theorem 8.1, `sections/critical-last-event.tex:18` | Product recurrence cancels the bounded-test loss exactly. The pair integrand is bounded by one, making total-variation continuity sufficient for density continuity. Checked Laplace PDE sign, independent mixture, and zero atom. | Pass |
| 25 | Theorem 8.2, `sections/critical-last-event.tex:107` | Conditioning occurs at each genuine event stopping time and uses its post-event state before compensation. Rational envelopes imply `j<=bh`; the positive two-point preparation proves instantaneous coefficient sharpness. | Pass |
| 26 | Corollary 8.3, `sections/critical-last-event.tex:181` | Checked the tail bracket, positive initial event probability, and divergence at the upper exponential-moment endpoint itself. | Pass |
| 27 | Proposition 8.4, `sections/critical-last-event.tex:213` | Both atoms remain positive and the law has mean one. The dissipation is bounded by the small atom plus `Psi(R)`; finitely many product factors give decay faster than any chosen power. Continuity extends an initial strict violation to positive time. | Pass |
| 28 | Proposition 9.1, `sections/finite-population.tex:34` | Recomputed distinct-pair total rate, count generator on first two powers, variance, martingale bracket, and maximal L2 constants. Nonexplosion and eventwise mass conservation are justified. | Pass |
| 29 | Theorem 9.2, `sections/finite-population.tex:103` | The finite support ceiling and continuum fractional moment yield the stated CDF bound from identical initial data. Checked cancellation of `m`, fixed choice of `p`, uniformity under bounded `c_n`, expectation version, and simultaneous count accuracy. | Pass |
| 30 | Theorem 10.1, `sections/observable-boundaries.tex:24` | Monodisperse and two-atom fixed-mass preparations determine the diagonal and cross kernel; direct substitution proves sufficiency. Full-time neutrality uses a valid integrable count balance. | Pass |
| 31 | Proposition 10.2, `sections/observable-boundaries.tex:56` | Recomputed both fractional and second-moment monodisperse vector fields. Nonnegative `d` and positive strict constants force pointwise zero kinetics. | Pass |
| 32 | Proposition 10.3, `sections/observable-boundaries.tex:95` | Checked exact M2 production, daughter bounds, entropy pair limit as `p` approaches one, and the sharp net entropy coefficient. Appendix D supplies the required unbounded balances and initial right derivative. | Pass |
| 33 | Theorem 10.4, `sections/observable-boundaries.tex:178` | Count balance forces `s=m`; finite flux gives the invariant rate-weighted probability. The inverse power is integrable under that probability. Monotone bounded tests justify gain/loss subtraction, and the symmetrized coagulation estimate is strictly beaten by fragmentation. | Pass |
| 34 | Theorem 11.1, `sections/fourier-identification.tex:50` | Recomputed forcing bound, sign of the damping exponent `delta=omega+Re psi`, integral amplitude, absolute/relative errors, and uniform local nonvanishing. | Pass |
| 35 | Corollary 11.2, `sections/fourier-identification.tex:104` | Checked denominator lower bound, both errors in the quotient, uniform local convergence, and the anchored logarithm branch. | Pass |
| 36 | Lemma 11.3, `sections/fourier-identification.tex:143` | Subtracting the zero atom converts exponent equality to transform equality. Negative support gives damping in the lower half-plane; reflection across the zero boundary segment and Fourier uniqueness identify the signed measure. | Pass |
| 37 | Theorem 11.4, `sections/fourier-identification.tex:173` | Intersecting candidate low-frequency intervals suffices for uniqueness. Checked rate and daughter normalization, zero-selection nonidentification, and separate count/mass recovery of lambda. | Pass |
| 38 | Proposition 11.5, `sections/fourier-identification.tex:258` | Recomputed the four-component Hoeffding union bound and both quotient identities. The strict observed-denominator requirement, signal condition, and schedule exponent all have the stated constants. | Pass |
| 39 | Lemma A.1, `appendices/wellposedness.tex:67` | The survival majorant has an exact integrated weighted loss identity. Replacing its loss by that of the dominated variation gives the stated Gronwall estimate without differentiation of a Hahn sign. | Pass |
| 40 | Proposition B.1, `appendices/product.tex:11` | Re-indexed the two product tails, checked the quadratic and linear log terms, endpoint periodicity, and geometric sums in both explicit remainder bounds. | Pass |
| 41 | Proposition B.2, `appendices/product.tex:76` | Omitted log sum gives the exponential bounds; the rational lower surrogate and exact 128-factor certificate validate both displayed decimal endpoints. | Pass |
| 42 | Proposition C.1, `appendices/finite-count.tex:11` | Shifted count is critical branching with immigration. Checked PGF, scaled transition transform, compact containment, stopped martingale tightness, and the dimension-two squared-Bessel normalization and moments. | Pass |
| 43 | Proposition E.1, `appendices/observation-design.tex:21` | Recomputed the projector construction of `A_0`, residual in the row space, skew correction sign, converse, and rank bound. Strict positive feasibility and `h!=0` cover the needed algebraic boundaries. | Pass |
| 44 | Proposition E.2, `appendices/observation-design.tex:97` | Monodisperse and equal-mixture evaluations give the complete one-concentration gauge. Solving the two-concentration unknown-source system gives the stated constants, and a third concentration removes them. | Pass |

I also checked the consequential equations outside numbered formal statements: inverse-size generator transformation; Golovin–Borel normalization and last-event asymptotic; product recurrence and Taylor coefficients; omitted-diagonal finite-generator correction; power-kernel fractional counterexample and multiplicative equilibrium rescaling; the hypothetical fraction-one atom recovery; variation-norm instability; finite-grid tomography formulas, parameter count, and short-time/noise constants. No correction is required.

## Integration, assumptions, and completeness

The opening argument is appropriate for a PBE reader. It starts with familiar count, mass, and mean-size observables, then introduces number versus mass sampling before using their affinities. The introduction explains the connection between fractional-moment decay, the finite log correction, path comparison, the physical material ceiling, and late-time Fourier cancellation. The abstract accurately limits transport to parent-independent fractions and distinguishes the finite-vessel theorem from the independent continuum sampling certificate.

The three stochastic objects are explicitly separated in the introduction, in their own sections, and in the discussion. The auxiliary process is not described as a material genealogy. Its doubled fragmentation rate follows from normalized number sampling. The finite vessel has complementary eventwise positive binary splits, a stricter assumption than the expected daughter measure of the continuum equation. The empirical Fourier samples are independent draws from deterministic continuum marginals. Consequently the logarithmic time in sample size is not silently equated with the finite-vessel growing-time approximation scale.

The assumption roadmap agrees with the statements. Finite initial M2 is a sufficient existence hypothesis and is not silently made a log-moment hypothesis. The stronger second-moment class is used for entropy and broadening. Constant-rate and critical specializations are announced where introduced. Parent dependence is retained in controlled estimates and daughter envelopes and is removed precisely for the independent fragmentation reference and Fourier application. Total variation distance versus full signed variation is consistently distinguished. Reused local symbols are defined, with explicit distinctions for `b(t)`/`b_(t,x)`, `H`/entropy, the controlled clock/amplitude, and Laplace/Fourier transforms.

The coverage map and relevant source-result inventory account for the complete substantive line of work:

- Well-posedness, all fractional orders, sharp instantaneous coefficients, Hellinger/TV separation, boundary limits, moving windows, and perturbation criterion appear in Sections 2–3 and Appendix A.
- Controlled auxiliary construction, marginal identification, finite correction/count, constant-rate transport, log limits, entropy identity, and the pure-coagulation endpoint appear in Sections 4–5.
- Controlled last-event/window tails, future-path TV, rare event-bearing counts, sharp daughter envelopes, overlap constants, critical exact density/Laplace observables, lower tail, scalar obstruction, and product errors appear in Sections 6–8 and Appendix B.
- Exact physical count laws, logarithmic-time mass discrepancy, omitted diagonal, all nine retained trajectories, classical count diffusion, bulk-observable classification/rigidity, M2 and entropy production, and power-kernel boundaries appear in Sections 9–10 and Appendices C–D.
- Fourier factorization, ideal identification, independent empirical ratio bounds, observation-time balance, preparation-shell algebra, concentration/source ambiguities, tomography, and noise/preparation qualifications appear in Section 11 and Appendix E.

The manuscript improves on the narrower existence note by supplying a weighted-variation proof for measurable parent dependence and uniqueness in its stated M2 class. The inverse appendix preserves the distinction between a complete finite-grid shell classification and a continuum sufficient family under two constraints. No relevant completed result in the mapped additive-coagulation program is missing. The unrelated extinction and coarse-graining investigations are appropriately excluded.

The unresolved exact critical calendar-time exponent and stable full daughter-law inversion from noisy local frequencies are consistently identified as separate research questions. Neither is promised by the abstract or required to complete a theorem. Likewise, the manuscript does not claim an optimal first finite-population breakdown time, count collapse at logarithmic time, a density-level Gaussian limit, raw-variance convergence, or physical zero-size daughters attaining the lower envelope.

## Sources and attribution

All scientific citations resolve in the private build, and the 23 bibliography entries are complete enough to locate the cited works. Repository development notes are not used as scientific authorities. I independently checked these particularly important direct sources:

- The original displayed additive solution agrees with equation (3) of [Bertoin (2009)](https://www.numdam.org/item/10.1016/j.anihpc.2008.10.007.pdf). The paper credits Golovin and labels its last-event formula as a deduction from this established solution.
- Equations (1.3), (1.6), and Theorem 1.1(i) of [Bertoin, Biane, and Yor (2004)](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf) give the exponential sum and transform used here. The manuscript's factor of one half in `S=I^(1/2)/2` is correct.
- [Garnier, Section 2.2](https://arxiv.org/html/2405.10588v1) explicitly uses two-time characteristic-function quotients and a distinguished logarithm. The manuscript credits that algebra while identifying its own nonlinear remainder as the additional ingredient.
- [Hoang et al., Sections 3.1.1–3.1.4](https://www.math.univ-paris13.fr/~phamngoc/HoangPhamRivoirardTran.pdf) supports the comparison to log-size Fourier estimation and denominator regularization from independent asymptotic-profile samples. The different growth/fragmentation model is correctly stated.
- [Tran and Van, preprint Proposition 4.3 and Remark 4.4](https://arxiv.org/pdf/1910.13424v3) give the cited stationary transform family and relation `G/(1-G)^3=Cq`. The manuscript's further infinite-count deduction and its normalization to `K=2xy` are correct.
- The locally available full text of Ramkrishna's *Population Balances* supports the chapter references: Chapter 2 develops the framework, Chapter 6 treats inverse problems, and Chapter 7 treats stochastic populations and mean-field limitations.

These checks support the main attribution boundaries; they are not an exhaustive historical priority search. I inspected the remaining citations in their mathematical and modeling context. I did not obtain the full primary text of every background PBE article during this review, and do not claim a fresh full-text verification of every bibliographic source. No dependent mathematical gap or misattribution was found.

## Numerical evidence, reproduction, and rendered document

I read the simulator's event selection, Fenwick tree growth/removal, output timing, normalization, and diagnostics, together with the runner, figure script, archived-data verifier, optional count wrapper, and both arithmetic scripts. The event sampler has the stated unordered pair rates; snapshots do not restart the clock. Finite floating-point and random-grid limitations are stated accurately. The prior transient sanitizer harness is explicitly described as unarchived, rather than presented as a newly reproducible retained artifact.

In the private copy:

- `make -B` passed and produced 55 pages with a clean final log.
- `python3 supplement/verify_saved_particles.py` passed: all nine declared runs, 90 snapshots, count identities, moment floor, CDF ranges, mass ceilings, summaries, and 6,588,932 events.
- `python3 supplement/count_neutral_power.py` passed its direct/formula checks and exact rational certificate `151/500`.
- `python3 supplement/last_coagulation_exact.py` passed and reproduced the supplied JSON byte-for-byte.
- The C++ source compiled with the documented C++17 command, and `critical_particles --self-test` passed.

The unchanged nine research paths were not rerun; the task permits retaining them, and no simulator issue warranted a new full ensemble. I did not reinterpret the three-seed ranges as confidence intervals. The prose explicitly says no continuum PDE was computed, reports the weak discrepancy certificate at time 10, retains the low-count seed, and avoids using observed log variance as proof of a second-moment limit.

I rendered all 55 pages, inspected pages 1–54 as contact sheets, and inspected the final bibliography page and the six-panel figure at larger resolution. Tables 1 and 2, Figure 1, equation numbers, proof endings, and references are present and legible. There are no cropped formulas, overflowing table entries, missing plots, or unresolved citation marks. The figure has readable panel labels and legends at manuscript width. Its count/half-moment references and mean-log band are clearly identified as continuum references, not sample-path bounds. The table's three-seed ranges agree with the verified saved summaries.

## Numbered actionable findings

There are **no MAJOR findings** and **no MINOR findings**. No mandatory correction is requested.

## Optional presentation preferences

1. `sections/introduction.tex:140` and Table 1: a compact diagram showing the deterministic number law feeding the auxiliary path and the independent sample model, with the finite vessel shown separately, could help readers less familiar with probabilistic representations. The current prose already makes the distinction adequately; this is optional.
2. `sections/finite-population.tex:215` and Figure 1: use distinct line styles for the three seeds if identifying an individual seed directly on the plot becomes important in a later revision. The existing color grouping and explicit three-seed caption are sufficient for the current descriptive claims.

**Final recommendation: accept. Counts: 44/44 formal statements checked; 0 MAJOR, 0 MINOR; 2 optional preferences.**
