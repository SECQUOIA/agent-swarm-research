# Results and verification record

Developed 2026-09-06–07. This report consolidates the current investigations at the user's request. It separates proved statements, literature precedents, numerical evidence, and unresolved questions. Independent proof reviews accompany the substantive results. A search that finds no matching theorem does not establish publication priority.

**Completed manuscript update, 2026-09-07.** The [55-page additive coagulation–fragmentation paper](../paper-additive-coagulation/README.md) develops and consolidates this package. All five writing stages passed five independent reviews each, with every valid issue corrected. Five fresh whole-manuscript reviewers then recommended acceptance with zero major and zero minor findings. The paper proves measurable-parent existence and uniqueness in the locally bounded second-moment class and justifies the sharp entropy-production coefficient `lambda m^2 log 2`. Its [final report](../paper-additive-coagulation/development/FINAL-REPORT.md) records the advances, corrections, and verification.

The strongest coherent research package concerns **additive coagulation–fragmentation: separation of sampling laws, quantitative decay of nonlinear effects on number-weighted trajectories, and inverse identification**. This connects directly to Ramkrishna's population-balance and inverse-problem interests. It is more developed and has a stronger prospective application than the early coarse-graining or extinction investigations. Citation impact cannot be established in advance.

## 1. The main model and a uniform inequality

Coagulation has kernel K_t(x,y)=λ(t)(x+y), fragmentation selection is σ(t), and the expected positive daughter measure has count two and conserved parent mass. The controls are deterministic, nonnegative, and locally integrable. Let n_t be a global mass-conserving weak solution with finite initial count N_0 and positive mass m. Define

\[
 b(t)=m\lambda(t),\quad B_c(t)=\int_0^t b(s)ds,\quad
 F(t)=\int_0^t\sigma(s)ds,
 \quad N(t)=N_0e^{F(t)-B_c(t)}.
\]

The number and mass sampling laws are η_t=n_t/N(t) and π_t=xn_t/m. For 0<p<1,

\[
 \mathcal A_p(t)=\frac{\int x^p n_t(dx)}{N(t)^{1-p}m^p},
 \qquad a_p=1+p-2^p>0.
\]

The central estimate is

\[
 \boxed{\mathcal A_p(t)\le\mathcal A_p(0)
 e^{-a_pB_c(t)-a_{1-p}F(t)}.}
\]

It holds even for measurable parent- and time-dependent daughter laws. Its instantaneous coefficients are sharp uniformly over the allowed initial data and daughters. That does not make every resulting long-time exponent sharp.

At constant critical rates σ=b=λm>0, count stays fixed and every positive fractional moment decays. Almost all particles move toward size zero while almost all material mass moves beyond every bounded size interval. There is no finite-count, positive-finite-mass stationary measure. This is a long-time result, not finite-time mass loss.

Sources: [fractional-moment theorem](results/invisible-kinetics-extension.md), [controlled extension](results/controlled-additive-trajectories.md), and their linked independent reviews.

## 2. Finite nonlinear correction and quantitative last coagulation

There is an auxiliary Markov process with one-time law η_t. It fragments at rate 2σ(t) and coagulates at rate λ(t)N(t)X_t. It is a representation of number sampling, **not a physical tagged unit of material**.

The sum A_t of its upward logarithmic size increments converges almost surely and in L¹ to a finite limit. The auxiliary path has only finitely many coagulations almost surely, although the expected total count is B_c(∞) and may be infinite. The first-event argument gives an explicit tail: if L is the last coagulation time,

\[
 \mathbb P(L>t)\le
 \left(1-e^{-\int_t^\infty b(s)ds}\right)^p
 \mathcal A_p(0)e^{-a_pB_c(t)-a_{1-p}F(t)}.
\]

The same bound controls the total variation distance between entire future auxiliary paths and fragmentation-only paths started from the actual current distribution. It also quantifies how rare paths carry large event counts in fixed future windows.

For constant rates with b>0 and selfsimilar parent-independent daughters, the log process differs from a compound-Poisson fragmentation process by a finite integrable increasing correction. This yields a uniform finite transport cost without logarithmic moments. When daughter log-size increments have finite second moment, it transfers the usual log-size central limit theorem, with limiting Gaussian variance 2σE[(log Θ)²]. This uses the raw second moment of the jump; convergence of the actual variances is not asserted.

Sources: [arbitrary constant-rate coupling](results/general-additive-log-coupling.md), [pathwise construction](results/pathwise-additive-log-coupling.md), [controlled theorem](results/controlled-additive-trajectories.md), and [quantitative last-event theorem](results/last-coagulation-tail.md).

## 3. Sharp daughter-law comparisons and sampling overlap

At fixed constant rates with b>0 and σ≥0, equal splitting maximizes the conditional probability of a future auxiliary coagulation. Positive splits tending to fractions zero and one approach its minimum. These bounds remain valid for the daughter rule being compared when it depends on parent size and time.

At criticality, for normalized size q=Nx/m, the sharp conditional bounds are

\[
 \frac q{1+q}\le
 \mathbb P(\text{future coagulation}\mid q)
 \le1-\prod_{k=1}^\infty(1+q/2^k)^{-1}.
\]

Thus, using total variation as the supremum over measurable sets,

\[
 \tfrac12(1-\|\eta_t-\pi_t\|_{\rm TV})
 \le\mathbb P(L>t)
 \le1-\|\eta_t-\pi_t\|_{\rm TV}.
\]

The lower constant one half is optimal over the full daughter class. For equal splitting it improves to the optimal constant

\[
 0.580577558204892402290043892297
 <c_*<
 0.580577558204892402290043892298,
\]

certified by rational product bounds. The infinite-product distribution itself is classical and is explicitly attributed to Bertoin, Biane, and Yor.

The exact last-event density provides a lower bound P(L>t)≥P(L>0)e^(−bt) at criticality. Combined with the upper bound, it brackets the possible tail decay but does not determine its exact exponent. Explicit positive two-point populations rule out every universal scalar dissipation inequality of the form −h′≥c h^α with c,α>0 and h=P(L>t).

Sources: [sharp daughter-law theorem](results/sharp-daughter-extremality.md), [exact critical observable and counterexamples](results/last-coagulation-exact-equal-split.md), and [rational verification](verification/last_coagulation_exact.json).

## 4. Identification despite persistent coagulation

For constant rates with λ>0 and σ≥0 and parent-independent daughter measure B, let

\[
 \phi_t(k)=\int e^{ik\log x}\eta_t(dx),\qquad
 \psi(k)=\sigma\int(\theta^{ik}-1)B(d\theta).
\]

On a nonempty interval of frequencies around zero, there is a continuous nonvanishing amplitude C such that

\[
 \phi_t(k)=e^{t\psi(k)}C(k)+O(e^{-\omega t}),
 \qquad\omega=(3-2\sqrt2)(b+\sigma).
\]

The error has an explicit bound. Consequently, for each fixed lag h>0,

\[
 \frac{\phi_{t+h}(k)}{\phi_t(k)}\longrightarrow e^{h\psi(k)}
\]

at an explicit exponential rate. A logarithm anchored at zero recovers ψ locally. One-sided transform uniqueness then identifies the whole expected daughter measure and σ from ideal exact late-time traces. Observed count growth and conserved mass additionally identify λ. If σ=0, the unused daughter law is unidentifiable.

Fourier quotients and cancellation of an unknown factor are established methods, including a direct decompounding precedent. The candidate contribution is the proved nonlinear coagulation error and the resulting asymptotic factorization under weak moment assumptions. Exact identifiability does not make analytic continuation stable.

An accompanying independent-sampling calculation gives a finite-time error certificate for one empirical Fourier ratio and a sufficient logarithmic observation-time schedule. It assumes independent draws from continuum distributions, not dependent particles in one finite vessel, and does not establish full daughter-law reconstruction under noise.

Sources: [identification theorem](results/fourier-identification.md), [sampling certificate](results/fourier-sampling-tradeoff.md), and [comparison with primary inverse-problem literature](reviews/fourier-identification-literature.md).

## 5. Finite-population and broader-kernel results

For a finite critical additive system with b>0, total mass nm, and O(n) initial particles, normalized count tracks its constant continuum prediction uniformly on every o(n) time horizon. Yet, for every C>1/(b log 2), the finite and continuum mass-size cumulative distributions differ by an amount tending to one at time C log n. Both start from exactly the same empirical measure. This proves a separation between validity of count predictions and mass-distribution predictions; it is not merely an initial approximation error.

Nine independently reviewed particle simulations processed approximately 6.59 million events and illustrate number–mass separation. They do not independently establish the continuum discrepancy, because no deterministic-solution comparison was computed. Sources: [finite-population theorem](results/finite-population-breakdown.md) and [reproducible experiment](results/critical-additive-particle-experiment.md).

Beyond the additive case, for K(x,y)=xy^α+yx^α with 0<α≤1 and binary fragmentation selection σx^α, no stationary measure has both finite count and positive finite mass. A jump-rate-weighted inverse-power test proves this without negative moments of the population. Counterexamples show that the additive model's positive fractional-moment monotonicity does not extend across this range. Known critical multiplicative equilibria have infinite count and are explicitly distinguished. Source: [power-kernel result and boundary examples](results/count-neutral-power-kernels.md).

## 6. Proof status, prior art, and limits

The substantive mathematical developments have independent subagent proof reviews, followed by staged and whole-manuscript reviews of the completed paper. The paper supplies global mass-conserving existence for measurable parent- and time-dependent expected daughters with finite initial second moment, and uniqueness in the locally bounded second-moment class. These arguments use established methods and are not claimed as new general existence theory. The later conditional finite-count, finite-mass estimates can apply outside this sufficient construction class when a solution is separately supplied.

Primary-source audits found close precedents for tagged processes, change of weighting, pure-fragmentation limits, exponential functionals, inverse transforms, logarithmic finite-size effects, and stationary infinite-count populations. These are attributed. No inspected source matched the complete nonlinear coupling, last-event, sharp daughter-law, or asymptotic-factorization package. This is bounded-search evidence, not a settled priority claim or peer-reviewed publication decision.

The exact long-time last-event exponent and stable full nonparametric inversion remain outside the established results. General-parent existence and nonlinear uniqueness, formerly open in this report, were resolved during manuscript development under the stated second-moment hypotheses. No existence or uniqueness claim is made for a wider first-moment-only class. These boundaries are recorded explicitly; no theorem depends on solving them. No further research direction was started after completion of the requested manuscript.

Earlier work is also preserved: [coarse-graining results and a failed novelty claim](ideas/coarse-graining.md), [inverse preparation and hidden kinetics](ideas/inverse-design.md), [extinction bounds](results/extinction-coupling.md), [uniform near-critical corrections](results/extinction-near-critical.md), and [Perron-value tie breaking](results/extinction-perron-ties.md). A semigroup literature match substantially downgraded the coarse-graining dimension theorem; that correction is part of the record.
