Focused audit of controlled additive coagulation and the last-collision bound

Date: 2026-09-07. This independent audit concerns [controlled-additive-trajectories.md](../results/controlled-additive-trajectories.md) and the proposed conditional bound on future coagulation. It supplements [the general pathwise audit](general-additive-path-literature.md). It is not a priority certification or an exhaustive literature review. No inspected source gives the stated controlled, parent-dependent, number-sampled last-collision estimate. The estimate uses familiar killing and first-jump ideas; the model-specific content lies in the exact normalization and the quantitative decay of fractional sampling moments.

Write `b(t)=mλ(t)`, `B_c(t)=∫₀ᵗb`, `F(t)=∫₀ᵗσ`, `N(t)=N₀exp(F(t)−B_c(t))`, and `Q_t=N(t)X_t/m`. The auxiliary number process fragments at rate `2σ(t)` with daughter kernel `b_{t,x}/2` and coagulates at rate `b(t)Q_t`. The daughter kernel may depend on parent size and time, but its conditional mean daughter size is always `x/2`. The moment estimate is

```math
\mathbb E Q_t^p=\mathcal A_p(t)
\le\mathcal A_p(0)
 e^{-(1+p-2^p)B_c(t)-(2-p-2^{1-p})F(t)},\qquad 0<p<1.
```

The preceding equality follows from the number marginal and is not an extra probabilistic hypothesis.

The proposed first-event argument checks algebraically and admits a simple strengthening. This calculation is the reviewer's deduction, not a theorem found in a source. Starting from `X_t=x`, construct the fragmentation-only future `V_s`, using the same parent-dependent fragmentation kernel, and suppress coagulation. Up to the first accepted coagulation, this agrees with the full process. Its conditional mean is

```math
\mathbb E_{t,x}V_s=x e^{-[F(s)-F(t)]}.
```

Boundedness `V_s≤x` and local integrability of `σ` justify this mean identity on finite intervals without logarithmic or higher-moment assumptions. Conditional on the fragmentation-only path, the no-coagulation probability is the usual exponential of integrated hazard. Thus, if `L` is the last auxiliary coagulation time,

```math
\mathbb P(L>t\mid X_t=x)
=1-\mathbb E_{t,x}e^{-H_t},\qquad
H_t=\int_t^\infty\lambda(s)N(s)V_s\,ds.
```

The event on the left means at least one coagulation strictly after `t`; this identity does not condition on `L` itself. Tonelli gives

```math
\mathbb E_{t,x}H_t=\frac{N(t)x}{m}I_t,\qquad
I_t=1-e^{-[B_c(\infty)-B_c(t)]}\in[0,1].
```

For infinite remaining activity take `I_t=1`. Jensen's inequality therefore yields

```math
\mathbb P(L>t\mid X_t=x)
\le 1-e^{-I_tN(t)x/m}
\le \min\{1,I_tN(t)x/m\}.
```

The first inequality is exact when fragmentation is absent after `t`, because then `V_s=x` and `H_t` is deterministic. This makes clear that the state bound belongs to standard integrated-hazard estimation, not a new general result about killed Markov processes. The important cancellation is that the fragmentation contribution to `N(s)` cancels the mean decay of `V_s`.

For a useful scalar improvement define

```math
c_p=\sup_{q>0}\frac{1-e^{-q}}{q^p}<1.
```

The unique positive maximizer satisfies `q/(e^q−1)=p`. Averaging the conditional bound gives

```math
\mathbb P(L>t)
\le c_p I_t^p\mathcal A_p(0)
 e^{-(1+p-2^p)B_c(t)-(2-p-2^{1-p})F(t)}.
```

Dropping `c_pI_t^p` recovers the proposed bound. These are exponential estimates in cumulative activity; they are exponential in calendar time only when the controls provide corresponding growth of cumulative activity. The refined bound proves a finite last event without using the finite-log-correction theorem: if `B_c(∞)=∞`, its coagulation exponent tends to infinity; if `B_c(∞)<∞`, then `I_t→0`. In either case `P(L>t)→0`. A separate proof review should check the filtration and coupling construction before this shorter argument replaces the existing proof.

The primary sources inspected for this focused comparison are as follows.

1. Jean Bertoin and Alexander R. Watson, *A probabilistic approach to spectral analysis of growth-fragmentation equations*, Journal of Functional Analysis 274 (2018), 2163–2204, [accepted manuscript](https://pure.manchester.ac.uk/ws/portalfiles/portal/66369837/gfe_fk_version_sent_at_resubmission.pdf), [DOI](https://doi.org/10.1016/j.jfa.2018.01.014). Inspected Section 2, the kernel transformation, Lemma 2.2 and its proof, and the introduction's description of later change-of-measure and exponential convergence results. They explicitly connect parent-dependent growth-fragmentation kernels to a size-biased Markov process by Feynman–Kac and many-to-one formulas. Exponential functionals and martingale changes of measure are established tools in this area. Their equation is linear growth-fragmentation, with no additive binary-coagulation background or last-coagulation observable. Their exponential convergence to a spectral profile is not the proposed tail estimate.

2. Robert Knobloch and Andreas E. Kyprianou, *Survival of homogeneous fragmentation processes with killing*, Annales de l'Institut Henri Poincaré, Probabilités et Statistiques 50 (2014), 476–491, [full author-hosted article](https://warwick.ac.uk/fac/sci/statistics/staff/academic-research/kyprianou/KK2014.pdf), [DOI](https://doi.org/10.1214/12-AIHP520). Inspected the killing definition in Section 1.2, Theorems 2–4, and the martingale/tilting preliminaries. Their fragments are killed on crossing an exponential space-time barrier; their questions concern extinction of the whole killed fragmentation and the largest surviving fragment. The present construction instead uses soft killing of one auxiliary path at its first coagulation, with rate `λ(t)N(t)x`. The objects, sampling, and killing mechanisms differ. The source confirms that fragmentation survival probabilities and exponential-rate arguments have a substantial prior literature; it does not contain the present nonlinear moment-to-tail implication.

3. Denis Villemonais, *General approximation method for the distribution of Markov processes conditioned not to be killed*, ESAIM: Probability and Statistics 18 (2014), 441–467, [primary full article](https://www.esaim-ps.org/articles/ps/pdf/2014/01/ps130045.pdf), [DOI](https://doi.org/10.1051/ps/2013045). Inspected the primary abstract and introductory distinction between hard and soft killing. The paper treats general killed processes and particle approximations of conditional distributions, including time- and environment-dependent settings. It explicitly gives reaction with a concentration-dependent exponential clock as an example of soft killing. This is direct methodological context for stopping at the first coagulation, but the inspected material does not state the specific bound or address additive-coagulation last-event tails. Its full technical results were not audited for this task.

4. Christophe Giraud, *Gravitational clustering and additive coalescence*, Stochastic Processes and their Applications 115 (2005), 1302–1322, [author manuscript](https://www.imo.universite-paris-saclay.fr/~christophe.giraud/publis/article7.pdf), [DOI](https://doi.org/10.1016/j.spa.2005.03.006). Inspected the primary abstract and initial model description. The paper relates one-dimensional gravitational sticky-particle dynamics to additive coalescence and discusses prior results on last collision times. Those collisions concern aggregation of spatial systems and their hydrodynamic limits. They are not future collisions of the normalized auxiliary number process with arbitrary binary fragmentation. This is a useful warning that “last collision in additive coagulation” is not itself an unexplored phrase or observable.

The full Deaconu–Fournier–Tanré (2002) source and the additive Borel formula were inspected in the preceding audit. Their distinctions remain decisive: the physical mass tag has additive-coagulation intensity `λN(t)x+b(t)`, whereas the auxiliary number process has `λN(t)x`. A last-collision claim for the latter cannot be restated as physical cessation along a uniformly tagged mass element. Parent-dependent daughter kernels are standard in fragmentation theory. Here their significance is that the estimate uses only their mean, allowing a bound uniform across that class.

The classical monodisperse pure-additive endpoint provides a sharper adverse benchmark. Set `σ=0` and `λ=m=N₀=1`. The known number law is `η_t=Borel(1−δ)` with `δ=e^{-t}`. Its probability-generating function satisfies `G_a(z)=z exp(a(G_a(z)−1))`. The exact conditional no-future-coagulation probability is `exp(−δk)`, so

```math
h_t:=\mathbb P(L>t)=1-G_{1-\delta}(e^{-\delta}),
\qquad -\log(1-h_t)=\delta+(1-\delta)h_t.
```

The proper Borel limit implies `h_t→0`, and expansion of the last equation gives

```math
h_t\sim\sqrt{2}\,e^{-t/2}.
```

This last-tail calculation was derived during this audit from the established formula, not located verbatim in a paper. It shows that the moment bound's pure-coagulation exponent, at best `max₀<p<1(1+p−2^p)≈0.0861`, is conservative compared with the exact exponent `1/2`. The controlled bound should be described as a robust certificate, not a sharp universal last-event asymptotic. The Borel-law formula itself is recorded with its original attribution in [Bertoin (2009), equation (3)](https://www.numdam.org/article/AIHPC_2009__26_6_2073_0.pdf).

Finally, `E[number of coagulations through t]=B_c(t)` together with a small last-event tail indicates concentration of expected activity on rare trajectories. It does not by itself identify a burst-size distribution, burst duration, or temporal clustering law. A claim about “bursts” should specify the random variable and prove its distributional or conditional-moment bound. The familiar distinction between almost-sure finiteness and infinite expectation is not new probability theory.

Searches combined controlled/time-dependent coagulation, parent-dependent fragmentation, additive kernel, tagged and number-normalized processes, finite last collision, exponential tail, killing, Feynman–Kac, and rare events. Close primary sources were inspected to the extent stated above. Broad searches frequently returned blood-coagulation or unrelated partition results, so unsuccessful keyword searches provide limited evidence. The candidate contribution remains the explicit controlled nonlinear sampling-moment estimate and its application to pathwise cessation and quantitative last-event tails, with standard killing machinery and classical solvable endpoints separated from that claim.
