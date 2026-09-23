# Independent review: when does a physical hydrophobic promoter change catalysis?

Date: 2026-09-16. Scope: independent review of the proposed distinction among water transport conductance, water inventory, and changes to the catalyst or its immediate interface. This review evaluates the supplied primary articles and transparent peer-review replies; it does not establish experimental results or priority over all literature.

## Recommendation

**Develop a bounded experimental program, conditional on obtaining a reproducible physical-promotion effect and an informative water-response assay.** There is a consequential question here: under what operating conditions can an added, nominally inert solid prevent water-induced loss of catalytic function, and when does faster water release fail to provide protection? A reliable answer could guide catalyst-bed design without requiring a new active material. The contribution must be a tested prediction of catalytic behavior, including where promotion fails. Correcting the thermodynamic language or measuring another desorption curve would be insufficient.

The stronger framing is **steady protection versus protection through water-exposure history**, rather than assuming that conductance will prove to be the explanation. A physical promoter might change gas transport, liquid distributions, surface sorption, startup damage, or several of these together. These possibilities imply different design choices and different transferability. They should remain competing hypotheses.

Confidence in the existence of a useful physical-promotion phenomenon is reasonably strong for the published materials and conditions. Confidence that greater steady water conductance causes the reported cobalt protection is limited. A first discrimination campaign is feasible and likely informative if a suitable flow reactor and quantitative water detection are available. Confidence in an additional practical improvement beyond the published result is presently modest: the published durability is already impressive, and the promoter lowers initial conversion in the cobalt example.

## What is already established and must receive credit

[Fang et al., Nature Communications 2026](https://www.nature.com/articles/s41467-026-76571-8), Fig. 1 and accompanying results, report a Co/SiO2–PDVB physical mixture retaining approximately 44.1% CO conversion over 1200 h at 220 °C and 2 MPa, with 88–90% C5+ selectivity. The unpromoted reference begins at 67.9% conversion and loses activity. These are not equal initial productivities. At the headline promoter loading, 0.025 g PDVB is mixed with 0.5 g catalyst; “5 wt%” means relative to catalyst mass, not an industrial-volume penalty already established to be negligible.

The paper is not missing all obvious controls. It includes separate beds, different granule sizes, powder mixing, quartz and SiC comparisons, other hydrophobic materials, additional water, altered space velocity to lower reference conversion, and substantial polymer-stability and cobalt-state characterization. SI Fig. 30 and Note 9 address lower conversion by increasing flow over the reference. However, this test uses 1.0 g PDVB with 0.5 g catalyst, rather than the headline 0.025 g dose. The tests strengthen the physical-promotion interpretation without making local exposure, geometry, or thermal history identical in every comparison.

The transparent review explicitly raises the distinction between water adsorption and transport. In the later response to Reviewer 2, comment 2-5, the authors agree that the CoCl2 breakthrough result indicates decreased average water accumulation. Earlier replies include spatial NMR water-intensity maps and faster desorption near PDVB than farther away. A later reply states that some dynamic imaging belongs to other work and was not included in the revised article. **Spatial imaging of water storage or faster disappearance near a hydrophobe is therefore already part of the disclosed evidence, not a new program concept.** The remaining gap is quantitative relation to chemical activity, steady flux, and catalytic consequences under the relevant operating state.

[Fang et al., Science 2022, DOI 10.1126/science.abo0356](https://doi.org/10.1126/science.abo0356), pp. 406–410, already establishes physical PDVB promotion in CoMnC syngas conversion, dependence on mixing proximity, water inhibition and suppression of that inhibition, and different product distributions with porous promoters. Its modeling relates greater water mobility to hydrophobic surroundings. The 2026 article extends the phenomenon to metallic cobalt durability. Merely using another catalyst, another hydrophobe, or an isotope transient would not establish a substantial advance.

The 2026 model assigns water diffusion coefficients of 2.2 × 10−7 and 4.7 × 10−7 m² s−1 based on earlier work. The 2022 paper obtains those values from mean-square-displacement simulations and calls them self-diffusion coefficients. They are not independent measurements of the steady transport conductance of the actual 2026 catalyst bed. A successful simulation with these assigned coefficients is consistent with the proposed mechanism; it does not independently identify it.

## Physical limits and hidden assumptions

### Concentration is not chemical potential across unlike phases

At equilibrium, two materials exposed to the same water reservoir can hold very different water amounts while sharing the same water chemical potential. Different NMR intensity or adsorption capacity on silica and PDVB does not, by itself, demonstrate a sustained driving force from one domain to the other. For a nonequilibrium system, a suitable near-equilibrium transport law is expressed in terms of chemical-potential gradients, with phase-specific sorption relations connecting local concentrations to activity. A gradient in adsorbed amount across different materials cannot simply be inserted into a single, homogeneous Fickian law.

This does not forbid promotion. Wettability can change liquid configurations, accessible paths, adsorption kinetics, or mobilities. A reaction source and a flowing outlet can sustain chemical-potential gradients. The issue is identifying which property changed and showing that it controls the catalytic result.

### A washout time does not identify steady conductance

As a deliberately simplified local balance, let c be mobile-phase water concentration, B = dN/dc the accessible water-storage capacity, q the net local production rate, G the conductance to a reservoir of concentration cb, and assume fixed B, G, and q:

    B dc/dt = q − G(c − cb)
    τ = B/G
    c_ss − cb = q/G

Two samples can have identical normalized washouts with very different steady source-to-reservoir concentration differences. Lower B shortens washout without changing that difference. A lower water-production rate q also lowers the steady concentration without increasing G. Both matter here because the promoted cobalt catalyst initially has a lower reaction rate.

These equations are a diagnostic counterexample, not a realistic fit to an entire FT bed. Distributed production, axial flow, nonlinear sorption, changing wax, coupled H2/CO gradients, and evolving catalyst state generally require more than one compartment. Extracting a single exponential does not prove that its fitted parameters describe the active-site environment.

### Storage can matter greatly, but its direction is not predetermined

Unchanged steady concentration does not imply unchanged irreversible damage. Different water histories can create lasting differences in cobalt state even if the eventual conditions become identical. Therefore, persistence of a benefit for 1200 h does not alone exclude an early-history mechanism.

Conversely, lower storage is not universally protective. In the simple model, reducing B accelerates approach to a harmful concentration after a source or humidity step upward; it also shortens the tail after a downward step. Greater storage can buffer a short challenge. The effect on damage depends on the waveform, the initial state, and the nonlinear damage and recovery kinetics. A startup-only explanation needs an exposure-history experiment, not an assumption that less stored water means less damage.

Also distinguish total bed inventory from water held at the catalyst. Removing adsorption capacity from an inert diluent does not necessarily change catalyst coverage at a fixed water activity. A persistent change in catalyst-specific uptake under equilibrated, common conditions points to altered accessibility, interface, or catalyst chemistry, beyond the simplest storage-only explanation.

### There is a maximum benefit from changing a remote resistance

If water leaves through unchanged internal resistance Rin and a promoter-sensitive external resistance Rout in series, the local excess is q(Rin + Rout) in the linear fixed-source limit. Eliminating Rout can remove at most qRout of that excess. A remote promoter cannot overcome a dominant, unchanged internal resistance or lower the local steady activity below the imposed reservoir solely by accelerating passive removal from a positive source.

This bound is useful only after identifying the relevant phase and pathway. Wax or water films may make what appears geometrically “external” kinetically dominant. Polymer contact may change that pathway, and local water can be consumed as well as produced. Such cases require a revised balance rather than treating the bound as universal.

### The operating geometry and liquid state must be preserved

The headline 2026 stability result uses separately prepared Co/SiO2 and PDVB granules mixed together. The Fig. 4 caption describes CT imaging of a granule made from a powder mixture. Powder co-granulation and mixing separate granules differ in contact area and intragranular paths. Resolve which geometry each characterization represents before using a pore network to explain the headline result.

Equal mesh size and bed volume are valuable controls, but do not uniquely fix void fraction, contact topology, tortuosity, or liquid distribution. SiC controls weaken a simple thermal-conductivity explanation; they do not directly measure local temperature profiles in all beds. Room-temperature contact angle is a descriptor, not proof of the working interface under hot syngas and retained hydrocarbons.

[Zheng et al., Nature Catalysis 2023](https://doi.org/10.1038/s41929-023-00913-8) demonstrates that the retained liquid in FT pellets can evolve long after the outlet appears steady. Its Ru/TiO2 system is not the Fang cobalt catalyst, so its times cannot be transferred as design constants. It does establish why wax-conditioned transport and startup deserve explicit attention. Read local evidence: [[zheng2023-operando-magnetic-resonance-imaging-of]] p.4 and p.10.

## A decisive first campaign

### 1. Reproduce the effect with enough normalization to interpret it

Use one catalyst batch and the separate-granule geometry of the headline result. Compare PDVB with the matched inert reference. Measure rates and selectivities on catalyst-mass and total-bed-volume bases, quantify inlet and outlet water, document gas residence distribution and pressure drop, and record temperatures. Use independent bed preparations for the central contrast. A shorter observation window is acceptable for the pilot if it contains clear reference deactivation and distinguishes reversible rate response from permanent loss; it cannot establish 1200 h stability.

Keep a limited powder-mixture comparison only if needed to resolve geometry dependence. Do not begin with a wide screen of polymers. The first gate is whether the material effect survives controlled preparation and whether its magnitude is sufficient for mechanistic discrimination.

### 2. Separate inventory from response time before assigning a conductance

Use calibrated water concentration steps up and down at fixed temperature, total flow, pressure, and other gas partial pressures; replace inert gas to change water. Measure complete input/output water balances, with reactor-line blanks and a nonadsorbing tracer to characterize gas holdup. Integrated uptake gives an incremental accessible inventory when source and sink terms are absent or independently accounted for. The response shape provides additional kinetic information. Equal final water conditions and reverse steps test equilibration and hysteresis.

First establish this measurement on supports and physical mixtures without ongoing water-producing chemistry. Repeat on a relevant conditioned material where possible. Do not transfer a dry-support B or G to a working FT catalyst without checking the effect of retained hydrocarbons and the reactive state. If both inventory and transfer dynamics change, report both. A single B/G fit should be retained only if spatial and multi-step checks support the approximation.

A separate steady permeation measurement can independently constrain conductance in a representative sample, but a membrane-like test fixture may introduce contacts absent from a loose bed. It is optional corroboration, not a substitute for testing the reaction geometry.

### 3. Use imposed water to distinguish source-generated gradients from chemistry at fixed exposure

Run a differential reaction regime with an externally imposed water background that dominates product-generated water, while holding H2 and CO partial pressures fixed. Independently characterize the unpromoted catalyst's reversible water response and damage over the accessible range. Compare promoted and unpromoted behavior after matched conditioning, then vary particle dimension or flow to reduce the water gradient that the proposed transport mechanism requires.

If the benefit decreases as the estimated source-generated gradient disappears, this supports a transport-mediated explanation. If a persistent benefit remains at equilibrated, common local exposure, the simple remote-conductance explanation is inadequate; examine catalyst/interface changes or an incorrectly assessed local environment. Neither bulk outlet humidity nor rate alone certifies equal active-site exposure. Use rate response together with catalyst-state information or calibrated water-sensitive spectroscopy where practicable, and state the remaining spatial uncertainty.

The imposed-water regime must remain mechanistically relevant. Very low conversion, unusual steam ratios, or wax-free fresh catalysts may test a different state from high-conversion operation. A negative result there is a mechanistic boundary, not automatically a refutation of the reported high-conversion effect.

### 4. Make exposure history a planned variable

Compare an upward water step, a finite pulse followed by recovery, and steady exposure, using matched initial catalyst states and measured delivered water. Measure residual catalytic function after a common recovery protocol. If feasible, compare promoter present during conditioning only with promoter present during the subsequent challenge; account for disturbance when separating granules.

Freeze predictions before the decisive runs. For example, a measured capacity change at unchanged G predicts different ingress and washout behavior, but no stationary source-generated gradient change in the simple model. A conductance increase predicts a smaller source-generated excess and a response dependent on where resistance lies. A persistent interface modification predicts retained differences after removing the promoter, subject to possible reversibility and handling artifacts. History dependence is established only when the measured sequence explains the retained functional differences.

Isotope experiments can support this stage after the water balance is understood. A syngas-to-Ar switch changes production, adsorption competition, and catalyst reduction conditions simultaneously. An H2O isotope switch avoids some perturbations but introduces isotope exchange with hydroxyls, oxygen species, and continuously generated water; label residence is not automatically water escape time. The existing SSITKA review remains relevant to these identifiability limits: [Shannon and Goodwin, 1995](https://doi.org/10.1021/cr00035a011), local [[shannon1995-characterization-of-catalytic-surfaces-by]] p.10 and p.17.

## What would justify a substantial program

A strong outcome would predict, before testing, the sign and useful magnitude of promotion when particle size, water source strength, conditioning history, or promoter placement changes. It would also predict an operating region where faster washout gives little durability benefit. A second catalytic system is valuable after this first predictive test; transfer is not established by fitting separate coefficients to each system after seeing the outcomes.

The practical comparison is against simpler ways to achieve the same retained productivity: appropriate granule size, dilution, water partial pressure, or a more hydrothermally stable catalyst. Include bed-volume productivity, cumulative useful product, pressure drop, regeneration compatibility, and the promoter's working lifetime. The initial activity penalty in the cobalt case must be recovered by useful output over the relevant operating interval. Do not assume catalyst-weight-normalized stability alone establishes a process advantage.

Stop or narrow the program if the reproducible effect is explainable by an ordinary change in dilution or conversion with no distinct capability, if transport and catalyst-state effects remain unidentifiable with accessible measurements, or if the proposed metric predicts only the calibration samples. An informative mechanistic rejection remains publishable in principle, but that possibility alone does not justify a large experimental platform.

## Source status and review limits

Primary material read for this review: supplied public 2026 main-article text, SI, transparent peer-review file, supplied original 2022 Science article, and local read notes for the MRI and SSITKA papers. The MRI and SSITKA claims above are confined to those documented notes; this review did not independently repeat their complete paper audits. The 2026 and 2022 anchors are being handled by the shared literature agent. The relevant SSITKA review already exists in the KB.

Two additional methodological works were identified and routed to the root for the single literature agent. Neither full text was read for this review, and neither supplies an unverified detailed claim above:

1. Barrer and Fender, “The diffusion and sorption of water in zeolites—II. Intrinsic and self-diffusion,” Journal of Physics and Chemistry of Solids 21, 12–24 (1961), [DOI 10.1016/0022-3697(61)90207-4](https://doi.org/10.1016/0022-3697(61)90207-4). Relevant as an experimental precedent for separating sorption and isotope-exchange measurements. No full text retrieved during this review.
2. “Diffusion in nanoporous materials with special consideration of the measurement of determining parameters (IUPAC Technical Report),” [DOI 10.1515/pac-2023-1126](https://doi.org/10.1515/pac-2023-1126). Relevant to definitions and measurement of diffusion parameters. A [lawful institutional full-text link](https://discovery.ucl.ac.uk/10201708/1/KargerCoppensWeckhuysen_PAC24.pdf) was located for the literature agent to retrieve and assess.

This review supports a staged development decision, not a claim that a new universal law, a practical improvement, or priority over all related hydrophobic-promotion studies has been established. The concurrently reviewed Cu physical-regulation literature remains necessary before making a broad originality claim.

## Independent review of the transport calculation and revised candidate

Follow-up review on 2026-09-16 of `research/calculations/water-transport-limits.md`, `water_transport_limits.py`, its JSON output, and the revised `research/working/program-development/physical-water-management.md`. Only this review file was edited. The script was inspected and its numerical output independently recalculated with a separate read-only calculation; its output file was not regenerated.

**Verdict: keep the calculation, but narrow its evidentiary role.** Its algebra, units and numerical results are correct within the assumptions. The dimensionless storage/conductance comparison is a clear counterexample and worth retaining. The sphere calculation is useful primarily as an inverse question—what effective resistance would be required for a specified exposure difference? The 93–883 Pa result should remain subordinate to that question. It is not a bound on the real catalyst, evidence that the real gradients are small, or evidence against the reported mechanism.

### Verified mathematics and source normalization

For uniform generation in a sphere, solving `D ∇²c + qv = 0` with a finite centre derivative and fixed surface concentration gives `c(r) − cb = qv(R² − r²)/(6D)`. The outward surface flux is `qv R/3`; multiplying by `4πR²` reproduces the integrated generation `4πR³ qv/3`. The centre excess is the maximum within this model. The volume-average excess would be `qv R²/(15D)`; neither is directly a measured active-site exposure.

The source normalization uses 2.4 L gas/(g catalyst h), 0.32 inlet CO fraction, 0.441 conversion, and 22.414 or 24.465 L/mol. It correctly gives 3.8455–4.1974 × 10−6 mol/(g catalyst s). The main article specifies 0.5 g Co/SiO2 with added PDVB and reports flow per g catalyst, which supports using the Co/SiO2 mass rather than cobalt-metal mass. The volumetric reference conditions are not established in the supplied source, so the 0 versus 25 °C calculation remains an explicit convention sensitivity, not a measured uncertainty interval. Approximating one water per converted CO is appropriate for the stated illustrative hydrocarbon-dominated oxygen balance, but it remains an approximation in the presence of CO2 and oxygenates.

The 0.5–1.5 g/cm³ density range converts correctly to 0.5–1.5 × 10⁶ g/m³. Multiplication gives 1.9227–6.2961 mol/(m³ particle s). With the selected radii and D, the independently recomputed centre-pressure range is 93.3214–883.1335 Pa. Converting Pa to bar and comparing with the chosen 1–4 bar background is correct. Every output row and its inverse diffusivity threshold reproduces the equations. The diffusivity required for a 10% centre excess spans 5.13 × 10−10 to 1.94 × 10−8 m²/s across the assumed cases.

The assumed 250–425 μm diameters correspond to No. 60 and No. 40 U.S. sieve openings, as listed in the [W.S. Tyler manufacturer catalog](https://wstyler.com/wp-content/uploads/2024/04/WSTyler-Test-Sieves-and-Particle-Analysis-Equipment-Catalog.pdf). The source reports “40–60 mesh,” not a verified sieve standard or equivalent spherical diameter. Thus 125–212.5 μm is a reasonable stated geometric scenario, not an exact reconstruction of these irregular granules. No claim about particle dimensions more precise than that is warranted.

The unit-time concentration integrals are also correct: 0.367879 for the reference, 0.567668 for lower storage, and 0.283834 for greater conductance. Their different ordering is a valid illustration of why equal washout times do not imply equal startup exposure. The script correctly avoids calling this concentration integral a cobalt-damage law.

### Clarifications needed before using the sphere example in decisions

1. **Define density as catalyst mass per granule-envelope volume.** Skeletal density and packed-bed density do not produce the same qv. For a co-granulate, catalyst mass per complete co-granulate volume is the required quantity. The present numerical choices are sensitivity assumptions, not density measurements.
2. **Define D by its concentration and flux basis.** Here c is mobile gas concentration per gas volume, qv is per full particle-envelope volume, and the effective D multiplies the macroscopic gradient to give flux per macroscopic particle area. Porosity, tortuosity and other pathway factors must already be incorporated consistently. The source's molecular self-diffusivity has no demonstrated conversion to this D. Identical SI units do not make those coefficients interchangeable.
3. **Do not describe the chosen endpoints as bounds on real gradients.** The source is a reactor-average generation rate at substantial conversion. Upstream local rates, activity distributions, internal reaction gradients, nonuniform catalyst loading and particle shape can differ. The chosen 1–4 bar water background excludes the nearly dry inlet limit; it is not a whole-bed range verified experimentally. At small cb, a relative excess can be large even when the absolute excess is small.
4. **The fixed boundary omits external resistance.** This example quantifies an assumed intragranular contribution only. It neither quantifies nor excludes an external film, intergranular boundary, wax interface, adsorption-mediated route, or multicomponent coupling. Those are especially relevant when the promoter is separately granulated.
5. **The 10% diagnostic threshold is arbitrary.** It may help set a measurement question, but it is not the required change for durability. A sharp redox or damage response could make a much smaller activity change consequential. Conversely, a large mobile-water difference may not affect the operative surface oxygen-removal rate.

I recommend foregrounding `D_f = qv R² RT/(6 f pb)` and the need to measure its inputs. Keep the borrowed 2.2 × 10−7 m²/s value explicitly counterfactual, or replace it with a generic sensitivity range if readers repeatedly mistake it for a measured property. The distinction is already substantially present in the calculation note; these clarifications prevent its memorable numerical result from becoming an unsupported mechanistic conclusion.

### Remaining material limits in the revised program

The revised program correctly incorporates the prior-art controls, geometry distinction, inventory/conductance ambiguity, isotope-exchange caveats, and startup-history mechanism. It is a defensible staged candidate. Three dependencies should remain visible:

- A stable, reversible water-response interval on the parent catalyst must be demonstrated. The source reference deactivates, so a calibration cannot simply assume that changing water leaves a fixed parent state. Brief perturbations, bracketed returns and separate damage challenges are useful only if the measured reference response actually returns.
- Cobalt oxidation and reduction depend on the reducing and oxidizing environment, including local H2O/H2 and CO-derived oxygen, rather than water alone. Fixed inlet H2 and CO do not prove fixed local values. A purported water-conductance rule must check whether the same packing or liquid change also alters H2/CO delivery. Otherwise a successful empirical rule may describe coupled transport while its water-only interpretation remains unsupported.
- Aggregate uptake plus outlet transients may not identify the water pool coupled to cobalt. Stage 2 should establish practical parameter identifiability before an extended predictive campaign. If multiple physically different parameter sets reproduce the same measurements but predict different protection, retain that ambiguity or obtain an independent constraint; do not select the preferred set by its later fit to deactivation.

These limits do not justify abandoning the candidate. They favor making the initial deliverable an experimentally distinguishable mechanism and a prospective operating-history or geometry prediction, with practical improvement assessed subsequently against the existing promoted recipe and simpler operating changes.
