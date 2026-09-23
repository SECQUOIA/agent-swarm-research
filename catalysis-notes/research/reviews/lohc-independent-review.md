# Independent review: productive inhibitor removal in MCH dehydrogenation

**Source and decision update, 2026-09-16:** This is a historical screen of an existing idea, not an active campaign. The [decision brief](../decision-brief.md) controls current priorities. Access statements and source-request lists below describe the original review unless explicitly updated; current access is recorded in the [literature status](../literature-status.md). Availability of a full text does not mean that every claim or benchmark in it has been rechecked. No new idea or experimental campaign is started by this update.

This review's original “advance a bounded feasibility study” recommendation predates the final portfolio selection and is superseded. LOHC remains nonselected. Tengco and Holcombe main texts are now retained and marked read; the old abstract-only descriptions record historical evidence access. Support carbon storage, productive molecular recycling and changing Pt accessibility must still be allowed to coexist. No native recycling-flux measurement or Pt-saving benefit has been established by this repository.

Date: 2026-09-15  
Scope: scientific novelty, identifiability, experimental feasibility, and practical value of testing oxide-mediated inhibitor recycling and a Zr–O intervention. No new experimental results are available. The proposed working draft was not present when this review began; this review evaluates the research premise supplied by the coordinating agent.

## Original recommendation (superseded by the update above)

**Advance a bounded feasibility study, not yet a full application program.** The useful question is whether a deliberately prepared oxide converts the carbon responsible for Pt inhibition into recoverable carrier molecules, with bounded carbon inventory and a sustained improvement in hydrogen production per gram of Pt. Merely observing a support effect, suppressing it with an acid-site titrant, or detecting toluene from a diene on an oxide would repeat established work.

The proposal has a credible mechanistic opening but two independent hurdles:

1. **Mechanistic:** distinguish sustained catalytic removal from reversible storage, irreversible deposition, direct Pt changes, and combinations of these processes.
2. **Practical:** show that an intervention preserves its advantage at useful conversion, product and hydrogen pressures, and operating duration, against a competent alumina-supported Pt benchmark.

Success on the first does not establish success on the second. A well-identified negative result could still explain why a tempting oxide intervention fails, but its scope should be a mechanistic study rather than a Pt-saving technology claim.

## 1. What is already known, and what could be new

### Established starting point

Chen et al. already describe oxide Lewis acid–base pairs scavenging desorbable forms of less reactive Pt-bound species. Their Scheme 3 explicitly includes conversion of these species to toluene on the support. The paper also measures reactions of added methylcyclohexene and methylcyclohexadiene on metal-free oxides. Therefore, **“the support catalytically converts an inhibitor” is already a published proposal with supporting experiments**, not a new hypothesis in its general form. [[chen2025-elementary-steps-and-bifunctional-scavenging]] p.11-14

The remaining uncertainty is sharper: the native inhibitor is not directly identified or quantified, and the proxy-reaction experiments do not establish a lifetime carbon partition between useful conversion and accumulation under native MCH dehydrogenation. Diene isomers are inferred as plausible shuttles after the authors exclude equilibrated methylcyclohexene as the relevant scavenged pool. The reported proxy feed is 4 Pa, whereas the native diene is below detection. The quoted equilibrium estimate is not a measured native concentration and should not be imposed as an actual concentration in an irreversible reaction network. [[chen2025-elementary-steps-and-bifunctional-scavenging]] p.5 p.13

Fischer and Iglesia provide prior kinetic and transport treatments of molecular inhibitor scavenging in the reverse, toluene hydrogenation reaction. They already distinguish the small inhibitor flux from the much larger increase in metal turnover. A large rate enhancement therefore does not imply that a large fraction of product carbon passes through the oxide. Their oxide diene experiments also show time-dependent deactivation and discuss possible oligomer formation at elevated proxy concentrations. [[fischer2023-the-nature-of-hydrogen-spillover]] p.8 p.13-14

**Source correction:** Fischer's `13CHD` means **1,3-cyclohexadiene**, not carbon-13-labelled cyclohexadiene; `14CHD` is 1,4-cyclohexadiene. The original local paper note misdescribed this as an isotope-labelled probe; the source correction is recorded here for continuity. Chen's PA is **propionic acid**, also called propanoic acid, not phenylacetic acid. These corrections have been sent to the coordinator for literature maintenance. [[fischer2023-the-nature-of-hydrogen-spillover]] p.4 p.8 [[chen2025-elementary-steps-and-bifunctional-scavenging]] p.9

### Recent work narrows the opportunity

The 2026 support-deactivation study compares SiO₂, Al₂O₃, TiO₂, and ZrO₂ and links stability to the location of carbonaceous residues, including migration to supports and removal of soft coke by hydrogenation. Its abstract identifies alumina as the strongest long-term benchmark and also reports an ensemble-modifying TiOₓ intervention. This directly anticipates a generic “protect Pt by moving carbon to the support” claim. Full-text review remains necessary before judging the detailed evidence for migration. [Tengco et al., Journal of Catalysis, 116959](https://www.sciencedirect.com/science/article/abs/pii/S0021951726002940).

A second 2026 study reports soft coke predominantly associated with the alumina support and worse deactivation after ammonia treatment masks acid sites. Consequently, loss of promotion after acid-site blocking is compatible with carbon management as well as useful molecular recycling. This review verified the institutional abstract, not the full experimental article. [Holcombe et al., Applied Catalysis A, 121061](https://inl.elsevierpure.com/en/publications/support-acidity-effect-on-coke-formation-in-platinum-catalysts-fo/).

The Zr–O work establishes a plausible intervention: DME treatment removes strongly bound titrants and exposes minority Lewis acid–base pairs with hydrogenation/dehydrogenation activity. However, the demonstrated substrates and conditions are not native methylcyclohexadiene scavenging. Cyclic/arene-side-chain examples are chiefly measured at 573 K and above, and strongly binding water and CO₂ suppress the competent sites. Generalizing from these experiments to selective diene recycling at 453–513 K is an experimental question. [[jaegers2024-heterolytic-ch-activation-routes-in]] p.4-9 [[jaegers2025-hydrogenation-of-alkenes-cycloalkenes-and]] p.6-7 p.15

### Defensible novelty statement

> Quantify the competing productive and accumulating carbon pathways responsible for oxide-mediated Pt protection, then test whether independently exposing Zr–O pairs shifts that partition and sustains hydrogen productivity at reduced Pt inventory.

This is narrower than discovering scavenging and stronger than another support ranking. The two directly overlapping 2026 full texts are now available. Their existence does not establish novelty for the retained flux question; this historical proposal remains nonselected under the final decision brief.

## 2. Mechanisms must be allowed to coexist

| Candidate process | Expected observation | What would distinguish it |
|---|---|---|
| Catalytic diene-to-toluene conversion | Product carbon continues leaving while total retained carbon becomes stationary | Sustained carbon-resolved output beyond measured storage capacity; oxide-only competence; a coupled-system causal intervention |
| Reversible support storage | Uptake followed by delayed release; history-dependent promotion | Inert and reactant pulse/chase measurements, finite recoverable inventory, breakthrough |
| Irreversible oligomer/coke accumulation | Persistent retained carbon; capacity-dependent lifetime | Destructive carbon inventories at several operating times, spent-support swap, regeneration balance |
| Carbon-pool-mediated catalysis | A support carbon inventory persists but turns over | Isotope replacement and sustained product flux without growth of total inventory; test whether the pool is necessary |
| Pt electronic, structural, or ensemble change | Promotion depends on treatment/contact and Pt properties | Pretreat oxide separately, use one parent Pt batch, compare remote mixtures and supported Pt, examine Pt before/after |
| Direct oxide conversion of ordinary feed/intermediates | Added oxide increases product rate without relieving inhibition | Oxide-only rate bounds at matched partial pressures and isotope attribution |

A carbon pool that reaches constant mass is not automatically inactive coke. Conversely, label appearing in product is not proof that the oxide is free of irreversible deposition. Report flux fractions and inventory changes rather than forcing a binary interpretation.

## 3. Minimal decisive experimental sequence

### A. Establish a controlled material and reactor comparison

Use a single characterized Pt/SiO₂ parent batch with independently prepared additives: inert SiO₂, Al₂O₃, untreated monoclinic ZrO₂, and DME-treated monoclinic ZrO₂. Add a competent Pt/Al₂O₃ benchmark for practical comparison. Treat ZrO₂ separately and purge it before combining it with Pt; otherwise DME exposure of Pt becomes a competing intervention. Verify residual carbon and oxygenates after preparation.

Hold Pt amount, aggregate size, bed dilution, residence time, and measured temperature constant for the initial mechanistic comparison. Use more than one additive loading and at least two controlled mixing distances. Do not equate BET area with competent site count. Report area, mass, an independently measured site-capacity proxy, and activity. Water titration of ZrO₂ can establish a relevant site population in its own probe reaction, but it must not be assumed to count exactly the diene-active population.

Begin near the Chen conditions, then include 493 K to overlap the 220 °C deactivation literature and at least one hotter operating condition appropriate to the intended application. Track raw time-on-stream rates. Chen's corrected kinetic rates refer to a chosen partially covered state and cannot substitute for an uncorrected lifetime productivity measurement. [[chen2025-elementary-steps-and-bifunctional-scavenging]] p.4 p.8-9

An upstream oxide guard bed tests removal of feed impurities; a downstream bed tests independent processing of effluent. Neither replaces an intimate-mixture test. In directed flow, a downstream oxide may not change the inhibitor concentration near upstream Pt, even if it is a good scavenger. A null result there is not sufficient to reject molecular coupling.

### B. Establish oxide-only carbon fate before buying a complex isotope campaign

Feed available MCHD isomers individually over oxide-only beds, with the MCH/TOL/H₂ background controlled. Include empty-reactor, SiO₂, Al₂O₃, and Pt-only controls. Verify feed purity and delivery stability; dienes can react before reaching the catalyst. Calibrate all available isomers and capture condensable/oligomeric material in the downstream train.

Measure a dose series down to the lowest quantitatively defensible level. High-dose oligomerization can dominate a scarce native diene reaction, while an apparently selective low-dose response may merely fill a large reservoir. Require repeated pulses and continuous-feed segments through measurable breakthrough or repeated turnover. Neither one clean pulse nor initial selectivity establishes catalysis.

Measure toluene, all resolved MCHE/MCHD isomers, MCH, benzene, light gases, heavy products, and retained carbon. With an isolated C₇H₁₀ diene feed, toluene formation can release one H₂ per molecule, MCHE formation consumes one, and MCH formation consumes two. Thus, after correcting for other products and inventory changes:

`net H₂ = toluene formed − MCHE formed − 2 × MCH formed`.

Toluene alone does not establish net dehydrogenation: disproportionation can also make it. In the mixed feed, the corresponding small H₂ increment can be obscured by much larger Pt production and by hydrogen exchange, so use the isolated experiment to constrain this pathway.

### C. Close a labelled-carbon balance, including the solid

If oxide-only results justify the expense, use a verified carbon-labelled MCHD, preferably uniformly labelled, in otherwise unlabelled feed. Confirm actual procurement or synthesis feasibility before scheduling this as an essential deliverable. If only a different diene is available, label the result explicitly as a proxy test.

For each interval, calculate in moles of carbon-13 atoms:

`label admitted = label in gaseous/liquid effluent + change in retained label + label recovered from lines/traps`.

Correct natural abundance, isotope enrichment, fragmentation overlaps, feed carryover, and gas residence-time response. Account for unreacted labelled diene separately from product label. Report carbon selectivity on converted tracer and the cumulative unresolved label fraction. Set the analytical precision against the **tracer-carbon flux**, not total MCH throughput: ordinary bulk carbon closure can hide the whole inhibitor branch.

Use isotope switches at unchanged total diene concentration, followed by an unlabelled chase at unchanged chemical conditions. An inert switch defines line and pore hold-up. Matched sacrificial beds stopped at several times provide total carbon and isotope inventory; calibrated oxidation with isotope-resolved detection can quantify retained carbon. Trap analysis and extraction recover material that would otherwise disappear from the balance.

The essential conjunction is sustained labelled-product formation, a bounded **total** carbon inventory, and repeated isotope replacement. Labelled toluene alone could result from direct Pt conversion or release of previously stored label. A falling labelled inventory alone could conceal simultaneous deposition of unlabelled MCH-derived carbon. Avoid using TPO peak temperatures alone to assign carbon to Pt versus support: oxidation kinetics and metal proximity also affect them.

### D. Connect probe chemistry to native Pt protection

Return to unspiked MCH after each perturbation and compare the raw rate and deactivation trajectory. Determine whether trace MCHD dosing changes Pt activity over a range that remains analytically and kinetically controlled; assess whether oxide addition attenuates the same response. Extrapolation from a strong inhibitor dose to the unknown native pool must retain uncertainty.

Separately block or rehydrate the oxide before assembly; then show the loss of both oxide-only productive conversion and coupled promotion. Include the same treatment on Pt-only material and inert additive. On-stream propionic acid, water, or CO₂ can affect adsorption and Pt chemistry, so their response is not a standalone selective-site proof.

Preload the support with a known carbon exposure, purge it, and compare it with fresh and regenerated support while retaining the same Pt component. Loss of benefit after exhausting measured capacity supports a storage explanation; recovery after regeneration establishes reversibility, not necessarily productive recycling. A support-swap experiment is especially informative when support and metal can be separated without changing bed transport.

Isotopically switching native MCH can reveal long-lived carbon pools, but the large ordinary Pt-to-toluene flux will dominate. It does not identify the scarce inhibitor without additional kinetic or molecular evidence. If native identity remains inaccessible, the conclusion must remain “consistent with productive removal of a diene-like inhibitor,” not identification of one definitive molecular shuttle.

## 4. Identifiability and modeling requirements

Fit the smallest dynamic model that includes a metal inhibitor pool, an oxide reversible pool, productive oxide conversion, and irreversible accumulation. Begin with nested models rather than fitting all elementary constants at once. Constrain oxide rates and capacities with oxide-only experiments, hydrodynamics with the inert tracer, and total retained carbon independently.

A rate-enhancement curve by itself cannot separate inhibitor formation, desorption, readsorption, oxide capacity, and oxide conversion. Steady-state site coverage probes also cannot assign carbon identity. Report which parameter combinations are identifiable and which competing mechanisms remain compatible with the uncertainty.

Do not require the carbon recycled through the oxide to equal the additional toluene produced on Pt. Inhibitor removal can unlock many subsequent Pt turnovers. The relevant relationship is sufficient inhibitor removal to sustain the observed change in Pt coverage and rate. Conversely, a very small estimated inhibitor flux means a finite support reservoir can last a long time: elapsed hours alone cannot prove catalytic turnover.

## 5. Practical benchmarks and decision gates

### Benchmark choice

Pt/SiO₂ is a mechanistic reference, not a sufficient practical comparator. At minimum compare against competent Pt/Al₂O₃ with matched feed, conversion, temperature, Pt inventory, and bed volume. A second benchmark should address a distinct stabilization strategy if it is accessible.

Zeolite-confined PtFe is a meaningful published challenge: the reported study claims >2000 h stability and high-purity hydrogen, with separate short-run evaluations at 350 °C and high-space-velocity tests at 400 °C. These data must be compared at their actual conditions rather than treating the longest duration and highest rate as one operating point. The DOI includes 2024, but the paper was published in 2025. [He et al., Nature Communications](https://doi.org/10.1038/s41467-024-55370-z).

Sulfur-modified Pt is another relevant mechanistic alternative. A 2026 DFT/microkinetic study attributes improved selectivity and activity to altered neighboring adsorption and promoted toluene desorption. It is a competing explanation and design principle, not by itself a demonstrated long-duration process benchmark. [Zaar et al., institutional publication record](https://research.chalmers.se/en/publication/552120).

Report usable hydrogen produced per gram of Pt over the complete run, including regeneration downtime; hydrogen purity and recoverable carrier yield; product distributions; additive mass and bed-volume penalty; and Pt surface/site-normalized rates as a separate mechanistic metric. Verify the selected reactor comparison is not dominated by heat or mass transfer. A reduction in Pt inventory has to maintain required hydrogen flow and purity; a larger per-site turnover frequency alone is insufficient.

The temperature dependence is a material risk: Chen reports declining support enhancement as temperature increases. Enhanced high-temperature ZrO₂ reactivity could arrive precisely where ordinary supports already remove inhibitors well. Exposing more competent Zr–O sites also offers no benefit once inhibitor desorption from Pt sets the ceiling. [[chen2025-elementary-steps-and-bifunctional-scavenging]] p.12 p.14

### Proposed gates

These are project decision rules to preregister after analytical commissioning, not thresholds established by literature.

| Gate | Advance criterion | Reject or pivot criterion |
|---|---|---|
| Analytical feasibility | Quantify product carbon and retained carbon with uncertainty small enough to distinguish the proposed pathways | Unresolved tracer loss is comparable with the claimed recycled fraction: fix analytics before mechanistic interpretation |
| Oxide competence | Reproducible useful conversion at relevant temperature/background, with repeated turnover and quantified side products | Only transient uptake, or useful chemistry only at irrelevant high dose/temperature: stop the proposed recycling intervention |
| Finite-storage exclusion | Productive throughput exceeds a defensible upper bound on reversible storage several-fold, with stationary total inventory and repeated isotope replacement | Continued carbon accumulation, capacity-scaled benefit, or no defensible capacity bound: retain a storage/mixed interpretation |
| Native causality | The independently controlled oxide state changes productive probe chemistry and native Pt protection in the same direction, beyond direct/additive-rate and Pt-change explanations | Probe chemistry changes without native benefit: stop claiming the probe is the controlling native shuttle |
| Zr–O intervention | Treated ZrO₂ improves lifetime productivity over untreated ZrO₂ and the alumina benchmark without compensating carrier loss or bed penalty | Only extra fresh-surface capacity or temporary cleanliness helps: pivot to regeneration/carbon-management economics |
| Practical Pt saving | Prespecified reduction in Pt maintains required hydrogen flow, selectivity, and uptime under the selected application conditions | Advantage disappears at useful conversion or after realistic trace-contaminant exposure: retain a mechanistic result, reject the application claim |

Start with a 24–72 h screen only as a down-selection exercise; the decisive exposure is throughput relative to capacity. Advance a survivor to repeated regeneration and substantially longer runs appropriate to the claimed service interval. A small laboratory campaign cannot establish superiority to a multi-thousand-hour benchmark from a few dozen stable hours.

## 6. Resources and scope discipline

The first phase needs controlled feed delivery, quantitative GC/FID and H₂ detection, calibrated collection of heavy products, and post-run carbon measurements. The isotope phase additionally needs GC–MS or equivalent resolved label detection, carbon-isotope inventory measurement, and labelled-substrate access. These capabilities have not been confirmed.

Operando spectroscopy and advanced microscopy can test specific remaining alternatives after the kinetic/carbon tests. They are not substitutes for a balance and should not be prerequisite screening tools. Avoid beginning with a large oxide library or a comprehensive DFT surface search: first establish that the controllable ZrO₂ state performs the required chemistry and matters in the coupled system.

**Overall assessment:** scientifically worthwhile as a disciplined test of carbon fate and the limits of oxide promotion. The application case remains speculative until productive turnover, native-system relevance, and lifetime Pt savings pass separate gates. The most important positive result would be a quantitative carbon partition plus a reproducible intervention; the most important negative result would identify why an apparently catalytic support benefit is actually finite or operationally irrelevant.
