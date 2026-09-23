# Prior-art audit: weak surface diffusion near slow exchange points

Audit date: 2026-09-06. This note reviews the candidate in [exploration-interfaces.md](exploration-interfaces.md). It is an independent literature audit, not a proof of mathematical correctness or an exhaustive certification of novelty.

The strongest surviving candidate is a **transport asymptotic for smooth, nearly inactive exchange points at constant affinity**, including its surface-diffusion cutoff and prefactor. Neither anomalous dispersion from distributed trapping times, nor the harmonic-oscillator kernel used to compute the cutoff, should be presented as new. I found no openly accessible source giving the specific channel result below, but important older chromatography papers were accessible only through their abstracts.

## Candidate and claim boundaries

Write adsorption and desorption coefficients as \(k_a(s)=Kk_d(s)\), with constant finite \(K\), and suppose an isolated minimum satisfies \(k_d(s)=\delta+as^2+o(s^2)\). The proposed leading singular contribution is

\[
D_{\rm flow}\sim \frac{KV^2}{Z}D_s^{-1/4}a^{-3/4}
\mathcal C\!\left(\frac{\delta}{\sqrt{aD_s}}\right),\qquad
\mathcal C(z)=\frac\pi2\frac{\Gamma((z+1)/4)}{\Gamma((z+3)/4)}.
\]

Here \(Z=A+KP\), and \(V\) is the stationary mean axial speed. Constant affinity keeps the equilibrium occupation finite and independent of the exchange-rate landscape. This is kinetic heterogeneity, not a divergent equilibrium binding weight.

| Component | Audit assessment |
|---|---|
| Adsorption/desorption and lateral surface diffusion alter Taylor dispersion | Established for decades. |
| Distributed desorption rates generate memory and anomalous dispersion | Established multirate mass transfer and continuous-time random walk theory. |
| Finite mean trapping time with infinite second moment gives superlinear spreading under bias | Established. Finite equilibrium adsorption does not itself make this surprising or new. |
| \(t^{3/2}\) variance at a quadratic kinetic zero when \(D_s=\delta=0\) | Specific geometric realization of a known renewal universality class. A useful deduction, weak standalone novelty. |
| Stationary variance twice the initially mobile coefficient in that limit | Known initialization dependence of biased renewal processes; the factor two is the \(\alpha=3/2\) case of an established formula. |
| Quadratic killing yields a Mehler kernel, hyperbolic survival function, and gamma-function resolvent integral | Classical oscillator calculation; explicitly used for killed diffusion in modern primary literature. |
| Weak lateral surface diffusion gives \(D_s^{-1/4}\), with the stated \(\delta/\sqrt{aD_s}\) crossover and transport prefactor | No exact collision located. Plausible applied-theory contribution if proved for the coupled channel, with assumptions and asymptotic regime explicit. |
| Full bounded bulk changes this leading singular contribution only by a bounded remainder | Potentially the strongest theorem. Literature search does not establish its correctness; the uniform estimates require independent proof. |

## Closest transport precedents

**Dill and Brenner (1982), “A general theory of Taylor dispersion phenomena: III. Surface transport,” J. Colloid Interface Sci. 85, 101–117.** The publisher abstract explicitly includes adsorption, surface diffusion, and convection along the bounding surface in generalized Taylor dispersion. Therefore the combined bulk/surface framework is established. I did not obtain openly accessible full text, so cannot exclude a singular-limit result from the abstract alone. Bibliographic correction: the authors are **Loren H. Dill and Howard Brenner**, not Brenner alone. [Publisher record](https://www.sciencedirect.com/science/article/abs/pii/0021979782902399), [DOI](https://doi.org/10.1016/0021-9797(82)90239-9).

**Levesque et al. (2012), “Taylor Dispersion with Adsorption and Desorption,” Phys. Rev. E 86, 036316.** A stochastic treatment gives dispersion under steady and oscillatory flows, with explicit canonical channel examples. Its uniform-rate formulas already contain kinetic dispersion. The term “heterogeneous” reaction in this context must not automatically be read as a spatially vanishing desorption-rate field. I found no quadratic kinetic zero or weak lateral-diffusion crossover in the inspected manuscript. [Open manuscript](https://arxiv.org/html/1211.5224).

**Haggerty and Gorelick (1995), “Multiple-rate mass transfer for modeling diffusion and surface reactions in media with pore-scale heterogeneity,” Water Resour. Res. 31, 2383–2400.** Continuously distributed exchange rates between mobile and immobile domains are the direct background for the \(D_s=0\) reduction. The reduced channel model can be viewed as a particular capacity distribution over rate constants. A smooth coordinate labeling immobile states does not by itself change that equivalence. Lateral diffusion between those states is the additional structure in the present candidate. [Author-posted full paper](https://www.researchgate.net/profile/Steven-Gorelick/publication/262380391_haggerty_95WR10583/links/0c96053798e5f5e28a000000/haggerty-95WR10583.pdf), [DOI](https://doi.org/10.1029/95WR10583).

**Dentz (2003), “Transport behavior of a passive solute in continuous time random walks and multirate mass transfer,” Water Resour. Res.** The comparison includes temporal transport moments and broad waiting-time distributions. A truncated power law crosses from anomalous behavior to eventual Fickian spreading, so eventual regularization by a cutoff is also established. The prospective distinction is a cutoff derived from spatial lateral diffusion, together with its geometric exponent and complete crossover function. [Primary article](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2001WR001163).

**Gryczak et al. (2024), “Non-Markovian Diffusion and Adsorption–Desorption Dynamics: Analytical and Numerical Results,” Entropy 26, 294.** Full text inspected. The paper combines lateral surface diffusion, adsorption/desorption memory kernels, and heterogeneous bulk diffusivity. Section 1 specifies that inhomogeneity is only in the bulk; equation (3) has spatially uniform surface kernels. It therefore overlaps the broad modeling ingredients but does not give spatially degenerate surface exchange or the proposed small-\(D_s\) law. [Open institutional PDF](https://iris.cnr.it/retrieve/97d03450-2b3c-4248-be97-0e0ebd9b4c3b/entropy-26-00294.pdf), [DOI](https://doi.org/10.3390/e26040294).

**Krouskop and McGuffin (2002), “Stochastic simulation of the partition mechanism with a heterogeneous surface phase,” J. Chromatogr. A 959, 49–64.** The accessible abstract describes heterogeneous surface phases through partition coefficients, diffusion coefficients, and interfacial resistance. Thus independently varying thermodynamic partitioning and kinetic resistance has chromatography precedent. Full text was not available in this audit; this remains an important unresolved collision check. [DOI](https://doi.org/10.1016/S0021-9673(02)00427-2).

**Gortel and Turski (1991), “Diffusion of desorbing adsorbate: Study of a mesoscopic model,” Phys. Rev. B 43, 4598.** The primary abstract treats lateral diffusion and desorption on inequivalent sites using a master equation. This is a close conceptual precedent for coupled surface motion and heterogeneous escape. The abstract does not establish the particular smooth-degeneracy asymptotic. [Publisher abstract](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.43.4598).

**Cerofolini and Re (1997), “Kinetics of Desorption from Heterogeneous Surfaces,” Langmuir 13, 990–994.** Nonexponential aggregate desorption from heterogeneous local kinetics is established. The present claim should concern the spatially resolved exchange bottleneck and its regularization rather than discovery of broad desorption times. [Primary article](https://doi.org/10.1021/la950813e).

Recent experimental-method context also recognizes kinetic contributions from heterogeneous adsorption: “Preventing the impact of solute adsorption in Taylor dispersion analysis: Application to protein and lipid nanoparticle analysis” attributes adsorption broadening to older chromatographic theory and discusses replacing uniform inverse desorption rates by an adsorption-duration statistic. This reinforces the need to cite chromatography rather than frame kinetic Taylor dispersion as a new mechanism. Its search-accessible publisher text did not contain the small-surface-diffusion asymptotic. [Publisher article](https://www.sciencedirect.com/science/article/abs/pii/S002196732400699X).

## Why the zero-diffusion anomaly and factor two are not strong novelty

Let \(J=\int_\Gamma k(s)\,ds\). For the reduced well-mixed model at \(D_s=0\), an adsorption event selects its location with density \(k(s)/J\), whereas stationary adsorbed locations are uniform. Consequently the waiting-time density for a newly begun adsorbed interval is

\[
\psi(t)=J^{-1}\int_\Gamma k(s)^2e^{-k(s)t}\,ds.
\]

At one quadratic zero, direct Gaussian integration gives

\[
\psi(t)\sim\frac{3\sqrt\pi}{4J\sqrt a}\,t^{-5/2}.
\]

This has finite mean and infinite second moment. In the conventional notation \(\psi(t)\sim t^{-1-\alpha}\), the index is \(\alpha=3/2\). Standard biased renewal transport gives variance proportional to \(t^{3-\alpha}=t^{3/2}\). Starting in stationary internal conditions samples residual intervals differently from a fresh mobile injection.

**Akimoto, Cherstvy, and Metzler (2018), “Enhancement, slow relaxation, ergodicity and rejuvenation of diffusion in biased continuous-time random walks,” Phys. Rev. E 98, 022105**, explicitly calculates ordinary versus equilibrium preparation. In the anomalous regime, the equilibrium leading spreading coefficient is enhanced by \((\alpha-1)^{-1}\). This is exactly two at \(\alpha=3/2\). The channel coefficients can still be worth deriving and checking, but the coefficient ratio is an application of this known mechanism. [Open primary manuscript](https://arxiv.org/pdf/1803.07232).

For higher-order zeros \(k\sim a|s|^m\), the same local argument yields \(\psi(t)\sim t^{-2-1/m}\), hence \(\alpha=1+1/m\) and the existing renewal exponent \(2-1/m\). Those exponents should not be marketed as a new family of anomalous-transport universality classes. Deriving which smooth exchange geometry realizes them is a narrower contribution.

## Exact local oscillator: established ingredient

**Mazzolo and Monthus (2022), “Conditioning diffusion processes with killing rates.”** Section V explicitly studies pure diffusion with killing \(k(x)=\gamma x^2\). Equations (73)–(75) identify the harmonic-oscillator generator, and the subsequent propagator and survival calculation use the Mehler kernel. In dimension one and rescaled units \(D=\gamma=1\), their survival from location \(x\) is

\[
S(t|x)=(\cosh 2t)^{-1/2}\exp[-x^2\tanh(2t)/2].
\]

Integrating over \(x\) immediately gives

\[
\int_{\mathbb R}S(t|x)\,dx=\sqrt{\frac{2\pi}{\sinh 2t}}.
\]

Adding constant killing \(z\), integrating in time, and substituting \(q=e^{-4t}\) gives the candidate gamma quotient. Thus the local kernel and special-function evaluation are conventional consequences of an explicitly published killed-diffusion solution. [Open primary paper](https://arxiv.org/pdf/2204.05607).

What is not supplied by that oscillator solution is a proof that the coupled adsorption/bulk-diffusion system has the same leading singular contribution, the value of the channel prefactor, or the error under a local approximation to a globally bounded heterogeneous boundary. Those are the appropriate theorem targets.

## Search scope and remaining work

Searches covered combinations of heterogeneous adsorption and chromatography, multirate mass transfer, power-law mobile/immobile waiting times, surface-mediated diffusion, degenerate or vanishing desorption rates, lateral surface diffusion, kinetic disorder, and diffusion with quadratic killing. Searches also included the literal quarter-power scaling and harmonic-oscillator resolvent connection. No source located in this audit states the specific \(D_s^{-1/4}\) channel dispersion crossover above.

This negative search result is provisional. The highest-priority gaps are full-text inspection of Dill–Brenner (1982), Krouskop–McGuffin (2002), Gortel–Turski (1991), and older stochastic chromatography treatments cited by later papers. General small-noise resolvent asymptotics could also contain the mathematical local scaling without a transport interpretation.

A defensible manuscript claim would be: “We derive the singular effect of weak lateral surface diffusion near smooth kinetic exchange minima at fixed adsorption affinity, including the dispersion prefactor, the finite-minimum-rate crossover, and conditions under which bounded bulk transport affects only lower-order terms.” It should explicitly identify multirate trapping, preparation dependence, and the Mehler kernel as established tools. Calling the resulting theorem publishable still requires the independent mathematical verification recorded separately in the repository.
