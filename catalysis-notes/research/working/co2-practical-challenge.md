# CO/CO2 hydrogenation challenge to the current priorities

**Source and decision update, 2026-09-16:** This is a historical screen of an existing idea, not an active campaign. The [decision brief](../decision-brief.md) controls current priorities. Access statements and source-request lists below describe the original review unless explicitly updated; current access is recorded in the [literature status](../literature-status.md). Availability of a full text does not mean that every claim or benchmark in it has been rechecked. No new idea or experimental campaign is started by this update.

Chai's [carbide isotope-exchange paper](../../literature/papers/chai2022-isotopic-exchange-study-on-the/paper.md) is now retained and marked read in the KB. The pore-CO calculation remains an analytical counterexample, not evidence that the focal iron catalyst was transport limited. The old comparison against two first campaigns is superseded; this screen remains nonselected.

**Decision, 2026-09-15:** Neither candidate below is selected in the current portfolio. Retain one bounded mechanistic test: determine whether particle-scale CO retention accounts for an apparent direct CO2-to-hydrocarbon route on promoted iron. Its possible value is a rule for choosing catalyst proximity and pellet dimensions. Present evidence does not establish a substantial performance opportunity. A methanol nitrogen-impurity program is more immediately practical but has substantial prior art and an unverified low-concentration gap.

This was a bounded challenge, not a comprehensive COx review. Existing knowledge-base opportunities involving generic dynamic interfaces, water management, carbide facets, and pore liquids were treated as prior work. No experiments were performed.

## 1. Retained candidate: locate the CO intermediate before designing a tandem iron catalyst

### Consequential question and connection

Does CO2-derived carbon reach chain growth through a retained surface intermediate, through CO in catalyst pores, or through CO that equilibrates with the bulk gas? The distinction could determine whether mixing an RWGS catalyst with an FT catalyst helps, whether pellet dimensions should retain CO, and whether a separate iron-oxide component is needed. Iglesia's work on coverage, isotope kinetics, and reaction–diffusion effects provides a direct intellectual connection. The proposed question concerns intermediate transfer, not a new claim that iron carbide can activate CO2.

### Evidence and prior-art constraints

- **Existing evidence:** Fedorov et al. infer a direct C2+ route from nonzero zero-conversion selectivity on Fe–K and Fe–K–Mn; their strongest extrapolated C2+ fractions are roughly 29%. Bed-segment analysis and spent-phase measurements support their interpretation but do not identify an elementary intermediate. Their methods vary flow after conditioning; the unpromoted-Fe intercept is statistically inconclusive. See [[fedorov2023-elucidating-reaction-pathways-occurring-in]] pp.3–7, 8–11; [DOI](https://doi.org/10.1016/j.apcatb.2023.122505). Source text was reread.
- **Contrary or qualifying evidence:** Badoga et al. already cofed 13CO2 with CO/H2 on promoted iron. They detected label in CO and C1–C4 hydrocarbons and interpreted it as RWGS followed by FT. Their preproof also discusses much older, conflicting tracer results. These are different catalysts and feeds, so they do not refute Fedorov. Label in both products also does not, by itself, prove that every hydrocarbon precursor desorbed as CO. See author-posted [primary preproof](https://www.researchgate.net/publication/348596940_New_mechanism_insight_for_the_hydrogenation_of_COCO2_gas_mixtures_to_hydrocarbons_over_iron-based_catalyst), printed pp.3, 5–6; [DOI](https://doi.org/10.1016/j.catcom.2021.106284).
- **Recent primary prior art:** Li's 2025 thesis already studies K-promoted, initially phase-pure χ-Fe5C2 for CO2-FT and attributes activity to carbide rather than a required oxide partner. At 250 °C and 20 bar, its Fe–4.5K sample gives about 16% CO2 conversion and 56% C5+ selectivity after 20 h; the denominator and full product distribution must be preserved in later benchmarking. The thesis also separates carbon pools by isotope transients. These results remove novelty from simply proposing carbide-only CO2 conversion or carbon-pool measurements. See [thesis](https://pure.tue.nl/ws/portalfiles/portal/360421007/20250630_Li_S._hf.pdf), printed pp.73–98, 141, 147–148, 160. This is a thesis chapter, not an assumed peer-reviewed article.
- **Measurement constraint:** Chai et al. directly study carbon exchange between iron carbide and gas-phase carbon. Thus a slow product isotope transient need not report the lifetime of a single adsorbed CO intermediate. Their [primary paper](https://doi.org/10.1021/acscatal.1c05634) is queued for full reading; the abstract and source excerpt establish the relevance, but the detailed assignment is not independently endorsed here.

### Proposed hypothesis and an explicit counterexample

**Hypothesis:** At least part of the apparent primary hydrocarbon selectivity arises because CO formed inside a particle is consumed before escaping. This is unvalidated. Alternatives are surface transfer without CO desorption, a genuinely different oxygenated pathway, or a mixture whose contributions change with coverage and carbide state.

A simple model shows why the question matters. Consider a spherical particle of radius R, uniform CO generation rate q, first-order CO consumption kC, constant effective diffusivity D, and zero external CO concentration:

\[
D\nabla^2 C-kC+q=0,\qquad C(R)=0.
\]

The fraction of internally generated CO consumed before escape is

\[
f_{\mathrm{consume}}=1-\frac{3}{\phi^2}(\phi\coth\phi-1),
\qquad \phi=R\sqrt{k/D}.
\]

This fraction remains nonzero as total bed conversion tends to zero while the particle remains unchanged. For small φ, it is approximately φ²/15. All hydrocarbon carbon can therefore pass through pore-gas CO while showing a nonzero bulk zero-conversion intercept. This is an analytical counterexample under stated assumptions, not a fit or a claim that Fedorov's experiments were diffusion limited. Reactant diffusion criteria alone do not establish that a locally formed intermediate escapes without reaction.

Root source check: the focal paper explicitly allows CO2 activation to CO on the same site or a nearby ensemble (p.6); its term “direct” must not be paraphrased as proving the absence of a surface CO intermediate. The proposed counterexample instead concerns desorption into pore gas followed by recapture. The reported fixed-bed catalyst fraction is 0.25–0.45 mm (p.3); no particle-size test was located in the main-text methods. This does not establish that its particles were transport limited.

Neither this counterexample nor isotope incorporation distinguishes a surface CO* route from a CO-free elementary pathway. Use the specific term **bulk-gas-CO-bypassing flux** when that is the observable claim.

### Bounded first campaign

1. **Reproduce one consequential contrast.** Use Fe–K or Fe–K–Mn from the focal study and one independently prepared carbide-rich reference. Establish stationary carbon balances and catalyst state at the chosen conditions. Quantify carbon in wax and retained solids, not only light products.
2. **Vary intermediate escape while holding chemistry as nearly fixed as possible.** Compare several crushed particle fractions from one batch and several catalyst dilutions at matched local temperature and low overall conversion. Check that crushing does not change carbide fraction, accessible activity, potassium distribution, or pore structure. Vary flow and bed mass separately; they change external transfer and axial residence differently. Extrapolation alone is insufficient.
3. **Measure isotope transfer without changing chemical feed.** At fixed CO2/CO/H2 composition, perform independent 12C/13C switches in CO2 and CO, with an inert residence-time tracer. Fit CO, CO2, and C1–C3 isotopologue responses together. Repeat at two particle fractions. Include carbon-pool exchange and gas holdup explicitly; do not assign every tail to a productive adsorbate.
4. **Use a held-out test.** Predict the size or dilution dependence before measuring it. A model requiring an arbitrary new site distribution for every size has not established intermediate transfer. If the responses cannot distinguish pore CO from a retained surface pool, report that identification limit and stop structural catalyst design.

The smallest useful result is a bound on how much chain-growth flux could depend on pore-gas CO. A statistically nonzero intercept is not the success criterion.

### Practical benchmark and continuation rule

Only after establishing a transfer dependence should a larger campaign compare (a) the original promoted-iron catalyst, (b) a deliberately separated RWGS/FT pair, and (c) a controlled proximity arrangement. Compare useful carbon-product throughput, methane/CO loss, H2 consumption, and deactivation at matched conversion, feed, local temperature, and total catalyst inventory. Pellet benefits must survive heat-transfer and pressure-drop constraints. A higher C5+ fraction with lower total useful production is insufficient.

The phase-pure iron α-olefin result in [Wang et al., Nature 2024](https://doi.org/10.1038/s41586-024-08078-5) is a necessary comparator; it has been identified but not read here. Do not claim superiority before its operating basis and durability are checked. Existing Iglesia pellet-selectivity work also makes the general idea of beneficial intermediate retention established rather than new: [[iglesia1993-selectivity-control-and-catalyst-design]] pp.43–56.

**Stop:** If particle effects vanish after external-transfer/temperature controls, or if matched isotope responses identify no material gas-transfer contribution, stop the pore-retention hypothesis. A remaining surface mechanism question does not automatically justify a new materials library. If retention matters but deliberate proximity gives no useful throughput or selectivity advantage, preserve the design limit rather than relabeling a diagnostic as a practical advance.

### Confidence and priority

| Judgment | Assessment |
|---|---|
| Scientific hypothesis | Plausible, weakly supported for the particular catalysts. The counterexample establishes logical possibility only. |
| Feasibility and informative value | Moderate. Particle/dilution kinetics are accessible; isotope resolution, carbon reservoirs, and changing carbide state complicate causal identification. |
| Meaningful practical improvement | Low on current evidence. Carbide-only chemistry and particle-mediated selectivity are already demonstrated in related contexts; no specific lost performance has been quantified. |
| Decision | Retain as a bounded mechanism/transport alternative; do not promote above the reviewed Ag/polymer investigations. |

## 2. Rejected as a new lead: a nitrogen-impurity budget for CO2-to-methanol

### Initial proposition

**Proposed hypothesis:** Low concentrations of NH3 or capture-derived amines create a slowly accumulated interfacial defect that a short reversible poison pulse misses. Establishing whether damage depends on instantaneous concentration, cumulative nitrogen dose, or chemical identity could reduce unnecessary purification while protecting a commercial Cu/ZnO catalyst.

The natural first experiment would compare low/long and high/short exposures with equal nitrogen dose, followed by the same clean-feed recovery; measure complete nitrogen products, methanol loss, and an independently measured interfacial change. A practical benchmark would be the same commercial catalyst with a simple upstream removal step, including the latter's replacement or regeneration requirement. This is experimentally concrete and connected to Iglesia's site-specific kinetics.

### Why it does not displace the current priorities

Reversible NH3/methylamine inhibition, selective interfacial poisoning, and reaction of NH3 to methylamines are already established at 60 bar in [[laudenschleger2020-identifying-the-nature-of-the]] pp.2–6. More decisively, Bie et al. already compare immediate inhibition with long-term irreversible deterioration and investigate mitigation by NH3 decomposition. Their methanol test at 250 °C/30 bar shows inhibition by 1.4% NH3; the severe 100 h irreversible result is under **400 °C RWGS conditions**, not demonstrated long-term methanol synthesis. See [primary full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11937992/), sections “Alteration of the RWGS Reaction Pathway by NH3 Addition” and “NH3-Induced Long-Term Deactivation of Cu/ZnO/Al2O3,” Figure 1E–F and Figure 3; [DOI](https://doi.org/10.1021/jacsau.4c01097). HTML was read; printed-page locations were not verified.

A low-concentration methanol durability gap may remain, but the present search does not establish it or show that purification is materially overdesigned. Also, amines are not uniformly incompatible: integrated capture/hydrogenation has been demonstrated with tertiary-amine liquids and Cu/ZnO/Al2O3, although this is a different phase and process. [Suhail et al. 2024](https://doi.org/10.1021/acs.langmuir.3c03902), abstract only in this screen.

**Confidence:** High that nitrogen chemistry can impair activity; uncertain that a distinct irreversible mechanism matters at credible residual concentrations. Moderate to high feasibility for a specified feed. Low confidence in substantial practical improvement without measured impurity distributions and a cleanup-cost comparison. **Decision:** Do not promote a generic nitrogen tolerance or NH3 pre-decomposition program. Reopen only with an actual feed specification, a consequential unresolved lifetime loss, and full prior-art review.

## Note added 2026-09-16: the CO-addition policy on Ni

Hu, Tate and Iglesia 2025 ([[hu2025-a-mechanism-based-strategy-for]], 10.1021/jacs.5c04698) propose adding CO at a predicted steady-state pressure to suppress intraparticle CO gradients and obtain near-exclusive CH4 on Ru, Co and Ni at 483–573 K, and state that the small CO amounts can be recycled from effluent. The paper does not discuss Ni carbonyl formation under deliberate CO at the low end of that range; that hazard is an inference recorded by the [open-problems screen](direction-search/stated-open-problems-2026.md), not a finding. Any practical use of the policy on Ni needs a stated temperature floor and a Ni balance. This is a caveat on the retained CO-transfer diagnostic, not a new direction.

## Source handling

All missing sources were sent to the parent for the one reusable literature-maintenance agent. No knowledge-base files were changed. Research-only downloads are in `/tmp/co2-practical-challenge/`; the file named `nh3.pdf` is an HTML response and must not be ingested as a PDF. Relevant sources encountered but not read in detail were also routed for metadata inclusion. No unread result is treated here as proof of a detailed mechanism or a performance advantage.

## Independent algebra check by the parent

Solving the stated spherical boundary problem gives `C(r) = (q/k)[1 − (R/r)sinh(φr/R)/sinh(φ)]`, with the finite center limit. Its integrated escape fraction is `3(φ coth φ − 1)/φ²`; subtracting it from one gives the reported consumption fraction. The small-φ expansion is φ²/15. This confirms the counterexample mathematically, while leaving its applicability to the focal catalysts untested. No fitted diffusivity, kinetic constant or experimental attribution follows from this check.
