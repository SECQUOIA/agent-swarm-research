# Polymer ethenolysis: a recovered patent benchmark

2026-09-15. Root assessment of [WO2026011187A2, Conversion of polyolefins](https://patents.google.com/patent/WO2026011187A2/en), published January 8, 2026. The authentic patent HTML was retrieved to `/tmp/polymer-primary-gap/WO2026011187A2.html`; experimental text was read. Equations and figures are partly missing from this rendering. Patent intake and original-figure recovery were sent to the sole literature worker. At the 2026-09-15 review, the Science 2024 article and SI were separate unread sources; their uploaded originals are now checked as described below. An [independent protocol and arithmetic review](polymer-patent-protocol-review.md) checked these conclusions against the patent text.

**2026-09-16 correction after upload:** the [post-upload audit](post-upload-polymer-audit.md) visually checked Science Figure 4B and SI S20. The published reference uses **three total 1 g PE charges, with 400 mg fresh Na/alumina added before charge 2 only**; charge 3 receives only PE. The nominal fresh-solid total is 1.2 g and the conditional three-charge material-productivity ratio is `B = 2f`, not the separate every-later-charge illustration `B = 1.5f`. The Science SI reports **19.9658 g warm oil, 29.9717 g remaining solid and 80.1% apparent conversion** for its scale-up; the patent record below contains different numbers and remains a distinct source. Neither residue subtraction nor the condensate volume/density estimate closes a polymer-specific carbon balance. These corrections supersede the old missing-dose/Science-access limits; patent regeneration figures and the dissertation body remain unresolved.

## Decision

**The patent supplies a much firmer baseline for the conditional impurity-budget idea, while removing novelty from Na replacement and contaminant sensitivity themselves.** It does not establish that a new protective material is needed or that contaminant delivery controls the observed clean-feed reuse loss. The next useful distinction is whether a measured feed exposure explains a consequential repeated-charge loss beyond the clean-feed baseline and predicts a less burdensome feed preparation or catalyst-use policy.

## What the experimental disclosure establishes

| Observation | Source location | Interpretation boundary |
|---|---|---|
| A standard PE charge uses 1.000 g polymer, 400 mg WO3/SiO2 with 0.110 mmol W, and 400 mg Na/γ-Al2O3 with 1.740 mmol Na. Batch reaction is 320 °C for 90 min after charging ethylene and methane internal standard. | §0165 | Initial combined catalyst/polymer mass ratio is 0.8 g/g. This is a demonstrated recipe, not an optimized minimum inventory or proof of stoichiometric catalyst use. |
| Repeated HDPE charges on the same mixture lose output; the text says 50% activity retained after each subsequent run and 1030 total W turnovers over three runs. Adding fresh Na/alumina in the second cycle reportedly restores activity for two new cycles. | §0135, Figure 3B referenced but not recovered | Component supplementation is direct prior art. Science Figure 4B now resolves the three-charge schedule and 400 mg addition before charge 2 only; exact bar values are not raw data. Endpoint yield is not an independently established intrinsic activity or unique identification of the damaged function. |
| A 50 mg additive is mixed with 1 g HDPE: PVC, PET and DEHP reduce propylene yields to 20.5%, 16.9% and 25.7%, respectively; PS has a smaller reported effect. | §§0133, 0168 | This is 5 wt% relative to HDPE, not a trace-feed specification. It does not identify poison delivery, a tolerable cumulative dose, or the affected component. |
| Waste objects are dissolved in boiling toluene, precipitated in methanol, filtered, dried under vacuum for 18 h and ground. | §0198 | High yields from these samples do not demonstrate tolerance of untreated collected waste. The laboratory recipe charges 25 L toluene and 250 L methanol per kg starting sample; these are preparation volumes, not unrecovered industrial solvent demand. |
| The disclosure includes air treatment, air followed by H2, and air/He/DME/He regeneration protocols, plus Fe-containing catalyst variants. | §§0172–0177; Figure 21 referenced | DME regeneration is already disclosed. Missing figures and ambiguous catalyst identity prevent assigning its efficacy specifically to the original Na/alumina–W mixture. Do not infer a successful treatment merely from a method heading. |

## Elemental loading does not identify sacrificial protection

The reported contaminant doses correspond to the following **input** inventories, calculated from the source's molecular/repeat-unit amounts:

| Added material | Relevant elemental input | Atoms per bulk Na atom | Atoms per bulk W atom |
|---|---:|---:|---:|
| PVC, 0.800 mmol repeat units | 0.800 mmol Cl | 0.46 | 7.3 |
| PET, 0.260 mmol repeat units | 1.040 mmol O | 0.60 | 9.5 |
| DEHP, 0.128 mmol | 0.512 mmol O | 0.29 | 4.7 |

These numbers are not measured poison doses reaching W or Na. Polymer-bound oxygen can remain inaccessible; degradation can form several compounds with different effects; bulk Na is not a count of useful sites or a validated scavenging capacity. Severe loss before one input heteroatom per bulk Na does not disprove capture by a smaller accessible population. Conversely, bulk Na excess cannot establish protection. Measure delivery and retained function before interpreting a capacity threshold.

## Separate polymer recovery from ethylene incorporation

Ideal complete PE ethenolysis follows the repeat-unit balance

`(C2H4)_polymer + 2 C2H4 → 2 C3H6`.

Thus most product carbon can come from the ethylene cofeed even when nearly all polymer carbon is recovered. Section 0130 reports 62.2 mmol propylene and 62.5 mmol ethylene consumption from the standard HDPE charge. Dividing propylene by twice 35.65 mmol PE repeat units gives about 87.2%, consistent with the reported yield convention. It is not a product-mass fraction of the original plastic. Section 0134's labeled-polymer result argues against a dominant ethylene-only product route; it should not be paraphrased as showing that all propylene carbon came from PE.

For a new repeated-charge test, report cumulative polymer carbon in accepted products, net ethylene consumption, product carbon from each feed where distinguishable, and all retained/withdrawn inventories. A reported W turnover number counts product molecules, including carbon supplied by ethylene; it is not independently a polymer-carbon recycling efficiency.

## The larger-scale result has a different denominator and incomplete accounting

The 50 g example starts with 10 g of each catalyst, giving 0.4 g combined solid per g HDPE. It runs for three hours with an ethylene stream and staged condensation (§§0228–0231). The authors explicitly identify mixing as important and modify the impeller. Therefore, the standard 1 g batch performance cannot be transferred directly to this run or used to prove intrinsic kinetics.

The cold condensate is reported as 90 mL, approximately 76.1 mol% propylene and 21.1% butenes (§0236). The source estimates 1.00 mol propylene, 28.1% of the ideal PE-to-propylene amount and 364 turnovers per W. The earlier 438-turnover statement concerns the mixed light-olefin condensate (§0137); it must not be presented as 438 propylene turnovers.

Two limits prevent reconstructing a precise complete balance from this rendering:

- The warm condensate is 20.0 g in §0137 but 11.81 g in §0233. Do not silently select one or add incompatible records.
- Section 0236 describes its composition as a mole fraction but reproduces an estimate consistent with `V × assumed density × x_propylene / M_propylene`. If density is the total mixture density and `x` a mole fraction, conversion to moles requires the mixture-average molar mass. The density is itself approximated by pure propylene at its boiling point. Preserve 1.00 mol as the source's estimate; Science SI S20 now supplies the original equation S18 and directly reports 1.00 mol propylene, 28.1% yield and 364 W turnovers. Incomplete composition and unmeasured mixture density still prevent claiming a corrected measured yield.

For the **patent record**, the remaining reactor solid is 35.100 g (§0234). Subtracting the initial 20 g catalyst gives 15.100 g apparent unconverted polymer and the reported 69.8% conversion. This inference assumes the remaining noncatalyst mass is unconverted HDPE and the catalyst mass has not changed; it is not an independent polymer-specific assay. The **Science SI S20 record differs**: 19.9658 g warm condensate and 29.9717 g remaining reactor solid, assigned 80.1% apparent conversion after the same nominal 20 g catalyst subtraction. Preserve these source-specific numbers rather than silently selecting one as a correction to the other. The Science main text's 438 TON refers to mixed collected olefins; its SI gives 364 propylene-only TON. Neither is a catalyst-lifetime result.

These qualifications do not negate the larger-scale demonstration. They prevent conflating gas yield, isolated condensate, polymer conversion and carbon recovery when defining the next practical target.

## Consequence for the retained research idea

### An external light-olefin comparator requires a different comparison

Akin et al., [10.1016/j.jaap.2023.106036](https://doi.org/10.1016/j.jaap.2023.106036), report up to 83.4 wt% C2–C4 olefins from catalytic upgrading of mixed-waste pyrolysis vapors. The [institutional accepted manuscript](https://biblio.ugent.be/publication/01H8KCCAZPFQH7N44KMQAYSF6A/file/01H8KCDEDJ76F7HX0M0KMN4QCA.pdf) was recovered; methods and selected results were read here. It uses 0.5 mg waste pulses, typically 20 g catalyst/g plastic, 600 °C and about 2.7 bar absolute in a helium-diluted tandem micropyrolyzer (§§2.1, 2.3–2.4). Fresh catalyst is used after four experiments. This does not establish useful repeated-feed lifetime at a small catalyst inventory.

The waste includes PE, PP, PA, PET, PS and nonpolymer material; preparation uses grinding and sieving. Its vapor-stage catalyst encounters a different contaminant exposure from a melt-contact catalyst. Reported catalytic mass closures span 90–110%; coke was not directly quantified. The thermal reference closes only 61% because heavy compounds lie outside the analytical range. These conditions limit fine yield comparisons and any durability inference.

This is a relevant chemical selectivity benchmark, not a matched process contest. Comparing its 83.4 wt% mixed light-olefin result with an 87% stoichiometric propylene yield from ethenolysis would conflate product slate, cofeed carbon, catalyst inventory, exposure and temperature. Neither isolated reactor temperature nor fresh yield establishes the better complete process. Source artifacts were sent to the sole literature worker; SI remains to be assessed.

### Retained decision

Start with clean-feed repeated charges and one characterized feed preparation contrast. Determine whether an additional loss is explained by contaminant delivery, changing polymer access, or the known baseline decay. A generic rescue with fresh Na is insufficient because it is already reported and can change several functions simultaneously. A meaningful advance would predict cumulative useful polymer-carbon output and a better cleanup/replacement/regeneration choice with fixed parameters under a withheld exposure history.

Confidence is high that the disclosed baseline has a substantial reuse and contamination burden. Confidence is lower in any particular cross-protection mechanism, and low in a practical improvement before the cleanup and catalyst-inventory costs are measured. The patent improves experimental specification; it does not automatically move this proposal above the other bounded candidates.
