# Prior-art audit: random kinetic zeros and disorder moments

Literature audit, 2026-09-07. This note assesses novelty of [random-kinetic-barriers.md](random-kinetic-barriers.md). Mathematical verification is recorded separately in [review-random-kinetic-barriers.md](review-random-kinetic-barriers.md).

## Assessment

I found no openly accessible paper deriving the stated disorder-moment asymptotics for the compact periodic operator

\[
H_{D,c}=-D\partial_s^2+(c+\cos s)^2,
\qquad c\sim\mathrm{Uniform}[-2,2],
\qquad J_{D,c}=\langle1,H_{D,c}^{-1}1\rangle.
\]

The specific result remains a plausible original contribution: coalescing kinetic zeros produce a transition at moment order `q=4/3`, with low moments governed by ordinary simple zeros and high moments governed by the shrinking neighborhoods of `c=±1`. The resulting mean and variance have different small-diffusivity powers. Its surface-exchange interpretation is also not present in the sources inspected.

The broad mechanism is established. Parameter averaging of singularities, rare bifurcations dominating high moments, fractional moment spectra, and their derivation by balancing enhancement against parameter-space volume all have close prior art. The local quartic operator and semiclassical rescaling are classical tools. A defensible contribution is therefore the specific positive-resolvent theorem and its quantitative transport consequence, supported by uniform estimates; it is not a new general theory of rare-event scaling.

## Exact statement being compared

For positive `q`, the candidate powers are

\[
\mathbb E[J_D^q]\asymp
\begin{cases}
D^{-q/4},&q<4/3,\\
D^{-1/3}\log(1/D),&q=4/3,\\
D^{1/3-q/2},&q>4/3.
\end{cases}
\]

The research note gives leading constants, including the quartic resolvent integral

\[
\mathcal C(\mu)=\left\langle1,
[-\partial_y^2+(y^2-\mu)^2]^{-1}1\right\rangle,
\qquad
\mathbb E[J_D^q]\sim
2^{q-4/3}D^{1/3-q/2}\int_{\mathbb R}\mathcal C(\mu)^q\,d\mu
\quad(q>4/3).
\]

Consequently the proposed mean scales as `D^(-1/4)`, the variance as `D^(-2/3)`, and the squared coefficient of variation as `D^(-1/6)`. The reported variance prefactor `62.78994` is a numerical estimate of the stated integral, not a certified exact numerical constant.

These are disorder moments across fixed-amplitude walls. They are not displacement moments over time, and they do not establish a thermodynamic-limit failure of self-averaging. For each positive `D`, the compact family has finite moments. The Gaussian example in the research note, where the overall amplitude can approach zero, has an infinite mean for every `D`; it correctly prevents extending the theorem to arbitrary smooth Gaussian fields.

## Closest conceptual collision: bifurcation-dominated moments

Berry, Keating and Schomerus, *Universal twinkling exponents for spectral fluctuations associated with mixed chaology* (2000), study parameter-averaged moments of quantum spectral fluctuations. Equations (18)–(19) explicitly weigh the enhanced amplitude near a bifurcation against its shrinking parameter-space volume and select the largest resulting moment exponent. Different singularity classes can dominate different moments; logarithmic factors are also discussed. The observables are oscillatory spectral-counting fluctuations, not the positive integrated inverse considered here. Nevertheless, their reasoning directly anticipates the general organizing principle of the candidate. [Open author PDF](https://www.lorentz.leidenuniv.nl/beenakkr/mesoscopics/fulltext/schomerus00.pdf), [published article](https://doi.org/10.1098/rspa.2000.0580).

Keating, Ozorio de Almeida, Prado, Sieber and Vallejos, *Periodic orbit bifurcations and scattering time delay fluctuations* (2007), extend this idea to the Wigner time delay in open quantum systems. Their introduction and Section 4 explain moment-dependent rational powers arising from trapped periodic-orbit bifurcations. This is a particularly close conceptual comparator because it concerns a lifetime-related observable in an open transport problem. It does not give the killed-diffusion operator, the cosine-offset ensemble, the positive quartic source problem, or the `4/3` transition above. [Open paper](https://arxiv.org/pdf/nlin/0701025), [published article](https://doi.org/10.1143/PTPS.166.10).

For the present family the same established bookkeeping is especially simple: a fold has response size `D^(-1/2)` and parameter probability of order `D^(1/3)`, so its moment contribution has order `D^(1/3-q/2)`. The ordinary-zero contribution has order `D^(-q/4)`. Their powers cross at `q=4/3`. This argument predicts the exponents; establishing convergence and the constants requires the uniform operator estimates in the research note.

## Power-law tails and piecewise moment spectra

Vollmer, Giberti, Orchard, Reinhard, Mejía-Monasterio and Rondoni, *Universal hyper-scaling relations, power-law tails, and data analysis for strong anomalous diffusion* (2024 preprint), analyze how matching distribution bulk and tails yields piecewise-linear displacement-moment spectra. This provides a current primary discussion of the established tail-matching mechanism and of substantial preasymptotic errors. It is not a theorem about quenched wall-to-wall variation or elliptic resolvents. [Open paper](https://arxiv.org/abs/2412.20590).

The limiting marked-zero law in the research note follows directly from Kac–Rice size bias: a Gaussian zero has a Rayleigh-distributed absolute slope, and the transport mark is its inverse `3/2` power. The `4/3` tail then follows by a change of variables. Neither Kac–Rice nor this one-variable transformation should be presented as new. The substantive additional step is showing how finite surface diffusivity rounds close zero pairs and changes the actual finite-`D` ensemble moments.

Avoid describing the result as evidence of anomalous particle motion solely because the disorder moments have two slopes. That terminology usually concerns a different limit and a different average.

## Localization landscapes and squared random potentials

Arnold, David, Filoche, Jerison and Mayboroda, *Computing spectra without solving eigenvalue problems* (2017/2018), use the localization landscape, the solution of `Hu=1`, to locate and estimate localized eigenstates of Schrödinger operators. Thus `H^(-1)1` itself is an established object, and its spatial integral is a source-response or torsion-type observable. The paper emphasizes deterministic predictions for individual potential realizations and does not supply the proposed compact-ensemble moment spectrum. [Open paper](https://arxiv.org/abs/1711.04888).

Kirsch and Raikov, *Lifshits Tails for Squared Potentials* (2017/2018), study Schrödinger operators whose random potential is the square of an alloy-type field. They prove low-energy integrated-density-of-states tails, motivated by randomly twisted waveguides. This directly rules out novelty claims for using squared random potentials. Their infinite-volume low-energy spectral statistic differs from the present compact-domain, small-diffusivity moments of an integrated inverse. No direct result collision was found in the paper. [Open paper](https://arxiv.org/abs/1704.01435), [published article](https://doi.org/10.1007/s00023-018-0680-8).

The two limiting procedures should remain distinct. A finite-dimensional random offset crossing a local degeneracy is not an alloy field over a growing domain. The present calculation does not establish Anderson localization, a Lifshits tail, or a multifractal eigenfunction spectrum.

## Noisy saddle nodes and giant diffusion

Reimann, Van den Broeck, Linke, Hänggi, Rubí and Pérez-Madrid, *Giant Acceleration of Free Diffusion by Use of Tilted Periodic Potentials* (2001), derive enhanced effective diffusion and universal weak-noise scaling near the tilt at which deterministic running solutions appear. Their local bottleneck analysis is an important transport precedent for singular response near a coalescence. The stochastic dynamics contains a nonlinear drift and the observable is long-time diffusion along the tilted potential. This differs from a reversible diffusion with a spatially varying killing rate. [Open author PDF](https://www.physik.uni-augsburg.de/theo1/hanggi/Papers/273.pdf), [published article](https://doi.org/10.1103/PhysRevLett.87.010602).

Reimann and Eichhorn, *Weak disorder strongly improves the selective enhancement of diffusion in a tilted periodic potential* (2008), add quenched spatial disorder to that problem. Equations (22)–(26) give the near-critical diffusion enhancement and its dependence on disorder. This is a close physical precedent for disorder amplifying a bottleneck-induced transport effect, but it does not compute the proposed moments across random offsets. [Open paper](https://arxiv.org/pdf/0810.1857).

Hathcock and Sethna, *Reaction rates and the noisy saddle-node bifurcation: Renormalization group for barrier crossing* (2019 preprint, revised 2020), derive a universal escape-time crossover as an energy barrier disappears. Their mean-time scaling, corrections and approximate escape-time distribution concern overdamped drift across a cubic potential. They do not yield the quartic killing-resolvent integral here. [Open paper](https://arxiv.org/pdf/1902.07382).

Even after transforming a drift diffusion to a self-adjoint operator, its effective potential generally includes both a squared-drift term and a derivative term. Dropping that derivative term would change the problem. Thus a shared squared expression near a saddle node does not establish equivalence with `-∂²+(y²-μ)²`. In the candidate, the fold describes zeros of a kinetic field; it is not a bifurcation of the deterministic surface dynamics.

## Suggested scope of an originality claim

A suitably narrow claim is: a compact, explicitly controlled ensemble of reversible adsorption-rate patterns exhibits a rigorously computable change in disorder-moment scaling at order `4/3` as lateral mobility vanishes; coalescing kinetic zeros determine the high-moment constants through a quartic source problem. The mean therefore understates the increasing relative variation between walls. The finite-bulk statement must retain whatever hypotheses its independent remainder theorem requires.

The following should be attributed as established methods or concepts: Kac–Rice marked-zero statistics; harmonic and quartic local models; semiclassical localization; the landscape equation `Hu=1`; tail-cutoff moment calculations; and competition between response amplitude and the probability of a near-degenerate parameter value.

This audit found no exact match for the operator/ensemble theorem or its adsorption application. It does not prove that no match exists. Searches covered coalescing Schrödinger wells, squared random potentials, integrated resolvents and landscapes, rare-event moment spectra, bifurcation-dominated spectral and delay fluctuations, noisy saddle nodes, and disordered tilted-potential transport. Some terminology crosses fields poorly, so a subsequent manuscript search should include both *torsional rigidity with potential* and *integrated localization landscape*, in addition to transport terminology.
