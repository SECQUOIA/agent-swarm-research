# Finite coagulation along number-weighted trajectories under controlled rates

Date: 2026-09-07. Status: independently checked candidate extension; see [the controlled proof review](../reviews/controlled-additive-log-proof.md). The auxiliary representation uses established tagged-process and change-of-weighting ideas. The candidate contribution is the finite accumulated logarithmic correction and the almost-sure finite last coagulation event under the stated broad rate and daughter-law assumptions.

## Assumptions

Let λ(t),σ(t)≥0 be deterministic locally integrable functions. Coagulation has kernel K_t(x,y)=λ(t)(x+y). Each particle fragments at selection rate σ(t). Its expected daughter measure b_{t,x} is a measurable kernel, supported on (0,x), satisfying

\[
 b_{t,x}((0,x))=2,\qquad \int z\,b_{t,x}(dz)=x.
\]

The daughter law may depend on parent size and time. Let n_t be a global nonnegative weak solution conserving finite mass m>0, with finite initial count N_0>0. All weak tests and truncations are understood as in the preceding moment analysis. Write

\[
 b(t)=m\lambda(t),\quad
 B_c(t)=\int_0^t b(s)ds,\quad
 F(t)=\int_0^t\sigma(s)ds,\quad C(t)=B_c(t)+F(t).
\]

The symbol B_c is cumulative coagulation activity; it is not a daughter kernel. Number satisfies N(t)=N_0 exp(F(t)−B_c(t)). Let η_t=n_t/N(t) and π_t=x n_t/m.

## Theorem 1: a sampling-law estimate uniform over rate controls

For p∈(0,1), set a_p=1+p−2^p and

\[
 \mathcal A_p(t)=M_p(t)/(N(t)^{1-p}m^p).
\]

Then

\[
 \mathcal A_p(t)\le\mathcal A_p(0)
 \exp\{-a_pB_c(t)-a_{1-p}F(t)\}.
\tag{1}
\]

In particular H=M_1/2 satisfies

\[
 \frac{H(t)^2}{N(t)}\le\frac{H_0^2}{N_0}e^{-\kappa C(t)},
 \qquad \kappa=3-2\sqrt2.
\tag{2}
\]

**Proof.** Apply the sharp coagulation pair inequality and daughter Jensen inequality pointwise in time, then differentiate the explicit number normalization. The scalar differential inequality has locally integrable coefficients; its integrating factor gives (1). No self-similarity of b_{t,x} is used. Taking p=1/2 and squaring gives (2). The same finite-time moment bounds justify the bounded truncations. ∎

## Theorem 2: an auxiliary path with finitely many coagulations

There is a nonexplosive auxiliary process X_t with law η_t, having the following jumps:

- at rate 2σ(t), replace x by a daughter drawn from b_{t,x}/2;
- at rate λ(t)N(t)x, replace x by x+U_t with U_t independently sampled from η_t at that event.

Let Θ_j=X_{s_j}/X_{s_j-}∈(0,1) be the fraction retained at the j-th fragmentation time. Let A_t be the sum of the upward log increments log(1+U/X_−) at coagulations. Then

\[
 \log X_t=\log X_0+\sum_{s_j\le t}\log\Theta_j+A_t,
\tag{3}
\]

where A_t increases to a finite A_infinity almost surely and in L¹. Quantitatively,

\[
 \mathbb E(A_\infty-A_t)
 \le \frac{H_0^2}{mN_0}
       \int_t^\infty b(s)e^{-\kappa C(s)}ds
 \le \frac{H_0^2}{\kappa mN_0}e^{-\kappa C(t)}.
\tag{4}
\]

The auxiliary process has only finitely many coagulation jumps almost surely, over the entire time axis. In contrast, its expected total coagulation count is B_c(infinity), which can be infinite.

### Construction and finite-time justification

The generator is the time-controlled version of the generator in [the pathwise note](pathwise-additive-log-coupling.md). Conditional on current state and past, EΘ_j=1/2, and EU_t=m/N(t). Thus L_t x=(b(t)−σ(t))x≤b(t)x. Stopping and Grönwall yield E X_{t∧τ_k}≤E X_0 exp(B_c(t)). The expected stopped event count on [0,T] is bounded by

\[
 2F(T)+\mathbb E X_0\int_0^T\lambda(s)N(s)e^{B_c(s)}ds<\infty.
\]

Local integrability of the controls and boundedness of their cumulative exponentials on finite intervals justify finiteness. The bound is independent of k, proving nonexplosion. Marginal identification uses the positive minimal forward-equation expansion already proved in the pathwise note. Here q_t(x)=2σ(t)+λ(t)N(t)x is integrably bounded on each bounded-size set, which is sufficient for the loss integrating factor. The prescribed law has integrable flux ∫q_t dη_t=2σ(t)+b(t).

The coagulation compensator gives

\[
 \mathbb E[dA_t]=
 \frac{\lambda(t)}{N(t)}
 \iint x\log(1+y/x)n_t(dx)n_t(dy)\,dt
 \le\frac{\lambda(t)H(t)^2}{N(t)}dt.
\]

Insert (2) to obtain the first bound in (4). Since C'(t)=b(t)+σ(t)≥b(t), the second follows by integrating the derivative of exp(−κC). In particular E A_infinity≤H_0²/(κmN_0)≤1/κ, proving the finite logarithmic correction.

### A product martingale proves the last-event assertion

Define

\[
 M_t=e^{F(t)}\prod_{s_j\le t}\Theta_j.
\]

Its compensator drift vanishes: fragmentation has rate 2σ(t), and the conditional multiplier mean is 1/2. On each finite horizon M_t≤e^{F(T)}, so the local martingale is a true mean-one martingale. This remains true in the full filtration: coagulation randomness is nonanticipating and changes future daughter laws but not their conditional mean. Doob's inequality gives sup_{t≥0}M_t<∞ almost surely.

The path identity yields

\[
 N(t)X_t=N_0X_0e^{-B_c(t)}M_t e^{A_t}.
\]

Therefore the total coagulation intensity along this path is bounded by

\[
 \int_0^\infty\lambda(t)N(t)X_{t-}\,dt
 \le\frac{N_0X_0}{m}e^{A_\infty}\sup_tM_t
       \int_0^\infty b(t)e^{-B_c(t)}dt
 \le\frac{N_0X_0}{m}e^{A_\infty}\sup_tM_t<\infty
\]

almost surely. The finite-compensator criterion, or the random-time-change construction, proves a finite number of coagulation jumps. On the other hand E[λ(t)N(t)X_t]=b(t), so the expected number up to time t is B_c(t). This proves all assertions. No logarithmic moment is required. ∎

## What can be compared to an independent fragmentation process

If b_{t,x} is self-similar with parent-independent fraction law B_t, then the fragmentation times and marks in (3) form an independent marked inhomogeneous Poisson process, with rate 2σ(t) and mark law B_t/2 at time t. Dropping A_t defines a genuine independent-increment comparison process starting from X_0. The finite-cost, stochastic-order, and scaling-limit-transfer statements from the constant-rate notes then hold. The one-time comparison cost is E A_t, bounded by the integral of the displacement estimate from zero to t; it increases to a finite limit. Equation (4) bounds the remaining correction E(A_infinity−A_t), not that one-time comparison cost.

For a parent-dependent daughter law, the realized Θ_j depend on the current auxiliary state. Dropping A_t while retaining those marks need not produce the law of a standalone pure-fragmentation process. The finite-last-coagulation result still holds, but the independent Poisson-reference conclusion is not asserted. After the last coagulation, the auxiliary path obeys the fragmentation dynamics; the last coagulation time generally is not a stopping time, so its future must not be declared conditionally independent of that time.

## Interpretation and limits

The theorem permits externally controlled coagulation and fragmentation rates and arbitrary positive mass-conserving binary daughter laws. Its scope remains additive coagulation and number-normalized sampling. It does not say that coagulation ceases in the population or along the physical mass-tagged process. Expected auxiliary coagulation counts can remain large or infinite because rare trajectories dominate that expectation.

The finite logarithmic correction is a statement about an auxiliary representation of an existing weak solution. A separate independently reviewed [existence note](additive-model-wellposedness.md) supplies global mass-conserving solutions for finite initial second moment and selfsimilar, time-dependent daughter laws. It does not establish existence for arbitrary measurable parent-dependent kernels; that broader case remains conditional on the weak solution assumed here. Standard martingale, Doob-transform, and jump-process constructions are not claimed as new.
