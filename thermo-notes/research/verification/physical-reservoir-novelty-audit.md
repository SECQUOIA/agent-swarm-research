# Novelty audit: optimized physical reservoirs at phase coexistence

Date: 2026-09-06; final scope review 2026-09-07. Independent bounded literature audit of [the microscopic Potts benchmark](../potts-physical-bath.md), [the three-energy-phase theorem](../three-phase-physical-bath.md), [the support classification](../reservoir-support-classification.md), and [the consolidated manuscript](../reservoir-coexistence-manuscript.md).

**Assessment: there is enough evidence to develop an internal draft manuscript candidate, with novelty explicitly provisional.** I found no primary work stating either sharp optimized-total-energy threshold in these notes, nor the resulting two-versus-three-energy distinction. This does not certify priority or publishability. The new evidence narrows the contribution: a bath-size condition proportional to the square of the subsystem energy range is already a known *sufficient* strong-distance bound. The potentially new part is optimal necessity at coexistence, and the reduction to an \(N^{3/2}\) scale for two energy peaks after calibration.

This audit concerns prior art, not a replacement for the independent proof and numerical reviews linked in the research notes.

## Precise candidate being compared

The bath has density of states \(\omega_B(B)\propto B^{c_N}\mathbf1_{B>0}\). For a canonical subsystem law \(P_N\), the exact isolated-composite marginal has likelihood ratio proportional to

\[
\exp(\beta E)(\mathcal E_N-E)^{c_N}_+.
\]

Only the total composite energy is adjustable. The Hamiltonian, target inverse temperature, and other fields are fixed. The claimed conclusions are:

- For a microscopic three-state mean-field Potts model plus an extensive quadratic kinetic sector, some \(\mathcal E_N\) restores the entire canonical subsystem law in TV if and only if \(c_N/N^{3/2}\to\infty\).
- The final extension assumes only that \((E_N-a_N)/b_N\) converges weakly to a law with at least three support points, where \(b_N\to\infty\). Some total-energy calibration restores the full canonical law in TV if and only if \(c_N/b_N^2\to\infty\). This version requires no density, Gaussian local limit, moment bound, or interpeak tail envelope.

The Potts colors are not three distinct energy phases. Its ordered colors share one energy density, and the disordered phase supplies the second. The microscopic example therefore tests the first theorem. Its added kinetic sector makes the energy variance extensive in both phases.

The statements concern full-law TV, including conditional fluctuation laws and all positive phase weights. This target must remain visible when discussing ensemble equivalence; otherwise readers may interpret the result as a claim about thermodynamic potentials, local observables, or simultaneous spatial coexistence.

## A strong-distance square-energy-range bound is already known

A. Riera, C. Gogolin, J. Eisert, *Thermalization in Nature and on a Quantum Computer*, Physical Review Letters **108**, 080402 (2012), [DOI](https://doi.org/10.1103/PhysRevLett.108.080402), [open manuscript with appendices](https://arxiv.org/abs/1102.2389).

Appendix A, equations (22)–(29), controls the trace distance between a reduced microcanonical-shell state and a Gibbs state by the oscillation of the remainder in a linear expansion of the logarithmic bath density of states:

\[
D\le \tfrac12\{\exp(\gamma_{\max}-\gamma_{\min})-1\}+C.
\]

Appendix B, equation (35), specializes this to a bath of \(m\) perturbed spin-\(1/2\) degrees of freedom:

\[
D\le \tfrac12\left\{\exp\!\left[\frac{2\|H_S\|_\infty^2}{\eta^2m}\right]-1\right\}+C.
\]

Here \(\eta\) is the bath energy scale and \(C\) is their density-of-states approximation error. The main text also states this bound. The derivation uses a smoothed bath spectrum and a finite-dimensional subsystem.

Our comparison: this is genuine strong-metric prior art, not just macrostate equivalence. In the commuting case trace distance is TV. For subsystem energy range of order \(N\), its sufficient scale is \(m\gg N^2\). It does not optimize total energy to exploit two separated peaks or prove an unavoidable \(N^2\) scale for three peaks. Nor does it directly cover the unbounded kinetic energy in the present benchmark; a typical-energy truncation would require its own tail argument. Still, the manuscript should not present an \(N^2\) sufficient scale or a bath-Taylor-remainder TV estimate as unprecedented.

## Gaussian ensembles for the Curie–Weiss–Potts model

M. Costeniuc, R. S. Ellis, H. Touchette, *Nonconcave entropies from generalized canonical ensembles*, [open primary manuscript](https://arxiv.org/abs/cond-mat/0605213), explicitly treats the three-state Curie–Weiss–Potts model. It calculates generalized free energies and recovers nonconcave microcanonical entropy using Gaussian penalties. Its ensemble has weight \(\exp[-n\alpha h-ng(h)]\), with \(g\) fixed in the thermodynamic limit. Its principal object is the free energy per particle and the associated equilibrium optimization.

The related Costeniuc–Ellis–Touchette–Turkington chapter, *Global optimization, the Gaussian ensemble, and universal ensemble equivalence*, [open publisher-hosted chapter](https://library.slmath.org/books/Book55/files/06global.pdf), treats the same model in Section 5. Theorem 5.2 gives Gaussian/microcanonical macrostate equivalence on energy intervals by choosing a sufficiently large penalty parameter. This extends the earlier supporting-parabola theory; it does not establish shrinking-penalty full-distribution asymptotics.

Our comparison: the present threshold corresponds to a vanishing entropy-density penalty but a potentially nonvanishing effect on finite-system probabilities and standardized fluctuations. Fixed-penalty thermodynamic-limit results do not resolve that scale. I found no \(N^{3/2}\) physical-bath threshold or optimal three-peak obstruction in these texts. Their model and geometric methods must nevertheless be acknowledged. The earlier [multiphase audit](multiphase-reservoir-prior-art.md) gives the precise 2005/2006 supporting-paraboloid references.

## Gibbs conditioning has sharp growing-subsystem TV results

P. Diaconis and D. Freedman, *Conditional limit theorems for exponential families and finite versions of de Finetti's theorem*, Journal of Theoretical Probability **1**, 381–410 (1988), [DOI](https://doi.org/10.1007/BF01048727), [open Berkeley report](https://digicoll.lib.berkeley.edu/record/86140/files/91.pdf).

For suitably regular iid exponential families, this paper compares the first \(k\) variables conditioned on the sum of \(n\) variables with a matching tilted product law. Its variation norm has a sharp error asymptotic proportional to \(k/n\) when \(k/n\to0\), and it treats nonzero limiting ratios as well. The Gaussian-sphere example directly includes the conventional quadratic kinetic bath. Its convention for variation norm is twice the TV convention in the repository.

A. Dembo and O. Zeitouni, *Refinements of the Gibbs conditioning principle*, Probability Theory and Related Fields **104** (1996), [DOI](https://doi.org/10.1007/BF01303799), [open full version](https://www.wisdom.weizmann.ac.il/~zeitouni/pdf/sanovreffull.pdf), extends conditioning to growing blocks under convexity assumptions, including certain interaction constraints through U-statistics. The full-version introduction, page 3, discusses \(k\log n/n\to0\), improvements to \(k=o(n)\), and corresponding necessary conditions.

Our comparison: TV itself, bath-to-subsystem scaling questions, and sharp conditioning rates are all established. These results do not directly identify the present threshold: here the subsystem is an interacting, multiphase object coupled to a different reservoir, and the target retains a mixture of phase laws. It is not a homogeneous iid block converging to one product tilt. Even conditioning results admitting interactions need their convexity, limiting target, and identification of the subsystem checked before they can be applied. The manuscript should explain this distinction rather than describing all conditioning literature as restricted to fixed subsystem size.

## Local central limit theory and fluctuation corrections

N. Cancrini and S. Olla, *Ensemble Dependence of Fluctuations: Canonical Microcanonical Equivalence of Ensembles*, Journal of Statistical Physics **168**, 707–730 (2017), [DOI](https://doi.org/10.1007/s10955-017-1830-y), [open manuscript](https://arxiv.org/abs/1701.07705).

This work proves energy local CLT/Edgeworth and local large-deviation expansions, then ensemble-comparison and kinetic-energy fluctuation formulas. Its Section 2 assumes uniform-in-\(N\) bounds on the first four derivatives of the free energy per particle. The introduction explicitly places the analysis away from phase transitions. At coexistence of distinct energy densities, the canonical energy variance is of order \(N^2\), so the second derivative of that free energy is order \(N\); this hypothesis fails. The result is essential methodological prior but does not provide the proposed coexistence threshold.

K. Koskinen and J. Lukkarinen, *Estimation of Local Microcanonical Averages in Two Lattice Mean-Field Models Using Coupling Techniques*, Journal of Statistical Physics **180**, 1206–1251 (2020), [DOI](https://doi.org/10.1007/s10955-020-02612-1), [open manuscript](https://arxiv.org/abs/2001.03047), compares local observables through explicit couplings and Wasserstein fluctuation distances for a paramagnet and a mean-field spherical model. This is another quantitative mean-field ensemble comparison, but its local-observable target differs from full-law TV at coexistence.

## Exact finite baths and first-order numerical precedents

The finite power-law marginal itself is standard. For example, M. Campisi, *On the limiting cases of nonextensive thermostatistics*, Physics Letters A **366**, 335–338 (2007), [DOI](https://doi.org/10.1016/j.physleta.2007.01.082), [open manuscript](https://arxiv.org/abs/cond-mat/0611068), relates finite constant-heat-capacity baths to power-law subsystem laws and discusses the canonical limit. It builds on earlier work by Plastino and Plastino and by Almeida. Its heat-capacity conventions should not be imported without checking the surface-versus-volume entropy definition.

Challa–Hetherington's 1988 Gaussian-bath papers and Griffin–Matty–Swendsen's 2017 physical finite-bath study remain the nearest first-order precedents. The latter optimizes comparison temperature and exhibits loss and recovery of the canonical Potts double peak as bath size varies. Its unweighted energy-level \(\ell^2\) distance does not control full-law TV on growing supports. Neither study supplies the exact optimized two-versus-three-phase result located in the current notes. Details and links are in the [previous audit](multiphase-reservoir-prior-art.md).

L. Velazquez and S. Curilef, *Geometrical aspects and connections of the energy-temperature fluctuation relation*, [open manuscript](https://arxiv.org/abs/0910.2864), studies finite thermostats, stability, fluctuation identities, and access to otherwise suppressed energies. This further rules out broad novelty claims about finite baths changing phase sampling. No sharp full-law bath-size classification was found there.

## Draft recommendation and remaining uncertainty

### Final scope and novelty wording review, 2026-09-07

The weak-limit support theorem strengthens the original three-Gaussian-phase result by removing local regularity and tail assumptions. Its necessity applies to every total-energy calibration for the stated physical power-law bath. The unequal-spacing chord argument also gives the necessary scale \(c_N\gg\Delta_N s_N\) when two phase centers are separated by \(\Delta_N\) and one phase has a nondegenerate weak fluctuation limit on scale \(s_N=o(\Delta_N)\). This does not by itself prove sufficiency, compute new critical exponents, or extend the classification to every reservoir density of states.

The prior-art comparison above remains the basis for the final assessment; this final wording check is not a new exhaustive literature search. The sources examined did not state the optimized necessity theorem under this weak three-support hypothesis or the corresponding unequal-scale obstruction. An energy-range-squared sufficient bound and ordinary growing-block conditioning results are established prior art and remain credited.

The plain short-range realization now uses two-dimensional nearest-neighbor Potts models on periodic squares at a fixed sufficiently large number of colors. For an isolated copy, the manuscript proves the \(N^{3/2}\) scale is necessary, not sufficient. For two independent copies, the total energy has three limiting support points, so the \(N^2\) condition is both necessary and sufficient. This latter conclusion does not resolve the isolated-copy sufficiency gap. The manuscript credits the published phase-partition input and distinguishes the additional conditional fluctuation argument.

I found no critical novelty overclaim in the final manuscript wording. The abstract, prior-work discussion, and limitations distinguish known mechanisms from the candidate distribution-level classification, and keep priority provisional. Here “sharp” describes a proved necessary-and-sufficient asymptotic condition where both directions are available; it does not certify historical priority. The remaining literature and isolated-copy sufficiency gaps should stay explicit in any external draft.

A defensible draft can lead with: **the required size of a finite thermal reservoir depends on whether two or at least three distinct energy phases must be preserved, even after optimizing the composite energy.** State the assumptions and the probability metric immediately, and present the actual Potts-plus-kinetic model as a microscopic realization of the two-energy case.

The three-energy necessity is a clean result, but its proof is elementary once one asks the right question. Its potential value comes from the physical classification and its contrast with the optimally calibrated two-phase law, rather than proof complexity. The microscopic realization and boundary-scale predictions strengthen that case. This audit does not justify claims that the work will be highly cited, or that it already meets a particular journal's threshold.

The main unresolved prior-art risks are older finite-bath/nonextensive Potts studies, conditioning results for triangular arrays or nonconvex constraints, and papers using a different description of the same calibration problem. A bounded search cannot exclude these. No statement here should be upgraded from “not found in the sources examined” to “not previously known.”

New source PDFs and searchable text are preserved in the research/sources folder with stems: riera-gogolin-eisert-2012-thermalization; diaconis-freedman-1988-conditioning; dembo-zeitouni-1996-conditioning; costeniuc-etal-2006-potts-gaussian; costeniuc-etal-global-optimization; cancrini-olla-2017-ensembles; campisi-2007-limiting-tsallis; velazquez-curilef-2009-fluctuation; and koskinen-lukkarinen-2020-local. The Dembo–Zeitouni PDF has broken text encoding; the relevant introduction page was inspected visually.
