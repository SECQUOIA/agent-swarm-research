# Independent review of quantitative last-coagulation tails

Date: 2026-09-07. Reviewer: `/root/inverse_direction`, with a separate algebraic and probabilistic check by `/root/inverse_direction/review_gauge`. This reviews the actual file [last-coagulation-tail.md](../results/last-coagulation-tail.md), including its overlap and window-count sections, and the auxiliary construction in [controlled-additive-trajectories.md](../results/controlled-additive-trajectories.md). This is a proof review, not an independent priority determination.

**Verdict:** the conditional survival estimate, controlled tail, almost-sure finite total coagulation count, future-path total variation approximation, sharp critical overlap comparison, and window-count moment inequalities are correct under the stated existing mass-conserving weak-solution and auxiliary-process assumptions. An initial wording issue in section 5 was corrected: both b>0 and σ≥0 are now explicitly constant when using the exponent γ_p. The final full file, including its strengthened factor 1/2, was checked by both reviewers. No logarithmic moment is needed.

## 1. The first-event construction is valid for parent-dependent daughters

Fix a deterministic t and condition on X_t=x. Put q=N(t)x/m. Run the fragmentation-only process V from x, with the prescribed time- and parent-dependent daughter kernel. The daughter mean is V/2 and the event rate is 2σ(s), so

\[
 E V_s=x\exp\left[-\int_t^s\sigma(r)dr\right],\qquad
 E\frac{N(s)V_s}{m}=q\exp\left[-\int_t^s b(r)dr\right].
\]

This calculation does not assume independent fraction marks. On each finite horizon V≤x, and the fragmentation clock has finite integrated rate. The bounded mean equation therefore follows directly by compensation and its scalar integrating factor.

Use an independent unit exponential variable to kill this path at hazard b(s)N(s)V_s/m. This reproduces the auxiliary process up to its first future coagulation. The partner law is irrelevant until that event. With

\[
 H=\int_t^T b(s)N(s)V_s/m\,ds,
 \qquad u=1-\exp\left[-\int_t^T b(s)ds\right],
\]

Tonelli gives EH=qu, including T=∞. In particular H is integrable for each finite q even when cumulative future coagulation activity is infinite. Consequently

\[
 P(J_T>J_t\mid X_t=x)=E(1-e^{-H})\le1-e^{-qu}\le\min(1,qu).
\]

The conditioning is justified by the auxiliary Markov construction with fresh future clock randomness. The daughter law can depend on absolute time and current size. Deterministic t is not a last-event stopping time. The argument makes no conditional independence assertion after the random last coagulation.

The equality at the first step and Jensen inequality concern the first coagulation only. They do not identify the total future compensator after coagulations resume. Its expectation can be infinite even though H has finite conditional expectation.

## 2. Fractional tails, finite last time, and sharp scalar facts

For 0<p<1, averaging the preceding inequality gives

\[
 P(J_T>J_t)\le u^pE Q_t^p
 \le u^p\mathcal A_p(0)
 e^{-a_pB_c(t)-a_{1-p}F(t)}.
\]

Here the nontrivial model input is the independently reviewed fractional-affinity estimate; the survival step alone does not prove separation of number and mass laws.

For T=∞, this proves finite last time without invoking the earlier finite-log-correction argument. If B_c(∞)=∞, the affinity estimate tends to zero. If B_c(∞)<∞, then u→0 and E Q_t^p≤1 by Jensen. Thus P(L>t)→0 in both cases. Finite-horizon nonexplosion then implies finitely many coagulations in total. This reasoning is not circular.

For constant b>0 and σ≥0, γ_p=b a_p+σ a_{1-p}>0. Tonelli applied to e^{rL}−1 yields the stated exponential-moment bound for 0<r<γ_p. It also implies every polynomial moment of L is finite. Activity-based estimates under controls do not imply a fixed calendar-time rate without additional control assumptions.

The optional scalar coefficient is correct:

\[
 c_p=\max_{z>0}\frac{1-e^{-z}}{z^p}<1.
\]

The ratio vanishes at both endpoints and its derivative changes sign exactly when z/(e^z−1)=p. This equation has one positive solution because its left side decreases continuously from 1 to 0. The coefficient is sharp for this scalar power domination; this does not establish a sharp model decay exponent.

If fragmentation vanishes after t, V is constant and H=qu is deterministic. The sharper conditional estimate 1−e^{-qu} is then exact. Averaging it and using E Q_t=1 gives the additional bound P(J_T>J_t)≤1−e^{-u}; it is exact from a monodisperse state with no subsequent fragmentation. This simple endpoint prevents a claim that the conditional Jensen estimate can be improved uniformly over the stated class.

## 3. The future-path claim has the correct initialization

Start the fragmentation-only comparison from the actual random X_t. Use common fragmentation clock times and common uniform innovations to sample the measurable daughter kernels. The paths coincide until the auxiliary process first coagulates. After divergence, each path uses its own current state in the prescribed daughter rule. This gives both correct marginals even for parent-dependent daughters.

The coupling inequality therefore bounds total variation of their entire path laws by P(J_T>J_t). It applies on finite horizons and on the usual infinite-horizon càdlàg path space. The comparison begins from η_t; it does not compare with pure fragmentation started from η_0. This distinction in the theorem is essential and correct.

## 4. Critical overlap and a constant-rate extension

The first version used a valid weaker factor 1/3, retained here to document a simple direct check. At b=σ>0, N is constant and Q does not change before an event. Competing rates bq and 2b give a first-event coagulation probability q/(2+q). This event is included in any future coagulation, regardless of the future daughter rules. Pointwise,

\[
 \frac{q}{2+q}\ge\frac13\min(1,q).
\]

Since dπ_t/dη_t=q, the standard overlap identity with total variation defined as a supremum over sets is

\[
 E\min(1,Q_t)=1-\|\eta_t-\pi_t\|_{\rm TV}.
\]

The claimed two-sided inequality follows. There is no missing factor two under the stated convention.

A further verified extension holds for every constant b>0 and σ≥0. Let T be the time of the first fragmentation after a deterministic start, T∼Exp(2σ), and put T=∞ when σ=0. Before that event, define

\[
 Z=\int_0^T b e^{(\sigma-b)s}ds,\qquad
 f(q)=E(1-e^{-qZ}).
\]

Then f(q) is the probability that coagulation occurs before the first fragmentation. It is increasing and concave with f(0)=0, so f(q)≥f(1)min(1,q). Direct integration gives

\[
 EZ=\frac{b}{b+\sigma},\qquad
 EZ^2=2b^2\int_0^\infty\!\int_0^s
 e^{(\sigma-b)(s+r)}e^{-2\sigma s}\,dr\,ds
 =\frac{b}{b+\sigma}.
\]

Using 1−e^{-z}≥z−z²/2 proves

\[
 \frac{b}{2(b+\sigma)}\bigl(1-\|\eta_t-\pi_t\|_{\rm TV}\bigr)
 \le P(L>t)\le1-\|\eta_t-\pi_t\|_{\rm TV}.
\]

The sharper coefficient f(1) is available without this second-moment estimate. At criticality f(1)=1/3; at σ=0, Z=1 and f(1)=1−e^{-1}. These identities verify the two endpoints. This extension uses only the rates before the first fragmentation and remains valid for parent-dependent daughter rules.

### Sharp critical improvement

The root agent subsequently proposed a stronger critical comparison. Its following independent verification upgrades the factor 1/3 above to the optimal uniform factor 1/2.

For b=σ>0, let Q_s denote the fragmentation-only process starting at q at the conditioning time. Let w(q)=1/(1+q). Convexity gives the chord bound

\[
 E[w(q\Theta)\mid q]\le\tfrac12(1+w(q)),
\]

because 0<Θ<1 and its conditional mean is 1/2. This bound holds at every time and state. Therefore the killed generator satisfies

\[
 (L_{\rm frag}-bq)w(q)
 =2bEw(q\Theta)-(2b+bq)w(q)\le0.
\]

Thus exp(−∫_0^s bQ_r dr)w(Q_s) is a bounded supermartingale. Pure fragmentation gives Q_s↓0 almost surely: it is nonincreasing and E Q_s=q e^{-bs}→0. Dominated convergence consequently gives

\[
 \Psi(q):=E\exp\left(-\int_0^\infty bQ_sds\right)
 \le\frac1{1+q}.
\]

The conditional probability g(q) of any future coagulation satisfies

\[
 \frac{q}{1+q}\le g(q)\le1-e^{-q}.
\]

In particular,

\[
 \tfrac12(1-\|\eta_t-\pi_t\|_{\rm TV})
 \le P(L>t)\le1-\|\eta_t-\pi_t\|_{\rm TV}.
\]

The lower conditional function and the factor 1/2 are sharp over the class of positive binary daughter laws. To verify this claim, take the selfsimilar daughter fractions ε and 1−ε, with each selected with probability 1/2. The marked clock splits into independent clocks of rate b for these two fractions. Let T be the first ε-event, so T∼Exp(b). Before T,

\[
 H_{\varepsilon}^{\rm pre}=bq\int_0^T(1-\varepsilon)^{P_s}ds
 \longrightarrow bqT\quad\hbox{in }L^1,
\]

where P is the independent rate-b clock; domination by bqT justifies the limit. Immediately after T, Q_T≤qε. The conditional expected remaining hazard equals Q_T, by the first-event mean calculation, so its expectation is at most qε. Hence the full hazard converges in L¹ to bqT, and

\[
 \Psi_\varepsilon(q)\longrightarrow E e^{-bqT}=\frac1{1+q}.
\]

At a monodisperse initial state, q=1 and the number–mass overlap is one. The future-coagulation probability therefore tends to 1/2, excluding any larger uniform lower overlap coefficient. Each approximating law has strictly positive daughters; the limiting zero-size daughter is used only to describe a limit and is not admitted into the model. This argument verifies sharpness at an endpoint of the allowed family, not attainment by a positive daughter law.

## 5. Rare window counts and higher moments

For constant b>0 and constant σ≥0, fix h>0 and D_t=J_{t+h}−J_t. The auxiliary coagulation intensity is bQ_s, whose expectation is b. Compensation and Tonelli therefore give E D_t=bh exactly, without a second moment. Almost-sure finite last time implies D_t=0 for every sufficiently large t on each path. Hence these counts are not uniformly integrable.

Set d_p=(1−e^{-bh})^p\mathcal A_p(0)>0. The window form of the first-event estimate gives P(D_t>0)≤d_p e^{-γ_pt}. Since E D_t=bh>0, this event has positive probability, and

\[
 E[D_t\mid D_t>0]=\frac{bh}{P(D_t>0)}
 \ge\frac{bh}{d_p}e^{\gamma_pt}.
\]

For r>1, Hölder on the event D_t>0 gives

\[
 bh\le (E D_t^r)^{1/r}P(D_t>0)^{1-1/r},
\]

which rearranges to the stated lower bound

\[
 E D_t^r\ge(bh)^r d_p^{1-r}e^{(r-1)\gamma_pt}.
\]

If the rth moment is infinite, the inequality remains correct in the extended sense. These results quantify increasingly large conditional event counts on rare auxiliary paths. They do not establish a burst-size limit law or a temporal clustering law.

## 6. Scope and novelty limits

All statements concern the number-weighted auxiliary representation, not a physical mass-tagged particle and not aggregate reactor event counts. General measurable parent-dependent daughters retain the assumed existing global mass-conserving solution; the tail calculation does not establish existence or uniqueness.

The separate [literature audit](controlled-last-collision-literature.md) records an exact pure-additive monodisperse benchmark from the known Borel solution. Its equation −log(1−h)=δ+(1−δ)h, δ=e^{-t}, implies h∼√(2δ). This algebra confirms that the general affinity-derived pure-coagulation decay exponent need not be optimal. The review has not independently repeated that source search. Killing clocks, Jensen, total variation coupling, overlap identities, and Hölder are standard; a publication claim must concern the verified model-specific combination and survive the separate priority audit.
