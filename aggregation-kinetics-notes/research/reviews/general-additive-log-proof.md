# Independent review: arbitrary constant selection and auxiliary paths

Reviewer: `review_gauge`, 2026-09-07. This review checks the full [general additive-log theorem](../results/general-additive-log-coupling.md), building on the separate [critical-rate review](log-size-poisson-proof.md). The auxiliary-process extension was initially communicated for independent scrutiny and is proved separately below. The subsequently written [pathwise theorem](../results/pathwise-additive-log-coupling.md), including its last-coagulation corollary, was then read in full and audited in [a separate review](pathwise-additive-log-proof.md).

**Verdict.** The arbitrary-selection statements are correct under the stated global mass-conserving weak-solution assumptions. The auxiliary jump process can also be constructed rigorously, identified with the normalized number marginals, and used for pathwise limit results. Its interpretation must remain an auxiliary process; it is not asserted to be a physical tagged lineage.

## 1. Count and normalized equation

For `K(x,y)=λ(x+y)`, constant selection `σ≥0`, and conserved mass `m>0`, set `b=λm>0`. The count equation is

$$N'=(\sigma-b)N,\qquad N(t)=N_0e^{(\sigma-b)t}.$$

Thus count stays positive and finite on every finite interval. Write `η_t=n_t/N(t)` and `ρ_t=(log)#η_t`. Coagulation contributes `−bρ_t` plus its upward remainder; fragmentation contributes `2σE[shift]ρ_t−σρ_t`; normalization contributes `−(σ−b)ρ_t`. Therefore

$$\partial_t\rho_t=2\sigma(T_B-I)\rho_t+R_t,$$

where

$$R_t\varphi=\frac\lambda{N(t)}\iint x[\varphi(\log(x+y))-\varphi(\log x)]\,dn_t(x)dn_t(y).$$

This checks that the reference Poisson rate is `2σ` for every `σ`, including zero. The total variation of `R_t` is at most `2b`.

## 2. Fractional affinities

The sharp moment inequality gives

$$M_p'\le[-b(2-2^p)+\sigma(2^{1-p}-1)]M_p.$$

After dividing by `N(t)^(1−p)m^p`, the resulting decay coefficient is exactly

$$b(1+p-2^p)+\sigma(2-p-2^{1-p}).$$

Both bracketed coefficients are strictly positive for `0<p<1`, since the strictly convex function `2^p` lies below the chord `1+p` on that interval. No division by a possibly vanishing moment is needed; an integrating factor proves the inequality directly.

The measure identity also checks:

$$\mathcal A_p=\frac{M_p}{N^{1-p}m^p}
=\int\left(\frac{d\pi_t}{d\eta_t}\right)^p d\eta_t,
\qquad \pi_t=\frac{x n_t}{m}.$$

In particular `H/√(mN)` is precisely the Hellinger affinity. With `κ=3−2√2`,

$$\frac{H(t)^2}{N(t)}\le\frac{H_0^2}{N_0}e^{-\kappa(b+\sigma)t}.$$

The exponent can be checked directly:

$$2[-b(2-\sqrt2)+\sigma(\sqrt2-1)]-(\sigma-b)
=-\kappa(b+\sigma).$$

This normalization is essential: the unnormalized half moment can increase when fragmentation is strong. The instantaneous affinity coefficient is sharp over the permitted initial data and daughter laws, because monodisperse initial data with equal splitting attains both underlying bounds.

## 3. Uniform and exact transport cost

For bounded 1-Lipschitz tests, the upward remainder is bounded by

$$a(t)=\frac\lambda{N(t)}\iint x\log(1+y/x)\,dn_t(x)dn_t(y)
\le\frac\lambda{N(t)}H(t)^2.$$

The bounded-test Duhamel argument, stochastic order, and clipped quantile proof from the critical-rate review apply to the compound-Poisson reference of rate `2σ` without any logarithmic moment assumptions. Hence the exact extended transport cost is `∫₀ᵗa(s)ds`, and

$$\int_0^t a(s)\,ds\le C_0(1-e^{-\kappa(b+\sigma)t}),$$

$$C_0=\frac{\lambda H_0^2}{\kappa(b+\sigma)N_0}
\le\frac b{\kappa(b+\sigma)}.$$

The prefactor reduces to the earlier one at `σ=b` and is nonsingular at `σ=0`, because `b>0`. This is finite expected coupling displacement even if the marginal logarithmic means are infinite; ordinary `P₁-W₁` conclusions retain their first-moment assumptions.

All stated one-time scaling consequences check. With finite jump second moment, the centered Gaussian variance rate is `2σE(Y²)`, and the drift is `2σEY`. Any other weak scaling limit of the reference transfers whenever its scale diverges. The finite correction need not control raw-size moments.

## 4. Pure additive coagulation

When `σ=0`, the normalized equation has only upward shifts. Thus `ρ_s` is stochastically dominated by `ρ_t` for `s≤t`, and their common quantile coupling satisfies

$$\mathbb E[Q_t-Q_s]=\int_s^t a(r)\,dr\le C_0e^{-\kappa bs}.$$

The quantiles increase to a limit whose increase from the initial quantile has finite expectation. This limit is finite almost surely and defines a probability law on the ordinary real log axis. Monotone convergence proves

$$\mathcal W_1(\rho_t,\rho_\infty)=\int_t^\infty a(r)\,dr
\le C_0e^{-\kappa bt}.$$

This verifies tightness and the stronger exponential convergence in finite-cost transport. It does not imply convergence of the arithmetic mean. This limiting pure-coagulation phenomenon has prior literature; the present review establishes correctness rather than novelty.

## 5. Auxiliary jump process: construction and nonexplosion

Fix the deterministic population-balance solution, so that `η_t` and `N(t)` are prescribed. Consider a time-inhomogeneous jump process `X_t>0` started with law `η₀`:

- At an independent Poisson rate `2σ`, replace `X` by `ΘX`, with independent marks `Θ~B/2`.
- At rate `λN(t)X`, replace `X` by `X+V`, with a mark drawn independently from the prescribed law `η_t`.

The state-dependent coagulation rate is unbounded, so nonexplosion needs proof. The mark means are finite:

$$\mathbb E\Theta=\tfrac12,\qquad\int y\eta_t(dy)=m/N(t).$$

The formal drift of `V(x)=x` is therefore

$$L_tV(x)=\lambda N(t)x\frac m{N(t)}+2\sigma x(\tfrac12-1)
=(b-\sigma)x\le bx.$$

Let `τ_k` stop the minimal construction at its `k`th jump. Localization and the preceding Lyapunov bound give

$$\mathbb E X_{t\wedge\tau_k}\le\mathbb E X_0e^{bt},
\qquad\mathbb E X_0=m/N_0<\infty.$$

For completeness, this estimate can first be proved with bounded-state localization and then extended; the positive jump mark has finite first moment and the displayed drift upper bound is uniform under that localization. Negative fragmentation increments do not obstruct the upper bound.

On any finite interval `[0,T]`, the expected number of coagulation jumps before `T∧τ_k` is bounded by

$$\lambda\sup_{s\le T}N(s)\int_0^T\mathbb E X_{s\wedge\tau_k}\,ds.$$

The expected fragmentation count is at most `2σT`. These bounds are uniform in `k`. Consequently `P(τ_k≤T)≤C_T/k`, proving that the minimal process is nonexplosive. Finite first raw-size moment, which is already part of the population assumptions, is sufficient; no logarithmic moments enter.

## 6. Identification of its marginals

The generator of this process is

$$L_tf(x)=2\sigma\mathbb E[f(\Theta x)-f(x)]
+\lambda N(t)x\int[f(x+y)-f(x)]\eta_t(dy).$$

Its linear forward equation is exactly the normalized population-balance equation, with the environment `η_t` held fixed. The candidate marginal `η_t` has finite integrated total jump flux, since

$$\int[2\sigma+\lambda N(t)x]\eta_t(dx)=2\sigma+b.$$

The identification does not require an unproved nonlinear uniqueness claim. One rigorous route is the usual positive jump-series construction, which can be seen directly here. For the total rate `q_t(x)=2σ+λN(t)x`, write the linear forward equation in killed-jump Duhamel form with survival factor

$$S_{s,t}(x)=\exp\left(-\int_s^tq_r(x)\,dr\right).$$

The candidate's finite flux makes its gain integral well defined. Iterating this positive integral equation shows that any nonnegative solution with the prescribed initial law dominates each finite-jump term of the minimal process's law. Hence it dominates the full minimal law. Nonexplosion makes the latter a probability law, while the candidate `η_t` is also a probability law. Their difference is a nonnegative measure of mass zero, so they are equal.

The killed-jump formula can be derived from bounded backward survival tests; approaching the terminal time is justified by the finite flux. This gives a direct forward-equation uniqueness argument in the required class.

## 7. Finite pathwise coagulation correction

On the constructed process, let

$$A_t=\sum_{\substack{s\le t\\\text{coagulation jump}}}\log(1+V_s/X_{s-}).$$

This process is nonnegative and increasing. The exact pathwise identity is

$$\log X_t=\log X_0+\sum_{j=1}^{J_t}\log\Theta_j+A_t,$$

where the fragmentation clock has rate `2σ`. Since the marginals have now been identified as `η_t`, the coagulation compensator gives

$$\mathbb E A_t=\int_0^t a(s)\,ds.$$

Monotone convergence and the uniform bound imply

$$A_t\uparrow A_\infty<\infty\quad\text{almost surely and in }L^1,$$

$$\mathbb E(A_\infty-A_t)=\int_t^\infty a(s)\,ds
\le C_0e^{-\kappa(b+\sigma)t}.$$

Thus there is a single pathwise coupling, rather than only separate couplings of one-time marginals. It is monotone relative to its reference path, and its expected log displacement is the already established optimal one-time transport cost. This also proves the almost-sure multiplicative correction limit

$$X_t\exp\left(-\sum_{j=1}^{J_t}\log\Theta_j\right)
\longrightarrow X_0e^{A_\infty}\in(0,\infty).$$

The limiting correction generally depends on the fragmentation history; independence from the reference process is not asserted.

## 8. Pathwise scaling consequences and interpretation

With `E|Y|<∞`, the compound-Poisson strong law gives

$$\frac{\log X_t}{t}\longrightarrow2\sigma\mathbb EY\quad\text{almost surely}.$$

With finite `E(Y²)`, the compound-Poisson functional central limit theorem transfers to the auxiliary process: on each fixed rescaled time interval,

$$\left\{\frac{\log X_{ts}-2\sigma\mathbb EY\,ts}{\sqrt t}\right\}_{s\ge0}
\Longrightarrow\left\{\sqrt{2\sigma\mathbb E(Y^2)}\,B_s\right\}_{s\ge0}.$$

The correction is negligible uniformly on compact rescaled intervals because `sup_{s≤T}A_{ts}/√t≤A∞/√t→0` almost surely. The initial logarithmic variable divided by `√t` also tends to zero almost surely because initial sizes are positive and finite. No initial logarithmic moment is needed for this weak functional convergence. A final theorem should specify a conventional path topology, for example Skorokhod `J₁`; the continuous Brownian limit and uniform negligibility of the correction make the transfer immediate from the reference functional theorem.

For `σ=0`, no daughter-jump moment assumptions are needed: `X_t` increases to a finite positive limit almost surely, recovering the limiting normalized log law above.

These statements refer to the constructed process with normalized-number marginals. Its fragmentation rate `2σ` and its coagulation sampling rule differ from a naive physical lineage. The result must not be described as a trajectory theorem for a physically tagged particle without a separate probabilistic interpretation.

## 9. Finite last coagulation, without logarithmic moments

The stronger corollary also checks. If `σ=0`, the already proved finite limit of `X_t` and exponential decay of `N(t)` make `∫₀∞λN(t)X_{t-}dt` finite almost surely. If `σ>0`, truncate the negative fragmentation marks by `Y^(M)=max{Y,−M}`. Extended Jensen gives `EY≤log EΘ=−log2`. Hence some finite `M` satisfies

$$\sigma-b+2\sigma\mathbb E Y^{(M)}<0.$$

The strong law for these bounded compound-Poisson marks, the path identity, and `A∞<∞` imply a strictly negative upper limit for `t⁻¹ log[λN(t)X_{t-}]`. Thus cumulative coagulation intensity is finite almost surely. The point-process time change then gives finitely many coagulation jumps almost surely. After their last occurrence, the upward logarithmic correction is exactly constant.

At the same time, the identified marginals give `E[λN(t)X_{t-}]=b` for almost every time, so the expected total coagulation count is infinite. This is consistent with an almost surely finite random count having infinite mean. The last jump time generally is not a stopping time; no independence of subsequent fragmentation from that time or the limiting correction follows.

## 10. Remaining scope

The deterministic global mass-conserving population-balance solution is assumed. The process construction conditions on that solution; it is not an independent proof of nonlinear existence or uniqueness. The elementary generator and moment computations have been checked directly. Standard compound-Poisson strong laws and functional limit theorems still need suitable primary attribution in a manuscript. No novelty conclusion is made here.
