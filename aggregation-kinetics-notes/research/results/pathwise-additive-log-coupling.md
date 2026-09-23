# A pathwise finite correction to fragmentation in logarithmic size

Started 2026-09-06; extended 2026-09-07. Status: candidate theorem, construction and proof independently checked by `inverse_direction` and its reviewer; see [the general proof review](../reviews/general-additive-log-proof.md). This develops [the arbitrary-rate transport theorem](general-additive-log-coupling.md). The process constructed here is an auxiliary process with the number-normalized population as its one-time marginals. It is not asserted to be a physical tagged particle or a chronological cell lineage.

## Model and theorem

Retain K(x,y)=λ(x+y), total mass m>0, b=λm>0, constant binary fragmentation selection σ≥0, and the fixed daughter fraction probability Θ~B/2. Write η_t=n_t/N(t) and N(t)=N_0 exp((σ−b)t). The background n_t is a specified mass-conserving weak solution in the class of the preceding note. Particle sizes and fractions are positive and finite. No logarithmic moment is required for the construction.

**Theorem.** There exists a nonexplosive time-inhomogeneous Markov jump process X_t>0 whose law is η_t and, on the same probability space, a Poisson process J of rate 2σ with independent marks Θ_j~B/2 such that

\[
 \log X_t=\log X_0+\sum_{j=1}^{J_t}\log\Theta_j+A_t,
\tag{1}
\]

where A_t is nonnegative and increasing. It converges almost surely and in L¹ to a finite A_infinity, and

\[
 \mathbb E A_t=\int_0^t a(s)\,ds,
 \qquad
 \mathbb E(A_\infty-A_t)
 \le C_0e^{-\kappa(b+\sigma)t}.
\tag{2}
\]

Here κ=3−2√2 and a,C_0 are given in equations (4)–(5) of [the arbitrary-rate note](general-additive-log-coupling.md). The Poisson marks are independent of X_0. They need not be independent of A_infinity, which depends on the whole coupled evolution.

Thus the one-time finite-cost coupling can be chosen consistently for all times. Its expected displacement equals the optimal one-time transport cost already obtained from stochastic order.

## Construction and generator

Given a current state x at time t, impose two jump mechanisms:

- at rate 2σ, replace x by xΘ with Θ~B/2;
- at rate λN(t)x, replace x by x+U, with U independently sampled from the prescribed number law η_t at that event.

Independent Poisson random measures supply the clocks and marks; the second rate is implemented by thinning against the current state. Equivalently, its time-dependent jump kernel is

\[
 Q_t(x,dz)=2\sigma\operatorname{Law}(x\Theta)(dz)
              +\lambda N(t)x\operatorname{Law}(x+U_t)(dz),
 \quad q_t(x)=2\sigma+\lambda N(t)x.
\tag{3}
\]

The expected daughter fraction is EΘ=1/2 and the background mean is EU_t=m/N(t). For the Lyapunov function V(x)=x, the generator satisfies

\[
 \mathcal L_t V(x)=(b-\sigma)x\le bx.
\tag{4}
\]

The generator on bounded log tests is exactly (6) in the arbitrary-rate note. This is why this auxiliary process uses the division rate 2σ rather than the original event rate σ: it represents a number-weighted population balance after accounting for daughter multiplicity and normalization.

## Nonexplosion

Construct the minimal jump process, stopping at the k-th jump and, initially, at a size cutoff. Dynkin's formula for (4) and Grönwall give

\[
 \mathbb E X_{t\wedge\tau_k}\le\mathbb E X_0 e^{bt},
\]

after removing the size cutoff by the usual nonnegative Lyapunov localization. The initial mean is m/N_0<∞. On each finite interval [0,T], N is bounded, and the expected stopped number of jumps is at most

\[
 2\sigma T+\lambda\sup_{s\le T}N(s)\,
           \mathbb E X_0\int_0^T e^{bs}\,ds.
\tag{5}
\]

This bound does not depend on k. Hence P(τ_k≤T) is at most the bound divided by k and tends to zero. There is no finite-time explosion. The same argument works from each deterministic finite initial state.

## Identification of the one-time laws

It remains to show that the constructed process has law η_t, rather than simply giving a formal generator with the desired equation.

The normalized weak equation proves that η_t solves the forward equation for (3). Its jump flux is integrable on finite time intervals since

\[
 \int q_t(x)\eta_t(dx)=2\sigma+b.
\tag{6}
\]

For completeness, the minimal-process characterization supplies a direct uniqueness argument. Any nonnegative probability solution μ_t with integrable jump flux satisfies the survival/gain identity

\[
 \mu_t(dx)=e^{-\int_0^tq_r(x)dr}\mu_0(dx)
 +\int_0^t e^{-\int_s^tq_r(x)dr}(Q_s^*\mu_s)(dx)\,ds.
\tag{7}
\]

This is a weak identity for bounded tests. Restrict the output measure to (0,R], retaining the full incoming gain (Q_s*μ_s) restricted to this set. The loss rate is bounded there on each finite time interval, so its integrating factor gives (7) on that output set. Finite integrated gain follows from the flux assumption. Let R increase to infinity using nonnegativity. This restriction does not delete transitions or modify the gain. Iterating the positive right side shows that μ_t dominates the sum of the zero-jump, one-jump, and all finite-jump contributions of the minimal process. Nonexplosion makes that sum a probability measure. Domination between probability measures forces equality. Applying the argument to η_t identifies it with the law of X_t. This avoids a weighted-total-variation Grönwall estimate that could incorrectly require a second mass moment.

## Finite accumulated upward displacement

Each coagulation jump contributes log(1+U/X_−)≥0. Let A_t be their sum. The independent fragmentation jumps give the exact path identity (1). By the jump compensator and the just-established marginal law,

\[
 \mathbb E A_t
 =\int_0^t\lambda N(s)
 \iint x\log(1+y/x)\eta_s(dx)\eta_s(dy)\,ds
 =\int_0^t a(s)\,ds.
\]

The half-affinity estimate gives a(s)≤κ(b+σ)C_0e^{−κ(b+σ)s}. Hence EA_infinity≤C_0 by monotone convergence. In particular A_infinity is finite almost surely, and (2) follows by integrating the remaining tail. Monotone convergence plus convergence of expectations also gives A_t→A_infinity in L¹. ∎

## An almost-sure finite last coagulation event

In fact the auxiliary process has only finitely many coagulation jumps over its entire infinite time horizon, almost surely. No daughter log moment or initial log moment is needed for this assertion. After a random finite last coagulation time, its log path differs from the same-clock fragmentation path by an exactly constant random offset.

To prove this, consider its coagulation intensity

\[
 q_c(t)=\lambda N_0e^{(\sigma-b)t}X_{t-}.
\]

When σ=0, equation (1) and A_infinity<∞ show that X_t has a finite limit, so q_c is integrable. When σ>0, write Y=log Θ<0 and Y^{(M)}=max(Y,−M). Jensen's inequality, in its extended expectation form, gives EY≤log EΘ=−log2. Monotone convergence of the negative parts allows choosing M large enough that

\[
 \sigma-b+2\sigma\mathbb E Y^{(M)}<0,
\]

since σ−b−2σ log2 is strictly negative. Equation (1), the bound Y≤Y^{(M)}, the finite A_infinity, and the compound-Poisson strong law for the bounded marks imply

\[
 \limsup_{t\to\infty}\frac1t\log q_c(t)
 \le\sigma-b+2\sigma\mathbb E Y^{(M)}<0.
\]

Thus ∫_0^infinity q_c(t)dt<∞ almost surely. The random-time-change construction of its coagulation counting process, or the standard finite-compensator criterion for point processes, gives an almost-sure finite total count.

This random count nevertheless has infinite expectation. Marginal identification gives E q_c(t)=λN(t)E X_t=b at every time. Hence

\[
 \mathbb E\#\{\text{coagulation jumps before }t\}=bt,
 \qquad
 \mathbb E\#\{\text{all coagulation jumps}\}=\infty.
\]

There is no contradiction: a finite-valued random variable may have an infinite mean. The result concerns this auxiliary number-weighted process, not disappearance of coagulation events from the full population. The last coagulation time need not be a stopping time; no independence of future fragmentation from that time or from A_infinity is asserted. The stronger finite-last-event deduction was independently proposed and checked by `inverse_direction`.

## Pathwise and functional limits for the auxiliary process

If σ>0 and E|log Θ|<∞, the compound-Poisson strong law and (1) give

\[
 \frac{\log X_t}{t}\longrightarrow
 2\sigma\mathbb E\log\Theta\quad\text{almost surely}.
\tag{8}
\]

No initial log moment is needed: log X_0 is finite almost surely. If E(log Θ)²<∞, write μ=Elog Θ and ν_2=E(log Θ)². The usual functional central limit theorem for compound-Poisson processes yields, on every fixed compact time interval,

\[
 \left(\frac{\log X_{Ts}-2\sigma\mu Ts}{\sqrt T}\right)_{s\ge0}
 \Longrightarrow \left(\sqrt{2\sigma\nu_2}\,W_s\right)_{s\ge0}
\tag{9}
\]

in the Skorokhod topology. The transfer is immediate from

\[
 \sup_{0\le s\le s_0}\frac{A_{Ts}}{\sqrt T}
 \le A_\infty/\sqrt T\longrightarrow0
\]

almost surely, and the same observation removes the initial log value. The functional CLT for the reference process is established probability theory; the candidate result is the finite perturbation that transfers it to this nonlinear population model's auxiliary representation.

For σ=0, (1) gives actual almost-sure convergence of this auxiliary log-size path to log X_0+A_infinity, with the expected remaining displacement bounded in (2). This is consistent with the normalized additive-coagulation limit discussed in the preceding note.

## Limits and attribution

The jump-process construction uses a deterministic background solution, and the sampling weight is particle number. These auxiliary path results do not establish pathwise statements for a physical tagged particle in a finite coagulating system. The finite-system effects in [the logarithmic-time breakdown theorem](finite-population-breakdown.md) remain distinct.

Lyapunov nonexplosion, the minimal positive forward-equation expansion, and compound-Poisson limit theorems are standard tools. The novelty target is the finite cumulative nonlinear log displacement and its explicit all-time expectation bound, not the existence of jump representations in general.

The literature reviewer identified the representation as the inverse-size Doob transform of the usual mass-tagged process: h(x)=1/x satisfies L_t h=(σ−b)h, and weighting jump rates by h(new)/h(old) changes the mass-tagged coagulation rate λ(x+y)n_t(dy) to λx n_t(dy), and the mass-biased daughter measure σθB(dθ) to σB(dθ). Nonlinear mass-tagged Poisson representations are established, for example in [Deaconu, Fournier, and Tanré (2002), open author copy](https://www-sop.inria.fr/members/Etienne.Tanre/publication/AOP104.pdf). The finite-displacement conclusion needs separate comparison; it must not be marketed as the first stochastic representation of this equation.
