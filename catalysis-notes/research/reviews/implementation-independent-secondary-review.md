# Independent check of the implemented methane, CHA and styrene revisions

Date: 2026-09-16. Fresh review of the implemented files, independent of their revisers. No experiments, new research directions, literature discovery or knowledge-base changes were undertaken.

## Decision

**The current three studies pass this bounded implementation review. No further substantive correction was identified in the checked claims or experimental logic.** Retain methane and zirconia as lower-priority diagnostic studies and CHA as a conditional assay-transferability pilot. Their expansion gates are explicit; none currently establishes a practical improvement or warrants promotion to a substantial research program.

This conclusion covers the files and source passages below. It does not certify that every source, figure, calculation or experimental contingency in the repository has been exhausted. Several uncertainties are the intended subjects of the experiments, not errors that prose revisions can remove.

## Scope and evidence checked

Read the current [decision brief](../decision-brief.md), [methane screen](../working/wet-methane-value-screen.md), [CHA program](../programs/zeolite-durability-and-measurement.md), [styrene program](../programs/zirconia-styrene-oxygen-fate.md), their [post-upload methane audit](post-upload-methane-audit.md) and [CHA/styrene audit](post-upload-cha-styrene-audit.md), and the associated aging, steam-free-comparator and methane-application reviews. Checked the earlier-screen framing against the current recommendations.

The following checks used fresh text extraction directly from retained original PDFs, rather than relying only on knowledge-base notes:

| Primary source and checked passages | Independent finding |
|---|---|
| [Luo 2018](../../literature/papers/luo2018-nh3-tpd-methodology-for-quantifying/original.pdf), PDF pp.5–6, §3.4.2 | The same two cores receive intermediate NH3-TPD and then opposite-order additional aging. Final agreement is a meaningful cumulative-aging precedent; it does not answer assay-versus-no-assay causality. |
| [Ladshaw 2022](../../literature/papers/ladshaw2022-measurement-and-modeling-of-the/original.pdf), PDF pp.8–10 | Rates estimated from the de-greened data predict aged transients with the aging/storage model supplying changing site populations. This supports the revised requirement for prediction across assay schedules, beyond a generic population-change model. |
| [Auvinen 2021](../../literature/papers/auvinen2021-effects-of-no-and-no2/original.pdf), methods and mechanistic discussion | Pd:Pt 4:1, 7.06 g precious metal/L and 50,000 h−1 are stated. Measured NO effects and proposed HNO2/sulfur explanations remain distinct; the authors discuss uncertainty. The revised proposal preserves that distinction. |
| [Tan 2025](../../literature/papers/tan2025-a-highly-active-and-stable/original.pdf), PDF p.2, Figure 2 discussion and conclusions | The 0.3 g, 1500 ppm CH4, 5% O2, 10% water, atmospheric-pressure, 100,000 h−1 conditions and approximately 85% conversion at 330 °C over 100 h support the stated wet sulfur-free reference. They do not supply a sulfur-tolerance result. |
| [Tang 2024](../../literature/papers/tang2024-experimental-kinetics-and-reactor-modeling/original.pdf), PDF p.7 and pp.11–12 | The 10 mL/min, 2,860 Pa temperature series and 9–11 h averaging are measured-data conditions. The 0.341 kmol/(m³·h) value at 109 mL/min and 9,350 Pa is an optimization result. The revised files keep these separate. |
| [Dimian 2019](../../literature/papers/dimian2019-energy-efficient-styrene-process-design/original.pdf), PDF pp.15–16, Table 15 | The table supports about 72% hot-utility reduction, rounded to 73% in the source, about 48% annual energy-cost reduction and about 36% reduction in the stated reaction-section annualized cost. The current program does not convert these into whole-plant or zirconia savings. |

These are targeted source checks, not full independent figure digitizations or reanalyses of raw data. Other source claims retain the evidence boundaries stated in the earlier independent reviews and post-upload audits.

## Experimental logic

### Methane: a material boundary with an application gate

The first study now requires reproduction of the preparation contrast, explicit formulation/geometry, actual internal temperature, independent preparation and history repeats, and measured wet-gas delivery. Sequential bridging avoids assigning changes in methane concentration, water, sulfur and temperature to NO alone.

Sulfur-free NO responses, never-NO sulfur histories, shams and ordinary continuation constrain the causal contrast. The revised multiplicative differential-rate null is correct: a nonlinear conversion interaction alone cannot establish coupled chemistry, and an additive rate interaction tests a different assumption. Sulfur inventories do not uniquely identify the active sulfur population or pathway.

The material-ranking/output decision uses cumulative methane slip and measured precious-metal inventories. The real-application gate remains essential: the approximately 60 ppm NO engine stream has reportedly negligible sulfur, so pairing it with another study's 2 ppm SO2 does not create a demonstrated operating envelope. Zero-NO testing remains diagnostic. If a consequential real envelope is absent, the text explicitly stops at the tested material boundary.

### CHA: assay intervention separated from terminal measurement

The complete-assay, matched NH3-free sham and uninterrupted histories estimate different causal effects; the current program does not pretend their full histories are identical. It matches damaging wet exposure, records added thermal time, checks ligand removal, and commissions endpoint variation before setting repeats and minimum useful contrasts.

Pre-assay functional response and common-terminal-assay capacity remain separate. The functional probe can itself condition the catalyst; its dose dependence must be checked. Recovered tetrahedral Al or NH3 capacity is not treated as proof of framework reconnection. Luo and Ladshaw are now credited without transferring their Cu-CHA results into measured H-CHA recovery kinetics.

A held-out assay-spacing prediction or consequential ranking change is required beyond an immediate known uptake response. Null results bound benefit over the tested histories, not an unobserved intermediate lifetime. The dry-interruption and process-transfer branches remain conditional. The historical review's opening status note points readers to the current program and its later update.

### Styrene: useful net output precedes specialized oxygen attribution

The initial sequence is coherent: measured moisture/reference behavior, a small product-containing net-output gate at favorable affinity, then the water/sham × EB/no-EB recovery comparison. EB can erase a control's state during the activity assay; the current text explicitly withholds the recovery inference when an early readout cannot be validated.

Native-product identity, oxygen provenance, net oxygen balance and oxygen per active pair are different claims. The proposal does not infer one from another. Finite prelabel recovery is kept separate from sustained closed-cycle thermodynamics, and storage/exchange controls remain necessary for stronger attribution.

Tang provides a documented laboratory comparator, while low-steam Fe–K and heat-integrated process alternatives set a different practical boundary. The model optimum is not presented as measured output. More complete oxygen attribution is conditional on a consequential prediction that the simpler measured-water model cannot already provide. An unidentified peak or an unrealistic poison dose cannot pass that gate.

## Numerical consistency checks

Recomputed the following from the stated inputs; these are arithmetic checks of conditional quantities, not new experimental results:

- Ryu/Mortensen nominal gas throughput per Pd: `(200/0.01)/(126/0.03) = 4.76`. This is not a matched catalytic-performance ratio.
- Ideal adiabatic bounds with the stated heat capacity: 125.3 K at 5000 ppm methane and 25.1 K at 1000 ppm. Neither is a measured bed temperature.
- The specified one-inch-diameter/one-inch-long Ryu monolith gives 1.287 g catalyst at 100 g/L. At the stated gas reference, inlet sulfur is about 0.873 S/Pd/h, or 61.1 over 70 h. This is inlet dose, not uptake.
- The zirconia design inventory gives 2.418 μmol pairs; a quarter is 0.604 μmol oxygen only under the one-water-per-pair assumption. Twenty milligrams of ZrO2 contains about 324.6 μmol lattice oxygen. Inventory does not establish exchange rate.
- Dimian's stated entries give reductions of 72.35% in hot utility, 48.29% in annual energy cost and 36.28% in the specified annualized cost. The source's rounded 73% is adequately qualified.
- The ideal-gas styrene reaction quotient and methane multiplicative-rate null are dimensionally and algebraically consistent as written. No claim that the assumed kinetic models apply outside their validated domains follows.

## Remaining limits and required action

**No additional research-file repair is required by this review.** Maintain the current conditional scope. Instrument capability, material reproducibility, useful effect size, real application conditions and prospective prediction remain unvalidated. Numerical success thresholds should be set after commissioning, before definitive comparisons; supplying invented targets now would weaken the plans.

Current source availability is distinct from selective researcher reading. Historical handoffs are labeled as snapshots and point to the current status records. This review did not certify completion of the sole literature maintainer's separate note repairs or revalidate every package's access metadata.

The minimum experiments are sufficiently specified to support a scoped platform assessment and commissioning plan. Their expected value lies in resolving the stated uncertainties; practical superiority remains an experimental question.
