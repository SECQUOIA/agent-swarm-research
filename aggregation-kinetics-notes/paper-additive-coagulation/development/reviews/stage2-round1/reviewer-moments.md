# Independent Stage 2 review: moments, transport, and logarithmic limits

**Recommendation: accept Stage 2. MAJOR issues: 0. MINOR issues: 0. The reviewed mathematics is clean.**

I independently reviewed all of `sections/auxiliary-process.tex` and `sections/log-limits.tex`, their use of the accepted Stage 1 model and estimates, and the relevant bibliography. I did not read other current Stage 2 reports, communicate with other reviewers, edit the manuscript, or run a shared build. Material assigned to later stages is outside this review's defect list.

## Construction and marginal identification

The number-normalization calculation gives the stated generator. In particular, its fragmentation rate is `2 sigma`, its daughter law is `b_{t,x}/2`, and its coagulation rate is `lambda N x`; there is no extra additive `b` in this last rate. The cancellation using the count equation is correct.

The nonexplosion proof works under the stated finite first moment, without a second moment. Before the size and jump stops, the upward mark has finite conditional mean. The stopped drift estimate uses `L_t x = (b-sigma)x <= bx`. Nonnegativity permits replacing the active stopped-state expectation by the full stopped expectation in Gronwall's inequality. Fatou removes the size stop, and the resulting bound controls the expected stopped jump count. All deterministic coefficients in `L_T` are locally integrable.

The prescribed probability curve has integrated jump flux `2 sigma+b`. Its survival formula retains the full incoming gain when the output coordinate is restricted. Positive iteration then yields domination of every finite-jump contribution, and nonexplosion plus total probability one establishes equality of the marginals. This avoids an unsupported uniqueness assumption for an unbounded forward operator. The accepted Stage 1 loss identity now explicitly has the local integrable loss-rate bound required here.

The inverse-size identity for the mass-tag generator is algebraically correct. The text appropriately distinguishes that identity from the independently constructed number-process path law.

## Finite correction, martingale, and controlled clocks

The elementary bound `log(1+r) <= sqrt(r)` gives exactly

`a(t) <= lambda(t) H(t)^2/N(t) <= [H(0)^2/(m N_0)] b(t) exp(-kappa C(t))`.

The compensator calculation and monotone convergence justify the expected correction, its integrable limit, and the tail bound. Integrating against `C'=b+sigma` produces the stated factor `1/kappa`. The text also correctly retains the sharper integral tail when total activity is finite, since the final exponential bound alone would then not establish convergence of the tail to zero.

For general parent-dependent daughters, the retained fraction has conditional mean one half. Therefore `exp(F(t)) product Theta_j` has zero predictable drift in the full filtration. Its deterministic bound on every finite horizon makes the local martingale a true mean-one martingale there. Doob's inequality yields an almost surely finite supremum over the entire half-line; no uniform integrability at infinite time is being assumed.

Combining this product with the count identity gives the factor `exp(-Bc(t))` in `N(t)X_t`. The pathwise cumulative coagulation intensity is consequently finite because `integral b exp(-Bc) = 1-exp(-Bc(infinity)) <= 1`. Stopping at compensator levels then proves a finite total number of coagulations almost surely. The separate expectation identity `E K_t = Bc(t)` is correct and is compatible with an infinite mean of the finite terminal count. The text does not incorrectly take expectations of the pathwise random bound.

Both branches of the controlled fragmentation dichotomy follow: diverging fragmentation activity sends the size to zero, while finite fragmentation activity and finite total coagulations leave an eventually constant positive finite state.

## Transport and exact constants

The independent marked-Poisson reference is valid for a selfsimilar daughter kernel, including a measurable time-dependent fraction law. The manuscript correctly declines to use it for general parent-dependent marks.

The ordered coupling has displacement `A_t`. The clipped-test argument proves optimality for the extended cost without requiring either marginal to have a finite first log moment: the clipped difference is nonnegative and increases to the displacement. No undefined subtraction of infinite means occurs.

The signed remainder has total mass zero and variation at most `2b`; its increasing-test sign and Lipschitz estimate follow from the paired upward increments. The manuscript correctly distinguishes these estimates from absolute logarithmic moments of its separate positive components.

The constant-rate decay parameter is `omega=kappa(b+sigma)`, and its integrated constant is `D_0=lambda H(0)^2/[kappa(b+sigma)N_0]`. At criticality this becomes `omega=2 kappa b` and `D_0=H(0)^2/(2 kappa m N_0)`. The factors of two, mass, count, and time are consistent with Stage 1. The growing accumulated transport cost and decreasing remaining correction are not confused.

## LLN, functional CLT, and ordinary Wasserstein conclusions

The path LLN requires only an integrable daughter log jump. A finite initial log value and an almost surely finite correction suffice; an initial log moment is unnecessary.

The functional CLT uses the correct compound-Poisson variance `r E Y^2`, rather than `r Var(Y)`. The unit-interval increments have this variance. The finite-second-moment maximal estimate for the within-interval total jump variation justifies replacing interpolation by the actual compound-Poisson path. The correction and initial value vanish uniformly after division by `sqrt(T)`, so the `J_1` transfer is valid, including at time zero.

For ordinary one-time Wasserstein convergence, the additional initial first log moment is correctly imposed. Uniform bounded second moments of the centered reference give uniform integrability of its first absolute moments, and adding the initial value and correction costs at most their expected absolute sizes divided by the scaling. The displayed speed bound has the correct square-root term. The separate truncated-jump proof gives convergence to the speed with only first jump and initial moments, without asserting the square-root rate in that setting.

The infinite-negative-log-moment conclusion and the universal upper speed `-2 sigma log 2` follow by bounded truncation and Jensen. The deterministic complementary-fraction and equal-split examples have the correct speeds and raw-second-moment variance parameters. The general diverging-scale proposition transfers only reference limits that have actually been established and does not assert an unjustified stable domain of attraction.

## Mean logs, entropy, and the pure-coagulation endpoint

The mean-log identity, geometric-mean prefactor, and exponential prefactor error follow under exactly the stated integrability assumptions. The relative entropy has the correct orientation and density ratio `m/(N(t)x)`. Its slope is `b-sigma-r E Y`, which becomes `-2b E Y` at criticality. No mass-weighted logarithmic moment is needed. The manuscript's distinction between this sampling-weight identity and a new entropy-production estimate is appropriate.

At the pure-coagulation endpoint, finite total auxiliary jumps imply an eventually constant path and a proper limiting size law. The ordered-coupling proof supplies both extended transport identities even when the initial first log moment is infinite.

The displayed monodisperse solution agrees with equation (3) of [Bertoin (2009)](https://www.numdam.org/article/AIHPC_2009__26_6_2073_0.pdf), including the additive-kernel time normalization. The limiting Borel probabilities, their normalization by critical Galton–Watson extinction, their `k^(-3/2)` tail, infinite arithmetic mean, and finite first log moment are all correct. The attribution to classical additive-coagulation work is appropriate.

The contextual fragmentation citations also use the correct sampling distinction: [Bertoin (2003), Section 2.2](https://ems.press/content/serial-article-files/31511?nt=1) uses mass-weighted log sizes, and [Doumic–Escobedo, Corollary 1](https://arxiv.org/html/1510.03588) gives the corresponding mass-weighted Gaussian limit. Neither is presented as a substitute for the manuscript's number-weighted compound-Poisson argument.

No corrective manuscript change is requested by this review.
