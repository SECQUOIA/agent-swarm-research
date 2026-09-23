# Independent review: equal-split last-coagulation formulas

Date: 2026-09-07. Reviewer: independent subagent `review_last_exact`.

The formulas are correct under the existing assumptions of a nonexplosive auxiliary process with its prescribed self-consistent marginal law. This review independently derives the identities and strengthens the proposed negative result. The review began with formulas supplied in the task; after the manuscript was written, the reviewer also read [the complete result note](../results/last-coagulation-exact-equal-split.md) and checked its additional formulas and conclusions. The manuscript passes this review.

## 1. Survival product and normalization

At criticality, the normalized state fragments from q to q/2 at rate 2b and coagulates at rate bq. Along a fragmentation-only path, its successive holding times are E_k/(2b), with independent unit exponentials E_k. The accumulated coagulation hazard is therefore qS, where

\[
 S=\sum_{k\ge1}2^{-k}E_k,\qquad ES=1.
\]

The probability of no later coagulation is

\[
 \Psi(q)=E e^{-qS}=\prod_{k\ge1}(1+q2^{-k})^{-1}.
\]

The partner law does not enter this calculation because only the first future coagulation matters. The product converges locally uniformly, and its functional equation is

\[
 2\{\Psi(q/2)-\Psi(q)\}=q\Psi(q).
\]

The product itself is established prior work: it is Theorem 1.1(i) of [Bertoin, Biane and Yor, *Poissonian exponential functionals, q-series, q-integrals, and the moment problem for log-normal distributions*](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf), with their geometric parameter 1/2 and their Laplace argument −q/2. Their exponential functional is twice S. No novelty claim should be made for this transform.

## 2. Both overlap constants are sharp

Put g=1−Ψ. The Laplace representation proves that g is increasing and concave, g(0)=0, and g'(0)=1. Consequently,

\[
 c_*\min(1,q)\le g(q)\le\min(1,q),\qquad
 c_*=g(1)=0.580577558204892\ldots.
\]

For q≤1, the lower bound is the chord inequality between 0 and 1; for q≥1 it follows from monotonicity. The upper bound follows from 1−e^{-x}≤min(1,x) and ES=1. Averaging gives the claimed sharp comparison for h(t)=P(L>t).

The lower constant remains sharp when EQ=1: equality holds for Q≡1. The upper constant is sharp in this same class: give Q the value ε² with probability 1−ε and the value [1−(1−ε)ε²]/ε with probability ε. Both Eg(Q) and E min(1,Q) are asymptotic to ε. Thus the mean constraint does not improve either constant.

## 3. Rigorous last-event density

For the marginal law μ_t of Q_t, the generator applied to Ψ is

\[
 \mathcal G_t\Psi(q)
 =2b[\Psi(q/2)-\Psi(q)]
 +bq\int[\Psi(q+v)-\Psi(q)]\mu_t(dv)
 =bq\int\Psi(q+v)\mu_t(dv).
\]

This computation is legitimate despite the unbounded jump rate. The absolute coagulation contribution before cancellation is at most bqΨ(q)≤2b, and the fragmentation contribution is bounded. Localize the process, apply the jump compensation formula, and use bounded convergence at endpoints and dominated convergence in the integrals. Nonexplosion removes the stopping times. Thus

\[
 h(t)-h(s)=-b\int_s^t E[Q_u\Psi(Q_u+V_u)]\,du,
\]

where Q_u and V_u are independent with law μ_u. No second moment is needed for this step. In particular h is absolutely continuous and the claimed derivative holds almost everywhere.

In fact the derivative holds at every time where μ_t is weakly continuous, with a right derivative at zero. The integrand (q,v)↦qΨ(q+v) is bounded and continuous. Weak continuity of μ_t, hence of μ_t⊗μ_t, gives continuity of its expectation. For the assumed jump process, stochastic continuity follows from the expected number of jumps in a short interval: the fragmentation contribution is 2b times its length and the coagulation contribution is b times its length, using EQ_t=1. Therefore h is continuously differentiable for t>0.

This identifies the density of L on (0,∞). There may also be an atom at L=0 for paths with no coagulations. Strict positivity of q and Ψ makes the density positive at finite times; it need not have a uniform lower bound in terms of h.

## 4. A stronger failure of scalar differential inequalities

The proposed ε² example correctly gives h(0)∼ε and D(0)=E[QΨ(Q+V)]=O(ε²), excluding h'≤−rbh with a universal r>0. A stronger example excludes every fixed positive power of h.

Let ε↓0, define

\[
 \delta_\varepsilon=\exp[-(\log(1/\varepsilon))^3],\qquad
 A_\varepsilon=\frac{1-(1-\varepsilon)\delta_\varepsilon}{\varepsilon},
\]

and let Q equal δ_ε with probability 1−ε and A_ε with probability ε. Then EQ=1, each individual distribution has all moments finite, and

\[
 \varepsilon g(A_\varepsilon)\le h(0)\le\varepsilon+\delta_\varepsilon,
 \qquad
 D(0)\le\delta_\varepsilon+\Psi(A_\varepsilon).
\]

For every integer M, retaining the first M product factors gives

\[
 \Psi(q)\le 2^{M(M+1)/2}q^{-M}.
\]

It follows that h(0)∼ε and D(0)/h(0)^α→0 for every fixed α>0. Hence no positive constants c, α can give a distribution-uniform inequality h'≤−cbh^α for all mean-one initial laws in this class. This statement concerns instantaneous dissipation uniformly over initial data; it does not contradict the previously established exponential upper bounds with other initial-data functionals.

## 5. Large-state expansion

For q≥1, write log₂q=n+θ with integer n≥0 and θ∈[0,1). Splitting the product at k=n gives exactly

\[
 \log\Psi(q)=-\frac{(\log q)^2}{2\log2}
 +\frac12\log q-P(\theta)+R(q),
\]

where

\[
 P(\theta)=\frac{\log2}{2}(\theta-\theta^2)
 +\sum_{j\ge0}\log(1+2^{-j-\theta})
 +\sum_{\ell\ge1}\log(1+2^{\theta-\ell}),
 \qquad
 R(q)=\sum_{r\ge0}\log(1+q^{-1}2^{-r}).
\]

This verifies all signs and constants in the proposed expression. The defining sums for P converge uniformly on [0,1]. The endpoint values agree, so P extends to a continuous periodic function; it also satisfies P(1−θ)=P(θ).

The requested remainder bound is valid, and can be sharpened:

\[
 0\le R(q)\le\frac2q,\qquad
 \frac2q-\frac{2}{3q^2}\le R(q)
 \le\frac2q-\frac{2}{3q^2}+\frac{8}{21q^3}.
\]

These follow by summing the first two or three alternating bounds for log(1+x), valid here because 0≤x≤1. The lower bound 0 also covers any concern about the quadratic truncation. The expansion establishes faster-than-polynomial decay directly. Since it is an elementary rearrangement of a known q-product, it should be treated as a useful explicit formula unless a separate priority search supports stronger claims.

## 6. General daughter laws: independently verified extremality

A follow-up supplied a stronger statement at criticality b=σ. Allow the daughter fraction Θ to depend measurably on the current time and state, subject to 0<Θ<1 and E[Θ | time, state]=1/2. Let Ψ_true(t,q) be the conditional no-future-coagulation probability. Then

\[
 \boxed{\quad \Psi_{\rm eq}(q)\le\Psi_{\rm true}(t,q)
 \le\frac1{1+q}.\quad}
\]

Equivalently,

\[
 \boxed{\quad \frac{q}{1+q}\le
 P(\text{a future coagulation}\mid Q_t=q)
 \le1-\Psi_{\rm eq}(q).\quad}
\]

Here Ψ_eq is the equal-split product above. Both conditional bounds are optimal over these daughter laws, the lower event bound being an infimum when daughter fractions must be strictly positive.

For a complete verification, write Y_s for the fragmentation-only state starting at q and H_s=b∫₀ˢY_u du. For bounded f, the process e^{-H_s}f(Y_s) has drift

\[
 e^{-H_s}\left\{2b(E[f(Y_s\Theta)\mid s,Y_s]-f(Y_s))
 -bY_s f(Y_s)\right\}.
\]

All drift terms are bounded along this path because 0≤Y_s≤q and fragmentation has constant rate. For f=Ψ_eq, convexity and Jensen's inequality give E f(qΘ)≥f(q/2). The functional equation from Section 1 therefore makes the drift nonnegative. For w(q)=(1+q)^{-1}, convexity gives the chord inequality

\[
 w(q\Theta)\le(1-\Theta)w(0)+\Theta w(q),
\]

and hence E w(qΘ)≤[1+w(q)]/2. The killed drift of w is at most b[1−w(q)−qw(q)]=0.

Now Y_s decreases almost surely, and E Y_s=qe^{-bs}. Thus Y_s→0 almost surely. Both test functions tend to 1 at zero; bounded convergence yields

\[
 E[e^{-H_s}\Psi_{\rm eq}(Y_s)]\longrightarrow\Psi_{\rm true}(t,q),
 \qquad
 E[e^{-H_s}w(Y_s)]\longrightarrow\Psi_{\rm true}(t,q).
\]

The submartingale and supermartingale inequalities prove the claimed bounds. This argument applies to the stated parent- and time-dependent daughter kernels without assuming a stationary daughter distribution.

The upper future-event bound is attained by equal halves. For sharpness of the lower bound, take constant binary splits (ε,1−ε), with the auxiliary daughter chosen uniformly. Couple all ε using common rate-2b fragmentation times and fair branch coins. There are finitely many fragmentation events on each finite interval, so the fragmentation paths and accumulated hazards converge almost surely as ε↓0 to those with Θ∈{0,1}, each with probability 1/2. In the limiting process, the first zero branch occurs at rate b, so H_∞ has law qE for a unit exponential E, giving Ψ_true=1/(1+q).

Passing from finite to infinite horizons is uniform in ε because

\[
 E(H_\infty-H_T)=b\int_T^\infty E Y_s\,ds=qe^{-bT},
 \qquad
 |E e^{-H_\infty}-E e^{-H_T}|\le qe^{-bT}.
\]

Therefore the same value is approached by strictly positive binary splits. Averaging q/(1+q)≥(1/2)min(1,q) proves the improved general overlap bound

\[
 \tfrac12 E\min(1,Q_t)\le P(L>t)\le E\min(1,Q_t).
\]

The lower constant 1/2 is optimal over all allowed laws and initial states: use Q_0≡1 and let ε↓0. The upper constant 1 remains optimal by the equal-split two-atom example in Section 2. The stronger pointwise upper bound E[1−Ψ_eq(Q_t)] is also available for every allowed daughter law.

## 7. A sharp upper bound on the last-event hazard

Another follow-up observation is correct. In the equal-split case, the product inequality ∏_{k≥1}(1+q2^{-k})≥1+q gives Ψ_eq(q)≤1/(1+q) and hence qΨ_eq(q)≤1−Ψ_eq(q)=g(q). Therefore

\[
 D(t)=E[Q_t\Psi_{\rm eq}(Q_t+V_t)]
 \le E[Q_t\Psi_{\rm eq}(Q_t)]\le h(t).
\]

The exact derivative yields h'≥−bh, or

\[
 h(t)\ge h(s)e^{-b(t-s)},\qquad t\ge s.
\]

The constant b is optimal as a distribution-uniform coefficient. To see this, let Q=ε with probability 1−ε², and Q=[1−(1−ε²)ε]/ε² with probability ε². Then EQ=1. The small-state contribution and g'(0)=1 give h(0)∼ε. Its pair with another small state gives D(0)≥(1−ε²)²εΨ_eq(2ε)∼ε, while D≤h proves D(0)∼ε. Thus D/h→1.

The inequality extends to the general daughter kernels in Section 6. Define Ψ_true(t,z) as there. Mark each coagulation event by the indicator that no coagulation follows it. Conditional on the event time t and post-event state z, its expected mark is Ψ_true(t,z). Taking this conditional expectation and then using the coagulation compensator gives the density of the last-event law on (0,∞):

\[
 j(t)=bE[Q_t\Psi_{\rm true}(t,Q_t+V_t)].
\]

This can be stated first as an integral identity on a deterministic time interval. It requires only the process and its conditional future law, not differentiation of Ψ_true with respect to time. The previous finite-last-event theorem supplies finiteness of L; an atom at zero represents paths with no coagulations. The daughter envelopes now give

\[
 j(t)\le bE\frac{Q_t}{1+Q_t+V_t}
 \le bE\frac{Q_t}{1+Q_t}
 \le b h(t).
\]

Consequently h is absolutely continuous and h'≥−bh almost everywhere, giving the same lower exponential comparison for all critical daughter kernels. The bound is sharp because the equal-split examples belong to this class.

This is an **upper** bound b on the instantaneous conditional rate at which the final-event tail disappears. Section 4 rules out a uniform positive **lower** bound on that rate. The two conclusions are compatible and should be clearly distinguished.

## 8. Checks of the complete manuscript

The manuscript's Laplace equation (11) has the correct sign and factor. For φ_t(s)=E e^{-sQ_t}, the coagulation term is

\[
 bE[Q_t e^{-sQ_t}](\phi_t(s)-1)
 =b[1-\phi_t(s)]\partial_s\phi_t(s),
\]

while fragmentation contributes 2b[φ_t(s/2)−φ_t(s)]. The derivative in s exists at s≥0 because EQ_t=1, and the generator terms are integrable. The mixture formulas (10) follow from the independent S representation and Tonelli; the sign in −φ_t'(S)φ_t(S) is correct.

The exponential-moment bracket (14) is also correct, including divergence at r=b. The lower bound h(t)≥h(0)e^{-bt}, with h(0)>0 because Q_0>0, implies

\[
 E e^{rL}=1+r\int_0^\infty e^{rt}h(t)\,dt=\infty
 \quad\text{for }r\ge b.
\]

The preceding fractional-moment estimate gives finiteness for 0<r<(3−2√2)b. No conclusion at the lower endpoint (3−2√2)b follows from that estimate, and the manuscript correctly leaves it unresolved.

The alternative wording used to demonstrate sharpness of the overlap upper constant is valid: a typical atom ε and a rare atom of order ε^{-1} works, as well as the ε² example in Section 2 of this review. For a precise instance, give ε probability 1−ε and give [1−(1−ε)ε]/ε probability ε. Then EQ=1, h∼2ε, and E min(1,Q)∼2ε. Thus their ratio tends to one.

The Taylor coefficients 1, −1, 2/3, −8/21 in manuscript equation (3), Var(S)=1/3, and the finite-product certificate (17) are correct. The latter follows from log(1+x)≤x and ∑_{k>K}q2^{-k}=q2^{-K}; its rational lower certificate follows from e^{-x}≥1−x.

## Verdict

The survival formula, sharp overlap constants, density identity, proposed counterexample, and log-periodic expansion pass independent verification. The strengthened counterexample, general daughter-law extremality, and sharp upper bound on the last-event hazard also pass. The product is known; publication novelty of its application to the nonlinear auxiliary process, of the daughter extremality, and of the dissipation obstruction remains unresolved.
