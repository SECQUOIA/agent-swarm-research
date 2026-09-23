# Sharp daughter-law bounds and an exact last-coagulation observable

Date: 2026-09-07. Status: complete manuscript independently verified under the stated solution assumptions. The underlying Poisson exponential functional and its infinite product are established results. The application to the nonlinear auxiliary process, daughter-law bounds, and limits of scalar tail closure are retained here without a publication-priority claim.

## 1. Setting and conclusions

Use the critical constant-rate model and auxiliary number-weighted process from [last-coagulation-tail.md](last-coagulation-tail.md). Thus b=σ>0, N is constant, and the normalized size Q=NX/m has mean one. The auxiliary process fragments at rate 2b and coagulates at rate bQ. Its independent coagulation partner V has the current law of Q.

Let L be the time of the last auxiliary coagulation, with L=0 if none occur, and write h(t)=P(L>t). The earlier theorem proves L<∞ almost surely. None of these event statements refer to a physical mass-tagged particle.

The following refinements hold:

- Among all positive binary daughter laws, equal splitting maximizes the conditional probability of any future coagulation. Splits tending to a zero-mass and a full-mass daughter minimize it in the limit.
- The sharp generic overlap coefficient is 1/2. For equal splitting it improves to the sharp constant approximately 0.58058.
- Equal splitting gives an explicit bounded observable for h and an exact nonlinear dissipation formula.
- At criticality h(t) cannot decrease faster than h(s)e^{-b(t-s)}. Conversely, no positive uniform power-law lower bound on its instantaneous dissipation is possible from h alone.

The deterministic solution and auxiliary process retain the existence hypotheses of the source note. The daughter-law envelopes allow measurable dependence on parent size and time, provided a uniformly selected daughter fraction Θ lies in (0,1) and has conditional mean 1/2.

Conditional probabilities specified for every q>0 use the auxiliary Markov construction restarted from that state and time. They are consequently defined even when the state has zero probability under the current population law.

## 2. Exact equal-split conditional probability

For equal splitting, define

\[
 \Psi(q)=P(\text{no future auxiliary coagulation}\mid Q_t=q),\qquad q>0.
\]

The function is independent of t and the future population distributions: before the first coagulation, only fragmentation matters. The next event has fragmentation probability 2/(2+q). Hence

\[
 \Psi(q)=\frac2{2+q}\Psi(q/2),\qquad \Psi(0)=1,
\]

and therefore

\[
 \boxed{\quad\Psi(q)=\prod_{k=1}^{\infty}(1+q/2^k)^{-1}.\quad}
 \tag{1}
\]

There is also a direct hazard representation. Let E_1,E_2,… be independent mean-one exponential variables and put

\[
 S=\sum_{k=1}^{\infty}2^{-k}E_k.
\]

During fragmentation alone, successive waiting times have rate 2b and the successive normalized sizes are q,q/2,q/4,…. The total coagulation hazard is distributed as qS. Thus

\[
 \Psi(q)=E e^{-qS},\qquad ES=1,\qquad \operatorname{Var}S=1/3.
 \tag{2}
\]

In particular Ψ is decreasing, strictly convex, and completely monotone. Its complement g=1−Ψ is increasing, strictly concave, and satisfies g(0)=0, g'(0)=1. The expansion at zero is

\[
 \Psi(q)=1-q+\frac23q^2-\frac8{21}q^3+O(q^4).
 \tag{3}
\]

Equation (1) is **not a new probability distribution or transform**. [Bertoin, Biane, and Yor, *Poissonian exponential functionals, q-series, q-integrals, and the moment problem for log-normal distributions*, equations (1.3) and (1.6), Theorem 1.1(i)](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf), give exactly this geometrically weighted exponential sum and its product transform. In their notation S=I^(1/2)/2 and Ψ(q)=1/(-q/2;1/2)_∞. The useful specialization here is that it computes the nonlinear auxiliary process's future-event probability without knowing its future partner laws.

## 3. Sharp bounds over every daughter law

Let Ψ_true(t,q) be the conditional probability of no future coagulation for any of the allowed daughter laws. Then

\[
 \boxed{\quad
 \Psi(q)\leq\Psi_{\rm true}(t,q)\leq\frac1{1+q},
 \qquad
 \frac q{1+q}\leq P(L>t\mid Q_t=q)\leq1-\Psi(q).
 \quad}
 \tag{4}
\]

Here the conditional event L>t means at least one coagulation strictly after t. The formula does not condition on whether earlier coagulations occurred.

The general constant-rate theorem, including the proof and sharpness, is developed in [sharp-daughter-extremality.md](sharp-daughter-extremality.md). Its critical specialization (4) can also be checked directly. The killed fragmentation generator is

\[
 \mathcal K_sf(z)=2b\{E[f(z\Theta)\mid z,s]-f(z)\}-bzf(z).
 \tag{5}
\]

Convex Jensen gives \(\mathcal K_s\Psi\geq0\), while the convex chord bound for w(z)=1/(1+z) gives \(\mathcal K_sw\leq0\). The fragmentation-only size decreases to zero almost surely, so bounded killed submartingale and supermartingale limits give (4). Equal splitting attains the upper future-event probability. The lower probability is approached by positive splits with fractions ε and 1−ε as ε↓0; zero-sized daughters are only a limiting construction. Parent and time dependence do not affect these comparisons.

## 4. Optimal overlap constants

Let η_t be the number probability law and π_t the mass probability law. Since dπ_t/dη_t=Q,

\[
 O(t):=1-\|\eta_t-\pi_t\|_{\rm TV}=E\min(1,Q_t),
\]

where total variation is sup_A|η(A)−π(A)|. Equation (4) implies

\[
 \boxed{\quad \tfrac12O(t)\leq h(t)\leq O(t).\quad}
 \tag{6}
\]

The lower factor 1/2 is optimal over all allowed daughter laws and initial distributions: take Q_0=1 and let ε-splits approach the limiting law above.

For equal splitting there is the sharper result

\[
 \boxed{\quad c_*O(t)\leq h(t)\leq O(t),\qquad
 c_*=1-\prod_{k\geq1}(1+2^{-k})^{-1}\approx0.58058.\quad}
 \tag{7}
\]

Indeed g(q)/q decreases on (0,∞) by concavity. For q≤1 this gives g(q)≥g(1)q; for q≥1 monotonicity gives g(q)≥g(1). Thus g(q)≥c_*min(1,q). The lower constant is attained at initial monodispersity Q_0=1, so it cannot be increased. The common upper constant one is optimal as a universal comparison: a mean-one two-point law with typical small value ε and rare value of order ε^-1 has h/O→1 under equal splitting.

These are pointwise and averaged sharp constants. They do not determine a sharp long-time exponential rate.

## 5. Exact equal-split tail density and Laplace observables

For equal splitting,

\[
 h(t)=1-E\Psi(Q_t).
 \tag{8}
\]

Its exact derivative is

\[
 \boxed{\quad
 h'(t)=-bE[Q_t\Psi(Q_t+V_t)],
 \quad V_t\text{ independent with the law of }Q_t.
 \quad}
 \tag{9}
\]

To verify it, the auxiliary generator applied to Ψ is

\[
 2b[\Psi(q/2)-\Psi(q)]
 +bqE[\Psi(q+V_t)-\Psi(q)].
\]

The recurrence cancels the negative coagulation term and leaves bqEΨ(q+V_t). All generator terms are bounded: qΨ(q)≤1, as follows from (4) for equal splitting, and Ψ(q+v)≤Ψ(q). Thus the bounded-test generator identity justifies the integrated version of (9) without higher size moments. Under weakly continuous one-time laws, the bounded continuous pair integrand gives the derivative at every time; otherwise the integrated identity supplies its almost-everywhere version.

Consequently the law of L has an atom EΨ(Q_0) at zero and density bE[Q_tΨ(Q_t+V_t)] on t>0. The density describes a coagulation at t followed by no further coagulation, rather than the expected rate of all coagulations, which remains b.

Let φ_t(s)=E e^{-sQ_t}. Using an independent S from (2), Tonelli gives

\[
 h(t)=1-E_S\phi_t(S),\qquad
 -h'(t)/b=E_S[-\phi_t'(S)\phi_t(S)].
 \tag{10}
\]

The ordinary Laplace transform obeys

\[
 \partial_t\phi_t(s)=2b[\phi_t(s/2)-\phi_t(s)]
 +b[1-\phi_t(s)]\partial_s\phi_t(s).
 \tag{11}
\]

Equations (10)–(11) supply an explicit distributional observable and a deterministic route to computing the last-event tail. They do not close its evolution in the scalar h alone.

## 6. A universal lower tail bound and exponential-moment bracket

For equal splitting, monotonicity and Ψ(q)≤1/(1+q) imply

\[
 E[Q\Psi(Q+V)]\leq E[Q\Psi(Q)]\leq E[1-\Psi(Q)]=h.
\]

Therefore h'≥−bh and

\[
 \boxed{\quad h(t)\geq h(s)e^{-b(t-s)},\qquad t\geq s\geq0.\quad}
 \tag{12}
\]

The same lower bound holds for all critical daughter laws covered by (4), even when they depend on parent and time. To see this, mark each auxiliary coagulation according to whether it is the last one. Conditional on the state immediately after an event at t, its probability of being final is Ψ_true(t,q+v). The event intensity and the conditional Markov construction therefore give the last-event density

\[
 j(t)=bE[Q_t\Psi_{\rm true}(t,Q_t+V_t)],\qquad -h'(t)=j(t)
\]

almost everywhere. This identity can first be integrated over a bounded time interval; the expected number of all events there is b times its length, so integrability is automatic. The envelopes give

\[
 j(t)\leq bE\frac{Q_t}{1+Q_t+V_t}
 \leq bE\frac{Q_t}{1+Q_t}\leq bh(t),
\]

which proves (12).

Together with the previous fractional-moment upper bound, this yields

\[
 h(0)e^{-bt}\leq h(t)\leq
 E\sqrt{Q_0}\,e^{-\kappa bt},\qquad\kappa=3-2\sqrt2.
 \tag{13}
\]

In particular,

\[
 E e^{rL}<\infty\quad(0<r<\kappa b),\qquad
 E e^{rL}=\infty\quad(r\geq b).
 \tag{14}
\]

The first assertion is inherited from the source note. The second follows from the tail integral formula and h(0)>0. The interval κb≤r<b remains unresolved. No existence or value of an exact tail exponent is asserted.

The coefficient b in (12) is best as a universal instantaneous bound. Under equal splitting take Q=ε with probability 1−ε² and choose the other atom to enforce EQ=1; its value is of order ε^-2. Then h∼ε and E[QΨ(Q+V)]∼ε, so the ratio of the two tends to one. This sharpness concerns arbitrary initial laws, not a claimed long-time asymptotic for a fixed law.

## 7. Why a scalar power-law dissipation estimate cannot hold

The opposite inequality cannot be bounded uniformly away from zero using any positive power of h. More precisely, for every α>0,

\[
 \inf_{\mathcal L(Q):\,Q>0,\,EQ=1}
 \frac{E[Q\Psi(Q+V)]}{(E[1-\Psi(Q)])^\alpha}=0.
 \tag{15}
\]

For a proof, let ε↓0, choose δ_ε>0 smaller than every power of ε, and let

\[
 Q=\begin{cases}
 \delta_\varepsilon,&\text{probability }1-\varepsilon,\\
 R_\varepsilon=[1-(1-\varepsilon)\delta_\varepsilon]/\varepsilon,
 &\text{probability }\varepsilon.
 \end{cases}
\]

One choice is δ_ε=exp[-(log(1/ε))³]. Then h=Eg(Q)∼ε, whereas monotonicity gives

\[
 E[Q\Psi(Q+V)]\leq\delta_\varepsilon+\Psi(R_\varepsilon).
\]

For every integer K, the first K factors in (1) give

\[
 \Psi(R)\leq2^{K(K+1)/2}R^{-K}.
\]

Since R_ε∼ε^-1, the last bound is smaller than every prescribed power of ε by choosing K sufficiently large. This proves (15). Every member of the example has finite moments of all orders and is a valid positive two-point initial population law.

Thus an argument seeking h'≤−cbh^α with fixed c>0 and α>0 for all initial distributions cannot succeed. This does not contradict the global exponential upper bound with an initial fractional-moment prefactor: that estimate uses more distributional information than h alone.

## 8. Explicit conditional large-size asymptotics

The equal-split no-future-event probability has a sharply described conditional tail, distinct from the unresolved time tail h(t). For q≥1, write a=log_2q=n+θ, where n is an integer and 0≤θ<1. Then

\[
 \log\Psi(q)=-\frac{(\log q)^2}{2\log2}+\frac12\log q-P(\theta)+R(q),
 \qquad0\leq R(q)\leq2/q,
 \tag{16}
\]

where

\[
 P(\theta)=\frac{\log2}{2}(\theta-\theta^2)
 +\sum_{j=0}^{\infty}\log(1+2^{-j-\theta})
 +\sum_{\ell=1}^{\infty}\log(1+2^{\theta-\ell}).
\]

The uniformly convergent sums define a bounded continuous function whose endpoint values at zero and one agree, giving a periodic correction on log_2q. To derive (16), split the log product in (1) at k=n, factor out q/2^k from the first n terms, and complete their remaining sum to infinity. The omitted tail is

\[
 R(q)=\sum_{j=n}^{\infty}\log(1+2^{-j-\theta})\leq2/q.
\]

In particular, Ψ(q) decreases faster than every inverse power of q, with leading log-square exponent. This calculation is an elementary asymptotic property of a classical q-product and is not proposed as a new special-function result.

A simpler finite-product certificate is often sufficient. For
\(P_K(q)=\prod_{k=1}^K(1+q/2^k)^{-1}\),

\[
 P_K(q)e^{-q/2^K}\leq\Psi(q)\leq P_K(q).
 \tag{17}
\]

If q/2^K<1, the weaker lower bound P_K(q)(1−q/2^K) uses only rational operations when q is rational. It can certify the overlap constant or conditional probabilities without an uncontrolled truncation of the product.

The [standard-library verification script](../verification/last_coagulation_exact.py) applies this rational bound with K=128 and outward decimal rounding. It certifies

\[
 0.580577558204892402290043892297
 <c_*<0.580577558204892402290043892298.
\]

The [saved JSON](../verification/last_coagulation_exact.json) also contains floating-point evaluations of the two-point dissipation counterexample. Those examples illustrate the proof and are explicitly separated from the rationally certified constant.

## 9. Novelty and review boundaries

The primary source identified above contains the exact exponential functional and Laplace product. The killed-process comparison uses established convexity and martingale arguments. No claim is made that either tool or the conditional q-product asymptotic is new.

The retained candidate applications are the sharp daughter-law envelopes for future coagulation, optimal overlap constants, the nonlinear tail-density observable, the universal lower calendar-time tail bound, and the failure of scalar power-law dissipation closure. Searches on 2026-09-07 included “Poissonian exponential functionals,” “geometric exponential sum q-Pochhammer,” and “q-exponential infinite product asymptotic.” A specific literature comparison for these coagulation applications remains necessary.

An independent reviewer checked every new formula and the counterexamples, then read the complete manuscript. Its report is [last-coagulation-exact-review.md](../reviews/last-coagulation-exact-review.md). The parent note's general controlled-clock theorem has its own review. The distinction between an auxiliary number-weighted process and a physical tagged particle must be retained in any manuscript or application.
