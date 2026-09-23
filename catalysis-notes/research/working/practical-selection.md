# Practical selection challenge: which catalyst uncertainty deserves the first experiment?

2026-09-15. Assessment of `zeolite-screen.md`, `alternative-screen.md`, and `oxide-screen.md`, using their cited evidence and additional primary-source checks. Proposed experiments are not results. No full process simulation or cost estimate is claimed.

**Status of this working assessment:** this records the initial selection rationale. The [decision brief](../decision-brief.md) and [developed styrene program](../programs/zirconia-styrene-oxygen-fate.md) supersede its experimental order: calibrated native-product discovery precedes specialist isotope closure, and the zeolite alternative is now an assay-history validation pilot. The later independent reviews also require net oxygen export, source-specific moisture accounting and carbon-diversion accounting before practical claims.

## Decision

**The most justified new oxide experiment is an oxygen-balance test of ethylbenzene-assisted regeneration of Zr–O pairs, followed by a test of the cleaning products in a product-rich/recycle-relevant feed.** It is more consequential and more directly testable than the original LOHC inhibitor-recycling proposal. The question is whether the observed self-cleaning exports oxygen harmlessly, or converts water into oxygenated aromatic species that later block sites, make deposits, or return with recycle.

This does **not** justify a large “water-tolerant zirconia” synthesis program. Nor does it establish that zirconia will outperform industrial styrene catalysts. The early experiment has a stronger justification than the performance forecast: it tests an unclosed chemical balance on which sustained bare-pair catalysis already depends.

Among all three screens, retain the polymer component-rescue experiment and the zeolite matched-history experiment as useful bounded alternatives. The polymer program addresses a potentially process-stopping catalyst-lifetime issue, but has substantial unresolved prior-art and feed-accounting risks. The zeolite program has broad potential leverage and a clean null experiment, but no evidence yet that a useful recovery interval exists. The original MCH/LOHC program ranks lower because durable alternatives are mature, support scavenging is already established, and the native inhibitor flux may be exceptionally difficult to measure.

There is no defensible basis for an unconditional ranking of dollar losses across these platforms. The relevant uncertainties, process maturity and evidence are too different. Rank the **first information-producing experiments**, then let measured benefit and existing alternatives decide the research investment.

## 1. Correcting the first oxide screen

Trace-water sensitivity is real; its practical consequences are substrate-dependent.

Artsiusheuski et al. report ethylbenzene dehydrogenation on zirconia reaching approximately 70% of its initial DME-activated rate with rigorously purified feed assigned an estimated water level of 4 ppm. Their model predicts approximately 95% at 1 ppm. He-treated and DME-treated specimens approach the same asymptotic rate with a given purified feed. The stable interval reported in the main text exceeds 50 ks, about 14 hours. **The 1 ppm result is a prediction, the water concentrations are inferred from site counts/transients, and the duration is not an industrial lifetime.** [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]] p.6-8.

I visually checked original PDF p.8, including Figure 6, against the extraction and corrected item 6 of `oxide-screen.md`. The text explicitly attributes persistent activity to ethylbenzene-assisted cleaning. The generic statement that ppm water rules out useful bare Zr–O catalysis would therefore be wrong.

A more important limitation appears on p.7. The cleaning products, called X, were below detection. The authors suggest aromatic hydroxylation or side-chain hydrolysis and infer that ethylbenzene predominates as scavenger at the low conversions tested, 0.5–2%. These are plausible assignments, not a measured oxygen balance. The reported catalyst comparisons also extrapolate zirconia rates from its kinetic laws to conditions used for other catalysts; they are not all simultaneous side-by-side reactor tests. [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]] p.5-7.

The new chemical uncertainty is thus **what becomes of the oxygen that must leave the active pair**, and whether the same site-recovery mechanism remains beneficial when styrene, recycling impurities, and carbon deposits matter. Scheme 1 assumes X binds much more weakly than water; that is not a measured adsorption comparison. The subsequently retrieved [SI](https://doi.org/10.1021/acscatal.5c04904.s001), p.6, confirms a total-gas mole basis for the inferred water ppm. SI p.10 explicitly assumes X is irrelevant to further transformations, leaving its actual fate open. SI p.9 confirms that the tabulated zirconia comparisons are extrapolations. The inferred moisture concentrations still require independent measurement before sizing cleanup.

## 2. What thermodynamics does and does not imply

### Bare-pair stabilization in genuinely wet feeds is a demanding materials target

The 2026 Zr(O)2 adatom calculation finds hydroxylation favorable above roughly 10^-7 bar H2O at 773 K, and predicts an effective dehydrogenation barrier increase from 1.82 to 2.32 eV as water pressure increases from 10^-8 to 10^-4 bar. These values concern one modeled site/network, not a measured universal water specification. [[ammal2026-mechanistic-insights-into-light-alkane]] p.11-12.

At fixed temperature, shifting a hydration crossover by pressure factor f requires a free-energy change of `RT ln(f)`, if the same one-water hydration stoichiometry applies. At 773 K:

| Pressure increase relative to 10^-7 bar | Required shift of relative hydration free energy |
|---|---:|
| To 10^-5 bar, about 10 ppm at 1 bar | 30 kJ/mol |
| To 10^-3 bar, about 1000 ppm at 1 bar | 59 kJ/mol |
| To 0.1 bar, a wet process | 89 kJ/mol |

These are thermodynamic scales calculated here, not achievable material improvements. Likewise, a 0.50 eV barrier increase corresponds to a rate factor of about 5.5 × 10^-4 at 773 K if all other factors remain the same. The calculation makes a broad claim of “water tolerance by modestly weakening adsorption” suspect. The low coordination that binds water also stabilizes useful C–H activation; weakening both can erase the catalytic advantage.

The same calculation does not contradict substrate-assisted cleaning: a reacting hydrocarbon supplies another route that changes the site balance. Its rate and material cost must be measured. A permanently hydroxylated catalyst with an alternative active pathway is also a different hypothesis, not proof that bare pairs survived.

A hydrophobic coating is not automatically a solution. At gas-phase equilibrium, a passive shell cannot indefinitely maintain an arbitrarily lower water chemical potential at an accessible strongly binding site. A useful coating would have to change adsorption thermodynamics, impose verified selective transport under reaction, or alter the working site. Each could also obstruct hydrocarbons or remove the very pairs of interest. Do not start there.

### Trace impurity loading is not the same as bulk steam duty

A simple inventory bound illustrates why inlet ppm alone does not decide feasibility. The reported 0.55 pairs/nm2 and a representative reported surface area of 130 m2/g correspond to about **0.119 mmol pairs/g**. These values come from the zirconia hydrogenation study and are an illustrative inventory, not an exact count for every ethylbenzene catalyst. [[jaegers2025-hydrogenation-of-alkenes-cycloalkenes-and]] p.2 p.7.

If every incoming water molecule permanently blocks one pair and no cleaning occurs, then

`t_capacity = N_pairs × X × y_HC / (r_HC × y_water)`.

Here r_HC is net hydrocarbon consumption per catalyst mass, X is conversion, and y denotes inlet mole fraction. For an illustrative r_HC = 0.010 mol/g/h:

| Assumed operation | 1 ppm H2O | 10 ppm | 100 ppm |
|---|---:|---:|---:|
| Undiluted hydrocarbon, X = 0.30 | 3560 h | 356 h | 36 h |
| y_HC = 0.20, X = 0.05 | 119 h | 12 h | 1.2 h |

These are full-capacity exhaustion times, not predictions of useful lifetime; significant rate decline begins earlier, and water adsorption need not be irreversible. The chosen rates/conversions are scenario assumptions, not measured zirconia performance. The point is that dilution, throughput, capture probability, and self-cleaning change the implication of “1 ppm” by orders of magnitude.

If incoming water is exported as one oxygenated hydrocarbon per water molecule, its minimum associated hydrocarbon loss is likewise governed by impurity loading and cleaning stoichiometry. At ppm concentrations, that direct loss could be small. But a strongly adsorbing product can have a disproportionate effect on the sparse active sites, and a retained/recycled product can accumulate. This is why identify-and-dose experiments are more useful than immediately demanding complete tolerance of steam.

## 3. Removing steam does not remove the equilibrium or energy constraint

For ideal-gas ethylbenzene `E -> S + H2`, feed one mole E, s moles inert diluent, no initial S/H2, and conversion x:

`Qp = (P/p°) x^2 / [(1 − x)(1 + s + x)]`,

where Qp is dimensionless, P is total pressure, and p° is the standard pressure.

Removing diluent at fixed P, T, x raises Qp and reduces forward driving force. To maintain the same reaction quotient at the same x and T, the dry pressure must satisfy

`P_dry/P_diluted = (1 + x)/(1 + s + x)`.

Clariant's current product page claims a steam/oil mass ratio of 0.76 for StyroMax UL-100. Treat this as a manufacturer claim, not independent performance validation. That mass ratio corresponds to about 4.48 mol water/mol ethylbenzene. At x = 0.5, a dry process would need approximately **one-quarter of the diluted-process total pressure** for the same ideal-gas reaction quotient. This is an illustration of pressure/steam exchange, not a recommended operating point. [Clariant StyroMax portfolio](https://www.clariant.com/en/Business-Units/Catalysts/Petrochemical-and-Refining-Catalysts/Styrene-Catalysts/StyroMax-Catalyst-Portfolio).

The equation has no catalyst activity in it. Higher intrinsic activity can reduce required catalyst inventory or permit operation nearer equilibrium; it cannot move equilibrium. Product/H2 removal, lower pressure or higher temperature changes the constraint, with corresponding separation, compression, heat-transfer or side-reaction costs. Vacuum operation and steam-free ethylbenzene dehydrogenation are established alternatives and must not be claimed as novel.

**Local flow consequence, independently checked:** at equal temperature, ethylbenzene molar feed and a specified conversion x, the pressure ratio above also preserves each reactive partial pressure and the local actual volumetric gas flow. This follows from `p_i = P n_i/(1+s+x)` and `Vdot = FE,0(1+s+x)RT/P`. Removing steam while matching those local conditions therefore gives no automatic local volumetric-rate advantage; equal rates would additionally require unchanged catalyst state and kinetics. The required pressure ratio varies with x, so one constant pressure ratio does not match the whole reactor profile. This identity cannot establish equal reactor volume or eliminate differences in heat transfer, pressure drop, adsorption and regeneration.

Using the approximately 125 kJ/mol reaction enthalpy quoted in the zirconia study gives roughly **1.2 MJ/kg styrene** for the reaction itself, before vaporization, heating, losses or separations. Steam elimination does not remove that heat demand. Steam also provides thermal capacity and affects deposits. Removing it can shift the burden to reactor heat transfer, recycle, and regeneration. [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]] p.1 p.5.

Two distinct comparisons are necessary:

- **Catalyst chemistry:** measure net rates, selectivity and survival at matched ethylbenzene/styrene/H2 fugacities, temperature and transport conditions, with a deliberate water difference only when testing water effects. Report per initial catalyst mass and volume, not merely surviving sites.
- **Process option:** compare each catalyst under a sensible operating envelope. Fe–K may require steam for its working state; forcing both catalysts into a dry feed is not a fair process benchmark. Include low-steam Fe–K, vacuum/inert alternatives, heat integration, and catalyst inventory.

The 2025 MacroCat-201S industrial article is a relevant contemporary baseline, but its abstract's 1.0 steam/oil ratio is not the documented long-term operating value. The retrieved full text reports approximately 1.2 by mass over 36 months (p.6, Figure 3 on p.8, visually checked), and 1.15 during a three-day calibration. Its company-affiliated authors report roughly 64% conversion and selectivity above 96.3% during operation, with temperature adjusted over time. This is operating evidence from a supplier/operator report, not an independent matched-catalyst comparison. [Primary industrial report](https://doi.org/10.3390/catal15040308). The uploaded [Luyben primary text](../../literature/papers/luyben2010-design-and-control-of-the/original.pdf), p.16, explicitly couples steam ratio, selectivity, recycle and reactor size: its simulated cost improvement uses more steam, larger reactors and higher recycle. The uploaded [Dimian and Bildea primary text](../../literature/papers/dimian2019-energy-efficient-styrene-process-design/original.pdf), pp.15–16, Table 15, instead sharpens the heat-integration comparison. Hot utility falls from 42.5 to 11.75 MW (about 73%), but total annual energy cost including compression and steam credit falls from 11.08 to 5.73 M$/y (about 48%). Its approximately 36% annualized-cost reduction is for reaction-section energy/equipment, not the whole plant. These simulated results use historical assumptions; no savings percentage transfers to zirconia.

The now-read [Tang 2024 comparator](../reviews/styrene-steam-free-benchmark.md) also supplies a documented steam-free laboratory reference. Its temperature series uses nitrogen/saturator feed, 2,860 Pa ethylbenzene and 10 mL/min, with averages over 9–11 h after induction. Its 0.341 kmol/(m³·h) optimum at 109 mL/min is a model result, not measured optimized production. Measured ppm dryness and repeated-regeneration durability remain unestablished. The [post-upload audit](../reviews/post-upload-cha-styrene-audit.md) details the source boundaries; these updates strengthen the fair comparison without promoting zirconia to a substantial program.

## 4. Specific new experiment: does hydroxyl removal create the next titrant?

### Falsifiable hypothesis

**A chemically regenerated Zr–O pair exports part of its bound water oxygen as an oxygenated aromatic product. Some such products bind more persistently than water or become carbon deposits; under product-rich conditions or recycle this secondary fate limits site survival.** The beneficial dilute-feed self-cleaning regime therefore has a boundary set by oxygen-product removal and reaction, not just inlet water ppm.

This is not established. Strong alternatives are: oxygen exits harmlessly; water simply desorbs or exchanges with lattice oxygen; apparent recovery comes from a different site population; or irreversible carbon deposition is independent of the hydroxyl-cleaning reaction. Importantly, “oxygenates return with recycle” must be tested against their actual separation/partitioning: heavy phenolics may leave efficiently in a purge rather than return with ethylbenzene.

### First experiment, before a materials campaign

1. Reproduce the two pretreatment histories and their convergence using **independently metered and measured** low water concentrations. Record bed temperature, direct inlet/outlet H2O and O2, and actual water breakthrough. State whether ppm is molar or mass-based and whether it refers to the full gas or liquid hydrocarbon; report molar oxygen flux as well. Resolve the uncertainty caused by estimating inlet water from the same activity model later used to infer cleaning.
2. Titrate a known fraction of the competent pairs with H2-18O, purge mobile water, then introduce rigorously characterized ethylbenzene. Measure rate recovery together with isotope-resolved H2O, CO/CO2, condensable oxygenates and retained oxygen/carbon. Use a heated transfer line and an integrated condensate trap with analytical recovery standards; online GC alone may miss the relevant low flux. Empty-reactor controls, blank zirconia, hydroxylated zirconia held in He without hydrocarbon, and an unlabeled sequence quantify lattice exchange, desorption and line memory. If oxygen-product assignment remains ambiguous, add labeled ethylbenzene to establish the source of product carbon; this is a targeted follow-up, not a mandatory large isotope matrix.
3. Test whether recovery of a measured competent-site fraction requires loss of a corresponding labeled-oxygen inventory. Do not demand one precise stoichiometry before establishing whether oxygen exchange or multi-site adsorption matters. A null detection needs a calibrated upper bound relative to recovered sites, not simply an absent peak.
4. Identify candidate oxygen products by GC–MS and standards, then dose the measured candidates separately at their observed fluxes and plausible recycle accumulation levels. Require that they reproduce a site-loss or carbon-deposition signature that differs from water at matched oxygen input. If a stronger titrant is never formed or does not accumulate, reject the relay hypothesis.
5. At matched E/S/H2 fugacities, vary styrene and water independently on replicate beds. Distinguish simple reversible inhibition, water titration, and irreversible deposit formation by dry-feed recovery and competent-site titration on matched specimens. A product-rich differential reactor can test this chemistry before an integral high-conversion reactor introduces severe gradients. Only then test a realistic conversion trajectory and a standardized coke-removal/restart cycle.

The useful advance is a chemically closed, experimentally bounded site-survival law, for example a balance among water arrival, hydrocarbon-assisted oxygen export, product rebinding and irreversible pair loss. It should predict a held-out water/product history and regeneration restart. A general multi-parameter fit to deactivation does not meet this standard.

**Positive consequence:** identify a specific impurity/product to remove or avoid, a selective regeneration sequence, or a justified operating composition that preserves bare pairs without frequent DME. Any proposed remedy must beat simple feed drying and product separation.

**Negative consequence:** show that self-cleaning has negligible oxygen-product penalty and that coke or the equilibrium/heat-transfer constraint is the real obstacle. This would prevent an unnecessary water-tolerant materials campaign and redirect work toward the relevant chemistry. If no consequential unclosed balance survives examination of the original SI and patents, stop rather than relabel existing findings.

Confidence that this experiment is informative is moderate to high; confidence that the relay mechanism is true is low; confidence in a process improvement remains low until selectivity, inventory, and regeneration are measured. Identifying every atomistic site is not a prerequisite.

## 5. Comparative practical losses and selection

| Program | Loss that could matter most | Strongest simpler alternative | Best first discriminating experiment | Present decision |
|---|---|---|---|---|
| Styrene/Zr–O oxygen fate | Loss of useful pairs or selectivity during product-rich operation/restart; steam savings offset by recycle/vacuum/heat duty | Low-steam Fe–K with established heat recovery; straightforward feed drying | Metered water plus 18O oxygen balance and product rechallenge | Best new oxide test; no broad synthesis yet |
| Polymer Na/W ethenolysis | Expensive catalyst function lost to real contaminants; cleanup/adsorbent demand and ethylene usage erase value | Feed sorting/washing/drying, known 4A protection, documented regeneration | One impurity, independently exposed/recombined catalyst components, closed polymer/ethylene carbon balance | Worth retaining; full methods/thesis boundary first |
| Zeolite Al recovery window | Permanent useful acid inventory lost per regeneration; recovery downtime consumes preservation benefit | More stable formulation and milder conventional regeneration | Identical delivered wet/dry/time histories with different order, no intervening healing assay | Clean, useful falsification; application benefit unproved |
| MCH/Pt oxide scavenging | Pt inventory, carrier destruction and eventual support-carbon saturation | Existing Pt/alumina, moderated/alloyed Pt and durable confined Pt systems | Bound accessibility headroom at useful feeds before tracing carbon flux | Lower priority than original optimism would suggest |

### Polymer accounting is a prerequisite, not an optional refinement

For an ideal long PE chain converted entirely to propylene using ethylene, the bulk stoichiometric limit is `CH2 + C2H4 -> C3H6`, apart from initiation/end-group corrections. Thus the idealized process consumes roughly **2 kg ethylene per kg PE** and makes about 3 kg propylene; only about one-third of its product carbon originates from PE. This is a stoichiometric illustration, not an assertion about the published experimental yield basis. It explains why gross olefin yield and catalyst productivity can mislead if ethylene-derived carbon is counted as recovered polymer.

The process may still be useful, but its incremental value must be judged against ethylene consumption, product composition and alternative uses of that ethylene. Improved poison tolerance cannot fix an unfavorable underlying material balance. The alternative screen correctly requests isotopic source allocation and component-specific rescue. These measurements should precede a broad impurity-tolerant catalyst campaign.

### Zeolite recovery must pay for the added interval

For unchanged productive run duration, let g be the gain in integrated useful product per run after an intervention, T0 the original full run/regeneration cycle time, and Δt its extra time. The average-throughput ratio is `g T0/(T0 + Δt)`. A 10-minute addition to a 70-minute original cycle requires more than a 14% product-per-run gain merely to preserve throughput. This is an illustrative local bound; longer catalyst replacement intervals and changing selectivity require a fuller lifecycle calculation. A larger NH3 count alone cannot show the tradeoff is favorable.

The zeolite experiment is particularly useful if conducted first under fixed-temperature waveforms: it can reject a recovery-window story without buying a complex regeneration system. The polymer and styrene experiments similarly should begin with causal chemical balances rather than a materials library.

## 6. Source handoff and next decision

Historical 2026-09-15 handoff: the parent received requests for the zirconia paper's SI, Luyben 2011, Dimian/Bildea 2019, MacroCat-201S 2025, the current Clariant portfolio, and a 2024 steam-free fixed-bed ethylbenzene study (10.1021/acs.iecr.4c01175). The named scientific article/SI sources have since been read in the current program and 2026-09-16 comparator audit; this paragraph is not a current retrieval queue. These go through the single reusable literature agent; no KB maintenance occurred here. The original zirconia p.8 was visually checked, and p.6–7 was read directly in extracted full text.

Before promoting this styrene branch, fresh review should ask whether the SI or patent already closes oxygen-product fate; whether isotope exchange prevents a useful balance at obtainable sensitivity; whether anticipated products are actually recycled; and whether a modern Fe–K comparison leaves meaningful rate/selectivity/utility headroom. If those checks hold, the first oxygen-fate experiment is strongly justified even though a successful process improvement is uncertain.
