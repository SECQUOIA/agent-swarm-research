# Close the cleaning cycle in zirconia-catalyzed styrene production

## Main recommendation

**Retain a bounded diagnostic pilot; a substantial research campaign is not yet justified.** Test whether a measured oxygen pathway can explain and predict sustained styrene-forming function. Begin with calibrated moisture/reference measurements, a small product-containing net-output gate, and the smallest informative native-product/function comparison. Use isotope labelling only for a specific consequential question that those results make testable. The later aims below are conditional options, not a default sequence of commitments.

This program is a proposal, not a demonstrated improvement. It is connected directly to Iglesia's recent zirconia dehydrogenation chemistry and to both groups' interests in quantitative kinetics, working-site populations, adsorption, and catalyst durability. It presently offers a stronger application question than the initial [LOHC support-scavenging screen](../working/oxide-screen.md), while retaining substantial scientific and practical uncertainty.

Date: 2026-09-16, updated after the [post-upload comparator audit](../reviews/post-upload-cha-styrene-audit.md). The initial [independent review](../reviews/styrene-independent-review.md) supported a bounded first campaign. The subsequent [fresh value review](../reviews/program-value-challenge.md) tightened the investment criterion: passing analytical or product-cofeed gates does not by itself justify expanding oxygen attribution. The balanced reactions, recycle equations and measurement controls remain useful, but do not establish the importance of the unresolved chemistry. [Practical selection assessment](../working/practical-selection.md) and [recycle bounds](../calculations/styrene-recycle-bounds.md) record the supporting reasoning.

### Result required for expansion

Show that a chemically specified maintenance pathway controls sustained catalytic function, and use its independently measured behavior to predict the response to an untested feed-composition or product-removal change. Exact atomistic structure and an oxygen-per-pair census are not prerequisites for an explicitly functional claim. A new peak, isotope transfer or harmless separation alone is insufficient.

After the first repeatable oxygen/function result, state prospectively which untested response the chemistry should predict and why the existing measured-water model does not already provide an adequately supported answer. Continue only if the contrast and attainable precision can test that prediction. If X is benign and the simpler model already predicts function within useful uncertainty, close the oxygen-fate work at its diagnostic scope. If product-rich damage appears without evidence linking it to oxygen chemistry, investigate the observed damage on its own evidence.

## The gap is a chemical balance, not a new claim of self-cleaning

Artsiusheuski et al. demonstrate selective ethylbenzene dehydrogenation on chemically exposed Lewis acid–base Zr–O pairs. Water lowers activity, while sufficiently purified ethylbenzene can increase the activity of initially He-treated zirconia toward the same asymptote reached from DME-activated material. The authors interpret this convergence as hydrocarbon-assisted removal of bound water. [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]] p.3-4, p.6-8; [DOI](https://doi.org/10.1021/acscatal.5c04904).

The cleaning products, denoted X, were not identified under the reported low-conversion conditions. The model assumes that X binds more weakly than water. Ring hydroxylation and side-chain hydrolysis are suggested possibilities, not experimentally assigned routes. The published water levels are estimated from titration/kinetic information; they are not independent inlet-water measurements. These distinctions matter when predicting a different feed, recycle composition, or operating duration. [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]] p.6-8.

The reported roughly 70% retained initial rate at an estimated 4 ppm and the predicted roughly 95% at 1 ppm must remain distinct. The stable interval reported in the main text exceeds 50 ks, roughly 14 h; it is not a lifetime demonstration. The main experiments use dilute hydrocarbon feeds and the cleaning interpretation is assessed at about 0.5–2% ethylbenzene conversion. These are valid kinetic conditions; transfer to an integral reactor requires new evidence. The retrieved [SI](https://doi.org/10.1021/acscatal.5c04904.s001), p.6, establishes a total-gas mole basis for the estimated water ppm. It does not independently measure inlet moisture. SI p.10 explicitly excludes further transformations of X from the model; no product identification or closed oxygen balance was found.

**What is already anticipated:** chemical cleaning and repeated DME activation; removal of oxygenated feed impurities; and avoiding cleaning reagents that leave persistent debris. In particular, [WO2024177986A2](https://patents.google.com/patent/WO2024177986A2/en) discusses oxygenated impurities and cleanup-product requirements. Thus neither “oxygenates poison oxides” nor “add a guard bed” is original here. The potentially new contribution is an ethylbenzene-specific oxygen/carbon balance tied to useful site recovery, species-specific removal/recycle behavior, and a validated prediction of sustained function. Ordinary feed components may also limit the driving force for cleaning without directly poisoning exposed pairs; that hypothesis becomes testable once the net oxygen-export route is identified.

## Why a clear answer could be consequential

If a substrate repeatedly removes the poison from its own active site without generating persistent inhibition, strict thermodynamic water-binding predictions alone may be overly pessimistic about useful operation. Conversely, a stable dilute-feed rate may conceal a finite oxygen/carbon reservoir or a product that becomes consequential only after repeated exposure.

A positive mechanistic result could define the actual feed-purity requirement and whether ordinary product separation is sufficient. An adverse result could identify a particular species requiring removal or a regeneration step, or show that this catalyst cannot justify its impurity-control burden. These outcomes influence process viability and offer a transferable approach for other oxide acid–base reactions where activity and chemical cleaning occur together.

Do not promise energy savings simply because steam is omitted. Endothermic reaction heat, equilibrium, heat transfer, vacuum/compression, separations, and coke control remain. Modern low-steam Fe–K is the appropriate process competitor; forcing that catalyst into a dry feed would be an unfair comparison.

## Hypotheses and meaningful alternatives

**H1 — useful oxygen export.** The oxygen removed from rate-blocking species leaves primarily as identifiable products that ordinary separation removes, with little persistent site loss. Direct water cleanup largely determines useful lifetime.

**H2 — harmful secondary fate.** Some cleaning products readsorb, form more persistent titrants, or become deposits at their actual operating concentrations. If sufficiently returned by separation, they change the catalyst's long-term working state. This is plausible but presently low-confidence; it must not be assumed from the existence of oxygenates.

**H3 — exchange or storage explains the label.** Oxygen exchanges among water, surface/lattice oxygen, and pre-existing organic species; the detected labelled product does not account for recovery of the active pairs. Some oxygen is retained rather than exported.

**H4 — a different change controls activity.** Ordinary thermal desorption, residual activation products, site restructuring, or product inhibition creates the observed transient. Hydrocarbon-assisted oxygen export may occur without being the cause of recovery.

**H5 — product chemical potentials limit cleaning.** Aromatic feed impurities or generated coproducts suppress a reversible oxygen-export route, even if they have little direct effect on dry active pairs. This requires an identified net route and credible local product concentrations; a thermodynamic possibility is not evidence that it controls the catalyst.

**H6 — the cleaning chemistry is benign but another process limitation dominates.** Product-rich inhibition, carbon deposition unrelated to the cleaning route, insufficient volumetric rate, or equilibrium/heat-transfer costs prevent a practical benefit. This is a valuable result if it prevents unnecessary impurity-tolerant synthesis.

## Aim 1: identify or bound the oxygen pathway during recovery

### Establish independently measured inputs

Use one parent monoclinic zirconia preparation, with controlled He-treated and DME-treated histories. Reproduce the convergence behavior using measured inlet/outlet water and oxygen, rather than assigning water from the same deactivation model being evaluated. Report molar flux, partial pressure, and an explicit ppm basis. Characterize the complete organic feed, including oxygenated impurities and residual inhibitors in styrene cofeeds. Measure the sources of moisture and report its ratio to ethylbenzene as well as total-gas ppm. The published cleaning model responds to that local ratio; concentration changes need not preserve its poisoning/cleaning balance. The [feed-scaling calculation](../calculations/styrene-feed-scaling.md) defines a small transferability test and explains why low ethylbenzene conversion does not guarantee a negligible water gradient.

Calibrate heated-line and trap recovery with representative standards before interpreting a missing product. Collect both volatile gases and condensable material. Trace products may require time-integrated collection rather than faster online sampling. Collect the complete transient, but do not extend collection after a finite prelabelled reservoir is exhausted merely to increase signal: this adds background. Pool independently validated repeat cycles or increase catalyst throughput while preserving chemistry when necessary.

### Order of work: a small pilot before specialist isotope accounting

The independent [staged-pilot review](../reviews/oxygen-measurement-feasibility.md) recommends starting with unlabeled feeds. This changes the order of investment, not the required evidence for stronger claims.

| Stage | Minimum work | Decision produced |
|---|---|---|
| Calibrate the train | Measure inlet/outlet water uncertainty, drift and lag in the real matrix; verify collection recovery and blanks | Can the net trace oxygen difference be resolved at all? |
| Test product-containing operation | After reproducing the reference, measure net styrene output under matched E/S/H2 cofeeds and return to reference | Does the selected operating window retain enough useful function to justify application-driven oxygen-fate work? |
| Resolve a recovery-associated native signal | Cross water/sham history with EB/no-EB recovery exposure; validate the functional readout and collect matched product windows | Does EB provide additional recovery with incremental oxygen output, and which products or bounds justify further work? |
| Test a specific consequence | Challenge identified products/aromatic coproducts at credible exposure; track clean-site inhibition, recovery and net oxygen exits | Is there a consequential product effect worth explaining? |
| Resolve provenance or site attribution | Use a targeted 18O sequence and exchange controls; add solid-isotope accounting only for claims that require it | Does water-derived oxygen enter the product, and what further attribution is supportable? |

A missing native product is informative only when its calibrated upper bound is small relative to a measured net oxygen flux or a defined competing pathway. Subtracting two large uncertain water readings cannot supply that denominator reliably. If the native signal is obscured but isotope enrichment could answer a consequential question, the third and fourth stages can be reordered on that evidence.

Unlabeled product collection can reveal chemical identity and net output. It cannot establish that the oxygen came from the blocking species, rule out stored material, or count oxygen per recovered pair. Successive stable effluent windows and a flat rate do not prove that a large solid reservoir is stationary. Keep those limits attached to every initial conclusion rather than requiring a difficult whole-solid isotope measurement before useful product discovery.

### Early practical gate: measure net styrene in a product-containing feed

The [independent product-headroom review](../reviews/styrene-product-headroom.md) recommends this small test before substantial oxygen-product or isotope work. The source's zero H2 order describes equilibrium-corrected forward dehydrogenation. Reverse hydrogenation is first order in styrene and H2 in its measured regime. The recovery SI varies mean styrene only around 15–50 Pa; it does not establish useful output in a product-rich cofeed.

After reproducing a reference under measured moisture, use two styrene levels and two H2 levels at fixed EB, temperature, total flow and moisture. Choose the higher S/EB ratio from a stated prospective operating composition and check `η = Q/K(T)`, where `Q = aS aH2/aE` uses dimensionless activities. Include a product-containing point with appreciable forward affinity; a negative net rate at η greater than one is not evidence of poor catalytic function. Obtain K(T) and its uncertainty before setting actual pressures. The conditional relation `rnet = rforward(1 − η)` explains reverse-reaction loss only while the focal kinetic assumptions hold.

The [independently checked equilibrium screen](../calculations/styrene-cofeed-equilibrium.md) gives K approximately 0.026 at 773 K. At 12 kPa H2, S/EB = 1 would favor hydrogenation. A nominal η = 0.5 at that ratio requires about 1.3 kPa H2; retaining the screen's full ±5 kJ/mol sensitivity as a planning margin would require about 0.60 kPa or less. That sensitivity is not a confidence interval, and the low-H2 kinetics/durability are untested. Select an interpretable composition with explicit uncertainty; do not extrapolate the published forward-rate law to promise performance there.

Measure `(FS,out − FS,in)/initial catalyst mass`, side products and drift, with interleaved return-to-reference tests. Calibrate the uncertainty of that difference against the larger fed-styrene stream. Control styrene-feed water and stabilizer carryover; the source reagent contains 4-tert-butylcatechol. A reversible loss beyond the affinity effect calls for an inhibition/state test; failure to recover the baseline calls for damage/contaminant diagnosis. Neither identifies cleaning product X as the cause.

Predeclare a useful net-output/selectivity requirement from the selected operating window and catalyst-inventory constraint when those are available. Otherwise this is a chemical continuation test, not an economic viability gate. If the selected window fails despite favorable affinity, pause its application-driven oxygen-fate expansion. A smaller mechanistic study can still be warranted for a clearly stated independent scientific question. Native collection can accompany the cofeed test where practical, without committing to exhaustive product identification.

### Minimal causal comparison and the assay-validity gate

The [fresh pilot review](../reviews/styrene-pilot-decision-review.md) replaces a simple pretreatment comparison as the first scientific discriminator. Use one reproducible starting preparation, a measured partial water dose or sham, and the same purge. Cross these histories with a fixed recovery interval with or without EB, replacing EB with carrier and matching H2, temperature, pressure and flow. Collect water and native organic/COx outlets in separate dosing, purge and recovery windows. Include train/quartz blanks and independent specimens sufficient to resolve the contrast.

Compare the effect of EB in the water-dosed history with its effect in the sham history. For non-water oxygen output, report all four measurements and their interaction, `(Owater,EB − Owater,noEB) − (Osham,EB − Osham,noEB)`. Each term is net outlet oxygen after measured feed/apparatus contributions. Keep water release separate before combining the oxygen balance. A resolved interaction plus additional recovery supports an association; water can still change side chemistry independently of the cause of recovery.

**Validate the common functional assay first.** EB is both reactant and proposed cleaning agent. It can erase the state of a no-EB control during switching or measurement. If the difference disappears before an early readout is reliable, equal final rates cannot distinguish prior thermal recovery from assay-induced recovery. Report exposure-period oxygen outlets and function after the common assay, but withhold the thermal-versus-EB recovery inference. Fitting an unobserved initial rate does not resolve this ambiguity by itself.

Repeat a resolved contrast without renewing activation reagents, then add a second measured partial dose if useful. Repeated recovery with a fading oxygen burst argues against that burst as the continuing cleaning marker. Repeated coupled responses justify targeted provenance work, but a few cycles cannot exhaust or exclude the much larger oxide oxygen reservoir. Net input/output closure constrains net storage, not equal opposing exchange fluxes.

The pilot has two routes to further work: a resolved recovery-associated oxygen signal, or an identified product that affects net styrene output at credible exposure. A new peak alone is insufficient. If thermal/H2 recovery explains the functional response, or organic outlets are bounded below a consequential level, retain that result and narrow the mechanism. If uncertainty exceeds the proposed signal, report analytical ambiguity rather than a negative chemical result. Defer the feed-scaling matrix and coproduct-pressure grid until one of these outcomes identifies their purpose.

Keep measured retained water, operational activity recovery and native oxygen output as separate observables. Water uptake plus correlated rate loss is **not an independent active-pair census** unless uptake specificity, stoichiometry and per-site kinetics have independent support. Separate specimens avoid measurement interference but do not remove shared assumptions. The first pilot needs no oxygen-per-pair claim.

### Commissioning gate: can the measurement resolve the proposed chemistry?

The [independent measurement review](../reviews/oxygen-measurement-feasibility.md) uses the focal SI's stated 20 mg bed, 130 m²/g area, and 0.56 pairs/nm²: approximately **2.4 μmol active pairs**. If 25% are poisoned and recovered, a one-water-per-pair hypothesis corresponds to only **0.60 μmol oxygen**. These are design inventories, not observed cleaning yields. A 10% branch is about 0.060 μmol oxygen; isotope enrichment, recovery and background reduce the usable signal further.

The same bed contains about 325 μmol lattice oxygen; the reported 1 g quartz diluent contains about 33 mmol structural oxygen. These capacities do not establish exchange rates, but even small accessible exchange fractions can rival the target. Include a quartz-only sequence and account separately for catalyst, diluent and apparatus. Specialist whole-solid isotope analysis may be needed for a closed balance; routine surface spectra alone cannot provide it.

Measure blank variance, product recovery and retained-label uncertainty before committing to molecular attribution. The review's illustrative 10%-branch target would require combined uncertainty and unmeasured bounds appreciably below about 54 nmol excess 18O for 90%-enriched water. This is an example for commissioning, not a promised instrument capability or mandatory universal threshold. If that precision is unavailable, choose a larger resolvable pathway bound and state the narrower inference.

The SI's 50 mL/min flow at 298 K and 101.325 kPa applies to the 723 K water-estimation experiment. It gives approximately 0.122 μmol/h per total-gas ppm. Do not transfer that flow to the distinct 773 K recovery experiment without checking the actual conditions. SI p.6 also has a small internal inconsistency between its prose and printed deactivation time; use new independent moisture calibration rather than fitting an exact feed specification to that arithmetic.

### Conditional labelled-water recovery experiment

1. On activated zirconia, introduce a calibrated H2-18O exposure giving a measurable partial loss of activity. Measure uptake/breakthrough independently and retain an unlabeled-water counterpart. The dose should be chosen from measured capacity and analytical precision, not an arbitrary high concentration.
2. Purge mobile water under a defined condition while measuring its complete isotope tail. The remaining label is not automatically confined to active-pair hydroxyls: it can have exchanged with other surface or lattice oxygen.
3. Introduce characterized ethylbenzene at the original reaction condition. Follow activity recovery, water isotopologues, CO/CO2, organic oxygenates, and trapped material. Obtain matched solid specimens to assess persistent carbon and oxygen label where reliable quantification is feasible.
4. Compare the same labelled exposure without ethylbenzene, an empty train, an unlabeled sequence, and an initially hydroxylated specimen. These controls constrain thermal desorption, apparatus memory, nonspecific oxygen exchange, and a chemistry that does not require active-pair recovery.
5. If product origin remains ambiguous, use labelled ethylbenzene in a targeted follow-up to separate feed-derived carbon from residual DME, pre-existing deposits, or background oxygenates. Do not assume that detecting 18O in a product identifies the site that supplied it.

Activity is an independent observable throughout. A labelled oxygenate peak establishes oxygen transfer; it does not by itself establish the mechanism responsible for reactivating a Zr–O pair.

After identifying an X candidate, feed an authentic standard over a labelled surface and through the sampling train separately. Product oxygen can exchange after X forms, including in adsorbed states or wet collection media. These controls distinguish newly formed labelled X from an existing oxygenate that merely acquires label. On separate matched specimens, compare kinetic recovery with calibrated operational water uptake. Do not calculate both from the same fitted activity curve or treat their correlation as an independent validation of blocking stoichiometry. Reserve oxygen-per-pair claims for independently supported site counting.

### Required balances

Count **18O atoms**, including singly and doubly labelled molecules where relevant:

```text
admitted 18O = effluent 18O + change in retained 18O + train/trap inventory change.
```

Also close ordinary carbon and oxygen balances as far as sensitivity permits. Bulk carbon closure is not sufficient: quantify the incremental uncertainty on the trace cleaning-product carbon/oxygen flux itself. State unresolved fractions explicitly. A retained inventory inferred only by subtraction is not an independent solid measurement. If unresolved label is comparable to the proposed cleaning flux, the experiment has not identified that flux. Report a calibrated upper/lower bound and improve the relevant measurement before claiming closure.

Report the carbon cost relative to reacted ethylbenzene and actual net styrene output. The [conditional diversion bound](../calculations/styrene-feed-scaling.md#5-trace-relative-to-total-gas-can-be-significant-relative-to-product) shows why a ppm oxygen flux can matter in a low-conversion experiment, without establishing an actual yield penalty. Reconcile cleaning products with existing cleavage channels to avoid double-counting benzene or toluene. Distinguish per-pass oxygenated intermediates from final product loss. The bound applies to net external oxygen export under stationary inventories; recovery of preloaded oxygen and repeated cleaning after water regeneration require their own balances. Do not use an equilibrium-corrected forward styrene rate as product output.

Within existing product analysis, independently calibrate net toluene/methane and benzene/ethane fluxes. The source reports equimolar pairs but provides no precision-based bound on their imbalance. A resolved change during recovery flags incomplete paired-cleavage accounting and directs the C1/C2 oxygen-product search. It does not uniquely identify hydrolysis. Secondary reactions can erase the imbalance, so a null result bounds only the unmasked difference; it cannot exclude cleaning. The [paired-product review](../reviews/styrene-independent-review.md) details these limits.

The isotope balance need not prove one molecule of water removed per active pair. That stoichiometry is an independently testable assumption. Compare the measured change in functional capacity with several chemically allowed accounts, including exchange and changes in the population sampled by titration.

### Chemical possibilities to discriminate, not predicted products

The following balanced reactions illustrate distinct carbon/hydrogen signatures of one-water oxygen transfer; they are not asserted elementary steps or observed products:

| Possible overall route | Balanced example | Distinguishing output |
|---|---|---|
| Hydroxylation without carbon cleavage | C8H10 + H2O → C8H10O + H2 | An oxygenated C8 product; isomer identity remains to be measured. |
| Further dehydrogenation of a C8 oxygenate | C8H10 + H2O → C8H8O + 2 H2 | A C8 carbonyl product and different hydrogen balance. |
| Side-chain cleavage | C8H10 + H2O → C7H8 + CH4O | Toluene plus a C1 oxygenate. |
| Aryl–ethyl bond cleavage | C8H10 + H2O → C6H6 + C2H6O | Benzene plus a C2 oxygenate. |
| Thermal water release or exchange | No necessary organic oxygen product | Water-label response without the corresponding carbon flux. |

Bulk dehydrogenation generates much more H2 than trace cleaning may produce, so hydrogen differences may be unresolvable in the main stream. Product and isotope balances carry the primary inference. Adsorbed intermediates can further react before leaving; absence of an initially plausible oxygenate does not eliminate every route.

### Check sustained thermodynamic feasibility after identifying the net route

The [thermodynamic screen](../reviews/styrene-cleaning-thermodynamics.md), verified by a [fresh independent review](../reviews/styrene-thermodynamics-independent-review.md), finds approximate 773 K standard Gibbs energies of +61 kJ/mol for benzene/ethanol cleavage and +56 kJ/mol for toluene/methanol cleavage. Trace products can nevertheless be thermodynamically allowed. Positive standard ΔG alone does not reject these reactions. Their reaction quotients depend on both coproducts, so benzene or toluene already in the feed counts even when it is unrelated to cleaning.

These are conditional candidate calculations, with incomplete thermochemical uncertainty, not product assignments. A low equilibrium alcohol concentration constrains that terminal outlet, not total cleaning. Further alcohol conversion to carbonyls or CO changes the net stoichiometry; measure those oxygen exits. Also, successful self-cleaning need not consume all incoming water. Quantify net water consumption and working-site state instead of comparing an alcohol ceiling with inlet water alone.

The acetophenone route produces two H2 per water. Its reaction Gibbs energy falls by about 30 kJ/mol when H2 drops tenfold at fixed other partial pressures. Absolute feasibility remains conditional on missing high-temperature gas heat-capacity data. An H2 perturbation is therefore useful only with simultaneous correction for styrene reaction affinity, direct inhibition and other oxygen pathways.

Apply closed-cycle thermodynamics only after water breakthrough, working-site capacity, and bounded solid/apparatus oxygen and carbon inventories become stationary. Use net molar formation rates and a measured local reaction quotient; combining inlet water with outlet products can be misleading when water has a strong axial gradient. A finite prelabel recovery changes the solid state; gas-only equilibrium bounds cannot be used to reject such a transient. Conversely, a labelled pulse cannot establish sustained oxygen-export feasibility.

## Aim 2: determine whether the products actually threaten useful operation

Advance only after identifying products or obtaining bounds narrow enough to choose a meaningful exposure test. Do not begin with an arbitrary phenol cofeed and label its toxicity proof of the proposed pathway.

For each relevant identified species, measure adsorption/reaction, breakthrough, rate suppression, and recovery at the measured formation level and a justified upper recycle exposure. Compare matched water input, clean ethylbenzene, and a sham change in flow. Track persistent carbon and whether dry ethylbenzene restores activity. A product that disappears from the effluent may be harmlessly converted or may be accumulating on the catalyst; the solid inventory distinguishes them.

Measure whether X forms water as it reacts. Compare a water-only exposure matched to that measured output before assigning direct organic blockage. Normalize cumulative challenge to both catalyst mass and the independently constrained functional inventory. Audit traps for removal of X as well as water: a treatment that removes both cannot by itself distinguish which caused recovery.

### Distinguish direct poisoning from a loss of cleaning driving force

Once a candidate net route is identified, vary its aromatic coproduct and oxygenate pressures independently in three matched settings: dry exposed pairs, a known partially poisoned specimen during recovery, and stationary operation with measured water breakthrough. Control impurities in every cofeed. Measure normalized dehydrogenation activity, independently constrained functional recovery, net water consumption, all oxygen products, and retained inventories.

Do not treat a weak dry response and strong wet response as the generic signature of thermodynamic reversal. The [reversible two-state calculation](../calculations/reversible-cleaning-cycle.md) predicts the opposite steady ordering when complete product activities and other transition frequencies are matched: reverse cleaning lowers the free-pair fraction more in dry operation, both absolutely and fractionally. A wet-only response can instead reflect inhibition of forward cleaning, a short dry test, or a missing coproduct in the dry feed. For example, adding benzene alone need not drive reverse benzene/ethanol chemistry when ethanol is absent. Match or quantify the whole local product factor before applying this rejection criterion.

A reproducible net-flux zero crossing or reversal near the calculated complete reaction quotient would be stronger evidence of a reversible route than activity suppression alone. It still cannot identify the functional pairs if a parallel reversible side reaction produces the same flux. Use a grid of both product pressures, approach the boundary from both directions, and include equal-Q conditions. Equal-Q rate collapse away from equilibrium is not required: adsorption kinetics can still differ. Competitive adsorption, changed site state, and a coupled product sink remain alternatives. If a low-concentration reverse reaction cannot be measured, retain a quantitative bound rather than assigning an elementary mechanism. Independent site-count claims remain conditional on a validated assay.

Test actual aromatic/ethylbenzene ratios as well as oxygenates. A reported industrial Fe–K feed contains benzene and toluene; this motivates a conditional comparator experiment, not a zirconia purity specification. The [screen](../reviews/styrene-cleaning-thermodynamics.md) translates those ratios and keeps thermochemical sensitivity separate from statistical confidence.

Estimate the fraction of each product returned by the actual proposed condensation/distillation/purge scheme. This fraction differs from the bulk ethylbenzene recycle ratio. Heavy oxygenates may leave with product/heavies; COx may leave in offgas. If ordinary separation gives negligible return, reject the recycle-accumulation branch while retaining any once-through product inhibition.

The [species balance](../calculations/styrene-recycle-bounds.md) gives, at fixed reactor flow, `Jin = (Jfresh + q*G)/(1-q*s)` for an illustrative linear system. Here q is the measured species return fraction, s its reactor survival fraction, and G its formation rate. This is a design bound, not a fitted process model. Capture on the catalyst invalidates a presumed steady state until the retained inventory is stationary.

Initially reproduce product-rich conditions by controlled cofeeds in a differential reactor. Vary ethylbenzene, styrene, H2, and water systematically while tracking chemical affinity and transport. Keep the isotope experiment interpretable before testing an integral reactor with strong axial changes. Do not build a recycle loop merely to demonstrate a deliberately exaggerated impurity accumulation.

## Aim 3: make a catalyst or process decision from the chemistry

If harmful species survive ordinary separation and inhibit at credible exposure, test the simplest justified remedy: feed purification, species-specific removal, a purge change, or an established regeneration treatment. Include its finite capacity, regeneration chemicals, downtime, and material losses. Chemical cleaning and feed traps are prior art; the new value would be choosing and sizing an effective remedy from a validated mechanism and demonstrating sustained output.

If useful oxygen export is benign, focus on retained selectivity, net productivity, and restart at meaningful ethylbenzene/styrene/H2 chemical potentials. A successful negative result for the poisoning hypothesis could establish that existing drying and separation suffice.

Only after chemistry and repeated regeneration support a benefit should catalyst structure be varied. A materials change must target a measured rate or selectivity bottleneck—for example increasing cleaning selectivity while retaining C–H activation—rather than simply creating more dry initial sites. An indiscriminate hydrophobic coating can obstruct hydrocarbons or change the active pairs and has no automatic thermodynamic exemption from water binding.

## Practical benchmark and accounting

Run two separate comparisons:

- **Intrinsic catalyst comparison:** matched temperature, relevant gas chemical potentials, transport regime, and site/initial-mass denominators. Use net rates and disclose any equilibrium correction. Do not compare an initial dry zirconia rate to an aged or transport-limited reference.
- **Process comparison:** allow each catalyst an appropriate working feed. Compare low-steam Fe–K and relevant steam-free alternatives with zirconia under its measured purity requirements. Include catalyst volume, heater duty, pressure, purification, product quality, regeneration, and replacement.

Removing steam raises the reaction quotient at a fixed total pressure and conversion. For ideal-gas E → S + H2, an initially product-free feed with s mol inert per mol E has dimensionless `Qp = (P/p°)*x²/[(1-x)*(1+s+x)]`, where p° is the standard pressure and P is total pressure. Maintaining the same Qp after removing diluent requires a lower pressure or another change. The catalyst cannot change equilibrium. [The practical assessment](../working/practical-selection.md) derives this bound and records modern low-steam comparisons; it does not constitute a techno-economic analysis.

The now-read process/comparator sources include [Luyben](https://doi.org/10.1021/ie100023s), [Dimian and Bildea](https://doi.org/10.1021/acs.iecr.8b05560), the [MacroCat-201S industrial report](https://doi.org/10.3390/catal15040308), and [Tang's steam-free fixed-bed study](https://doi.org/10.1021/acs.iecr.4c01175). The MacroCat report describes approximately 1.2 steam/oil by mass during its 36-month operation, despite 1.0 in its abstract. Treat its company-affiliated operating report as a qualified benchmark, not an independent comparison. Manufacturer claims require explicit attribution and independent qualification.

The [Luyben primary text](../../literature/papers/luyben2010-design-and-control-of-the/original.pdf), p.16, demonstrates a simulated tradeoff in which more steam, larger reactors and more recycle improve yield enough to lower operating cost. The [Dimian primary text](../../literature/papers/dimian2019-energy-efficient-styrene-process-design/original.pdf), pp.15–16 and Table 15, describes a heat-integrated steam-diluted alternative: hot utility falls from 42.5 to 11.75 MW (about 73%), while total annual energy cost including compression and steam credit falls from 11.08 to 5.73 M$/y (about 48%). Its 13.70 to 8.73 M$/y annualized-cost reduction (about 36%) concerns reaction-section energy/equipment; separation costs are discussed separately. These are simulations under historical assumptions, not whole-plant savings demonstrated experimentally or savings transferable to zirconia. Count ethylbenzene losses, recycle and realistic heat integration before valuing steam elimination.

The updated [Tang 2024 comparator review](../reviews/styrene-steam-free-benchmark.md) now includes the main article. It describes an 8 mm internal-diameter reactor with a 74 mm packed height, nitrogen carrying ethylbenzene from a saturator, and aromatic collection in cold ethanol (PDF p.3). Its temperature series uses 10 mL/min flow and 2,860 Pa inlet ethylbenzene; reported values average 9–11 h after an approximately 8 h induction period (p.7). At 873.15 K, reported conversion is about 80% with approximately 97.5% styrene selectivity. Its four aromatic fractions remain unsuitable as total-gas compositions because H2 and carrier are excluded.

The quoted 0.341 kmol styrene/(m³·h) at 109 mL/min and 9,350 Pa ethylbenzene is a **model optimum**, with packed cylindrical volume as denominator (Equation 37 and pp.10–12), not measured optimized performance. Numeric total-pressure/flow-reference details and directly weighed inventory still need care for matched-rate reconstruction. The paper establishes neither measured ppm dryness nor repeated-regeneration durability. Use it as a documented dilute-feed steam-free comparator without replacing the industrial benchmark or bypassing the zirconia net-output gate.

The performance endpoint is cumulative on-spec styrene per initial catalyst inventory and occupied reactor time, with selectivity, catalyst volume, impurity-removal burden, and utilities separately reported. A dry initial-rate advantage or restored site count is insufficient.

A [conditional industrial productivity scale](../calculations/styrene-industrial-productivity-scale.md) combines the MacroCat report's design flow and loading with approximate long-run conversion/selectivity to give roughly 170 kg styrene/(m³ catalyst·h), or 0.11–0.13 kg/(kg·h). This is scenario arithmetic with an unresolved mass/molar selectivity basis and nonsimultaneous inputs. It is useful for denominator checks, not a scalar pass criterion for a local differential zirconia rate. The integrated reactor, net feed/product balance and working life require a common comparison boundary.

## Optional add-ons from the 2026-09-16 direction search

The [direction search](../reviews/direction-search-outcome.md) declined four ZrO2-related candidates as programs but left cheap checks that share this pilot's m-ZrO2 batch, pulse train and water titration. None changes the pilot's gates; each carries a frozen prediction and is run only after commissioning.

| Add-on | Source screen | Frozen prediction | What a failure would mean |
|---|---|---|---|
| Water-only exposure at reaction temperature followed by dry purge, then the ethylbenzene rate | [Ketonization screen](../working/direction-search/liquid-phase-oxygenate.md), H4, and its [review](../reviews/direction-search-ketonization-independent-review.md) | Rate returns to the DME-treated asymptote after dry purge plus ethylbenzene cleaning, with no residual loss beyond replicate scatter | A persistent water-only loss would be a restructuring branch that the published titration model does not contain |
| Ethylbenzene-to-propane transfer of the titration and cleaning constants: predict the propane-dehydrogenation asymptote at 823 K and the post-air-regeneration induction from the ethylbenzene-fitted titration constant and an independently measured propene cleaning constant | [Cross-reaction screen](../working/direction-search/zro2-water-rule-cross-reaction.md) | Prediction within the measured uncertainty of the two constants | Cleaning is reagent-specific; record the reaction-specific constant and stop the transfer claim |
| Dry 18O2 exposure of an active, hydrocarbon-free surface with uptake and rate accounting; H2 and CO2 stoichiometry during a CO treatment | [Oxide-pair screen](../working/direction-search/oxide-pair-dehydrogenation.md) | 18O uptake and H2 18O release at blank level with unchanged rate; CO treatment evolves H2 and CO2 near 1:1 | Net lattice-oxygen loss would reopen the reduction branch at this temperature |
| One day of Zr-Beta-F, Si-Beta-F and empty-bed propane runs on the same train | [Confined-pair screen](../working/direction-search/confined-framework-lewis-pairs.md) | Per-Zr rate indistinguishable from the blank; no DME response | A DME-responsive, water-titratable rate with a C–H kinetic isotope effect above about 1.5 would justify a separate screen |

Ketonization on this batch is not added: its water effect is a weak reversible inhibition at carboxylate saturation, not pair titration, and the route owners are already measuring its wet-feed deactivation.

## Milestones and rejection criteria

| Milestone | Useful result | Stop or narrow when |
|---|---|---|
| Prior art | Focal SI checked: X remains unassigned and outside further transformations in its model. Check wider prior art before a priority claim | Existing work already resolves the proposed new observation. |
| Independent water/recovery measurements | Reproduce recovery under a known oxygen flux without relying on circular impurity estimates | The effect disappears under controlled feeds or is fully accounted for by apparatus/thermal changes. |
| Product-containing output | Sustained net styrene is resolved under a specified favorable-affinity cofeed, with acceptable losses and return-to-reference behavior | Reject that operating window or diagnose its dominant limitation before application-driven oxygen attribution; unresolved difference measurements do not reject the catalyst. |
| Oxygen/carbon fate | Identify a product pathway or a consequential quantitative bound tied to functional recovery | Unresolved isotope exchange/storage exceeds the claimed signal; retain only the narrower observation. |
| Product consequence | Identified species causes inhibition, limits sustained cleaning, or is demonstrably harmless at credible exposure | Only unrealistic doses matter, or incomplete product accounting creates an apparent limit. |
| Separation/recycle relevance | Measured return and reaction predict a held-out exposure history | Ordinary separation prevents relevant accumulation; stop adding cleanup complexity. |
| Useful intervention | Improved lifetime output survives regeneration, purification, and operating costs | It only increases fresh-site inventory or transfers the burden to expensive purification/downtime. |

Choose analytical precision and practical effect thresholds before the definitive comparison. Do not assign an arbitrary percentage improvement as a scientifically established success threshold.

## Separate confidence judgments

| Question | Current judgment | Why |
|---|---|---|
| Does ethylbenzene-induced recovery occur in the published regime? | High | Convergence from two pretreatments and rate transients are directly reported. Chemical attribution still has limits. |
| Does organic oxygen export cause the recovery? | Moderate plausibility | It is a proposed account consistent with the study, but products and full oxygen fate remain unresolved here. |
| Does secondary product fate materially limit operation? | Low | It requires sufficient formation and consequential binding, reaction, return or suppression of a verified cleaning route. Current thermodynamics supplies conditional tests, not an observed limitation. |
| Can a first campaign be feasible and informative? | Moderate, with staged analytical validation | Product transfer and kinetic contrasts are accessible in principle. Quantitative attribution to pair recovery is harder because of exchange, retained-label analysis and low flux. Instrument capability is unconfirmed. |
| Will practical performance improve? | Low at present | Existing catalysts and separations are strong alternatives; utility and durability constraints may dominate. |
| Is there an original substantial contribution? | Provisional | Generic cleaning/poisoning concepts are anticipated. The proposed contribution must be a closed, predictive chemical account with a consequential operating decision. |

This program remains valuable if it rejects recycle poisoning and establishes the limits of a simpler working-state model. It does not justify claiming a new steam-free styrene process or a new class of water-tolerant oxide catalysts before the experiments.
