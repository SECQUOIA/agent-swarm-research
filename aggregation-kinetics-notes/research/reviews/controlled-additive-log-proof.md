# Independent review of controlled additive kinetics

Reviewer: `review_gauge`, 2026-09-07. Initially reviewed the communicated controlled-coefficient derivation. Subsequently read the complete actual source [controlled-additive-trajectories.md](../results/controlled-additive-trajectories.md), and reread the refined output-localization proof in the [pathwise theorem](../results/pathwise-additive-log-coupling.md). This is now an actual-file audit. It extends the [general-rate review](general-additive-log-proof.md) and [pathwise audit](pathwise-additive-log-proof.md).

**Verdict.** The deterministic-control extension, product-martingale argument, finite expected accumulated log displacement, and almost-sure finite total coagulation count are correct. The last assertion requires no daughter logarithmic moment. The same affinity and last-event conclusions remain valid for measurable parent-size-dependent daughter fractions with conditional mean one half, although an independent fragmentation reference then need not exist.

## 1. Setting and notation

Assume a specified global mass-conserving weak population-balance solution on positive finite sizes, with initial finite positive count `N₀` and mass `m`. The weak formulation includes the bounded continuous tests and integrated balances used in the preceding notes. Let

$$K_t(x,y)=\lambda(t)(x+y),\qquad S_t(x)=\sigma(t),$$

where the deterministic controls `λ,σ≥0` are locally integrable. Set

$$b(t)=m\lambda(t),\qquad
\mathsf B(t)=\int_0^t b(s)\,ds,\qquad
F(t)=\int_0^t\sigma(s)\,ds.$$

The cumulative symbol `mathsf B` here distinguishes the coagulation control from a daughter measure. Initially suppose the daughter-fraction measure `D_t` is a measurable time-dependent kernel on `(0,1)`, with total measure two and first fraction moment one. Equivalently a number-selected fraction `Θ_t~D_t/2` has mean one half. Section 7 removes the parent-independence assumption for the conclusions that do not need an independent reference.

## 2. Count, affinity, and accumulated log displacement

The count identity is

$$N(t)=N_0\exp(F(t)-\mathsf B(t)).$$

It is positive and bounded above and below away from zero on every finite interval. The same sharp fractional-moment argument, now integrated against locally integrable coefficients, gives

$$\frac{H(t)^2}{N(t)}
\le\frac{H_0^2}{N_0}
\exp[-\kappa(\mathsf B(t)+F(t))],\qquad\kappa=3-2\sqrt2.$$

More generally, the fractional affinity has the bound

$$\mathcal A_p(t)\le\mathcal A_p(0)
\exp[-a_p\mathsf B(t)-a_{1-p}F(t)],\qquad a_p=1+p-2^p.$$

These follow from differential inequalities almost everywhere and absolutely continuous integrating factors; no boundedness of the instantaneous controls is needed.

For the normalized law `η_t=n_t/N(t)`, the upward log-displacement rate is

$$a(t)=\frac{\lambda(t)}{N(t)}\iint x\log(1+y/x)\,dn_t(x)dn_t(y).$$

It obeys

$$a(t)\le\frac{H_0^2}{mN_0}\,b(t)
e^{-\kappa(\mathsf B(t)+F(t))}.$$

Consequently

$$\int_0^\infty a(t)\,dt
\le\frac{H_0^2}{mN_0}
\int_0^\infty b(t)e^{-\kappa(\mathsf B(t)+F(t))}\,dt
\le\frac{H_0^2}{\kappa mN_0}.$$

The last step uses nonnegativity of `F` and the absolutely continuous substitution `d mathsf B=b(t)dt`. It remains valid when either cumulative control has a finite limit, when both diverge, or when one control vanishes identically.

## 3. Auxiliary process and local nonexplosion

In the prescribed background, use fragmentation events at time-dependent rate `2σ(t)`, multiplying the state by a fraction drawn from `D_t/2`, and coagulation events at rate `λ(t)N(t)X`, adding an independent mark drawn from `η_t`. The expected raw-size drift is

$$L_t x=(b(t)-\sigma(t))x\le b(t)x.$$

The localized nonexplosion argument of the preceding review therefore gives

$$\mathbb E X_{t\wedge\tau_k}\le\mathbb E X_0e^{\mathsf B(t)},
\qquad\mathbb E X_0=m/N_0.$$

The expected number of stopped jumps on `[0,T]` is bounded uniformly in `k` by

$$2F(T)+\mathbb E X_0\int_0^T\lambda(t)N(t)e^{\mathsf B(t)}\,dt.$$

This is finite: the second integrand is `λ(t)N₀e^{F(t)}`, and `F` is bounded on the finite interval while `λ` is integrable there. Thus the argument does not incorrectly require `sup λ(t)<∞`.

The normalized candidate law has finite integrated total jump flux `2σ(t)+b(t)`. The same survival/gain iteration and nonexplosion argument identifies the auxiliary marginals with `η_t`. Loss factors now use the locally integrable rate `q_t(x)=2σ(t)+λ(t)N(t)x`; no other change is needed.

## 4. Exact product representation and finite correction

Let `Θ_j` be the fractions used at the actual fragmentation times. Then

$$X_t=X_0\left(\prod_{\text{fragmentation times }s\le t}\Theta_s\right)e^{A_t},$$

where `A_t` is the sum of nonnegative coagulation log increments. Marginal identification and the compensator give

$$\mathbb E A_t=\int_0^t a(s)\,ds.$$

The integrable bound in Section 2 proves `A_t↑A∞<∞` almost surely and in `L¹`. No logarithmic moment of a fragmentation fraction or initial size is used. In particular the product representation is well defined at every finite time, because the fragmentation clock has finite cumulative rate `2F(t)` there.

Define

$$M_t=e^{F(t)}\prod_{\text{fragmentation times }s\le t}\Theta_s.$$

Its predictable multiplicative drift is

$$\sigma(t)M_{t-}+2\sigma(t)M_{t-}(\mathbb E\Theta_t-1)=0.$$

Thus it is a local martingale. On every fixed finite interval `[0,T]`, it is bounded by `e^{F(T)}`, since every fraction is in `(0,1)`. It is therefore a true mean-one martingale on that interval, and hence a nonnegative martingale over the whole time axis.

This martingale assertion holds in the full construction filtration. The fragmentation driver has independent future increments from the past of both independent driving random measures and the initial state, and the prescribed daughter kernel is deterministic in time. The coagulation state may depend on past fragmentation without changing this conditional-mean computation.

Doob's maximal inequality gives

$$\mathbb P\left(\sup_{t\ge0}M_t>L\right)\le1/L.$$

Hence `sup_t M_t<∞` almost surely. Uniform integrability as time tends to infinity is not required, and the limit need not retain mean one.

## 5. Almost-sure finite total coagulation count

The exact count and product identities combine to give

$$N(t)X_t=N_0X_0e^{-\mathsf B(t)}M_te^{A_t}.$$

Use predictable left limits in the coagulation intensity. Then pathwise

$$\begin{aligned}
\int_0^\infty\lambda(t)N(t)X_{t-}\,dt
&\le\frac{N_0X_0}{m}\,e^{A_\infty}\sup_{t\ge0}M_t
\int_0^\infty b(t)e^{-\mathsf B(t)}\,dt\\
&\le\frac{N_0X_0}{m}\,e^{A_\infty}\sup_{t\ge0}M_t<\infty.
\end{aligned}$$

Here `∫b e^(−mathsf B)=1−e^(−mathsf B(∞))≤1`. All the other factors are finite almost surely. Their expectations need not be finite, which is immaterial for this pathwise bound.

Finite cumulative predictable intensity implies that the auxiliary process has finitely many coagulation events almost surely. Thus its upward logarithmic correction becomes exactly constant after a finite random last event. This proof requires neither a strong law for fragmentation marks nor asymptotically constant controls.

The expected total count nevertheless satisfies

$$\mathbb E\#\{\text{coagulation events in }[0,t]\}=\mathsf B(t),$$

because marginal identification gives expected instantaneous intensity `b(t)`. Therefore the expected total count is `mathsf B(∞)`, which can be finite or infinite. Almost-sure finiteness is consistent with infinite expectation. As before, the last event time generally is not a stopping time and no independent-future assertion at that time is implied.

## 6. Independent reference when fractions are parent-independent

For a prescribed time-dependent daughter kernel `D_t`, the fragmentation clock and marks form an independently scattered marked Poisson process with intensity `2σ(t)dt` and time-dependent mark law `D_t/2`. The reference log path is its additive mark sum plus `log X₀`. It has independent increments, but is not generally a stationary compound-Poisson process.

The bounded-test transport argument and the pathwise representation give the same exact one-time finite transport cost `∫a`. Any weak scaling limit of this prescribed reference with a diverging scale transfers through the finite correction. No unconditional Gaussian or deterministic-speed claim is justified for arbitrary controls and arbitrary time-dependent mark laws without additional assumptions on that reference process.

## 7. Parent-size-dependent fractions: valid extension and boundary

Now allow a measurable fraction kernel `D_{t,x}` depending on parent size, while retaining total measure two, first fraction moment one, and support in `(0,1)`. Conditional on the pre-jump state, the selected fraction still satisfies `E(Θ|t,X_{t-})=1/2`.

The moment and affinity inequalities remain valid by conditional Jensen at each parent size. The auxiliary process, nonexplosion, and marginal identification use only this conditional mean and the same finite jump flux, so they remain valid as well.

The product `M_t` is still a martingale in the full filtration. Although marks are now state-dependent, they are sampled from a predictable probability kernel using fresh randomness, and their conditional mean is exactly one half. The preceding drift calculation holds conditionally on the full past. Boundedness by `e^{F(T)}` on finite intervals again upgrades the local martingale to a true martingale.

Consequently the proofs of finite `A∞`, finite cumulative coagulation intensity, and finitely many coagulation jumps remain valid unchanged. The affinity decay likewise holds in this more general class.

What fails without further assumptions is the independent fragmentation reference: the realized fraction marks now depend on the coupled state, including its coagulation history. Subtracting the actual mark sum still leaves the finite pathwise correction, but that sum need not have the law of an independent fragmentation-only process. A fixed Poisson-reference transport theorem or scaling-limit transfer from such an independent process must not be asserted from this argument alone.

## 8. Actual-file audit and wording qualifications

The actual controlled source matches the mathematical scope verified above. Its measurable parent-dependent daughter kernel is sufficient: conditional daughter means and Jensen do not require continuity in parent size. The normalized solution's flux is `2σ+b`, which is locally integrable. In the referenced survival/gain argument, restriction of the output measure to `(0,R]` retains the complete incoming gain, while the loss multiplier is bounded by the locally integrable function `2σ+λNR`. The resulting integrating-factor identity therefore remains valid under time controls. No transition is improperly discarded by that localization.

The actual source's remaining-displacement estimate also checks:

$$\mathbb E(A_\infty-A_t)
\le\frac{H_0^2}{mN_0}\int_t^\infty b(s)e^{-\kappa(\mathsf B(s)+F(s))}\,ds
\le\frac{H_0^2}{\kappa mN_0}e^{-\kappa(\mathsf B(t)+F(t))}.$$

The second inequality uses `(mathsf B+F)'=b+σ≥b`. When cumulative activity remains finite, this second upper bound need not tend to zero, but the first does by integrability; the asserted `L¹` convergence is still valid.

The full-filtration martingale claim is correct. State-dependent daughter laws use fresh random marks with conditional mean one half, so coagulation's effect on their future distribution does not alter the compensator. The product remains bounded by `e^{F(T)}` on each fixed finite horizon. The final path-intensity bound is pathwise and does not require integrability of `exp(A∞)sup M`.

Two small source-text clarifications were reported to the root agent, without editing its file. In the independent-reference paragraph, equation (4) bounds the *remaining* correction `E(A∞−A_t)`; the one-time comparison cost is instead `E A_t=∫₀ᵗa(s)ds`. These should be distinguished so that the former is not read as a decreasing bound for the latter. The expression `mathbb E,dA_t` in the displayed compensator is also a typesetting issue; it should denote `E[dA_t]` or `d E A_t`. Neither issue changes the theorem or proof.

The deterministic nonlinear background solution is assumed, not constructed. Its separate existence review is outside this audit. Standard point-process and martingale tools need primary attribution in a manuscript; this review does not certify novelty. No mathematical counterexample or missing moment assumption was found in the actual-file reread.
