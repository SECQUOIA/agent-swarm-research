# Oxygen-fate measurements: feasibility and decision limits

Date: 2026-09-15. Independent, bounded experimental review of the [oxygen-fate program](../programs/zirconia-styrene-oxygen-fate.md) and [independent review](styrene-independent-review.md).

## Decision

**Proceed with a small analytical validation campaign. Do not yet describe H2-18O prelabelling as a way to assign the oxygen specifically to active-pair poisons.** The expected finite oxygen inventory is measurable in principle: roughly 0.24–2.4 μmol for 10–100% of a representative 20 mg bed's active pairs. Actual feasibility depends on collection recovery, blank variability, exchange, and independent site-count precision. No instrument capability is established here.

Prelabelling can establish transfer of water-derived oxygen to an organic product. Assigning that transfer to the removal of the species that blocked an active pair additionally requires controls for water release, exchange with other oxygen reservoirs, product oxygen exchange, and retained deposits. A total isotope balance, even if closed, does not itself localize the original label to active sites.

The weakest step is likely quantitative retained-label accounting and attribution, rather than the nominal amount of a collected organic compound. If exchange cannot be bounded tightly enough, retain the narrower oxygen-transfer result and use total oxygen removal plus independent site recovery to test cleaning stoichiometry.

## 1. Basis and inventory calculation

The focal paper reports 0.02 g zirconia mixed with 1 g quartz (section 2.2), 0.56 active pairs nm−2 from earlier water titrations (section 3.6), and recovery experiments at 773 K, 1.2 kPa ethylbenzene and 12 kPa H2 (Figure 5). The newly retrieved 2025 SI, p.6, section 1.3, explicitly uses 20 mg, 130 m² g−1, and 0.56 sites nm−2 to calculate 2.4 μmol LAB pairs. Thus this inventory is the focal paper’s stated basis, rather than a transferred area assumption. It remains necessary to measure the actual campaign batch area and working accessible-site inventory; the earlier paper reports area loss at higher treatment temperature. See the SI addendum below. Sources: [[artsiusheuski2025-selective-ethylbenzene-dehydrogenation-to-styrene]], p.2, p.6–7, [DOI](https://doi.org/10.1021/acscatal.5c04904); [[jaegers2024-heterolytic-ch-activation-routes-in]], p.2, [DOI](https://doi.org/10.1021/jacs.4c07766).

Using Avogadro's constant and 123.222 g mol−1 for ZrO2:

```text
Area = 0.020 g × 130 m²/g = 2.60 m²
Active pairs = 2.60 × 10^18 × 0.56 / NA = 2.418 μmol
Lattice O atoms = 2 × 0.020 / 123.222 = 324.6 μmol
Lattice O / active pairs = 134
```

One water molecule per blocked pair is a **design hypothesis to test**, not an automatic interpretation of label uptake. Under that hypothesis:

| Fraction of all pairs titrated and subsequently recovered | Oxygen associated with recovery | Mass if entirely exported as one-O product of 120 g/mol |
|---|---:|---:|
| 10% | 0.242 μmol O | 29 μg |
| 25% | 0.604 μmol O | 73 μg |
| 100% | 2.418 μmol O | 290 μg |

A 10% organic branch of the 25% case contains only 0.0604 μmol O, or 7.3 μg of that example product. If the product contains two oxygen atoms, count atoms separately; product moles no longer equal oxygen moles. The 120 g/mol example represents an approximate aromatic oxygenate mass, not a predicted product identity.

The zirconia lattice is not the only reservoir. The reported 1 g quartz diluent contains about **33.3 mmol structural oxygen**, over 100 times the zirconia oxygen inventory. This arithmetic does not imply that bulk quartz exchanges at 773 K; it makes a matched quartz-only experiment and separation of catalyst from diluent essential. Reactor walls and quartz wool add possible surface storage. We must measure accessible exchange, not infer its rate from bulk capacity.

## 2. Flux and collection time

For an **illustrative** 100 standard cm³/min total flow, defined here at 273.15 K and 1 atm, the total molar flow is 0.2677 mol/h:

```text
1 ppm mol/mol total gas = 0.2677 μmol/h
Mean product ppm = exported product μmol / (0.2677 × collection hours)
```

| One-O export inventory | Mean ppm over 1 h | Mean ppm over 14 h |
|---|---:|---:|
| 0.242 μmol | 0.90 | 0.0645 |
| 0.604 μmol | 2.26 | 0.161 |
| 2.418 μmol | 9.03 | 0.645 |

A 10% branch gives one tenth of these concentrations. Temporal peaks can differ greatly from these averages. Online nondetection cannot bound an integrated transient without time resolution, calibration, and sampling coverage.

**100 standard cm³/min is not a recommended reproduction flow.** At the reported approximately 4 mol kg−1 h−1 initial rate, a 20 mg bed produces about 80 μmol styrene/h. With 1.2 mol% ethylbenzene, 100 standard cm³/min would imply approximately 2.5% conversion; about 125–500 standard cm³/min would span 2–0.5% at that rate. These are idealized design calculations, not reported experimental flows. Preserve measured conversion and partial pressures; concentration signals scale inversely with flow.

The retrieved SI establishes a **total-gas basis for the estimated water ppm** by dividing the site inventory by total gas throughput. The water levels remain model-derived rather than independent moisture measurements. The main text’s approximately 10 ppm estimate for X points to SI section 1.3, but that section calculates inlet water rather than independently measured X; do not treat 10 ppm as a measured product concentration. State the concentration basis explicitly in every new collection calculation.

Longer collection accumulates a continuing source, but **cannot increase the total signal of an exhausted finite prelabelled reservoir**. Once the transient ends, longer sampling adds blank and feed background. Pool repeated independently validated cycles or increase catalyst throughput while preserving chemistry if necessary; do not assume label uptake or site capacity remains constant across cycles.

## 3. Why label location is difficult

Let a 25% site-recovery experiment contain 0.604 μmol site-associated oxygen. For a design example with water at 90 atom% 18O and an approximate 0.2 atom% natural baseline, its expected excess label is only:

```text
0.604 × (0.900 − 0.002) = 0.543 μmol excess 18O
```

Use measured starting isotope composition and certified label enrichment in the real calculation. If all this excess label were dispersed uniformly through zirconia oxygen, it would increase bulk 18O abundance by only 0.167 percentage points. Detecting that increase would not say which sites exchanged. Exchange of an amount equivalent to just 0.19% of the lattice oxygen already matches the entire 25% site-recovery oxygen inventory. These are capacity comparisons, not evidence for rapid lattice exchange.

Water dissociation can place a proton on a pre-existing surface oxygen as well as create an OH containing the incoming water oxygen. Recombination, exchange, and migration can therefore separate the label from the original blocking configuration. Preferential binding at active pairs does not establish exclusive labelling of those pairs. Increasing label dose to saturate a large background reservoir would compromise the intended selective partial titration.

Distinguish four observables:

| Observation | What it establishes | What remains unresolved |
|---|---|---|
| Labelled water leaves during purge or recovery | Water oxygen reaches the effluent | Thermal desorption versus exchange; whether the rate-blocking population was removed |
| Labelled organic product leaves | Water-derived or exchanged oxygen enters an organic molecule | Whether it caused site recovery; post-formation oxygen exchange; carbon origin |
| Label remains on the solid | A retained isotope inventory, if measured quantitatively | Lattice/surface exchange versus an organic deposit; whether it blocks active sites |
| Activity or titratable capacity recovers | Functional change under the measurement conditions | Oxygen route and exact one-water-per-pair stoichiometry |

Candidate oxygenates must be passed over the labelled surface and through the sampling train to test oxygen exchange after formation. A product could acquire 18O by exchange without removing a poison. An unlabeled product could arise from labelled water after dilution into a larger oxygen reservoir. Neither result alone identifies or excludes cleaning.

## 4. Minimum measurements and controls

1. **Inputs and apparatus.** Calibrate admitted water moles and isotope composition, carrier/organic flow, and oxygen leakage in the actual matrix. Run the entire exposure/purge/reaction sequence on an empty train and a matched 1 g quartz bed with wool. Measure water tails and delayed release through traps and storage. Use repeated procedural blanks to measure variability and drift, not just a clean chromatogram.
2. **Functional inventory.** Measure the partially poisoned starting state and recovered endpoint on matched samples using calibrated uptake/site titration and activity. Endpoint titration changes the specimen; use separate specimens for isotope accounting. Report uncertainty in the difference between endpoints. An activity change is not automatically proportional to all sites under changed feed or inhibition conditions.
3. **All oxygen exits.** Quantify H2O isotopologues, CO, CO2, condensable oxygenates, and any identified volatile oxygenates over the full transient. Count singly and doubly labelled CO2 separately. Calibrate isotope response and molecular/fragment interferences using unlabeled matrix and labelled standards where available. An M+2 organic peak alone is inadequate because natural carbon isotope combinations and coelution can contribute.
4. **Collection recovery.** Spike representative products upstream of the hot train at the expected cumulative dose, concentration, and matrix. Determine recovery, breakthrough into a backup trap, storage stability, and carryover. Use compound-specific calibration for assigned products. Unknown peak areas are not quantitative oxygen balances without defensible response-factor bounds. Recovery need not be close to 100%, but its correction and uncertainty must meet the inventory budget.
5. **Exchange and desorption controls.** Use identical label dose, purge, temperature, H2, and elapsed time with no ethylbenzene; unlabeled-water counterparts; dry activated zirconia with ethylbenzene; and initially hydroxylated zirconia. The matched no-hydrocarbon experiment controls thermal release; it cannot automatically reproduce hydrocarbon-induced exchange. Use at least two resolved titration inventories and seek a relationship between recovered capacity and incremental oxygen export.
6. **Retained matter.** Obtain quantitative bulk oxygen-isotope inventories before and after on matched specimens if full closure is claimed. Quantitative conversion of refractory zirconia oxygen to a measurable form may require a specialist isotope laboratory and recovery standards. Do not assume routine combustion/pyrolysis extracts all lattice oxygen. Surface isotope profiles and infrared OH bands alone do not provide whole-solid isotope inventories. Measure retained carbon separately; oxidative burnoff can quantify carbon but introduces external oxygen and cannot automatically recover the original deposit oxygen isotope balance. Separate zirconia, diluent, and train inventories or validate their combined accounting.
7. **Carbon source.** If residual DME, pre-existing carbon, or feed impurities remain plausible contributors, use a targeted 13C-ethylbenzene experiment. This labels the carbon source; it does not independently locate the oxygen source. Avoid relying on total reactor carbon closure to detect a minor oxygen-transfer route.

## 5. Error budget and go/no-go rules

Define excess label relative to the measured unlabeled baseline and calculate every term in moles of 18O atoms:

```text
Residual = admitted excess 18O
         − all effluent excess 18O
         − change in solid excess 18O
         − change in train/trap excess 18O
```

For a recovery-stage balance, the initial solid/train inventory after purge replaces the original admission; quantify it with matched specimens or include the entire dosing/purge history. Do not count captured effluent twice as both effluent and trap accumulation. Propagate calibration, blank, recovery, integration, specimen variability, and shared-reference covariance. A small residual produced by defining solid retention as the missing amount is not independent closure.

**Illustrative design target, not an established success criterion:** distinguish pathways separated by 10% of the 0.543 μmol excess-label inventory. Then the combined 95% uncertainty and conservative unmeasured bounds must be appreciably below approximately 54 nmol 18O. A possible allocation for calibration development is:

| Inventory contribution | Illustrative 95% uncertainty allocation |
|---|---:|
| Admitted dose and enrichment | 10 nmol |
| Integrated water outlet/tail | 15 nmol |
| Organic outlet, including recovery correction | 15 nmol |
| CO/CO2 outlet | 10 nmol |
| Change in solid retained label | 20 nmol |
| Train storage and procedural blank correction | 15 nmol |

If independent, these expanded contributions combine to approximately 36 nmol by root-sum-square. Correlated errors require covariance; unbounded bias or unidentified channels cannot be reduced by this arithmetic. These numbers are requirements to check experimentally, not a claim that available equipment meets them. A looser scientific question can use a looser budget stated in advance.

The 20 nmol solid allocation corresponds to approximately **0.0062 atom-percentage-point precision in the change of whole-zirconia 18O abundance** at 324.6 μmol total oxygen. Sample preparation, isotope extraction, specimen heterogeneity, oxygen inventory changes, and natural-baseline subtraction must all fit within that allocation. Bulk isotope precision alone is insufficient. Quartz contamination would increase the denominator and alter this requirement.

Independent site recovery can be equally limiting. In the 25% example, a ±10% uncertainty on the recovered 0.604 μmol capacity means ±0.0604 μmol. Two independent endpoint counts with equal uncertainty would each need approximately ±0.0427 μmol, or ±1.8% of the initial 2.418 μmol full capacity, using the same confidence convention. Two counts each uncertain by 5% of full capacity would give a difference uncertain by approximately 28% of the recovered capacity. Do not claim a precise oxygen-per-recovered-pair ratio from those counts.

Use these gates:

- **Detection gate:** the blank-corrected incremental product signal must be statistically resolved and above the whole-method quantification limit after collection/recovery correction. Demonstrate this with low-level spikes and replicate blanks in the relevant matrix. Instrument detection limit alone is insufficient.
- **Exclusion gate:** to exclude a branch carrying 10% of the illustrative site oxygen inventory, its total oxygen-equivalent upper bound must be below 60 nmol O; on the assumed excess-label basis, below 54 nmol 18O. Sum bounds across missing channels. A labelled-channel nondetection cannot exclude an unlabeled product route when dilution/exchange is unresolved.
- **Attribution gate:** recovered capacity and corrected oxygen export must covary across at least two titration inventories, while desorption, exchange, pre-existing organic oxygen, and storage alternatives are bounded below the assigned flux. Fit a plausible stoichiometry with uncertainty rather than imposing one O per pair.
- **Closure gate:** independent residual uncertainty and unresolved inventory must be smaller than the route contribution being claimed. A blanket “80% isotope closure” would leave approximately 109 nmol unresolved in the example, already twice the proposed 10% branch. Even 100% total closure does not eliminate exchange between site populations.
- **Stop or narrow:** if solid/train storage or isotope exchange remains comparable to the cleaning signal, stop attempting site-specific oxygen attribution from prelabelling. Report product oxygen transfer, an oxygen-export bound, and independent functional recovery. Escalate to specialist solid-isotope measurements only if the remaining mechanistic question warrants the cost.

## Overall judgment

The finite inventory is large enough to justify measured recovery and blank trials. It does not justify assuming that online GC-MS, an infrared OH signal, and an ordinary carbon balance will close the experiment. A careful first campaign can distinguish substantial organic export from predominantly water release, or place a useful bound on either, provided the appropriate uncertainty gates pass. Assigning exported oxygen specifically to the water-derived species blocking active Zr–O pairs remains a harder, separate inference.


## Addendum: focal SI confirms inventory and water ppm basis

The retrieved [2025 supporting information](https://acs.figshare.com/doi/suppl/10.1021/acscatal.5c04904), public [Figshare record](https://api.figshare.com/v2/articles/30529766), was inspected from `/tmp/styrene-oxygen-review/cs5c04904_si_001.pdf` via its extracted text `/tmp/styrene-oxygen-review/si.txt`. This addendum records the source without adding or modifying literature-library entries.

- **Inventory confirmed:** SI p.6, section 1.3, gives 20 mg zirconia, 130 m²/g, 0.56 sites/nm², and 2.4 μmol LAB pairs. The calculation above therefore matches the focal study’s stated specimen basis.
- **Flow now available for the SI titration experiment:** 50 mL/min at 298 K and 101.325 kPa, reported as 0.034 mol/ks, or approximately 0.122 mol/h. Figure S4 uses 723 K, 1 kPa ethylbenzene, and 12.5 kPa H2. This flow should not be assigned automatically to the distinct main-text 773 K recovery experiment. At this SI flow, 1 ppm total gas equals approximately 0.122 μmol/h. Export of the example 0.604 μmol over 1 or 14 h would average approximately 4.94 or 0.353 ppm total gas; a 10% branch averages 0.494 or 0.0353 ppm, respectively.
- **Water basis resolved:** SI section 1.3 estimates approximately 40 ppm for as-supplied ethylbenzene and 10 ppm for dried ethylbenzene by dividing the site inventory by total gas throughput during initial deactivation. The denominator is total gas. These remain estimates from site titration and rate decay, not independent inlet-water measurements. The main text reports 43 ppm rather than 40 ppm; retain those source-specific values rather than implying analytical precision. The SI paragraph also uses 1.7 ks in its prose and 1.5 ks in its printed as-supplied-feed expression, so its displayed arithmetic should not be treated as an exact independent calibration.
- **X remains unassigned:** SI p.10, section 1.7, places X outside further transformations in the model. This is a modeling assumption, not demonstrated absence of product readsorption, oxygen exchange, or subsequent poisoning. The SI does not turn the main-text approximately 10 ppm X estimate into product identification or analytical recovery data.

These findings strengthen the inventory calculation and remove the water-ppm denominator ambiguity. They do not remove the analytical gates: calibrated product recovery, exchange and storage bounds, and independent functional-site recovery are still required.

## Addendum: simplify the first campaign by postponing isotope closure

**Yes: begin with measured, unlabeled water input/output and integrated native-product collection.** This can establish whether a consequential oxygen outlet exists and whether the analytical method can measure it before investing in whole-solid isotope accounting. It also identifies the products needed to design useful isotope-exchange controls. It does not make isotope provenance or retained oxygen irrelevant.

Use the following order:

1. **Establish the measurement floor.** Measure feed water and oxygenated impurities, paired inlet/outlet water uncertainty, and complete-train blanks in the reaction matrix. Validate collection recovery and carryover at relevant cumulative doses. Express quantification limits and blank uncertainty as oxygen atoms per experiment. Because net water consumption is the difference between two fluxes, independently accurate inlet and outlet readings can still give an imprecise difference; assess that difference directly.
2. **Collect native products while reproducing functional behavior.** Compare a characterized dry-feed baseline with one independently measured low-water condition, using matched catalyst histories, temperature, partial pressures, and flow. Record activity and integrate water, gas, and condensable oxygen outlets over successive collection windows. Avoid treating the startup transient as a sustained source. A second matched run or condition should establish whether incremental product output and functional recovery are repeatable. Track feed-derived oxygen and train memory before attributing an outlet to cleaning.
3. **Choose the next question from the result.** If a product is identified at a meaningful flux, first bound its persistence and practical exposure using the measured concentration. That can justify a small product-response or separation test even while its exact surface origin remains unresolved. If products are not identified, advance only when their summed oxygen-equivalent upper bounds address a meaningful branch; poor recovery or large blank uncertainty calls for analytical improvement, not an isotope pulse. A sustained apparent oxygen deficit calls for investigating storage or missing outlets before assigning a route.
4. **Use finite 18O for a specific unresolved provenance question.** Once products or tight bounds emerge, ask whether water oxygen reaches a particular outlet during measured site recovery. Include product-exchange, no-hydrocarbon, and apparatus controls tailored to that outlet. Quantitative bulk solid-isotope analysis becomes necessary when the intended claim requires isotope closure or distinguishing a retained/exchanged reservoir comparable to the assigned signal. A narrower demonstrated oxygen-transfer result can be useful without claiming that closure.

The first two stages can identify products, establish formation-rate bounds, reject an analytically inaccessible design, and prioritize whether a product could matter at credible exposure. They can also show that a proposed alcohol outlet is absent within a useful limit while oxygen instead exits through another measured channel. They **cannot** prove that an organic oxygen atom came from the water blocking an active pair, exclude exchange or oxygen uptake by the solid, or assign one oxygen exported per recovered pair.

At stationary inventories, net water consumption should balance the other net oxygen outlets after accounting for all oxygen inputs. Apparent stationarity of activity or effluent composition is insufficient: finite solid or train reservoirs can change slowly. Compare cumulative oxygen with plausible inventories and obtain retained-inventory evidence when it becomes consequential; do not silently set storage to zero. Conversely, a small fraction of inlet water consumed may still be sufficient to maintain working sites because unreacted water can leave. Judge the pilot by whether its measured fluxes and uncertainties resolve a useful question, not by an obligation to close every isotope reservoir in the first experiment.
