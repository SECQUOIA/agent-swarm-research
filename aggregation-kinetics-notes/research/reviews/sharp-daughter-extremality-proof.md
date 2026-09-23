# Independent audit of sharp daughter-law extremality

Reviewer: `review_gauge`, 2026-09-07. Read the complete actual source [sharp-daughter-extremality.md](../results/sharp-daughter-extremality.md), including both benchmarks, the generator comparisons, positive-daughter sharpness, and the overlap coefficient. The communicated derivation had previously been checked; this records a separate actual-file audit.

**Verdict.** All displayed formulas and comparison directions are correct under the inherited weak-solution and auxiliary-process assumptions. Equal splitting attains the largest future-coagulation probability. Increasingly unequal positive splits approach its smallest possible value. The stated lower overlap coefficient is optimal. No logarithmic or second hazard moment is needed.

## 1. Scope of the conditional probability

With constant `b=mλ>0` and `σ≥0`, write `d=σ−b`. Starting at a deterministic time `t` and state `x`, normalized size is `q=N(t)x/m`. Before the next coagulation it evolves through deterministic drift `dq` and fragmentation at rate `2σ`, with conditional fraction mean one half.

For a claim at every `q>0`, the clean interpretation is to restart the already constructed Markov process from that state at time `t`, in its prescribed deterministic environment. This gives a transition probability defined for every positive state. A bare regular conditional probability given `X_t=x` is otherwise defined only almost everywhere with respect to its current marginal. The developing agent added this restarted-law definition explicitly, and I reread the resulting text; the qualification is resolved.

The time- and parent-dependent daughter kernel becomes a time- and state-dependent fraction kernel in the normalized coordinate. The conversion between physical and normalized size is deterministic, so its conditional mean remains one half. No self-similarity or continuity of that kernel is needed for the comparison.

## 2. Hazard representation

For the fragmentation-only future `Q_s`, started at `q`, the exact mean is

$$\mathbb E Q_s=qe^{-bs}.$$

Indeed, the deterministic drift contributes `dQ`, while fragmentation contributes `2σ(1/2−1)Q=−σQ`. On every finite horizon, `Q_s≤q exp(max{d,0}s)` pathwise, so the mean equation is legitimate without an extra moment assumption.

Its accumulated coagulation hazard is `H∞=∫₀∞bQ_s ds`. Tonelli gives `E H∞=q`, and therefore `H∞<∞` almost surely. Independent killing at this rate is precisely the first future auxiliary coagulation, giving survival `E exp(−H∞)`. The subsequent partner law is irrelevant to this first-event calculation.

## 3. Benchmark integrability and regularity

For `σ>0`, the extreme benchmark is

$$Z_{\rm ext}=b\int_0^T e^{ds}\,ds,\qquad T\sim\operatorname{Exp}(\sigma),$$

while the equal-split benchmark is

$$Z_{\rm eq}=b\int_0^\infty e^{ds}2^{-P_s}\,ds,
\qquad P_s\sim\operatorname{Poisson}(2\sigma s).$$

Both have mean one: `e^(ds)P(T>s)=e^(−bs)`, and `e^(ds)E2^(−P_s)=e^(−bs)`. They are positive and finite almost surely. At `σ=0`, both hazards equal one directly.

Their Laplace transforms `w(q)=E exp(−qZ)` are convex, decreasing, bounded between zero and one, and continuously differentiable up to zero from the right because `EZ=1`. In particular `|w'(q)|≤1` and `0≤1−w(q)≤q`. They are smooth for positive `q`.

A finite second hazard moment must not be inserted into the proof. For example, when `σ≥2b`, the extreme benchmark has infinite second moment. The actual source correctly avoids needing it. All derivative and generator arguments use only the finite first moment or positive `q`.

## 4. Independent verification of the benchmark equations

The extreme benchmark corresponds to normalized deterministic growth at rate `d`, killed at rate `bq`, with an absorbing reset to zero at rate `σ`. Its Laplace transform therefore satisfies

$$dq w'_{\rm ext}(q)+\sigma[1-w_{\rm ext}(q)]-bq w_{\rm ext}(q)=0.$$

This can also be checked directly from

$$w_{\rm ext}(q)=\int_0^\infty\sigma e^{-\sigma t}
\exp\left[-qb\int_0^t e^{ds}\,ds\right]dt.$$

Writing `h(t)=b∫₀ᵗe^(ds)ds`, the relation `dh(t)=b(e^(dt)−1)` converts the `dq w'−bq w` terms into a time derivative, and integration by parts gives `−σ+σw`. The boundary term at infinity vanishes. The equation is also valid directly at `σ=0`, where `d=−b` and `w=e^(−q)`.

The equal-split hazard obeys the first-event decomposition

$$Z_{\rm eq}\overset{d}=b\int_0^S e^{ds}ds+\tfrac12e^{dS}Z'_{\rm eq},
\qquad S\sim\operatorname{Exp}(2\sigma),$$

with an independent copy after the first fragmentation. First-step conditioning gives

$$dq w'_{\rm eq}(q)+2\sigma[w_{\rm eq}(q/2)-w_{\rm eq}(q)]-bq w_{\rm eq}(q)=0.$$

Thus the extreme clock has rate `σ`, whereas the equal-split clock has rate `2σ`. The actual source uses both rates correctly.

## 5. Generator signs and infinite-horizon passage

For every convex `w` with `w(0)=1` and every admissible conditional fraction law,

$$w(q/2)\le\mathbb E[w(q\Theta)]\le\tfrac12[1+w(q)].$$

The first inequality is Jensen. The second is the chord bound on `[0,q]`, followed by `EΘ=1/2`. Applying the upper bound to the extreme benchmark makes its actual killed generator nonpositive. Applying the lower bound to the equal benchmark makes its actual killed generator nonnegative.

Consequently `exp(−H_s)w_ext(Q_s)` is a supermartingale and `exp(−H_s)w_eq(Q_s)` is a submartingale. Their signs in the actual source are correct. Compensation is justified on finite horizons by the pathwise bound on `Q`, the finite fragmentation rate, and the bounded transform and its first derivative. This reasoning still applies to measurable time- and parent-dependent fraction kernels.

The terminal step is also correct even when normalized size is not monotone. Uniformly for either transform,

$$\mathbb E\left|e^{-H_s}w(Q_s)-e^{-H_s}\right|
\le\mathbb E Q_s=qe^{-bs}\longrightarrow0.$$

Meanwhile `exp(−H_s)` converges boundedly to `exp(−H∞)`. The resulting inequalities are

$$w_{\rm eq}(q)\le\mathbb E e^{-H_\infty}\le w_{\rm ext}(q).$$

Subtracting from one gives exactly the claimed sharp probability envelope. No monotonicity of `Q` or logarithmic moment is hidden in this passage.

## 6. Sharpness using strictly positive daughters

Equal splitting gives the equal-split hazard exactly, so it attains its bound.

For fractions `ε` and `1−ε`, the two fragmentation mark types arise from independent Poisson clocks of rate `σ`. Let `T` be the first `ε` event and let `R_s` count the other type. Before `T`, the integrated hazard is

$$bq\int_0^T e^{ds}(1-\varepsilon)^{R_s}\,ds.$$

Using common clocks for decreasing `ε`, this converges almost surely to `qZ_ext` and is dominated by that integrable variable. Thus convergence also holds in `L¹`.

After the first `ε` event, the normalized state is

$$Q_T=q\varepsilon e^{dT}(1-\varepsilon)^{R_T}.$$

The actual source's residual expectation checks exactly:

$$\mathbb E Q_T
=q\varepsilon\sigma\int_0^\infty e^{-(b+\sigma\varepsilon)s}ds
=\frac{q\varepsilon\sigma}{b+\sigma\varepsilon}\longrightarrow0.$$

By the conditional mean formula, the expected remaining hazard equals `E Q_T`. Hence the total hazard converges to `qZ_ext` in `L¹`, and its survival transform converges as claimed. The stopping time here is the first `ε` event, so conditioning after it is legitimate; this does not use the generally non-stopping last-coagulation time.

Each approximating daughter pair is strictly positive. The zero daughter appears only in the comparison representation and as a limiting infimum, never as an admissible actual daughter. At `σ=0`, all daughter choices are irrelevant and both envelopes reduce to the exact probability `1−e^(−q)`.

Sharpness at arbitrary prescribed `q` can be read through restarted conditional processes. If an actual initial population containing that normalized state is desired, a finite two-state preparation with mean normalized size one provides it whenever `q≠1`; the monodisperse preparation covers `q=1`.

## 7. Optimal sampling-overlap coefficient

The Radon–Nikodym derivative of mass sampling relative to number sampling is `Q`, and both are probability laws. Therefore, for total variation defined as the supremum over measurable sets,

$$O_t=1-\|\eta_t-\pi_t\|_{\rm TV}=\mathbb E\min(1,Q_t).$$

The function `f(q)=1−w_ext(q)` is increasing, concave, and zero at zero. Hence `f(q)≥f(1)q` on `[0,1]` and `f(q)≥f(1)` on `[1,∞)`. This proves

$$[1-w_{\rm ext}(1)]O_t\le\mathbb P(L>t)\le O_t.$$

The upper bound uses the previously verified conditional hazard bound `g_t(q)≤min(1,q)`. Positivity of the lower coefficient follows because `Z_ext>0` almost surely.

For optimality of the lower coefficient, start monodisperse, so `Q₀=1` and `O₀=1`. The positive `ε`-split family then approaches event probability `1−w_ext(1)`. Thus any strictly larger uniform coefficient fails. This is sharpness across initial preparations and daughter laws, not a claim about an asymptotic exponential rate.

At `σ=0`, the coefficient is `1−e^(−1)`. At `σ=b`, the extreme hazard is exponential with mean one and `w_ext(q)=1/(1+q)`, giving coefficient one half. For critical equal splitting, the successive holding times have rate `2b`, and the normalized state is `q/2^j`. Multiplying their Laplace factors gives

$$w_{\rm eq}(q)=\prod_{k=1}^\infty(1+q/2^k)^{-1}.$$

The indexing, convergence, and normalization of this product are correct.

## 8. Scope and final assessment

The theorem compares the event of a future first auxiliary coagulation; it does not order the total number of subsequent coagulations or physical tagged-particle histories. Time and parent dependence of the daughter rule is permitted because the generator inequalities hold conditionally at every state and time. Constant `b` and `σ` are used in defining these stationary benchmark transforms.

The comparison remains conditional on the existence of the given weak solution and the previously audited auxiliary representation. The positive self-similar sharpness examples fit the more regular solution class discussed elsewhere in the repository. This audit does not supply a new existence theorem or prove publication priority.

No formula correction was required after reading the actual source. The conditioning-state clarification has been incorporated explicitly into the theorem and checked. The final source also directly attributes its critical equal-split product and geometric exponential sum to Bertoin, Biane, and Yor, equations (1.3) and (1.6), and links the specialized critical note; this is consistent with treating the benchmark as classical. The present proof review independently checks the product's normalization and mathematics, rather than certifying the literature priority of every cited formula. A focused literature audit remains necessary to assess novelty of this specific extremal comparison.
