# Prior-art audit of the conditional capacity certificate

Audit date: 2026-09-06. Independent adversarial literature review of `research/capacity-certificates.md`.

The exact finite-parameter conditional capacity lower bound was **not located in the sources inspected**, but the planar hard-channel resistance formula is the classical **Ahlfors–Warschawski bound**, including its rigorous inequality status. Higher-dimensional and weighted foliation methods also have direct precedents. The remaining candidate is the specific conditional score/Poisson construction and its practical capacity certificate; its novelty and impact remain uncertain.

## What is already established

| Component | Closest inspected source | Assessment |
|---|---|---|
| Projected capacity upper bound and energy-error identity | Zhang, Hartmann and Schütte (2016), Proposition 6 | Established; already correctly acknowledged in the candidate note. |
| Conditional relaxation controls for effective dynamics | Legoll and Lelièvre (2009/2010), Sections 3–5 | Established. Their estimates concern distributions and paths, rather than the proposed exact capacity certificate. |
| Stiff confinement does not rescue an unsuitable coordinate | Legoll and Lelièvre, Sections 4–5 | Established mechanism, including a failure of projection and stiff-limit operations to commute. |
| Friction as an equilibrium-restricted Wasserstein metric | Zhong and DeWeese (2024) | Explicit prior theorem. |
| Friction, electrical resistance, and probability transport on graphs | Sawchuk and Sivak (2026 preprint), Sections III–IV | Explicit prior correspondence. A discrete version cannot claim this identification as new. |
| Rational geometric correction in a symmetric channel | Zwanzig (1992), reproduced as Eq. (120) by Mangeat, Guérin and Dean (2017) | Formula already present as an approximation; its resistance inequality is also classical by Ahlfors–Warschawski. |
| Exact planar resistance bound with width and midline slopes | Ahlfors–Warschawski, explicitly restated as Theorem 8.1 in Avkhadiev, Kayumov and Nasyrov (2023) | Exact mathematical prior result; planar geometric bound is a rediscovery. |
| Midline slope and width slope corrections | Bradley (2009), especially Eq. (42) | Established asymptotic corrections; no inspected exact conditional certificate. |

## Primary sources and scope of inspection

**Zhang, Hartmann and Schütte**, *Effective dynamics along given reaction coordinates, and reaction rate theory* (2016), [DOI](https://doi.org/10.1039/C6FD00147E), [author manuscript](https://publications.imp.fu-berlin.de/1974/1/201606_ZIB_16-35_report_Zhang_Hartmann_Schuette.pdf). Proposition 6 supplies the reaction-coordinate capacity upper bound and exact Dirichlet error identity. The candidate's use of these results should remain explicit. A local PDF and extracted text were already present under `research/sources/`.

**Legoll and Lelièvre**, *Effective dynamics using conditional expectations*, [arXiv:0906.4865](https://arxiv.org/abs/0906.4865), published in *Nonlinearity* 23 (2010), [DOI](https://doi.org/10.1088/0951-7715/23/9/006). Inspected Sections 3–5 in the full manuscript. Section 4 explains that the free energy and projected dynamics can be independent of stiffness while the full dynamics is not. Section 5 considers a potential `V0+q²/ε`, constrained diffusion on `q=0`, and conditions under which coordinate projection commutes with the stiff limit. Thus neither the warning about stiffness nor the general geometric reason is new. The proposed exact capacity interval appears different from their time-marginal and pathwise estimates.

**Kalinay and Percus**, *Extended Fick-Jacobs equation: Variational approach*, *Physical Review E* 72, 061203 (2005), [publisher page](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.72.061203), [open full text](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevE.72.061203/fulltext). Inspected the formulation, introduction, examples, and conclusion. Equation (2.1) is a space-time variational functional with forward and backward densities. The authors explicitly use stationarity without requiring an absolute minimum or maximum. They choose a curvilinear coordinate, impose a density ansatz, and derive an effective equation. Their method can be exact in suitable solvable coordinates, but the inspected formulation does not give the candidate's Thomson trial current or a certified two-sided interval. The word “variational” in the title therefore does not establish exact overlap.

**Bradley**, *Diffusion in a two-dimensional channel with curved midline and varying width: Reduction to an effective one-dimensional description*, *Physical Review E* 80, 061142 (2009), [publisher page](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.80.061142), [open full text](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevE.80.061142/fulltext). The full text derives an asymptotic generalized Zwanzig equation with both midline and width derivatives and discusses periodic effective diffusivity. This is important precedent for the Gaussian and curved-channel examples. A rigorously justified asymptotic expansion is distinct from a bound valid without the small-parameter assumption.

**Mangeat, Guérin and Dean**, *Dispersion in two dimensional channels—the Fick-Jacobs approximation revisited*, *Journal of Statistical Mechanics* (2017) 123205, [arXiv:1710.02699v2](https://arxiv.org/abs/1710.02699), [DOI](https://doi.org/10.1088/1742-5468/aa9bb5), [author PDF](https://www.mangeatm.fr/papers/mangeat_guerin_2017_dispersion.pdf). Full-text inspection focused on Sections VII–VIII and Eq. (120). They reproduce a rational approximation attributed to Zwanzig and show its limitations for wide channels. Their separate bound, Eq. (102), is `D_eff/D ≥ h_min/⟨h⟩`. The rational approximation and this geometric lower bound are different expressions. I did not find a theorem there asserting that Eq. (120) is always a lower bound.

**Zhong and DeWeese**, *Beyond Linear Response: Equivalence between Thermodynamic Geometry and Optimal Transport*, *Physical Review Letters* 133, 057102 (2024), [arXiv:2404.01286](https://arxiv.org/abs/2404.01286), [author PDF](https://redwood.berkeley.edu/wp-content/uploads/2025/06/zhong2024beyond.pdf). Their continuous overdamped friction/optimal-transport equivalence directly precedes the interpretation of `g=⟨s,K⁻¹s⟩`. Inspection found no capacity inequality. The metric interpretation should cite this work rather than be presented as a discovery.

**Sawchuk and Sivak**, *Thermodynamic geometry of friction on graphs: Resistance, commute times, and optimal transport*, [arXiv:2601.01273v2](https://arxiv.org/html/2601.01273v2). This preprint explicitly identifies the friction metric of slowly driven reversible chains with electrical resistance and commute-time geometry, and gives an equilibrium-path-restricted transport formulation. The object is a driven distribution, not the longitudinal capacity of the strip. Its current-routing interpretation nevertheless substantially narrows any novelty claim for a network analogue.

**Berezhkovskii and Szabo**, *One-dimensional reaction coordinates for diffusive activated rate processes in many dimensions*, *Journal of Chemical Physics* 122, 014503 (2005), [DOI](https://doi.org/10.1063/1.1818091), [indexed author PDF](https://simbios.stanford.edu/svn/neq-mc/references/berezhkovskii-szabo-reaction-coordinates.pdf). Search-indexed primary text describes minimizing the one-dimensional Kramers rate over a reaction coordinate in the saddle-point setting. The download failed due to a server certificate mismatch, so this was not a complete text inspection. The result concerns an upper variational construction, not an identified match to the candidate lower bound.

**Doi**, *Theory of diffusion-controlled reaction between non-simple molecules. I*, *Chemical Physics* 11, 107–113 (1975), [publisher abstract](https://www.sciencedirect.com/science/article/pii/0301010475800437), [DOI](https://doi.org/10.1016/0301-0104(75)80043-7). The primary abstract explicitly describes a lower reaction-rate variational principle and relates it to the Wilemski–Fixman closure. Full text was not inspected. This is a remaining historical comparison, not grounds to dismiss or establish the conditional formula's novelty.

## Exact algebraic overlap with the channel approximation

This calculation was developed during the audit and needs independent verification before promotion to a result. It does not follow by blindly inserting a moving hard boundary into the fixed-fiber score formula.

Take a periodic hard channel of period `L`, isotropic microscopic diffusivity `D`, midline `m(x)`, and width `W(x)>0`, with no external potential. In a period define

\[
J_x=\frac1W,\qquad
J_y=\frac{m'+(W'/W)(y-m)}{W}.
\]

Direct differentiation gives `div J=0`, unit section flux, and tangency to both boundaries `y=m±W/2`. Its dissipation is

\[
R_J=\frac1D\int_0^L\frac{1+m'^2+W'^2/12}{W}\,dx.
\]

The standard periodic conductivity/diffusivity duality then suggests

\[
\frac{D_{\rm eff}}D\ge
\frac1{\langle W\rangle\left\langle
 (1+m'^2+W'^2/12)/W\right\rangle},
\]

where averages are over one period. The normalization is `D_eff=L²/(|Ω| R_min)`, for a unit circulating current and `|Ω|=∫W dx`; it must be checked against the exact periodic variational problem, not a cell with independently imposed constant end potentials.

For `m=0`, write `W=2h=2εζ` in the dimensionless notation of Mangeat et al. The right-hand side becomes

\[
\frac1{\langle\zeta\rangle\langle\zeta^{-1}\rangle}
\frac1{1+\epsilon^2\langle\zeta'^2/\zeta\rangle/
(3\langle\zeta^{-1}\rangle)}.
\]

This is exactly the expression of their Eq. (120). The formula and its underlying universal resistance inequality are old; see the decisive mathematical comparison below. The lower bound can tend to zero while the true diffusivity stays positive in a wide-channel limit; this makes the bound weak, not false.

## Decisive mathematical prior art: Ahlfors–Warschawski

**Avkhadiev, Kayumov and Nasyrov**, *Extremal problems in geometric function theory*, *Russian Mathematical Surveys* 78:2 (2023), 211–271, [DOI](https://doi.org/10.4213/rm10076e), [open PDF](https://www.mathnet.ru/php/getFT.phtml?jrnid=rm&option_lang=eng&paperid=10076&what=fullteng). Page 247 (PDF page 37), Theorem 8.1, defines `θ=g-f` and `φ=(g+f)/2` for a graph-bounded quadrilateral and states

\[
\int_a^b\frac{dx}{\theta}\le\operatorname{Mod}(Q)
\le\int_a^b\frac{1+\phi'^2+\theta'^2/12}{\theta}\,dx.
\]

The authors attribute the lower estimate to Ahlfors and the upper estimate to Warschawski (spelled “Warshawski” there). Their cited references are Ahlfors, *Conformal Invariants*, Chapter 4 §5; Evgrafov, *Asymptotic Estimates and Entire Functions*, Chapter 2 §5; and Miklyukov, *Conformal Mapping of a Non-Regular Surface and Its Applications* (2005), Chapter 7 §1. The PDF was inspected through the web reader; direct download returned HTTP 403.

**Our comparison:** in the rectangle convention used in that theorem, `Mod(Q)=length/width`, hence `Mod(Q)=D/C` for the physical planar conductance. Substitution `θ=W`, `φ=m` gives exactly our trial-current resistance. Periodic homogenization adds a normalization and a long-channel limit, not a new geometric inequality. An anisotropic constant `D` can be handled by a linear coordinate change, so that extension alone also gives little novelty.

The likely original historical paper is **S. E. Warschawski**, *On conformal mapping of infinite strips*, *Transactions of the AMS* 51 (1942), 280–335, [DOI](https://doi.org/10.1090/S0002-9947-1942-0006583-6). Access to the AMS PDF failed. The exact original theorem number and its relation to the finite-quadrilateral version are therefore not verified. Do not cite an invented theorem number or treat the 1942 identification as a completed original-source inspection.

## Higher-dimensional and weighted foliation bounds

**Brakalova, Markina and Vasil'ev**, *Extremal functions for modules of systems of measures*, [arXiv:1409.1626](https://arxiv.org/abs/1409.1626), *Journal d'Analyse Mathématique* 133 (2017), 335–359, [DOI](https://doi.org/10.1007/s11854-017-0036-1). Full text is saved locally. Theorem 3 gives the exact `p`-modulus of a smooth family of curves connecting a condenser's plates in `R^n`. With `p=2`, its formula is `∫ℓ(z)⁻¹ dz`, where `ℓ(z)=∫|∂tF(z,t)|²/J_F(z,t) dt`. Section 3.2 points to Ohtsuka, *Extremal Length and Precise Functions*, Theorem 3.4.3, for a weighted modulus theorem on tubes whose curves follow a solenoidal field. Ohtsuka's theorem was not independently read. The paper also identifies Rodin, *The Method of Extremal Length* (1974), Theorem 14, as the planar predecessor.

**Our comparison:** a smooth admissible current with positive longitudinal component generates just such a connecting foliation. Optimizing the amount of current carried by each streamline leads to the parallel sum `∫ℓ⁻¹`; prescribing uniform streamline weights yields `1/∫ℓ`, which is weaker by Jensen. Thus the general idea “build transport paths, then infer a capacity lower bound” is established, even in higher dimensions. The specific least-cost conditional transport field may still be useful because it avoids a global committor calculation, but merely changing the dimension or adding a scalar weight does not establish an independent theoretical advance. A full mapping to the weighted anisotropic setting would require checking Ohtsuka's definitions and hypotheses.

## Search limits and next decisions

Searches combined the terms reaction rate, capacity, reaction coordinate, conditional Poincaré, Poisson equation, Thomson principle, Fick–Jacobs, variational bounds, Zwanzig, thermodynamic friction, Wasserstein, and the relevant author names. Many search results were irrelevant; unsuccessful keyword searches provide little novelty confidence. Positive matches above were traced to primary texts where accessible. New PDFs and extracted texts are retained in `research/sources/`.

Before a publishable novelty claim, inspect Doi/Wilemski–Fixman lower variational principles, Ohtsuka's weighted theorem, and the later Kalinay–Percus corrections papers. The classical planar bound is now identified, so that novelty question is resolved negatively. Also compare with generic equilibrated-flux error estimators: the proof mechanism is standard, so the contribution must explain why the conditional choice makes a useful quantity accessible or yields a previously unrecognized exact guarantee. No inspected source justifies calling the current result wholly new or high impact yet.
