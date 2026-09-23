# Sharp daughter-law bounds for future auxiliary coagulation

Date: 2026-09-07. Status: theorem independently checked, with [full actual-file proof review complete](../reviews/sharp-daughter-extremality-proof.md). Publication priority is not established. The exponential functionals used below are classical objects. The candidate contribution is the sharp comparison over all parent- and time-dependent binary daughter laws within the additive model.

## 1. Statement and scope

Assume the existing mass-conserving weak solution and number-weighted auxiliary process in [the controlled trajectory theorem](controlled-additive-trajectories.md). In this note λ and σ are constant, b=mλ>0, and σ≥0. Expected daughters are positive, have total count two, and conserve parent mass. Their law may depend measurably on time and parent size.

The auxiliary process X has law n_t/N(t), where N(t)=N_0 exp((σ−b)t). It fragments at rate 2σ and coagulates at rate λN(t)X_t. Its daughter fraction Θ has conditional mean 1/2. This process represents number sampling; it is not a physical tagged material particle.

Restart the auxiliary Markov construction at a deterministic time t from X_t=x, and put q=N(t)x/m. Let g_t(q) be the probability of at least one later auxiliary coagulation under this restarted law. This defines g_t at every q>0, including states of zero η_t probability; it is also a version of the conditional probability for the original process. For each fixed t the conversion between x and q is one-to-one; parent dependence is included in g_t.

Write d=σ−b. For σ>0, let T be exponential with rate σ and P a Poisson process of rate 2σ. Define two nonnegative random variables

\[
 Z_{\rm ext}=b\int_0^T e^{ds}ds,
 \qquad
 Z_{\rm eq}=b\int_0^\infty e^{ds}2^{-P_s}ds.
\tag{1}
\]

For σ=0, define both variables to be 1. Both have expectation one. Their Laplace transforms are

\[
 w_{\rm ext}(q)=E e^{-qZ_{\rm ext}},\qquad
 w_{\rm eq}(q)=E e^{-qZ_{\rm eq}}.
\tag{2}
\]

Then, for every allowed daughter law and every q>0,

\[
 \boxed{\quad
 1-w_{\rm ext}(q)\le g_t(q)\le1-w_{\rm eq}(q).
 \quad}
\tag{3}
\]

Both bounds are sharp over this class. Equal splitting attains the upper bound. Selfsimilar fractions ε and 1−ε, each selected with probability 1/2, approach the lower bound as ε↓0. No zero-size daughter is admitted into the model.

Thus equal splitting maximizes the probability of a future auxiliary coagulation, while arbitrarily unequal binary splitting approaches its infimum. The comparison includes daughter rules that depend on the whole prescribed time and current parent size; no selfsimilarity assumption is imposed on the law being bounded.

## 2. Reduction to a killed fragmentation process

Until its next coagulation, the auxiliary process follows fragmentation alone. In the normalized coordinate Q_s=N(t+s)V_{t+s}/m, this process has deterministic drift dQ_s between fragmentation events, and multiplies by a fraction Θ at rate 2σ. Its conditional fraction mean is 1/2, so

\[
 E Q_s=q e^{-bs}.
\tag{4}
\]

The first future coagulation is killing at rate bQ_s. Therefore

\[
 1-g_t(q)=E\exp\left(-\int_0^\infty bQ_sds\right).
\tag{5}
\]

In particular the accumulated hazard is integrable, with expectation q. This first-event reduction is independent of the coagulation partner law. It remains valid when the actual process has infinitely many expected future coagulations.

The two benchmark hazards in (1) have mean one because

\[
 E Z_{\rm ext}=b\int_0^\infty e^{ds}e^{-\sigma s}ds=1,
 \qquad
 E Z_{\rm eq}=b\int_0^\infty e^{ds}e^{-\sigma s}ds=1.
\tag{6}
\]

Thus both transforms are convex, continuously differentiable on [0,∞), bounded by one, and satisfy

\[
 0\le1-w(q)\le q.
\tag{7}
\]

The extreme benchmark can be viewed as deterministic growth at rate d followed by a jump to zero at rate σ. This is a comparison process only. Equal splitting gives the second benchmark directly.

## 3. Generator comparison proves both bounds

First-step conditioning for the two benchmark processes gives, for q>0,

\[
 dq w_{\rm ext}'(q)+\sigma[1-w_{\rm ext}(q)]
 -bq w_{\rm ext}(q)=0,
\tag{8}
\]

\[
 dq w_{\rm eq}'(q)+2\sigma[w_{\rm eq}(q/2)-w_{\rm eq}(q)]
 -bq w_{\rm eq}(q)=0.
\tag{9}
\]

These equations also hold at σ=0 with w(q)=e^{-q}. They can equivalently be obtained by conditioning on the first exponential waiting time. The finite first moments in (6) justify the derivatives; no second moment of either benchmark is required.

For any convex w with w(0)=1, the binary daughter constraints give

\[
 w(q/2)\le E[w(q\Theta)\mid q]
 \le\tfrac12[1+w(q)].
\tag{10}
\]

The lower inequality is Jensen. The upper inequality follows from the chord joining 0 and q and the conditional mean EΘ=1/2.

Let L_s be the actual fragmentation-only generator in the Q coordinate; its jump distribution may depend on t+s and q. Equations (8)–(10) imply

\[
 (L_s-bq)w_{\rm ext}(q)\le0,
 \qquad
 (L_s-bq)w_{\rm eq}(q)\ge0.
\tag{11}
\]

Consequently, writing H_s=∫_0^s bQ_rdr,

\[
 e^{-H_s}w_{\rm ext}(Q_s)
 \quad\hbox{is a supermartingale},\qquad
 e^{-H_s}w_{\rm eq}(Q_s)
 \quad\hbox{is a submartingale}.
\tag{12}
\]

For completeness, finite-horizon compensation is justified directly: starting at fixed q, Q_s≤q exp(max(d,0)s), and the fragmentation clock has finite rate. All terms of the differentiated bounded test are then integrable. The processes in (12) are bounded between zero and one.

Equation (7) and the mean formula (4) show

\[
 E\left|e^{-H_s}w(Q_s)-e^{-H_s}\right|
 \le E Q_s=q e^{-bs}\longrightarrow0.
\]

Also e^{-H_s} converges boundedly to e^{-H_∞}. Taking expectations and then s→∞ in (12) gives

\[
 w_{\rm eq}(q)\le E e^{-H_\infty}\le w_{\rm ext}(q),
\]

which proves (3). This passage uses neither monotonicity of Q nor logarithmic moments.

## 4. Sharpness within positive daughter laws

Equal splitting gives Q_s=q exp(ds)2^{-P_s}, hence H_∞=qZ_eq. Its equality case is immediate.

For the extreme limit, take daughter fractions ε and 1−ε. The two marked clocks are independent Poisson processes of rate σ. Let T be the first ε-event, and let R_s count the (1−ε)-events. Up to T the hazard is

\[
 H_{\varepsilon}^{\rm pre}
 =bq\int_0^T e^{ds}(1-\varepsilon)^{R_s}ds
 \longrightarrow qZ_{\rm ext}\quad\hbox{in }L^1.
\tag{13}
\]

The convergence follows from a common clock construction and domination by qZ_ext, which is integrable. Immediately after T,

\[
 Q_T=q\varepsilon e^{dT}(1-\varepsilon)^{R_T}.
\]

The conditional mean remaining integrated hazard is Q_T, by (4). Moreover

\[
 E Q_T
 =q\varepsilon\sigma\int_0^\infty
 e^{-(b+\sigma\varepsilon)s}ds
 =\frac{q\varepsilon\sigma}{b+\sigma\varepsilon}
 \longrightarrow0.
\tag{14}
\]

Therefore the full hazard converges in L¹ to qZ_ext. Since z↦e^{-z} is Lipschitz on [0,∞), the survival probabilities converge to w_ext(q). At σ=0 there are no fragmentation events and both bounds are equalities for every daughter rule.

## 5. The optimal overlap coefficient

Let η_t=n_t/N(t) and π_t=xn_t/m. Since dπ_t/dη_t=Q_t,

\[
 O_t:=1-\|\eta_t-\pi_t\|_{\rm TV}=E\min(1,Q_t),
\]

where total variation is the supremum over measurable sets. The function 1−w_ext is increasing, concave, and zero at zero. Hence, with

\[
 c_{b,\sigma}=1-w_{\rm ext}(1)>0,
\tag{15}
\]

equation (3) and the elementary upper bound g_t(q)≤min(1,q) imply

\[
 \boxed{\quad
 c_{b,\sigma}O_t\le P(L>t)\le O_t.
 \quad}
\tag{16}
\]

The lower coefficient is the largest uniform coefficient over the stated class and all initial states: choose a monodisperse initial law, so Q_0=1 and O_0=1, and use the ε-family limit in section 4. This is sharpness of the overlap coefficient, not of a long-time exponential decay exponent.

At σ=0, Z_ext=Z_eq=1, so c_{b,0}=1−e^{-1}. At criticality σ=b,

\[
 w_{\rm ext}(q)=\frac1{1+q},\qquad
 w_{\rm eq}(q)=\prod_{k=1}^\infty(1+q/2^k)^{-1},
 \qquad c_{b,b}=\tfrac12.
\tag{17}
\]

The equal-split product follows by summing the independent exponential holding times at the successive values q,q/2,q/4,…. It is a classical exponential-functional expression: [Bertoin, Biane, and Yor, *Poissonian exponential functionals, q-series, q-integrals, and the moment problem for log-normal distributions*, equations (1.3) and (1.6)](https://monge.univ-eiffel.fr/~biane/q_poisson.pdf) give the underlying geometric exponential sum and its transform. Their I^(1/2)/2 has the law of Z_eq at criticality. Equations (3) and (17) provide the exact sharp conditional envelopes at criticality.

## 6. Caveats and relation to prior results

The theorem is conditional on the existing weak solution and its verified auxiliary representation. It introduces no additional solution-existence assertion. The benchmark with a zero daughter is used only in the comparison proof; sharpness is approached through admissible positive daughter laws.

The result bounds the event of a first future auxiliary coagulation. It does not order total coagulation counts, final masses, physical tagged-particle events, or the full reactor. It does not establish a scalar closed evolution equation for a sampled Laplace transform.

The general theory of exponential functionals of Lévy processes, killed-process representations, and convex generator comparison predates this note. The equal-split benchmark is a particular exponential functional. Those identities are not asserted to be new. See [the specialized critical note](last-coagulation-exact-equal-split.md) for its classical product-law attribution and further equal-split identities. The candidate new statement is the sharp extremal comparison over parent- and time-dependent binary daughter laws for this auxiliary representation, together with its optimal sampling-overlap coefficient. The completed [focused literature audit](../reviews/sharp-daughter-extremality-literature.md) found no exact match in its inspected primary sources, while recording close methodological precedents. Priority remains unresolved.
