# Stage 1, round 1, independent review 1

**Verdict: no major issues.** The weak-support theorem, arbitrary-tuning necessity, unequal-spacing necessity, and both sufficient criteria are correct under their stated hypotheses. I found two minor local wording issues.

## Scope and independence

I read `reviews/README.md` and independently reviewed the frozen `main.tex`, `sections/framework.tex`, and `sections/thresholds.tex`. I did not read other round reports, edit the manuscript, or delegate. Missing sections reserved for later stages are not counted as defects. This review establishes mathematical consistency of this stage; it does not establish literature priority. No external source or numerical check was necessary for the elementary identities and estimates reviewed here.

## Issues

1. **Minor — specify the cutoff value explicitly in the secant notation.** In `sections/framework.tex`, immediately after the definition of the secant residual log-weight (line 170), “set ... zero above the cutoff” should read “at and above the cutoff.” The original exact likelihood correctly vanishes when the energy equals the cutoff, and the later positive-decomposition proof uses the correct convention. The requested change merely makes the intervening definition complete for discrete laws that can assign positive probability to the cutoff.

2. **Minor — identify the interval in the interpolation argument.** In `sections/framework.tex`, the proof of the two-center bounds (line 222) says the convex difference “vanishes at both endpoints, hence is nonpositive there.” Replace the last words by “hence is nonpositive throughout the interval.” The calculation is correct: if the parabolic majorant is `p`, then `(h-p)'' = h'' + C/c >= 0`; convexity and the two zero endpoint values give the desired interior upper bound. The current “there” points ambiguously to the endpoints, where the difference is exactly zero.

## Independent mathematical checks

- **Exact marginal and full-state distance:** integrating the bath density produces an energy-only likelihood. Its boundedness on the full feasible half-line follows from exponential decay at negative infinity and the positive power at the upper cutoff. Consequently the normalization is finite, with positivity precisely as stated. The full-state and energy-law total variations agree by their identical Radon–Nikodym derivatives; no disintegration or density assumption is hidden here.

- **Center calibration and rare tails:** the identity `log W = beta(e-a) + c log(1-beta(e-a)/c)` gives `W <= 1` on the entire real line after the cutoff convention. If `E-a = O_P(b)` and `c >> b^2`, the quadratic logarithmic remainder vanishes in probability, and boundedness supplies the required mean convergence. No moment assumption is being smuggled into this argument.

- **Chord identity and uniform inequality:** substituting `u_j = total_energy-e_j` gives `u_2 = (1-theta)u_1 + theta u_3` and exactly the displayed chord function. Its second derivative is positive and is at least `theta(1-theta)/e` on `[0,1]`; double integration gives the quadratic bound. Convexity makes `f(q)/q` nondecreasing, giving the linear bound for `q >= 1`. The coefficient remains valid when the middle point approaches an endpoint, which is essential to the unequal-scale theorem.

- **Arbitrary-tuning necessity:** total variation produces a single likelihood-good set whose probability tends to one. Each of three separated neighborhoods with positive limiting lower probability intersects that set. Selected energies are necessarily strictly below the bath cutoff, even if the original law is discrete, mixed, or supported on unbounded energies. The normalization constant cancels from both endpoint differences and the chord. The identities `cq = beta D + o(1)` and `c f_theta(q) = o(1)` first force `q -> 0`, then `cq^2 -> 0`, and finally `D^2/c -> 0`. None of these steps assumes the tuning is centered or secant calibrated.

- **Unequal-spacing necessity:** positivity of the mixture and phase weights bounded away from zero transfer the same good-set property to each phase. The two within-phase points have separation comparable to `s`, while their distance from a point in the other phase is comparable to `Delta`. Thus `theta(1-theta)` is comparable to `s/Delta`. Using `q` comparable to `Delta/c`, the lower chord defect is comparable to `min(Delta s/c, s)`. Since the defect tends to zero and `s` diverges, `c >> Delta s` follows. The upper-phase variant is valid because the chord bound is uniform in both endpoint spacings. No exceptional-mass decay is needed for this necessary statement.

- **Two-atom exception:** equal unnormalized likelihoods at the two energies make the normalized likelihood identically one, independently of their probabilities and state-space degeneracies. This is correctly distinguished from a two-atom scaling limit with unresolved fluctuations.

- **Positive-decomposition sufficiency:** the secant tangent estimate and the uniform phase exponential moment give a bounded second moment of each phase weight, so convergence in phase probability does imply convergence in phase mean. The exceptional component is controlled separately by its positive mass times the global amplification bound. The exponential exceptional-mass corollary uses `Delta^2/c = o(Delta/s)`, correctly matching the necessary mixed scale. The manuscript correctly refrains from replacing a positive exceptional measure with a signed partition-function remainder.

- **Interior-density sufficiency:** the curvature majorant produces local flatness and an interior gain bounded by `C kappa N x`. Relative to the Gaussian and interfacial costs this is at most `C lambda/R` and `C lambda N^(1/2-alpha)`, respectively, where `lambda = kappa N^(3/2)`. Both vanish for the stated `alpha >= 1/2`. The weighted interior tail is integrable after separating the two exponential costs. Concavity prevents exterior amplification. Local density convergence with total limiting phase weight one supplies the unweighted tightness needed to remove both exterior tails.

- **Necessity in the density corollary:** splitting at the midpoint yields genuinely positive conditional measures. The two local Gaussian masses exhaust total probability as the window radius increases; this establishes their weights and conditional weak limits without additional tail hypotheses. Applying the earlier unequal-scale result is legitimate.

## Presentation assessment

The stage has a clear progression from the physical marginal and two calibrations to the weak-support obstruction, the unequal-scale refinement, and the distinct extra hypotheses needed for sufficiency. The distinction between the bath surface exponent and canonical heat capacity is accurate. The abstract states results conditionally rather than asserting that local Gaussian behavior alone gives the coexistence threshold. Beyond the two wording corrections above, I found no required readability or consistency correction in this frozen stage.
