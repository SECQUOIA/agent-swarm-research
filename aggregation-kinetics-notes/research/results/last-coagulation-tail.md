# Quantitative disappearance of coagulation along number-weighted paths

Date: 2026-09-07. Status: candidate result with independent full-file proof review complete; the strengthened critical overlap constant has also been independently checked. See [the proof review](../reviews/last-coagulation-tail-proof.md) and [the focused literature audit](../reviews/controlled-last-collision-literature.md). This note strengthens [the controlled pathwise theorem](controlled-additive-trajectories.md). The first-event survival calculation is standard. The candidate contribution is its combination with nonlinear sampling-law separation, including a uniform tail bound, approximation of entire future paths, and quantitative concentration of window event counts on rare paths. Publication priority is not established.

## 1. Model and notation

Assume the mass-conserving weak solution and auxiliary process of the controlled theorem. Coagulation has kernel λ(t)(x+y), fragmentation selection is σ(t), and the expected positive daughter measure has count two and mass equal to its parent. The daughter law may depend measurably on parent size and time. Put

\[
 b(t)=m\lambda(t),\quad B_c(t)=\int_0^t b(s)ds,\quad
 F(t)=\int_0^t\sigma(s)ds,\quad
 N(t)=N_0e^{F(t)-B_c(t)}.
\]

The auxiliary process has law η_t=n_t/N(t), fragments at rate 2σ(t), and coagulates at rate λ(t)N(t)X_t. Its coagulation partner has law η_t. Define

\[
 Q_t=\frac{N(t)X_t}{m},\qquad
 \pi_t(dx)=\frac{x n_t(dx)}m,\qquad
 \mathcal A_p(t)=\mathbb E Q_t^p,\quad 0<p<1.
\]

Thus E Q_t=1 and dπ_t/dη_t=N(t)x/m. The earlier fractional-moment theorem proves

\[
 \mathcal A_p(t)\le\mathcal A_p(0)
 e^{-a_pB_c(t)-a_{1-p}F(t)},\qquad a_p=1+p-2^p>0.
\tag{1}
\]

Let J_t count auxiliary coagulations. Let L be their last time, with L=0 if none occur and L=∞ if they occur arbitrarily late. Nonexplosion holds on finite intervals. No logarithmic moment is needed below.

## 2. A conditional first-event bound

For a deterministic interval [t,T], allowing T=∞, set

\[
 u_{t,T}=1-\exp\left[-\int_t^T b(s)ds\right]\in[0,1].
\]

Conditional on X_t=x, run a fragmentation-only process V_s starting at x, using the same daughter rule as the auxiliary process. Until the first later coagulation the two processes can be identical. If q=N(t)x/m, then

\[
 \mathbb E[V_s\mid V_t=x]=x e^{-[F(s)-F(t)]},\qquad
 \mathbb E\left[\frac{N(s)V_s}{m}\right]
 =q e^{-[B_c(s)-B_c(t)]}.
\tag{2}
\]

These identities hold for parent-dependent daughter laws: the conditional daughter mean is always one half of the parent. Finite-horizon fragmentation has finitely many events and V_s≤x, so the linear mean equation needs no additional moment assumption.

Give V an independent unit exponential killing threshold and accumulated hazard

\[
 H_{t,T}=\int_t^T b(s)\frac{N(s)V_s}{m}ds.
\]

The killing time is the first future coagulation time of the auxiliary process. This construction concerns the first event only; after that event the actual coagulation dynamics must resume. Tonelli and (2) give E H_{t,T}=q u_{t,T}. Consequently

\[
 \boxed{\quad
 \mathbb P(J_T>J_t\mid X_t=x)
 =\mathbb E[1-e^{-H_{t,T}}]
 \le1-e^{-q u_{t,T}}
 \le\min(1,q u_{t,T}).\quad}
\tag{3}
\]

For T=∞, the event on the left means at least one coagulation after t, without assuming a finite total count in advance. Jensen applies because 1−e^(−z) is concave. If σ vanishes after t, H is deterministic and the first inequality in (3) is equality. Thus the conditional bound cannot be uniformly improved over this model class.

## 3. Last-event tails and future-path approximation

For every p∈(0,1), averaging (3) and using min(1,z)≤z^p proves

\[
 \mathbb P(J_T>J_t)
 \le u_{t,T}^{p}\mathcal A_p(t)
 \le u_{t,T}^{p}\mathcal A_p(0)
 e^{-a_pB_c(t)-a_{1-p}F(t)}.
\tag{4}
\]

In particular, with u_t=u_{t,∞},

\[
 \boxed{\quad
 \mathbb P(L>t)\le
 u_t^p\mathcal A_p(0)e^{-a_pB_c(t)-a_{1-p}F(t)}.\quad}
\tag{5}
\]

If B_c(∞)=∞, then B_c(t)→∞ and the right side tends to zero. If B_c(∞)<∞, then u_t→0 and A_p(t)≤1. Thus (5) itself proves L<∞ almost surely for every allowed control, without using the earlier finite-log-correction martingale proof. Nonexplosion then gives a finite total number of coagulations.

An optional strictly smaller coefficient is available: replace u^p A_p by c_p u^p A_p, where

\[
 c_p=\sup_{z>0}\frac{1-e^{-z}}{z^p}<1.
\tag{6}
\]

The unique maximizer solves z/(e^z−1)=p. This improves a bound; no optimal long-time exponent is claimed.

For constant b,σ with b>0, let γ_p=b a_p+σ a_{1-p}. Then

\[
 \mathbb P(L>t)\le \mathcal A_p(0)e^{-\gamma_p t},
 \qquad
 \mathbb E e^{rL}\le
 1+\frac{r\mathcal A_p(0)}{\gamma_p-r},\quad 0<r<\gamma_p.
\tag{7}
\]

The moment formula follows from Tonelli applied to e^(rL)−1. Under controls, decay is in cumulative activity; calendar-time exponential decay requires an appropriate lower bound on activity. The constant-rate exponent in (7) need not be sharp.

There is also a direct statement about **entire future paths**. Start a fragmentation-only process at the random actual state X_t and use the same future fragmentation noise until the next coagulation. The auxiliary and fragmentation-only paths agree on [t,T] unless J_T>J_t. Therefore their path-law total variation distance, using the convention sup_A|P(A)−Q(A)|, is at most the right side of (4). This includes T=∞ on the usual càdlàg path space. The fragmentation-only process uses the prescribed parent-dependent daughter dynamics after any divergence; equality before divergence is sufficient for the coupling bound.

This is an approximation starting from the current distribution η_t. It does not assert that the auxiliary law at large t is close in total variation to pure fragmentation started at time zero.

## 4. At criticality, last-event tails measure number–mass overlap

Suppose b=σ>0 are constant. Along a fragmentation-only future, write Q_s for normalized size and let w(q)=1/(1+q). Convexity of w gives the chord bound

\[
 \mathbb E w(q\Theta)\le\tfrac12[1+w(q)].
\]

The conditional mean of Θ is one half, even for time- and parent-dependent daughters. Therefore the fragmentation generator with killing at rate bq satisfies

\[
 (L_{\rm frag}-bq)w(q)
 =2b\mathbb E w(q\Theta)-(2b+bq)w(q)\le0.
\]

The bounded process exp(−∫_t^s bQ_v dv)w(Q_s) is a supermartingale. The fragmentation-only Q_s decreases and has expectation q exp(−b(s−t)), hence converges to zero almost surely. Dominated convergence at infinite time gives the no-future-coagulation probability Ψ_t(q)≤w(q). Thus

\[
 \mathbb P(L>t\mid Q_t=q)\ge\frac{q}{1+q}
 \ge\tfrac12\min(1,q).
\]

Since E min(1,Q_t)=1−‖η_t−π_t‖_TV, equation (3) yields

\[
 \boxed{\quad
 \frac12\bigl(1-\|\eta_t-\pi_t\|_{\rm TV}\bigr)
 \le\mathbb P(L>t)
 \le1-\|\eta_t-\pi_t\|_{\rm TV}.\quad}
\tag{8}
\]

Thus the disappearance of future coagulation along this auxiliary sampling process is equivalent, up to fixed constants, to vanishing overlap between the number and mass laws. The total variation identity is the standard overlap formula for probability measures; its dynamical interpretation is the application here.

The factor one half is optimal over the allowed daughter laws. Take monodisperse Q_0=1 and selfsimilar fractions ε and 1−ε, chosen with equal probability by the auxiliary process. The two marked fragmentation clocks each have rate b. If T is the first ε-mark, then T is exponential with rate b. Before T, the integrated hazard converges in L¹ to bqT as ε decreases to zero, by domination by bqT. The expected remaining integrated hazard is at most qε, using (2) after T. Thus the total hazard converges in L¹ to bqT, and the conditional survival probability tends to E exp(−bqT)=1/(1+q). At q=1, the last-event probability tends to one half while the overlap equals one. All approximating daughters are strictly positive; the zero-size limiting law is used only to establish sharpness of the infimum.

## 5. Rare paths carry increasingly large event counts

For constant b>0 and σ≥0, fix a window length h>0 and write D_t=J_{t+h}−J_t. Its exact mean is

\[
 \mathbb E D_t=\int_t^{t+h}\mathbb E[bQ_s]ds=bh.
\tag{9}
\]

But D_t=0 eventually almost surely, by the finite-last-event theorem. In particular these window counts are not uniformly integrable. More quantitatively, (4) implies

\[
 \mathbb P(D_t>0)\le d_p e^{-\gamma_p t},\qquad
 d_p=(1-e^{-bh})^p\mathcal A_p(0).
\tag{10}
\]

For every r>1, Hölder's inequality, also valid as an extended-moment bound, yields

\[
 \mathbb E[D_t\mid D_t>0]\ge\frac{bh}{d_p}e^{\gamma_p t},
 \qquad
 \mathbb E D_t^r\ge (bh)^r d_p^{1-r}e^{(r-1)\gamma_p t}.
\tag{11}
\]

The first expression is well-defined because bh>0 guarantees a positive event probability. These are quantitative statements about rare coagulation bursts in the auxiliary number-weighted representation. They are not event statistics of a physical tagged material particle or the whole reactor.

## 6. Relation to the remaining research

The survival-clock construction, Jensen's inequality, coupling bound, overlap identity, and Hölder step are established tools. They do not on their own imply the nonlinear decay (1). The substantive candidate is the resulting complete quantitative theorem for the additive coagulation–fragmentation model, including the relation (8). A separate literature audit is required to assess whether this combination or equivalent results have already appeared.

Existence is supplied for finite initial second moment and selfsimilar time-dependent daughters by [the reviewed existence proof](additive-model-wellposedness.md). For arbitrary measurable parent-dependent kernels, all conclusions here retain the existing weak-solution assumption. The argument applies to every solution in that class and does not assert uniqueness.
