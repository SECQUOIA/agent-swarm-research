# Independent audit of the pathwise additive-log theorem

Reviewer: `review_gauge`, 2026-09-07. Read the complete [pathwise theorem](../results/pathwise-additive-log-coupling.md) and reread the complete [arbitrary-selection theorem](../results/general-additive-log-coupling.md), including the actual finite-last-coagulation proof. This audit supplements the calculations and construction in [the general additive review](general-additive-log-proof.md).

**Verdict.** The stated pathwise theorem, nonexplosion argument, marginal identification, functional limit transfer, and moment-free finite-last-coagulation corollary are correct in the inherited solution class. No extra raw second moment or logarithmic moment is needed for construction, finite accumulated displacement, or the finite-last-event assertion. The first and second daughter log moments are used only for the specified strong-law and Gaussian limits.

## 1. Weak-solution assumptions checked against the files

The general theorem inherits the mass-conserving weak-solution setting of the fractional-moment note: finite initial count and mass, locally finite count, and the integrated balance for bounded continuous tests. These are enough for the required normalized forward equation. On every finite interval, count is explicitly `N₀exp((σ−b)t)`, so it is positive and bounded. The normalized solution has total jump flux `2σ+b`; in particular its gain and loss measures are time-integrable.

The argument conditions on this given deterministic solution. It does not prove existence or uniqueness of the nonlinear population equation. The asserted process is a time-inhomogeneous Markov process in that prescribed environment.

## 2. Nonexplosion localization

The actual file uses `V(x)=x` and the drift `L_tV=(b−σ)x≤bx`. This is correct because the incoming coagulation mark has mean `m/N(t)` and the multiplicative fragmentation mark has mean one half.

The brief localization statement can be made explicit as follows. Stop at both the `k`th jump and first crossing of a size bound `R`. Before those stops, the jump rate is bounded on a finite time interval. A coagulation mark can overshoot `R`, but its conditional mean is finite, so Dynkin's formula for the stopped first moment is legitimate. Its upper drift bound and Gronwall give the stated expectation bound uniformly in `R`. For fixed `k`, a sample path has only finitely many positive finite marks before the stopping time, so removing the size bound gives convergence of the stopped state. Fatou's lemma preserves the expectation upper bound; uniform integrability of the stopped state is not needed for this step.

The compensator of the jump count, with these same stops, is bounded in expectation by

$$2\sigma T+\lambda\sup_{s\le T}N(s)\,\mathbb E X_0\int_0^T e^{bs}\,ds.$$

Removing the size localization and then using the bound for the first `k` jumps gives `P(τ_k≤T)≤C_T/k`. This proves nonexplosion. It does not silently assume a second raw-size moment.

## 3. Marginal identification and survival/gain formula

For the fixed environmental law `η_t`, the process has jump kernel

$$Q_t(x,dz)=2\sigma\operatorname{Law}(x\Theta)(dz)
+\lambda N(t)x\operatorname{Law}(x+U_t)(dz),$$

with `U_t~η_t`. The normalized population equation is exactly its linear forward equation. This verifies the rate `2σ`, the state-dependent coagulation rate, and the distinction from a naive physical lineage.

The survival/gain identity in the actual file has the correct orientation: survival is evaluated at the post-arrival state, and `Q_s^*μ_s` is the positive arrival measure. It follows by applying the weak equation to bounded backward survival tests. One can restrict their size support, where the loss rate is bounded, and then remove the restriction using the finite gain/loss flux. Alternatively, time truncation before the terminal time makes the exponential survival factor bound the apparent unbounded derivative. Neither route requires a weighted-total-variation estimate involving `M₂`.

Iterating the positive survival/gain equation gives domination of each finite-jump term of the minimal Markov law. The minimal process is conservative by the preceding nonexplosion proof. Domination between it and the candidate normalized probability law forces equality. This identifies the marginals through linear positivity and conservation; nonlinear uniqueness is not being assumed.

## 4. Finite accumulated displacement and exact path identity

Independent fragmentation clock and marks, together with the coagulation random measure, give the path identity

$$\log X_t=\log X_0+\sum_{j\le J_t}\log\Theta_j+A_t.$$

Each coagulation jump adds `log(1+U/X_−)`, so `A_t` is nonnegative and increasing. The identified marginals make its expected compensator exactly `∫₀ᵗa(s)ds`. The previously proved affinity bound gives a finite integral over all time and the claimed exponential remainder. Monotone convergence therefore gives a finite almost-sure limit and convergence in `L¹`.

The same construction couples all times on one probability space. It need not make the limiting correction independent of the fragmentation marks. Its expected displacement agrees with the optimal one-time transport cost because the coupled paths are ordered and attain the same integrated mean displacement as the quantile proof.

## 5. Finite last coagulation: complete moment-free check

The relevant predictable intensity is `q_c(t)=λN(t)X_{t-}`. For `σ=0`, the process increases to a finite positive limit while `N(t)=N₀e^(−bt)`, so the integral of this intensity is finite.

For `σ>0`, write `Y=log Θ` and `Y^(M)=max{Y,−M}`. Extended Jensen is justified even if `EY=−∞`: apply ordinary Jensen to `log(max{Θ,e^(−M)})` and then let `M` increase, or use monotone convergence of negative parts. It gives `EY≤−log2`. Thus a finite truncation can be chosen with

$$\sigma-b+2\sigma\mathbb E Y^{(M)}<0,$$

because the limiting upper value is at most `−b−σ(2log2−1)<0`.

The path identity, `Y≤Y^(M)`, and the bounded-jump compound-Poisson strong law yield a strictly negative upper limit for `t⁻¹log q_c(t)`. Left limits cause no problem: the truncated marks are bounded, so their left and right versions have the same strong-law limit. The remaining upward correction is bounded by `A∞`. Hence the intensity decays exponentially after a random finite time. On bounded time intervals its integral is finite by nonexplosion and finiteness of the states. Therefore its full cumulative integral is finite almost surely.

The time-change representation of the coagulation counting process now proves a finite total count almost surely. A realized unit-rate Poisson path has finitely many points before any finite operational time, including this random finite terminal operational time. The conclusion does not require independence between the intensity and its driving clock.

Marginal identification gives `E q_c(t)=b` at deterministic times up to an irrelevant null set of times. Tonelli's theorem consequently gives expected count `bt` up to time `t` and infinite expected total count. An almost surely finite count with infinite mean is consistent.

The actual theorem correctly limits its claim to an exactly constant pathwise offset after the last coagulation. That last event time is generally not a stopping time. No assertion of independent future fragmentation conditioned on that time should be added without further proof.

## 6. Limit statements and interpretation

The strong law with finite `E|log Θ|` follows from the reference compound-Poisson strong law and bounded `A_t`. The functional central limit theorem has variance rate `2σE[(log Θ)²]`, including Poisson count fluctuations. The correction and the finite initial log value vanish uniformly on compact rescaled time intervals after division by the square-root scale. Thus transfer in the standard Skorokhod topology is valid; no initial log moment is needed for this weak functional convergence.

The `σ=0` almost-sure limit also follows directly from the same path identity. All these paths belong to the auxiliary number-normalized representation. They do not establish statements about a tagged particle in a finite physical coagulation system.

The process and limit tools have established precedents. The proof audit does not certify novelty, and the manuscript still needs primary attribution for the standard jump-process and functional-limit machinery. No mathematical correction to the actual theorem files was required by this reread.
