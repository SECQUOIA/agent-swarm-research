# Stage 3 independent review: measure and probability arguments

I reviewed all of `sections/last-event.tex`, `sections/daughter-comparison.tex`, `sections/critical-last-event.tex`, `appendices/product.tex`, and the supplement script and JSON, together with their use of the accepted solution framework and auxiliary process. I also checked the Stage 3 coverage entries, author report, relevant source developments, and the newly cited primary sources. I did not consult another current Stage 3 report, communicate with reviewers, edit the manuscript, or compile it. All source hashes still match the frozen Stage 3 snapshot.

**Findings: no actionable mathematical, scientific, or expository defect identified. Major issues: 0. Minor issues: 0.**

## First-event construction and entire future paths

**Locations:** `last-event.tex`, Theorem `thm:last-controlled`, lines 22–96; Corollary `cor:future-path-TV`, lines 115–140.

The fragmentation-only process is bounded by its initial raw size on every future interval. Consequently its conditional mean equation follows from bounded-process compensation even for merely measurable parent- and time-dependent daughters. The exact normalization by the count curve gives the factor involving only cumulative coagulation activity. Tonelli then gives the finite expected first-event hazard \(q u_{t,T}\), including an infinite horizon. The independent exponential threshold identifies the first future coagulation because the full and fragmentation-only processes agree before that event. The proof correctly distinguishes this first-event hazard from the full process's later compensator.

The Jensen bound has the correct direction, and the fractional-moment estimate applies to \(Q_t\) with no additional size or logarithmic moments. The two cases of finite and infinite total coagulation activity prove that the last-event tail tends to zero. Together with finite-horizon nonexplosion, this gives a finite total coagulation count without using the earlier product-martingale proof. The no-fragmentation equality case and the strictly smaller optimal scalar domination factor are valid.

The future-path result constructs both processes on one probability space for the whole future. Each process evaluates the daughter map at its own state after divergence, so both marginals remain correct for arbitrary measurable parent dependence. Equality of paths until the first coagulation gives the total variation bound on the specified Borel path space. The same coupling proves the infinite-horizon assertion; the reference starts from the actual law at the observation time, as stated.

The exponential-moment formula and all rare-window count inequalities follow from the tail estimate and the exact mean count. Their moment assumptions and allowance for infinite higher moments are correct. The pure-coagulation Borel calculation gives

\[
-\log(1-h)=\delta+(1-\delta)h,
\]

and hence \(h\sim\sqrt{2\delta}\). Its distinction from the robust moment exponent is accurate.

## Measurable daughter-law comparison and sharpness

**Locations:** `daughter-comparison.tex`, Theorem `thm:daughter-envelopes`, lines 29–150; overlap and critical corollaries, lines 160–274.

The normalized fragmentation-only process can grow between events when \(\sigma>b\), but the proof does not assume monotonicity. Its first moment decays as \(qe^{-bs}\). Both benchmark hazards have expectation one, giving the asserted continuously differentiable transforms and derivative bound using only a first hazard moment. The short-time benchmark equations require only this regularity and bounded states on a finite horizon, so no unmentioned second hazard moment enters.

The conditional Jensen and chord inequalities use only \(\mathbb E\Theta=1/2\). They yield the stated supermartingale and submartingale directions. Finite-horizon drift integrability follows from the deterministic state bound. At infinite time, the estimate

\[
\mathbb E\left|e^{-H_s}w(Y_s)-e^{-H_s}\right|\le qe^{-bs}
\]

supplies the needed convergence without extra regularity of the competing daughter kernel. Thus the comparison remains valid for measurable time and parent dependence.

The positive \(\varepsilon\)-daughter construction gives the claimed sharp infimum. Its pre-reset hazard converges in \(L^1\) by domination, and the expected residual hazard is exactly \(q\varepsilon\sigma/(b+\sigma\varepsilon)\), which vanishes. No zero daughter is admitted as a model law. Equal splitting attains the opposite envelope, and the zero-fragmentation case reduces correctly to deterministic hazard one.

The all-rate overlap coefficient follows from the chord of the increasing concave event-probability function. The critical constants, equal-split constant, and upper constant one have valid mean-one sharpness preparations. The manuscript explicitly realizes those finite-support laws as finite-second-moment initial population measures, so the sharpness examples lie within the accepted existence theorem.

## Last-event projection, density, and differentiability

**Locations:** `critical-last-event.tex`, Theorems `thm:exact-last-density` and `thm:general-last-density`, lines 18–179.

For equal splitting, the product recurrence cancels the direct coagulation loss. The remaining pair integrand \(q\Psi(q+v)\) is bounded by one. Total variation continuity of the normalized population therefore gives a continuous expectation and a continuous density, with the stated right derivative at zero. The proof needs no second size moment. The zero atom and the continuous part exhaust the last-event law because the last time is finite almost surely.

The Laplace equation has the correct sign and normalization. For positive Laplace argument the relevant observables are bounded; at argument zero the finite first moment gives the right size derivative, and both sides of the time equation are zero. The independent exponential-sum mixture is justified by Tonelli.

For general measurable daughters, the restarted survival function is measurable in time and state through the clock construction and an infinite-horizon limit. Conditioning occurs at each actual coagulation stopping time, using the post-event state. Fresh Poisson increments justify the restarted survival probability there. After projecting the future “no successor” mark, the resulting function of deterministic time, pre-event state, and fresh partner is eligible for compensation. The finite expected event count on bounded intervals justifies the summation. This proves an integrated density formula and an almost-everywhere derivative without assuming time differentiability of the daughter kernel. The manuscript correctly reserves the stronger continuity assertion for equal splitting.

The rational envelopes give \(j(t)\le bh(t)\), and absolute continuity yields the lower calendar-time tail. The instantaneous sharpness family has \(h(0)\sim\varepsilon\) and normalized density asymptotic to \(\varepsilon\), verifying the claimed optimal coefficient. The positive lower initial tail also proves divergence of the exponential moment at the endpoint \(r=b\).

## Scalar obstruction, product asymptotics, and supplement

**Locations:** `critical-last-event.tex`, Proposition `prop:scalar-obstruction`, lines 213–273; `appendices/product.tex`, both propositions.

The two-point obstruction has positive sizes, mean one, and finite moments of every positive order for each member of the family. Its event probability is asymptotic to \(\varepsilon\), while its normalized density is bounded by \(\delta_\varepsilon+\Psi(R_\varepsilon)\). The finite-product bound gives decay faster than any fixed required power. The exact derivative and its continuity transfer the strict violation at zero to a positive interval. The conclusion excludes precisely the advertised uniform power-law dissipation estimates.

The exponential-sum scaling, product recurrence, first three Taylor coefficients, and variance are correct. I independently checked the product split producing the periodic correction, including the case \(n=0\), the matching endpoint values, and the quadratic/cubic remainder constants. The finite-product rational bound is also correct.

I ran the supplement from a private temporary copy, leaving the frozen files untouched. Its generated JSON matched the supplied JSON byte for byte. I separately executed the exact `Fraction` endpoint assertions in the appendix; both strict 30-decimal bounds passed. The script's directed decimal rounding preserves the rational enclosures. Its floating-point examples are clearly distinguished from the certificate and are not used as proof of the asymptotics or obstruction.

The underlying exponential sum and product match [Bertoin–Biane–Yor, equations (1.3), (1.6), and Theorem 1.1(i)](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf), with the stated factor of one half. The [Rüschendorf–Schnurr–Wolf reference](https://arxiv.org/abs/1505.02925) supplies relevant methodological context; the manuscript proves its own particular comparison directly. The distinction between conditional-size product asymptotics and an unresolved calendar-time exponent is maintained throughout.

Every Stage 3 coverage item is present, with the required conditional probabilities, path-law comparison, general daughter envelopes, overlap constants, density identities, lower tail, scalar obstruction, and certified product calculation. The new claims use the accepted Stage 1–2 hypotheses consistently. Unwritten later-stage results are outside this review.

**Final major issue count: 0. Final minor issue count: 0. Recommendation: accept Stage 3.**
