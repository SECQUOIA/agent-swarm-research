# Post-upload audit: CHA assay history and zirconia styrene

Date: 2026-09-16. Bounded reassessment of existing proposals after the literature uploads. No new research direction, external search, or experiment was started. Literature packages were read but not changed. Page numbers below refer to the local original PDFs; extracted full text was used for navigation and relevant passages were checked with independent PDF text extraction.

**Implementation status:** corrections to the two current programs, aging/styrene reviews and corresponding working screens are implemented. Dated notes preserve the earlier source-access boundaries. The Dimian KB correction is assigned separately to the sole literature maintainer; this audit did not edit literature packages. Both programs remain conditional secondary studies.

## Decision

**Update the evidence and comparator sections; retain both programs as conditional secondary studies.** The uploads strengthen several existing cautions. They do not establish an assay-induced change in subsequent H-CHA damage or resolve the oxygen products of zirconia cleaning. They also do not justify raising either program's practical priority.

The largest substantive changes are:

1. Credit the experimentally tested cumulative-aging null in Luo 2018, including the fact that both sequences contain intermediate NH3-TPD. It does not answer the proposed assay-versus-no-assay question.
2. Replace the incomplete Tang comparator assessment with its now-available methods and distinguish measured dilute-feed conversion from its simulated production optimum.
3. Use the process studies to sharpen the practical styrene comparison. In particular, distinguish reduced hot-utility demand, total energy cost, and reaction-section annualized cost in Dimian 2019.

## 1. CHA: stronger prior art, same narrow causal question

### Luo provides a tested null, with a specific treatment history

The uploaded [Luo original PDF](../../literature/papers/luo2018-nh3-tpd-methodology-for-quantifying/original.pdf), pp.5–6, Section 3.4.2 and Figure 7, compares two Cu/SSZ-13 cores aged first at 700 °C for 2 h or 600 °C for 24 h. They are measured by NH3-TPD and **the same cores** then undergo the other aging treatment. Final TPD ratios and catalytic functions, including NH3 oxidation, remain similar. The material and aging gas are specified on p.2: commercial Cu/SSZ-13, Si/Al approximately 9.5, Cu/Al 0.3, and 10% O2/8% CO2/7% H2O in N2.

This is meaningful negative prior art against a general claim that reversing thermal aging order necessarily changes durability. It is stronger than an abstract-level warning. However, both arms have an intermediate assay, so it does **not** test whether that assay changes subsequent aging relative to uninterrupted or sham-treated specimens. The paper addresses mild Cu-site redistribution; its pp.2 and 7 explicitly distinguish that regime from severe dealumination. It therefore cannot directly validate an irreversible-loss model for the isolated-Al H-CHA proposal.

**Recommended edit:** update the source tier in [the original zeolite screen](../working/zeolite-screen.md) and [independent review](aging-independent-review.md), and add this exact distinction to the [current program](../programs/zeolite-durability-and-measurement.md). Keep the A/B/C comparison. Do not call Luo a direct null result for the proposed NH3 intervention or imply that its order-independence test used unassayed specimens.

### Ladshaw strengthens the predictive benchmark, not the intervention claim

The [Ladshaw original PDF](../../literature/papers/ladshaw2022-measurement-and-modeling-of-the/original.pdf), pp.2–3 and 8–10, gives a storage/aging/transient model for commercial Cu-SSZ-13. Kinetic parameters fitted to de-greened transients are retained when predicting aged transients, while age-dependent site densities are supplied by the aging/storage analysis. Figure 8 covers 4 h aging and Figure 9 covers 16 h. This is evidence that a relatively compact model with fixed adsorption kinetics and changing site populations can explain useful aged responses.

**Recommended edit:** explicitly credit this prior predictive work when describing the proposed model contribution. The new contribution must remain **prediction across different assay schedules and its consequences for useful function**, beyond an ordinary population-change model. Do not suggest that fitting a state model to aged NH3 storage is itself new. Conversely, Ladshaw's predictions are not evidence that an NH3 assay leaves future aging unchanged, and the fitted site densities are not independent atomic inventories.

### Coordination and cooling controls are now supported by full texts

The current program's sentence that Wouters and Agostini remain pending full reading is obsolete. The new documents reinforce controls already present rather than overturning the proposal:

| Source | Verified evidence | Consequence |
|---|---|---|
| [Wouters 1998](../../literature/papers/wouters1998-reversible-tetrahedraloctahedral-framework-aluminum-transformation/original.pdf), p.7 | Hydration can partially hydrolyze Y-zeolite framework Al; ammonia changes some hydrated Al from sixfold to tetrahedral coordination. The authors distinguish partially hydrolyzed framework-related species from completely removed Al. | A recovered tetrahedral signal does not demonstrate restored framework connectivity or durable recovery. |
| [Wouters 2001](../../literature/papers/wouters2001-steaming-of-zeolite-y-formation/original.pdf), p.5 | Framework-related Al–OH and octahedral Al signals are observed at low steam pressure, whereas the transient framework-related species is absent at higher steam pressure. | Observation of an intermediate or NH3-induced coordination change alone is established prior art. Absence of its signal does not supply its lifetime. |
| [Agostini 2010](../../literature/papers/agostini2010-in-situ-xas-and-xrpd/original.pdf), p.11 | Under the tested NH4-Y sequence, less than 10% of Al leaves the framework on heating to 873 K; the extraframework fraction rises to roughly 35% during cooling around 500–450 K as water returns. | Cooling and hydration are potentially active parts of the intervention. The matched thermal/water sham and controlled transfer remain essential. Do not transfer the numerical fractions to CHA. |
| [Nielsen 2015](../../literature/papers/nielsen2015-kinetics-of-zeolite-dealumination-insights/original.pdf), p.8 | The H-SSZ-13 model places increasing rate control on the final hydrolysis at high temperature; empirical water-reference corrections improve comparison with **H-ZSM-5** experimental data. Direct experimental validation in H-SSZ-13 was still requested. | Label this a computational alternative with a cross-framework experimental comparison, not measured H-CHA recovery kinetics. It supplies no demonstrated usable dry-interruption window. |

Nielsen 2015 should also be read alongside the already available Nielsen 2019 cooperative-water calculation. Neither justifies one universally established rate-controlling hydrolysis step across water loadings and material states.

**Priority effect:** confidence that these are necessary controls increases. Confidence in the proposed persistent assay effect remains moderate and unvalidated; informative comparison remains feasible in principle. Confidence in a useful regeneration improvement stays low. No additional characterization campaign is warranted before the existing causal gate succeeds.

## 2. Styrene: replace the missing-methods discussion with a bounded comparator

### Tang's main article resolves several major access gaps

The [Tang original PDF](../../literature/papers/tang2024-experimental-kinetics-and-reactor-modeling/original.pdf) is now local and read. The [earlier comparator review](styrene-steam-free-benchmark.md) and the current program's practical-benchmark paragraphs need an update:

- **PDF p.3, Sections 2.1–2.3:** catalyst preparation is given. The quartz reactor has 8 mm internal diameter and a 74 mm packed height. Nitrogen carries ethylbenzene from a temperature-controlled saturator; aromatics are collected in 10 mL ethanol cooled with ice water and analyzed by GC. Thus feed preparation, carrier, bed geometry and sampled product phase are no longer wholly unknown.
- **PDF p.7, Section 4.1:** the temperature series uses 10 mL/min flow and 2,860 Pa inlet ethylbenzene. The authors average the 9–11 h values following an approximately 8 h induction period. The pressure series at 873.15 K and the same stated flow spans 2,860–14,332.4 Pa ethylbenzene. Reported conversion falls from approximately 80% to 30%, while styrene selectivity falls from about 97.5% to 94.9%.
- **PDF p.10, Equation 37, and pp.11–12:** the production measure uses the cylindrical packed volume, and **0.341 kmol/(m³·h) at 109 mL/min and 9,350 Pa ethylbenzene is a model optimization result**. It is not a directly measured output at that optimized condition. The principal measurements used 10 mL/min.

The main text explains why the SI's four aromatic fractions cannot be used as total gas composition: the experimental sampling collects aromatics, with nitrogen and hydrogen absent from those four reported fractions. This strengthens the old warning; it does not supply a complete gas-phase carbon/hydrogen balance.

Several comparison limits remain. The inspected methods do not give a measured ppm water specification or an experimentally established trace-water tolerance. Catalyst deactivation is omitted from the model (p.4); the 9–11 h averaging and a cited earlier study's longer run are not a repeated-regeneration demonstration for this experiment. The numeric total-pressure/flow-reference and directly weighed catalyst-inventory basis still need care before reconstructing matched intrinsic rates. The model's packing density is not a substitute for a reported weighing record.

**Recommended edit:** retire the statement that all methods must first be retrieved. Treat Tang as a documented steam-free laboratory comparator with defined dilute ethylbenzene conditions and a short working-state interval. Keep its optimized volume productivity separate from measurements and retain the zirconia product-cofeed/net-output gate. The evidence narrows any broad steam-free novelty claim but does not identify zirconia's cleaning products or establish which catalyst wins under matched conditions.

### Process value requires a stronger comparison than removing steam

[Luyben's original PDF](../../literature/papers/luyben2010-design-and-control-of-the/original.pdf), p.16, explicitly shows a simulated tradeoff where **more** steam, larger reactors and more recycle improve yield and reduce operating cost under that study's assumptions. This validates the current proposal's caution about steam-free operation. It supplies a concrete reason to count selectivity, raw-material losses and recycle together with heating duty. The old process economics are not current plant quotes.

[Dimian and Bildea's original PDF](../../literature/papers/dimian2019-energy-efficient-styrene-process-design/original.pdf), pp.15–16, Tables 14–15, supports a substantial heat-integration alternative within a steam-diluted process. Its percentages need precise boundaries:

| Quantity in Table 15 | Base case → MVR case | Correct interpretation |
|---|---|---|
| Hot utility | 42.5 → 11.75 MW | Approximately 72% reduction, rounded in the paper to 73%. |
| Annual energy cost, including compressor and steam credit | 11.08 → 5.73 M$/y | Approximately 48% reduction; **not 73%**. |
| Installed equipment cost in this comparison | 7.85 → 9.00 M$ | Approximately 15% increase. |
| Total annualized cost in this comparison | 13.70 → 8.73 M$/y | Approximately 36% reduction for the reaction-section energy/equipment comparison; the paper discusses separation costs separately. |

Page 15 contains a loose sentence assigning 73% to energy cost, whereas its table and p.16 give the consistent 48% total-energy-cost figure. Prefer the explicit table boundary. The current KB summary's unqualified “utility consumption” and “total annualized cost” wording should be clarified to prevent a future claim of a 73% total-energy saving or a 36% whole-plant cost reduction. This is a small **substantive KB correction**, not merely an access-status update; route it through the sole literature maintainer.

**Priority effect:** these sources strengthen the requirement to compare zirconia with an appropriately integrated low-steam process and a documented steam-free laboratory catalyst. They do not demonstrate an energy or lifetime advantage for zirconia. Retain low confidence in practical improvement until useful net output and chemical consequences pass the existing staged tests.

## Implemented research-file changes and separate KB handoff

1. Updated both current program files with the source distinctions above and linked this audit.
2. Added dated source-access notes to the aging and initial styrene reviews; rewrote the Tang comparator around the now-read main article while recording the original abstract/SI-only assessment.
3. Updated the practical-selection and zeolite working screens, and labeled original retrieval handoffs as historical. The zeolite screen now directs the first experiment to assay carryover and avoids inferring an intermediate lifetime from a null schedule effect.
4. Handed the Dimian KB summary correction to the parent for the sole literature maintainer. No new source is required for these findings.
5. Retained conditional, secondary status, existing causal controls and staged stop criteria, and distinct hypothesis/feasibility/practical-value confidence judgments. The uploads justify better grounded controls and comparisons; they do not justify larger experimental scope.

**Verification:** checked the material claims against original PDF passages cited above; `git diff --check` passed for the seven edited existing research files. A local-link check covered 76 links across those files and this audit, with no missing file targets. No calculation changed and no experimental result was generated.
