# Independent critical review: oxygen fate and recycle after ethylbenzene self-cleaning of Zr–O pairs

## Recommendation

**2026-09-16 status:** this review records the earlier proposal and its successive corrections. Its original missing-SI/process-source statements are historical: the focal SI was reviewed below, and Tang, Luyben and Dimian are now read in the [post-upload audit](post-upload-cha-styrene-audit.md). Follow the [current program](../programs/zirconia-styrene-oxygen-fate.md), which places calibrated moisture/net-output and native-product gates before a conditional specialist isotope or recycle study.

**Original recommendation: fund a bounded analytical and recycle screen. Do not yet commit to a substantial program.** The defensible new question is whether ethylbenzene-induced removal of water-derived titrants creates a quantitatively important, returning source of persistent blockage under a specified separation and recycle flowsheet. Self-cleaning, water sensitivity, chemical regeneration, and the general need to remove oxygenates are already established or explicitly anticipated.

A full program becomes justified only if the screen connects three observations: an oxygen/carbon source associated with restored sites, a measured return path through separation, and consequential site loss at the resulting concentration or cumulative dose. A chemically interesting product identification alone would warrant a narrower mechanistic study, not the proposed process program.

## Evidence and its limits

The principal source is [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]] p.6-8, DOI [10.1021/acscatal.5c04904](https://doi.org/10.1021/acscatal.5c04904). I inspected the original PDF images of these pages, including Scheme 1 and equation 13; their important claims agree with the extraction. The paper establishes convergence from initially activated and initially less active states, purification-dependent asymptotic rates, and recovery by DME. These observations support net reactant-assisted clearance of titrated sites. They do not identify the atomistic route or the products carrying oxygen away.

The particularly important qualifications are:

- The 43, 10, and 4 ppm water levels are estimates using known site density and deactivation/titration behavior, not an independent moisture analysis. The 95% initial-rate retention at 1 ppm is a model prediction. Direct moisture measurements are an essential new control, not merely a better instrument for an already independent input. p.6, p.8.
- Products X were not detected; their approximately 10 ppm level is estimated. Scheme 1 assumes X binds much more weakly than water. Neither their identity nor that binding assumption is independently established. p.7.
- The proposed ring hydroxylation and side-chain/ring hydrolysis descriptions are mechanistic suggestions. The cited alkene analogies do not establish ethylbenzene ring oxygenation. p.7.
- The relevant experiments used about 0.5–2% conversion. Stability beyond 50 ks is about 14 hours, valuable mechanistically but far shorter than an industrial catalyst campaign. p.6-7.
- The rate comparison uses zirconia rate relations to estimate performance under other studies' conditions. It does not establish matched integral-reactor productivity or process energy savings. p.5-6.

The absence of slow decay within the reported experiments already constrains very strong once-through self-poisoning. Recycle-specific poisoning needs additional exposure or a change of composition sufficient to evade that existing constraint. It must not be presumed merely because X contains oxygen.

## Strongest relevant prior art

1. **The focal 2025 paper itself** establishes ethylbenzene self-cleaning and proposes oxygen-containing X. Calling either the phenomenon or the generic product hypothesis new would misstate the starting point.
2. **Jaegers et al., JACS 2024, DOI [10.1021/jacs.4c07766](https://doi.org/10.1021/jacs.4c07766).** The local full text reports DME cleaning products CO, H2, and methanol and alkene-assisted cleaning, including propene at 873 K. It also discusses CO cleaning producing CO2, an alternate titrant that binds less strongly than water. Thus conversion of one titrant into a weaker one is already direct mechanistic context. [[jaegers2024-heterolytic-ch-activation-routes-in]] p.4, p.14.
3. **WO2024177986A2** is particularly close conceptual prior art. Paragraph [00087] anticipates oxygenates reacting to form titrants; [000110] describes cleaner selection to avoid leaving irreversible site-blocking debris. Claim 1 includes alcohols, ketones, and oxygenates among impurities removed with a trap. These are broad patent disclosures, not evidence that ethylbenzene-derived X actually causes the proposed recycle failure. They substantially weaken generic novelty claims about oxygenate poisoning or guard beds. [Patent text](https://patents.google.com/patent/WO2024177986A2/en).
4. **Graham, Rudham, and Rochester, 1984, DOI [10.1039/F19848000895](https://pubs.rsc.org/en/content/articlelanding/1984/f1/f19848000895).** The publisher abstract reports propene forming adsorbed isopropoxide and subsequently surface carboxylates on rutile. This supports investigating bound oxygenated intermediates, while involving a different oxide, reactant, and temperature regime. It does not verify volatile ethylphenol formation.
5. **Industrial alternative:** the primary MacroCat-201S report describes 36 months of operation around a 1.2 steam/ethylbenzene mass ratio in a large styrene unit. This sets a more serious practical comparator than an unspecified old high-steam catalyst. [Industrial application report](https://www.mdpi.com/2073-4344/15/4/308).

Independent web searches found no direct demonstration of the entire ethylbenzene self-cleaning → separated/recycled X → persistent zirconia blockage chain. That limited search result is not proof that no such prior art exists. The original supporting information was pending retrieval by the designated literature agent during this review. The queued process comparators, including 10.1021/acs.iecr.8b05560 and 10.1021/acs.iecr.4c01175, still require full-text assessment before quantitative process ranking.

## What must be distinguished

| Explanation | Decisive observation | Consequence |
|---|---|---|
| Organic oxygen export clears sites; recycled X leaves a persistent adsorbate or carbonaceous residue | X production tracks recovered site inventory; realistic recycled X decreases independently measured accessible sites after clean-feed washout | Supports the proposed full program |
| Organic oxygen export occurs, but X regenerates water on return | Extra water production quantitatively accounts for inhibition and matched water dosing reproduces it | Oxygen management matters, but a direct persistent-X-poisoning claim fails |
| X is formed and potentially inhibitory, but exits to gas, water, product, or heavy fractions | Low measured fraction returning with recovered ethylbenzene | Study product fate narrowly; reject recycle accumulation as the principal problem |
| Water cleanup already suffices | Independently verified dry feeds give sustained activity; adding the realistic recycled fraction produces no material incremental loss | Favor simple drying; reject the large recycle program |
| Organic oxygen export is not the main clearance route | Recovered site inventory is instead balanced by water release or another oxygen outlet, after exchange controls | Revise chemistry; preserve the established self-cleaning observation |
| Apparent inhibition reflects equilibrium, styrene adsorption, or residence-time changes | Effect vanishes when those variables are held fixed or corrected | Reject X poisoning attribution |

## A bounded, falsifiable screen

### 1. Establish the analytical floor and reproduce the native observation

Use the same zirconia preparation and chemical activation, approximately 773 K, 1.2 kPa ethylbenzene, and 12 kPa H2 for the primary reproduction. Maintain the reported differential conversion before moving toward integral operation. Independently measure inlet and outlet water with a method calibrated in the actual ethylbenzene/H2 matrix, and quantify O2 ingress. Blank tests must cover the reactor, quartz dilution, sampling line, feed vessel, collection traps, and storage period.

Calibrate the entire sampling train with realistic trace additions of likely compounds: ethylphenol isomers, 1-phenylethanol, acetophenone, benzaldehyde, phenol, and appropriate volatile oxygen products. This list guides recovery tests; it must not restrict an untargeted search. Measure CO, CO2, and water as well as condensable organics. Use authentic retention standards and mass spectra for assignments. Preserve samples against post-reactor oxidation and styrene-derived artifacts; any stabilizer introduced only in the collection system requires its own analytical blank.

Feasibility is plausible but unproven. At an **illustrative**, independently specified 100 standard cm³ min⁻¹ total flow, 1 ppm mol/mol gas equals about 0.268 μmol h⁻¹, or 32 μg h⁻¹ for a 120 g mol⁻¹ compound. At 0.01 ppm this falls to about 0.32 μg h⁻¹. These are potentially collectable amounts, but quantitative collection, matrix interference, adsorption on tubing, and unknown products can dominate the error. Establish method limits from recovered standards and oxygen inventories, not a GC-MS brochure.

The paper's estimated 10 ppm must be checked in the SI for its denominator before designing collection times. At 1.2 mol% ethylbenzene, ppm relative to total gas differs by roughly 83-fold from ppm relative to ethylbenzene. Increase collection time or parallel catalyst throughput while preserving partial pressures, conversion, and surface state. Large water pulses or concentrated oxygenate challenges can aid identification but cannot establish the native mechanism without a bridge back to native conditions.

**Analytical gate:** proceed only if recoveries and blank variability allow a meaningful bound on the oxygen accompanying the observed site recovery. A nondetection with an insufficient oxygen-equivalent detection limit is inconclusive.

### 2. Close a transient site, oxygen, isotope, and carbon balance

First quantify accessible LAB pairs using calibrated water uptake and the associated rate loss on matched samples. The reported 0.56 pairs nm⁻² corresponds to 0.93 μmol pairs per m². Thus a 20 mg bed with an **illustrative** measured area of 100 m² g⁻¹ contains about 1.86 μmol pairs. Its complete one-water-per-pair titration is an experimentally useful finite oxygen inventory. Actual area and uptake must be measured for each catalyst batch.

Titrate a known fraction with H2-18O, remove gas-phase label with a monitored purge, then expose to ethylbenzene at the native reaction conditions. Use matched destructive endpoint samples to count the pairs that become accessible again; do not derive both the water inventory and site recovery exclusively from the same deactivation fit. Activity is an additional observable, not a complete site census. Track surface OH and carbon-containing adsorbates where feasible, while recognizing that total OH intensity does not uniquely count the sparse active pairs.

For a finite transient, the excess oxygen input plus initial excess surface oxygen must equal oxygen leaving as water, COx, and organics plus the change in retained oxygen. Close the corresponding **18O balance separately**, including label retained or exchanged into the solid. Quantify carbon in assigned oxygenates, COx, and retained deposits against blank-corrected hydrocarbon consumption. The large ethylbenzene-to-styrene carbon flow makes an ordinary overall carbon closure of 99% nearly useless for a ppm pathway. Use isotope-resolved incremental balances, preferably paired 13C-ethylbenzene/18O-water experiments, and validated collection recovery.

Label in a product alone does not prove removal of the water oxygen originally blocking the active pair. Required controls include:

- H2-18O on zirconia with no hydrocarbon for the same time, temperature, and purge history, measuring exchange and water release.
- The corresponding unlabeled-water experiment and a dry activated-catalyst baseline.
- Labeled versus unlabeled ethylbenzene, to distinguish newly formed products from background carbon and feed impurities.
- Candidate oxygenates passed through the labeled surface and the collection system to test product oxygen exchange independently of their formation.
- A styrene-only or controlled styrene cofeed experiment to assess whether its role grows beyond the original low-conversion range.

Bound the solid isotope sink with a validated solid oxygen-isotope measurement or a stated inventory uncertainty. A convenient signal such as an OH infrared band or a surface isotope profile alone is not automatically a quantitative solid isotope balance. If lattice exchange dominates beyond measurable uncertainty, the isotope experiment cannot uniquely assign the oxygen source; rely on quantitative total oxygen removal and site recovery and report the remaining ambiguity.

An oxygenate route also needs chemically balanced stoichiometry. For example, ethylbenzene + water → ethylphenol + H2 differs from ethylbenzene + water → acetophenone + 2 H2. Do not label both simply “hydrolysis.” Their trace H2 increments may be experimentally inaccessible against the main dehydrogenation flow, so hydrogen balance can be a consistency constraint rather than a promised direct measurement.

**Chemistry gate:** establish a statistically resolved connection between oxygen export and site recovery across at least two initial titration inventories. For any claimed dominant route, the inventory uncertainty must be smaller than the fraction of site recovery assigned to that route. Do not set a universal 80% closure target if measurement uncertainty cannot justify it.

### 3. Measure return fractions before building a loop

Separate the condensed effluent into a recovered ethylbenzene fraction and the product/heavy fractions using a defined, credible separation. Determine species-specific returns with trace spiking and actual generated effluent. A cold trap returning every condensable molecule is not equivalent to ethylbenzene recovery by distillation. COx, water, aromatic alcohols/ketones, and phenols may follow very different outlets. Normal boiling points can guide the screen, but measured cut distributions are the decisive input.

For fixed reactor-inlet ethylbenzene molar flow, let:

- g_i be newly generated species i, mol per mol inlet ethylbenzene per pass;
- c_i be its inlet concentration on that same ethylbenzene basis;
- d_i be its fractional disappearance per reactor pass;
- a_i be the fraction of reactor-outlet species i returned after all separation and purge steps.

Then, for the simple noninterconverting case,

`c_i(next) = a_i [(1 − d_i)c_i + g_i]`

and

`c_i(steady) = a_i g_i / [1 − a_i(1 − d_i)]`.

These equations concern contaminant flux relative to a fixed inlet ethylbenzene flux. To obtain mol/mol total gas for kinetic dosing, convert using the actual reactor feed composition.

For d_i = 0, the inlet multipliers c_i/g_i are 0.0101, 1, 9, and 99 for a_i = 0.01, 0.5, 0.9, and 0.99, respectively. Thus an illustrative g_i = 1 ppm on the ethylbenzene basis gives about 0.01, 1, 9, or 99 ppm at the reactor inlet. A purge-limited 100-fold accumulation requires almost complete return of that species; it does not follow from efficient ethylbenzene recycle alone. Conversely, reaction disappearance is not necessarily detoxification: conversion to water or a stronger surface poison needs coupled species and site balances.

At steady state the ultimate oxygen source remains incoming water/O2 and any depletion of initial solid inventory. Self-cleaning cannot create oxygen indefinitely. However, the same oxygen can circulate as water and organic X many times; gross X generation need not be bounded by fresh oxygen input if X regenerates water. The whole-flowsheet oxygen balance must include that cycling and every exit stream.

**Partition gate:** continue toward a recycle program only when measured returns predict meaningful exposure. Low return plus no significant single-pass damage rejects the central recycle-accumulation concern.

### 4. Test inhibition at the predicted exposure

Compare once-through operation with a reconstructed recycle mixture at the same temperature, ethylbenzene, styrene, H2, water, total pressure, and residence time. Challenge with identified X singly and together, then with the measured recovered ethylbenzene cut. Match both concentration and cumulative dose per accessible pair. Low instantaneous concentration does not rule out slow irreversible poisoning, and a short high-dose test need not reproduce it.

Measure rate loss, site count, carbon retention, oxygen outlet, and recovery during a clean-feed washout. Separate immediate reversible inhibition from persistent site loss and from water formed by X conversion. Compare to a matched water-only dose. DME recovery is informative about reversibility but does not, by itself, identify the original poison.

If a cleanup treatment is tested, demonstrate what it actually removes. A nominal water trap may also remove X, confounding a claim that drying alone suffices. Compare inlet/outlet water and X and use a defined synthetic add-back where necessary. Correct net dehydrogenation for product approach to equilibrium; recycled H2 and styrene can reduce net rate without site poisoning.

**Process gate:** define an economically meaningful loss before testing—for example, an illustrative 10% persistent productivity penalty after exposure corresponding to a stated operating interval. Advance only if the penalty survives composition controls, occurs at measured credible recycle exposure, and is not cheaply avoided by the base-case separation or water cleanup. A demonstrably strong mechanistic result can still justify a smaller paper if this process gate fails.

## Practical significance and scale of the eventual program

Steam-free zirconia must be compared with low-steam Fe–K operation at common styrene purity, annual throughput, conversion, selectivity, and catalyst replacement assumptions. Steam supplies heat and dilution as well as affecting catalyst stability. Removing it leaves duties for reactor heat delivery, low partial pressures, vacuum/compression, cooling, separation, and impurity removal. Higher catalyst mass activity does not remove the endothermic reaction duty or solve the equilibrium constraint.

A useful flowsheet comparison therefore includes unconverted ethylbenzene recycle, H2 removal, water/O2 control on fresh and recycled feeds, any X guard-bed lifetime, regeneration frequency, purge/product losses, heat integration, and actual utility consumption. Evaluate at least a dry zirconia case with conventional ethylbenzene recovery, a dry zirconia case with the measured X-control requirement, and a credible low-steam Fe–K/vacuum case. Do not assign a process advantage from initial gravimetric rates alone.

The plausible major insight is a quantitative rule connecting surface clearance to exported oxygen chemistry and contaminant return: when a cleaning pathway is sustainable once the full reaction/separation loop is closed. That could generalize beyond styrene. The simpler outcomes—X exits naturally, independent water control is enough, or X only regenerates water—are at least as plausible today and should be designed as successful falsifications.

**Decision now: bounded screen.** Release a larger program only after analytically feasible native-condition oxygen accounting and a measured, consequential recycle pathway. Reject a proposal centered on “discovering self-cleaning,” “finding an oxygenate poison,” or adding a generic impurity trap as its main novelty.

## Final consistency check of the developed program — 2026-09-15

Reviewed `research/programs/zirconia-styrene-oxygen-fate.md` and `research/calculations/styrene-recycle-bounds.md`. **No blocker to the bounded first campaign.** The recommendation, prior-art limits, alternative explanations, conditional progression, and practical caution agree with this independent review. The proposed molecular reaction examples are atom-balanced. The species-recycle equation and three-state steady site fraction are algebraically correct under their stated assumptions. The equilibrium quotient is correct for the stated product-free, ideal-gas feed if its pressure convention is made explicit.

Four short clarifications are required before treating the experimental plan as definitive:

1. **Add product oxygen-exchange controls.** Passing an authentic candidate oxygenate over an 18O-labeled surface, and through the sampling train with labeled water, tests exchange into a pre-existing product independently of product formation. A no-ethylbenzene surface control alone does not exclude this confounder. Make the test contingent on which products are identified.
2. **Require incremental carbon accounting at the cleaning-flux scale.** “Ordinary carbon and oxygen balances as far as sensitivity permits” is too weak if read as a bulk ethylbenzene carbon closure. Even a 99% bulk carbon closure can conceal the entire ppm pathway. Explicitly compare the analytical uncertainty of blank-corrected oxygenate/COx/retained-carbon fluxes with the proposed cleaning flux. Use targeted labeled-ethylbenzene follow-up where the main carbon stream prevents a useful bound. Define the matched functional-capacity measurement, such as calibrated water uptake with activity response, rather than equating recovered rate with an independent site census.
3. **Separate organic blockage from water regenerated by X.** Aim 2 should explicitly measure water formed during X exposure, compare a matched water-only dose, and verify whether the proposed water trap also removes X. If X only reproduces water titration, the oxygen-management problem may remain relevant, but the specific persistent organic-poisoning interpretation fails. Concentration and cumulative exposure per accessible pair should both be matched to the proposed operating history.
4. **State the pressure standard in the equilibrium expression.** For dimensionless thermodynamic Kp write `Qp = (P/p°)*x²/[(1−x)*(1+s+x)]`. The existing expression with P alone is valid as a dimensional pressure quotient if Kp uses that same pressure convention; say which is intended.

No additional literature search was needed for this check. The SI-dependent ppm denominator and instrument-specific recovery limits remain explicitly pending, appropriately. The first campaign should retain its analytical feasibility gate; none of these corrections supports immediate construction of a recycle loop or a claim of process improvement.

## Challenge of the feed-scaling inference — 2026-09-15

**Verdict:** the local scaling and integrated steady PFR balance are correct with explicit consistent units and the stated kinetic assumptions. They are useful experimental-design consequences of the published model, not a new mechanism or a substantial result by themselves. I checked SI p.10 against its original PDF image.

### Local kinetics and source dependence

With `A = kc*cEB`, `B = kw*cwater`, and constant local concentrations, the consistent site balance is `dtheta/dt = A − (A+B)*theta`. Thus `theta_ss = A/(A+B)` and `lambda = A+B`. Scaling both concentrations by the same factor preserves theta_ss and multiplies the local relaxation rate by that factor. Raising ethylbenzene at fixed water improves theta_ss. These statements assume unchanged rate constants, site population, and competing species; they do not establish that a real feed change respects those assumptions.

Consequently, an ethylbenzene-borne water impurity at a fixed molar water/ethylbenzene ratio does not become less inhibitory merely by removing inert dilution. A fixed external water concentration behaves differently. “Carrier water stays fixed” must be an imposed condition or a measured approximation: replacing carrier with ethylbenzene can change the carrier-borne water flux. The catalyst responds to mixed-feed concentrations, not to the upstream identity of the water source.

The SI has genuine printed dimensional inconsistencies: its rate and rate-constant units under S11–S13 do not match its rate expressions, and S18 places bed density on only the right side of a mass-specific site balance. Do not reproduce those labels or that density factor. Define `kc, kw` as volume/(mol·time), `ns` as mol sites/mass, and one titration event per blocked pair. Then `A`, `B`, and `lambda` have units of inverse time, without a bed-density factor.

### Steady PFR check

For constant volumetric flow Q at reactor conditions, uniform ns and rate constants, negligible ethylbenzene depletion, no water-forming secondary reaction, and locally stationary site coverage:

```text
Q*dcwater/dW = −ns*kw*cwater*A/(A+kw*cwater)
ln(cwater_out/cwater_in) + (kw/A)*(cwater_out−cwater_in)
    = −ns*kw*W/Q.
```

Both terms on the left and the right side are dimensionless. The logarithm requires positive inlet/outlet concentrations. At low water the profile tends toward exponential depletion; at high water the consumption rate approaches the cleaning-limited ceiling `ns*A`. This is a steady concentration profile, not a prediction of a moving transient front.

At fixed W/Q, jointly scaling inlet water and ethylbenzene preserves the normalized steady water profile and theta profile in this same model. Changing pressure at fixed molar flow changes Q, however, so an inlet ratio alone does not fix the bed-averaged state. Heating, pressure drop, integral ethylbenzene conversion, oxygenate-to-water reactions, or irreversible inventories require a coupled balance. A low ethylbenzene conversion does not guarantee negligible axial water depletion.

### Minimal discriminating experiment

Use a small 2 × 2 matrix: `(cEB,cwater) = (e,w), (alpha*e,w), (e,alpha*w), (alpha*e,alpha*w)`, with alpha modest enough to remain in the original kinetic regime. Hold temperature, total pressure, H2, and total volumetric flow fixed; replace inert as needed. Measure water rather than relying on nominal additions. Select catalyst mass/flow so water gradients are demonstrably small, or explicitly fit the PFR instead of a single relaxation.

The diagonal tests equal-ratio invariance. The off-diagonals distinguish ethylbenzene enrichment from water increase. Normalize rate by the clean-state rate at each composition, account for affinity, and use a calibrated accessible-site fraction with a repeatable initial state. Correct sampling delays and test repeated baseline returns so drift is not interpreted as a concentration effect. Within the model, the diagonal relaxation constants differ by alpha; one off-diagonal changes only A, the other only B.

Only with known local concentrations and calibrated theta can `kc = lambda*theta_ss/cEB` and `kw = lambda*(1−theta_ss)/cwater` separate the two constants. Steady coverage alone identifies only their ratio. Near theta = 0 or 1, one estimate becomes poorly conditioned. A bed-average rate transient can contain multiple local relaxation rates plus changing water penetration and cannot generally be assigned one mechanistic lambda.

For **source-resolved** specifications, add independent component-stream water measurements or bypass blanks for the ethylbenzene delivery, carrier/H2 supply, and mixing train. The 2 × 2 kinetic experiment alone cannot identify where natural moisture entered. An additive source-flux balance can then translate a target mixed-feed ratio into requirements for each stream; oxygen ingress that forms water requires separate accounting.

### Practical value and novelty

This screen can prevent a wrong claim that concentrating ethylbenzene automatically solves water inhibition, and can direct drying effort to the responsible feed stream. A target local coverage gives the conditional specification `cwater/cEB <= (kc/kw)*(1−theta_target)/theta_target`; it is not a universal ppm specification. Simple confirmation of these scaling relations is routine model validation. Greater value requires independent prediction across changed feeds or a material failure of the two-state model tied to measured oxygen fate. Keep this experiment inside the bounded first campaign, not as grounds to launch the full recycle program.

## Target-product accounting for the native pilot — 2026-09-15

**Yes: explicitly quantify or bound ethylbenzene diverted from styrene, alongside oxygen fate and carbon closure.** The paper defines its selectivity discussion around dehydrogenation versus C–C scission; p.5 explicitly uses `rdehyd/rC–C`, while the methods describe carbon-based accounting for those product channels. That evidence does not independently quantify an unidentified cleaning-product channel. It also does not establish that the published selectivity is wrong. [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]] p.3, p.5, p.7.

For an illustrative stationary, once-through balance, let `nu` be ethylbenzene molecules diverted from target styrene per oxygen atom exported by the relevant cleaning route, and `f` the fraction of inlet water oxygen exported by that route. If water is the only oxygen input and inventories are stationary, the diverted fraction of reacted ethylbenzene is

`Lclean = nu*f*ywater/(yEB*XEB) = nu*f*beta/XEB`,

where `XEB` is actual total ethylbenzene conversion, `beta = ywater/yEB`, and all mole fractions use the same inlet-total-gas basis. This is a conditional accounting relation; `f = 1` supplies a bound for specified nu, not a measured capture fraction.

At `yEB = 0.012`, `ywater = 4e−6`, and `nu*f = 1`, ethylbenzene conversion of 0.5%, 1%, and 2% corresponds to 60, 120, and 240 ppm reacted ethylbenzene on the inlet-gas basis. The conditional cleaning diversion is therefore **6.7%, 3.3%, and 1.7% of reacted ethylbenzene**, respectively. A small gas-phase oxygen flux can thus be material compared with a low-conversion product flux. These examples do not reproduce a complete reported experiment or demonstrate such a loss. The estimated approximately 10 ppm X is unmeasured and must not be inserted as an independently measured oxygen or carbon flux.

The pilot should report net styrene formation, ethylbenzene-equivalent carbon assigned to cleaning products, other side products, and retained carbon, with uncertainty relative to **reacted ethylbenzene and net styrene**, not only total feed. Do not double-count: a cleavage cleaning route producing toluene or benzene may overlap the paper's already measured scission channel. Reconcile complete product events and carbon atoms before assigning an additional penalty. Likewise, an oxygenated intermediate later yielding styrene is a per-pass diversion, not necessarily an ultimate process yield loss.

Apply the bound to net oxygen export. Gross cleaning turnovers can exceed fresh-water input if products regenerate water; then a simple f bounded by one cannot describe gross turnover without further accounting. During a recovery transient, depletion of preloaded hydroxyl or lattice oxygen also invalidates the inlet-water-only bound; use the measured finite oxygen inventory. At higher conversion the same fixed impurity burden could become a smaller fractional sacrifice, but neither constant f/nu nor unchanged chemistry is established. Use actual net rates for this product accounting, not equilibrium-corrected forward dehydrogenation rates.

## Paired-product imbalance as a pilot cross-check — 2026-09-15

**Worth including as a modest screening cross-check, not as a standalone measure of cleaning.** The main text reports equimolar methane/toluene and ethane/benzene. Its methods describe GC-FID/TCD measurements and standards/MS for identification. However, SI Figure S1 calculates terminal and nonterminal cleavage rates from **toluene and benzene formation**, respectively; it does not supply paired methane/toluene or ethane/benzene ratios with the calibration, replicate precision, and covariance needed to infer a numerical imbalance bound. I inspected original SI p.4. [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]] p.2-3; SI p.4, Figure S1.

Use separately calibrated, inlet/background-corrected net molar fluxes, measured over matching collection intervals:

`Delta_T = Jtoluene − Jmethane`; `Delta_B = Jbenzene − Jethane`.

In a restricted model containing only conventional paired cleavage and hydrolytic cleavage, with stable products, these differences equal the rates of `EB + H2O → toluene + methanol` and `EB + H2O → benzene + ethanol`, respectively. Conventional cleavage instead satisfies `EB + H2 → toluene + methane` or `EB + H2 → benzene + ethane`. All four net equations are atom-balanced. A measured positive imbalance would therefore motivate examining the missing C1/C2 carbon and oxygen; it would not identify hydrolysis or prove active-pair recovery.

Calibrate the **difference uncertainty**, including response factors, trace recovery, inlet aromatic contamination, and correlated flow error. Compare dry baseline, labeled-water recovery, and blank histories. Track methanol/ethanol, COx, other C1/C2 products, and retained carbon alongside the pairs. Secondary alcohol conversion can preserve, redistribute, or erase the imbalance; methane/ethane formed from other sources can cancel it. Ethane-to-ethylene conversion can create an apparent benzene excess without hydrolytic cleavage. Feed aromatics, ordinary decomposition, residual DME, and preloaded carbon are additional alternatives.

Even exact equimolarity cannot generally bound gross hydrolytic cleaning. For example, if a fraction a of a hydrolysis-derived C1 coproduct eventually appears as methane, then `Delta_T = (1−a)*rhydrolysis` under otherwise ideal assumptions. As a approaches one, the null imbalance loses its upper-bound power. A quantitative bound requires both measurement precision and a justified lower bound on the surviving imbalance per cleaning event. The existing qualitative equimolarity statement supplies neither.

The limited useful inference is: **a resolved change in paired-product imbalance tests whether the simple paired-cleavage accounting remains sufficient during recovery and directs the oxygen/carbon search. A null result constrains only unmasked imbalance at the achieved precision.** It cannot exclude ring hydroxylation, intact C8 oxygenates, or hydrolysis followed by compensating secondary chemistry. Keep this cross-check within the existing product-analysis workload and avoid launching a separate campaign around it.
