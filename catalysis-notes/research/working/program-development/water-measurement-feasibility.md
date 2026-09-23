# Can a small water-step apparatus identify storage and transport?

2026-09-16. Feasibility assessment for the [physical-water program](physical-water-management.md), [first causal test](water-management-first-test.md), and [size prediction](../../calculations/water-size-discriminator.md). No new experiment, material coefficient or direct active-site water measurement is claimed. Revised after the [independent feasibility review](../../reviews/water-measurement-feasibility-review.md).

**A modest apparatus qualification is justified. A classical nonreacting zero-length-column measurement is not yet a validated route to the operative transport coefficients of wax-bearing Co/SiO2–PDVB.** The first deliverable should be an uncertainty-bounded inventory and response-time window for a representative small packing under the relevant gas, followed by a decision on whether a useful conductance can be identified. It should not be a fitted diffusivity obtained automatically from a desorption tail.

## What the primary demonstrations establish

Brandani and Mangano demonstrate water equilibrium and kinetics on a small commercial silica-gel fragment: low-flow experiments determine loading curves; higher-flow experiments resolve exchange. Their coefficient `ka` is defined through a loading driving force, and adsorption/desorption are not interchangeable where hysteresis occurs. The experiments are at 10–40 °C, not FT conditions. The paper supports the method, not transferring silica-gel coefficients to cobalt/wax. [Energy 2021, DOI 10.1016/j.energy.2021.121945](https://doi.org/10.1016/j.energy.2021.121945), accepted manuscript pp. 3–8, [institutional full text](https://www.pure.ed.ac.uk/ws/files/225421831/MassTransportCoeffWaterZLC_revised.pdf).

Their methodological review recommends multiple flows, blank characterization, equilibrium/kinetic checks and simple resistance models before combined fits. It documents misleading tails from equilibrium, heat effects and leaks, and discusses partial-loading tests when diffusion and barriers might coexist. Those checks remain relevant; their success on adsorbents does not establish a fixed catalyst state under changing syngas. [Adsorption 2021, DOI 10.1007/s10450-020-00273-w](https://doi.org/10.1007/s10450-020-00273-w), Sections 2 and 3.4–3.9, 3.13.

The newly supplied [Elgersma et al. 2022 original](../../../literature/papers/elgersma2022-measuring-the-liquid-solid-mass/fulltext.md), pp. 4–6 and 8–11, demonstrates an independent exchange measurement using T2–T2 NMR in water-filled 1.3 mm silica and 3.1 mm titania spheres. Its model estimates an external transfer coefficient only after bed geometry, intra-pellet diffusivity and relaxation properties are independently known. It distinguishes local film transfer from an apparent bed coefficient that absorbs axial dispersion. This is a concrete method precedent, but transfer to hot, pressurized Co/SiO2–PDVB with wax, smaller granules and cobalt-induced magnetic effects is unvalidated. It supplies neither a coefficient for the proposed packing nor a measurement of water activity at cobalt. No NMR campaign is added to the first stage.

The [den Breejen 2009 original](../../../literature/papers/breejen2009-on-the-origin-of-the/fulltext.md), pp. 2–3 and 5, confirms that C16O/C18O switching measures a water-response pool containing O, OH and adsorbed H2O. The authors explicitly warn that water readsorption may inflate residence times and coverages. Their 210 °C, 1.85 bar, H2/CO = 10 Co/CNF protocol is a useful methods anchor, not validation of passive exchange or source-site identification at the proposed FT condition. The newly read [IUPAC transport report](../../../literature/papers/karger2024-diffusion-in-nanoporous-materials-with/fulltext.md), pp. 5–12 and 35–38, also reinforces the distinction between self, transport and apparent diffusivities. These sources strengthen the current measurement cautions; they do not overturn the two-pool counterexample.

## Which coefficient would actually be measured?

Keep three quantities separate:

- A fitted relaxation rate λ has units s−1; its reciprocal is a time.
- A local gas-referenced conductance G has units m³/s in `dN/dt = G(cb − x)`.
- A continuum effective coefficient K multiplying a gas-concentration gradient has units m²/s. It requires a specified flux area, geometry and concentration basis.

For a genuinely single, linear, reversible pool with internal concentration coordinate x and independently measured capacity `B = dN/dx`,

\[
B\dot x=G(c_b-x),\qquad \lambda=G/B.
\]

Thus independently measuring B can convert an identified passive-exchange λ into G for **that pool and geometry**. A reacting-source feedback can change the observed rate: linearizing `B dx/dt = Q(x) + G(cb − x)` gives `λ_observed = (G − ∂Q/∂x)/B`. Therefore a live-catalyst pole is not automatically G/B, even when B is known. The source dynamics must be independently constrained or negligible on the measurement scale. It does not identify which pore water controls cobalt chemistry. For a local-equilibrium continuum with mobile concentration c, dimensionless differential storage s and flux `J = −K∇c`,

\[
s\,\partial_t c=\nabla\!\cdot(K\nabla c),\qquad D_{relax}=K/s.
\]

Here s includes mobile pore volume and the derivative of sorbed inventory per envelope volume. A transient-derived diffusivity can therefore change because storage changed. Recovering K requires that storage and transport describe the same equilibrating spatial pool. A fitted linear-driving-force coefficient, a diffusion eigenmode and a mean uptake time have different geometry factors; they cannot all be converted by multiplying by radius squared without defining the model.

For the whole small cell, the observable balance is

\[
\frac{dN_{retained}}{dt}=\dot n_{w,in}-\dot n_{w,out}+Q_{w,net}(t)
-\frac{dN_{gas}}{dt}.
\]

Q includes net chemical water formation/consumption. A humidity perturbation changes reaction rates, potentially surface oxygen and hydroxyl inventories, and sometimes the working state. Without a resolved or bounded Q term, the integrated transient is not an adsorption capacity. Slow-flow curve collapse does not make a reacting experiment an equilibrium isotherm.

## Choose a small representative packing, not a single isolated particle

The physical intervention is neighboring PDVB granules at 0.05 g/g catalyst. A single catalyst particle without representative polymer contacts removes that intervention. At low loading, a tiny randomly packed sample may contain too few promoter granules to reproduce its neighborhood distribution. Record actual granule counts or a packing image and compare independent packings. Increase sample size only enough to make the composition/contact distribution and water signal reproducible; retain the measured apparatus response rather than assuming the resulting bed is an ideal mixed cell.

The [review calculates the sampling scale](../../reviews/water-measurement-feasibility-review.md): at 4.3 mg catalyst, 5 wt% additive and illustrative spherical-equivalent diameters of 250–425 μm and envelope densities of 0.5–1.2 g/cm³, there are roughly 4–53 promoter granules, centrally fourteen. These are assumptions, not measured material bounds. Counting/weighing deliberately can control composition; independent packings must still test spatial variability. A larger small packing may be justified, rather than importing the ambient silica-gel paper's sample mass.

Use a short cartridge in an existing qualified high-pressure flow system if available. The relevant temperature, pressure and water background should match one stable interval from the first-test protocol. An ambient-pressure room-temperature ZLC built first would calibrate the technique, but not answer the deciding question. Equipment access is not established here.

Preserve the conditioned material's liquid inventory and activation history. Prefer conditioning and measuring in the same cartridge where that configuration reproduces the relevant functional state. If transfer is necessary, apply the already required handling pilot. A different small-packing conditioning history must not be described as the same state merely because outlet conversion matches.

## The smallest useful qualification

### 1. Establish what the instrument can resolve

At the chosen hot, pressurized gas condition, apply the same small water step to an empty cartridge and the quartz/PDVB packing blanks. Include an inert tracer, but also measure the actual water blank: an inert tracer does not capture water stored in valves, lines or the detector path. Maintain H2 and CO partial pressures by replacing inert gas; keep switching-line pressures matched. Calibrate water at both endpoints and the molar flow correction. At the proposed high-water plateau the water mole fraction is about 0.2, so do not import the Energy paper's dilute-water flow approximation without checking it.

Measure the repeated blank's integrated-area uncertainty, time resolution, baseline drift and flow dependence. These define the minimum resolvable inventory and exchange time. Heated pressure reduction and detector sampling must be part of the blank, not treated as instant. Resolve any water condensation or baseline memory before introducing catalyst. This step alone can stop an uninformative campaign cheaply.

### 2. Ask whether the live sample supplies identifiable extra information

Use one representative conditioned parent packing and one PDVB packing. Apply the same small up/down perturbation at two flows within the already qualified low-conversion regime, keeping gas partial pressures fixed. Repeat the initial condition to detect drift. Measure reaction rates and the oxygen balance with sufficient time resolution to bound the integrated change in Q. Do not infer a small source correction by subtracting two large, noisy water signals alone. Use the product balance and report unresolved oxygen storage explicitly.

The immediate outputs are source-corrected retained-water intervals, reproducibility between step directions, and whether the sample response is distinguishable from the instrument blank. If the retained amount is reversible and the chemical-source uncertainty is smaller than the intended contrast, an incremental capacity for the observed response may be estimable. It is not automatically the capacity with respect to an internal cobalt-pool concentration: a derivative along a reacting steady-state curve has a different meaning. If an extra time scale is resolved, test the simplest pool or spatial model against both flows and the return step. A second exponential is not automatically a second physical pool.

Include one reduced-amplitude repeat and baseline returns to test linearity and drift. Use independent packings before reporting a formulation contrast; repeated switches in one cartridge do not establish packing reproducibility. Define beforehand which inventory and time contrast would change the intended decision, and include blank, source, packing and drift uncertainty rather than fit uncertainty alone.

Two flows are an initial feasibility check, not guaranteed separation of equilibrium and kinetic regimes. Add lower/higher flow points only when they are needed to determine whether an apparent coefficient is flow-controlled, or when a particular prediction requires it. If lowering flow changes conversion, temperature, liquid inventory or cobalt state, it cannot serve as an equilibrium calibration of the original state.

### 3. Make one held-out response prediction before using a coefficient in design

If the capacity and response model survive those checks, choose a held-out perturbation that separates their plausible explanations. Prefer a partial-loading pulse near or below the inferred exchange time when competing models predict resolvably different responses; a third nearby flow that they all fit adds little. Predict the absolute uptake and full time response at the same operating state. Use a perturbation large enough to resolve but small enough that returns show the chosen state is preserved. Do not refit its capacity or introduce a new water pool after observing the held-out response and call that validation.

This first prediction tests an apparatus/formulation transfer function. It does not yet validate a new granule size, water-damage law or active-site chemical potential. Successful prediction can justify one further measurement tied to a concrete design decision; failure can stop the conductance-based program before a broad catalyst campaign.

To justify an operating-history research branch, add a functional prediction fixed before the same held-out pulse. Independently calibrate each formulation's reversible response to nearby imposed water levels, check a reduced-amplitude repeat for linearity and bound temperature/reactant-transfer changes. Combine the proposed dynamic model with that calibration to predict diagnostic productivity recovery or integrated hydrocarbon output. Correct product-collection delays. This remains a conditional operating rule, because a steady external-water calibration is not a selective local-water reporter and surface chemistry can itself relax. No resolvable water sensitivity means this functional endpoint cannot test the proposed contrast.

## What can be bounded without resolving every mechanism?

| Observable outcome | Defensible information and next decision |
|---|---|
| Positive capacity is resolved and a validated model bounds exchange above the apparatus bandwidth | Report a relaxation-time bound and, only with source feedback constrained, a conductance lower bound for that pool. Matching the blank without resolved positive capacity does not establish fast exchange; no unseen cobalt pool is bounded. |
| Capacity and an extra relaxation mode survive corrections and predict the held-out perturbation | Estimate G only if consistent source dynamics justify its conversion from λ and B. A successful functional prediction can support a bounded pulse/purge rule. Neither result automatically separates external k from internal K for shaping. |
| The response collapses with eluted volume and shows no independently resolved kinetic contribution | Capacity/equilibrium information may be available; transport is too fast relative to the chosen operating window or remains unidentifiable. Do not identify a slow-looking equilibrium washout as internal diffusion. |
| Different parameter sets fit all measured responses but give conflicting stationary or size predictions | The intended prediction is not identified. Seek one specific additional constraint only if it can discriminate those sets; otherwise retain an empirical formulation result. |
| Source correction, state drift or blank uncertainty is comparable to the proposed uptake or kinetic contrast | No meaningful capacity/conductance contrast is established. Stop or change the measurement window; do not rescue it by adding unconstrained pools. |

For a spatially distributed linear system, a boundary humidity step weights accessible storage and the pathways reached from that boundary. Internally generated reaction water and damage near cobalt weight locations differently. Even a correct boundary-response model may not constrain those source-to-site transfer functions. Consequently, no general active-site drying bound follows from total inventory alone. An [explicit two-pool counterexample](../../calculations/water-local-exposure-identifiability.md), independently checked, shows that even inlet-water and source-water tracer responses can both agree while concentration at the producing region differs. This disproves guaranteed identification, not the possibility of identification with a genuinely independent constraint.

## Heat, films and the carrier-switch trap

Small samples and small steps reduce heat effects, but hot cobalt adds reaction heat and changing inhibition. Check whether step amplitude and a reduced sample inventory change the apparent response after accounting for known flow/holdup changes. Include a conservative temperature-effect estimate using measured thermal behavior; wall temperature alone cannot exclude a particle transient. A carrier-gas switch is useful in a passive adsorbent, but replacing H2 or syngas on cobalt changes reaction and redox conditions as well as heat and mass transfer.

External gas-film resistance can remain in a fitted exchange coefficient. Flow dependence can expose that limitation, but flow independence over a narrow range does not prove its absence. Do not transfer the coefficient to another packing geometry without an applicable film/interface model. Wax can introduce partitioning, slow liquid rearrangement and multiple inventories, so a dry support or synthetic-wax blank is an apparatus/mechanism control, not the working catalyst's calibration.

Switching syngas off to obtain a clean nonreacting isotherm is particularly risky. The operation removes the water source and changes H2/CO coverages, cobalt redox and possibly retained liquid. Recovery of the original rate afterward does not prove that the intermediate measurement sampled the same transport state. A passive measurement may characterize the explicitly defined post-switch state; transfer to the live catalyst requires evidence. If no source-preserving measurement or demonstrated state-preserving pause is available, stop short of claiming operative G or K.

## Investment decision

The bounded first measurement stage is: hot blank and matched packing blanks; parent and low-dose PDVB at one qualified state; small up/down steps at two flows; one reduced-amplitude repeat and baseline returns; independent packing checks; and, only if resolved, one held-out partial-loading pulse. Stop after this qualification decision. Use an existing FT system if it can support the measurement; this proposal does not justify an open-ended apparatus build.

The pilot can qualify a measurement, and may support a useful operating-history prediction. It does not yet establish a route to the stationary source-to-site transport mechanism. Do not commit to a broad two-size mechanistic campaign unless independently constrained source weighting and the relevant resistance partition support its prediction; a validated outlet response alone does not meet that requirement. If it resolves only capacity or a formulation-level transient, retain that result and return to the direct challenge/output decision. Failure to resolve a signal is a measurement limitation. An informative negative instead needs an uncertainty interval that excludes an operationally consequential change for the stated observable, state and timescale. If it resolves a model-specific G, next constrain only the coefficient partition or source weighting required for the selected shaping prediction. No direct local-water-activity measurement is promised, and no room-temperature silica coefficient is imported.

The distinction among **qualified measurement**, **predicted operating-history consequence**, and **identified stationary mechanism** is an investment boundary. The first is plausible, the second experimentally unresolved, and no demonstrated route to the third is established. Predicting an outlet trace alone does not constitute a substantial mechanistic program. The [working-liquid preloading evaluation](water-working-liquid-intervention.md) also closes that proposed shortcut as a selective mechanism test: it changes capacity and the water/reactant interface together. No preloading, isotope expansion or materials screen is included in this pilot. All substantive fresh-review corrections are accepted; remaining limitations require experiments.

Source status: original accepted Energy manuscript read from `/tmp/catalysis-program-development/water-zlc.pdf` and `.txt`; methodological review read through its open publisher full text. Both DOIs and the Energy artifact were supplied by the root and are routed to the sole literature agent. No new scholarly source was identified, no KB edits were made, and no new agents were used.
